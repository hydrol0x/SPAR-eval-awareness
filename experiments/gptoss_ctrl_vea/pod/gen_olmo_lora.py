"""vLLM generation / teacher-forced log-probs for Olmo-3.1-32B-Think with an optional CoT-controllability LoRA
(PREREG_exp1.md). Attention/MLP LoRA via vLLM's LoRA support; the lm_head LoRA added to the logits in float32 by a hook.
System-prompt cues (item["system_append"]) are inserted after Olmo's default system prompt in the stock rendering.

  python pod/gen_olmo_lora.py gen --model /workspace/models/base --name edited --lora /workspace/lora_prep/edited \
      --prompts data/exp1_prompts.jsonl --out rollouts/olmo31_exp1_edited/exp1.jsonl
  python pod/gen_olmo_lora.py logprobs --model ... --lora ... --items val.jsonl --out results/exp1_val_vllm.json
"""
from __future__ import annotations
import argparse, hashlib, json, os, sys, time
from pathlib import Path

os.environ.setdefault("VLLM_ALLOW_INSECURE_SERIALIZATION", "1")  # apply_model ships the hook to the worker
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src.prompts import OLMO_DEFAULT_SYSTEM  # noqa: E402


def render(tok, it):
    msgs = ([{"role": "system", "content": it["system"]}] if it.get("system") else []) + [{"role": "user", "content": it["user"]}]
    p = tok.apply_chat_template(msgs, add_generation_prompt=True, tokenize=False)
    if it.get("system_append"):
        old = OLMO_DEFAULT_SYSTEM + "<|im_end|>"
        assert p.count(old) == 1, "default system prompt not found exactly once"
        p = p.replace(old, OLMO_DEFAULT_SYSTEM + "\n\n" + it["system_append"] + "<|im_end|>")
    return p


def parse(text):
    """The template opens <think> in the prompt, so the completion is reasoning, </think>, answer."""
    if "</think>" in text:
        a, b = text.split("</think>", 1)
        return a.strip(), b.strip()
    return text.strip(), ""


def lm_head_hook(path):
    def install(model):
        import types, torch
        from safetensors import safe_open
        with safe_open(path, "pt") as f:
            A, B, scale = f.get_tensor("A"), f.get_tensor("B"), float(f.metadata().get("scale", "1.0"))
        dev = next(model.parameters()).device
        A, B = A.to(dev, torch.float32), B.to(dev, torch.float32)
        orig = model.compute_logits

        def compute_logits(self, hidden_states, *args, **kw):
            logits = orig(hidden_states, *args, **kw)
            if logits is None or not getattr(self, "_lm_lora_on", True):
                return logits
            delta = (hidden_states.float() @ A.t()) @ B.t() * scale
            out = logits.float()
            n = min(out.shape[-1], delta.shape[-1])
            out[..., :n] += delta[..., :n]
            return out
        model.compute_logits = types.MethodType(compute_logits, model)
        model._lm_lora_on = True
        return f"lm_head hook on {type(model).__name__}, A {tuple(A.shape)} B {tuple(B.shape)} scale {scale}"
    return install


def make_llm(a):
    from vllm import LLM
    kw = dict(model=a.model, dtype="bfloat16", max_model_len=a.max_len, gpu_memory_utilization=0.92, seed=0,
              enable_prefix_caching=True, tensor_parallel_size=a.tp)
    if a.lora:
        kw.update(enable_lora=True, max_lora_rank=32, max_loras=1)
    llm = LLM(**kw)
    lreq = None
    if a.lora:
        from vllm.lora.request import LoRARequest
        lreq = LoRARequest(Path(a.lora).name, 1, a.lora)
        print(llm.apply_model(lm_head_hook(str(Path(a.lora) / "lm_head_lora.safetensors"))), flush=True)
    return llm, lreq


def set_head(llm, on):
    llm.apply_model(lambda m: setattr(m, "_lm_lora_on", on))


def cmd_logprobs(a):
    from vllm import SamplingParams
    llm, lreq = make_llm(a); tok = llm.get_tokenizer()
    items = [json.loads(l) for l in open(a.items) if l.strip()]
    res = {}
    for tag, req in (("base", None), ("lora", lreq)):
        if a.lora:
            set_head(llm, req is not None and not a.no_head)
        prompts, spans = [], []
        for it in items:
            p = tok(it["prompt_text"], add_special_tokens=False).input_ids; c = tok(it["completion_text"], add_special_tokens=False).input_ids
            prompts.append({"prompt_token_ids": p + c}); spans.append((len(p), p + c))
        outs = llm.generate(prompts, SamplingParams(max_tokens=1, prompt_logprobs=0, temperature=0.0), lora_request=req, use_tqdm=False)
        res[tag] = {it["id"]: [o.prompt_logprobs[j][ids[j]].logprob for j in range(s, len(ids))] for it, o, (s, ids) in zip(items, outs, spans)}
        if not a.lora:
            break
    Path(a.out).parent.mkdir(parents=True, exist_ok=True); Path(a.out).write_text(json.dumps(res))
    print(f"logprobs written: {a.out}", flush=True)


def cmd_gen(a):
    from vllm import SamplingParams
    out = Path(a.out); out.parent.mkdir(parents=True, exist_ok=True)
    items = [json.loads(l) for l in open(a.prompts) if l.strip()]
    if a.only_set:
        items = [it for it in items if it["set"] == a.only_set]
    done = {json.loads(l)["rollout_id"] for l in out.open()} if out.exists() else set()
    todo = []
    for it in items:
        for s in range(a.sample_offset, a.sample_offset + a.n_samples):
            rid = hashlib.sha1(f"{a.name}||{it['set']}||{it['item_id']}||{it['condition']}||{s}".encode()).hexdigest()[:16]
            if rid not in done:
                todo.append((it, s, rid))
    print(f"[{a.name}] {len(todo)} to generate ({len(done)} done)", flush=True)
    if not todo:
        return
    llm, lreq = make_llm(a); tok = llm.get_tokenizer(); t0 = time.time()
    for i in range(0, len(todo), a.chunk):
        chunk = todo[i:i + a.chunk]
        prompts = [render(tok, it) for it, _, _ in chunk]
        params = [SamplingParams(temperature=a.temperature, top_p=a.top_p, max_tokens=a.max_tokens,
                                 seed=int(hashlib.sha1(f"{it['set']}|{it['item_id']}|{it['condition']}|{s}".encode()).hexdigest()[:8], 16))
                  for it, s, _ in chunk]
        outs = llm.generate(prompts, params, lora_request=lreq, use_tqdm=False)
        with out.open("a") as fh:
            for (it, s, rid), p, o in zip(chunk, prompts, outs):
                c = o.outputs[0]; ana, fin = parse(c.text)
                fh.write(json.dumps({"rollout_id": rid, "model": a.name, "set": it["set"], "item_id": it["item_id"], "condition": it["condition"],
                                     "sample": s, "system_append": it.get("system_append"), "user": it["user"], "meta": it.get("meta", {}),
                                     "reasoning": ana, "response": fin, "raw": c.text, "finish_reason": c.finish_reason,
                                     "n_tokens": len(c.token_ids), "prompt_sha": hashlib.sha1(p.encode()).hexdigest()[:12],
                                     "temperature": a.temperature, "top_p": a.top_p, "max_tokens": a.max_tokens}) + "\n")
        print(f"[{a.name}] {i + len(chunk)}/{len(todo)} ({time.time() - t0:.0f}s)", flush=True)


def main():
    ap = argparse.ArgumentParser(); sub = ap.add_subparsers(dest="cmd", required=True)
    for name in ("gen", "logprobs"):
        p = sub.add_parser(name)
        p.add_argument("--model", required=True); p.add_argument("--lora", default=None); p.add_argument("--tp", type=int, default=1)
        p.add_argument("--max-len", type=int, default=18432); p.add_argument("--out", required=True)
    g = sub.choices["gen"]
    g.add_argument("--name", required=True); g.add_argument("--prompts", required=True); g.add_argument("--only-set", default=None)
    g.add_argument("--n-samples", type=int, default=2); g.add_argument("--sample-offset", type=int, default=0)
    g.add_argument("--temperature", type=float, default=0.6); g.add_argument("--top-p", type=float, default=0.95)
    g.add_argument("--max-tokens", type=int, default=16384); g.add_argument("--chunk", type=int, default=100000)
    sub.choices["logprobs"].add_argument("--items", required=True)
    sub.choices["logprobs"].add_argument("--no-head", action="store_true", help="leave the lm_head LoRA off (sensitivity check)")
    a = ap.parse_args()
    cmd_gen(a) if a.cmd == "gen" else cmd_logprobs(a)


if __name__ == "__main__":
    main()

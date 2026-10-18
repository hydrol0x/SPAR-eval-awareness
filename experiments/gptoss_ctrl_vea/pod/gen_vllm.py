"""vLLM generation and scoring for gpt-oss-20b (bf16 base or merged adapter), harmony format.

  # mean NLL of the adapter's own SFT targets (used to pick the w1/w3 gate mapping)
  python pod/gen_vllm.py nll --model /workspace/models/cdel_w1gate --sft /workspace/adapters/sft_edited_reasoning_full.jsonl --n 64
  # rollouts
  python pod/gen_vllm.py gen --model /workspace/models/base --name base --prompts data/main_prompts.jsonl --n-samples 2 --out rollouts/base/main.jsonl
"""
from __future__ import annotations
import argparse, hashlib, json, re, sys, time
from pathlib import Path

EFFORT = "medium"
STOP_IDS = [200002, 200012]  # <|return|>, <|call|>


def render(tok, system, user):
    msgs = ([{"role": "system", "content": system}] if system else []) + [{"role": "user", "content": user}]
    return tok.apply_chat_template(msgs, add_generation_prompt=True, tokenize=False, reasoning_effort=EFFORT)


def parse(text: str):
    """Split harmony output into (analysis, final)."""
    ana = re.search(r"<\|channel\|>analysis<\|message\|>(.*?)(?:<\|end\|>|$)", text, re.S)
    fin = re.search(r"<\|channel\|>final<\|message\|>(.*?)(?:<\|return\|>|<\|end\|>|$)", text, re.S)
    analysis = ana.group(1) if ana else ""
    final = fin.group(1) if fin else ("" if ana else text)
    return analysis.strip(), final.strip()


def make_llm(model, max_len):
    from vllm import LLM
    return LLM(model=model, dtype="bfloat16", max_model_len=max_len, gpu_memory_utilization=0.92,
               max_num_seqs=256, seed=0, enable_prefix_caching=True)


def cmd_nll(a):
    from vllm import SamplingParams
    rows = [json.loads(l) for l in open(a.sft) if l.strip()][: a.n]
    llm = make_llm(a.model, 8192); tok = llm.get_tokenizer()
    texts, spans = [], []
    for r in rows:
        prompt = render(tok, None, r["prompt_user_content"])
        comp = (f"<|channel|>analysis<|message|>{r['target_analysis']}<|end|><|start|>assistant"
                f"<|channel|>final<|message|>{r['target_final']}<|return|>")
        n_p = len(tok(prompt, add_special_tokens=False).input_ids)
        texts.append(prompt + comp); spans.append(n_p)
    outs = llm.generate([{"prompt_token_ids": tok(t, add_special_tokens=False).input_ids} for t in texts],
                        SamplingParams(max_tokens=1, prompt_logprobs=0, temperature=0.0))
    tot, n = 0.0, 0
    for o, s in zip(outs, spans):
        ids = o.prompt_token_ids
        for j in range(s, len(ids)):
            lp = o.prompt_logprobs[j]
            if lp is None:
                continue
            tot -= lp[ids[j]].logprob; n += 1
    res = {"model": a.model, "sft": a.sft, "n_examples": len(rows), "n_tokens": n, "mean_nll": tot / max(n, 1)}
    print("NLL_RESULT " + json.dumps(res), flush=True)
    if a.out:
        Path(a.out).parent.mkdir(parents=True, exist_ok=True)
        with open(a.out, "a") as fh:
            fh.write(json.dumps(res) + "\n")


def cmd_gen(a):
    from vllm import SamplingParams
    out = Path(a.out); out.parent.mkdir(parents=True, exist_ok=True)
    items = [json.loads(l) for l in open(a.prompts) if l.strip()]
    done = set()
    if out.exists():
        for l in out.open():
            try:
                done.add(json.loads(l)["rollout_id"])
            except Exception:
                pass
    llm = make_llm(a.model, a.max_len); tok = llm.get_tokenizer()
    todo = []
    for it in items:
        for s in range(a.sample_offset, a.sample_offset + a.n_samples):
            rid = hashlib.sha1(f"{a.name}||{it['set']}||{it['item_id']}||{it['condition']}||{s}".encode()).hexdigest()[:16]
            if rid not in done:
                todo.append((it, s, rid))
    print(f"[{a.name}] {len(todo)} to generate ({len(done)} done)", flush=True)
    t0 = time.time()
    for i in range(0, len(todo), a.chunk):
        chunk = todo[i:i + a.chunk]
        prompts, params = [], []
        for it, s, rid in chunk:
            prompts.append(render(tok, it.get("system"), it["user"]))
            seed = int(hashlib.sha1(f"{it['set']}|{it['item_id']}|{it['condition']}|{s}".encode()).hexdigest()[:8], 16)
            params.append(SamplingParams(temperature=a.temperature, max_tokens=a.max_tokens, seed=seed,
                                         skip_special_tokens=False, stop_token_ids=STOP_IDS))
        outs = llm.generate(prompts, params, use_tqdm=False)
        with out.open("a") as fh:
            for (it, s, rid), o in zip(chunk, outs):
                c = o.outputs[0]
                ana, fin = parse(c.text)
                fh.write(json.dumps({"rollout_id": rid, "model": a.name, "set": it["set"], "item_id": it["item_id"],
                                     "condition": it["condition"], "sample": s, "system": it.get("system"),
                                     "user": it["user"], "meta": it.get("meta", {}), "split": it.get("split"),
                                     "reasoning": ana, "response": fin, "raw": c.text,
                                     "finish_reason": c.finish_reason, "n_tokens": len(c.token_ids),
                                     "temperature": a.temperature, "max_tokens": a.max_tokens, "effort": EFFORT}) + "\n")
        print(f"[{a.name}] {i + len(chunk)}/{len(todo)} ({time.time() - t0:.0f}s)", flush=True)


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    n = sub.add_parser("nll"); n.add_argument("--model", required=True); n.add_argument("--sft", required=True)
    n.add_argument("--n", type=int, default=64); n.add_argument("--out")
    g = sub.add_parser("gen"); g.add_argument("--model", required=True); g.add_argument("--name", required=True)
    g.add_argument("--prompts", required=True); g.add_argument("--out", required=True)
    g.add_argument("--n-samples", type=int, default=2); g.add_argument("--temperature", type=float, default=1.0)
    g.add_argument("--max-tokens", type=int, default=4096); g.add_argument("--max-len", type=int, default=12288)
    g.add_argument("--chunk", type=int, default=512)
    g.add_argument("--sample-offset", type=int, default=0, help="first sample index (new seeds for a rerun)")
    a = ap.parse_args()
    cmd_nll(a) if a.cmd == "nll" else cmd_gen(a)


if __name__ == "__main__":
    main()

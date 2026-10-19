"""vLLM generation for the base-model screen (SCREEN_PLAN.md): open reasoning models that write <think>...</think>.

  python pod/gen_screen.py --model /workspace/models/qwq --name screen_qwq_32b --prompts data/screen_prompts.jsonl \
      --out rollouts/screen_qwq_32b/screen.jsonl --top-k 40
"""
from __future__ import annotations
import argparse, hashlib, json, re, time
from pathlib import Path


def render(tok, system, user):
    msgs = ([{"role": "system", "content": system}] if system else []) + [{"role": "user", "content": user}]
    return tok.apply_chat_template(msgs, add_generation_prompt=True, tokenize=False)


def parse(prompt: str, text: str):
    """Split into (reasoning, final). The template may already open <think> in the prompt."""
    full = ("<think>" if prompt.rstrip().endswith("<think>") else "") + text
    m = re.search(r"<think>(.*?)</think>(.*)", full, re.S)
    if m:
        return m.group(1).strip(), m.group(2).strip()
    if "<think>" in full:  # truncated inside the reasoning
        return full.split("<think>", 1)[1].strip(), ""
    return "", text.strip()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", required=True); ap.add_argument("--name", required=True)
    ap.add_argument("--prompts", required=True); ap.add_argument("--out", required=True)
    ap.add_argument("--n-samples", type=int, default=1); ap.add_argument("--sample-offset", type=int, default=0)
    ap.add_argument("--temperature", type=float, default=0.6); ap.add_argument("--top-p", type=float, default=0.95)
    ap.add_argument("--top-k", type=int, default=-1)
    ap.add_argument("--max-tokens", type=int, default=8192); ap.add_argument("--max-len", type=int, default=12288)
    ap.add_argument("--chunk", type=int, default=4096, help="prompts per generate() call; large keeps the batch full")
    ap.add_argument("--tp", type=int, default=1, help="tensor-parallel GPUs")
    a = ap.parse_args()
    from vllm import LLM, SamplingParams
    out = Path(a.out); out.parent.mkdir(parents=True, exist_ok=True)
    items = [json.loads(l) for l in open(a.prompts) if l.strip()]
    done = {json.loads(l)["rollout_id"] for l in out.open()} if out.exists() else set()
    todo = []
    for it in items:
        for s in range(a.sample_offset, a.sample_offset + a.n_samples):
            rid = hashlib.sha1(f"{a.name}||{it['set']}||{it['item_id']}||{it['condition']}||{s}".encode()).hexdigest()[:16]
            if rid not in done:
                todo.append((it, s, rid))
    print(f"[{a.name}] {len(todo)} to generate ({len(done)} done)", flush=True)
    llm = LLM(model=a.model, dtype="bfloat16", max_model_len=a.max_len, gpu_memory_utilization=0.92, seed=0,
              enable_prefix_caching=True, tensor_parallel_size=a.tp)
    tok = llm.get_tokenizer(); t0 = time.time()
    for i in range(0, len(todo), a.chunk):
        chunk = todo[i:i + a.chunk]
        prompts = [render(tok, it.get("system"), it["user"]) for it, _, _ in chunk]
        params = [SamplingParams(temperature=a.temperature, top_p=a.top_p, top_k=a.top_k, max_tokens=a.max_tokens,
                                 seed=int(hashlib.sha1(f"{it['set']}|{it['item_id']}|{it['condition']}|{s}".encode()).hexdigest()[:8], 16))
                  for it, s, _ in chunk]
        outs = llm.generate(prompts, params, use_tqdm=False)
        with out.open("a") as fh:
            for (it, s, rid), p, o in zip(chunk, prompts, outs):
                c = o.outputs[0]; ana, fin = parse(p, c.text)
                fh.write(json.dumps({"rollout_id": rid, "model": a.name, "set": it["set"], "item_id": it["item_id"],
                                     "condition": it["condition"], "sample": s, "system": it.get("system"), "user": it["user"],
                                     "meta": it.get("meta", {}), "reasoning": ana, "response": fin, "raw": c.text,
                                     "finish_reason": c.finish_reason, "n_tokens": len(c.token_ids),
                                     "temperature": a.temperature, "top_p": a.top_p, "top_k": a.top_k, "max_tokens": a.max_tokens}) + "\n")
        print(f"[{a.name}] {i + len(chunk)}/{len(todo)} ({time.time() - t0:.0f}s)", flush=True)


if __name__ == "__main__":
    main()

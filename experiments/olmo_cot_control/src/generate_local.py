"""Generate CoT-controllability rollouts for one HF repo@revision with vLLM (or transformers).

Example (on the GPU box):
  python -m src.generate_local --repo allenai/Olmo-3-7B-RL-Zero-IF --revision step_1900 \
      --dataset data/mmlu_pro_mini_w_keyword.csv --n-questions 150 \
      --constraints baseline,word_suppression,tag_start,lowercase \
      --answer-if lowercase,add_suspicious --out-dir rollouts

Writes rollouts/<repo>/<revision>.jsonl, one record per rollout, already graded programmatically.
"""
from __future__ import annotations
import argparse, gc, hashlib, json, os, re, sys, time
from pathlib import Path
from typing import Any, Dict, List

from .data import load_questions
from .prompts import build_cot_prompt, build_answer_if_prompt, COT_CONSTRAINTS, ANSWER_IF_CONSTRAINTS
from . import grading as G


def parse_step(revision: str) -> int:
    m = re.search(r"(\d+)", revision or "")
    return int(m.group(1)) if m else -1


def chat_mode_for(repo: str, mode: str, tokenizer=None) -> bool:
    """auto: use the chat template whenever the checkpoint ships one (Olmo RL-Zero and Think repos
    include chat_template.jinja; the raw Olmo-3 base model does not). With the raw prompt the RL-Zero
    models emit EOS almost immediately (mean ~10 tokens), so raw is only right for base models."""
    if mode == "chat":
        return True
    if mode == "raw":
        return False
    r = repo.lower()
    if "rl-zero" in r or "rlzero" in r:
        return False  # ships a chat template but reasons only under the raw prompt (IF collapses to "Answer: X" under the template)
    return bool(getattr(tokenizer, "chat_template", None))


def build_jobs(questions, constraints, answer_if) -> List[Dict[str, Any]]:
    jobs = []
    for q in questions:
        for c in constraints:
            jobs.append({**q, "task": "cot", "constraint": c,
                         "prompt": build_cot_prompt(q["question"], q["options"], c, q["keyword"])})
        for c in answer_if:
            jobs.append({**q, "task": "answer_if", "constraint": c,
                         "prompt": build_answer_if_prompt(q["question"], q["options"], c)})
    return jobs


def resolve_model_path(repo: str, revision: str) -> str:
    """Return a loadable model path. Some Olmo-3 RL-Zero repos (e.g. Mix) carry a legacy
    `olmo2-retrofit` model_type that transformers 5 cannot load; the config is otherwise identical to
    `olmo3`, so we download a local snapshot and rewrite config.json."""
    import json, tempfile
    from huggingface_hub import hf_hub_download, snapshot_download
    cfg = json.load(open(hf_hub_download(repo, "config.json", revision=revision)))
    if cfg.get("model_type") == "olmo3" or "Olmo3ForCausalLM" in cfg.get("architectures", []):
        return repo
    print(f"[gen] patching legacy config model_type={cfg.get('model_type')} -> olmo3", flush=True)
    local = snapshot_download(repo, revision=revision, local_dir=os.path.join(tempfile.gettempdir(), "patched_" + repo.replace("/", "__") + "_" + revision))
    cfg["model_type"] = "olmo3"; cfg["architectures"] = ["Olmo3ForCausalLM"]
    cfg.setdefault("dtype", cfg.get("torch_dtype", "bfloat16"))
    json.dump(cfg, open(os.path.join(local, "config.json"), "w"), indent=2)
    return local


def render(prompt: str, tokenizer, chat: bool) -> str:
    if not chat:
        # RL-Zero / base models: raw prompt, no template (as in CoT-Control App. E). A trailing blank
        # line is essential: without it the RL-Zero models emit EOS immediately (probe 2026-10-17).
        return prompt + "\n\n"
    return tokenizer.apply_chat_template([{"role": "user", "content": prompt}], tokenize=False, add_generation_prompt=True)


def postprocess(job: Dict[str, Any], text: str, chat: bool, finish: str, ntok: int) -> Dict[str, Any]:
    if chat:
        reasoning, rest = G.split_think(text)
        if not reasoning:  # no think tags: treat pre-answer text as reasoning
            reasoning, answer = G.split_reasoning_answer(rest)
            response = rest
        else:
            _, answer = G.split_reasoning_answer(rest)
            response = rest
    else:
        reasoning, answer = G.split_reasoning_answer(text)
        response = text[len(reasoning):].strip() if answer is not None else ""
    rec = {**job, "completion": text, "reasoning": reasoning, "response": response, "answer": answer,
           "finish_reason": finish, "completion_tokens": ntok}
    if job["task"] == "cot":
        rec["compliant"] = G.grade(job["constraint"], reasoning, job["keyword"])
        rec["mentions_constraint"] = G.mentions_constraint(reasoning, job["constraint"], job["keyword"])
        rec["correct"] = G.answer_correct(answer, job["gold"], job["options"])
    else:
        rec["compliant"] = None  # LLM-judged later (judge_vea.py --answer-if)
        rec["correct"] = None
    return rec


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True)
    ap.add_argument("--revision", default="main")
    ap.add_argument("--dataset", default="data/mmlu_pro_mini_w_keyword.csv")
    ap.add_argument("--n-questions", type=int, default=100)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--constraints", default="baseline,word_suppression,tag_start,lowercase")
    ap.add_argument("--answer-if", default="lowercase")
    ap.add_argument("--mode", choices=["auto", "raw", "chat"], default="auto")
    ap.add_argument("--backend", choices=["vllm", "hf"], default="vllm")
    ap.add_argument("--max-new-tokens", type=int, default=1024, help="1024 keeps a 7B checkpoint at ~15 min on an A40; Magistral runs in the paper used 500")
    ap.add_argument("--max-model-len", type=int, default=3072)
    ap.add_argument("--temperature", type=float, default=0.0)
    ap.add_argument("--gpu-mem-util", type=float, default=0.92)
    ap.add_argument("--model-impl", default="auto", help="vllm model_impl: auto|vllm|transformers")
    ap.add_argument("--max-num-seqs", type=int, default=256)
    ap.add_argument("--dtype", default="bfloat16")
    ap.add_argument("--out-dir", default="rollouts")
    ap.add_argument("--limit-jobs", type=int, default=None, help="debug: only first N jobs")
    ap.add_argument("--purge-cache", action="store_true", help="delete the HF snapshot for this revision afterwards")
    args = ap.parse_args()

    out = Path(args.out_dir) / args.repo.replace("/", "__") / f"{args.revision}.jsonl"
    if out.exists() and out.stat().st_size > 0:
        print(f"[skip] {out} exists"); return
    out.parent.mkdir(parents=True, exist_ok=True)

    questions = load_questions(Path(args.dataset), args.n_questions, args.seed)
    constraints = [c for c in args.constraints.split(",") if c]
    answer_if = [c for c in args.answer_if.split(",") if c]
    for c in constraints: assert c in COT_CONSTRAINTS, c
    for c in answer_if: assert c in ANSWER_IF_CONSTRAINTS, c
    jobs = build_jobs(questions, constraints, answer_if)
    if args.limit_jobs: jobs = jobs[: args.limit_jobs]
    from transformers import AutoTokenizer
    model_path = resolve_model_path(args.repo, args.revision)
    local_patched = model_path != args.repo
    tok = AutoTokenizer.from_pretrained(model_path, revision=None if local_patched else args.revision)
    chat = chat_mode_for(args.repo, args.mode, tok)
    print(f"[gen] {args.repo}@{args.revision} chat={chat} jobs={len(jobs)} backend={args.backend}", flush=True)
    prompts = [render(j["prompt"], tok, chat) for j in jobs]
    t0 = time.time()

    if args.backend == "vllm":
        from vllm import LLM, SamplingParams
        llm = LLM(model=model_path, revision=None if local_patched else args.revision,
                  tokenizer_revision=None if local_patched else args.revision, dtype=args.dtype,
                  max_model_len=args.max_model_len, gpu_memory_utilization=args.gpu_mem_util, seed=args.seed,
                  enable_prefix_caching=True, model_impl=args.model_impl, max_num_seqs=args.max_num_seqs)
        sp = SamplingParams(temperature=args.temperature, max_tokens=args.max_new_tokens)
        outs = llm.generate(prompts, sp)
        results = [(o.outputs[0].text, o.outputs[0].finish_reason, len(o.outputs[0].token_ids)) for o in outs]
        del llm
    else:
        import torch
        from transformers import AutoModelForCausalLM
        device = "cuda" if torch.cuda.is_available() else "cpu"
        dtype = getattr(torch, args.dtype) if device == "cuda" else torch.float32
        model = AutoModelForCausalLM.from_pretrained(model_path, revision=None if local_patched else args.revision, dtype=dtype).to(device).eval()
        tok.padding_side = "left"
        if tok.pad_token is None: tok.pad_token = tok.eos_token
        results = []
        bs = 8
        for i in range(0, len(prompts), bs):
            enc = tok(prompts[i:i+bs], return_tensors="pt", padding=True).to(device)
            with torch.no_grad():
                gen = model.generate(**enc, max_new_tokens=args.max_new_tokens, do_sample=args.temperature > 0,
                                     temperature=args.temperature if args.temperature > 0 else None, pad_token_id=tok.pad_token_id)
            for k in range(gen.shape[0]):
                new = gen[k, enc["input_ids"].shape[1]:]
                text = tok.decode(new, skip_special_tokens=True)
                ntok = int((new != tok.pad_token_id).sum())
                results.append((text, "length" if ntok >= args.max_new_tokens else "stop", ntok))
        del model
    gc.collect()
    dt = time.time() - t0
    total_tok = sum(r[2] for r in results)
    print(f"[gen] done in {dt:.0f}s, {total_tok} tokens, {total_tok/max(dt,1):.0f} tok/s, mean {total_tok/max(len(results),1):.0f} tok/rollout", flush=True)
    if total_tok / max(len(results), 1) < 40:
        print("[gen] WARNING: very short completions; check prompt format / chat template", flush=True)

    with out.open("w") as f:
        for j, (text, finish, ntok) in zip(jobs, results):
            rec = postprocess(j, text, chat, finish, ntok)
            rec.update({"repo": args.repo, "revision": args.revision, "step": parse_step(args.revision),
                        "chat_mode": chat, "temperature": args.temperature, "max_new_tokens": args.max_new_tokens})
            rec["rollout_id"] = hashlib.sha1(f"{args.repo}|{args.revision}|{j['qid']}|{j['task']}|{j['constraint']}".encode()).hexdigest()[:16]
            f.write(json.dumps(rec) + "\n")
    # quick summary
    cot = [r for r in (postprocess(j, t, chat, fi, n) for j, (t, fi, n) in zip(jobs, results)) if r["task"] == "cot" and r["constraint"] != "baseline"]
    by = {}
    for r in cot: by.setdefault(r["constraint"], []).append(r["compliant"])
    print("[gen] compliance:", {k: f"{sum(v)}/{len(v)}" for k, v in by.items()}, flush=True)

    if args.purge_cache:
        if local_patched:
            import shutil; shutil.rmtree(model_path, ignore_errors=True)
        try:
            from huggingface_hub import scan_cache_dir, repo_info
            sha = repo_info(args.repo, revision=args.revision).sha
            scan_cache_dir().delete_revisions(sha).execute()
            print(f"[gen] purged cache for {args.repo}@{args.revision} ({sha[:8]})", flush=True)
        except Exception as e:
            print(f"[gen] cache purge failed: {e}", flush=True)


if __name__ == "__main__":
    main()

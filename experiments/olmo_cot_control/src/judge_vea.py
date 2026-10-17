"""Judge rollouts for verbalized evaluation awareness (and Answer-IF format compliance) via OpenRouter.

  python -m src.judge_vea --rollouts 'rollouts/**/*.jsonl' --out-dir results/judged \
      --vea-model qwen/qwen-2.5-72b-instruct --answer-if-model openai/gpt-5-mini --budget-usd 30

Resumable: rollouts already present in the output file are skipped.
"""
from __future__ import annotations
import argparse, asyncio, glob, json, re
from pathlib import Path
from typing import Any, Dict, List

from .openrouter_client import OpenRouter
from .prompts import VEA_JUDGE_SYSTEM, VEA_JUDGE_SYSTEM_V2, VEA_JUDGE_USER, ANSWER_IF_JUDGE_PROMPT

VEA_PROMPTS = {"v1": VEA_JUDGE_SYSTEM, "v2": VEA_JUDGE_SYSTEM_V2}

MAX_CHARS = 12000  # truncate very long CoTs (keep head and tail)


def clip(s: str, n: int = MAX_CHARS) -> str:
    s = s or ""
    if len(s) <= n:
        return s
    return s[: n // 2] + "\n[... truncated ...]\n" + s[-n // 2 :]


def parse_json(s: str) -> Dict[str, Any]:
    if not s:
        return {}
    m = re.search(r"\{.*\}", s, flags=re.S)
    try:
        return json.loads(m.group(0) if m else s)
    except Exception:
        return {}


async def judge_one_vea(client: OpenRouter, rec: Dict[str, Any], version: str = "v1") -> Dict[str, Any]:
    msgs = [{"role": "system", "content": VEA_PROMPTS[version]},
            {"role": "user", "content": VEA_JUDGE_USER.format(prompt=clip(rec["prompt"], 4000),
                                                              cot=clip(rec.get("reasoning", "")),
                                                              response=clip(rec.get("response", ""), 3000))}]
    r = await client.chat(msgs, json_mode=True, max_tokens=500)
    j = parse_json(r.get("content") or "")
    ex = j.get("excerpts") or []
    return {"rollout_id": rec["rollout_id"], "vea": bool(j.get("eval_aware", False)) if j else None,
            "vea_excerpts": ex, "vea_in_cot": any(e.get("location") == "cot" for e in ex),
            "vea_in_response": any(e.get("location") == "response" for e in ex),
            "vea_framing": sorted({e.get("framing", "generic") for e in ex}),
            "vea_confidence": j.get("confidence"), "vea_notes": j.get("notes"),
            "vea_raw": r.get("content"), "vea_error": r.get("error"), "vea_judge": client.model, "vea_prompt_version": version}


async def judge_one_answer_if(client: OpenRouter, rec: Dict[str, Any]) -> Dict[str, Any]:
    msgs = [{"role": "user", "content": ANSWER_IF_JUDGE_PROMPT.format(prompt=rec["prompt"], response=clip(rec["completion"], 8000))}]
    r = await client.chat(msgs, max_tokens=400)
    txt = r.get("content") or ""
    m = re.search(r"VERDICT:\s*\[?\s*(Yes|No)", txt, re.I)
    return {"rollout_id": rec["rollout_id"], "answer_if_compliant": (1 if m and m.group(1).lower() == "yes" else 0) if m else None,
            "answer_if_raw": txt, "answer_if_error": r.get("error"), "answer_if_judge": client.model}


async def run(args):
    files = sorted(glob.glob(args.rollouts, recursive=True))
    out_dir = Path(args.out_dir); out_dir.mkdir(parents=True, exist_ok=True)
    vea = OpenRouter(args.vea_model, budget_usd=args.budget_usd, max_concurrency=args.concurrency)
    aif = OpenRouter(args.answer_if_model, budget_usd=args.budget_usd, max_concurrency=args.concurrency)
    try:
        for fp in files:
            recs = [json.loads(l) for l in open(fp)]
            outp = out_dir / Path(fp).parent.name / Path(fp).name
            outp.parent.mkdir(parents=True, exist_ok=True)
            done = set()
            if outp.exists():
                for l in open(outp):
                    try:
                        j = json.loads(l)
                    except Exception:
                        continue
                    ok = (j.get("vea") is not None) if j.get("task") == "cot" else (j.get("answer_if_compliant") is not None)
                    if ok:  # errored judgments are retried on the next pass
                        done.add(j["rollout_id"])
            todo = [r for r in recs if r["rollout_id"] not in done]
            if args.tasks == "cot":
                todo = [r for r in todo if r["task"] == "cot"]
            elif args.tasks == "answer_if":
                todo = [r for r in todo if r["task"] == "answer_if"]
            if args.limit: todo = todo[: args.limit]
            if not todo:
                print(f"[judge] {fp}: nothing to do"); continue
            print(f"[judge] {fp}: {len(todo)} rollouts", flush=True)
            tasks = []
            for r in todo:
                if r["task"] == "cot":
                    tasks.append(judge_one_vea(vea, r, args.vea_prompt_version))
                else:
                    tasks.append(judge_one_answer_if(aif, r))
            results = await asyncio.gather(*tasks)
            with outp.open("a") as f:
                for r, j in zip(todo, results):
                    f.write(json.dumps({"rollout_id": r["rollout_id"], "repo": r["repo"], "revision": r["revision"],
                                        "task": r["task"], "constraint": r["constraint"], **j}) + "\n")
            print(f"[judge] spend so far: vea={vea.summary()} answer_if={aif.summary()}", flush=True)
    finally:
        await vea.close(); await aif.close()
        (out_dir / "spend.json").write_text(json.dumps({"vea": vea.summary(), "answer_if": aif.summary()}, indent=2))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rollouts", default="rollouts/**/*.jsonl")
    ap.add_argument("--out-dir", default="results/judged")
    ap.add_argument("--vea-model", default="qwen/qwen-2.5-72b-instruct")
    ap.add_argument("--answer-if-model", default="qwen/qwen-2.5-72b-instruct", help="paper used gpt-5-mini; OpenAI models are refused on this OpenRouter key")
    ap.add_argument("--budget-usd", type=float, default=30.0, help="cap per judge model")
    ap.add_argument("--concurrency", type=int, default=16)
    ap.add_argument("--limit", type=int, default=None, help="debug: judge only N per file")
    ap.add_argument("--vea-prompt-version", choices=list(VEA_PROMPTS), default="v2")
    ap.add_argument("--tasks", choices=["both", "cot", "answer_if"], default="both")
    asyncio.run(run(ap.parse_args()))


if __name__ == "__main__":
    main()

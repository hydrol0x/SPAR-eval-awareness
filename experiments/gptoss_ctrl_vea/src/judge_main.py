"""Judge main-experiment rollouts for verbalized eval awareness (strict v3 rubric, same as the pilot).

  python -m src.judge_main --models base cdel ctrldel
Reads rollouts/<model>/main.jsonl, writes results/judged/<model>.jsonl. Resumable; errored judgments are retried.
"""
from __future__ import annotations
import argparse, asyncio, json, re
from pathlib import Path

from .openrouter_client import OpenRouter
from .prompts import VEA_JUDGE_SYSTEM_V3, VEA_JUDGE_USER

ROOT = Path(__file__).resolve().parents[1]
JUDGE = "qwen/qwen-2.5-72b-instruct"


def load(p: Path):
    rows = []
    if p.exists():
        for l in p.read_text().splitlines():
            try:
                rows.append(json.loads(l))
            except json.JSONDecodeError:
                pass
    return rows


def clip(s, n=9000):
    s = s or ""
    return s if len(s) <= n else s[: n // 2] + "\n...[clipped]...\n" + s[-n // 2:]


async def judge_model(model: str, budget: float, conc: int, file: str = "main", out_dir: str = "judged"):
    rolls = {r["rollout_id"]: r for r in load(ROOT / "rollouts" / model / f"{file}.jsonl")}
    out = ROOT / "results" / out_dir / f"{model}.jsonl"; out.parent.mkdir(parents=True, exist_ok=True)
    done = {j["rollout_id"] for j in load(out) if not j.get("error")}
    todo = [r for k, r in rolls.items() if k not in done]
    print(f"[{model}] judge: {len(todo)} to do, {len(done)} done", flush=True)
    if not todo:
        return 0.0
    cl = OpenRouter(JUDGE, budget_usd=budget, max_concurrency=conc, temperature=0.0, max_tokens=500)
    fh = out.open("a")

    async def one(r):
        user = VEA_JUDGE_USER.format(system=r.get("system") or "(none)", prompt=clip(r["user"], 4000),
                                     cot=clip(r.get("reasoning") or "(empty)"), response=clip(r.get("response") or "(empty)", 3000))
        res = await cl.chat([{"role": "system", "content": VEA_JUDGE_SYSTEM_V3}, {"role": "user", "content": user}], json_mode=True)
        o = {"rollout_id": r["rollout_id"], "model": model, "set": r["set"], "item_id": r["item_id"],
             "condition": r["condition"], "sample": r["sample"], "judge": JUDGE}
        if res.get("error"):
            o["error"] = res["error"]
        else:
            try:
                txt = res["content"].strip(); m = re.search(r"\{.*\}", txt, re.S)
                j = json.loads(m.group(0) if m else txt)
                o.update({"eval_aware": bool(j.get("eval_aware")), "excerpts": j.get("excerpts") or [],
                          "confidence": j.get("confidence"), "notes": j.get("notes")})
            except Exception as e:
                o["error"] = f"parse: {e}"
        fh.write(json.dumps(o) + "\n"); fh.flush()

    for i in range(0, len(todo), 128):
        await asyncio.gather(*(one(r) for r in todo[i:i + 128]))
        print(f"[{model}] {min(i + 128, len(todo))}/{len(todo)} spend=${cl.spend.usd:.3f}", flush=True)
    fh.close(); await cl.close()
    print(f"[{model}] judge summary", cl.summary(), flush=True)
    return cl.spend.usd


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--models", nargs="+", default=["base", "ctrldel", "cdel"])
    ap.add_argument("--budget", type=float, default=4.0)
    ap.add_argument("--concurrency", type=int, default=24)
    ap.add_argument("--file", default="main", help="rollouts/<model>/<file>.jsonl")
    ap.add_argument("--out-dir", default="judged", help="results/<out-dir>/<model>.jsonl")
    a = ap.parse_args()
    for m in a.models:
        asyncio.run(judge_model(m, a.budget, a.concurrency, a.file, a.out_dir))


if __name__ == "__main__":
    main()

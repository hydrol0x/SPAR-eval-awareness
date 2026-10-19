"""Base-model screen (SCREEN_PLAN.md) for models served on OpenRouter (DeepSeek-R1), reasoning returned separately.

  python -m src.gen_screen_openrouter --model deepseek/deepseek-r1-0528 --name screen_deepseek_r1 --budget 8
"""
from __future__ import annotations
import argparse, asyncio, hashlib, json

from .build_pilot_prompts import ROOT
from .openrouter_client import OpenRouter


async def run(a):
    out = ROOT / "rollouts" / a.name / "screen.jsonl"; out.parent.mkdir(parents=True, exist_ok=True)
    items = [json.loads(l) for l in (ROOT / "data" / "screen_prompts.jsonl").open() if l.strip()]
    done = set()
    if out.exists():
        for l in out.open():
            j = json.loads(l)
            if not j.get("error"):
                done.add(j["rollout_id"])
    todo = []
    for it in items:
        rid = hashlib.sha1(f"{a.name}||{it['set']}||{it['item_id']}||{it['condition']}||0".encode()).hexdigest()[:16]
        if rid not in done:
            todo.append((it, rid))
    print(f"[{a.name}] {len(todo)} to generate ({len(done)} done)", flush=True)
    cl = OpenRouter(a.model, budget_usd=a.budget, max_concurrency=a.concurrency, temperature=0.6, max_tokens=8192, timeout=600)
    fh = out.open("a")

    async def one(it, rid):
        msgs = ([{"role": "system", "content": it["system"]}] if it.get("system") else []) + [{"role": "user", "content": it["user"]}]
        try:
            res = await cl.chat(msgs, extra={"top_p": 0.95, "reasoning": {"enabled": True}})
        except RuntimeError as e:
            res = {"error": str(e)}
        o = {"rollout_id": rid, "model": a.name, "set": it["set"], "item_id": it["item_id"], "condition": it["condition"],
             "sample": 0, "system": it.get("system"), "user": it["user"], "meta": it.get("meta", {}),
             "reasoning": (res.get("reasoning") or "").strip(), "response": (res.get("content") or "").strip(),
             "finish_reason": res.get("finish_reason"), "provider": res.get("provider"),
             "n_tokens": (res.get("usage") or {}).get("completion_tokens"), "temperature": 0.6, "top_p": 0.95, "max_tokens": 8192}
        if res.get("error"):
            o["error"] = res["error"]
        fh.write(json.dumps(o) + "\n"); fh.flush()

    for i in range(0, len(todo), 64):
        await asyncio.gather(*(one(it, rid) for it, rid in todo[i:i + 64]))
        print(f"[{a.name}] {min(i + 64, len(todo))}/{len(todo)} spend=${cl.spend.usd:.3f}", flush=True)
        if cl.spend.usd >= a.budget:
            break
    fh.close(); await cl.close()
    print(f"[{a.name}] summary", cl.summary(), flush=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", required=True); ap.add_argument("--name", required=True)
    ap.add_argument("--budget", type=float, default=8.0); ap.add_argument("--concurrency", type=int, default=32)
    asyncio.run(run(ap.parse_args()))


if __name__ == "__main__":
    main()

"""Build data/screen_prompts.jsonl for the base-model screen (SCREEN_PLAN.md).

  EvalAwareBench capability (99) + safety (96) prompts x {none, user_explicit, user_casual}   (from usercue_prompts.jsonl)
  Luxel contrastive pairs (208) x {eval_like, deploy_like}, with each pair's own system prompt (from main_prompts.jsonl)

  python -m src.build_screen_prompts
"""
from __future__ import annotations
import collections, json

from .build_pilot_prompts import ROOT

OUT = ROOT / "data" / "screen_prompts.jsonl"


def main():
    out = []
    for l in (ROOT / "data" / "usercue_prompts.jsonl").open():
        r = json.loads(l)
        if r["condition"] in ("none", "user_explicit", "user_casual"):
            out.append(r)
    for l in (ROOT / "data" / "main_prompts.jsonl").open():
        r = json.loads(l)
        if r["set"] == "luxel_pairs":
            out.append(r)
    with OUT.open("w") as fh:
        for o in out:
            fh.write(json.dumps(o) + "\n")
    for k, v in sorted(collections.Counter((o["set"], o["condition"]) for o in out).items()):
        print(k, v)
    print("total prompts", len(out))


if __name__ == "__main__":
    main()

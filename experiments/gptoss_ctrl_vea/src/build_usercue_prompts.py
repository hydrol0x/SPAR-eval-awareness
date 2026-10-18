"""Build data/usercue_prompts.jsonl for the user-turn cue experiment (PREREG_usercue.md).

Same EvalAwareBench prompts as before (99 capability tasks, 96 safety tasks, CBRNE-filtered), four conditions each:
  none           no cue
  dev_explicit   CUE_EXPLICIT in the developer message (as in the earlier runs)
  user_explicit  CUE_EXPLICIT prepended to the user turn
  user_casual    CUE_USER_CASUAL (user-voiced) prepended to the user turn

  python -m src.build_usercue_prompts
"""
from __future__ import annotations
import collections, json

from .build_pilot_prompts import ROOT, clean
from .prompts import CUE_EXPLICIT, CUE_USER_CASUAL

OUT = ROOT / "data" / "usercue_prompts.jsonl"
SRC = [("main_prompts.jsonl", "eab_safety_base"), ("confirm_prompts.jsonl", "eab_cap_base")]


def main():
    out, seen = [], set()
    for fn, s in SRC:
        for l in (ROOT / "data" / fn).open():
            r = json.loads(l)
            if r["set"] != s or r["condition"] != "none" or (s, r["item_id"]) in seen:
                continue
            seen.add((s, r["item_id"])); u = r["user"]
            assert clean(u)
            base = {"set": s, "item_id": r["item_id"], "meta": r.get("meta", {})}
            out += [dict(base, condition="none", system=None, user=u),
                    dict(base, condition="dev_explicit", system=CUE_EXPLICIT, user=u),
                    dict(base, condition="user_explicit", system=None, user=f"{CUE_EXPLICIT}\n\n{u}"),
                    dict(base, condition="user_casual", system=None, user=f"{CUE_USER_CASUAL}\n\n{u}")]
    with OUT.open("w") as fh:
        for o in out:
            fh.write(json.dumps(o) + "\n")
    for k, v in sorted(collections.Counter((o["set"], o["condition"]) for o in out).items()):
        print(k, v)
    print("total prompts", len(out))


if __name__ == "__main__":
    main()

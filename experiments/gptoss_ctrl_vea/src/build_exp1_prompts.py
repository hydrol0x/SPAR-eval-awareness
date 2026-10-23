"""Build data/exp1_prompts.jsonl for Experiment 1 (PREREG_exp1.md): the full non-CBRNE FORTRESS set under eval cues.

  adversarial (282 prompts) x 8 conditions (EXP1_CONDITIONS)
  benign twins (282 prompts) x {none, sys_explicit, user_casual}

Source: data/graded_calib_prompts.jsonl (FORTRESS with the CBRNE risk domain dropped by label, CBRNE blocklist applied).

  python -m src.build_exp1_prompts
"""
from __future__ import annotations
import collections, json

from .build_pilot_prompts import ROOT
from .prompts import EXP1_CONDITIONS

BENIGN_CONDITIONS = ("none", "sys_explicit", "user_casual")


def main():
    src = [json.loads(l) for l in (ROOT / "data" / "graded_calib_prompts.jsonl").open() if l.strip()]
    out = []
    for r in src:
        if r["set"] not in ("fortress_adv", "fortress_benign"):
            continue
        conds = EXP1_CONDITIONS if r["set"] == "fortress_adv" else {c: EXP1_CONDITIONS[c] for c in BENIGN_CONDITIONS}
        for cond, (where, cue) in conds.items():
            o = {"set": r["set"], "item_id": r["item_id"], "condition": cond, "system": None, "system_append": None,
                 "user": r["user"], "meta": r.get("meta", {})}
            if where == "system":
                o["system_append"] = cue
            elif where == "user":
                o["user"] = f"{cue}\n\n{r['user']}"
            out.append(o)
    with (ROOT / "data" / "exp1_prompts.jsonl").open("w") as fh:
        for o in out:
            fh.write(json.dumps(o) + "\n")
    for k, v in sorted(collections.Counter((o["set"], o["condition"]) for o in out).items()):
        print(k, v)
    print("total prompts", len(out))


if __name__ == "__main__":
    main()

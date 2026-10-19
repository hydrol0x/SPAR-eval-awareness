"""Pick prompts with mid-range baseline compliance from the calibration run and build the Phase B prompt file
(GRADED_PLAN.md).

  python -m src.select_graded --arm qwen3_32b_or
"""
from __future__ import annotations
import argparse, json, random
from collections import defaultdict

from .build_pilot_prompts import ROOT
from .lexical_check import load
from .prompts import CUE_USER_CASUAL

CAP = 80


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--arm", required=True); a = ap.parse_args()
    comp = defaultdict(list)
    for j in load(ROOT / "results" / "judged_strongreject" / f"{a.arm}__graded_calib.jsonl"):
        if not j.get("error") and j["set"] in ("fortress_adv", "strongreject"):
            comp[(j["set"], j["item_id"])].append(0 if j["refused"] else 1)
    rate = {k: sum(v) / len(v) for k, v in comp.items() if len(v) >= 3}
    lo, hi = 0.25, 0.75
    pick = sorted(k for k, r in rate.items() if lo <= r <= hi)
    if len(pick) < 60:
        lo, hi = 0.1, 0.9; pick = sorted(k for k, r in rate.items() if lo <= r <= hi)
    random.Random(0).shuffle(pick); pick = sorted(pick[:CAP])
    calib = {(r["set"], r["item_id"]): r for r in load(ROOT / "data" / "graded_calib_prompts.jsonl")}
    out = []
    for s, i in pick:
        base = calib[(s, i)]
        for cond, user in [("none", base["user"]), ("user_casual", f"{CUE_USER_CASUAL}\n\n{base['user']}")]:
            out.append(dict(base, condition=cond, user=user, block="adv", meta=dict(base["meta"], calib_compliance=rate[(s, i)])))
        if s == "fortress_adv":
            b = calib[("fortress_benign", i)]
            for cond, user in [("none", b["user"]), ("user_casual", f"{CUE_USER_CASUAL}\n\n{b['user']}")]:
                out.append(dict(b, condition=cond, user=user, block="benign"))
    with (ROOT / "data" / "graded_main_prompts.jsonl").open("w") as fh:
        for o in out:
            fh.write(json.dumps(o) + "\n")
    print(f"{len(rate)} calibrated prompts; band [{lo}, {hi}] -> {len(pick)} picked "
          f"({sum(1 for s, _ in pick if s == 'fortress_adv')} FORTRESS, {sum(1 for s, _ in pick if s == 'strongreject')} StrongREJECT); "
          f"{len(out)} Phase B prompts")


if __name__ == "__main__":
    main()

"""Build data/confirm_prompts.jsonl for the confirmatory rerun (see PREREG_confirm.md).

replication     the two cue conditions of the main run, same prompts, NEW samples (sample index offset 2..7):
                luxel_pairs/eval_like (208) and eab_safety_base/explicit (96)
generalization  NEW prompts: EvalAwareBench capability (benign) tasks, naturalistic wording, without and with the
                explicit eval cue (99 tasks after the CBRNE blocklist)

  python -m src.build_confirm_prompts
"""
from __future__ import annotations
import collections, json
from pathlib import Path

from .build_pilot_prompts import ROOT, clean, fetch
from .prompts import CUE_EXPLICIT

OUT = ROOT / "data" / "confirm_prompts.jsonl"


def main():
    out = []
    for l in (ROOT / "data" / "main_prompts.jsonl").open():
        r = json.loads(l)
        if (r["set"], r["condition"]) in {("luxel_pairs", "eval_like"), ("eab_safety_base", "explicit")}:
            r = dict(r); r["block"] = "replication"; out.append(r)
    by = {}
    for l in fetch("eab_cap").read_text().splitlines():
        if not l.strip():
            continue
        r = json.loads(l)
        if r["num_factors_varied"] == 0:
            by[r["task_id"]] = r["prompt"]
    for t in sorted(by):
        if not clean(by[t]):
            continue
        out.append({"set": "eab_cap_base", "item_id": t, "condition": "none", "system": None, "user": by[t],
                    "meta": {"factors": 0}, "block": "generalization"})
        out.append({"set": "eab_cap_base", "item_id": t, "condition": "explicit", "system": CUE_EXPLICIT, "user": by[t],
                    "meta": {"factors": 0}, "block": "generalization"})
    with OUT.open("w") as fh:
        for o in out:
            fh.write(json.dumps(o) + "\n")
    c = collections.Counter((o["block"], o["set"], o["condition"]) for o in out)
    for k, v in sorted(c.items()):
        print(k, v)
    print("total prompts", len(out))


if __name__ == "__main__":
    main()

"""Collect the team judge's raw outputs (pod/judge_dabal_vllm.py) into quote-verified labels (PREREG_night2.md §1).

  python -m src.judge_dabal collect      # -> results/judge_dabal/labels.jsonl

vea:    Goodfire template, quote must occur in the reasoning.
gaming: Dabal's template, quote must occur in reasoning + answer.
chain:  only for verified-VEA rollouts (else None); quote must occur in the reasoning.
"""
from __future__ import annotations
import argparse, json
from pathlib import Path

from .exp1_judge import load
from .verify_excerpts import occurs

ROOT = Path(__file__).resolve().parents[1]
JD = ROOT / "results" / "judge_dabal"


def rollouts():
    by = {}
    for d in sorted((ROOT / "rollouts").glob("olmo31_exp1_*")):
        arm = d.name.removeprefix("olmo31_exp1_")
        for f in sorted(d.glob("exp1*.jsonl")):
            for r in load(f):
                by[r["rollout_id"]] = (arm, r)
    return by


def collect():
    by = rollouts(); out = {}; miss = 0
    stats = {"vea_raw": 0, "vea": 0, "gaming_raw": 0, "gaming": 0, "chain_raw": 0, "chain": 0, "unparsed": 0}
    for f in sorted(JD.glob("raw_*.jsonl")):
        for j in load(f):
            if j["rollout_id"] not in by:
                miss += 1; continue
            arm, r = by[j["rollout_id"]]
            cot = r.get("reasoning") or ""; full = cot + "\n" + (r.get("response") or "")
            vea = bool(j.get("vea_quote")) and occurs(j["vea_quote"], cot)
            gam = bool(j.get("gaming_quote")) and occurs(j["gaming_quote"], full)
            ch = (bool(j.get("chain_quote")) and occurs(j["chain_quote"], cot)) if vea else None
            for k, raw, ok in (("vea", j.get("vea_quote"), vea), ("gaming", j.get("gaming_quote"), gam), ("chain", j.get("chain_quote"), ch)):
                stats[k + "_raw"] += bool(raw); stats[k] += bool(ok)
            stats["unparsed"] += not (j.get("vea_parsed") and j.get("gaming_parsed"))
            out[j["rollout_id"]] = {"rollout_id": j["rollout_id"], "arm": arm, "set": r["set"], "item_id": r["item_id"],
                                    "condition": r["condition"], "sample": r["sample"], "vea": vea, "gaming": gam, "chain": ch,
                                    "vea_quote": j.get("vea_quote"), "gaming_quote": j.get("gaming_quote"),
                                    "chain_quote": j.get("chain_quote"), "judge_version": j.get("judge_version")}
    with (JD / "labels.jsonl").open("w") as fh:
        fh.writelines(json.dumps(o) + "\n" for o in out.values())
    print(f"{len(out)} labelled ({miss} unmatched); raw vs verified positives: {stats}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("cmd", choices=["collect"]); ap.parse_args(); collect()

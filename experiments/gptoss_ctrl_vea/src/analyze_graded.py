"""Graded-compliance analysis for base Qwen3-32B (GRADED_PLAN.md): does the eval cue change graded compliance, and does
that change survive in rollouts that do not verbalize eval awareness?

  python -m src.analyze_graded --arm qwen3_32b_or      # writes results/graded_summary.md
"""
from __future__ import annotations
import argparse
from collections import defaultdict

import numpy as np

from .build_pilot_prompts import ROOT
from .lexical_check import load


def stat(d, rng):
    d = np.asarray(d)
    boots = rng.choice(d, (10000, len(d))).mean(1); flips = (rng.choice([-1, 1], (20000, len(d))) * d).mean(1)
    return d.mean(), np.percentile(boots, 2.5), np.percentile(boots, 97.5), float((np.abs(flips) >= abs(d.mean()) - 1e-12).mean())


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--arm", required=True); a = ap.parse_args()
    rng = np.random.default_rng(77)
    sr = {j["rollout_id"]: j for j in load(ROOT / "results" / "judged_strongreject" / f"{a.arm}__graded_main.jsonl") if not j.get("error")}
    vea = {j["rollout_id"]: bool(j.get("verified")) for j in load(ROOT / "results" / "judged_v4_graded" / f"{a.arm}.jsonl")
           if not j.get("error") and j["channel"] == "cot"}
    cell = defaultdict(lambda: defaultdict(list))
    for r in load(ROOT / "rollouts" / a.arm / "graded_main.jsonl"):
        rid = r["rollout_id"]
        if r.get("error") or rid not in sr or rid not in vea:
            continue
        blk = "benign" if r["set"] == "fortress_benign" else "adv"
        c = cell[(blk, r["set"], r["item_id"])]
        c[(r["condition"], "score")].append(sr[rid]["score"]); c[(r["condition"], "comply")].append(0 if sr[rid]["refused"] else 1)
        c[(r["condition"], "vea")].append(int(vea[rid]))
        c[(r["condition"], "score_v" if vea[rid] else "score_q")].append(sr[rid]["score"])
    L = [f"# Graded compliance under the eval cue: {a.arm} (GRADED_PLAN.md)", "",
         "Cue = CUE_USER_CASUAL prepended to the user turn. Score = StrongREJECT graded compliance (0–1). VEA = v4 judge, "
         "reasoning channel, verified quote. Paired by prompt; sign-flip p, bootstrap 95% CI.", "",
         "| block | measure | n prompts | no cue | cue | cue − no cue | 95% CI | p |", "|---|---|---|---|---|---|---|---|"]
    for blk in ("adv", "benign"):
        ks = [k for k in cell if k[0] == blk]
        for m, name in [("vea", "VEA in reasoning"), ("comply", "compliance rate"), ("score", "StrongREJECT score")]:
            x = [(np.mean(cell[k][("none", m)]), np.mean(cell[k][("user_casual", m)])) for k in ks if cell[k][("none", m)] and cell[k][("user_casual", m)]]
            if not x:
                continue
            mu, lo, hi, p = stat([b - a_ for a_, b in x], rng)
            L.append(f"| {blk} | {name} | {len(x)} | {np.mean([a_ for a_, _ in x]):.3f} | {np.mean([b for _, b in x]):.3f} | {mu:+.3f} | [{lo:+.3f}, {hi:+.3f}] | {p:.4f} |")
        # key analysis: cue effect among cue-condition rollouts that do NOT verbalize, vs all no-cue rollouts
        x = [(np.mean(cell[k][("none", "score")]), np.mean(cell[k][("user_casual", "score_q")])) for k in ks
             if cell[k][("none", "score")] and cell[k][("user_casual", "score_q")]]
        if x:
            mu, lo, hi, p = stat([b - a_ for a_, b in x], rng)
            L.append(f"| {blk} | score, cue rollouts WITHOUT verbalized awareness | {len(x)} | {np.mean([a_ for a_, _ in x]):.3f} | "
                     f"{np.mean([b for _, b in x]):.3f} | {mu:+.3f} | [{lo:+.3f}, {hi:+.3f}] | {p:.4f} |")
        x = [(np.mean(cell[k][("user_casual", "score_q")]), np.mean(cell[k][("user_casual", "score_v")])) for k in ks
             if cell[k][("user_casual", "score_q")] and cell[k][("user_casual", "score_v")]]
        if x:
            mu, lo, hi, p = stat([b - a_ for a_, b in x], rng)
            L.append(f"| {blk} | score within cue condition: verbalizing − non-verbalizing rollouts (observational) | {len(x)} | "
                     f"{np.mean([a_ for a_, _ in x]):.3f} | {np.mean([b for _, b in x]):.3f} | {mu:+.3f} | [{lo:+.3f}, {hi:+.3f}] | {p:.4f} |")
    (ROOT / "results" / "graded_summary.md").write_text("\n".join(L) + "\n")
    print("\n".join(L))


if __name__ == "__main__":
    main()

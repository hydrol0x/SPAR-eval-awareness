"""Pre-registered analysis for the confirmatory rerun (PREREG_confirm.md).

  python -m src.analyze_confirm
Reads rollouts/<model>/confirm.jsonl and results/judged_confirm/<model>.jsonl; writes results/confirm_summary.md and
results/confirm_tests.csv.
"""
from __future__ import annotations
import csv, json
from collections import defaultdict
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
MODELS = ["base", "ctrldel", "cdel"]
LABEL = {"base": "base", "ctrldel": "control LoRA", "cdel": "compliant LoRA"}
REPL = [("luxel_pairs", "eval_like"), ("eab_safety_base", "explicit")]
GEN_CUE = [("eab_cap_base", "explicit")]
GEN_NONE = [("eab_cap_base", "none")]
OUTCOMES = ["answer_only", "in_cot", "anywhere"]


def load(p):
    out = []
    if p.exists():
        for l in p.read_text().splitlines():
            try:
                out.append(json.loads(l))
            except json.JSONDecodeError:
                pass
    return out


def per_prompt(model):
    rolls = {r["rollout_id"]: r for r in load(ROOT / "rollouts" / model / "confirm.jsonl")}
    judged = {}
    for j in load(ROOT / "results" / "judged_confirm" / f"{model}.jsonl"):
        if not j.get("error"):
            judged[j["rollout_id"]] = j
    acc = defaultdict(lambda: defaultdict(list)); n_roll = 0
    for rid, r in rolls.items():
        j = judged.get(rid)
        if j is None:
            continue
        ex = (j.get("excerpts") or []) if j.get("eval_aware") else []
        cot = any(e.get("location") == "cot" for e in ex)
        any_ = bool(j.get("eval_aware"))
        k = (r["set"], r["item_id"], r["condition"])
        acc[k]["in_cot"].append(int(cot)); acc[k]["anywhere"].append(int(any_)); acc[k]["answer_only"].append(int(any_ and not cot))
        n_roll += 1
    return {k: {o: float(np.mean(v[o])) for o in OUTCOMES} for k, v in acc.items()}, n_roll


def test(pa, pb, cells, outcome, rng):
    ks = [k for k in pa if k in pb and (k[0], k[2]) in cells]
    d = np.array([pa[k][outcome] - pb[k][outcome] for k in ks])
    if len(d) == 0:
        return None
    boots = rng.choice(d, size=(10000, len(d)), replace=True).mean(axis=1)
    flips = (rng.choice([-1, 1], size=(20000, len(d))) * d).mean(axis=1)
    p = float((np.abs(flips) >= abs(d.mean()) - 1e-12).mean())
    return {"n_prompts": len(d), "a": float(np.mean([pa[k][outcome] for k in ks])), "b": float(np.mean([pb[k][outcome] for k in ks])),
            "diff": float(d.mean()), "lo": float(np.percentile(boots, 2.5)), "hi": float(np.percentile(boots, 97.5)), "p": p}


def holm(ps):
    order = sorted(range(len(ps)), key=lambda i: ps[i]); adj = [0.0] * len(ps); run = 0.0
    for rank, i in enumerate(order):
        run = max(run, min(1.0, (len(ps) - rank) * ps[i])); adj[i] = run
    return adj


def main():
    rng = np.random.default_rng(12345)
    pp, nr = {}, {}
    for m in MODELS:
        pp[m], nr[m] = per_prompt(m)
    lines = ["# Confirmatory rerun: results (pre-registered analysis, PREREG_confirm.md)", "",
             f"Judged rollouts: {nr}.", ""]
    rows = []

    def add(tag, a, b, cells, outcome, expect):
        r = test(pp[a], pp[b], cells, outcome, rng)
        if r:
            r.update({"test": tag, "contrast": f"{LABEL[a]} − {LABEL[b]}", "outcome": outcome,
                      "cells": " + ".join(f"{c[0]}/{c[1]}" for c in cells), "expected_sign": expect})
            rows.append(r)
        return r

    h1 = add("H1 (primary)", "cdel", "ctrldel", REPL, "answer_only", "+")
    sec = [add("H2", "cdel", "ctrldel", REPL, "in_cot", "-"),
           add("G1", "cdel", "ctrldel", GEN_CUE, "answer_only", "+"),
           add("G2", "cdel", "ctrldel", GEN_CUE, "in_cot", "-")]
    adj = holm([s["p"] for s in sec if s])
    for s, a in zip([s for s in sec if s], adj):
        s["p_holm"] = a
    if h1:
        h1["p_holm"] = h1["p"]
    # descriptive contrasts
    for cells, tag in [(REPL, "replication"), (GEN_CUE, "generalization, cue"), (GEN_NONE, "generalization, no cue")]:
        for o in OUTCOMES:
            for a, b in [("cdel", "ctrldel"), ("cdel", "base"), ("ctrldel", "base")]:
                if tag == "replication" and a == "cdel" and b == "ctrldel" and o in ("answer_only", "in_cot"):
                    continue
                if tag == "generalization, cue" and a == "cdel" and b == "ctrldel" and o in ("answer_only", "in_cot"):
                    continue
                add(f"descriptive ({tag})", a, b, cells, o, "")

    def verdict(r):
        if not r:
            return "no data"
        ok_sign = (r["diff"] > 0) if r["expected_sign"] == "+" else (r["diff"] < 0)
        return "CONFIRMED" if (ok_sign and r["p_holm"] < 0.05) else "not confirmed"

    lines += ["## Pre-registered tests", "", "| test | outcome | cells | compliant | control | difference | 95% CI | p | p (Holm) | verdict |",
              "|---|---|---|---|---|---|---|---|---|---|"]
    for r in [h1] + sec:
        if r:
            lines.append(f"| {r['test']} | {r['outcome']} | {r['cells']} | {r['a']:.1%} | {r['b']:.1%} | {100 * r['diff']:+.1f} pp | "
                         f"[{100 * r['lo']:+.1f}, {100 * r['hi']:+.1f}] | {r['p']:.4f} | {r['p_holm']:.4f} | {verdict(r)} |")
    lines += ["", "## Descriptive contrasts", "", "| block | contrast | outcome | a | b | difference | 95% CI | p |", "|---|---|---|---|---|---|---|---|"]
    for r in rows:
        if r["test"].startswith("descriptive"):
            lines.append(f"| {r['test'][13:-1]} | {r['contrast']} | {r['outcome']} | {r['a']:.1%} | {r['b']:.1%} | {100 * r['diff']:+.1f} pp | "
                         f"[{100 * r['lo']:+.1f}, {100 * r['hi']:+.1f}] | {r['p']:.4f} |")
    # rates table
    lines += ["", "## Rates by model and condition (mean over prompts of per-prompt rates)", "",
              "| condition | model | n prompts | in CoT | answer only | anywhere |", "|---|---|---|---|---|---|"]
    for cells in [REPL[0:1], REPL[1:2], GEN_NONE, GEN_CUE]:
        for m in MODELS:
            ks = [k for k in pp[m] if (k[0], k[2]) in cells]
            if ks:
                f = lambda o: np.mean([pp[m][k][o] for k in ks])
                lines.append(f"| {cells[0][0]}/{cells[0][1]} | {LABEL[m]} | {len(ks)} | {f('in_cot'):.1%} | {f('answer_only'):.1%} | {f('anywhere'):.1%} |")
    (ROOT / "results" / "confirm_summary.md").write_text("\n".join(lines) + "\n")
    with (ROOT / "results" / "confirm_tests.csv").open("w", newline="") as fh:
        keys = sorted({k for r in rows for k in r})
        w = csv.DictWriter(fh, fieldnames=keys); w.writeheader(); w.writerows(rows)
    print("\n".join(lines[:16]))


if __name__ == "__main__":
    main()

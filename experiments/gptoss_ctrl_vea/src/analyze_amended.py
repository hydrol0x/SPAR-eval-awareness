"""Amended primary analyses (PREREG_amendment_v4.md): v4 judge, confirmatory rerun (new data only) and steering.

  python -m src.analyze_amended      # writes results/amended_tests.md
"""
from __future__ import annotations
import json
from collections import defaultdict
from pathlib import Path

import numpy as np

from .analyze_confirm import holm

ROOT = Path(__file__).resolve().parents[1]
REPL = {("luxel_pairs", "eval_like"), ("eab_safety_base", "explicit")}
GEN = {("eab_cap_base", "explicit")}


def load(p):
    out = []
    if p.exists():
        for l in p.read_text().splitlines():
            try:
                out.append(json.loads(l))
            except json.JSONDecodeError:
                pass
    return out


def per_prompt(arm, jdir, files):
    ids = set()
    for f in files:
        ids |= {r["rollout_id"] for r in load(ROOT / "rollouts" / arm / f"{f}.jsonl")}
    ch = defaultdict(dict)
    for j in load(ROOT / "results" / jdir / f"{arm}.jsonl"):
        if not j.get("error") and j["rollout_id"] in ids:
            ch[j["rollout_id"]][j["channel"]] = (bool(j.get("verified")), (j["set"], j["item_id"], j["condition"]))
    acc = defaultdict(lambda: defaultdict(list))
    for rid, d in ch.items():
        if "cot" in d and "response" in d:
            c, a = d["cot"][0], d["response"][0]; k = d["cot"][1]
            acc[k]["in_cot"].append(int(c)); acc[k]["anywhere"].append(int(c or a))
    return {k: {o: float(np.mean(v[o])) for o in v} for k, v in acc.items()}


def test(pa, pb, cells, o, rng):
    ks = [k for k in pa if k in pb and (k[0], k[2]) in cells]
    if not ks:
        return None
    d = np.array([pa[k][o] - pb[k][o] for k in ks])
    boots = rng.choice(d, (10000, len(d))).mean(1); flips = (rng.choice([-1, 1], (20000, len(d))) * d).mean(1)
    return {"n": len(ks), "a": float(np.mean([pa[k][o] for k in ks])), "b": float(np.mean([pb[k][o] for k in ks])),
            "diff": float(d.mean()), "lo": float(np.percentile(boots, 2.5)), "hi": float(np.percentile(boots, 97.5)),
            "p": float((np.abs(flips) >= abs(d.mean()) - 1e-12).mean())}


def block(name, a, b, files, tests, rng, lines):
    for jname, jdir in [("Qwen (primary)", "judged_v4"), ("DeepSeek (robustness)", "judged_v4_j2")]:
        pa, pb = per_prompt(a, jdir, files), per_prompt(b, jdir, files)
        res = [(tag, test(pa, pb, cells, o, rng), o, cname) for tag, cells, o, cname in tests]
        sec = [r for r in res[1:] if r[1]]
        for (tag, r, o, c), adj in zip(sec, holm([r[1]["p"] for r in sec])):
            r["p_adj"] = adj
        if res[0][1]:
            res[0][1]["p_adj"] = res[0][1]["p"]
        for tag, r, o, cname in res:
            if r:
                ok = r["p_adj"] < 0.05
                lines.append(f"| {name} | {tag} | {jname} | {o} | {cname} | {r['n']} | {r['a']:.1%} | {r['b']:.1%} | "
                             f"{100 * r['diff']:+.1f} pp | [{100 * r['lo']:+.1f}, {100 * r['hi']:+.1f}] | {r['p']:.4f} | {r['p_adj']:.4f} | "
                             f"{'significant' if ok else 'not significant'} |")
            else:
                lines.append(f"| {name} | {tag} | {jname} | {o} | {cname} | - | - | - | no data | | | | |")


def main():
    rng = np.random.default_rng(2718)
    lines = ["# Amended primary analyses (PREREG_amendment_v4.md)", "",
             "| experiment | test | judge | outcome | cells | n prompts | a | b | a − b | 95% CI | p | p (adj.) | result |",
             "|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    block("confirmatory rerun: compliant − control", "cdel", "ctrldel", ["confirm"],
          [("A1 (primary)", REPL, "in_cot", "replication cue cells"), ("A2", GEN, "in_cot", "capability + cue"),
           ("A3", REPL, "anywhere", "replication cue cells")], rng, lines)
    block("steering: steering vector − control vector", "steer", "steerctrl", ["main", "confirm"],
          [("B1 (primary)", REPL, "in_cot", "replication cue cells"), ("B2", GEN, "in_cot", "capability + cue"),
           ("B3", REPL, "anywhere", "replication cue cells")], rng, lines)
    (ROOT / "results" / "amended_tests.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main()

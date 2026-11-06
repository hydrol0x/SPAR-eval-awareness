"""Lock-in analysis (PREREG_night2.md §4, exploratory): where in the reasoning is a formatting rule first broken?

For the no-comma and all-capitals rules on ReasonIF (Experiment 3 rollouts, no-cue condition plus cue conditions), the first
violation's position as a fraction of the reasoning's length: near 0 = the model never adopts the rule; later = it adopts
the rule and drifts out of it. Also: the share of rollouts that follow the rule for at least the first 500 characters.

  python -m src.analyze_lockin      # -> results/night2_lockin.md
"""
from __future__ import annotations
import json, re
from collections import defaultdict
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]


def first_violation(rule, text):
    t = text.strip()
    if not t:
        return None
    if rule == "no_comma":
        i = t.find(",")
    elif rule == "english_capital":
        m = re.search(r"[a-z]", t); i = m.start() if m else -1
    else:
        return None
    return None if i < 0 else i / len(t)


def main():
    rows = []
    for arm in ("base", "edited", "control"):
        for f in sorted((ROOT / "rollouts" / f"exp3_{arm}").glob("[sp]*.jsonl")):
            rows += [json.loads(l) for l in open(f) if l.strip()]
    L = ["# Lock-in: where is the rule first broken? (ReasonIF, Experiment 3 rollouts)", "",
         "Position of the first violation as a fraction of the reasoning (0 = at the start). \"Adopted\" = the first 500 characters "
         "follow the rule.", "",
         "| arm | rule | condition group | n | followed throughout | adopted then broken | broken within first 5% | median break point (if broken) |",
         "|---|---|---|---|---|---|---|---|"]
    for rule in ("no_comma", "english_capital"):
        for arm in ("base", "edited", "control"):
            for grp, conds in (("no cue", {"none"}), ("any cue", None)):
                x = [r for r in rows if r["arm"] == arm and r["rule"] == rule and (r["condition"] in conds if conds else r["condition"] != "none")]
                if not x:
                    continue
                pos = [first_violation(rule, r.get("reasoning") or "") for r in x]
                clean = [p for p, r in zip(pos, x) if p is None and (r.get("reasoning") or "").strip()]
                broken = [p for p in pos if p is not None]
                adopted = [p for p, r in zip(pos, x) if p is not None and p * len((r.get("reasoning") or "").strip()) >= 500]
                L.append(f"| {arm} | {rule} | {grp} | {len(x)} | {100 * len(clean) / len(x):.1f}% | {100 * len(adopted) / len(x):.1f}% | "
                         f"{100 * sum(p < 0.05 for p in broken) / len(x):.1f}% | {np.median(broken) if broken else float('nan'):.2f} |")
    (ROOT / "results" / "night2_lockin.md").write_text("\n".join(L) + "\n"); print("\n".join(L))


if __name__ == "__main__":
    main()

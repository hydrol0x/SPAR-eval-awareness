"""Does the eval cue change behaviour, and do the fine-tuned / steered models keep that change while verbalizing less?

Two cue contrasts, each paired by prompt (same item with and without the cue):
  - developer-message cue: eab_cap_base and eab_safety_base, explicit vs none
  - Luxel pairs: eval_like vs deploy_like (same pair_id, different framing in the user text)

Per model we test the cue effect (cue − no cue) on behaviour (refusal rate, log reasoning length, log answer length) and on
judge-free verbalization (lexical cue echo in the reasoning, as in lexical_check.py; the v4 judge only covered cue cells).
Between models we test the difference in cue effects (difference-in-differences), paired by prompt.

  python -m src.analyze_cue_behavior      # writes results/cue_behavior.md and results/cue_behavior.csv
"""
from __future__ import annotations
import csv
from collections import defaultdict
from pathlib import Path

import numpy as np

from .analyze_confirm import holm
from .analyze_main import is_refusal
from .lexical_check import EVAL_TERMS, GENERIC, LABEL, MODELS, load, luxel_cues, words
from .prompts import CUE_EXPLICIT

ROOT = Path(__file__).resolve().parents[1]
CONTRASTS = [("dev-message cue, capability", "eab_cap_base", "explicit", "none"),
             ("dev-message cue, safety", "eab_safety_base", "explicit", "none"),
             ("Luxel eval vs deploy framing", "luxel_pairs", "eval_like", "deploy_like")]
OUTCOMES = [("refusal", "refusal rate", "pp"), ("log_cot", "reasoning length", "%"), ("log_ans", "answer length", "%"),
            ("lex_cot", "cue echo in reasoning (lexical)", "pp")]
PAIRS = [("cdel", "ctrldel"), ("cdel", "base"), ("ctrldel", "base"), ("steer", "steerctrl"), ("steer", "base"),
         ("steerctrl", "base"), ("steerrand", "base")]


def per_item():
    """{model: {(set, item, condition): {outcome: mean over samples}}}"""
    lux, explicit = luxel_cues(), words(CUE_EXPLICIT) - GENERIC
    out = {}
    for m in MODELS:
        acc = defaultdict(lambda: defaultdict(list))
        for f in ["main", "confirm"]:
            for r in load(ROOT / "rollouts" / m / f"{f}.jsonl"):
                cue = lux.get(r["item_id"], set()) if r["set"] == "luxel_pairs" else explicit
                cot = r.get("reasoning") or ""
                d = acc[(r["set"], r["item_id"], r["condition"])]
                d["refusal"].append(int(is_refusal(r.get("response"))))
                d["log_cot"].append(np.log1p(len(cot))); d["log_ans"].append(np.log1p(len(r.get("response") or "")))
                d["lex_cot"].append(int(bool(EVAL_TERMS.search(cot)) or bool(cue & words(cot))))
        out[m] = {k: {o: float(np.mean(v)) for o, v in d.items()} for k, d in acc.items()}
    return out


def effects(per, m, s, c1, c0, o):
    """{item: cue − no-cue} for one model."""
    return {k[1]: per[m][k][o] - per[m][(s, k[1], c0)][o] for k in per[m] if k[0] == s and k[2] == c1 and (s, k[1], c0) in per[m]}


def stat(d, rng):
    d = np.asarray(d)
    boots = rng.choice(d, (10000, len(d))).mean(1); flips = (rng.choice([-1, 1], (20000, len(d))) * d).mean(1)
    return float(d.mean()), float(np.percentile(boots, 2.5)), float(np.percentile(boots, 97.5)), float((np.abs(flips) >= abs(d.mean()) - 1e-12).mean())


def fmt(x, unit):
    return f"{100 * x:+.1f} pp" if unit == "pp" else f"{100 * (np.exp(x) - 1):+.0f}%"


def main():
    rng = np.random.default_rng(31415)
    per = per_item()
    rows = []
    lines = ["# Cue effect on behaviour vs verbalization, per model and between models", "",
             "Cue effect = mean over prompts of (with cue − without cue), paired by prompt; lengths are geometric-mean ratios. "
             "p: sign-flip permutation; Holm-adjusted within each table over all its rows.", ""]
    for cname, s, c1, c0 in CONTRASTS:
        lines += [f"## {cname}: cue effect within each model", "",
                  "| model | outcome | n prompts | cue effect | 95% CI | p | p (Holm) |", "|---|---|---|---|---|---|---|"]
        block = []
        for m in MODELS:
            for o, oname, unit in OUTCOMES:
                e = effects(per, m, s, c1, c0, o)
                if e:
                    block.append((m, o, oname, unit, len(e)) + stat(list(e.values()), rng))
        for b, adj in zip(block, holm([b[-1] for b in block])):
            m, o, oname, unit, n, mu, lo, hi, p = b
            lines.append(f"| {LABEL[m]} | {oname} | {n} | {fmt(mu, unit)} | [{fmt(lo, unit)}, {fmt(hi, unit)}] | {p:.4f} | {adj:.4f} |")
            rows.append({"contrast": cname, "test": "within", "a": m, "b": "", "outcome": o, "n": n, "effect": mu, "lo": lo, "hi": hi, "p": p, "p_holm": adj})
        lines += ["", f"## {cname}: difference in cue effect between models (a − b)", "",
                  "| a − b | outcome | n prompts | cue effect a | cue effect b | difference | 95% CI | p | p (Holm) |",
                  "|---|---|---|---|---|---|---|---|---|"]
        block = []
        for a, b in PAIRS:
            for o, oname, unit in OUTCOMES:
                ea, eb = effects(per, a, s, c1, c0, o), effects(per, b, s, c1, c0, o)
                ks = [k for k in ea if k in eb]
                if ks:
                    block.append((a, b, o, oname, unit, len(ks), float(np.mean([ea[k] for k in ks])), float(np.mean([eb[k] for k in ks])))
                                 + stat([ea[k] - eb[k] for k in ks], rng))
        for bl, adj in zip(block, holm([x[-1] for x in block])):
            a, b, o, oname, unit, n, ma, mb, mu, lo, hi, p = bl
            lines.append(f"| {LABEL[a]} − {LABEL[b]} | {oname} | {n} | {fmt(ma, unit)} | {fmt(mb, unit)} | {fmt(mu, unit)} | "
                         f"[{fmt(lo, unit)}, {fmt(hi, unit)}] | {p:.4f} | {adj:.4f} |")
            rows.append({"contrast": cname, "test": "between", "a": a, "b": b, "outcome": o, "n": n, "effect": mu, "lo": lo, "hi": hi, "p": p, "p_holm": adj})
        lines.append("")
    (ROOT / "results" / "cue_behavior.md").write_text("\n".join(lines) + "\n")
    with (ROOT / "results" / "cue_behavior.csv").open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
    print("\n".join(lines))


if __name__ == "__main__":
    main()

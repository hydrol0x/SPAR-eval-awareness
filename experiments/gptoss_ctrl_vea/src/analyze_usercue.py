"""Analysis for the user-turn cue experiment (PREREG_usercue.md).

  python -m src.analyze_usercue      # writes results/usercue_summary.md and results/usercue_tests.csv
"""
from __future__ import annotations
import csv
from collections import defaultdict
from pathlib import Path

import numpy as np

from .analyze_confirm import holm
from .analyze_main import is_refusal
from .lexical_check import EVAL_TERMS, GENERIC, LABEL, MODELS, load, words
from .prompts import CUE_EXPLICIT, CUE_USER_CASUAL

ROOT = Path(__file__).resolve().parents[1]
CONDS = ["none", "dev_explicit", "user_explicit", "user_casual"]
CUE_WORDS = (words(CUE_EXPLICIT) | words(CUE_USER_CASUAL)) - GENERIC
JUDGES = [("Qwen (primary)", "judged_v4_usercue"), ("DeepSeek (robustness)", "judged_v4_j2_usercue")]
OUTCOMES = {"vea_cot": ("VEA in reasoning (v4)", "pp"), "vea_any": ("VEA anywhere (v4)", "pp"), "refusal": ("refusal rate", "pp"),
            "log_cot": ("reasoning length", "%"), "log_ans": ("answer length", "%"), "lex_cot": ("cue echo in reasoning (lexical)", "pp")}


def per_item(jdir):
    """{model: {(set, item, condition): {outcome: mean over samples}}}"""
    out = {}
    for m in MODELS:
        lab = defaultdict(dict)
        for j in load(ROOT / "results" / jdir / f"{m}.jsonl"):
            if not j.get("error"):
                lab[j["rollout_id"]][j["channel"]] = bool(j.get("verified"))
        acc = defaultdict(lambda: defaultdict(list))
        for r in load(ROOT / "rollouts" / m / "usercue.jsonl"):
            cot = r.get("reasoning") or ""
            d = acc[(r["set"], r["item_id"], r["condition"])]
            d["refusal"].append(int(is_refusal(r.get("response"))))
            d["log_cot"].append(np.log1p(len(cot))); d["log_ans"].append(np.log1p(len(r.get("response") or "")))
            d["lex_cot"].append(int(bool(EVAL_TERMS.search(cot)) or bool(CUE_WORDS & words(cot))))
            l = lab.get(r["rollout_id"], {})
            if "cot" in l and "response" in l:  # judgment failures are excluded per outcome
                d["vea_cot"].append(int(l["cot"])); d["vea_any"].append(int(l["cot"] or l["response"]))
        out[m] = {k: {o: float(np.mean(v)) for o, v in d.items() if v} for k, d in acc.items()}
    return out


def level(per, m, c, o):
    return {k[:2]: v[o] for k, v in per[m].items() if k[2] == c and o in v}


def effect(per, m, c1, c0, o):
    a, b = level(per, m, c1, o), level(per, m, c0, o)
    return {k: a[k] - b[k] for k in a if k in b}


def stat(d, rng):
    d = np.asarray(list(d))
    boots = rng.choice(d, (10000, len(d))).mean(1); flips = (rng.choice([-1, 1], (20000, len(d))) * d).mean(1)
    return {"n": len(d), "diff": float(d.mean()), "lo": float(np.percentile(boots, 2.5)), "hi": float(np.percentile(boots, 97.5)),
            "p": float((np.abs(flips) >= abs(d.mean()) - 1e-12).mean())}


def paired(x, y, rng):
    ks = [k for k in x if k in y]
    r = stat([x[k] - y[k] for k in ks], rng); r["a"] = float(np.mean([x[k] for k in ks])); r["b"] = float(np.mean([y[k] for k in ks]))
    return r


def fmt(x, unit):
    return f"{100 * x:+.1f} pp" if unit == "pp" else f"{100 * (np.exp(x) - 1):+.0f}%"


def lvl(x, unit):
    return f"{100 * x:.1f}%" if unit == "pp" else f"{np.expm1(x):.0f} chars"


def main():
    rng = np.random.default_rng(20261019)
    rows, lines = [], ["# User-turn cue experiment (PREREG_usercue.md)", ""]
    for jname, jdir in JUDGES:
        per = per_item(jdir)
        if not any(level(per, "base", "user_explicit", "vea_cot").values()) and not level(per, "base", "user_explicit", "vea_cot"):
            lines += [f"## {jname}: no judgments yet", ""]; continue
        lines += [f"## {jname}", "", "### Levels (mean over prompts)", "",
                  "| model | outcome | " + " | ".join(CONDS) + " |", "|---|---|" + "---|" * len(CONDS)]
        for m in MODELS:
            for o, (oname, unit) in OUTCOMES.items():
                vals = [level(per, m, c, o) for c in CONDS]
                lines.append(f"| {LABEL[m]} | {oname} | " + " | ".join(lvl(np.mean(list(v.values())), unit) if v else "-" for v in vals) + " |")

        def rec(test, family, desc, r, unit, o):
            rows.append({"judge": jname, "test": test, "family": family, "desc": desc, "outcome": o, **r}); r["unit"] = unit

        # P0 manipulation check
        p0 = paired(level(per, "base", "user_explicit", "vea_cot"), level(per, "base", "none", "vea_cot"), rng)
        rec("P0", "check", "base: user_explicit − none", p0, "pp", "vea_cot")
        # primary
        prim = [("P1", "cdel", "ctrldel"), ("P2", "steer", "steerctrl")]
        P = {t: paired(level(per, a, "user_explicit", "vea_cot"), level(per, b, "user_explicit", "vea_cot"), rng) for t, a, b in prim}
        for (t, a, b), adj in zip(prim, holm([P[t]["p"] for t, _, _ in prim])):
            P[t]["p_adj"] = adj; rec(t, "primary", f"{LABEL[a]} − {LABEL[b]}, user_explicit", P[t], "pp", "vea_cot")
        # secondary family
        sec = []
        for t, a, b in prim:
            sec.append((f"S1.{t[1]}", f"{LABEL[a]} − {LABEL[b]}, user_casual", "vea_cot",
                        paired(level(per, a, "user_casual", "vea_cot"), level(per, b, "user_casual", "vea_cot"), rng)))
            sec.append((f"S2.{t[1]}", f"{LABEL[a]} − {LABEL[b]}, cue effect (user_explicit − none)", "vea_cot",
                        paired(effect(per, a, "user_explicit", "none", "vea_cot"), effect(per, b, "user_explicit", "none", "vea_cot"), rng)))
            for o in ["refusal", "log_ans"]:
                sec.append((f"S3.{t[1]}-{o}", f"{LABEL[a]} − {LABEL[b]}, cue effect (user_explicit − none)", o,
                            paired(effect(per, a, "user_explicit", "none", o), effect(per, b, "user_explicit", "none", o), rng)))
        for (t, desc, o, r), adj in zip(sec, holm([s[3]["p"] for s in sec])):
            r["p_adj"] = adj; rec(t, "secondary", desc, r, OUTCOMES[o][1], o)
        lines += ["", "### Pre-registered tests", "",
                  "| test | contrast | outcome | n prompts | a | b | a − b | 95% CI | p | p (Holm, family) |", "|---|---|---|---|---|---|---|---|---|---|"]
        for x in [r for r in rows if r["judge"] == jname]:
            u = OUTCOMES[x["outcome"]][1]
            a, b = (fmt(x["a"], u), fmt(x["b"], u)) if x["test"].startswith("S2") or x["test"].startswith("S3") else (lvl(x["a"], u), lvl(x["b"], u))
            lines.append(f"| {x['test']} | {x['desc']} | {OUTCOMES[x['outcome']][0]} | {x['n']} | {a} | {b} | {fmt(x['diff'], u)} | "
                         f"[{fmt(x['lo'], u)}, {fmt(x['hi'], u)}] | {x['p']:.4f} | {x.get('p_adj', x['p']):.4f} |")
        # behaviour-preserved rule and descriptive cue effects
        lines += ["", "### Cue effects within each model (cue − none, paired by prompt; descriptive)", "",
                  "| model | cue | outcome | cue effect | 95% CI | p |", "|---|---|---|---|---|---|"]
        within = {}
        for m in MODELS:
            for c in CONDS[1:]:
                for o, (oname, unit) in OUTCOMES.items():
                    e = effect(per, m, c, "none", o)
                    if e:
                        r = stat(e.values(), rng); within[(m, c, o)] = r
                        lines.append(f"| {LABEL[m]} | {c} | {oname} | {fmt(r['diff'], unit)} | [{fmt(r['lo'], unit)}, {fmt(r['hi'], unit)}] | {r['p']:.4f} |")
        lines += ["", "### Decision: \"verbalizes less while the behavioural response is preserved\"", ""]
        for t, a, b in prim:
            ok_v = P[t]["diff"] < 0 and P[t]["p_adj"] < 0.05
            beh = []
            for o in ["refusal", "log_ans"]:
                ra, rb = within.get((a, "user_explicit", o)), within.get((b, "user_explicit", o))
                if ra and rb and rb["p"] < 0.05:
                    beh.append(f"{OUTCOMES[o][0]}: {'preserved' if ra['p'] < 0.05 and np.sign(ra['diff']) == np.sign(rb['diff']) else 'not preserved'}")
            lines.append(f"* {LABEL[a]} vs {LABEL[b]}: verbalization {'lower (P significant)' if ok_v else 'not significantly lower'}; "
                         f"behaviour {', '.join(beh) if beh else 'no significant behavioural cue effect in the control arm'}.")
        lines.append("")
    (ROOT / "results" / "usercue_summary.md").write_text("\n".join(lines) + "\n")
    if rows:
        keys = sorted({k for r in rows for k in r})
        with (ROOT / "results" / "usercue_tests.csv").open("w", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=keys); w.writeheader(); w.writerows(rows)
    print("\n".join(lines))


if __name__ == "__main__":
    main()

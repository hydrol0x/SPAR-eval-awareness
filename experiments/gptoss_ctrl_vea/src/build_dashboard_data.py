"""Build the JSON datasets behind the results dashboard (one file per source) in results/dashboard/.

  python -m src.build_dashboard_data
"""
from __future__ import annotations
import csv, json, re
from collections import defaultdict
from pathlib import Path

import numpy as np

from .analyze_v4 import rollout_labels, per_prompt as v4_per_prompt, kappa
from .verify_excerpts import verified_labels
from .grade_ctrl import grade
from .analyze_steer import is_refusal

ROOT = Path(__file__).resolve().parents[1]
OLMO = ROOT.parent / "olmo_cot_control"
OUT = ROOT / "results" / "dashboard"
ARMS = ["base", "ctrldel", "cdel", "steerctrl", "steer", "steerrand"]
LABEL = {"base": "Base", "ctrldel": "Control LoRA", "cdel": "Compliant LoRA", "steerctrl": "Control vector",
         "steer": "Steering vector", "steerrand": "Random vector"}
REPL = {("luxel_pairs", "eval_like"), ("eab_safety_base", "explicit")}
CELLNAME = {("luxel_pairs", "eval_like"): "Luxel eval-framed", ("eab_safety_base", "explicit"): "Safety + system cue",
            ("eab_cap_base", "explicit"): "Capability + system cue"}
rng = np.random.default_rng(31)


def load(p):
    out = []
    if p.exists():
        for l in p.read_text().splitlines():
            try:
                out.append(json.loads(l))
            except json.JSONDecodeError:
                pass
    return out


def r4(x):
    return None if x is None or (isinstance(x, float) and np.isnan(x)) else round(float(x), 4)


def wilson(k, n, z=1.96):
    if n == 0:
        return (None, None)
    p = k / n; d = 1 + z * z / n; c = p + z * z / (2 * n); h = z * np.sqrt((p * (1 - p) + z * z / (4 * n)) / n)
    return (max(0.0, (c - h) / d), min(1.0, (c + h) / d))


def dump(name, rows):
    (OUT / f"{name}.json").write_text(json.dumps(rows, indent=0))
    print(f"{name}: {len(rows)} rows, {(OUT / f'{name}.json').stat().st_size // 1024} KB")


def olmo():
    s = list(csv.DictReader((OLMO / "results" / "summary_by_checkpoint.csv").open()))
    g = {(r["pipeline"], r["revision"]): r for r in csv.DictReader((OLMO / "results" / "graded_by_checkpoint.csv").open())}
    nice = {"Olmo-3-1025-7B": "7B base", "RLZero-IF": "RL-Zero IF", "RLZero-Math": "RL-Zero Math", "RLZero-Code": "RL-Zero Code",
            "RLZero-Mix": "RL-Zero Mix", "RLZero-General": "RL-Zero General", "Think": "7B Think RLVR", "Think-SFT": "7B Think SFT",
            "Think-DPO": "7B Think DPO", "Olmo-3-1125-32B": "32B base", "Think32B": "32B Think RLVR", "Think32B-SFT": "32B Think SFT",
            "Think32B-DPO": "32B Think DPO", "Think32B-3.1": "32B Think 3.1 (RLVR cont.)"}
    rows = []
    for r in s:
        gg = g.get((r["pipeline"], r["revision"]), {})
        f = lambda k, src=r: r4(float(src[k])) if src.get(k) not in (None, "", "nan") else None
        plot = r["plot_step"]
        rows.append({"ckpt": f"{r['pipeline']}@{r['revision']}", "size": "32B" if "32B" in r["pipeline"] else "7B",
                     "pipeline": nice.get(r["pipeline"], r["pipeline"]), "revision": r["revision"],
                     "step": None if not plot else int(float(plot)),
                     "stage": "base" if "base" in nice.get(r["pipeline"], "") else ("SFT" if "SFT" in r["pipeline"] else "DPO" if "DPO" in r["pipeline"] else "RL"),
                     "valid_ctrl": f("cot_controllability_valid"), "valid_lo": f("cot_ctrl_valid_lo"), "valid_hi": f("cot_ctrl_valid_hi"),
                     "raw_ctrl": f("cot_controllability"), "output_ctrl": f("output_controllability"), "tag_start": f("ctrl_tag_start"),
                     "tag_anywhere": f("tag_anywhere_rate", gg), "word_rel_reduction": f("word_rel_reduction", gg),
                     "vea": f("vea_rate_all"), "vea_lo": f("vea_lo"), "vea_hi": f("vea_hi"),
                     "reasoning_words": r4(float(r["mean_reasoning_words"])) if r.get("mean_reasoning_words") else None})
    dump("olmo_checkpoints", rows)


def pilot():
    rows = []
    for r in csv.DictReader((ROOT / "results" / "pilot_summary.csv").open()):
        rows.append({"cell": f"{r['set']}|{r['condition']}", "set": r["set"], "condition": r["condition"], "n": int(r["n"]),
                     "vea_any": r4(float(r["vea_any"])), "vea_lo": r4(float(r["vea_lo"])), "vea_hi": r4(float(r["vea_hi"])),
                     "cue_uptake": r4(float(r["vea_cue"])), "spontaneous": r4(float(r["vea_spont"]))})
    dump("pilot_sets", rows)


def ctrl_check():
    split = {"all_caps": "train", "all_lower": "train", "bullet": "held-out", "numbered": "held-out", "no_word_so": "held-out"}
    nice = {"all_caps": "All caps", "all_lower": "All lowercase", "bullet": "Bulleted list", "numbered": "Numbered list", "no_word_so": "Avoid “so”"}
    rows = []
    for a in ARMS:
        cc = load(ROOT / "rollouts" / a / "ctrl_check.jsonl")
        for ins in split:
            v = [r for r in cc if r["condition"] == ins]
            k = sum(1 for r in v if grade(ins, r["reasoning"])[0]); lo, hi = wilson(k, len(v))
            rows.append({"key": f"{a}|{ins}", "arm": LABEL[a], "instruction": nice[ins], "split": split[ins], "n": len(v),
                         "compliance": r4(k / len(v)), "lo": r4(lo), "hi": r4(hi)})
    dump("ctrl_check", rows)


def boot_ci(vals):
    v = np.array(vals); b = rng.choice(v, (5000, len(v))).mean(1)
    return float(v.mean()), float(np.percentile(b, 2.5)), float(np.percentile(b, 97.5))


def v4_rates():
    rows = []
    for jname, jdir in [("Qwen", "judged_v4"), ("DeepSeek", "judged_v4_j2")]:
        for a in ARMS:
            pp = v4_per_prompt(rollout_labels(a, jdir))
            for cell, cname in CELLNAME.items():
                ks = [k for k in pp if (k[0], k[2]) == cell]
                if not ks:
                    continue
                m, lo, hi = boot_ci([pp[k]["in_cot"] for k in ks])
                rows.append({"key": f"{jname}|{a}|{cname}", "judge": jname, "arm": LABEL[a], "cell": cname, "n_prompts": len(ks),
                             "in_cot": r4(m), "lo": r4(lo), "hi": r4(hi),
                             "anywhere": r4(np.mean([pp[k]["anywhere"] for k in ks])), "answer_only": r4(np.mean([pp[k]["answer_only"] for k in ks]))})
    dump("v4_rates", rows)


def v3_labels(arm, verify):
    acc = defaultdict(lambda: defaultdict(list))
    for f, d in [("main", "judged"), ("confirm", "judged_confirm")]:
        roll = {r["rollout_id"]: r for r in load(ROOT / "rollouts" / arm / f"{f}.jsonl")}
        for j in load(ROOT / "results" / d / f"{arm}.jsonl"):
            if j.get("error") or j["rollout_id"] not in roll:
                continue
            r = roll[j["rollout_id"]]; k = (r["set"], r["item_id"], r["condition"])
            if verify:
                v = verified_labels(j, r); c, ao, an = v["in_cot"], v["answer_only"], v["anywhere"]
            else:
                ex = [e for e in ((j.get("excerpts") or []) if j.get("eval_aware") else []) if isinstance(e, dict)]
                c = int(any(e.get("location") == "cot" for e in ex)); an = int(bool(j.get("eval_aware"))); ao = int(an and not c)
            acc[k]["in_cot"].append(c); acc[k]["answer_only"].append(ao); acc[k]["anywhere"].append(an)
    return {k: {o: float(np.mean(v[o])) for o in v} for k, v in acc.items()}


def lexical_pp(arm):
    from .lexical_check import luxel_cues, words, EVAL_TERMS, GENERIC
    from .prompts import CUE_EXPLICIT
    lux = luxel_cues(); explicit = words(CUE_EXPLICIT) - GENERIC
    acc = defaultdict(list)
    for f in ["main", "confirm"]:
        for r in load(ROOT / "rollouts" / arm / f"{f}.jsonl"):
            if (r["set"], r["condition"]) not in REPL | {("eab_cap_base", "explicit")}:
                continue
            cue = lux.get(r["item_id"], set()) if r["set"] == "luxel_pairs" else explicit
            t = r.get("reasoning")
            acc[(r["set"], r["item_id"], r["condition"])].append(int(bool(EVAL_TERMS.search(t or "")) or bool(cue & words(t))))
    return {k: {"in_cot": float(np.mean(v))} for k, v in acc.items()}


def paired(pa, pb, cells, o):
    ks = [k for k in pa if k in pb and (k[0], k[2]) in cells]
    d = np.array([pa[k][o] - pb[k][o] for k in ks])
    b = rng.choice(d, (5000, len(d))).mean(1); fl = (rng.choice([-1, 1], (10000, len(d))) * d).mean(1)
    return float(d.mean()), float(np.percentile(b, 2.5)), float(np.percentile(b, 97.5)), float((np.abs(fl) >= abs(d.mean()) - 1e-12).mean()), len(ks)


def contrasts_and_artifact():
    measures = {
        "v4 judge (Qwen)": lambda a: v4_per_prompt(rollout_labels(a, "judged_v4")),
        "v4 judge (DeepSeek)": lambda a: v4_per_prompt(rollout_labels(a, "judged_v4_j2")),
        "Text search (no judge)": lexical_pp,
        "v3 judge, verified quotes": lambda a: v3_labels(a, True),
        "v3 judge, raw": lambda a: v3_labels(a, False),
    }
    pairs = [("cdel", "ctrldel", "Compliant LoRA − control LoRA"), ("steer", "steerctrl", "Steering vector − control vector"),
             ("ctrldel", "base", "Control LoRA − base"), ("steerctrl", "base", "Control vector − base"), ("steerrand", "base", "Random vector − base")]
    cache, rows = {}, []
    for mname, fn in measures.items():
        for a in ARMS:
            cache[(mname, a)] = fn(a)
        for for_cells, cname in [({("luxel_pairs", "eval_like")}, "Luxel eval-framed"), (REPL, "Luxel + safety cue prompts")]:
            for a, b, label in pairs:
                d, lo, hi, p, n = paired(cache[(mname, a)], cache[(mname, b)], for_cells, "in_cot")
                rows.append({"key": f"{mname}|{label}|{cname}", "measure": mname, "contrast": label, "cells": cname, "n_prompts": n,
                             "diff": r4(d), "lo": r4(lo), "hi": r4(hi), "p": r4(p)})
    dump("contrasts", rows)
    art = []
    for a in ARMS:
        raw, ver = cache[("v3 judge, raw", a)], cache[("v3 judge, verified quotes", a)]
        ks = [k for k in raw if (k[0], k[2]) in REPL and k in ver]
        art.append({"arm": LABEL[a], "answer_only_raw": r4(np.mean([raw[k]["answer_only"] for k in ks])),
                    "answer_only_verified": r4(np.mean([ver[k]["answer_only"] for k in ks])),
                    "in_cot_raw": r4(np.mean([raw[k]["in_cot"] for k in ks])), "in_cot_verified": r4(np.mean([ver[k]["in_cot"] for k in ks])),
                    "in_cot_v4": r4(np.mean([v["in_cot"] for k, v in cache[("v4 judge (Qwen)", a)].items() if (k[0], k[2]) in REPL]))})
    dump("v3_artifact", art)


def agreement():
    rows = []
    # v3: main-run cue rollouts judged by both v3 judges (LoRA arms only)
    for a in ["base", "ctrldel", "cdel"]:
        j1 = {j["rollout_id"]: j for j in load(ROOT / "results" / "judged" / f"{a}.jsonl") if not j.get("error")}
        j2 = {j["rollout_id"]: j for j in load(ROOT / "results" / "judged_j2" / f"{a}.jsonl") if not j.get("error")}
        lab = lambda j: (lambda ex, an: {"In reasoning": int(any(e.get("location") == "cot" for e in ex)), "Anywhere": int(an),
                                         "Final answer only": int(an and not any(e.get("location") == "cot" for e in ex))})(
            [e for e in ((j.get("excerpts") or []) if j.get("eval_aware") else []) if isinstance(e, dict)], bool(j.get("eval_aware")))
        ids = [k for k in j1 if k in j2]
        for o in ["In reasoning", "Anywhere", "Final answer only"]:
            k, po = kappa([lab(j1[i])[o] for i in ids], [lab(j2[i])[o] for i in ids])
            rows.append({"key": f"v3|{a}|{o}", "judge_version": "v3 (sees prompt)", "arm": LABEL[a], "label": o, "n": len(ids), "kappa": r4(k), "agreement": r4(po)})
    for a in ARMS:
        q, d = rollout_labels(a, "judged_v4"), rollout_labels(a, "judged_v4_j2")
        ids = [i for i in q if i in d]
        for o, key in [("In reasoning", "in_cot"), ("Anywhere", "anywhere"), ("Final answer only", "answer_only")]:
            k, po = kappa([q[i][1][key] for i in ids], [d[i][1][key] for i in ids])
            rows.append({"key": f"v4|{a}|{o}", "judge_version": "v4 (channel-blind)", "arm": LABEL[a], "label": o, "n": len(ids), "kappa": r4(k), "agreement": r4(po)})
    dump("judge_agreement", rows)


def refusal_and_narration():
    rows, nar = [], []
    nice = {("eab_safety_base", "none"): "Safety prompt, no cue", ("eab_safety_base", "explicit"): "Safety prompt + system cue",
            ("eab_safety_all8", "none"): "Safety prompt, all cue factors"}
    W = re.compile(r"[a-z0-9']+")
    grams = lambda s: (lambda w: {tuple(w[i:i + 6]) for i in range(len(w) - 5)})(W.findall((s or "").lower()))
    instr = re.compile(r"(formatting requirement|format(ting)? (instruction|requirement)|requirement for (the|your|our) reasoning|chain of thought|all caps|all capital|capital letters|uppercase|lowercase|lower[- ]case|bullet|numbered list|the word \"?so\"?|instruction says|they want (the|our) reasoning|reasoning must|we must write (our|the) reasoning)", re.I)
    for a in ARMS:
        main = load(ROOT / "rollouts" / a / "main.jsonl")
        for cell, cname in nice.items():
            v = [r for r in main if (r["set"], r["condition"]) == cell]
            k = sum(is_refusal(r["response"]) for r in v); lo, hi = wilson(k, len(v))
            rows.append({"key": f"{a}|{cname}", "arm": LABEL[a], "condition": cname, "n": len(v), "refusal": r4(k / len(v)), "lo": r4(lo), "hi": r4(hi)})
        cc = [r for r in load(ROOT / "rollouts" / a / "ctrl_check.jsonl") if r["condition"] != "baseline"]
        lux_n = [r for r in main if (r["set"], r["condition"]) == ("luxel_pairs", "deploy_like")]
        lux_e = [r for r in main if (r["set"], r["condition"]) == ("luxel_pairs", "eval_like")]
        q = lambda v: np.mean([bool(grams((r.get("system") or "") + " " + r["user"]) & grams(r["reasoning"])) for r in v])
        nar.append({"arm": LABEL[a], "instruction_talk": r4(np.mean([bool(instr.search(r["reasoning"])) for r in cc])),
                    "quotes_prompt_normal": r4(q(lux_n)), "quotes_prompt_eval": r4(q(lux_e)),
                    "reasoning_words": r4(np.mean([len(r["reasoning"].split()) for r in main]))})
    dump("refusals", rows); dump("narration", nar)


def prereg():
    rows = []
    def md_rows(path, exp):
        for l in (ROOT / "results" / path).read_text().splitlines():
            if not l.startswith("| ") or l.startswith("| test") or l.startswith("| experiment") or "---" in l:
                continue
            c = [x.strip() for x in l.strip("|").split("|")]
            yield c
    for c in md_rows("confirm_summary.md", "rerun"):
        if c[0][:2] in ("H1", "H2", "G1", "G2"):
            rows.append({"key": f"confirm|{c[0]}", "experiment": "Fine-tune rerun (v3 judge, original plan)", "test": c[0], "outcome": c[1], "cells": c[2],
                         "a": c[3], "b": c[4], "diff": c[5], "ci": c[6], "p_adj": c[8], "result": c[9]})
        if len(rows) >= 4:
            break
    for c in md_rows("steer_summary.md", "steer"):
        if c[0][:2] in ("P1", "S1", "S2", "S3"):
            rows.append({"key": f"steer|{c[0]}", "experiment": "Steering (v3 judge, original plan)", "test": c[0], "outcome": c[1], "cells": c[2],
                         "a": c[3], "b": c[4], "diff": c[5], "ci": c[6], "p_adj": c[8], "result": "significant" if float(c[8]) < 0.05 else "not significant"})
    for c in md_rows("amended_tests.md", "amended"):
        if len(c) >= 13 and c[2].startswith("Qwen"):
            rows.append({"key": f"amended|{c[1]}", "experiment": ("Fine-tune rerun" if "rerun" in c[0] else "Steering") + " (v4 judge, amendment)",
                         "test": c[1], "outcome": c[3], "cells": c[4], "a": c[6], "b": c[7], "diff": c[8], "ci": c[9], "p_adj": c[11], "result": c[12]})
    dump("prereg_tests", rows)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    olmo(); pilot(); ctrl_check(); v4_rates(); contrasts_and_artifact(); agreement(); refusal_and_narration(); prereg()


if __name__ == "__main__":
    main()

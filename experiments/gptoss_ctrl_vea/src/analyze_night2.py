"""Night-2 analysis (PREREG_night2.md). Team-judge labels (results/judge_dabal/labels.jsonl: VEA, causal chain; eval gaming dropped, amendment 2)
plus refusal from the provisional judge (results/exp1_judge/labels_qwen.jsonl). Sample 0, adversarial FORTRESS, paired by
prompt; bootstrap 95% CIs over prompts, sign-flip p.

  python -m src.analyze_night2      # -> results/night2_summary.md
"""
from __future__ import annotations
import json
from collections import defaultdict
from pathlib import Path

import numpy as np

from .exp1_judge import load

ROOT = Path(__file__).resolve().parents[1]
ARMS = ["base", "edited", "control", "steer_edited", "steer_control"]
EXP1_CUES = ["sys_explicit", "user_explicit", "sys_hint", "user_hint", "sys_metr", "user_metr", "user_casual"]
PRESSURE = ["none", "sys_explicit", "user_explicit", "sys_explicit_suppress", "user_explicit_suppress",
            "sys_monitor", "user_monitor", "sys_punish", "user_punish"]


def stat(d, rng):
    d = np.asarray(d, float); b = rng.choice(d, (10000, len(d))).mean(1); f = (rng.choice([-1, 1], (20000, len(d))) * d).mean(1)
    return d.mean(), np.percentile(b, 2.5), np.percentile(b, 97.5), float((np.abs(f) >= abs(d.mean()) - 1e-12).mean())


def fmt(r):
    return f"{100 * r[0]:+.1f} pp [{100 * r[1]:+.1f}, {100 * r[2]:+.1f}] (p={r[3]:.3f})"


def main():
    rng = np.random.default_rng(42)
    dab = {j["rollout_id"]: j for j in load(ROOT / "results" / "judge_dabal" / "labels.jsonl")}
    qw = {j["rollout_id"]: j for j in load(ROOT / "results" / "exp1_judge" / "labels_qwen.jsonl")}
    # cell[arm][item][condition] -> dict of labels for sample 0 (adversarial)
    cell = {a: defaultdict(dict) for a in ARMS}
    for a in ARMS:
        for f in sorted((ROOT / "rollouts" / f"olmo31_exp1_{a}").glob("exp1*.jsonl")):
            for r in load(f):
                if r.get("error") or r["sample"] != 0 or r["set"] != "fortress_adv" or r["rollout_id"] not in dab:
                    continue
                d, q = dab[r["rollout_id"]], qw.get(r["rollout_id"])
                beh = q["behavior"] if q else None
                cell[a][r["item_id"]][r["condition"]] = {
                    "vea": int(d["vea"]), "chain": None if d["chain"] is None else int(d["chain"]),
                    "chain_all": int(bool(d["chain"])), "vea_qwen": int(q["eval_aware"]) if q else None,
                    "refuse": None if beh not in ("refuse", "partial", "comply") else int(beh == "refuse")}

    def rate(a, conds, k):
        v = [x[c][k] for x in cell[a].values() for c in conds if c in x and x[c][k] is not None]
        return (np.mean(v), len(v)) if v else (None, 0)

    def per_item(a, conds, k):
        out = {}
        for it, x in cell[a].items():
            v = [x[c][k] for c in conds if c in x and x[c][k] is not None]
            if v:
                out[it] = np.mean(v)
        return out

    def uplift(a, conds, k="refuse", quiet=False):
        out = {}
        for it, x in cell[a].items():
            if "none" not in x or x["none"]["refuse"] is None:
                continue
            v = [x[c]["refuse"] for c in conds if c in x and x[c]["refuse"] is not None and (not quiet or x[c]["vea"] == 0)]
            if v:
                out[it] = np.mean(v) - x["none"]["refuse"]
        return out

    def diff(da, db):
        d = [da[k] - db[k] for k in da if k in db]
        return (*stat(d, rng), len(d)) if len(d) >= 10 else None

    n = {a: sum(len(x) for x in cell[a].values()) for a in ARMS}
    L = ["# Night 2: team judge, pressure test, steering arms (PREREG_night2.md)", "",
         "VEA = Goodfire template; chain = our question on VEA-positive rollouts (\"this may be a "
         "test\" → \"so I should …\"); all with Qwen2.5-72B (FP8) and verified quotes. Refusal = provisional Exp1 judge. "
         "Adversarial FORTRESS, sample 0, paired by prompt.", "",
         "Labelled rollouts: " + ", ".join(f"{a} {n[a]}" for a in ARMS), ""]

    # 1. judges compared on Exp1 rollouts
    L += ["## 1. Team judge vs provisional judge (Exp1 rollouts, VEA)", "", "| condition | n | team (Goodfire) | provisional | agreement | Cohen's kappa |",
          "|---|---|---|---|---|---|"]
    for c in ["none"] + EXP1_CUES:
        pr = [(x[c]["vea"], x[c]["vea_qwen"]) for a in ("base", "edited", "control") for x in cell[a].values() if c in x and x[c]["vea_qwen"] is not None]
        if not pr:
            continue
        t, q = np.array(pr).T; po = (t == q).mean(); pe = t.mean() * q.mean() + (1 - t.mean()) * (1 - q.mean())
        L.append(f"| {c} | {len(pr)} | {100 * t.mean():.1f}% | {100 * q.mean():.1f}% | {100 * po:.1f}% | {(po - pe) / (1 - pe) if pe < 1 else float('nan'):.2f} |")

    # 2. Exp1 re-judged
    L += ["", "## 2. Experiment 1 re-judged (pooled over the 7 cues)", "", "| arm | VEA no cue | VEA under cue | P(chain \\| VEA) under cue | refusal uplift (cue − none) |",
          "|---|---|---|---|---|"]
    for a in ("base", "edited", "control"):
        up = uplift(a, EXP1_CUES)
        L.append(f"| {a} | {100 * (rate(a, ['none'], 'vea')[0] or 0):.1f}% | {100 * (rate(a, EXP1_CUES, 'vea')[0] or 0):.1f}% | "
                 f"{100 * (rate(a, EXP1_CUES, 'chain')[0] or 0):.1f}% (n={rate(a, EXP1_CUES, 'chain')[1]}) | "
                 f"{100 * np.mean(list(up.values())):+.1f} pp |")
    L += ["", "| contrast | measure | difference |", "|---|---|---|"]
    for x, y in (("edited", "control"), ("edited", "base"), ("control", "base")):
        for k, name in (("vea", "VEA under cue"), ("chain_all", "VEA with a stated chain, under cue")):
            r = diff(per_item(x, EXP1_CUES, k), per_item(y, EXP1_CUES, k))
            if r:
                L.append(f"| {x} − {y} | {name} | {fmt(r)} (n={r[4]}) |")
        r = diff(uplift(x, EXP1_CUES), uplift(y, EXP1_CUES))
        if r:
            L.append(f"| {x} − {y} | refusal uplift | {fmt(r)} (n={r[4]}) |")
        r = diff(per_item(x, ["none"], "vea"), per_item(y, ["none"], "vea"))
        if r:
            L.append(f"| {x} − {y} | VEA, no cue (baseline) | {fmt(r)} (n={r[4]}) |")

    # 3. pressure test
    L += ["", "## 3. Pressure test: propensity vs capability to hide eval awareness", "",
          "| arm | condition | n | refusal | VEA | P(chain \\| VEA) | refusal uplift vs none | uplift among non-verbalizing |",
          "|---|---|---|---|---|---|---|---|"]
    for a in ARMS:
        for c in PRESSURE:
            rr, nn = rate(a, [c], "refuse")
            if not nn:
                continue
            up, uq = uplift(a, [c]), uplift(a, [c], quiet=True)
            ch = rate(a, [c], "chain")[0]
            L.append(f"| {a} | {c} | {nn} | {100 * rr:.1f}% | {100 * rate(a, [c], 'vea')[0]:.1f}% | "
                     f"{'-' if ch is None else f'{100 * ch:.1f}%'} | "
                     f"{'-' if c == 'none' or not up else f'{100 * np.mean(list(up.values())):+.1f} pp'} | "
                     f"{'-' if c == 'none' or not uq else f'{100 * np.mean(list(uq.values())):+.1f} pp'} |")
    L += ["", "Key contrasts (treated − matched control):", "", "| contrast | condition | VEA | refusal uplift vs none |", "|---|---|---|---|"]
    for x, y in (("edited", "control"), ("steer_edited", "steer_control")):
        for c in PRESSURE[1:]:
            rv = diff(per_item(x, [c], "vea"), per_item(y, [c], "vea")); ru = diff(uplift(x, [c]), uplift(y, [c]))
            if rv or ru:
                L.append(f"| {x} − {y} | {c} | {fmt(rv) if rv else '-'} | {fmt(ru) if ru else '-'} |")
    L += ["", "Within arm: pressure cue vs the plain explicit cue (same placement), VEA:", "", "| arm | contrast | VEA difference |", "|---|---|---|"]
    for a in ARMS:
        for c, ref in (("sys_monitor", "sys_explicit"), ("user_monitor", "user_explicit"), ("sys_punish", "sys_explicit"), ("user_punish", "user_explicit"),
                       ("sys_explicit_suppress", "sys_explicit"), ("user_explicit_suppress", "user_explicit")):
            r = diff(per_item(a, [c], "vea"), per_item(a, [ref], "vea"))
            if r:
                L.append(f"| {a} | {c} − {ref} | {fmt(r)} |")

    # 4. steering arms' controllability
    rows = load(ROOT / "results" / "exp1_cotcheck_rows.jsonl")
    L += ["", "## 4. CoT controllability of all arms (ReasonIF trained rules, 195 prompts, 1 sample)", "", "| arm | n | rule followed | finished |", "|---|---|---|---|"]
    for a in ("edited", "control", "steer_edited", "steer_control"):
        x = [r for r in rows if r["arm"] == a]
        if x:
            L.append(f"| {a} | {len(x)} | {100 * np.mean([r['pass'] for r in x]):.1f}% | {100 * np.mean([r['finished'] for r in x]):.1f}% |")
    (ROOT / "results" / "night2_summary.md").write_text("\n".join(L) + "\n"); print("\n".join(L))


if __name__ == "__main__":
    main()

"""Analysis with the channel-blind, quote-verified v4 judge (both judges), for the LoRA and steering arms.

A rollout mentions eval awareness in a channel only if that channel's v4 judgment is positive AND its quote is found in
that channel's text. Outcomes: in_cot, answer_only (reply positive, reasoning not), anywhere.

  python -m src.analyze_v4     # writes results/v4_summary.md, results/v4_tests.csv, figures/v4_in_cot.png
"""
from __future__ import annotations
import csv, json
from collections import defaultdict
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
ARMS = ["base", "ctrldel", "cdel", "steerctrl", "steer", "steerrand"]
LABEL = {"base": "base", "ctrldel": "control LoRA", "cdel": "compliant LoRA", "steerctrl": "control vector",
         "steer": "steering vector", "steerrand": "random vector"}
COLOR = {"base": "#2a78d6", "ctrldel": "#eb6834", "cdel": "#1baf7a", "steerctrl": "#eda100", "steer": "#e87ba4", "steerrand": "#6250d6"}
REPL = {("luxel_pairs", "eval_like"), ("eab_safety_base", "explicit")}
GEN = {("eab_cap_base", "explicit")}
JUDGES = {"Qwen": "judged_v4", "DeepSeek": "judged_v4_j2"}
CONTRASTS = [("cdel", "ctrldel"), ("cdel", "base"), ("ctrldel", "base"), ("steer", "steerctrl"), ("steer", "base"),
             ("steerctrl", "base"), ("steerrand", "base")]


def load(p):
    out = []
    if p.exists():
        for l in p.read_text().splitlines():
            try:
                out.append(json.loads(l))
            except json.JSONDecodeError:
                pass
    return out


def rollout_labels(arm, jdir):
    ch = defaultdict(dict)
    for j in load(ROOT / "results" / jdir / f"{arm}.jsonl"):
        if not j.get("error"):
            ch[j["rollout_id"]][j["channel"]] = (bool(j.get("verified")), (j["set"], j["item_id"], j["condition"]))
    out = {}
    for rid, d in ch.items():
        if "cot" in d and "response" in d:
            c, a, key = d["cot"][0], d["response"][0], d["cot"][1]
            out[rid] = (key, {"in_cot": int(c), "answer_only": int(a and not c), "anywhere": int(a or c)})
    return out


def per_prompt(lab):
    acc = defaultdict(lambda: defaultdict(list))
    for rid, (k, v) in lab.items():
        for o, x in v.items():
            acc[k][o].append(x)
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


def kappa(x, y):
    x, y = np.array(x), np.array(y)
    if len(x) == 0:
        return float("nan"), float("nan")
    po = (x == y).mean(); pe = x.mean() * y.mean() + (1 - x.mean()) * (1 - y.mean())
    return ((po - pe) / (1 - pe) if pe < 1 else float("nan")), po


def main():
    rng = np.random.default_rng(404)
    labs = {j: {a: rollout_labels(a, d) for a in ARMS} for j, d in JUDGES.items()}
    # combined labels: both judges agree (AND)
    labs["both agree"] = {}
    for a in ARMS:
        q, d = labs["Qwen"][a], labs["DeepSeek"][a]
        labs["both agree"][a] = {rid: (q[rid][0], {o: int(q[rid][1][o] and d[rid][1][o]) for o in q[rid][1]}) for rid in q if rid in d}
    pp = {j: {a: per_prompt(labs[j][a]) for a in ARMS} for j in labs}
    present = [a for a in ARMS if labs["Qwen"][a]]
    lines = ["# Channel-blind, quote-verified VEA judge (v4): LoRA and steering arms", "",
             "Each channel of the model output (reasoning, final reply) is judged on its own, without the prompt; a positive "
             "counts only if the judge's quote is found in that channel. Cue conditions only. Judges: qwen/qwen-2.5-72b-instruct "
             "and deepseek/deepseek-v3.2 (same v4 prompt).", "",
             "Judged rollouts (Qwen): " + ", ".join(f"{LABEL[a]} {len(labs['Qwen'][a])}" for a in present), "",
             "## Judge agreement (per rollout and channel, verified labels)", "", "| arm | channel | n | Qwen rate | DeepSeek rate | agreement | kappa |", "|---|---|---|---|---|---|---|"]
    for a in present:
        q, d = labs["Qwen"][a], labs["DeepSeek"][a]
        ids = [r for r in q if r in d]
        for o in ["in_cot", "anywhere"]:
            x = [q[r][1][o] for r in ids]; y = [d[r][1][o] for r in ids]
            k, po = kappa(x, y)
            if ids:
                lines.append(f"| {LABEL[a]} | {o} | {len(ids)} | {np.mean(x):.1%} | {np.mean(y):.1%} | {po:.1%} | {k:.2f} |")
    lines += ["", "## Rates (mean over prompts of per-prompt rates)", "", "| cells | arm | judge | n prompts | in CoT | answer only | anywhere |", "|---|---|---|---|---|---|---|"]
    for cname, cells in [("replication cue cells", REPL), ("capability + cue", GEN)]:
        for a in present:
            for j in ["Qwen", "DeepSeek"]:
                ks = [k for k in pp[j][a] if (k[0], k[2]) in cells]
                if ks:
                    f = lambda o: np.mean([pp[j][a][k][o] for k in ks])
                    lines.append(f"| {cname} | {LABEL[a]} | {j} | {len(ks)} | {f('in_cot'):.1%} | {f('answer_only'):.1%} | {f('anywhere'):.1%} |")
    rows = []
    lines += ["", "## Contrasts (per-prompt means over all samples, sign-flip permutation p, bootstrap 95% CI)", "",
              "| cells | outcome | contrast | judge | n prompts | a | b | difference | 95% CI | p |", "|---|---|---|---|---|---|---|---|---|---|"]
    for cname, cells in [("replication cue cells", REPL), ("capability + cue", GEN)]:
        for o in ["in_cot", "answer_only", "anywhere"]:
            for a, b in CONTRASTS:
                if a not in present or b not in present:
                    continue
                for j in ["Qwen", "DeepSeek", "both agree"]:
                    r = test(pp[j][a], pp[j][b], cells, o, rng)
                    if r:
                        r.update({"cells": cname, "outcome": o, "contrast": f"{a}-{b}", "judge": j}); rows.append(r)
                        lines.append(f"| {cname} | {o} | {LABEL[a]} − {LABEL[b]} | {j} | {r['n']} | {r['a']:.1%} | {r['b']:.1%} | "
                                     f"{100 * r['diff']:+.1f} pp | [{100 * r['lo']:+.1f}, {100 * r['hi']:+.1f}] | {r['p']:.4f} |")
    (ROOT / "results" / "v4_summary.md").write_text("\n".join(lines) + "\n")
    if rows:
        with (ROOT / "results" / "v4_tests.csv").open("w", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
    # figure: in-CoT rate by arm, replication cue cells, both judges
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, axes = plt.subplots(1, 2, figsize=(10, 4), facecolor="#fcfcfb", sharey=True)
    for ax, j in zip(axes, ["Qwen", "DeepSeek"]):
        ax.set_facecolor("#fcfcfb")
        xs, vals, los, his, cols = [], [], [], [], []
        for i, a in enumerate(present):
            ks = [k for k in pp[j][a] if (k[0], k[2]) in REPL]
            if not ks:
                continue
            v = np.array([pp[j][a][k]["in_cot"] for k in ks]); bo = rng.choice(v, (5000, len(v))).mean(1)
            xs.append(i); vals.append(v.mean()); los.append(v.mean() - np.percentile(bo, 2.5)); his.append(np.percentile(bo, 97.5) - v.mean()); cols.append(COLOR[a])
        ax.bar(xs, vals, color=cols, width=0.7, edgecolor="#fcfcfb", linewidth=2, zorder=2)
        ax.errorbar(xs, vals, yerr=[los, his], fmt="none", ecolor="#52514e", elinewidth=1, capsize=2, zorder=3)
        ax.set_xticks(xs); ax.set_xticklabels([LABEL[present[i]].replace(" ", "\n", 1) for i in xs], fontsize=9, color="#52514e")
        ax.set_title(f"judge: {j}", loc="left", fontsize=10, color="#0b0b0b")
        ax.grid(axis="y", color="#e6e5e0", linewidth=0.8, zorder=0); ax.set_axisbelow(True)
        for sp in ("top", "right"):
            ax.spines[sp].set_visible(False)
        ax.yaxis.set_major_formatter(matplotlib.ticker.PercentFormatter(1.0))
    axes[0].set_ylabel("cue mentioned inside the reasoning", color="#52514e")
    fig.suptitle("Eval-cue mentions in the CoT (v4 judge, quote-verified), cue prompts", x=0.01, ha="left", fontsize=11)
    fig.tight_layout(); fig.savefig(ROOT / "figures" / "v4_in_cot.png", dpi=160); plt.close(fig)
    print("\n".join(lines[:40]))


if __name__ == "__main__":
    main()

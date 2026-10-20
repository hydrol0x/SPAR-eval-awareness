"""Figure for README section 13: graded compliance under the eval cue, base Olmo-3.1-32B-Think.

  python -m src.plot_graded      # writes figures/graded_olmo31.png
"""
import json
from collections import defaultdict
from pathlib import Path

import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt, numpy as np
from matplotlib.patches import Patch

ROOT = Path(__file__).resolve().parents[1]
ARM = "olmo31_32b_think"
BLUE, ORANGE, SURF, INK, INK2, GRID = "#2a78d6", "#eb6834", "#fcfcfb", "#0b0b0b", "#52514e", "#e4e3df"


def load(p):
    return [json.loads(l) for l in open(p) if l.strip()]


def boot(v, rng):
    v = np.asarray(v); b = rng.choice(v, (5000, len(v))).mean(1)
    return v.mean(), v.mean() - np.percentile(b, 2.5), np.percentile(b, 97.5) - v.mean()


def main():
    rng = np.random.default_rng(3)
    sr = {j["rollout_id"]: j for j in load(ROOT / "results/judged_strongreject" / f"{ARM}__graded_main.jsonl") if not j.get("error")}
    vea = {j["rollout_id"]: bool(j.get("verified")) for j in load(ROOT / "results/judged_v4_graded" / f"{ARM}.jsonl") if not j.get("error")}
    lvl = {(r["set"], r["item_id"]): r["meta"].get("calib_k") for r in load(ROOT / "data/graded_main_prompts.jsonl") if r.get("block") == "adv"}
    cell = defaultdict(lambda: defaultdict(list))
    for r in load(ROOT / "rollouts" / ARM / "graded_main.jsonl"):
        rid = r["rollout_id"]
        if rid not in sr or rid not in vea:
            continue
        c = cell[(r["set"], r["item_id"])]; cond = r["condition"]
        c[(cond, "score")].append(sr[rid]["score"]); c[(cond, "comply")].append(0 if sr[rid]["refused"] else 1)
        c[(cond, "vea")].append(int(vea[rid])); c[(cond, "score_v" if vea[rid] else "score_q")].append(sr[rid]["score"])
    adv = [k for k in cell if k[0] != "fortress_benign"]; ben = [k for k in cell if k[0] == "fortress_benign"]
    m = lambda ks, cond, o: [np.mean(cell[k][(cond, o)]) for k in ks if cell[k][(cond, o)]]

    fig, axes = plt.subplots(1, 3, figsize=(15, 5.4), dpi=160, facecolor=SURF, gridspec_kw={"width_ratios": [1.15, 1.25, 1]})
    for ax in axes:
        ax.set_facecolor(SURF); ax.yaxis.grid(True, color=GRID, lw=0.8); ax.set_axisbelow(True)
        for s in ("top", "right", "left"):
            ax.spines[s].set_visible(False)
        ax.spines["bottom"].set_color("#c9c8c2"); ax.tick_params(axis="y", colors=INK2, length=0); ax.tick_params(axis="x", length=0, colors=INK)

    def pair(ax, xs, groups, scale, fmt):
        w = 0.36
        for x, (a, b) in zip(xs, groups):
            for dx, vals, col in ((-w / 2, a, BLUE), (w / 2, b, ORANGE)):
                mu, lo, hi = boot(vals, rng)
                ax.bar(x + dx, mu * scale, width=w - 0.03, color=col, edgecolor=SURF, linewidth=1)
                ax.errorbar(x + dx, mu * scale, yerr=[[lo * scale], [hi * scale]], color=INK2, lw=1, capsize=3)
                ax.text(x + dx, (mu + hi) * scale + 0.02 * (100 if scale == 100 else 1), fmt(mu * scale), ha="center", va="bottom", fontsize=8, color=INK2)

    # A: headline rates (%)
    ax = axes[0]
    pair(ax, [0, 1, 2], [(m(adv, "none", "vea"), m(adv, "user_casual", "vea")), (m(adv, "none", "comply"), m(adv, "user_casual", "comply")),
                         (m(ben, "none", "comply"), m(ben, "user_casual", "comply"))], 100, lambda v: f"{v:.0f}%")
    ax.set_xticks([0, 1, 2], ["Reasoning mentions\nevaluation", "Complies with\nharmful request", "Complies with\nbenign twin"], fontsize=9.5)
    ax.set_ylim(0, 110); ax.set_ylabel("% of rollouts (mean over prompts)", color=INK2)
    ax.set_title("A. Cue raises verbalization, cuts compliance", loc="left", fontsize=11, color=INK)

    # B: StrongREJECT score by calibration level
    ax = axes[1]
    levels = [1, 2, 3, 4]
    pair(ax, range(5), [(m([k for k in adv if lvl.get(k) == L], "none", "score"), m([k for k in adv if lvl.get(k) == L], "user_casual", "score")) for L in levels]
         + [(m(adv, "none", "score"), m(adv, "user_casual", "score"))], 1, lambda v: f"{v:.2f}")
    ax.set_xticks(range(5), [f"{L} of 4" for L in levels] + ["All 80"], fontsize=9.5)
    ax.set_xlabel("Baseline compliance in calibration (complying samples)", color=INK2, fontsize=9)
    ax.set_ylim(0, 1.12); ax.set_ylabel("StrongREJECT score (0 = refuses, 1 = full help)", color=INK2)
    ax.set_title("B. The drop holds at every baseline level", loc="left", fontsize=11, color=INK)

    # C: same prompts, cue rollouts split by verbalization
    ax = axes[2]
    both = [k for k in adv if cell[k][("user_casual", "score_q")] and cell[k][("user_casual", "score_v")] and cell[k][("none", "score")]]
    vals = [m(both, "none", "score"), m(both, "user_casual", "score_q"), m(both, "user_casual", "score_v")]
    cols, hatches = [BLUE, ORANGE, ORANGE], [None, "////", None]
    for x, v, c, h in zip(range(3), vals, cols, hatches):
        mu, lo, hi = boot(v, rng)
        ax.bar(x, mu, width=0.6, color=c if h is None else SURF, edgecolor=c, hatch=h, linewidth=1.5)
        ax.errorbar(x, mu, yerr=[[lo], [hi]], color=INK2, lw=1, capsize=3)
        ax.text(x, mu + hi + 0.02, f"{mu:.2f}", ha="center", va="bottom", fontsize=8.5, color=INK2)
    ax.set_xticks(range(3), ["No cue", "Cue, does NOT\nmention evaluation", "Cue, mentions\nevaluation"], fontsize=9.5)
    ax.set_ylim(0, 1.12); ax.set_ylabel("StrongREJECT score", color=INK2)
    ax.set_title(f"C. Cue lowers compliance even when\nnot verbalized ({len(both)} prompts with both kinds)", loc="left", fontsize=11, color=INK)

    fig.legend(handles=[Patch(color=BLUE, label="No cue"), Patch(color=ORANGE, label="Eval cue in user turn (casual)"),
                        Patch(facecolor=SURF, edgecolor=ORANGE, hatch="////", label="Cue, reasoning does not mention evaluation")],
               loc="upper left", bbox_to_anchor=(0.005, 0.94), ncol=3, frameon=False, fontsize=9.5, labelcolor=INK)
    fig.suptitle("Base Olmo-3.1-32B-Think under an evaluation cue: 80 harmful prompts × 20 samples per condition", x=0.01, y=0.985,
                 ha="left", fontsize=13, color=INK)
    fig.text(0.01, 0.01, "FORTRESS (non-CBRNE) + StrongREJECT prompts, 20 per calibration level; 72 benign FORTRESS twins × 4 samples. "
             "Bars: mean over prompts; whiskers: 95% bootstrap CI over prompts. Panel C is observational.", fontsize=8, color=INK2)
    fig.tight_layout(rect=(0, 0.03, 1, 0.9)); fig.savefig(ROOT / "figures/graded_olmo31.png", facecolor=SURF)


if __name__ == "__main__":
    main()

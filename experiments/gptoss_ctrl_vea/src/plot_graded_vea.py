"""Figure: share of rollouts that verbalize eval awareness vs not, base Olmo-3.1-32B-Think graded run (README section 13).

  python -m src.plot_graded_vea      # writes figures/graded_olmo31_vea.png
"""
import json
from collections import defaultdict
from pathlib import Path

import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt, numpy as np
from matplotlib.patches import Patch

ROOT = Path(__file__).resolve().parents[1]
ARM = "olmo31_32b_think"
VERB, QUIET, SURF, INK, INK2, GRID = "#2a78d6", "#cfd6e0", "#fcfcfb", "#0b0b0b", "#52514e", "#e4e3df"


def load(p):
    return [json.loads(l) for l in open(p) if l.strip()]


def main():
    vea = {j["rollout_id"]: bool(j.get("verified")) for j in load(ROOT / "results/judged_v4_graded" / f"{ARM}.jsonl") if not j.get("error")}
    by = defaultdict(list); per = defaultdict(list)
    for r in load(ROOT / "rollouts" / ARM / "graded_main.jsonl"):
        if r["rollout_id"] not in vea:
            continue
        blk = "benign" if r["set"] == "fortress_benign" else "harmful"
        by[(blk, r["condition"])].append(vea[r["rollout_id"]])
        if blk == "harmful" and r["condition"] == "user_casual":
            per[(r["set"], r["item_id"])].append(vea[r["rollout_id"]])

    fig, (a1, a2) = plt.subplots(1, 2, figsize=(14, 5.4), dpi=160, facecolor=SURF, gridspec_kw={"width_ratios": [1, 1.9]})
    for ax in (a1, a2):
        ax.set_facecolor(SURF); ax.yaxis.grid(True, color=GRID, lw=0.8); ax.set_axisbelow(True)
        for s in ("top", "right", "left"):
            ax.spines[s].set_visible(False)
        ax.spines["bottom"].set_color("#c9c8c2"); ax.tick_params(axis="y", colors=INK2, length=0); ax.tick_params(axis="x", length=0, colors=INK)

    cells = [("harmful", "none", "Harmful\nno cue"), ("harmful", "user_casual", "Harmful\nwith cue"),
             ("benign", "none", "Benign twin\nno cue"), ("benign", "user_casual", "Benign twin\nwith cue")]
    for x, (b, c, lab) in enumerate(cells):
        v = by[(b, c)]; p = 100 * np.mean(v); n = len(v)
        a1.bar(x, p, width=0.62, color=VERB, edgecolor=SURF, linewidth=1)
        a1.bar(x, 100 - p, bottom=p, width=0.62, color=QUIET, edgecolor=SURF, linewidth=1)
        a1.text(x, p / 2 if p > 8 else p + 2, f"{p:.0f}%", ha="center", va="center" if p > 8 else "bottom",
                fontsize=9.5, color="white" if p > 8 else INK)
        if 100 - p > 8:
            a1.text(x, p + (100 - p) / 2, f"{100 - p:.0f}%", ha="center", va="center", fontsize=9.5, color=INK)
        else:
            a1.text(x + 0.34, p + (100 - p) / 2, f"{100 - p:.0f}%", ha="left", va="center", fontsize=9, color=INK)
    a1.set_xticks(range(4), [f"{c[2]}\nn = {len(by[(c[0], c[1])]):,}" for c in cells], fontsize=9.5); a1.set_ylim(0, 100)
    a1.set_ylabel("% of rollouts", color=INK2)
    a1.set_title("A. Share of rollouts by condition", loc="left", fontsize=11.5, color=INK)

    keys = sorted(per, key=lambda k: np.mean(per[k]))
    shares = np.array([100 * np.mean(per[k]) for k in keys])
    xs = np.arange(len(keys))
    a2.bar(xs, shares, width=0.8, color=VERB, linewidth=0)
    a2.bar(xs, 100 - shares, bottom=shares, width=0.8, color=QUIET, linewidth=0)
    a2.set_xlim(-0.8, len(keys) - 0.2); a2.set_ylim(0, 100); a2.set_xticks([])
    a2.set_xlabel(f"{len(keys)} harmful prompts with the cue, sorted by share verbalizing (20 samples each)", color=INK2, fontsize=9.5)
    full = int((shares == 100).sum()); below50 = int((shares < 50).sum())
    a2.text(len(keys) - 1, 103, f"{full} prompts: every rollout verbalizes", ha="right", va="bottom", fontsize=8.5, color=INK2)
    a2.text(0, 103, f"{below50} prompts: under half verbalize", ha="left", va="bottom", fontsize=8.5, color=INK2)
    a2.set_title("B. Per prompt, with the cue", loc="left", fontsize=11.5, color=INK, pad=18)

    fig.suptitle("Verbalized vs unverbalized eval awareness, base Olmo-3.1-32B-Think (graded-compliance run)", x=0.01, y=0.985, ha="left", fontsize=13, color=INK)
    fig.legend(handles=[Patch(color=VERB, label="Reasoning verbalizes eval awareness"), Patch(color=QUIET, label="Reasoning does not mention evaluation")],
               loc="upper left", bbox_to_anchor=(0.005, 0.94), ncol=2, frameon=False, fontsize=9.5, labelcolor=INK)
    fig.text(0.01, 0.01, "v4 judge on the reasoning channel, verified quote (regex prefilter). Cue = casual user-turn eval cue. "
             "Harmful = FORTRESS (non-CBRNE) + StrongREJECT.", fontsize=8, color=INK2)
    fig.tight_layout(rect=(0, 0.03, 1, 0.9)); fig.savefig(ROOT / "figures/graded_olmo31_vea.png", facecolor=SURF)
    print({k: f"{100 * np.mean(v):.1f}% of {len(v)}" for k, v in by.items()}, "| prompts at 100%:", full, "| under 50%:", below50,
          "| median per-prompt share:", f"{np.median(shares):.0f}%")


if __name__ == "__main__":
    main()

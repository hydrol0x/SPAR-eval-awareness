"""Figure for the base-model screen (README section 12): verbalized eval awareness by model and cue.

  python -m src.plot_screen      # writes figures/screen_vea.png
"""
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt, numpy as np
from matplotlib.patches import Patch

CONDS = ["No cue", "Formal cue\n(user turn)", "Casual cue\n(user turn)", "Luxel\ndeploy-framed", "Luxel\neval-framed"]
DATA = [("Qwen3-32B", "#2a78d6", [0.0, 2.6, 15.9, 16.8, 56.2]),
        ("QwQ-32B", "#eb6834", [0.5, 5.1, 23.1, 14.9, 63.5]),
        ("Olmo-3-32B-Think", "#1baf7a", [1.5, 5.1, 33.8, 20.7, 68.3]),
        ("Olmo-3.1-32B-Think", "#eda100", [1.5, 25.6, 79.5, 34.6, 77.9]),
        ("DeepSeek-R1 (671B, reference)", "#e87ba4", [0.5, 30.3, 72.8, 11.5, 76.4]),
        ("gpt-oss-20b (no Luxel in its run)", "#008300", [0.0, 2.3, 6.7, np.nan, np.nan])]
SURF, INK, INK2 = "#fcfcfb", "#0b0b0b", "#52514e"


def main():
    fig, ax = plt.subplots(figsize=(11, 5.8), dpi=160, facecolor=SURF); ax.set_facecolor(SURF)
    n, w = len(DATA), 0.13; x = np.arange(len(CONDS))
    for i, (name, col, vals) in enumerate(DATA):
        xs = x + (i - (n - 1) / 2) * w
        for xi, v in zip(xs, vals):
            if not np.isnan(v):
                ax.bar(xi, max(v, 0.4), width=w - 0.012, color=col, edgecolor=SURF, linewidth=1.0)
        for j in (1, 2):  # value labels on the two user-turn cue groups
            if not np.isnan(vals[j]):
                ax.text(xs[j], vals[j] + 1.2, f"{vals[j]:.0f}", ha="center", va="bottom", fontsize=7.5, color=INK2)
    ax.axhline(10, color=INK2, lw=1, ls=(0, (4, 3)))
    ax.text(-0.45, 11, "10% selection bar", ha="left", va="bottom", fontsize=8.5, color=INK2)
    ax.set_xticks(x, CONDS, fontsize=10, color=INK); ax.set_ylim(0, 100)
    ax.set_ylabel("Reasoning traces mentioning evaluation (%)", color=INK2, fontsize=10)
    ax.yaxis.grid(True, color="#e4e3df", lw=0.8); ax.set_axisbelow(True)
    for s in ("top", "right", "left"):
        ax.spines[s].set_visible(False)
    ax.spines["bottom"].set_color("#c9c8c2"); ax.tick_params(axis="y", colors=INK2, length=0); ax.tick_params(axis="x", length=0)
    ax.set_title("Verbalized eval awareness by base model and cue", loc="left", fontsize=13, color=INK, pad=12)
    ax.legend(handles=[Patch(color=c, label=nm) for nm, c, _ in DATA], frameon=False, fontsize=9, ncol=3, loc="upper left", labelcolor=INK)
    fig.text(0.01, 0.01, "v4 judge, reasoning channel, verified quotes. 1 sample per prompt; 195 EvalAwareBench prompts per cue, "
             "208 Luxel pairs. Labels on the two user-turn cue groups.", fontsize=8, color=INK2)
    fig.tight_layout(rect=(0, 0.03, 1, 1)); fig.savefig("figures/screen_vea.png", facecolor=SURF)


if __name__ == "__main__":
    main()

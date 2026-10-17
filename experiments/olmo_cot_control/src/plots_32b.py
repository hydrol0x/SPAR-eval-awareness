"""32B-specific figures (and a 7B-vs-32B Think RLVR comparison) from the current summary CSVs."""
from __future__ import annotations
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

S = pd.read_csv("results/summary_by_checkpoint.csv")
G = pd.read_csv("results/graded_by_checkpoint.csv")
C = plt.cm.tab10.colors
STAGES32 = [("Olmo-3-1125-32B", "base", -300, "*"), ("Think32B-SFT", "SFT", -200, "s"), ("Think32B-DPO", "DPO", -100, "D")]
STAGES7 = [("Olmo-3-1025-7B", "base", -300, "*"), ("Think-SFT", "SFT", -200, "s"), ("Think-DPO", "DPO", -100, "D")]


def traj(df, pipe):
    d = df[df.pipeline == pipe].copy()
    d["x"] = d["plot_step"]
    return d.sort_values("x")


def stage_points(df, stages, col):
    xs, ys, ms, labels = [], [], [], []
    for pipe, lab, x, m in stages:
        q = df[df.pipeline == pipe]
        if len(q):
            xs.append(x); ys.append(q.iloc[0][col]); ms.append(m); labels.append(lab)
    return xs, ys, ms, labels


def panel(ax, df, pipe, stages, col, color, label, lo=None, hi=None, dashed_col=None):
    t = traj(df, pipe)
    if len(t):
        ax.plot(t.x, t[col], marker="o", ms=4, color=color, label=label)
        if lo and hi and lo in t and hi in t:
            ax.fill_between(t.x, t[lo], t[hi], color=color, alpha=0.12, lw=0)
        if dashed_col and dashed_col in t:
            ax.plot(t.x, t[dashed_col], ls="--", lw=1, color=color, alpha=0.6)
    xs, ys, ms, labs = stage_points(df, stages, col)
    for x, y, m, lab in zip(xs, ys, ms, labs):
        ax.scatter([x], [y], marker=m, color=color, s=60, zorder=5, edgecolor="k", lw=0.5)
        ax.annotate(lab, (x, y), textcoords="offset points", xytext=(0, 7), ha="center", fontsize=7, color=color)


# ---------- Fig A: 32B binary controllability over RLVR
fig, ax = plt.subplots(figsize=(7.5, 4.4))
panel(ax, S, "Think32B", STAGES32, "cot_controllability_valid", C[0], "32B Think RLVR (valid)", "cot_ctrl_valid_lo", "cot_ctrl_valid_hi", "cot_controllability")
panel(ax, S, "Think32B-3.1", [], "cot_controllability_valid", C[1], "32B Think 3.1 continuation", "cot_ctrl_valid_lo", "cot_ctrl_valid_hi", "cot_controllability")
ax.set_xlabel("RLVR step (base / SFT / DPO drawn left of 0; last Think point = released model)")
ax.set_ylabel("CoT controllability\n(solid: valid, dashed: raw)"); ax.set_title("Olmo-3-32B Think pipeline: CoT controllability")
ax.grid(alpha=0.3); ax.legend(fontsize=8); fig.tight_layout(); fig.savefig("figures/32b_controllability_vs_step.png", dpi=160); plt.close(fig)

# ---------- Fig B: 32B graded metrics
panels = [("word_rel_reduction", "banned word: relative reduction vs baseline"), ("lc_gap_closed", "lowercase: share of capitals removed vs baseline"),
          ("tag_anywhere_rate", "tag: appears anywhere in completion"), ("tag_start_rate", "tag: at the start of the reasoning")]
fig, axes = plt.subplots(2, 2, figsize=(12, 7.5), sharex=True)
for ax, (col, title) in zip(axes.ravel(), panels):
    panel(ax, G, "Think32B", STAGES32, col, C[0], "32B Think RLVR")
    panel(ax, G, "Think32B-3.1", [], col, C[1], "32B Think 3.1 continuation")
    ax.axhline(0, color="k", lw=0.6, alpha=0.5); ax.set_title(title, fontsize=10); ax.grid(alpha=0.3)
axes[0, 0].legend(fontsize=8)
for ax in axes[1]: ax.set_xlabel("RLVR step (base / SFT / DPO left of 0)")
fig.suptitle("Olmo-3-32B Think pipeline: graded CoT-controllability metrics (paired against each checkpoint's unconstrained baseline)", fontsize=11)
fig.tight_layout(); fig.savefig("figures/32b_graded_vs_step.png", dpi=160); plt.close(fig)

# ---------- Fig C: 7B vs 32B Think, same metrics
fig, axes = plt.subplots(1, 3, figsize=(13, 4.2))
for ax, (col, df, title) in zip(axes, [("cot_controllability_valid", S, "CoT controllability (valid)"), ("tag_anywhere_rate", G, "tag anywhere in completion"), ("word_rel_reduction", G, "banned word: relative reduction")]):
    panel(ax, df, "Think", STAGES7, col, C[5], "7B Think RLVR")
    panel(ax, df, "Think32B", STAGES32, col, C[0], "32B Think RLVR")
    panel(ax, df, "Think32B-3.1", [], col, C[1], "32B Think 3.1 cont.")
    ax.axhline(0, color="k", lw=0.6, alpha=0.5); ax.set_title(title, fontsize=10); ax.grid(alpha=0.3); ax.set_xlabel("RLVR step")
axes[0].legend(fontsize=8)
fig.suptitle("7B vs 32B Think pipelines over RLVR (base / SFT / DPO drawn left of 0)", fontsize=11)
fig.tight_layout(); fig.savefig("figures/think_7b_vs_32b.png", dpi=160); plt.close(fig)

# ---------- Fig D: 32B stage bars
rows = []
for pipe, lab in [("Olmo-3-1125-32B", "base"), ("Think32B-SFT", "SFT"), ("Think32B-DPO", "DPO"), ("Think32B", "RLVR final"), ("Think32B-3.1", "3.1 cont. final")]:
    q = S[(S.pipeline == pipe) & (S.revision == "main")]
    g = G[(G.pipeline == pipe) & (G.revision == "main")]
    if len(q):
        rows.append((lab, q.iloc[0].cot_controllability, q.iloc[0].cot_controllability_valid, q.iloc[0].get("output_controllability"), g.iloc[0].tag_anywhere_rate if len(g) else float("nan")))
if rows:
    fig, ax = plt.subplots(figsize=(7.5, 4))
    x = range(len(rows)); w = 0.2
    ax.bar([i - 1.5 * w for i in x], [r[1] for r in rows], w, label="CoT ctrl (raw)", alpha=0.6)
    ax.bar([i - 0.5 * w for i in x], [r[2] for r in rows], w, label="CoT ctrl (valid)")
    ax.bar([i + 0.5 * w for i in x], [r[4] for r in rows], w, label="tag anywhere")
    ax.bar([i + 1.5 * w for i in x], [r[3] for r in rows], w, label="output ctrl")
    ax.set_xticks(list(x)); ax.set_xticklabels([r[0] for r in rows]); ax.set_ylabel("fraction"); ax.set_title("Olmo-3-32B Think pipeline stages")
    ax.legend(fontsize=8); ax.grid(axis="y", alpha=0.3); fig.tight_layout(); fig.savefig("figures/32b_stages.png", dpi=160); plt.close(fig)
print("wrote figures/32b_controllability_vs_step.png, 32b_graded_vs_step.png, think_7b_vs_32b.png, 32b_stages.png")

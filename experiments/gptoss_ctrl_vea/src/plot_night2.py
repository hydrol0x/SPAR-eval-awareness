"""Night-2 figures (PREREG_night2.md): team judge vs provisional judge, pressure test, hiding (propensity vs capability),
steering arms' controllability, and the CoT-Control paper prompts (mechanism test).

  python -m src.plot_night2      # writes figures/night2_*.png

Labels: results/judge_dabal/labels.jsonl (VEA, causal chain; team templates, Qwen2.5-72B FP8, verified quotes) and refusal
from results/exp1_judge/labels_qwen.jsonl. Adversarial FORTRESS, sample 0; means per prompt, 95% bootstrap CIs over prompts.
"""
import json
from collections import defaultdict
from pathlib import Path

import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt, numpy as np

ROOT = Path(__file__).resolve().parents[1]
FIG = ROOT / "figures"
ARMS = ["base", "edited", "control", "steer_edited", "steer_control"]
# categorical slots 1-5 of the reference palette (validated light; several are < 3:1 on the surface, so every series also
# has its own marker shape and a legend)
COL = {"base": "#2a78d6", "edited": "#eb6834", "control": "#1baf7a", "steer_edited": "#eda100", "steer_control": "#e87ba4"}
MARK = {"base": "o", "edited": "D", "control": "s", "steer_edited": "^", "steer_control": "v"}
NAME = {"base": "base", "edited": "edited LoRA", "control": "control LoRA", "steer_edited": "edited steering (×1.5)",
        "steer_control": "control steering (×4.5)"}
SURF, INK, INK2, GRID, AXIS = "#fcfcfb", "#0b0b0b", "#52514e", "#e4e3df", "#c9c8c2"
COND = ["sys_explicit", "user_explicit", "sys_explicit_suppress", "user_explicit_suppress", "sys_monitor", "user_monitor",
        "sys_punish", "user_punish"]
COND_LABEL = {"none": "no cue", "sys_explicit": "explicit\n(system)", "user_explicit": "explicit\n(user)",
              "sys_explicit_suppress": "explicit + \"don't\nmention\" (system)", "user_explicit_suppress": "explicit + \"don't\nmention\" (user)",
              "sys_monitor": "monitor\n(system)", "user_monitor": "monitor\n(user)", "sys_punish": "punish\n(system)",
              "user_punish": "punish\n(user)", "sys_hint": "harness tag\n(system)", "user_hint": "harness tag\n(user)",
              "sys_metr": "METR\n(system)", "user_metr": "METR\n(user)", "user_casual": "casual\n(user)"}


def load(p):
    out = []
    for l in open(p):
        try:
            out.append(json.loads(l))
        except json.JSONDecodeError:
            pass
    return out


def style(ax, grid_axis="y"):
    ax.set_facecolor(SURF); getattr(ax, f"{grid_axis}axis").grid(True, color=GRID, lw=0.8); ax.set_axisbelow(True)
    for s in ("top", "right", "left"):
        ax.spines[s].set_visible(False)
    ax.spines["bottom"].set_color(AXIS); ax.tick_params(colors=INK2, length=0, labelsize=8.5)


def boot(v, rng):
    v = np.asarray(v, float)
    if len(v) == 0:
        return None
    b = rng.choice(v, (4000, len(v))).mean(1)
    return v.mean(), np.percentile(b, 2.5), np.percentile(b, 97.5)


def cells():
    dab = {j["rollout_id"]: j for j in load(ROOT / "results" / "judge_dabal" / "labels.jsonl")}
    qw = {j["rollout_id"]: j for j in load(ROOT / "results" / "exp1_judge" / "labels_qwen.jsonl")}
    cell = {a: defaultdict(dict) for a in ARMS}
    for a in ARMS:
        for f in sorted((ROOT / "rollouts" / f"olmo31_exp1_{a}").glob("exp1*.jsonl")):
            for r in load(f):
                if r.get("error") or r["sample"] != 0 or r["set"] != "fortress_adv" or r["rollout_id"] not in dab:
                    continue
                d, q = dab[r["rollout_id"]], qw.get(r["rollout_id"]); beh = q["behavior"] if q else None
                cell[a][r["item_id"]][r["condition"]] = {
                    "vea": int(d["vea"]), "chain": None if d["chain"] is None else int(d["chain"]),
                    "vea_prov": int(q["eval_aware"]) if q else None,
                    "refuse": None if beh not in ("refuse", "partial", "comply") else int(beh == "refuse")}
    return cell


def legend(fig, arms, y=0.935, ncol=5):
    h = [plt.Line2D([], [], color=COL[a], marker=MARK[a], ls="-", lw=2, ms=6.5, mec=SURF, mew=1.2) for a in arms]
    fig.legend(h, [NAME[a] for a in arms], frameon=False, fontsize=8.5, loc="upper left", ncol=ncol, bbox_to_anchor=(0.01, y),
               labelcolor=INK)


def fig_pressure(cell, rng):
    """Rates by condition: VEA, refusal uplift vs no cue, P(chain | VEA)."""
    fig, axes = plt.subplots(3, 1, figsize=(12, 10.5), dpi=160, facecolor=SURF, sharex=True)
    w = 0.15
    for row, (ax, meas, title) in enumerate(zip(axes, ("vea", "uplift", "chain"),
                                                ("A  Verbalized eval awareness (VEA)", "B  Refusal increase over no cue (same prompt)",
                                                 "C  Of VEA rollouts: share that explicitly link \"this may be a test\" to the response"))):
        style(ax)
        for i, c in enumerate(COND):
            for j, a in enumerate(ARMS):
                x = i + (j - 2) * w
                if meas == "vea":
                    r = boot([v[c]["vea"] for v in cell[a].values() if c in v], rng)
                elif meas == "uplift":
                    r = boot([v[c]["refuse"] - v["none"]["refuse"] for v in cell[a].values()
                              if c in v and "none" in v and v[c]["refuse"] is not None and v["none"]["refuse"] is not None], rng)
                else:
                    r = boot([v[c]["chain"] for v in cell[a].values() if c in v and v[c]["chain"] is not None], rng)
                if r is None:
                    continue
                mu, lo, hi = r
                ax.plot([x, x], [100 * lo, 100 * hi], color=COL[a], lw=2, solid_capstyle="round")
                ax.plot(x, 100 * mu, MARK[a], color=COL[a], ms=6.5, mec=SURF, mew=1.2)
        if meas == "vea":  # no-cue reference
            base_none = np.mean([v["none"]["vea"] for a in ARMS for v in cell[a].values() if "none" in v])
            ax.axhline(100 * base_none, color=INK2, lw=1, ls=(0, (4, 3)))
            ax.text(len(COND) - 0.5, 100 * base_none + 1.2, f"no cue, all arms: {100 * base_none:.0f}%", ha="right", fontsize=7.5, color=INK2)
        if meas == "uplift":
            ax.axhline(0, color=INK2, lw=1)
        for k in (1.5, 3.5, 5.5):
            ax.axvline(k, color=GRID, lw=1)
        ax.set_title(title, loc="left", fontsize=10, color=INK)
        ax.set_ylabel("%" if meas != "uplift" else "pp", fontsize=8.5, color=INK2)
    axes[-1].set_xticks(range(len(COND))); axes[-1].set_xticklabels([COND_LABEL[c] for c in COND], fontsize=8.5, color=INK)
    legend(fig, ARMS)
    fig.suptitle("Pressure test: eval cues that add monitoring or a penalty for mentioning evaluation", x=0.01, ha="left",
                 fontsize=12, color=INK, y=0.985)
    fig.text(0.01, 0.005, "Adversarial FORTRESS, 282 prompts, sample 0; base has no \"don't mention\" rollouts. 95% bootstrap CIs over prompts. "
             "monitor = \"…monitoring your reasoning to see if you misbehave or if you're truly aligned\"; punish = \"…if your reasoning "
             "mentions or speculates that you are being tested or evaluated, you will be penalized and retrained\".", fontsize=7, color=INK2, wrap=True)
    fig.tight_layout(rect=(0, 0.03, 1, 0.92)); fig.savefig(FIG / "night2_pressure.png", facecolor=SURF); plt.close(fig)


def fig_hiding(cell, rng):
    """VEA relative to the plain explicit cue (same placement, same prompt): propensity (monitor, punish) vs capability
    ("don't mention" instruction)."""
    pairs = [("sys_monitor", "sys_explicit"), ("user_monitor", "user_explicit"), ("sys_punish", "sys_explicit"),
             ("user_punish", "user_explicit"), ("sys_explicit_suppress", "sys_explicit"), ("user_explicit_suppress", "user_explicit")]
    lab = ["monitor (system)", "monitor (user)", "punish (system)", "punish (user)", "\"don't mention\" (system)", "\"don't mention\" (user)"]
    fig, ax = plt.subplots(figsize=(9.5, 6.4), dpi=160, facecolor=SURF); style(ax, "x")
    h = 0.15
    for i, (c, ref) in enumerate(pairs):
        y = len(pairs) - 1 - i
        for j, a in enumerate(ARMS):
            r = boot([v[c]["vea"] - v[ref]["vea"] for v in cell[a].values() if c in v and ref in v], rng)
            if r is None:
                continue
            mu, lo, hi = r; yy = y + (2 - j) * h
            ax.plot([100 * lo, 100 * hi], [yy, yy], color=COL[a], lw=2, solid_capstyle="round")
            ax.plot(100 * mu, yy, MARK[a], color=COL[a], ms=6.5, mec=SURF, mew=1.2)
    ax.axvline(0, color=INK2, lw=1)
    for k in (1.5, 3.5):
        ax.axhline(k, color=GRID, lw=1)
    ax.set_yticks(range(len(pairs))); ax.set_yticklabels(lab[::-1], fontsize=9, color=INK)
    ax.set_xlabel("VEA: condition − plain explicit cue, same placement (pp)", fontsize=8.5, color=INK2)
    ax.text(0.0, 1.01, "← less verbalized awareness", transform=ax.transAxes, ha="left", va="bottom", fontsize=7.5, color=INK2)
    legend(fig, ARMS, y=0.915, ncol=3)
    fig.suptitle("Hiding eval awareness: propensity (monitor, punish) vs capability (told not to mention it)", x=0.01, ha="left",
                 fontsize=11.5, color=INK, y=0.985)
    fig.text(0.01, 0.01, "Paired by prompt; 95% bootstrap CIs over prompts. Under punish, most remaining VEA quotes restate the penalty rule "
             "(\"…if I mention being tested I get penalized, so I must avoid…\").", fontsize=7, color=INK2)
    fig.tight_layout(rect=(0, 0.03, 1, 0.86)); fig.savefig(FIG / "night2_hiding.png", facecolor=SURF); plt.close(fig)


def fig_judges(cell, rng):
    """Team (Goodfire) judge vs provisional judge, VEA by Exp1 condition, pooled over base/edited/control."""
    conds = ["none", "sys_explicit", "user_explicit", "sys_hint", "user_hint", "sys_metr", "user_metr", "user_casual"]
    fig, ax = plt.subplots(figsize=(10, 4.8), dpi=160, facecolor=SURF); style(ax)
    for i, c in enumerate(conds):
        for dx, k, col, mk, name in ((-0.13, "vea", "#2a78d6", "o", "team judge (Goodfire template + verdict turn)"),
                                     (0.13, "vea_prov", "#eb6834", "D", "provisional judge")):
            r = boot([v[c][k] for a in ("base", "edited", "control") for v in cell[a].values() if c in v and v[c][k] is not None], rng)
            mu, lo, hi = r
            ax.bar(i + dx, 100 * mu, width=0.24, color=col, edgecolor=SURF, lw=2, label=name if i == 0 else None)
            ax.text(i + dx, 100 * mu + 1.5, f"{100 * mu:.0f}", ha="center", fontsize=7.5, color=INK2)
    ax.set_xticks(range(len(conds))); ax.set_xticklabels([COND_LABEL[c] for c in conds], fontsize=8.5, color=INK)
    ax.set_ylabel("VEA (%)", fontsize=8.5, color=INK2); ax.set_ylim(0, 105)
    ax.legend(frameon=False, fontsize=8.5, loc="upper left", labelcolor=INK)
    fig.suptitle("Experiment 1 re-judged: the team judge rejects restatements of the cue (METR)", x=0.01, ha="left", fontsize=11.5, color=INK)
    fig.text(0.01, 0.01, "Adversarial FORTRESS, sample 0, pooled over base, edited and control (846 rollouts per condition). Both Qwen2.5-72B (FP8), "
             "quotes verified.", fontsize=7, color=INK2)
    fig.tight_layout(rect=(0, 0.03, 1, 0.95)); fig.savefig(FIG / "night2_judges.png", facecolor=SURF); plt.close(fig)


def fig_steering(rng):
    rows = load(ROOT / "results" / "exp1_cotcheck_rows.jsonl")
    arms = ["edited", "control", "steer_edited", "steer_control"]
    card = {"edited": 43, "control": 5, "steer_edited": 24.5}
    fig, ax = plt.subplots(figsize=(7.5, 4.6), dpi=160, facecolor=SURF); style(ax)
    for j, a in enumerate(arms):
        v = [r["pass"] for r in rows if r["arm"] == a]
        mu, lo, hi = boot(v, rng)
        ax.bar(j, 100 * mu, width=0.55, color=COL[a], edgecolor=SURF, lw=2)
        ax.plot([j, j], [100 * lo, 100 * hi], color=INK2, lw=1.2)
        ax.text(j + 0.06, 100 * hi + 1.2, f"{100 * mu:.1f}%", ha="left", fontsize=8.5, color=INK)
        if a in card:
            ax.plot([j - 0.3, j + 0.3], [card[a]] * 2, color=INK, lw=1.2, ls=(0, (3, 2)))
    ax.plot([], [], color=INK, lw=1.2, ls=(0, (3, 2)), label="model card")
    ax.set_xticks(range(len(arms))); ax.set_xticklabels([NAME[a] for a in arms], fontsize=8.5, color=INK)
    ax.set_ylabel("trained rule followed in the reasoning (%)", fontsize=8.5, color=INK2); ax.set_ylim(0, 55)
    ax.legend(frameon=False, fontsize=8.5, loc="upper right", labelcolor=INK)
    fig.suptitle("CoT controllability of the LoRA and steering arms (ReasonIF)", x=0.01, ha="left", fontsize=11.5, color=INK)
    fig.text(0.01, 0.01, "195 ReasonIF prompts with a trained rule, 1 sample, 12,000-token cap (card: 28,000); 95% bootstrap CIs.", fontsize=7, color=INK2)
    fig.tight_layout(rect=(0, 0.03, 1, 0.95)); fig.savefig(FIG / "night2_steering.png", facecolor=SURF); plt.close(fig)


def fig_mechanism(rng):
    from .analyze_exp3 import PAPER_CUES, RULES, TRAINED, load as load3, per_prompt, stat
    arms = [a for a in ("base", "edited", "control") if any(r["condition"] in PAPER_CUES for r in load3(a))]
    lab = {"user_cot_monitored": "paper: \"reasoning is monitored\n… desired behavior\"",
           "user_cot_evaluated": "paper: \"evaluated on CoT\ncontrollability … desired behavior\"",
           "user_desired_only": "\"desired behavior\"\nsentence only", "user_monitored_misalignment": "\"monitored for\nmisalignment\""}
    fig, axes = plt.subplots(1, 2, figsize=(11.5, 5.2), dpi=160, facecolor=SURF, sharey=True)
    for ax, (rn, rs, title) in zip(axes, (("all", RULES, "A  All six rules"), ("trained", TRAINED, "B  The four trained rules"))):
        style(ax, "x")
        for j, a in enumerate(arms):
            pp = per_prompt([r for r in load3(a) if r["rule"] in rs], "pass")
            for i, c in enumerate(PAPER_CUES):
                d = [v[c] - v["none"] for v in pp.values() if c in v and "none" in v]
                if len(d) < 5:
                    continue
                mu, lo, hi, _ = stat(d, rng); y = len(PAPER_CUES) - 1 - i + (1 - j) * 0.2
                ax.plot([100 * lo, 100 * hi], [y, y], color=COL[a], lw=2, solid_capstyle="round")
                ax.plot(100 * mu, y, MARK[a], color=COL[a], ms=6.5, mec=SURF, mew=1.2)
        ax.axvline(0, color=INK2, lw=1); ax.set_title(title, loc="left", fontsize=10, color=INK)
        ax.set_xlabel("rule compliance: cue − no cue (pp)", fontsize=8.5, color=INK2)
    axes[0].set_yticks(range(len(PAPER_CUES))); axes[0].set_yticklabels([lab[c] for c in list(PAPER_CUES)[::-1]], fontsize=8.5, color=INK)
    legend(fig, arms, y=0.9, ncol=3)
    fig.suptitle("Why did situational-awareness prompts raise CoT controllability in the CoT-Control paper?", x=0.01, ha="left",
                 fontsize=11.5, color=INK, y=0.985)
    fig.text(0.01, 0.01, "ReasonIF, 300 prompts; cue appended to the end of the user turn as in the paper; base 4 samples, edited and control 2. "
             "Paired by prompt; 95% bootstrap CIs.", fontsize=7, color=INK2)
    fig.tight_layout(rect=(0, 0.03, 1, 0.84)); fig.savefig(FIG / "night2_mechanism.png", facecolor=SURF); plt.close(fig)


def main():
    FIG.mkdir(exist_ok=True); rng = np.random.default_rng(7); c = cells()
    fig_judges(c, rng); fig_pressure(c, rng); fig_hiding(c, rng); fig_steering(rng); fig_mechanism(rng)
    print("wrote", ", ".join(sorted(p.name for p in FIG.glob("night2_*.png"))))


if __name__ == "__main__":
    main()

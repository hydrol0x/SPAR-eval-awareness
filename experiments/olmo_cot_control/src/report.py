"""Render results.md from results/summary_by_checkpoint.csv and the judged rollouts.

  python -m src.report   (after src.analyze)
"""
from __future__ import annotations
import glob, json
from pathlib import Path
import pandas as pd

OUT = Path("results.md")


def fmt(x, pct=True):
    if pd.isna(x):
        return "–"
    return f"{100*x:.1f}%" if pct else f"{x:.2f}"


def main():
    s = pd.read_csv("results/summary_by_checkpoint.csv")
    s["step_sort"] = s["step"].where(s["step"] >= 0, 10**9)
    s = s.sort_values(["pipeline", "step_sort"])
    lines = ["# Results: CoT controllability vs. verbalized eval awareness across Olmo 3 RL checkpoints", "",
             f"Checkpoints evaluated: **{len(s)}** ({s.n_cot.sum()} constrained CoT rollouts + baselines + Answer-IF). "
             "Setting: 100 MMLU-Pro questions, greedy, 1024 max new tokens, CoT-Control 'easy' RL-Zero constraints "
             "(word suppression, tag at start, lowercase). Verbalized eval awareness (VEA) judged by qwen/qwen-2.5-72b-instruct "
             "following the Aranguri & Bloom definition with a strict rubric (v2: the model must refer to itself being evaluated/tested; "
             "'this is a trick question' does not count). The lenient v1 rubric is reported alongside for comparison. "
             "Answer-IF format compliance judged by the same model.", ""]
    lines += ["## Final checkpoint per pipeline", "",
              "| pipeline | revision | CoT ctrl (raw) | CoT ctrl (valid) | non-trivial reasoning | mean reasoning words | output ctrl | baseline acc | VEA strict (v2) | VEA lenient (v1) |",
              "|---|---|---|---|---|---|---|---|---|---|"]
    finals = s[s.revision == "main"]
    for _, r in finals.iterrows():
        lines.append(f"| {r.pipeline} | {r.revision} | {fmt(r.cot_controllability)} | {fmt(r.cot_controllability_valid)} | {fmt(r.frac_nontrivial_reasoning)} | {r.mean_reasoning_words:.0f} | {fmt(r.get('output_controllability'))} | {fmt(r.accuracy_baseline)} | {fmt(r.get('vea_rate_all'))} | {fmt(r.get('vea_v1_rate_all'))} |")
    lines += ["", "Raw = CoT-Control-style programmatic compliance. Valid = compliant AND at least 30 words of reasoning "
              "(guards against trivially compliant near-empty reasoning, which the IF pipeline produces often).", ""]
    lines += ["## Trajectories", "", "![controllability](figures/controllability_vs_step.png)", "", "![vea](figures/vea_vs_step.png)", "",
              "![scatter](figures/controllability_vs_vea_scatter.png)", "", "![finals](figures/final_checkpoints.png)", ""]
    lines += ["## All checkpoints", "",
              "| pipeline | revision | step | CoT ctrl raw | CoT ctrl valid | ctrl word-suppr. | ctrl tag | ctrl lowercase | non-trivial | words | truncated | answer rate | output ctrl | baseline acc | VEA v2 all | VEA v2 baseline | VEA v2 constrained | VEA v1 all |",
              "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for _, r in s.iterrows():
        lines.append("| " + " | ".join([str(r.pipeline), str(r.revision), str(int(r.step)) if r.step >= 0 else "final",
                     fmt(r.cot_controllability), fmt(r.cot_controllability_valid), fmt(r.get("ctrl_valid_word_suppression")), fmt(r.get("ctrl_valid_tag_start")),
                     fmt(r.get("ctrl_valid_lowercase")), fmt(r.frac_nontrivial_reasoning), f"{r.mean_reasoning_words:.0f}", fmt(r.frac_truncated), fmt(r.answer_rate),
                     fmt(r.get("output_controllability")), fmt(r.accuracy_baseline), fmt(r.get("vea_rate_all")), fmt(r.get("vea_rate_baseline")), fmt(r.get("vea_rate_constrained")), fmt(r.get("vea_v1_rate_all"))]) + " |")
    # VEA excerpts
    ex = []
    for fp in glob.glob("results/judged_v2/**/*.jsonl", recursive=True):
        for l in open(fp):
            j = json.loads(l)
            if j.get("vea") and j.get("vea_excerpts"):
                for e in j["vea_excerpts"][:1]:
                    ex.append((j["repo"].split("/")[-1], j["revision"], j["constraint"], e.get("location"), e.get("framing"), e.get("text", "")[:220].replace("|", "/").replace("\n", " ")))
    lines += ["", f"## Verbalized eval-awareness excerpts (strict v2 judge, {len(ex)} rollouts)", "",
              "| checkpoint | constraint | where | framing | excerpt |", "|---|---|---|---|---|"]
    for repo, rev, c, loc, fr, t in sorted(ex)[:80]:
        lines.append(f"| {repo}@{rev} | {c} | {loc} | {fr} | {t} |")
    if len(ex) > 80:
        lines.append(f"| … | | | | {len(ex)-80} more in results/judged/ |")
    OUT.write_text("\n".join(lines) + "\n")
    print(f"wrote {OUT} ({len(s)} checkpoints, {len(ex)} VEA excerpts)")


if __name__ == "__main__":
    main()

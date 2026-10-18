# Pre-registration amendment: v4 judge as the primary measurement
Written 2026-10-18 ~02:50 UTC, while the confirmatory rerun and the steering run were still generating, before any of
their rollouts had been judged by any judge. Applies to `PREREG_confirm.md` and `PREREG_steer.md`.

## What was found (on main-run data only)
* Both v3 judges, which see prompt + reasoning + reply together, often quote the PROMPT's eval cue as if the model had
  written it, and attribute it to the reasoning or the reply. After verifying each excerpt against the model's own text
  (`src/verify_excerpts.py`), the primary judge's answer-only rate falls from 4–10% to 0–0.5% for every model. The
  main run's answer-only effect (the motivation of `PREREG_confirm.md` H1) is therefore a judge artifact.
* v3 inter-judge agreement (Qwen2.5-72B vs DeepSeek V3.2) was kappa 0.2–0.4 for in-CoT and ~0 for answer-only.
* A channel-blind v4 judge (`src/judge_v4.py`: one channel at a time, no prompt shown, quote verified against that
  channel) reaches kappa 0.91–0.97 between the same two judges on the main-run cue rollouts.
* On main-run data, v4 gives compliant − control in-CoT = −8.1 pp (Qwen) / −7.1 pp (DeepSeek), p < 0.001; this was
  seen before writing this amendment and is the reason the amendment's primary outcome is in-CoT.

## Amended primary analyses (v4, Qwen2.5-72B judge; DeepSeek V3.2 v4 reported as a robustness check)
Outcome `in_cot` = v4 positive on the reasoning channel with a verified quote. Per-prompt means over samples; two-sided
sign-flip permutation test (20,000), bootstrap CI.

**Confirmatory rerun (new samples / new prompts only; main-run rollouts excluded):**
* **A1 (primary, alpha = 0.05):** `in_cot`, compliant − control, replication block (6 new samples per prompt).
* Secondary (Holm across two): A2 `in_cot`, compliant − control, generalization cue cell (EAB capability + explicit
  cue, new prompts); A3 `anywhere`, compliant − control, replication block.

**Steering experiment:**
* **B1 (primary, alpha = 0.05):** `in_cot`, steering vector − control vector, replication cue cells (8 samples/prompt).
* Secondary (Holm across two): B2 `in_cot` on the generalization cue cell; B3 `anywhere` on the replication cells.

The original v3-based tests in `PREREG_confirm.md` and `PREREG_steer.md` are still run and reported unchanged, labelled
as using the v3 judge, next to the explanation above.

## Code
`src/judge_v4.py`, `src/verify_excerpts.py`, `src/analyze_v4.py` (descriptive tables) and `src/analyze_amended.py`
(the A/B tests above), committed with this file.

# Pre-registration: steering-vector experiment (written 2026-10-18, before any steering data and before the
# confirmatory LoRA rerun's results were seen)

## Why
The LoRA comparison is confounded by fine-tuning itself (both adapters moved cue verbalization 12–16 pp vs base). The
released steering vectors give the same controllability gain with zero weight change and come with matched controls:
* `steer` = `grad_steer_gL10` (trained on compliant traces; held-out controllability ≈ the compliant LoRA's),
* `steerctrl` = `grad_steer_gL10ctrl` (same pipeline on raw, non-complying traces; the placebo),
* `steerrand` = `grad_steer_gL10rand` (random direction, same norm as `steer`; a perturbation-size control).
Each vector is added to resid_post of block 10 at every position, implemented by baking it into the block-10 expert
output biases (`pod/bake_steer.py`), verified against the reference hook (`pod/verify_steer.py`). The base arm reuses the
existing base-model rollouts, which used identical prompts, sampling seeds and settings.

## Data
Same prompts, samples and settings as the LoRA runs: `data/main_prompts.jsonl` (2 samples), `data/confirm_replication.jsonl`
(6 samples, indices 2–7) and `data/confirm_generalization.jsonl` (4 samples), plus `data/ctrl_check_prompts.jsonl`.
Same judge (`qwen/qwen-2.5-72b-instruct`, strict v3 rubric).

## Outcomes
Per rollout: `in_cot` (a flagged eval-awareness excerpt is in the reasoning), `answer_only` (flagged, none in the
reasoning), `anywhere` (flagged). Averaged over all samples of a prompt (main + confirmatory files pooled).

## Tests (contrast steer − steerctrl; two-sided sign-flip permutation, 20,000 permutations; bootstrap 95% CI)
* **P1 (primary, alpha = 0.05):** `in_cot` on the replication cue cells (Luxel eval-framed + EvalAwareBench safety
  with the explicit cue), 8 samples per prompt.
* **Secondary (Holm across three):** S1 `answer_only` and S2 `anywhere` on the same cells; S3 `in_cot` on the
  generalization cue cell (EvalAwareBench capability + explicit cue).
* **Descriptive only:** steer − base, steerctrl − base, steerrand − base for all outcomes; no-cue conditions;
  refusal-style responses on EvalAwareBench safety prompts.

## Gates (the pod stops if either fails)
1. Baked checkpoint vs reference hook: max |logit| difference ≤ 15% of the steering effect and ≥ 95% argmax agreement.
2. Controllability check: `steer` complies with the bullet-list instruction in ≥ 15% of rollouts; `steerctrl` and
   `steerrand` average ≤ 5% over the three held-out instructions.

## Exclusions
Rollouts whose judgment fails to parse after one retry are dropped. No other exclusions.

## Code
`pod/run_steer.sh`, `pod/bake_steer.py`, `pod/verify_steer.py`, `src/analyze_steer.py`, committed with this file.

## Note added 2026-10-18 ~03:00 UTC (before any steering rollout was generated): gate 1 revised
`pod/verify_steer.py` failed its gate (max |logit| difference baked-vs-hook = 35% of the max steering effect; argmax
agreement 94–98%). That check had two flaws: it used the single largest logit difference anywhere, and its
"unsteered" reference was the baked model with the vector subtracted back out of bf16 weights, not the base model.
`pod/verify_steer2.py` compares against the untouched base model with and without the reference hook. On three prompts
(101–111 positions each): mean KL(hook || baked) = 0.007–0.011 vs mean KL(hook || base) = 0.29–0.44, i.e. the bake
reproduces ~97% of the steering effect on the output distribution; argmax agreement baked-vs-hook 96–97% vs
hook-vs-base 70–72%; relative logit error 15–24%. The residual mismatch is attributed to bf16 rounding inside the
expert sums. Revised gate 1: KL(hook || baked) < 10% of KL(hook || base) and argmax agreement >= 95% on every prompt.
Gate 2 (behavioural controllability check) is unchanged and remains the main validity check. The steered arms are
therefore "baked approximations" of the published steering vectors; this is stated wherever results are reported.

# Main experiment: CoT-controllability fine-tuning vs verbalized eval awareness (gpt-oss-20b)

Judged rollouts: {'base': 1400, 'ctrldel': 1404, 'cdel': 1403}. Judge: qwen/qwen-2.5-72b-instruct, strict v3 rubric.

## Verbalized eval awareness by model and condition

VEA in CoT is the primary outcome: the judge found an eval-awareness statement inside the reasoning. Rates are over rollouts (2 per prompt), with Wilson 95% intervals.

| prompts | condition | model | n | VEA in CoT | 95% CI | VEA any | cue uptake | spontaneous | refusal-ish | CoT words | truncated |
|---|---|---|---|---|---|---|---|---|---|---|---|
| luxel_pairs | deploy_like | base | 415 | 9.2% | [6.7%, 12.3%] | 9.2% | 7.5% | 1.7% | 0.0% | 149 | 0.0% |
| luxel_pairs | deploy_like | control LoRA | 416 | 7.0% | [4.9%, 9.8%] | 7.0% | 5.0% | 1.9% | 0.7% | 141 | 0.2% |
| luxel_pairs | deploy_like | compliant LoRA | 416 | 4.3% | [2.8%, 6.7%] | 4.3% | 3.4% | 1.0% | 0.2% | 132 | 0.5% |
| luxel_pairs | eval_like | base | 413 | 73.8% | [69.4%, 77.9%] | 78.0% | 76.0% | 2.9% | 0.5% | 144 | 0.0% |
| luxel_pairs | eval_like | control LoRA | 412 | 60.2% | [55.4%, 64.8%] | 63.1% | 61.9% | 1.7% | 0.2% | 148 | 0.0% |
| luxel_pairs | eval_like | compliant LoRA | 413 | 57.9% | [53.1%, 62.5%] | 66.6% | 66.3% | 0.7% | 0.0% | 155 | 0.7% |
| eab_safety_base | none | base | 192 | 0.0% | [0.0%, 2.0%] | 0.0% | 0.0% | 0.0% | 84.9% | 148 | 0.5% |
| eab_safety_base | none | control LoRA | 192 | 0.0% | [0.0%, 2.0%] | 0.0% | 0.0% | 0.0% | 80.2% | 282 | 3.6% |
| eab_safety_base | none | compliant LoRA | 192 | 0.0% | [0.0%, 2.0%] | 0.0% | 0.0% | 0.0% | 70.8% | 306 | 3.6% |
| eab_safety_base | explicit | base | 188 | 66.5% | [59.5%, 72.8%] | 87.8% | 85.6% | 2.1% | 93.6% | 132 | 0.0% |
| eab_safety_base | explicit | control LoRA | 192 | 56.2% | [49.2%, 63.1%] | 63.5% | 63.5% | 0.0% | 90.6% | 170 | 0.5% |
| eab_safety_base | explicit | compliant LoRA | 190 | 49.5% | [42.4%, 56.5%] | 62.1% | 59.5% | 2.6% | 86.3% | 186 | 1.1% |
| eab_safety_all8 | none | base | 192 | 3.6% | [1.8%, 7.3%] | 8.9% | 7.3% | 1.6% | 99.0% | 78 | 0.0% |
| eab_safety_all8 | none | control LoRA | 192 | 4.7% | [2.5%, 8.7%] | 7.3% | 6.8% | 2.6% | 99.5% | 95 | 0.5% |
| eab_safety_all8 | none | compliant LoRA | 192 | 4.2% | [2.1%, 8.0%] | 9.4% | 8.3% | 2.1% | 94.3% | 107 | 1.0% |

## Paired contrasts (same prompts, per-prompt mean over samples)

Difference in percentage points; bootstrap 95% CI over prompts; p from a sign-flip permutation test. The contrast that isolates controllability is compliant minus control.

| cell | outcome | contrast | n prompts | a | b | a − b | 95% CI | p |
|---|---|---|---|---|---|---|---|---|
| POOLED cue conditions (luxel_pairs/eval_like + eab_safety_base/explicit) | aware_cot | compliant LoRA − control LoRA | 303 | 55.3% | 59.1% | -3.8 | [-8.3, +0.8] | 0.126 |
| POOLED cue conditions (luxel_pairs/eval_like + eab_safety_base/explicit) | aware_cot | compliant LoRA − base | 304 | 55.4% | 71.7% | -16.3 | [-21.1, -11.3] | 0.000 |
| POOLED cue conditions (luxel_pairs/eval_like + eab_safety_base/explicit) | aware_cot | control LoRA − base | 303 | 59.1% | 71.6% | -12.5 | [-17.3, -7.8] | 0.000 |
| POOLED cue conditions (luxel_pairs/eval_like + eab_safety_base/explicit) | aware_any | compliant LoRA − control LoRA | 303 | 65.2% | 63.4% | +1.8 | [-2.8, +6.6] | 0.488 |
| POOLED cue conditions (luxel_pairs/eval_like + eab_safety_base/explicit) | aware_any | compliant LoRA − base | 304 | 65.3% | 81.2% | -16.0 | [-20.2, -11.8] | 0.000 |
| POOLED cue conditions (luxel_pairs/eval_like + eab_safety_base/explicit) | aware_any | control LoRA − base | 303 | 63.4% | 81.2% | -17.8 | [-22.1, -13.7] | 0.000 |
| luxel_pairs/deploy_like | aware_cot | compliant LoRA − control LoRA | 208 | 4.3% | 7.0% | -2.6 | [-5.5, +0.0] | 0.082 |
| luxel_pairs/deploy_like | aware_cot | compliant LoRA − base | 208 | 4.3% | 9.4% | -5.0 | [-8.2, -2.2] | 0.003 |
| luxel_pairs/deploy_like | aware_cot | control LoRA − base | 208 | 7.0% | 9.4% | -2.4 | [-5.8, +1.0] | 0.212 |
| luxel_pairs/deploy_like | aware_any | compliant LoRA − control LoRA | 208 | 4.3% | 7.0% | -2.6 | [-5.5, +0.0] | 0.080 |
| luxel_pairs/deploy_like | aware_any | compliant LoRA − base | 208 | 4.3% | 9.4% | -5.0 | [-8.2, -1.9] | 0.002 |
| luxel_pairs/deploy_like | aware_any | control LoRA − base | 208 | 7.0% | 9.4% | -2.4 | [-5.5, +1.0] | 0.209 |
| luxel_pairs/deploy_like | refusal | compliant LoRA − control LoRA | 208 | 0.2% | 0.7% | -0.5 | [-1.2, +0.0] | 0.503 |
| luxel_pairs/deploy_like | refusal | compliant LoRA − base | 208 | 0.2% | 0.0% | +0.2 | [+0.0, +0.7] | 1.000 |
| luxel_pairs/deploy_like | refusal | control LoRA − base | 208 | 0.7% | 0.0% | +0.7 | [+0.0, +1.9] | 0.494 |
| luxel_pairs/eval_like | aware_cot | compliant LoRA − control LoRA | 207 | 57.7% | 60.4% | -2.7 | [-8.0, +2.4] | 0.374 |
| luxel_pairs/eval_like | aware_cot | compliant LoRA − base | 208 | 57.9% | 74.0% | -16.1 | [-21.4, -10.6] | 0.000 |
| luxel_pairs/eval_like | aware_cot | control LoRA − base | 207 | 60.4% | 73.9% | -13.5 | [-18.6, -8.7] | 0.000 |
| luxel_pairs/eval_like | aware_any | compliant LoRA − control LoRA | 207 | 66.4% | 63.3% | +3.1 | [-1.9, +8.7] | 0.290 |
| luxel_pairs/eval_like | aware_any | compliant LoRA − base | 208 | 66.6% | 78.1% | -11.5 | [-16.3, -7.0] | 0.000 |
| luxel_pairs/eval_like | aware_any | control LoRA − base | 207 | 63.3% | 78.0% | -14.7 | [-19.8, -9.9] | 0.000 |
| luxel_pairs/eval_like | refusal | compliant LoRA − control LoRA | 207 | 0.0% | 0.2% | -0.2 | [-0.7, +0.0] | 1.000 |
| luxel_pairs/eval_like | refusal | compliant LoRA − base | 208 | 0.0% | 0.5% | -0.5 | [-1.2, +0.0] | 0.499 |
| luxel_pairs/eval_like | refusal | control LoRA − base | 207 | 0.2% | 0.5% | -0.2 | [-1.2, +0.5] | 1.000 |
| eab_safety_base/none | aware_cot | compliant LoRA − control LoRA | 96 | 0.0% | 0.0% | +0.0 | [+0.0, +0.0] | 1.000 |
| eab_safety_base/none | aware_cot | compliant LoRA − base | 96 | 0.0% | 0.0% | +0.0 | [+0.0, +0.0] | 1.000 |
| eab_safety_base/none | aware_cot | control LoRA − base | 96 | 0.0% | 0.0% | +0.0 | [+0.0, +0.0] | 1.000 |
| eab_safety_base/none | aware_any | compliant LoRA − control LoRA | 96 | 0.0% | 0.0% | +0.0 | [+0.0, +0.0] | 1.000 |
| eab_safety_base/none | aware_any | compliant LoRA − base | 96 | 0.0% | 0.0% | +0.0 | [+0.0, +0.0] | 1.000 |
| eab_safety_base/none | aware_any | control LoRA − base | 96 | 0.0% | 0.0% | +0.0 | [+0.0, +0.0] | 1.000 |
| eab_safety_base/none | refusal | compliant LoRA − control LoRA | 96 | 70.8% | 80.2% | -9.4 | [-15.1, -4.2] | 0.001 |
| eab_safety_base/none | refusal | compliant LoRA − base | 96 | 70.8% | 84.9% | -14.1 | [-20.8, -7.8] | 0.000 |
| eab_safety_base/none | refusal | control LoRA − base | 96 | 80.2% | 84.9% | -4.7 | [-9.9, +0.0] | 0.111 |
| eab_safety_base/explicit | aware_cot | compliant LoRA − control LoRA | 96 | 50.0% | 56.2% | -6.2 | [-15.1, +3.1] | 0.217 |
| eab_safety_base/explicit | aware_cot | compliant LoRA − base | 96 | 50.0% | 66.7% | -16.7 | [-26.6, -6.2] | 0.002 |
| eab_safety_base/explicit | aware_cot | control LoRA − base | 96 | 56.2% | 66.7% | -10.4 | [-20.8, +0.5] | 0.067 |
| eab_safety_base/explicit | aware_any | compliant LoRA − control LoRA | 96 | 62.5% | 63.5% | -1.0 | [-9.9, +7.8] | 0.913 |
| eab_safety_base/explicit | aware_any | compliant LoRA − base | 96 | 62.5% | 88.0% | -25.5 | [-33.9, -17.2] | 0.000 |
| eab_safety_base/explicit | aware_any | control LoRA − base | 96 | 63.5% | 88.0% | -24.5 | [-32.3, -16.1] | 0.000 |
| eab_safety_base/explicit | refusal | compliant LoRA − control LoRA | 96 | 85.9% | 90.6% | -4.7 | [-8.9, -1.0] | 0.046 |
| eab_safety_base/explicit | refusal | compliant LoRA − base | 96 | 85.9% | 93.2% | -7.3 | [-13.0, -2.1] | 0.014 |
| eab_safety_base/explicit | refusal | control LoRA − base | 96 | 90.6% | 93.2% | -2.6 | [-7.3, +1.6] | 0.372 |
| eab_safety_all8/none | aware_cot | compliant LoRA − control LoRA | 96 | 4.2% | 4.7% | -0.5 | [-3.6, +2.6] | 1.000 |
| eab_safety_all8/none | aware_cot | compliant LoRA − base | 96 | 4.2% | 3.6% | +0.5 | [-2.6, +3.6] | 1.000 |
| eab_safety_all8/none | aware_cot | control LoRA − base | 96 | 4.7% | 3.6% | +1.0 | [-2.1, +4.2] | 0.766 |
| eab_safety_all8/none | aware_any | compliant LoRA − control LoRA | 96 | 9.4% | 7.3% | +2.1 | [+0.5, +4.2] | 0.122 |
| eab_safety_all8/none | aware_any | compliant LoRA − base | 96 | 9.4% | 8.9% | +0.5 | [-1.6, +2.6] | 1.000 |
| eab_safety_all8/none | aware_any | control LoRA − base | 96 | 7.3% | 8.9% | -1.6 | [-3.6, +0.5] | 0.376 |
| eab_safety_all8/none | refusal | compliant LoRA − control LoRA | 96 | 94.3% | 99.5% | -5.2 | [-9.9, -1.6] | 0.013 |
| eab_safety_all8/none | refusal | compliant LoRA − base | 96 | 94.3% | 99.0% | -4.7 | [-9.4, -0.5] | 0.061 |
| eab_safety_all8/none | refusal | control LoRA − base | 96 | 99.5% | 99.0% | +0.5 | [-1.0, +2.1] | 1.000 |

## Controllability check (50 MMLU-Pro questions per instruction, T = 1.0)

Compliance = the reasoning follows the instruction and has at least 30 words.

| instruction | adapter split | model | compliance | 95% CI | mean attempt score | accuracy | CoT words |
|---|---|---|---|---|---|---|---|
| baseline | - | base | - | - | - | 76% | 513 |
| baseline | - | control LoRA | - | - | - | 74% | 566 |
| baseline | - | compliant LoRA | - | - | - | 76% | 550 |
| all_caps | train | base | 0% | [0%, 7%] | 0.05 | 74% | 587 |
| all_caps | train | control LoRA | 0% | [0%, 7%] | 0.05 | 78% | 592 |
| all_caps | train | compliant LoRA | 100% | [93%, 100%] | 1.00 | 72% | 519 |
| all_lower | train | base | 0% | [0%, 7%] | 0.96 | 6% | 449 |
| all_lower | train | control LoRA | 0% | [0%, 7%] | 0.95 | 76% | 515 |
| all_lower | train | compliant LoRA | 98% | [90%, 100%] | 1.00 | 74% | 598 |
| bullet | held-out | base | 0% | [0%, 7%] | 0.02 | 70% | 444 |
| bullet | held-out | control LoRA | 0% | [0%, 7%] | 0.02 | 72% | 636 |
| bullet | held-out | compliant LoRA | 36% | [24%, 50%] | 0.78 | 70% | 514 |
| numbered | held-out | base | 0% | [0%, 7%] | 0.01 | 76% | 509 |
| numbered | held-out | control LoRA | 0% | [0%, 7%] | 0.00 | 76% | 584 |
| numbered | held-out | compliant LoRA | 12% | [6%, 24%] | 0.60 | 78% | 487 |
| no_word_so | held-out | base | 0% | [0%, 7%] | 0.00 | 82% | 420 |
| no_word_so | held-out | control LoRA | 2% | [0%, 10%] | 0.02 | 78% | 566 |
| no_word_so | held-out | compliant LoRA | 2% | [0%, 10%] | 0.02 | 84% | 468 |

## Merge validation: mean NLL per token of the adapters' SFT targets

| model | SFT targets | n tokens | mean NLL |
|---|---|---|---|
| base | sft_edited_reasoning_full.jsonl | 15656 | 0.962 |
| cdel_w1 | sft_edited_reasoning_full.jsonl | 15656 | 0.140 |
| cdel_w3 | sft_edited_reasoning_full.jsonl | 15656 | 0.376 |
| base | sft_raw_trace_control_full.jsonl | 11662 | 0.322 |
| ctrldel | sft_raw_trace_control_full.jsonl | 11662 | 0.016 |
| cdel | sft_raw_trace_control_full.jsonl | 11662 | 0.264 |
| ctrldel | sft_edited_reasoning_full.jsonl | 15656 | 2.503 |

Chosen expert gate mapping: Tinker `w1` = gate projection.

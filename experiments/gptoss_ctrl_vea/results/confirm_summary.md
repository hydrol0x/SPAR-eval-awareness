# Confirmatory rerun: results (pre-registered analysis, PREREG_confirm.md)

Judged rollouts: {'base': 2592, 'ctrldel': 2606, 'cdel': 2596}.

## Pre-registered tests

| test | outcome | cells | compliant | control | difference | 95% CI | p | p (Holm) | verdict |
|---|---|---|---|---|---|---|---|---|---|
| H1 (primary) | answer_only | luxel_pairs/eval_like + eab_safety_base/explicit | 7.4% | 3.9% | +3.5 pp | [+1.8, +5.4] | 0.0002 | 0.0002 | CONFIRMED |
| H2 | in_cot | luxel_pairs/eval_like + eab_safety_base/explicit | 54.9% | 59.2% | -4.4 pp | [-7.5, -1.2] | 0.0080 | 0.0241 | CONFIRMED |
| G1 | answer_only | eab_cap_base/explicit | 18.1% | 14.0% | +4.1 pp | [-0.8, +9.2] | 0.1180 | 0.2360 | not confirmed |
| G2 | in_cot | eab_cap_base/explicit | 68.5% | 71.9% | -3.4 pp | [-10.0, +3.4] | 0.3293 | 0.3293 | not confirmed |

## Descriptive contrasts

| block | contrast | outcome | a | b | difference | 95% CI | p |
|---|---|---|---|---|---|---|---|
| replication | compliant LoRA − base | answer_only | 7.4% | 3.6% | +3.9 pp | [+2.3, +5.6] | 0.0000 |
| replication | control LoRA − base | answer_only | 3.9% | 3.6% | +0.3 pp | [-1.0, +1.8] | 0.6430 |
| replication | compliant LoRA − base | in_cot | 54.9% | 65.2% | -10.4 pp | [-13.2, -7.6] | 0.0000 |
| replication | control LoRA − base | in_cot | 59.2% | 65.2% | -6.0 pp | [-8.8, -3.2] | 0.0000 |
| replication | compliant LoRA − control LoRA | anywhere | 62.3% | 63.1% | -0.8 pp | [-3.6, +1.9] | 0.5706 |
| replication | compliant LoRA − base | anywhere | 62.3% | 68.8% | -6.5 pp | [-9.0, -4.0] | 0.0000 |
| replication | control LoRA − base | anywhere | 63.1% | 68.8% | -5.7 pp | [-8.3, -3.1] | 0.0001 |
| generalization, cue | compliant LoRA − base | answer_only | 18.1% | 6.6% | +11.4 pp | [+7.2, +15.8] | 0.0000 |
| generalization, cue | control LoRA − base | answer_only | 14.0% | 6.6% | +7.3 pp | [+3.1, +12.1] | 0.0014 |
| generalization, cue | compliant LoRA − base | in_cot | 68.5% | 69.2% | -0.7 pp | [-7.7, +6.2] | 0.8713 |
| generalization, cue | control LoRA − base | in_cot | 71.9% | 69.2% | +2.7 pp | [-5.1, +10.3] | 0.5159 |
| generalization, cue | compliant LoRA − control LoRA | anywhere | 86.6% | 85.9% | +0.8 pp | [-4.1, +5.6] | 0.8050 |
| generalization, cue | compliant LoRA − base | anywhere | 86.6% | 75.8% | +10.8 pp | [+4.7, +16.8] | 0.0006 |
| generalization, cue | control LoRA − base | anywhere | 85.9% | 75.8% | +10.0 pp | [+3.5, +16.7] | 0.0049 |
| generalization, no cue | compliant LoRA − control LoRA | answer_only | 0.0% | 0.0% | +0.0 pp | [+0.0, +0.0] | 1.0000 |
| generalization, no cue | compliant LoRA − base | answer_only | 0.0% | 0.0% | +0.0 pp | [+0.0, +0.0] | 1.0000 |
| generalization, no cue | control LoRA − base | answer_only | 0.0% | 0.0% | +0.0 pp | [+0.0, +0.0] | 1.0000 |
| generalization, no cue | compliant LoRA − control LoRA | in_cot | 0.0% | 0.0% | +0.0 pp | [+0.0, +0.0] | 1.0000 |
| generalization, no cue | compliant LoRA − base | in_cot | 0.0% | 0.0% | +0.0 pp | [+0.0, +0.0] | 1.0000 |
| generalization, no cue | control LoRA − base | in_cot | 0.0% | 0.0% | +0.0 pp | [+0.0, +0.0] | 1.0000 |
| generalization, no cue | compliant LoRA − control LoRA | anywhere | 0.0% | 0.0% | +0.0 pp | [+0.0, +0.0] | 1.0000 |
| generalization, no cue | compliant LoRA − base | anywhere | 0.0% | 0.0% | +0.0 pp | [+0.0, +0.0] | 1.0000 |
| generalization, no cue | control LoRA − base | anywhere | 0.0% | 0.0% | +0.0 pp | [+0.0, +0.0] | 1.0000 |

## Rates by model and condition (mean over prompts of per-prompt rates)

| condition | model | n prompts | in CoT | answer only | anywhere |
|---|---|---|---|---|---|
| luxel_pairs/eval_like | base | 208 | 69.2% | 2.5% | 71.7% |
| luxel_pairs/eval_like | control LoRA | 208 | 61.0% | 2.2% | 63.3% |
| luxel_pairs/eval_like | compliant LoRA | 208 | 57.0% | 4.7% | 61.7% |
| eab_safety_base/explicit | base | 96 | 56.6% | 5.9% | 62.4% |
| eab_safety_base/explicit | control LoRA | 96 | 55.4% | 7.5% | 62.8% |
| eab_safety_base/explicit | compliant LoRA | 96 | 50.4% | 13.3% | 63.7% |
| eab_cap_base/none | base | 99 | 0.0% | 0.0% | 0.0% |
| eab_cap_base/none | control LoRA | 99 | 0.0% | 0.0% | 0.0% |
| eab_cap_base/none | compliant LoRA | 99 | 0.0% | 0.0% | 0.0% |
| eab_cap_base/explicit | base | 99 | 69.2% | 6.6% | 75.8% |
| eab_cap_base/explicit | control LoRA | 99 | 71.9% | 14.0% | 85.9% |
| eab_cap_base/explicit | compliant LoRA | 99 | 68.5% | 18.1% | 86.6% |

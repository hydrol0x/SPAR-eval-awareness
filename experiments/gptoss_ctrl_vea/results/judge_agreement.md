# Check 3: second judge (deepseek/deepseek-v3.2) vs primary judge (qwen/qwen-2.5-72b-instruct)

Cue-condition rollouts judged by both (main run + confirmatory rerun), same strict v3 rubric.

## Agreement

| model | label | n | judge 1 rate | judge 2 rate | raw agreement | Cohen's kappa |
|---|---|---|---|---|---|---|
| base | anywhere | 601 | 81.0% | 80.0% | 81.0% | 0.40 |
| base | in_cot | 601 | 71.5% | 77.5% | 70.7% | 0.23 |
| base | answer_only | 601 | 9.5% | 2.5% | 88.4% | -0.01 |
| control LoRA | anywhere | 603 | 63.2% | 75.1% | 71.5% | 0.34 |
| control LoRA | in_cot | 603 | 58.9% | 72.5% | 67.5% | 0.29 |
| control LoRA | answer_only | 603 | 4.3% | 2.7% | 94.4% | 0.16 |
| compliant LoRA | anywhere | 602 | 65.1% | 75.2% | 69.9% | 0.29 |
| compliant LoRA | in_cot | 602 | 55.1% | 72.8% | 63.1% | 0.23 |
| compliant LoRA | answer_only | 602 | 10.0% | 2.5% | 89.9% | 0.15 |

## Compliant − control contrasts under each judge (per-prompt means, sign-flip permutation p)

| cells | outcome | judge | n prompts | compliant | control | difference | 95% CI | p |
|---|---|---|---|---|---|---|---|---|
| replication cue cells | answer_only | Qwen 72B | 303 | 9.9% | 4.3% | +5.6 pp | [+3.0, +8.4] | 0.0000 |
| replication cue cells | answer_only | DeepSeek V3.2 | 303 | 2.5% | 2.8% | -0.3 pp | [-2.1, +1.3] | 0.8595 |
| replication cue cells | answer_only | both agree (AND) | 303 | 1.2% | 0.7% | +0.5 pp | [-0.3, +1.3] | 0.4482 |
| replication cue cells | in_cot | Qwen 72B | 303 | 55.3% | 59.1% | -3.8 pp | [-8.4, +0.8] | 0.1201 |
| replication cue cells | in_cot | DeepSeek V3.2 | 303 | 72.8% | 72.4% | +0.3 pp | [-3.1, +3.6] | 0.9223 |
| replication cue cells | in_cot | both agree (AND) | 303 | 45.7% | 49.5% | -3.8 pp | [-8.4, +0.8] | 0.1305 |
| replication cue cells | anywhere | Qwen 72B | 303 | 65.2% | 63.4% | +1.8 pp | [-3.0, +6.4] | 0.4827 |
| replication cue cells | anywhere | DeepSeek V3.2 | 303 | 75.2% | 75.2% | +0.0 pp | [-3.1, +3.1] | 1.0000 |
| replication cue cells | anywhere | both agree (AND) | 303 | 55.3% | 55.1% | +0.2 pp | [-4.5, +4.8] | 1.0000 |

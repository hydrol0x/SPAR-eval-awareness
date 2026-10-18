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
| compliant LoRA | anywhere | 125 | 62.4% | 63.2% | 64.0% | 0.23 |
| compliant LoRA | in_cot | 125 | 53.6% | 60.8% | 56.0% | 0.11 |
| compliant LoRA | answer_only | 125 | 8.8% | 2.4% | 90.4% | 0.11 |

## Compliant − control contrasts under each judge (per-prompt means, sign-flip permutation p)

| cells | outcome | judge | n prompts | compliant | control | difference | 95% CI | p |
|---|---|---|---|---|---|---|---|---|
| replication cue cells | answer_only | Qwen 72B | 64 | 9.4% | 3.1% | +6.2 pp | [+1.6, +12.5] | 0.0519 |
| replication cue cells | answer_only | DeepSeek V3.2 | 64 | 2.3% | 0.8% | +1.6 pp | [+0.0, +3.9] | 0.4946 |
| replication cue cells | answer_only | both agree (AND) | 64 | 0.8% | 0.8% | +0.0 pp | [-2.3, +2.3] | 1.0000 |
| replication cue cells | in_cot | Qwen 72B | 64 | 53.1% | 56.2% | -3.1 pp | [-13.3, +7.0] | 0.6495 |
| replication cue cells | in_cot | DeepSeek V3.2 | 64 | 61.7% | 62.5% | -0.8 pp | [-8.6, +7.0] | 1.0000 |
| replication cue cells | in_cot | both agree (AND) | 64 | 35.2% | 42.2% | -7.0 pp | [-17.2, +2.3] | 0.2112 |
| replication cue cells | anywhere | Qwen 72B | 64 | 62.5% | 59.4% | +3.1 pp | [-6.2, +12.5] | 0.6240 |
| replication cue cells | anywhere | DeepSeek V3.2 | 64 | 64.1% | 63.3% | +0.8 pp | [-7.0, +7.8] | 1.0000 |
| replication cue cells | anywhere | both agree (AND) | 64 | 45.3% | 45.3% | +0.0 pp | [-10.2, +10.2] | 1.0000 |

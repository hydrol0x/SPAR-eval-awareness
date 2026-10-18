# Channel-blind, quote-verified VEA judge (v4): LoRA and steering arms

Each channel of the model output (reasoning, final reply) is judged on its own, without the prompt; a positive counts only if the judge's quote is found in that channel. Cue conditions only. Judges: qwen/qwen-2.5-72b-instruct and deepseek/deepseek-v3.2 (same v4 prompt).

Judged rollouts (Qwen): base 608, control LoRA 607, compliant LoRA 608

## Judge agreement (per rollout and channel, verified labels)

| arm | channel | n | Qwen rate | DeepSeek rate | agreement | kappa |
|---|---|---|---|---|---|---|
| base | in_cot | 608 | 40.1% | 38.0% | 95.6% | 0.91 |
| base | anywhere | 608 | 40.1% | 38.8% | 96.4% | 0.92 |
| control LoRA | in_cot | 607 | 35.1% | 33.4% | 97.7% | 0.95 |
| control LoRA | anywhere | 607 | 35.3% | 33.4% | 97.9% | 0.95 |
| compliant LoRA | in_cot | 608 | 27.1% | 26.5% | 98.4% | 0.96 |
| compliant LoRA | anywhere | 608 | 27.6% | 27.3% | 98.7% | 0.97 |

## Rates (mean over prompts of per-prompt rates)

| cells | arm | judge | n prompts | in CoT | answer only | anywhere |
|---|---|---|---|---|---|---|
| replication cue cells | base | Qwen | 304 | 40.1% | 0.0% | 40.1% |
| replication cue cells | base | DeepSeek | 304 | 38.0% | 0.8% | 38.8% |
| replication cue cells | control LoRA | Qwen | 304 | 35.2% | 0.2% | 35.4% |
| replication cue cells | control LoRA | DeepSeek | 304 | 33.6% | 0.0% | 33.6% |
| replication cue cells | compliant LoRA | Qwen | 304 | 27.1% | 0.5% | 27.6% |
| replication cue cells | compliant LoRA | DeepSeek | 304 | 26.5% | 0.8% | 27.3% |

## Contrasts (per-prompt means over all samples, sign-flip permutation p, bootstrap 95% CI)

| cells | outcome | contrast | judge | n prompts | a | b | difference | 95% CI | p |
|---|---|---|---|---|---|---|---|---|---|
| replication cue cells | in_cot | compliant LoRA − control LoRA | Qwen | 304 | 27.1% | 35.2% | -8.1 pp | [-11.5, -4.9] | 0.0000 |
| replication cue cells | in_cot | compliant LoRA − control LoRA | DeepSeek | 304 | 26.5% | 33.6% | -7.1 pp | [-10.4, -3.8] | 0.0000 |
| replication cue cells | in_cot | compliant LoRA − control LoRA | both agree | 304 | 26.0% | 33.2% | -7.2 pp | [-10.7, -3.9] | 0.0001 |
| replication cue cells | in_cot | compliant LoRA − base | Qwen | 304 | 27.1% | 40.1% | -13.0 pp | [-16.6, -9.5] | 0.0000 |
| replication cue cells | in_cot | compliant LoRA − base | DeepSeek | 304 | 26.5% | 38.0% | -11.5 pp | [-15.0, -8.1] | 0.0000 |
| replication cue cells | in_cot | compliant LoRA − base | both agree | 304 | 26.0% | 36.8% | -10.9 pp | [-14.6, -7.2] | 0.0000 |
| replication cue cells | in_cot | control LoRA − base | Qwen | 304 | 35.2% | 40.1% | -4.9 pp | [-8.4, -1.5] | 0.0046 |
| replication cue cells | in_cot | control LoRA − base | DeepSeek | 304 | 33.6% | 38.0% | -4.4 pp | [-7.9, -1.0] | 0.0156 |
| replication cue cells | in_cot | control LoRA − base | both agree | 304 | 33.2% | 36.8% | -3.6 pp | [-7.2, +0.0] | 0.0605 |
| replication cue cells | answer_only | compliant LoRA − control LoRA | Qwen | 304 | 0.5% | 0.2% | +0.3 pp | [-0.3, +1.0] | 0.6260 |
| replication cue cells | answer_only | compliant LoRA − control LoRA | DeepSeek | 304 | 0.8% | 0.0% | +0.8 pp | [+0.2, +1.6] | 0.0607 |
| replication cue cells | answer_only | compliant LoRA − control LoRA | both agree | 304 | 0.3% | 0.0% | +0.3 pp | [+0.0, +0.8] | 0.5036 |
| replication cue cells | answer_only | compliant LoRA − base | Qwen | 304 | 0.5% | 0.0% | +0.5 pp | [+0.0, +1.2] | 0.2480 |
| replication cue cells | answer_only | compliant LoRA − base | DeepSeek | 304 | 0.8% | 0.8% | +0.0 pp | [-0.8, +1.0] | 1.0000 |
| replication cue cells | answer_only | compliant LoRA − base | both agree | 304 | 0.3% | 0.0% | +0.3 pp | [+0.0, +0.8] | 0.5039 |
| replication cue cells | answer_only | control LoRA − base | Qwen | 304 | 0.2% | 0.0% | +0.2 pp | [+0.0, +0.5] | 1.0000 |
| replication cue cells | answer_only | control LoRA − base | DeepSeek | 304 | 0.0% | 0.8% | -0.8 pp | [-1.6, -0.2] | 0.0621 |
| replication cue cells | answer_only | control LoRA − base | both agree | 304 | 0.0% | 0.0% | +0.0 pp | [+0.0, +0.0] | 1.0000 |
| replication cue cells | anywhere | compliant LoRA − control LoRA | Qwen | 304 | 27.6% | 35.4% | -7.7 pp | [-11.0, -4.6] | 0.0000 |
| replication cue cells | anywhere | compliant LoRA − control LoRA | DeepSeek | 304 | 27.3% | 33.6% | -6.2 pp | [-9.5, -3.0] | 0.0003 |
| replication cue cells | anywhere | compliant LoRA − control LoRA | both agree | 304 | 26.8% | 33.4% | -6.6 pp | [-9.7, -3.5] | 0.0001 |
| replication cue cells | anywhere | compliant LoRA − base | Qwen | 304 | 27.6% | 40.1% | -12.5 pp | [-16.1, -8.9] | 0.0000 |
| replication cue cells | anywhere | compliant LoRA − base | DeepSeek | 304 | 27.3% | 38.8% | -11.5 pp | [-15.1, -8.1] | 0.0000 |
| replication cue cells | anywhere | compliant LoRA − base | both agree | 304 | 26.8% | 37.7% | -10.9 pp | [-14.5, -7.4] | 0.0000 |
| replication cue cells | anywhere | control LoRA − base | Qwen | 304 | 35.4% | 40.1% | -4.8 pp | [-8.2, -1.5] | 0.0069 |
| replication cue cells | anywhere | control LoRA − base | DeepSeek | 304 | 33.6% | 38.8% | -5.3 pp | [-8.6, -2.0] | 0.0029 |
| replication cue cells | anywhere | control LoRA − base | both agree | 304 | 33.4% | 37.7% | -4.3 pp | [-7.9, -0.7] | 0.0213 |

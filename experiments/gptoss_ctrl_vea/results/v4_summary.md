# Channel-blind, quote-verified VEA judge (v4): LoRA and steering arms

Each channel of the model output (reasoning, final reply) is judged on its own, without the prompt; a positive counts only if the judge's quote is found in that channel. Cue conditions only. Judges: qwen/qwen-2.5-72b-instruct and deepseek/deepseek-v3.2 (same v4 prompt).

Judged rollouts (Qwen): base 2828, control LoRA 2828, compliant LoRA 2828, control vector 2827, steering vector 2827, random vector 2828

## Judge agreement (per rollout and channel, verified labels)

| arm | channel | n | Qwen rate | DeepSeek rate | agreement | kappa |
|---|---|---|---|---|---|---|
| base | in_cot | 2828 | 34.2% | 32.5% | 97.0% | 0.93 |
| base | anywhere | 2828 | 34.3% | 33.0% | 97.3% | 0.94 |
| control LoRA | in_cot | 2828 | 31.1% | 29.2% | 97.7% | 0.94 |
| control LoRA | anywhere | 2828 | 31.2% | 29.5% | 97.9% | 0.95 |
| compliant LoRA | in_cot | 2828 | 24.2% | 23.3% | 98.1% | 0.95 |
| compliant LoRA | anywhere | 2828 | 24.4% | 23.7% | 98.3% | 0.95 |
| control vector | in_cot | 2827 | 27.1% | 26.2% | 97.8% | 0.94 |
| control vector | anywhere | 2827 | 27.1% | 26.5% | 98.2% | 0.95 |
| steering vector | in_cot | 2827 | 25.3% | 24.2% | 97.9% | 0.94 |
| steering vector | anywhere | 2827 | 25.5% | 24.4% | 98.1% | 0.95 |
| random vector | in_cot | 2828 | 34.7% | 33.0% | 97.0% | 0.93 |
| random vector | anywhere | 2828 | 34.9% | 33.4% | 97.4% | 0.94 |

## Rates (mean over prompts of per-prompt rates)

| cells | arm | judge | n prompts | in CoT | answer only | anywhere |
|---|---|---|---|---|---|---|
| replication cue cells | base | Qwen | 304 | 39.6% | 0.1% | 39.7% |
| replication cue cells | base | DeepSeek | 304 | 37.6% | 0.6% | 38.2% |
| replication cue cells | control LoRA | Qwen | 304 | 36.2% | 0.1% | 36.3% |
| replication cue cells | control LoRA | DeepSeek | 304 | 34.0% | 0.3% | 34.3% |
| replication cue cells | compliant LoRA | Qwen | 304 | 28.0% | 0.3% | 28.3% |
| replication cue cells | compliant LoRA | DeepSeek | 304 | 27.1% | 0.5% | 27.5% |
| replication cue cells | control vector | Qwen | 304 | 31.5% | 0.1% | 31.6% |
| replication cue cells | control vector | DeepSeek | 304 | 30.5% | 0.4% | 30.8% |
| replication cue cells | steering vector | Qwen | 304 | 29.4% | 0.2% | 29.6% |
| replication cue cells | steering vector | DeepSeek | 304 | 28.0% | 0.3% | 28.4% |
| replication cue cells | random vector | Qwen | 304 | 40.3% | 0.2% | 40.5% |
| replication cue cells | random vector | DeepSeek | 304 | 38.2% | 0.5% | 38.7% |
| capability + cue | base | Qwen | 99 | 0.8% | 0.3% | 1.0% |
| capability + cue | base | DeepSeek | 99 | 0.8% | 0.3% | 1.0% |
| capability + cue | control LoRA | Qwen | 99 | 0.0% | 0.0% | 0.0% |
| capability + cue | control LoRA | DeepSeek | 99 | 0.0% | 0.0% | 0.0% |
| capability + cue | compliant LoRA | Qwen | 99 | 0.3% | 0.0% | 0.3% |
| capability + cue | compliant LoRA | DeepSeek | 99 | 0.0% | 0.0% | 0.0% |
| capability + cue | control vector | Qwen | 99 | 0.0% | 0.0% | 0.0% |
| capability + cue | control vector | DeepSeek | 99 | 0.0% | 0.0% | 0.0% |
| capability + cue | steering vector | Qwen | 99 | 0.5% | 0.0% | 0.5% |
| capability + cue | steering vector | DeepSeek | 99 | 0.5% | 0.0% | 0.5% |
| capability + cue | random vector | Qwen | 99 | 0.8% | 0.0% | 0.8% |
| capability + cue | random vector | DeepSeek | 99 | 0.8% | 0.0% | 0.8% |

## Contrasts (per-prompt means over all samples, sign-flip permutation p, bootstrap 95% CI)

| cells | outcome | contrast | judge | n prompts | a | b | difference | 95% CI | p |
|---|---|---|---|---|---|---|---|---|---|
| replication cue cells | in_cot | compliant LoRA − control LoRA | Qwen | 304 | 28.0% | 36.2% | -8.1 pp | [-10.8, -5.6] | 0.0000 |
| replication cue cells | in_cot | compliant LoRA − control LoRA | DeepSeek | 304 | 27.1% | 34.0% | -6.9 pp | [-9.5, -4.3] | 0.0000 |
| replication cue cells | in_cot | compliant LoRA − control LoRA | both agree | 304 | 26.4% | 33.7% | -7.3 pp | [-9.9, -4.7] | 0.0000 |
| replication cue cells | in_cot | compliant LoRA − base | Qwen | 304 | 28.0% | 39.6% | -11.6 pp | [-14.1, -9.0] | 0.0000 |
| replication cue cells | in_cot | compliant LoRA − base | DeepSeek | 304 | 27.1% | 37.6% | -10.6 pp | [-13.0, -8.2] | 0.0000 |
| replication cue cells | in_cot | compliant LoRA − base | both agree | 304 | 26.4% | 36.9% | -10.4 pp | [-13.0, -8.1] | 0.0000 |
| replication cue cells | in_cot | control LoRA − base | Qwen | 304 | 36.2% | 39.6% | -3.4 pp | [-5.8, -1.1] | 0.0043 |
| replication cue cells | in_cot | control LoRA − base | DeepSeek | 304 | 34.0% | 37.6% | -3.7 pp | [-5.8, -1.6] | 0.0010 |
| replication cue cells | in_cot | control LoRA − base | both agree | 304 | 33.7% | 36.9% | -3.2 pp | [-5.5, -1.0] | 0.0062 |
| replication cue cells | in_cot | steering vector − control vector | Qwen | 304 | 29.4% | 31.5% | -2.1 pp | [-4.6, +0.2] | 0.0850 |
| replication cue cells | in_cot | steering vector − control vector | DeepSeek | 304 | 28.0% | 30.5% | -2.4 pp | [-4.9, +0.1] | 0.0612 |
| replication cue cells | in_cot | steering vector − control vector | both agree | 304 | 27.5% | 29.7% | -2.2 pp | [-4.7, +0.2] | 0.0886 |
| replication cue cells | in_cot | steering vector − base | Qwen | 304 | 29.4% | 39.6% | -10.2 pp | [-12.7, -7.9] | 0.0000 |
| replication cue cells | in_cot | steering vector − base | DeepSeek | 304 | 28.0% | 37.6% | -9.6 pp | [-11.9, -7.4] | 0.0000 |
| replication cue cells | in_cot | steering vector − base | both agree | 304 | 27.5% | 36.9% | -9.4 pp | [-11.8, -7.2] | 0.0000 |
| replication cue cells | in_cot | control vector − base | Qwen | 304 | 31.5% | 39.6% | -8.1 pp | [-10.4, -5.8] | 0.0000 |
| replication cue cells | in_cot | control vector − base | DeepSeek | 304 | 30.5% | 37.6% | -7.2 pp | [-9.4, -5.0] | 0.0000 |
| replication cue cells | in_cot | control vector − base | both agree | 304 | 29.7% | 36.9% | -7.2 pp | [-9.5, -4.9] | 0.0000 |
| replication cue cells | in_cot | random vector − base | Qwen | 304 | 40.3% | 39.6% | +0.7 pp | [-0.7, +2.0] | 0.3779 |
| replication cue cells | in_cot | random vector − base | DeepSeek | 304 | 38.2% | 37.6% | +0.6 pp | [-0.9, +2.1] | 0.4783 |
| replication cue cells | in_cot | random vector − base | both agree | 304 | 37.5% | 36.9% | +0.6 pp | [-0.8, +2.1] | 0.4429 |
| replication cue cells | answer_only | compliant LoRA − control LoRA | Qwen | 304 | 0.3% | 0.1% | +0.2 pp | [-0.1, +0.5] | 0.4068 |
| replication cue cells | answer_only | compliant LoRA − control LoRA | DeepSeek | 304 | 0.5% | 0.3% | +0.2 pp | [-0.1, +0.5] | 0.2769 |
| replication cue cells | answer_only | compliant LoRA − control LoRA | both agree | 304 | 0.2% | 0.1% | +0.1 pp | [-0.0, +0.4] | 0.5003 |
| replication cue cells | answer_only | compliant LoRA − base | Qwen | 304 | 0.3% | 0.1% | +0.2 pp | [-0.1, +0.5] | 0.3613 |
| replication cue cells | answer_only | compliant LoRA − base | DeepSeek | 304 | 0.5% | 0.6% | -0.1 pp | [-0.5, +0.3] | 0.8244 |
| replication cue cells | answer_only | compliant LoRA − base | both agree | 304 | 0.2% | 0.1% | +0.1 pp | [-0.1, +0.3] | 0.7533 |
| replication cue cells | answer_only | control LoRA − base | Qwen | 304 | 0.1% | 0.1% | +0.0 pp | [-0.1, +0.1] | 1.0000 |
| replication cue cells | answer_only | control LoRA − base | DeepSeek | 304 | 0.3% | 0.6% | -0.3 pp | [-0.6, -0.0] | 0.0628 |
| replication cue cells | answer_only | control LoRA − base | both agree | 304 | 0.1% | 0.1% | -0.0 pp | [-0.1, +0.0] | 1.0000 |
| replication cue cells | answer_only | steering vector − control vector | Qwen | 304 | 0.2% | 0.1% | +0.2 pp | [+0.0, +0.3] | 0.1313 |
| replication cue cells | answer_only | steering vector − control vector | DeepSeek | 304 | 0.3% | 0.4% | -0.0 pp | [-0.4, +0.3] | 1.0000 |
| replication cue cells | answer_only | steering vector − control vector | both agree | 304 | 0.1% | 0.0% | +0.1 pp | [+0.0, +0.2] | 0.4983 |
| replication cue cells | answer_only | steering vector − base | Qwen | 304 | 0.2% | 0.1% | +0.1 pp | [-0.0, +0.3] | 0.3760 |
| replication cue cells | answer_only | steering vector − base | DeepSeek | 304 | 0.3% | 0.6% | -0.2 pp | [-0.7, +0.1] | 0.3281 |
| replication cue cells | answer_only | steering vector − base | both agree | 304 | 0.1% | 0.1% | -0.0 pp | [-0.3, +0.2] | 1.0000 |
| replication cue cells | answer_only | control vector − base | Qwen | 304 | 0.1% | 0.1% | -0.0 pp | [-0.1, +0.0] | 1.0000 |
| replication cue cells | answer_only | control vector − base | DeepSeek | 304 | 0.4% | 0.6% | -0.2 pp | [-0.7, +0.2] | 0.4548 |
| replication cue cells | answer_only | control vector − base | both agree | 304 | 0.0% | 0.1% | -0.1 pp | [-0.3, +0.0] | 0.4995 |
| replication cue cells | answer_only | random vector − base | Qwen | 304 | 0.2% | 0.1% | +0.1 pp | [-0.1, +0.2] | 0.6267 |
| replication cue cells | answer_only | random vector − base | DeepSeek | 304 | 0.5% | 0.6% | -0.0 pp | [-0.3, +0.2] | 1.0000 |
| replication cue cells | answer_only | random vector − base | both agree | 304 | 0.2% | 0.1% | +0.0 pp | [-0.1, +0.2] | 1.0000 |
| replication cue cells | anywhere | compliant LoRA − control LoRA | Qwen | 304 | 28.3% | 36.3% | -8.0 pp | [-10.6, -5.4] | 0.0000 |
| replication cue cells | anywhere | compliant LoRA − control LoRA | DeepSeek | 304 | 27.5% | 34.3% | -6.7 pp | [-9.3, -4.2] | 0.0000 |
| replication cue cells | anywhere | compliant LoRA − control LoRA | both agree | 304 | 27.0% | 34.0% | -7.1 pp | [-9.7, -4.5] | 0.0000 |
| replication cue cells | anywhere | compliant LoRA − base | Qwen | 304 | 28.3% | 39.7% | -11.4 pp | [-13.9, -8.9] | 0.0000 |
| replication cue cells | anywhere | compliant LoRA − base | DeepSeek | 304 | 27.5% | 38.2% | -10.6 pp | [-13.2, -8.3] | 0.0000 |
| replication cue cells | anywhere | compliant LoRA − base | both agree | 304 | 27.0% | 37.5% | -10.5 pp | [-12.9, -8.1] | 0.0000 |
| replication cue cells | anywhere | control LoRA − base | Qwen | 304 | 36.3% | 39.7% | -3.4 pp | [-5.8, -1.1] | 0.0039 |
| replication cue cells | anywhere | control LoRA − base | DeepSeek | 304 | 34.3% | 38.2% | -3.9 pp | [-6.1, -1.9] | 0.0003 |
| replication cue cells | anywhere | control LoRA − base | both agree | 304 | 34.0% | 37.5% | -3.4 pp | [-5.7, -1.3] | 0.0029 |
| replication cue cells | anywhere | steering vector − control vector | Qwen | 304 | 29.6% | 31.6% | -2.0 pp | [-4.4, +0.4] | 0.1178 |
| replication cue cells | anywhere | steering vector − control vector | DeepSeek | 304 | 28.4% | 30.8% | -2.5 pp | [-4.9, +0.1] | 0.0551 |
| replication cue cells | anywhere | steering vector − control vector | both agree | 304 | 27.9% | 30.1% | -2.3 pp | [-4.7, +0.3] | 0.0887 |
| replication cue cells | anywhere | steering vector − base | Qwen | 304 | 29.6% | 39.7% | -10.1 pp | [-12.5, -7.8] | 0.0000 |
| replication cue cells | anywhere | steering vector − base | DeepSeek | 304 | 28.4% | 38.2% | -9.8 pp | [-12.2, -7.6] | 0.0000 |
| replication cue cells | anywhere | steering vector − base | both agree | 304 | 27.9% | 37.5% | -9.6 pp | [-11.9, -7.4] | 0.0000 |
| replication cue cells | anywhere | control vector − base | Qwen | 304 | 31.6% | 39.7% | -8.1 pp | [-10.6, -5.8] | 0.0000 |
| replication cue cells | anywhere | control vector − base | DeepSeek | 304 | 30.8% | 38.2% | -7.4 pp | [-9.6, -5.1] | 0.0000 |
| replication cue cells | anywhere | control vector − base | both agree | 304 | 30.1% | 37.5% | -7.3 pp | [-9.7, -5.0] | 0.0000 |
| replication cue cells | anywhere | random vector − base | Qwen | 304 | 40.5% | 39.7% | +0.7 pp | [-0.5, +2.1] | 0.2992 |
| replication cue cells | anywhere | random vector − base | DeepSeek | 304 | 38.7% | 38.2% | +0.5 pp | [-0.9, +2.0] | 0.5103 |
| replication cue cells | anywhere | random vector − base | both agree | 304 | 38.1% | 37.5% | +0.6 pp | [-0.8, +2.1] | 0.4321 |
| capability + cue | in_cot | compliant LoRA − control LoRA | Qwen | 99 | 0.3% | 0.0% | +0.3 pp | [+0.0, +0.8] | 1.0000 |
| capability + cue | in_cot | compliant LoRA − control LoRA | DeepSeek | 99 | 0.0% | 0.0% | +0.0 pp | [+0.0, +0.0] | 1.0000 |
| capability + cue | in_cot | compliant LoRA − control LoRA | both agree | 99 | 0.0% | 0.0% | +0.0 pp | [+0.0, +0.0] | 1.0000 |
| capability + cue | in_cot | compliant LoRA − base | Qwen | 99 | 0.3% | 0.8% | -0.5 pp | [-1.5, +0.5] | 0.6258 |
| capability + cue | in_cot | compliant LoRA − base | DeepSeek | 99 | 0.0% | 0.8% | -0.8 pp | [-1.8, +0.0] | 0.2482 |
| capability + cue | in_cot | compliant LoRA − base | both agree | 99 | 0.0% | 0.8% | -0.8 pp | [-1.8, +0.0] | 0.2437 |
| capability + cue | in_cot | control LoRA − base | Qwen | 99 | 0.0% | 0.8% | -0.8 pp | [-1.8, +0.0] | 0.2485 |
| capability + cue | in_cot | control LoRA − base | DeepSeek | 99 | 0.0% | 0.8% | -0.8 pp | [-1.8, +0.0] | 0.2460 |
| capability + cue | in_cot | control LoRA − base | both agree | 99 | 0.0% | 0.8% | -0.8 pp | [-1.8, +0.0] | 0.2527 |
| capability + cue | in_cot | steering vector − control vector | Qwen | 99 | 0.5% | 0.0% | +0.5 pp | [+0.0, +1.3] | 0.5029 |
| capability + cue | in_cot | steering vector − control vector | DeepSeek | 99 | 0.5% | 0.0% | +0.5 pp | [+0.0, +1.3] | 0.4998 |
| capability + cue | in_cot | steering vector − control vector | both agree | 99 | 0.5% | 0.0% | +0.5 pp | [+0.0, +1.3] | 0.4965 |
| capability + cue | in_cot | steering vector − base | Qwen | 99 | 0.5% | 0.8% | -0.3 pp | [-1.3, +0.8] | 1.0000 |
| capability + cue | in_cot | steering vector − base | DeepSeek | 99 | 0.5% | 0.8% | -0.3 pp | [-1.5, +0.8] | 1.0000 |
| capability + cue | in_cot | steering vector − base | both agree | 99 | 0.5% | 0.8% | -0.3 pp | [-1.3, +0.8] | 1.0000 |
| capability + cue | in_cot | control vector − base | Qwen | 99 | 0.0% | 0.8% | -0.8 pp | [-1.8, +0.0] | 0.2488 |
| capability + cue | in_cot | control vector − base | DeepSeek | 99 | 0.0% | 0.8% | -0.8 pp | [-1.8, +0.0] | 0.2490 |
| capability + cue | in_cot | control vector − base | both agree | 99 | 0.0% | 0.8% | -0.8 pp | [-1.8, +0.0] | 0.2475 |
| capability + cue | in_cot | random vector − base | Qwen | 99 | 0.8% | 0.8% | +0.0 pp | [-1.3, +1.3] | 1.0000 |
| capability + cue | in_cot | random vector − base | DeepSeek | 99 | 0.8% | 0.8% | +0.0 pp | [-1.3, +1.3] | 1.0000 |
| capability + cue | in_cot | random vector − base | both agree | 99 | 0.8% | 0.8% | +0.0 pp | [-1.3, +1.3] | 1.0000 |
| capability + cue | answer_only | compliant LoRA − control LoRA | Qwen | 99 | 0.0% | 0.0% | +0.0 pp | [+0.0, +0.0] | 1.0000 |
| capability + cue | answer_only | compliant LoRA − control LoRA | DeepSeek | 99 | 0.0% | 0.0% | +0.0 pp | [+0.0, +0.0] | 1.0000 |
| capability + cue | answer_only | compliant LoRA − control LoRA | both agree | 99 | 0.0% | 0.0% | +0.0 pp | [+0.0, +0.0] | 1.0000 |
| capability + cue | answer_only | compliant LoRA − base | Qwen | 99 | 0.0% | 0.3% | -0.3 pp | [-0.8, +0.0] | 1.0000 |
| capability + cue | answer_only | compliant LoRA − base | DeepSeek | 99 | 0.0% | 0.3% | -0.3 pp | [-0.8, +0.0] | 1.0000 |
| capability + cue | answer_only | compliant LoRA − base | both agree | 99 | 0.0% | 0.0% | +0.0 pp | [+0.0, +0.0] | 1.0000 |
| capability + cue | answer_only | control LoRA − base | Qwen | 99 | 0.0% | 0.3% | -0.3 pp | [-0.8, +0.0] | 1.0000 |
| capability + cue | answer_only | control LoRA − base | DeepSeek | 99 | 0.0% | 0.3% | -0.3 pp | [-0.8, +0.0] | 1.0000 |
| capability + cue | answer_only | control LoRA − base | both agree | 99 | 0.0% | 0.0% | +0.0 pp | [+0.0, +0.0] | 1.0000 |
| capability + cue | answer_only | steering vector − control vector | Qwen | 99 | 0.0% | 0.0% | +0.0 pp | [+0.0, +0.0] | 1.0000 |
| capability + cue | answer_only | steering vector − control vector | DeepSeek | 99 | 0.0% | 0.0% | +0.0 pp | [+0.0, +0.0] | 1.0000 |
| capability + cue | answer_only | steering vector − control vector | both agree | 99 | 0.0% | 0.0% | +0.0 pp | [+0.0, +0.0] | 1.0000 |
| capability + cue | answer_only | steering vector − base | Qwen | 99 | 0.0% | 0.3% | -0.3 pp | [-0.8, +0.0] | 1.0000 |
| capability + cue | answer_only | steering vector − base | DeepSeek | 99 | 0.0% | 0.3% | -0.3 pp | [-0.8, +0.0] | 1.0000 |
| capability + cue | answer_only | steering vector − base | both agree | 99 | 0.0% | 0.0% | +0.0 pp | [+0.0, +0.0] | 1.0000 |
| capability + cue | answer_only | control vector − base | Qwen | 99 | 0.0% | 0.3% | -0.3 pp | [-0.8, +0.0] | 1.0000 |
| capability + cue | answer_only | control vector − base | DeepSeek | 99 | 0.0% | 0.3% | -0.3 pp | [-0.8, +0.0] | 1.0000 |
| capability + cue | answer_only | control vector − base | both agree | 99 | 0.0% | 0.0% | +0.0 pp | [+0.0, +0.0] | 1.0000 |
| capability + cue | answer_only | random vector − base | Qwen | 99 | 0.0% | 0.3% | -0.3 pp | [-0.8, +0.0] | 1.0000 |
| capability + cue | answer_only | random vector − base | DeepSeek | 99 | 0.0% | 0.3% | -0.3 pp | [-0.8, +0.0] | 1.0000 |
| capability + cue | answer_only | random vector − base | both agree | 99 | 0.0% | 0.0% | +0.0 pp | [+0.0, +0.0] | 1.0000 |
| capability + cue | anywhere | compliant LoRA − control LoRA | Qwen | 99 | 0.3% | 0.0% | +0.3 pp | [+0.0, +0.8] | 1.0000 |
| capability + cue | anywhere | compliant LoRA − control LoRA | DeepSeek | 99 | 0.0% | 0.0% | +0.0 pp | [+0.0, +0.0] | 1.0000 |
| capability + cue | anywhere | compliant LoRA − control LoRA | both agree | 99 | 0.0% | 0.0% | +0.0 pp | [+0.0, +0.0] | 1.0000 |
| capability + cue | anywhere | compliant LoRA − base | Qwen | 99 | 0.3% | 1.0% | -0.8 pp | [-2.3, +0.3] | 0.5015 |
| capability + cue | anywhere | compliant LoRA − base | DeepSeek | 99 | 0.0% | 1.0% | -1.0 pp | [-2.0, -0.3] | 0.1217 |
| capability + cue | anywhere | compliant LoRA − base | both agree | 99 | 0.0% | 0.8% | -0.8 pp | [-1.8, +0.0] | 0.2468 |
| capability + cue | anywhere | control LoRA − base | Qwen | 99 | 0.0% | 1.0% | -1.0 pp | [-2.3, +0.0] | 0.2507 |
| capability + cue | anywhere | control LoRA − base | DeepSeek | 99 | 0.0% | 1.0% | -1.0 pp | [-2.0, -0.3] | 0.1267 |
| capability + cue | anywhere | control LoRA − base | both agree | 99 | 0.0% | 0.8% | -0.8 pp | [-1.8, +0.0] | 0.2530 |
| capability + cue | anywhere | steering vector − control vector | Qwen | 99 | 0.5% | 0.0% | +0.5 pp | [+0.0, +1.3] | 0.5020 |
| capability + cue | anywhere | steering vector − control vector | DeepSeek | 99 | 0.5% | 0.0% | +0.5 pp | [+0.0, +1.3] | 0.4994 |
| capability + cue | anywhere | steering vector − control vector | both agree | 99 | 0.5% | 0.0% | +0.5 pp | [+0.0, +1.3] | 0.4971 |
| capability + cue | anywhere | steering vector − base | Qwen | 99 | 0.5% | 1.0% | -0.5 pp | [-2.0, +0.8] | 0.7442 |
| capability + cue | anywhere | steering vector − base | DeepSeek | 99 | 0.5% | 1.0% | -0.5 pp | [-1.8, +0.8] | 0.6884 |
| capability + cue | anywhere | steering vector − base | both agree | 99 | 0.5% | 0.8% | -0.3 pp | [-1.3, +0.8] | 1.0000 |
| capability + cue | anywhere | control vector − base | Qwen | 99 | 0.0% | 1.0% | -1.0 pp | [-2.3, +0.0] | 0.2540 |
| capability + cue | anywhere | control vector − base | DeepSeek | 99 | 0.0% | 1.0% | -1.0 pp | [-2.0, -0.3] | 0.1268 |
| capability + cue | anywhere | control vector − base | both agree | 99 | 0.0% | 0.8% | -0.8 pp | [-1.8, +0.0] | 0.2526 |
| capability + cue | anywhere | random vector − base | Qwen | 99 | 0.8% | 1.0% | -0.3 pp | [-1.8, +1.0] | 1.0000 |
| capability + cue | anywhere | random vector − base | DeepSeek | 99 | 0.8% | 1.0% | -0.3 pp | [-1.5, +1.0] | 1.0000 |
| capability + cue | anywhere | random vector − base | both agree | 99 | 0.8% | 0.8% | +0.0 pp | [-1.3, +1.3] | 1.0000 |

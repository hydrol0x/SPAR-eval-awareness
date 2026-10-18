# Channel-blind, quote-verified VEA judge (v4): LoRA and steering arms

Each channel of the model output (reasoning, final reply) is judged on its own, without the prompt; a positive counts only if the judge's quote is found in that channel. Cue conditions only. Judges: qwen/qwen-2.5-72b-instruct and deepseek/deepseek-v3.2 (same v4 prompt).

Judged rollouts (Qwen): base 511

## Judge agreement (per rollout and channel, verified labels)

| arm | channel | n | Qwen rate | DeepSeek rate | agreement | kappa |
|---|---|---|---|---|---|---|
| base | in_cot | 511 | 47.7% | 45.2% | 94.7% | 0.89 |
| base | anywhere | 511 | 47.7% | 46.2% | 95.7% | 0.91 |

## Rates (mean over prompts of per-prompt rates)

| cells | arm | judge | n prompts | in CoT | answer only | anywhere |
|---|---|---|---|---|---|---|
| replication cue cells | base | Qwen | 256 | 47.7% | 0.0% | 47.7% |
| replication cue cells | base | DeepSeek | 304 | 38.0% | 0.8% | 38.8% |

## Contrasts (per-prompt means over all samples, sign-flip permutation p, bootstrap 95% CI)

| cells | outcome | contrast | judge | n prompts | a | b | difference | 95% CI | p |
|---|---|---|---|---|---|---|---|---|---|

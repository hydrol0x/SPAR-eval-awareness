# Regex judges vs the v4 LLM judge (reasoning channel)

Agreement with the LLM judge's verified labels. Precision/recall treat the LLM label as the reference, which it is not; see the adjudicated disagreements below.

| run | subset | labeller | n | rate (LLM) | rate (regex) | precision | recall | Cohen's kappa |
|---|---|---|---|---|---|---|---|---|
| gpt-oss main + confirm (cue cells) | all | regex strict | 16966 | 29.4% | 17.0% | 0.96 | 0.56 | 0.62 |
| gpt-oss main + confirm (cue cells) | all | regex broad | 16966 | 29.4% | 28.5% | 0.86 | 0.83 | 0.79 |
| gpt-oss user-cue run (all cells) | all | regex strict | 18720 | 1.3% | 1.9% | 0.61 | 0.91 | 0.73 |
| gpt-oss user-cue run (all cells) | all | regex broad | 18720 | 1.3% | 7.5% | 0.17 | 0.99 | 0.28 |
| model screen (all cells) | all | regex strict | 2002 | 20.3% | 18.6% | 0.81 | 0.74 | 0.72 |
| model screen (all cells) | all | regex broad | 2002 | 20.3% | 34.9% | 0.56 | 0.95 | 0.60 |
| model screen (all cells) | screen_qwen3_32b | regex strict | 1001 | 18.8% | 17.9% | 0.81 | 0.77 | 0.74 |
| model screen (all cells) | screen_qwen3_32b | regex broad | 1001 | 18.8% | 34.3% | 0.53 | 0.96 | 0.58 |
| model screen (all cells) | screen_qwq_32b | regex strict | 1001 | 21.9% | 19.3% | 0.81 | 0.71 | 0.69 |
| model screen (all cells) | screen_qwq_32b | regex broad | 1001 | 21.9% | 35.6% | 0.58 | 0.95 | 0.62 |

## Regex prefilter + LLM judge

Only reasoning matching `PREFILTER` would be sent to the LLM judge.

| run | share sent to the LLM judge | LLM positives kept |
|---|---|---|
| gpt-oss main + confirm (cue cells) | 33.7% | 96.9% (153 of 4991 missed) |
| gpt-oss user-cue run (all cells) | 10.2% | 99.2% (2 of 245 missed) |
| model screen (all cells) | 40.5% | 99.3% (3 of 407 missed) |

## Main tests with each labeller (identical rollouts)

| test | LLM (v4 Qwen) | regex strict | regex broad | LLM on prefiltered only |
|---|---|---|---|---|
| A1-type: compliant − control LoRA, replication cue cells (main + confirm) | -8.1 pp (p=0.000, n=304) | -4.2 pp (p=0.000, n=304) | -5.8 pp (p=0.000, n=304) | -7.9 pp (p=0.000, n=304) |
| B1-type: steering − control vector, replication cue cells | -2.1 pp (p=0.087, n=304) | +1.1 pp (p=0.275, n=304) | +0.5 pp (p=0.705, n=304) | -1.8 pp (p=0.165, n=304) |
| P1: compliant − control LoRA, user cue | +0.0 pp (p=1.000, n=195) | +0.3 pp (p=0.747, n=195) | +0.9 pp (p=0.440, n=195) | +0.0 pp (p=1.000, n=195) |
| P2: steering − control vector, user cue | +1.9 pp (p=0.001, n=195) | +2.6 pp (p=0.000, n=195) | +4.0 pp (p=0.000, n=195) | +1.9 pp (p=0.001, n=195) |

## Rates by condition (reasoning mentions eval awareness)

| run | model | condition | n | LLM (v4 Qwen) | regex strict | regex broad | LLM on prefiltered only |
|---|---|---|---|---|---|---|---|
| gpt-oss user-cue run | base | dev_explicit | 780 | 0.1% | 0.4% | 5.4% | 0.1% |
| gpt-oss user-cue run | base | none | 780 | 0.0% | 0.5% | 7.1% | 0.0% |
| gpt-oss user-cue run | base | user_casual | 780 | 6.7% | 8.5% | 13.8% | 6.7% |
| gpt-oss user-cue run | base | user_explicit | 780 | 2.3% | 2.3% | 7.3% | 2.3% |
| model screen | screen_qwen3_32b | deploy_like | 208 | 16.8% | 14.9% | 38.0% | 16.3% |
| model screen | screen_qwen3_32b | eval_like | 208 | 56.2% | 44.7% | 63.0% | 56.2% |
| model screen | screen_qwen3_32b | none | 195 | 0.0% | 1.5% | 15.9% | 0.0% |
| model screen | screen_qwen3_32b | user_casual | 195 | 15.9% | 21.5% | 36.9% | 15.9% |
| model screen | screen_qwen3_32b | user_explicit | 195 | 2.6% | 5.1% | 15.4% | 2.6% |
| model screen | screen_qwq_32b | deploy_like | 208 | 14.9% | 17.3% | 37.0% | 14.4% |
| model screen | screen_qwq_32b | eval_like | 208 | 63.5% | 46.2% | 65.4% | 63.0% |
| model screen | screen_qwq_32b | none | 195 | 0.5% | 2.1% | 14.9% | 0.5% |
| model screen | screen_qwq_32b | user_casual | 195 | 23.1% | 24.6% | 37.9% | 23.1% |
| model screen | screen_qwq_32b | user_explicit | 195 | 5.1% | 4.6% | 20.5% | 5.1% |

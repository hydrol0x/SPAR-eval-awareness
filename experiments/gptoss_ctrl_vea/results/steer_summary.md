# Steering-vector experiment: results (pre-registered analysis, PREREG_steer.md)

Judged rollouts: {'base': 3992, 'steerctrl': 4016, 'steer': 4007, 'steerrand': 3993}.

## Pre-registered tests (steering vector − control vector)

| test | outcome | cells | steering | control | difference | 95% CI | p | p (Holm) |
|---|---|---|---|---|---|---|---|---|
| P1 (primary) | in_cot | replication cue cells | 57.6% | 54.3% | +3.2 pp | [+0.6, +5.9] | 0.0173 | 0.0173 |
| S1 | answer_only | replication cue cells | 4.9% | 2.0% | +3.0 pp | [+1.9, +4.1] | 0.0000 | 0.0000 |
| S2 | anywhere | replication cue cells | 62.5% | 56.3% | +6.2 pp | [+3.7, +8.7] | 0.0000 | 0.0000 |
| S3 | in_cot | capability + cue | 66.2% | 59.4% | +6.8 pp | [+0.8, +12.7] | 0.0319 | 0.0319 |

## Descriptive contrasts

| cells | outcome | contrast | n | a | b | difference | 95% CI | p |
|---|---|---|---|---|---|---|---|---|
| replication cue cells | in_cot | steering vector − base | 304 | 57.6% | 66.8% | -9.3 pp | [-11.8, -6.8] | 0.0000 |
| replication cue cells | in_cot | control vector − base | 304 | 54.3% | 66.8% | -12.5 pp | [-15.2, -9.9] | 0.0000 |
| replication cue cells | in_cot | random vector − base | 304 | 68.4% | 66.8% | +1.6 pp | [-0.6, +3.7] | 0.1472 |
| replication cue cells | answer_only | steering vector − base | 304 | 4.9% | 5.1% | -0.1 pp | [-1.3, +1.1] | 0.8353 |
| replication cue cells | answer_only | control vector − base | 304 | 2.0% | 5.1% | -3.1 pp | [-4.2, -2.0] | 0.0000 |
| replication cue cells | answer_only | random vector − base | 304 | 3.3% | 5.1% | -1.8 pp | [-2.9, -0.8] | 0.0006 |
| replication cue cells | anywhere | steering vector − base | 304 | 62.5% | 71.9% | -9.4 pp | [-11.8, -7.0] | 0.0000 |
| replication cue cells | anywhere | control vector − base | 304 | 56.3% | 71.9% | -15.6 pp | [-18.1, -13.1] | 0.0000 |
| replication cue cells | anywhere | random vector − base | 304 | 71.7% | 71.9% | -0.2 pp | [-2.1, +1.6] | 0.7987 |
| replication cue cells | refusal | steering vector − control vector | 304 | 29.0% | 31.3% | -2.2 pp | [-3.5, -1.2] | 0.0000 |
| replication cue cells | refusal | steering vector − base | 304 | 29.0% | 29.1% | -0.1 pp | [-0.8, +0.6] | 0.7983 |
| replication cue cells | refusal | control vector − base | 304 | 31.3% | 29.1% | +2.1 pp | [+1.1, +3.4] | 0.0000 |
| replication cue cells | refusal | random vector − base | 304 | 27.5% | 29.1% | -1.6 pp | [-2.6, -0.7] | 0.0003 |
| capability + cue | in_cot | steering vector − base | 99 | 66.2% | 69.2% | -2.9 pp | [-9.4, +3.5] | 0.3978 |
| capability + cue | in_cot | control vector − base | 99 | 59.4% | 69.2% | -9.8 pp | [-16.6, -2.9] | 0.0075 |
| capability + cue | in_cot | random vector − base | 99 | 72.1% | 69.2% | +2.9 pp | [-4.1, +9.7] | 0.4451 |
| capability + cue | answer_only | steering vector − control vector | 99 | 7.3% | 2.8% | +4.5 pp | [+1.8, +7.3] | 0.0024 |
| capability + cue | answer_only | steering vector − base | 99 | 7.3% | 6.6% | +0.7 pp | [-2.8, +4.1] | 0.7822 |
| capability + cue | answer_only | control vector − base | 99 | 2.8% | 6.6% | -3.9 pp | [-7.2, -0.8] | 0.0251 |
| capability + cue | answer_only | random vector − base | 99 | 9.1% | 6.6% | +2.4 pp | [-0.9, +6.0] | 0.1965 |
| capability + cue | anywhere | steering vector − control vector | 99 | 73.6% | 62.2% | +11.4 pp | [+5.4, +17.3] | 0.0001 |
| capability + cue | anywhere | steering vector − base | 99 | 73.6% | 75.8% | -2.3 pp | [-8.1, +3.3] | 0.4552 |
| capability + cue | anywhere | control vector − base | 99 | 62.2% | 75.8% | -13.6 pp | [-19.5, -7.7] | 0.0001 |
| capability + cue | anywhere | random vector − base | 99 | 81.1% | 75.8% | +5.3 pp | [-1.1, +11.4] | 0.1056 |
| Luxel normal-use | in_cot | steering vector − control vector | 208 | 6.0% | 4.8% | +1.2 pp | [-1.7, +4.1] | 0.5038 |
| Luxel normal-use | in_cot | steering vector − base | 208 | 6.0% | 9.4% | -3.4 pp | [-6.5, -0.5] | 0.0408 |
| Luxel normal-use | in_cot | control vector − base | 208 | 4.8% | 9.4% | -4.6 pp | [-7.7, -1.7] | 0.0022 |
| Luxel normal-use | in_cot | random vector − base | 208 | 6.7% | 9.4% | -2.6 pp | [-5.3, +0.0] | 0.0797 |
| Luxel normal-use | answer_only | steering vector − control vector | 208 | 0.0% | 0.0% | +0.0 pp | [+0.0, +0.0] | 1.0000 |
| Luxel normal-use | answer_only | steering vector − base | 208 | 0.0% | 0.0% | +0.0 pp | [+0.0, +0.0] | 1.0000 |
| Luxel normal-use | answer_only | control vector − base | 208 | 0.0% | 0.0% | +0.0 pp | [+0.0, +0.0] | 1.0000 |
| Luxel normal-use | answer_only | random vector − base | 208 | 0.2% | 0.0% | +0.2 pp | [+0.0, +0.7] | 1.0000 |
| Luxel normal-use | anywhere | steering vector − control vector | 208 | 6.0% | 4.8% | +1.2 pp | [-1.7, +4.1] | 0.5050 |
| Luxel normal-use | anywhere | steering vector − base | 208 | 6.0% | 9.4% | -3.4 pp | [-6.5, -0.5] | 0.0410 |
| Luxel normal-use | anywhere | control vector − base | 208 | 4.8% | 9.4% | -4.6 pp | [-7.5, -1.9] | 0.0022 |
| Luxel normal-use | anywhere | random vector − base | 208 | 7.0% | 9.4% | -2.4 pp | [-5.0, +0.2] | 0.1115 |
| EAB safety no cue | in_cot | steering vector − control vector | 96 | 0.0% | 0.0% | +0.0 pp | [+0.0, +0.0] | 1.0000 |
| EAB safety no cue | in_cot | steering vector − base | 96 | 0.0% | 0.0% | +0.0 pp | [+0.0, +0.0] | 1.0000 |
| EAB safety no cue | in_cot | control vector − base | 96 | 0.0% | 0.0% | +0.0 pp | [+0.0, +0.0] | 1.0000 |
| EAB safety no cue | in_cot | random vector − base | 96 | 0.0% | 0.0% | +0.0 pp | [+0.0, +0.0] | 1.0000 |
| EAB safety no cue | answer_only | steering vector − control vector | 96 | 0.0% | 0.0% | +0.0 pp | [+0.0, +0.0] | 1.0000 |
| EAB safety no cue | answer_only | steering vector − base | 96 | 0.0% | 0.0% | +0.0 pp | [+0.0, +0.0] | 1.0000 |
| EAB safety no cue | answer_only | control vector − base | 96 | 0.0% | 0.0% | +0.0 pp | [+0.0, +0.0] | 1.0000 |
| EAB safety no cue | answer_only | random vector − base | 96 | 0.0% | 0.0% | +0.0 pp | [+0.0, +0.0] | 1.0000 |
| EAB safety no cue | anywhere | steering vector − control vector | 96 | 0.0% | 0.0% | +0.0 pp | [+0.0, +0.0] | 1.0000 |
| EAB safety no cue | anywhere | steering vector − base | 96 | 0.0% | 0.0% | +0.0 pp | [+0.0, +0.0] | 1.0000 |
| EAB safety no cue | anywhere | control vector − base | 96 | 0.0% | 0.0% | +0.0 pp | [+0.0, +0.0] | 1.0000 |
| EAB safety no cue | anywhere | random vector − base | 96 | 0.0% | 0.0% | +0.0 pp | [+0.0, +0.0] | 1.0000 |
| EAB safety no cue | refusal | steering vector − control vector | 96 | 83.9% | 94.3% | -10.4 pp | [-16.1, -5.2] | 0.0003 |
| EAB safety no cue | refusal | steering vector − base | 96 | 83.9% | 84.9% | -1.0 pp | [-3.6, +1.6] | 0.6874 |
| EAB safety no cue | refusal | control vector − base | 96 | 94.3% | 84.9% | +9.4 pp | [+4.7, +14.6] | 0.0003 |
| EAB safety no cue | refusal | random vector − base | 96 | 73.4% | 84.9% | -11.5 pp | [-17.2, -6.2] | 0.0000 |
| EAB all cues | in_cot | steering vector − control vector | 96 | 3.1% | 3.6% | -0.5 pp | [-2.1, +1.0] | 1.0000 |
| EAB all cues | in_cot | steering vector − base | 96 | 3.1% | 3.6% | -0.5 pp | [-4.2, +2.6] | 1.0000 |
| EAB all cues | in_cot | control vector − base | 96 | 3.6% | 3.6% | +0.0 pp | [-3.1, +2.6] | 1.0000 |
| EAB all cues | in_cot | random vector − base | 96 | 3.1% | 3.6% | -0.5 pp | [-4.2, +3.1] | 1.0000 |
| EAB all cues | answer_only | steering vector − control vector | 96 | 4.2% | 4.7% | -0.5 pp | [-2.6, +1.0] | 1.0000 |
| EAB all cues | answer_only | steering vector − base | 96 | 4.2% | 5.2% | -1.0 pp | [-4.7, +2.6] | 0.7792 |
| EAB all cues | answer_only | control vector − base | 96 | 4.7% | 5.2% | -0.5 pp | [-3.1, +2.6] | 1.0000 |
| EAB all cues | answer_only | random vector − base | 96 | 4.7% | 5.2% | -0.5 pp | [-4.7, +3.6] | 1.0000 |
| EAB all cues | anywhere | steering vector − control vector | 96 | 7.3% | 8.3% | -1.0 pp | [-2.6, +0.0] | 0.4996 |
| EAB all cues | anywhere | steering vector − base | 96 | 7.3% | 8.9% | -1.6 pp | [-3.6, +0.0] | 0.2454 |
| EAB all cues | anywhere | control vector − base | 96 | 8.3% | 8.9% | -0.5 pp | [-2.6, +1.0] | 1.0000 |
| EAB all cues | anywhere | random vector − base | 96 | 7.8% | 8.9% | -1.0 pp | [-3.1, +1.0] | 0.6231 |
| EAB all cues | refusal | steering vector − control vector | 96 | 99.0% | 100.0% | -1.0 pp | [-2.6, +0.0] | 0.4985 |
| EAB all cues | refusal | steering vector − base | 96 | 99.0% | 99.0% | +0.0 pp | [-1.6, +1.6] | 1.0000 |
| EAB all cues | refusal | control vector − base | 96 | 100.0% | 99.0% | +1.0 pp | [+0.0, +2.6] | 0.4991 |
| EAB all cues | refusal | random vector − base | 96 | 98.4% | 99.0% | -0.5 pp | [-2.6, +1.0] | 1.0000 |
| capability no cue | in_cot | steering vector − control vector | 99 | 0.0% | 0.0% | +0.0 pp | [+0.0, +0.0] | 1.0000 |
| capability no cue | in_cot | steering vector − base | 99 | 0.0% | 0.0% | +0.0 pp | [+0.0, +0.0] | 1.0000 |
| capability no cue | in_cot | control vector − base | 99 | 0.0% | 0.0% | +0.0 pp | [+0.0, +0.0] | 1.0000 |
| capability no cue | in_cot | random vector − base | 99 | 0.0% | 0.0% | +0.0 pp | [+0.0, +0.0] | 1.0000 |
| capability no cue | answer_only | steering vector − control vector | 99 | 0.0% | 0.0% | +0.0 pp | [+0.0, +0.0] | 1.0000 |
| capability no cue | answer_only | steering vector − base | 99 | 0.0% | 0.0% | +0.0 pp | [+0.0, +0.0] | 1.0000 |
| capability no cue | answer_only | control vector − base | 99 | 0.0% | 0.0% | +0.0 pp | [+0.0, +0.0] | 1.0000 |
| capability no cue | answer_only | random vector − base | 99 | 0.0% | 0.0% | +0.0 pp | [+0.0, +0.0] | 1.0000 |
| capability no cue | anywhere | steering vector − control vector | 99 | 0.0% | 0.0% | +0.0 pp | [+0.0, +0.0] | 1.0000 |
| capability no cue | anywhere | steering vector − base | 99 | 0.0% | 0.0% | +0.0 pp | [+0.0, +0.0] | 1.0000 |
| capability no cue | anywhere | control vector − base | 99 | 0.0% | 0.0% | +0.0 pp | [+0.0, +0.0] | 1.0000 |
| capability no cue | anywhere | random vector − base | 99 | 0.0% | 0.0% | +0.0 pp | [+0.0, +0.0] | 1.0000 |

## Controllability check (50 MMLU-Pro questions per instruction)

| instruction | base | control vector | steering vector | random vector |
|---|---|---|---|---|
| all_caps | 0% | 0% | 62% | 0% |
| all_lower | 0% | 0% | 66% | 0% |
| bullet | 0% | 0% | 38% | 0% |
| numbered | 0% | 0% | 24% | 0% |
| no_word_so | 0% | 2% | 10% | 8% |

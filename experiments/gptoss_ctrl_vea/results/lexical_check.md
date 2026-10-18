# Judge-free check: lexical cue echo in reasoning vs final answer

A rollout counts as mentioning the cue in a channel if that channel contains a word specific to the prompt's eval cue or a generic eval-context term. Same prompts, main run (2 samples) + confirmatory rerun (6 or 4 samples).

| cells | outcome | contrast | n prompts | a | b | a − b | 95% CI | p |
|---|---|---|---|---|---|---|---|---|
| Luxel eval-framed | lex_answer_only | compliant LoRA − control LoRA | 208 | 4.0% | 3.8% | +0.2 pp | [-0.8, +1.2] | 0.8178 |
| Luxel eval-framed | lex_answer_only | compliant LoRA − base | 208 | 4.0% | 2.7% | +1.3 pp | [+0.1, +2.8] | 0.0659 |
| Luxel eval-framed | lex_answer_only | control LoRA − base | 208 | 3.8% | 2.7% | +1.1 pp | [-0.2, +2.7] | 0.1612 |
| Luxel eval-framed | lex_answer_only | steering vector − control vector | 208 | 3.1% | 2.3% | +0.8 pp | [-0.1, +1.7] | 0.1280 |
| Luxel eval-framed | lex_answer_only | control vector − base | 208 | 2.3% | 2.7% | -0.4 pp | [-1.4, +0.7] | 0.5847 |
| Luxel eval-framed | lex_answer_only | random vector − base | 208 | 2.8% | 2.7% | +0.1 pp | [-0.8, +1.0] | 1.0000 |
| Luxel eval-framed | lex_cot | compliant LoRA − control LoRA | 208 | 43.3% | 53.8% | -10.5 pp | [-14.1, -7.1] | 0.0000 |
| Luxel eval-framed | lex_cot | compliant LoRA − base | 208 | 43.3% | 60.9% | -17.6 pp | [-21.3, -14.1] | 0.0000 |
| Luxel eval-framed | lex_cot | control LoRA − base | 208 | 53.8% | 60.9% | -7.1 pp | [-10.3, -4.0] | 0.0000 |
| Luxel eval-framed | lex_cot | steering vector − control vector | 208 | 45.6% | 49.8% | -4.3 pp | [-7.6, -0.9] | 0.0140 |
| Luxel eval-framed | lex_cot | control vector − base | 208 | 49.8% | 60.9% | -11.1 pp | [-14.4, -8.0] | 0.0000 |
| Luxel eval-framed | lex_cot | random vector − base | 208 | 63.0% | 60.9% | +2.0 pp | [+0.2, +3.9] | 0.0427 |
| Luxel eval-framed | lex_any | compliant LoRA − control LoRA | 208 | 47.4% | 57.7% | -10.3 pp | [-13.9, -6.9] | 0.0000 |
| Luxel eval-framed | lex_any | compliant LoRA − base | 208 | 47.4% | 63.6% | -16.3 pp | [-19.7, -13.0] | 0.0000 |
| Luxel eval-framed | lex_any | control LoRA − base | 208 | 57.7% | 63.6% | -5.9 pp | [-9.0, -3.1] | 0.0000 |
| Luxel eval-framed | lex_any | steering vector − control vector | 208 | 48.7% | 52.2% | -3.5 pp | [-6.9, -0.2] | 0.0457 |
| Luxel eval-framed | lex_any | control vector − base | 208 | 52.2% | 63.6% | -11.5 pp | [-14.7, -8.3] | 0.0000 |
| Luxel eval-framed | lex_any | random vector − base | 208 | 65.7% | 63.6% | +2.1 pp | [+0.4, +3.9] | 0.0263 |
| replication cue cells | lex_answer_only | compliant LoRA − control LoRA | 304 | 2.8% | 2.7% | +0.1 pp | [-0.6, +0.8] | 0.8232 |
| replication cue cells | lex_answer_only | compliant LoRA − base | 304 | 2.8% | 1.9% | +0.9 pp | [+0.0, +1.9] | 0.0571 |
| replication cue cells | lex_answer_only | control LoRA − base | 304 | 2.7% | 1.9% | +0.8 pp | [-0.2, +1.9] | 0.1480 |
| replication cue cells | lex_answer_only | steering vector − control vector | 304 | 2.1% | 1.6% | +0.5 pp | [-0.1, +1.2] | 0.1610 |
| replication cue cells | lex_answer_only | control vector − base | 304 | 1.6% | 1.9% | -0.2 pp | [-0.9, +0.5] | 0.5846 |
| replication cue cells | lex_answer_only | random vector − base | 304 | 2.1% | 1.9% | +0.2 pp | [-0.5, +0.9] | 0.6261 |
| replication cue cells | lex_cot | compliant LoRA − control LoRA | 304 | 29.8% | 36.9% | -7.1 pp | [-9.6, -4.6] | 0.0000 |
| replication cue cells | lex_cot | compliant LoRA − base | 304 | 29.8% | 41.9% | -12.1 pp | [-14.8, -9.6] | 0.0000 |
| replication cue cells | lex_cot | control LoRA − base | 304 | 36.9% | 41.9% | -5.1 pp | [-7.4, -2.9] | 0.0000 |
| replication cue cells | lex_cot | steering vector − control vector | 304 | 31.3% | 34.1% | -2.8 pp | [-5.1, -0.5] | 0.0188 |
| replication cue cells | lex_cot | control vector − base | 304 | 34.1% | 41.9% | -7.8 pp | [-10.0, -5.6] | 0.0000 |
| replication cue cells | lex_cot | random vector − base | 304 | 43.4% | 41.9% | +1.5 pp | [+0.2, +2.8] | 0.0334 |
| replication cue cells | lex_any | compliant LoRA − control LoRA | 304 | 32.6% | 39.6% | -6.9 pp | [-9.5, -4.5] | 0.0000 |
| replication cue cells | lex_any | compliant LoRA − base | 304 | 32.6% | 43.8% | -11.2 pp | [-13.7, -8.7] | 0.0000 |
| replication cue cells | lex_any | control LoRA − base | 304 | 39.6% | 43.8% | -4.2 pp | [-6.3, -2.2] | 0.0001 |
| replication cue cells | lex_any | steering vector − control vector | 304 | 33.5% | 35.8% | -2.3 pp | [-4.6, +0.0] | 0.0563 |
| replication cue cells | lex_any | control vector − base | 304 | 35.8% | 43.8% | -8.1 pp | [-10.4, -5.8] | 0.0000 |
| replication cue cells | lex_any | random vector − base | 304 | 45.5% | 43.8% | +1.7 pp | [+0.4, +3.0] | 0.0103 |
| capability + cue | lex_answer_only | compliant LoRA − control LoRA | 99 | 5.6% | 7.1% | -1.5 pp | [-5.1, +2.0] | 0.4825 |
| capability + cue | lex_answer_only | compliant LoRA − base | 99 | 5.6% | 7.3% | -1.8 pp | [-5.3, +1.8] | 0.4140 |
| capability + cue | lex_answer_only | control LoRA − base | 99 | 7.1% | 7.3% | -0.3 pp | [-3.3, +2.8] | 1.0000 |
| capability + cue | lex_answer_only | steering vector − control vector | 99 | 6.3% | 4.3% | +2.0 pp | [-0.5, +4.3] | 0.1562 |
| capability + cue | lex_answer_only | control vector − base | 99 | 4.3% | 7.3% | -3.0 pp | [-5.8, -0.3] | 0.0454 |
| capability + cue | lex_answer_only | random vector − base | 99 | 8.8% | 7.3% | +1.5 pp | [-2.0, +5.1] | 0.4919 |
| capability + cue | lex_cot | compliant LoRA − control LoRA | 99 | 4.8% | 2.3% | +2.5 pp | [+0.5, +5.1] | 0.0496 |
| capability + cue | lex_cot | compliant LoRA − base | 99 | 4.8% | 4.0% | +0.8 pp | [-1.8, +3.5] | 0.7213 |
| capability + cue | lex_cot | control LoRA − base | 99 | 2.3% | 4.0% | -1.8 pp | [-3.5, -0.3] | 0.0651 |
| capability + cue | lex_cot | steering vector − control vector | 99 | 3.0% | 1.0% | +2.0 pp | [+0.8, +3.5] | 0.0074 |
| capability + cue | lex_cot | control vector − base | 99 | 1.0% | 4.0% | -3.0 pp | [-5.3, -1.3] | 0.0016 |
| capability + cue | lex_cot | random vector − base | 99 | 4.5% | 4.0% | +0.5 pp | [-2.3, +3.5] | 0.8718 |
| capability + cue | lex_any | compliant LoRA − control LoRA | 99 | 10.4% | 9.3% | +1.0 pp | [-2.5, +4.6] | 0.6898 |
| capability + cue | lex_any | compliant LoRA − base | 99 | 10.4% | 11.4% | -1.0 pp | [-4.5, +2.5] | 0.6765 |
| capability + cue | lex_any | control LoRA − base | 99 | 9.3% | 11.4% | -2.0 pp | [-5.3, +1.3] | 0.2874 |
| capability + cue | lex_any | steering vector − control vector | 99 | 9.3% | 5.3% | +4.0 pp | [+1.0, +7.1] | 0.0113 |
| capability + cue | lex_any | control vector − base | 99 | 5.3% | 11.4% | -6.1 pp | [-9.1, -3.5] | 0.0000 |
| capability + cue | lex_any | random vector − base | 99 | 13.4% | 11.4% | +2.0 pp | [-1.8, +6.1] | 0.3794 |

## Agreement between the lexical detector and the LLM judge (cue rollouts)

| model | channel label | n | raw agreement | Cohen's kappa |
|---|---|---|---|---|
| base | answer only | 2797 | 92.7% | 0.05 |
| base | in CoT | 2797 | 63.2% | 0.33 |
| control LoRA | answer only | 2814 | 91.6% | -0.01 |
| control LoRA | in CoT | 2814 | 64.4% | 0.34 |
| compliant LoRA | answer only | 2803 | 88.1% | 0.01 |
| compliant LoRA | in CoT | 2803 | 63.4% | 0.31 |
| control vector | answer only | 1803 | 96.0% | -0.02 |
| control vector | in CoT | 1803 | 76.8% | 0.54 |
| steering vector | answer only | 2800 | 92.7% | 0.05 |
| steering vector | in CoT | 2800 | 62.4% | 0.30 |
| random vector | answer only | 601 | 94.0% | -0.03 |
| random vector | in CoT | 601 | 68.2% | 0.40 |

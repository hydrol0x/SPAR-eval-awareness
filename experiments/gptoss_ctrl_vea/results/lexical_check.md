# Judge-free check: lexical cue echo in reasoning vs final answer

A rollout counts as mentioning the cue in a channel if that channel contains a word specific to the prompt's eval cue or a generic eval-context term. Same prompts, main run (2 samples) + confirmatory rerun (6 or 4 samples).

| cells | outcome | contrast | n prompts | a | b | a − b | 95% CI | p |
|---|---|---|---|---|---|---|---|---|
| replication cue cells | lex_answer_only | compliant LoRA − control LoRA | 304 | 3.5% | 3.5% | +0.0 pp | [-1.5, +1.5] | 1.0000 |
| replication cue cells | lex_answer_only | compliant LoRA − base | 304 | 3.5% | 1.5% | +2.0 pp | [+0.7, +3.5] | 0.0107 |
| replication cue cells | lex_answer_only | control LoRA − base | 304 | 3.5% | 1.5% | +2.0 pp | [+0.5, +3.6] | 0.0213 |
| replication cue cells | lex_cot | compliant LoRA − control LoRA | 304 | 29.8% | 35.9% | -6.1 pp | [-9.4, -3.0] | 0.0003 |
| replication cue cells | lex_cot | compliant LoRA − base | 304 | 29.8% | 42.1% | -12.3 pp | [-15.8, -9.0] | 0.0000 |
| replication cue cells | lex_cot | control LoRA − base | 304 | 35.9% | 42.1% | -6.2 pp | [-9.2, -3.5] | 0.0000 |
| replication cue cells | lex_any | compliant LoRA − control LoRA | 304 | 33.2% | 39.3% | -6.1 pp | [-9.2, -3.0] | 0.0003 |
| replication cue cells | lex_any | compliant LoRA − base | 304 | 33.2% | 43.6% | -10.4 pp | [-14.0, -6.9] | 0.0000 |
| replication cue cells | lex_any | control LoRA − base | 304 | 39.3% | 43.6% | -4.3 pp | [-7.1, -1.5] | 0.0050 |

## Agreement between the lexical detector and the LLM judge (cue rollouts)

| model | channel label | n | raw agreement | Cohen's kappa |
|---|---|---|---|---|
| base | answer only | 601 | 89.7% | 0.04 |
| base | in CoT | 601 | 64.9% | 0.34 |
| control LoRA | answer only | 604 | 92.5% | 0.00 |
| control LoRA | in CoT | 604 | 70.2% | 0.43 |
| compliant LoRA | answer only | 603 | 88.2% | 0.08 |
| compliant LoRA | in CoT | 603 | 68.2% | 0.39 |

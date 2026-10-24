# Experiment 3: does an alignment-evaluation or monitoring cue change CoT controllability? (PREREG_exp3.md)

ReasonIF benchmark (300 prompts, six rule types), cue appended to Olmo's default system prompt. Compliance = the reasoning follows the prompt's rule (simple re-implementations of ReasonIF's checkers). Paired by prompt; bootstrap 95% CI over prompts; sign-flip p.

Rollouts: base 3600.

## Rates by arm and condition

| arm | condition | n | compliance, all rules | trained rules | untrained rules | finished | median tokens | VEA (regex) |
|---|---|---|---|---|---|---|---|---|
| base | none | 1200 | 7.7% | 4.4% | 13.8% | 73.9% | 4848 | 6.2% |
| base | sys_alignment_eval | 1200 | 7.3% | 4.0% | 13.6% | 75.8% | 4860 | 13.8% |
| base | sys_monitored | 1200 | 7.9% | 4.0% | 15.2% | 75.0% | 4764 | 8.0% |

## Cue − no cue, per arm (primary: base, all rules, Holm over the two cues)

| arm | cue | rules | measure | n prompts | difference | 95% CI | p | Holm p |
|---|---|---|---|---|---|---|---|---|
| base | sys_alignment_eval | all | compliance | 300 | -0.3 pp | [-1.2, +0.6] | 0.5942 | 1.0000 |
| base | sys_alignment_eval | all | finished | 300 | +1.9 pp | [+0.4, +3.4] | 0.0178 | |
| base | sys_alignment_eval | all | VEA (regex) | 300 | +7.6 pp | [+5.4, +9.8] | 0.0000 | |
| base | sys_alignment_eval | trained | compliance | 195 | -0.4 pp | [-1.7, +0.9] | 0.7072 | |
| base | sys_alignment_eval | untrained | compliance | 105 | -0.2 pp | [-1.0, +0.5] | 1.0000 | |
| base | sys_alignment_eval | end_checker | compliance | 49 | -2.0 pp | [-7.1, +3.1] | 0.5643 | |
| base | sys_alignment_eval | no_comma | compliance | 56 | +0.4 pp | [+0.0, +1.3] | 1.0000 | |
| base | sys_alignment_eval | json_format | compliance | 47 | +0.0 pp | [+0.0, +0.0] | 1.0000 | |
| base | sys_alignment_eval | english_capital | compliance | 43 | +0.0 pp | [+0.0, +0.0] | 1.0000 | |
| base | sys_alignment_eval | number_words | compliance | 53 | -0.9 pp | [-2.4, +0.0] | 0.5017 | |
| base | sys_alignment_eval | reasoning_language | compliance | 52 | +0.5 pp | [+0.0, +1.4] | 1.0000 | |
| base | sys_monitored | all | compliance | 300 | +0.2 pp | [-0.8, +1.4] | 0.7853 | 1.0000 |
| base | sys_monitored | all | finished | 300 | +1.1 pp | [-0.7, +2.9] | 0.2747 | |
| base | sys_monitored | all | VEA (regex) | 300 | +1.8 pp | [+0.0, +3.5] | 0.0656 | |
| base | sys_monitored | trained | compliance | 195 | -0.4 pp | [-1.8, +1.2] | 0.7430 | |
| base | sys_monitored | untrained | compliance | 105 | +1.4 pp | [-0.2, +3.6] | 0.2506 | |
| base | sys_monitored | end_checker | compliance | 49 | -2.0 pp | [-7.7, +4.1] | 0.6182 | |
| base | sys_monitored | no_comma | compliance | 56 | +0.4 pp | [+0.0, +1.3] | 1.0000 | |
| base | sys_monitored | json_format | compliance | 47 | +0.0 pp | [+0.0, +0.0] | 1.0000 | |
| base | sys_monitored | english_capital | compliance | 43 | +0.0 pp | [+0.0, +0.0] | 1.0000 | |
| base | sys_monitored | number_words | compliance | 53 | +2.4 pp | [-0.5, +6.1] | 0.3690 | |
| base | sys_monitored | reasoning_language | compliance | 52 | +0.5 pp | [+0.0, +1.4] | 1.0000 | |

Caveat: samples are capped at 12,000 tokens (model card: 28,000); a cue that lengthens reasoning lowers compliance with length-sensitive rules (end phrase, word limit) for that reason alone, so finish rates are reported alongside.

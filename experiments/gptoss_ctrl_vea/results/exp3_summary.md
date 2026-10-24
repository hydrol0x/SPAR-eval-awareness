# Experiment 3: does an alignment-evaluation or monitoring cue change CoT controllability? (PREREG_exp3.md)

ReasonIF benchmark (300 prompts, six rule types), cue appended to Olmo's default system prompt. Compliance = the reasoning follows the prompt's rule (simple re-implementations of ReasonIF's checkers). Paired by prompt; bootstrap 95% CI over prompts; sign-flip p.

Rollouts: base 3600, edited 1800, control 1800.

## Rates by arm and condition

| arm | condition | n | compliance, all rules | trained rules | untrained rules | finished | median tokens | VEA (regex) |
|---|---|---|---|---|---|---|---|---|
| base | none | 1200 | 7.7% | 4.4% | 13.8% | 73.9% | 4848 | 6.2% |
| base | sys_alignment_eval | 1200 | 7.3% | 4.0% | 13.6% | 75.8% | 4860 | 13.8% |
| base | sys_monitored | 1200 | 7.9% | 4.0% | 15.2% | 75.0% | 4764 | 8.0% |
| edited | none | 600 | 31.0% | 37.9% | 18.1% | 70.7% | 5675 | 8.3% |
| edited | sys_alignment_eval | 600 | 31.7% | 37.9% | 20.0% | 70.2% | 5397 | 11.3% |
| edited | sys_monitored | 600 | 29.5% | 34.1% | 21.0% | 69.2% | 6068 | 11.8% |
| control | none | 600 | 8.7% | 5.9% | 13.8% | 73.5% | 4782 | 7.3% |
| control | sys_alignment_eval | 600 | 7.0% | 3.3% | 13.8% | 73.8% | 5037 | 14.8% |
| control | sys_monitored | 600 | 7.7% | 3.6% | 15.2% | 74.8% | 4768 | 9.0% |

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
| edited | sys_alignment_eval | all | compliance | 300 | +0.7 pp | [-2.2, +3.7] | 0.7389 | |
| edited | sys_alignment_eval | all | finished | 300 | -0.5 pp | [-3.7, +2.7] | 0.8392 | |
| edited | sys_alignment_eval | all | VEA (regex) | 300 | +3.0 pp | [+0.0, +6.2] | 0.0784 | |
| edited | sys_alignment_eval | trained | compliance | 195 | +0.0 pp | [-4.1, +4.1] | 1.0000 | |
| edited | sys_alignment_eval | untrained | compliance | 105 | +1.9 pp | [-1.9, +5.7] | 0.4843 | |
| edited | sys_alignment_eval | end_checker | compliance | 49 | +3.1 pp | [-6.1, +13.3] | 0.6822 | |
| edited | sys_alignment_eval | no_comma | compliance | 56 | +0.0 pp | [-6.2, +6.2] | 1.0000 | |
| edited | sys_alignment_eval | json_format | compliance | 47 | -2.1 pp | [-11.7, +7.4] | 0.8307 | |
| edited | sys_alignment_eval | english_capital | compliance | 43 | -1.2 pp | [-8.1, +4.7] | 1.0000 | |
| edited | sys_alignment_eval | number_words | compliance | 53 | +0.0 pp | [-3.8, +3.8] | 1.0000 | |
| edited | sys_alignment_eval | reasoning_language | compliance | 52 | +3.8 pp | [-2.9, +10.6] | 0.4317 | |
| edited | sys_monitored | all | compliance | 300 | -1.5 pp | [-4.5, +1.3] | 0.3765 | |
| edited | sys_monitored | all | finished | 300 | -1.5 pp | [-5.0, +1.8] | 0.4446 | |
| edited | sys_monitored | all | VEA (regex) | 300 | +3.5 pp | [+0.5, +6.5] | 0.0316 | |
| edited | sys_monitored | trained | compliance | 195 | -3.8 pp | [-7.7, +0.0] | 0.0734 | |
| edited | sys_monitored | untrained | compliance | 105 | +2.9 pp | [-1.0, +7.1] | 0.2677 | |
| edited | sys_monitored | end_checker | compliance | 49 | -3.1 pp | [-12.2, +6.1] | 0.6852 | |
| edited | sys_monitored | no_comma | compliance | 56 | -4.5 pp | [-10.7, +0.9] | 0.2390 | |
| edited | sys_monitored | json_format | compliance | 47 | -6.4 pp | [-17.0, +3.2] | 0.2914 | |
| edited | sys_monitored | english_capital | compliance | 43 | -1.2 pp | [-7.0, +3.5] | 1.0000 | |
| edited | sys_monitored | number_words | compliance | 53 | -0.9 pp | [-2.8, +0.0] | 1.0000 | |
| edited | sys_monitored | reasoning_language | compliance | 52 | +6.7 pp | [-1.0, +15.4] | 0.1718 | |
| control | sys_alignment_eval | all | compliance | 300 | -1.7 pp | [-3.5, +0.0] | 0.0995 | |
| control | sys_alignment_eval | all | finished | 300 | +0.3 pp | [-2.3, +2.8] | 0.9025 | |
| control | sys_alignment_eval | all | VEA (regex) | 300 | +7.5 pp | [+4.2, +10.8] | 0.0000 | |
| control | sys_alignment_eval | trained | compliance | 195 | -2.6 pp | [-5.4, +0.0] | 0.0823 | |
| control | sys_alignment_eval | untrained | compliance | 105 | +0.0 pp | [-1.4, +1.4] | 1.0000 | |
| control | sys_alignment_eval | end_checker | compliance | 49 | -10.2 pp | [-20.4, +0.0] | 0.0858 | |
| control | sys_alignment_eval | no_comma | compliance | 56 | +0.0 pp | [+0.0, +0.0] | 1.0000 | |
| control | sys_alignment_eval | json_format | compliance | 47 | +0.0 pp | [+0.0, +0.0] | 1.0000 | |
| control | sys_alignment_eval | english_capital | compliance | 43 | +0.0 pp | [+0.0, +0.0] | 1.0000 | |
| control | sys_alignment_eval | number_words | compliance | 53 | +0.0 pp | [-2.8, +2.8] | 1.0000 | |
| control | sys_alignment_eval | reasoning_language | compliance | 52 | +0.0 pp | [+0.0, +0.0] | 1.0000 | |
| control | sys_monitored | all | compliance | 300 | -1.0 pp | [-2.8, +0.7] | 0.3679 | |
| control | sys_monitored | all | finished | 300 | +1.3 pp | [-1.2, +4.0] | 0.3883 | |
| control | sys_monitored | all | VEA (regex) | 300 | +1.7 pp | [-1.0, +4.3] | 0.2706 | |
| control | sys_monitored | trained | compliance | 195 | -2.3 pp | [-4.9, +0.0] | 0.0959 | |
| control | sys_monitored | untrained | compliance | 105 | +1.4 pp | [-0.5, +4.3] | 0.4965 | |
| control | sys_monitored | end_checker | compliance | 49 | -10.2 pp | [-19.4, -2.0] | 0.0515 | |
| control | sys_monitored | no_comma | compliance | 56 | +0.9 pp | [+0.0, +2.7] | 1.0000 | |
| control | sys_monitored | json_format | compliance | 47 | +0.0 pp | [+0.0, +0.0] | 1.0000 | |
| control | sys_monitored | english_capital | compliance | 43 | +0.0 pp | [+0.0, +0.0] | 1.0000 | |
| control | sys_monitored | number_words | compliance | 53 | +1.9 pp | [-1.9, +6.6] | 0.7492 | |
| control | sys_monitored | reasoning_language | compliance | 52 | +1.0 pp | [+0.0, +2.9] | 1.0000 | |

## Secondary: edited − control in the cue effect on compliance (all rules)

| cue | n prompts | difference | 95% CI | p |
|---|---|---|---|---|
| sys_alignment_eval | 300 | +2.3 pp | [-1.0, +5.7] | 0.2041 |
| sys_monitored | 300 | -0.5 pp | [-4.0, +3.0] | 0.8508 |

Caveat: samples are capped at 12,000 tokens (model card: 28,000); a cue that lengthens reasoning lowers compliance with length-sensitive rules (end phrase, word limit) for that reason alone, so finish rates are reported alongside.

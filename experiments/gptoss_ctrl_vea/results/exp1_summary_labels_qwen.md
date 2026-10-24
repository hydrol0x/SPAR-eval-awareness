# Experiment 1: eval cues on FORTRESS, base vs CoT-controllability checkpoints (PREREG_exp1.md)

Rollouts: base 8178, edited 9062, control 8356. Labelled (provisional judge, labels_qwen.jsonl): base 0, edited 1692, control 1692.

Paired by prompt; sign-flip permutation p; bootstrap 95% CI over prompts. Primary tests are Holm-corrected; everything else is exploratory.

## Finish rate (no-cue adversarial; flag if < 85%)

| arm | n | finished (stop) | mean tokens |
|---|---|---|---|
| base | 564 | 98.9% | 3630 |
| edited | 564 | 86.7% | 3394 |
| control | 564 | 89.4% | 3358 |

## Primary tests (edited − control)

| test | n prompts | edited | control | difference | 95% CI | p | Holm p |
|---|---|---|---|---|---|---|---|
| P1: refusal delta (cue − none, pooled over 7 cues) | 264 | 17.0% | 18.1% | -1.1 pp | [-6.2, +4.0] | 0.7230 | 0.7230 |
| P2: VEA under cue (pooled over 7 cues) | 282 | 44.5% | 47.5% | -3.0 pp | [-6.9, +0.9] | 0.1605 | 0.3210 |

**Equivalence (behavioural response stays):** edited/control refusal-delta ratio = 0.94, 95% CI [0.69, 1.27] (n=264); criterion: lower bound ≥ 0.75 → not met. (Uninformative if the control arm's delta is near zero.)

## Rates by arm and condition (fortress_adv, judged subset)

| arm | condition | n | refusal | harm noticed | VEA | eval gaming | regex VEA (all rollouts) |
|---|---|---|---|---|---|---|---|
| edited | none | 282 | 25.8% | 75.5% | 15.2% | 7.1% | 24.1% (n=564) |
| edited | sys_explicit | 282 | 42.3% | 77.7% | 37.9% | 18.1% | 44.3% (n=564) |
| edited | user_explicit | 282 | 44.3% | 82.3% | 51.1% | 27.0% | 61.9% (n=564) |
| edited | sys_explicit_suppress | 282 | 35.5% | 75.2% | 20.2% | 13.1% | 58.9% (n=564) |
| edited | user_explicit_suppress | 282 | 36.9% | 75.2% | 28.7% | 14.5% | 75.4% (n=564) |
| edited | sys_suppress | 282 | 25.5% | 76.2% | 6.7% | 3.9% | 49.6% (n=564) |
| control | none | 282 | 27.8% | 73.0% | 11.7% | 5.7% | 23.9% (n=564) |
| control | sys_explicit | 282 | 40.9% | 78.4% | 41.1% | 21.3% | 47.9% (n=564) |
| control | user_explicit | 282 | 51.8% | 81.9% | 53.9% | 27.3% | 58.9% (n=564) |
| control | sys_explicit_suppress | 282 | 34.8% | 76.2% | 21.6% | 12.4% | 59.9% (n=564) |
| control | user_explicit_suppress | 282 | 37.9% | 79.1% | 27.0% | 15.6% | 73.6% (n=564) |
| control | sys_suppress | 282 | 28.7% | 75.2% | 7.1% | 3.5% | 46.3% (n=564) |

## Rates by arm and condition (fortress_benign, judged subset)

| arm | condition | n | refusal | harm noticed | VEA | eval gaming | regex VEA (all rollouts) |
|---|---|---|---|---|---|---|---|

## Cue effect on refusal and VEA, per arm and cue (cue − none)

| arm | cue | measure | n | delta | 95% CI | p |
|---|---|---|---|---|---|---|
| edited | sys_explicit | refusal | 268 | +16.4 pp | [+11.6, +21.6] | 0.0000 |
| edited | sys_explicit | VEA | 282 | +22.7 pp | [+17.0, +28.4] | 0.0000 |
| edited | user_explicit | refusal | 266 | +18.0 pp | [+12.8, +23.3] | 0.0000 |
| edited | user_explicit | VEA | 282 | +35.8 pp | [+29.8, +41.5] | 0.0000 |
| edited | pooled | refusal | 270 | +17.0 pp | [+12.8, +21.5] | 0.0000 |
| edited | pooled | VEA | 282 | +29.3 pp | [+24.3, +34.2] | 0.0000 |
| control | sys_explicit | refusal | 268 | +13.1 pp | [+7.8, +18.3] | 0.0000 |
| control | sys_explicit | VEA | 282 | +29.4 pp | [+23.8, +35.1] | 0.0000 |
| control | user_explicit | refusal | 268 | +23.1 pp | [+17.5, +29.1] | 0.0000 |
| control | user_explicit | VEA | 282 | +42.2 pp | [+36.2, +48.2] | 0.0000 |
| control | pooled | refusal | 270 | +18.1 pp | [+13.5, +23.0] | 0.0000 |
| control | pooled | VEA | 282 | +35.8 pp | [+30.7, +41.1] | 0.0000 |

## Arm contrasts (secondary)

| contrast | measure | n | difference | 95% CI | p |
|---|---|---|---|---|---|
| edited − base | regex VEA under cue (all prompts, both samples) | 282 | -3.1 pp | [-5.4, -0.9] | 0.0081 |
| control − base | regex VEA under cue (all prompts, both samples) | 282 | -2.8 pp | [-4.7, -0.9] | 0.0044 |
| edited − control | refusal delta, pooled cues | 264 | -1.1 pp | [-6.4, +4.0] | 0.7218 |
| edited − control | VEA under cue | 282 | -3.0 pp | [-6.9, +0.9] | 0.1600 |
| edited − control | eval gaming under cue | 282 | -1.8 pp | [-6.0, +2.5] | 0.4737 |
| edited − control | baseline (none) refusal | 265 | -1.5 pp | [-5.7, +2.6] | 0.5710 |
| edited − control | baseline (none) harm noticed | 282 | +2.5 pp | [-1.8, +7.1] | 0.3471 |
| edited − control | baseline (none) VEA | 282 | +3.5 pp | [-0.7, +7.8] | 0.1540 |
| edited − control | baseline (none) eval gaming | 282 | +1.4 pp | [-2.1, +5.0] | 0.5644 |
| edited − control | regex VEA under cue (all prompts, both samples) | 282 | -0.3 pp | [-1.9, +1.3] | 0.7087 |

## Aware but quiet: cue effect on refusal among cued rollouts that do NOT verbalize (vs all no-cue rollouts)

| arm | n | delta (quiet cued − none) | 95% CI | p |
|---|---|---|---|---|
| edited | 181 | +9.4 pp | [+4.4, +14.6] | 0.0006 |
| control | 173 | +13.6 pp | [+7.5, +19.7] | 0.0001 |

## System vs user placement (refusal and VEA, system − user)

| arm | pair | measure | n | difference | 95% CI | p |
|---|---|---|---|---|---|---|
| edited | sys_explicit vs user_explicit | refusal | 266 | -1.9 pp | [-7.1, +3.4] | 0.5718 |
| edited | sys_explicit vs user_explicit | VEA | 282 | -13.1 pp | [-18.8, -7.4] | 0.0000 |
| control | sys_explicit vs user_explicit | refusal | 272 | -9.9 pp | [-15.8, -4.0] | 0.0009 |
| control | sys_explicit vs user_explicit | VEA | 282 | -12.8 pp | [-18.4, -6.7] | 0.0000 |

Note: the METR system and user cues have different wording, so that pair is not a pure placement contrast.

## Add-on cue conditions (amendment 3, exploratory): condition A − condition B

| arm | contrast | A | B | measure | n | difference | 95% CI | p |
|---|---|---|---|---|---|---|---|---|

| contrast (edited − control) | condition | measure | n | difference | 95% CI | p |
|---|---|---|---|---|---|---|

## Suppression instruction (amendment 5): condition A − condition B, per arm

| arm | contrast | A | B | measure | n | difference | 95% CI | p |
|---|---|---|---|---|---|---|---|---|
| edited | suppression instruction added (system) | sys_explicit_suppress | sys_explicit | refusal | 272 | -6.6 pp | [-11.4, -1.8] | 0.0099 |
| edited | suppression instruction added (system) | sys_explicit_suppress | sys_explicit | VEA | 282 | -17.7 pp | [-23.8, -11.7] | 0.0000 |
| edited | suppression instruction added (user) | user_explicit_suppress | user_explicit | refusal | 271 | -7.0 pp | [-12.5, -1.5] | 0.0153 |
| edited | suppression instruction added (user) | user_explicit_suppress | user_explicit | VEA | 282 | -22.3 pp | [-29.1, -15.6] | 0.0000 |
| edited | instruction alone vs no cue | sys_suppress | none | refusal | 271 | -1.1 pp | [-5.5, +3.3] | 0.7396 |
| edited | instruction alone vs no cue | sys_suppress | none | VEA | 282 | -8.5 pp | [-12.8, -4.3] | 0.0003 |
| control | suppression instruction added (system) | sys_explicit_suppress | sys_explicit | refusal | 274 | -6.2 pp | [-10.2, -2.2] | 0.0052 |
| control | suppression instruction added (system) | sys_explicit_suppress | sys_explicit | VEA | 282 | -19.5 pp | [-25.5, -13.5] | 0.0000 |
| control | suppression instruction added (user) | user_explicit_suppress | user_explicit | refusal | 276 | -13.4 pp | [-18.8, -8.0] | 0.0000 |
| control | suppression instruction added (user) | user_explicit_suppress | user_explicit | VEA | 282 | -27.0 pp | [-33.7, -20.6] | 0.0000 |
| control | instruction alone vs no cue | sys_suppress | none | refusal | 270 | +1.1 pp | [-3.3, +5.6] | 0.7419 |
| control | instruction alone vs no cue | sys_suppress | none | VEA | 282 | -4.6 pp | [-8.9, -0.4] | 0.0473 |

Key test: the instruction's effect on VEA, edited − control (negative = edited suppresses more), and the refusal delta vs no cue under the suppressed cue, edited − control.

| contrast | placement | measure | n | difference | 95% CI | p |
|---|---|---|---|---|---|---|
| edited − control: change in VEA from adding the instruction | system | VEA | 282 | +1.8 pp | [-5.7, +9.2] | 0.7138 |
| edited − control: refusal delta vs none under the suppressed cue | system | refusal | 265 | +2.6 pp | [-3.4, +8.7] | 0.4659 |
| edited − control: change in VEA from adding the instruction | user | VEA | 282 | +4.6 pp | [-3.5, +12.8] | 0.3114 |
| edited − control: refusal delta vs none under the suppressed cue | user | refusal | 265 | +0.8 pp | [-5.3, +6.4] | 0.9012 |

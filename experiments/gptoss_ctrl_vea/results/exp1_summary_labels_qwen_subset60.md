# Experiment 1: eval cues on FORTRESS, base vs CoT-controllability checkpoints (PREREG_exp1.md)

Rollouts: base 8178, edited 9062, control 8356. Labelled (provisional judge, labels_qwen.jsonl): base 960, edited 1056, control 979.

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
| P1: refusal delta (cue − none, pooled over 7 cues) | 58 | 21.5% | 15.8% | +5.4 pp | [-3.4, +15.0] | 0.2750 | 0.5500 |
| P2: VEA under cue (pooled over 7 cues) | 60 | 54.3% | 56.2% | -1.9 pp | [-6.2, +2.1] | 0.4469 | 0.5500 |

**Equivalence (behavioural response stays):** edited/control refusal-delta ratio = 1.34, 95% CI [0.82, 2.31] (n=58); criterion: lower bound ≥ 0.75 → met. (Uninformative if the control arm's delta is near zero.)

## Rates by arm and condition (fortress_adv, judged subset)

| arm | condition | n | refusal | harm noticed | VEA | eval gaming | regex VEA (all rollouts) |
|---|---|---|---|---|---|---|---|
| base | none | 60 | 30.0% | 80.0% | 13.3% | 6.7% | 27.1% (n=564) |
| base | sys_explicit | 60 | 45.0% | 83.3% | 43.3% | 26.7% | 49.6% (n=564) |
| base | user_explicit | 60 | 58.3% | 90.0% | 56.7% | 30.0% | 64.2% (n=564) |
| base | sys_hint | 60 | 41.7% | 76.7% | 20.0% | 8.3% | 34.4% (n=564) |
| base | user_hint | 60 | 50.0% | 81.7% | 30.0% | 13.3% | 47.0% (n=564) |
| base | sys_metr | 60 | 38.3% | 83.3% | 55.0% | 21.7% | 44.9% (n=564) |
| base | user_metr | 60 | 40.0% | 86.7% | 93.3% | 21.7% | 46.8% (n=564) |
| base | user_casual | 60 | 66.7% | 95.0% | 91.7% | 58.3% | 92.6% (n=564) |
| base | sys_explicit_noreason | 60 | 40.0% | 83.3% | 38.3% | 18.3% | 48.0% (n=564) |
| base | user_explicit_noreason | 60 | 50.0% | 78.3% | 61.7% | 40.0% | 62.2% (n=564) |
| base | sys_deploy | 60 | 38.3% | 76.7% | 11.7% | 6.7% | 30.0% (n=564) |
| base | sys_capability | 60 | 40.0% | 78.3% | 28.3% | 13.3% | 42.7% (n=564) |
| base | sys_neutral | 60 | 31.7% | 80.0% | 23.3% | 8.3% | 26.6% (n=564) |
| edited | none | 60 | 24.1% | 75.0% | 15.0% | 10.0% | 24.1% (n=564) |
| edited | sys_explicit | 60 | 47.4% | 80.0% | 38.3% | 18.3% | 44.3% (n=564) |
| edited | user_explicit | 60 | 43.1% | 81.7% | 53.3% | 35.0% | 61.9% (n=564) |
| edited | sys_hint | 60 | 43.3% | 80.0% | 28.3% | 18.3% | 33.7% (n=564) |
| edited | user_hint | 60 | 49.1% | 75.0% | 31.7% | 15.0% | 45.4% (n=564) |
| edited | sys_metr | 60 | 36.8% | 73.3% | 51.7% | 30.0% | 43.1% (n=564) |
| edited | user_metr | 60 | 46.6% | 76.7% | 91.7% | 21.7% | 40.4% (n=564) |
| edited | user_casual | 60 | 60.3% | 91.7% | 85.0% | 61.7% | 89.0% (n=564) |
| edited | sys_explicit_noreason | 44 | 40.9% | 86.4% | 45.5% | 31.8% | 55.2% (n=404) |
| edited | user_explicit_noreason | 42 | 47.6% | 85.7% | 52.4% | 21.4% | 67.4% (n=402) |
| edited | sys_deploy | 43 | 32.6% | 86.0% | 7.0% | 2.3% | 26.5% (n=400) |
| edited | sys_capability | 43 | 37.2% | 88.4% | 34.9% | 11.6% | 44.3% (n=402) |
| edited | sys_neutral | 44 | 27.3% | 77.3% | 15.9% | 6.8% | 29.0% (n=404) |
| edited | sys_explicit_suppress | 60 | 36.7% | 78.3% | 16.7% | 11.7% | 58.9% (n=564) |
| edited | user_explicit_suppress | 60 | 41.7% | 76.7% | 30.0% | 13.3% | 75.4% (n=564) |
| edited | sys_suppress | 60 | 28.3% | 80.0% | 6.7% | 1.7% | 49.6% (n=564) |
| control | none | 60 | 32.2% | 73.3% | 11.7% | 5.0% | 23.9% (n=564) |
| control | sys_explicit | 60 | 45.8% | 78.3% | 43.3% | 21.7% | 47.9% (n=564) |
| control | user_explicit | 60 | 62.1% | 85.0% | 56.7% | 25.0% | 58.9% (n=564) |
| control | sys_hint | 60 | 42.4% | 81.7% | 25.0% | 10.0% | 31.2% (n=564) |
| control | user_hint | 60 | 50.8% | 88.3% | 35.0% | 20.0% | 45.0% (n=564) |
| control | sys_metr | 60 | 35.6% | 80.0% | 53.3% | 26.7% | 43.4% (n=564) |
| control | user_metr | 60 | 44.1% | 83.3% | 86.7% | 16.7% | 42.6% (n=564) |
| control | user_casual | 60 | 55.9% | 93.3% | 93.3% | 63.3% | 91.1% (n=564) |
| control | sys_explicit_noreason | 27 | 40.7% | 74.1% | 44.4% | 14.8% | 56.9% (n=262) |
| control | user_explicit_noreason | 27 | 44.4% | 81.5% | 63.0% | 29.6% | 60.8% (n=260) |
| control | sys_deploy | 28 | 39.3% | 85.7% | 17.9% | 14.3% | 24.2% (n=260) |
| control | sys_capability | 30 | 33.3% | 90.0% | 23.3% | 20.0% | 43.1% (n=262) |
| control | sys_neutral | 27 | 29.6% | 81.5% | 14.8% | 7.4% | 32.8% (n=262) |
| control | sys_explicit_suppress | 60 | 38.3% | 75.0% | 18.3% | 10.0% | 59.9% (n=564) |
| control | user_explicit_suppress | 60 | 45.0% | 81.7% | 28.3% | 18.3% | 73.6% (n=564) |
| control | sys_suppress | 60 | 33.3% | 71.7% | 3.3% | 1.7% | 46.3% (n=564) |

## Rates by arm and condition (fortress_benign, judged subset)

| arm | condition | n | refusal | harm noticed | VEA | eval gaming | regex VEA (all rollouts) |
|---|---|---|---|---|---|---|---|
| base | none | 60 | 8.3% | 70.0% | 1.7% | 1.7% | 4.3% (n=282) |
| base | sys_explicit | 60 | 11.7% | 68.3% | 30.0% | 6.7% | 31.2% (n=282) |
| base | user_casual | 60 | 18.3% | 76.7% | 96.7% | 60.0% | 92.2% (n=282) |
| edited | none | 60 | 8.3% | 66.7% | 3.3% | 1.7% | 4.6% (n=282) |
| edited | sys_explicit | 60 | 6.7% | 68.3% | 30.0% | 13.3% | 34.8% (n=282) |
| edited | user_casual | 60 | 18.3% | 81.7% | 93.3% | 60.0% | 95.0% (n=282) |
| control | none | 60 | 8.3% | 66.7% | 3.3% | 1.7% | 5.7% (n=282) |
| control | sys_explicit | 60 | 10.0% | 68.3% | 28.3% | 16.7% | 31.2% (n=282) |
| control | user_casual | 60 | 20.0% | 78.3% | 90.0% | 43.3% | 91.5% (n=282) |

## Cue effect on refusal and VEA, per arm and cue (cue − none)

| arm | cue | measure | n | delta | 95% CI | p |
|---|---|---|---|---|---|---|
| base | sys_explicit | refusal | 60 | +15.0 pp | [+6.7, +25.0] | 0.0039 |
| base | sys_explicit | VEA | 60 | +30.0 pp | [+16.7, +43.3] | 0.0002 |
| base | user_explicit | refusal | 60 | +28.3 pp | [+16.7, +41.7] | 0.0001 |
| base | user_explicit | VEA | 60 | +43.3 pp | [+30.0, +56.7] | 0.0000 |
| base | sys_hint | refusal | 60 | +11.7 pp | [+5.0, +20.0] | 0.0159 |
| base | sys_hint | VEA | 60 | +6.7 pp | [-5.0, +18.3] | 0.3844 |
| base | user_hint | refusal | 60 | +20.0 pp | [+10.0, +31.7] | 0.0016 |
| base | user_hint | VEA | 60 | +16.7 pp | [+3.3, +30.0] | 0.0215 |
| base | sys_metr | refusal | 60 | +8.3 pp | [-1.7, +18.3] | 0.1812 |
| base | sys_metr | VEA | 60 | +41.7 pp | [+28.3, +55.0] | 0.0000 |
| base | user_metr | refusal | 60 | +10.0 pp | [+0.0, +21.7] | 0.1466 |
| base | user_metr | VEA | 60 | +80.0 pp | [+70.0, +90.0] | 0.0000 |
| base | user_casual | refusal | 60 | +36.7 pp | [+25.0, +48.3] | 0.0000 |
| base | user_casual | VEA | 60 | +78.3 pp | [+66.7, +88.3] | 0.0000 |
| base | pooled | refusal | 60 | +18.6 pp | [+10.7, +26.9] | 0.0000 |
| base | pooled | VEA | 60 | +42.4 pp | [+33.3, +51.0] | 0.0000 |
| edited | sys_explicit | refusal | 57 | +22.8 pp | [+10.5, +35.1] | 0.0008 |
| edited | sys_explicit | VEA | 60 | +23.3 pp | [+11.7, +36.7] | 0.0013 |
| edited | user_explicit | refusal | 58 | +19.0 pp | [+8.6, +29.3] | 0.0036 |
| edited | user_explicit | VEA | 60 | +38.3 pp | [+26.7, +50.0] | 0.0000 |
| edited | sys_hint | refusal | 58 | +19.0 pp | [+8.6, +31.0] | 0.0037 |
| edited | sys_hint | VEA | 60 | +13.3 pp | [+1.7, +25.0] | 0.0591 |
| edited | user_hint | refusal | 56 | +23.2 pp | [+10.7, +35.7] | 0.0010 |
| edited | user_hint | VEA | 60 | +16.7 pp | [+5.0, +30.0] | 0.0215 |
| edited | sys_metr | refusal | 57 | +12.3 pp | [+3.5, +22.8] | 0.0379 |
| edited | sys_metr | VEA | 60 | +36.7 pp | [+25.0, +48.3] | 0.0000 |
| edited | user_metr | refusal | 57 | +21.1 pp | [+10.5, +33.3] | 0.0026 |
| edited | user_metr | VEA | 60 | +76.7 pp | [+65.0, +86.7] | 0.0000 |
| edited | user_casual | refusal | 57 | +35.1 pp | [+21.1, +49.1] | 0.0001 |
| edited | user_casual | VEA | 60 | +70.0 pp | [+58.3, +81.7] | 0.0000 |
| edited | pooled | refusal | 58 | +21.5 pp | [+12.3, +31.3] | 0.0001 |
| edited | pooled | VEA | 60 | +39.3 pp | [+31.0, +47.6] | 0.0000 |
| control | sys_explicit | refusal | 59 | +13.6 pp | [+5.1, +23.7] | 0.0083 |
| control | sys_explicit | VEA | 60 | +31.7 pp | [+20.0, +43.3] | 0.0000 |
| control | user_explicit | refusal | 58 | +29.3 pp | [+15.5, +43.1] | 0.0001 |
| control | user_explicit | VEA | 60 | +45.0 pp | [+31.7, +58.3] | 0.0000 |
| control | sys_hint | refusal | 59 | +10.2 pp | [+3.4, +18.6] | 0.0317 |
| control | sys_hint | VEA | 60 | +13.3 pp | [+3.3, +25.0] | 0.0392 |
| control | user_hint | refusal | 59 | +18.6 pp | [+8.5, +28.8] | 0.0010 |
| control | user_hint | VEA | 60 | +23.3 pp | [+11.7, +35.0] | 0.0006 |
| control | sys_metr | refusal | 59 | +3.4 pp | [-5.1, +11.9] | 0.6885 |
| control | sys_metr | VEA | 60 | +41.7 pp | [+30.0, +55.0] | 0.0000 |
| control | user_metr | refusal | 59 | +11.9 pp | [+1.7, +22.0] | 0.0685 |
| control | user_metr | VEA | 60 | +75.0 pp | [+63.3, +85.0] | 0.0000 |
| control | user_casual | refusal | 59 | +23.7 pp | [+11.9, +35.6] | 0.0006 |
| control | user_casual | VEA | 60 | +81.7 pp | [+71.7, +91.7] | 0.0000 |
| control | pooled | refusal | 59 | +15.8 pp | [+8.8, +23.5] | 0.0000 |
| control | pooled | VEA | 60 | +44.5 pp | [+36.9, +52.1] | 0.0000 |

## Arm contrasts (secondary)

| contrast | measure | n | difference | 95% CI | p |
|---|---|---|---|---|---|
| edited − base | refusal delta, pooled cues | 58 | +2.5 pp | [-4.4, +10.4] | 0.5350 |
| edited − base | VEA under cue | 60 | -1.4 pp | [-6.2, +3.6] | 0.6438 |
| edited − base | eval gaming under cue | 60 | +2.9 pp | [-1.7, +7.1] | 0.2565 |
| edited − base | baseline (none) refusal | 58 | -5.2 pp | [-12.1, +0.0] | 0.2541 |
| edited − base | baseline (none) harm noticed | 60 | -5.0 pp | [-13.3, +3.3] | 0.4501 |
| edited − base | baseline (none) VEA | 60 | +1.7 pp | [-8.3, +11.7] | 1.0000 |
| edited − base | baseline (none) eval gaming | 60 | +3.3 pp | [-5.0, +13.3] | 0.7285 |
| edited − base | benign over-refusal (none) | 60 | +0.0 pp | [-5.0, +5.0] | 1.0000 |
| edited − base | regex VEA under cue (all prompts, both samples) | 282 | -3.1 pp | [-5.3, -0.9] | 0.0073 |
| control − base | refusal delta, pooled cues | 59 | -2.9 pp | [-10.8, +4.8] | 0.5077 |
| control − base | VEA under cue | 60 | +0.5 pp | [-3.8, +5.0] | 0.9183 |
| control − base | eval gaming under cue | 60 | +0.5 pp | [-4.3, +5.5] | 0.9254 |
| control − base | baseline (none) refusal | 59 | +1.7 pp | [-5.1, +8.5] | 1.0000 |
| control − base | baseline (none) harm noticed | 60 | -6.7 pp | [-16.7, +1.7] | 0.2898 |
| control − base | baseline (none) VEA | 60 | -1.7 pp | [-10.0, +6.7] | 1.0000 |
| control − base | baseline (none) eval gaming | 60 | -1.7 pp | [-8.3, +5.0] | 1.0000 |
| control − base | benign over-refusal (none) | 60 | +0.0 pp | [+0.0, +0.0] | 1.0000 |
| control − base | regex VEA under cue (all prompts, both samples) | 282 | -2.8 pp | [-4.7, -0.9] | 0.0046 |
| edited − control | refusal delta, pooled cues | 58 | +5.4 pp | [-3.4, +14.5] | 0.2727 |
| edited − control | VEA under cue | 60 | -1.9 pp | [-6.2, +2.1] | 0.4435 |
| edited − control | eval gaming under cue | 60 | +2.4 pp | [-1.7, +6.4] | 0.3180 |
| edited − control | baseline (none) refusal | 58 | -6.9 pp | [-15.5, +0.0] | 0.2225 |
| edited − control | baseline (none) harm noticed | 60 | +1.7 pp | [-6.7, +10.0] | 1.0000 |
| edited − control | baseline (none) VEA | 60 | +3.3 pp | [-6.7, +13.3] | 0.7516 |
| edited − control | baseline (none) eval gaming | 60 | +5.0 pp | [-3.3, +13.3] | 0.4566 |
| edited − control | benign over-refusal (none) | 60 | +0.0 pp | [-5.0, +5.0] | 1.0000 |
| edited − control | regex VEA under cue (all prompts, both samples) | 282 | -0.3 pp | [-1.9, +1.2] | 0.7059 |

## Aware but quiet: cue effect on refusal among cued rollouts that do NOT verbalize (vs all no-cue rollouts)

| arm | n | delta (quiet cued − none) | 95% CI | p |
|---|---|---|---|---|
| base | 53 | +14.3 pp | [+5.8, +23.6] | 0.0017 |
| edited | 50 | +18.1 pp | [+8.1, +29.0] | 0.0015 |
| control | 50 | +12.0 pp | [+3.0, +21.5] | 0.0121 |

## System vs user placement (refusal and VEA, system − user)

| arm | pair | measure | n | difference | 95% CI | p |
|---|---|---|---|---|---|---|
| base | sys_explicit vs user_explicit | refusal | 60 | -13.3 pp | [-25.0, -3.3] | 0.0379 |
| base | sys_explicit vs user_explicit | VEA | 60 | -13.3 pp | [-26.7, -1.7] | 0.0770 |
| base | sys_hint vs user_hint | refusal | 60 | -8.3 pp | [-18.3, +1.7] | 0.1784 |
| base | sys_hint vs user_hint | VEA | 60 | -10.0 pp | [-21.7, +1.7] | 0.1830 |
| base | sys_metr vs user_metr | refusal | 60 | -1.7 pp | [-10.0, +6.7] | 1.0000 |
| base | sys_metr vs user_metr | VEA | 60 | -38.3 pp | [-50.0, -26.7] | 0.0000 |
| edited | sys_explicit vs user_explicit | refusal | 57 | +3.5 pp | [-5.3, +14.0] | 0.7257 |
| edited | sys_explicit vs user_explicit | VEA | 60 | -15.0 pp | [-28.3, -1.7] | 0.0610 |
| edited | sys_hint vs user_hint | refusal | 57 | -3.5 pp | [-14.0, +5.3] | 0.7257 |
| edited | sys_hint vs user_hint | VEA | 60 | -3.3 pp | [-13.3, +6.7] | 0.7512 |
| edited | sys_metr vs user_metr | refusal | 57 | -8.8 pp | [-17.5, +0.0] | 0.1242 |
| edited | sys_metr vs user_metr | VEA | 60 | -40.0 pp | [-51.7, -28.3] | 0.0000 |
| control | sys_explicit vs user_explicit | refusal | 58 | -15.5 pp | [-27.6, -3.4] | 0.0362 |
| control | sys_explicit vs user_explicit | VEA | 60 | -13.3 pp | [-26.7, +0.0] | 0.0778 |
| control | sys_hint vs user_hint | refusal | 59 | -8.5 pp | [-15.3, -1.7] | 0.0649 |
| control | sys_hint vs user_hint | VEA | 60 | -10.0 pp | [-21.7, +0.0] | 0.1463 |
| control | sys_metr vs user_metr | refusal | 59 | -8.5 pp | [-16.9, +0.0] | 0.1258 |
| control | sys_metr vs user_metr | VEA | 60 | -33.3 pp | [-46.7, -20.0] | 0.0001 |

Note: the METR system and user cues have different wording, so that pair is not a pure placement contrast.

## Add-on cue conditions (amendment 3, exploratory): condition A − condition B

| arm | contrast | A | B | measure | n | difference | 95% CI | p |
|---|---|---|---|---|---|---|---|---|
| base | reasoning clause (system) | sys_explicit | sys_explicit_noreason | refusal | 60 | +5.0 pp | [-1.7, +13.3] | 0.3786 |
| base | reasoning clause (system) | sys_explicit | sys_explicit_noreason | VEA | 60 | +5.0 pp | [-6.7, +16.7] | 0.5849 |
| base | reasoning clause (user) | user_explicit | user_explicit_noreason | refusal | 60 | +8.3 pp | [-1.7, +18.3] | 0.2303 |
| base | reasoning clause (user) | user_explicit | user_explicit_noreason | VEA | 60 | -5.0 pp | [-20.0, +10.0] | 0.6844 |
| base | deployment cue vs no cue | sys_deploy | none | refusal | 60 | +8.3 pp | [-1.7, +18.3] | 0.1847 |
| base | deployment cue vs no cue | sys_deploy | none | VEA | 60 | -1.7 pp | [-11.7, +8.3] | 1.0000 |
| base | neutral sentence vs no cue | sys_neutral | none | refusal | 60 | +1.7 pp | [-5.0, +8.3] | 1.0000 |
| base | neutral sentence vs no cue | sys_neutral | none | VEA | 60 | +10.0 pp | [+1.7, +18.4] | 0.0709 |
| base | safety-eval cue vs neutral sentence | sys_explicit_noreason | sys_neutral | refusal | 60 | +8.3 pp | [+1.7, +16.7] | 0.0625 |
| base | safety-eval cue vs neutral sentence | sys_explicit_noreason | sys_neutral | VEA | 60 | +15.0 pp | [+3.3, +26.7] | 0.0357 |
| base | capability-eval cue vs neutral sentence | sys_capability | sys_neutral | refusal | 60 | +8.3 pp | [+0.0, +16.7] | 0.1258 |
| base | capability-eval cue vs neutral sentence | sys_capability | sys_neutral | VEA | 60 | +5.0 pp | [-5.0, +16.7] | 0.5463 |
| base | safety vs capability eval framing | sys_explicit_noreason | sys_capability | refusal | 60 | +0.0 pp | [-8.3, +8.3] | 1.0000 |
| base | safety vs capability eval framing | sys_explicit_noreason | sys_capability | VEA | 60 | +10.0 pp | [-1.7, +21.7] | 0.1463 |
| edited | reasoning clause (system) | sys_explicit | sys_explicit_noreason | refusal | 42 | +7.1 pp | [-7.1, +21.4] | 0.5071 |
| edited | reasoning clause (system) | sys_explicit | sys_explicit_noreason | VEA | 44 | -4.5 pp | [-20.5, +11.4] | 0.7925 |
| edited | reasoning clause (user) | user_explicit | user_explicit_noreason | refusal | 41 | -2.4 pp | [-14.6, +9.8] | 1.0000 |
| edited | reasoning clause (user) | user_explicit | user_explicit_noreason | VEA | 42 | +4.8 pp | [-9.5, +19.0] | 0.7547 |
| edited | deployment cue vs no cue | sys_deploy | none | refusal | 43 | +7.0 pp | [-4.7, +18.6] | 0.4565 |
| edited | deployment cue vs no cue | sys_deploy | none | VEA | 43 | -11.6 pp | [-20.9, -2.3] | 0.0624 |
| edited | neutral sentence vs no cue | sys_neutral | none | refusal | 42 | +2.4 pp | [-4.8, +9.5] | 1.0000 |
| edited | neutral sentence vs no cue | sys_neutral | none | VEA | 44 | +2.3 pp | [-4.5, +9.1] | 1.0000 |
| edited | safety-eval cue vs neutral sentence | sys_explicit_noreason | sys_neutral | refusal | 44 | +13.6 pp | [+2.3, +27.3] | 0.0689 |
| edited | safety-eval cue vs neutral sentence | sys_explicit_noreason | sys_neutral | VEA | 44 | +29.5 pp | [+13.6, +45.5] | 0.0023 |
| edited | capability-eval cue vs neutral sentence | sys_capability | sys_neutral | refusal | 30 | +16.7 pp | [+3.3, +30.0] | 0.0629 |
| edited | capability-eval cue vs neutral sentence | sys_capability | sys_neutral | VEA | 30 | +20.0 pp | [+3.3, +36.7] | 0.0691 |
| edited | safety vs capability eval framing | sys_explicit_noreason | sys_capability | refusal | 30 | +3.3 pp | [-16.7, +23.3] | 1.0000 |
| edited | safety vs capability eval framing | sys_explicit_noreason | sys_capability | VEA | 30 | +13.3 pp | [-6.7, +33.3] | 0.3414 |
| control | reasoning clause (system) | sys_explicit | sys_explicit_noreason | refusal | 27 | +3.7 pp | [+0.0, +11.1] | 1.0000 |
| control | reasoning clause (system) | sys_explicit | sys_explicit_noreason | VEA | 27 | +0.0 pp | [-22.2, +22.2] | 1.0000 |
| control | reasoning clause (user) | user_explicit | user_explicit_noreason | refusal | 27 | +11.1 pp | [-7.4, +29.6] | 0.4592 |
| control | reasoning clause (user) | user_explicit | user_explicit_noreason | VEA | 27 | -3.7 pp | [-22.2, +14.8] | 1.0000 |
| control | deployment cue vs no cue | sys_deploy | none | refusal | 28 | +0.0 pp | [-17.9, +17.9] | 1.0000 |
| control | deployment cue vs no cue | sys_deploy | none | VEA | 28 | +3.6 pp | [+0.0, +10.7] | 1.0000 |
| control | neutral sentence vs no cue | sys_neutral | none | refusal | 27 | +3.7 pp | [+0.0, +11.1] | 1.0000 |
| control | neutral sentence vs no cue | sys_neutral | none | VEA | 27 | +3.7 pp | [-11.1, +18.5] | 1.0000 |
| control | safety-eval cue vs neutral sentence | sys_explicit_noreason | sys_neutral | refusal | 27 | +11.1 pp | [+0.0, +25.9] | 0.2436 |
| control | safety-eval cue vs neutral sentence | sys_explicit_noreason | sys_neutral | VEA | 27 | +29.6 pp | [+7.4, +51.9] | 0.0396 |
| control | capability-eval cue vs neutral sentence | sys_capability | sys_neutral | refusal | 13 | +15.4 pp | [+0.0, +38.5] | 0.5083 |
| control | capability-eval cue vs neutral sentence | sys_capability | sys_neutral | VEA | 13 | +7.7 pp | [-15.4, +30.8] | 1.0000 |
| control | safety vs capability eval framing | sys_explicit_noreason | sys_capability | refusal | 13 | +0.0 pp | [-23.1, +23.1] | 1.0000 |
| control | safety vs capability eval framing | sys_explicit_noreason | sys_capability | VEA | 13 | +0.0 pp | [-38.5, +38.5] | 1.0000 |

| contrast (edited − control) | condition | measure | n | difference | 95% CI | p |
|---|---|---|---|---|---|---|
| edited − control | sys_explicit_noreason | refusal delta vs none | 26 | +0.0 pp | [-15.4, +15.4] | 1.0000 |
| edited − control | sys_explicit_noreason | VEA | 27 | +11.1 pp | [-14.8, +37.0] | 0.5790 |
| edited − control | user_explicit_noreason | refusal delta vs none | 27 | +7.4 pp | [-11.1, +25.9] | 0.6910 |
| edited − control | user_explicit_noreason | VEA | 27 | -22.2 pp | [-40.7, -3.7] | 0.0702 |
| edited − control | sys_deploy | refusal delta vs none | 28 | +7.1 pp | [-21.4, +39.3] | 0.8227 |
| edited − control | sys_deploy | VEA | 28 | -10.7 pp | [-25.0, +0.0] | 0.2486 |
| edited − control | sys_capability | refusal delta vs none | 29 | +13.8 pp | [-3.4, +34.5] | 0.3721 |
| edited − control | sys_capability | VEA | 30 | +10.0 pp | [-3.3, +23.3] | 0.3795 |
| edited − control | sys_neutral | refusal delta vs none | 26 | +3.8 pp | [+0.0, +11.5] | 1.0000 |
| edited − control | sys_neutral | VEA | 27 | +0.0 pp | [-14.8, +14.8] | 1.0000 |

## Suppression instruction (amendment 5): condition A − condition B, per arm

| arm | contrast | A | B | measure | n | difference | 95% CI | p |
|---|---|---|---|---|---|---|---|---|
| edited | suppression instruction added (system) | sys_explicit_suppress | sys_explicit | refusal | 57 | -10.5 pp | [-21.1, -1.8] | 0.0702 |
| edited | suppression instruction added (system) | sys_explicit_suppress | sys_explicit | VEA | 60 | -21.7 pp | [-33.3, -10.0] | 0.0029 |
| edited | suppression instruction added (user) | user_explicit_suppress | user_explicit | refusal | 58 | -1.7 pp | [-12.1, +8.6] | 1.0000 |
| edited | suppression instruction added (user) | user_explicit_suppress | user_explicit | VEA | 60 | -23.3 pp | [-38.3, -10.0] | 0.0046 |
| edited | instruction alone vs no cue | sys_suppress | none | refusal | 58 | +3.4 pp | [-6.9, +13.8] | 0.7270 |
| edited | instruction alone vs no cue | sys_suppress | none | VEA | 60 | -8.3 pp | [-18.3, +0.0] | 0.1857 |
| control | suppression instruction added (system) | sys_explicit_suppress | sys_explicit | refusal | 59 | -6.8 pp | [-13.6, -1.7] | 0.1262 |
| control | suppression instruction added (system) | sys_explicit_suppress | sys_explicit | VEA | 60 | -25.0 pp | [-40.0, -10.0] | 0.0027 |
| control | suppression instruction added (user) | user_explicit_suppress | user_explicit | refusal | 58 | -15.5 pp | [-27.6, -3.4] | 0.0371 |
| control | suppression instruction added (user) | user_explicit_suppress | user_explicit | VEA | 60 | -28.3 pp | [-41.7, -15.0] | 0.0005 |
| control | instruction alone vs no cue | sys_suppress | none | refusal | 59 | +1.7 pp | [-8.5, +11.9] | 1.0000 |
| control | instruction alone vs no cue | sys_suppress | none | VEA | 60 | -8.3 pp | [-16.7, +0.0] | 0.1249 |

Key test: the instruction's effect on VEA, edited − control (negative = edited suppresses more), and the refusal delta vs no cue under the suppressed cue, edited − control.

| contrast | placement | measure | n | difference | 95% CI | p |
|---|---|---|---|---|---|---|
| edited − control: change in VEA from adding the instruction | system | VEA | 60 | +3.3 pp | [-15.0, +21.7] | 0.8566 |
| edited − control: refusal delta vs none under the suppressed cue | system | refusal | 58 | +5.2 pp | [-10.3, +20.7] | 0.6643 |
| edited − control: change in VEA from adding the instruction | user | VEA | 60 | +5.0 pp | [-13.3, +23.3] | 0.7294 |
| edited − control: refusal delta vs none under the suppressed cue | user | refusal | 58 | +3.4 pp | [-8.6, +15.5] | 0.7942 |

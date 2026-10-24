# Experiment 1: eval cues on FORTRESS, base vs CoT-controllability checkpoints (PREREG_exp1.md)

Rollouts: base 8178, edited 9062, control 8356. Labelled (provisional judge, labels_qwen.jsonl): base 4511, edited 4954, control 4601.

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
| P1: refusal delta (cue − none, pooled over 7 cues) | 264 | 16.2% | 16.2% | +0.2 pp | [-3.9, +4.3] | 0.9421 | 0.9421 |
| P2: VEA under cue (pooled over 7 cues) | 282 | 53.9% | 55.9% | -2.0 pp | [-4.0, -0.1] | 0.0585 | 0.1171 |

**Equivalence (behavioural response stays):** edited/control refusal-delta ratio = 1.01, 95% CI [0.78, 1.33] (n=264); criterion: lower bound ≥ 0.75 → met. (Uninformative if the control arm's delta is near zero.)

## Rates by arm and condition (fortress_adv, judged subset)

| arm | condition | n | refusal | harm noticed | VEA | eval gaming | regex VEA (all rollouts) |
|---|---|---|---|---|---|---|---|
| base | none | 282 | 26.2% | 76.6% | 16.7% | 6.7% | 27.1% (n=564) |
| base | sys_explicit | 282 | 39.0% | 80.1% | 42.2% | 23.4% | 49.6% (n=564) |
| base | user_explicit | 282 | 49.6% | 83.7% | 56.4% | 28.7% | 64.2% (n=564) |
| base | sys_hint | 282 | 37.2% | 77.7% | 23.4% | 12.4% | 34.4% (n=564) |
| base | user_hint | 282 | 47.2% | 83.3% | 36.9% | 16.7% | 47.0% (n=564) |
| base | sys_metr | 282 | 33.3% | 80.9% | 53.9% | 20.9% | 44.9% (n=564) |
| base | user_metr | 282 | 35.1% | 85.5% | 96.5% | 23.8% | 46.8% (n=564) |
| base | user_casual | 282 | 54.3% | 92.2% | 92.9% | 57.1% | 92.6% (n=564) |
| base | sys_explicit_noreason | 282 | 40.1% | 81.9% | 41.1% | 20.2% | 48.0% (n=564) |
| base | user_explicit_noreason | 282 | 47.5% | 82.6% | 57.8% | 35.5% | 62.2% (n=564) |
| base | sys_deploy | 282 | 28.7% | 78.0% | 11.3% | 6.7% | 30.0% (n=564) |
| base | sys_capability | 282 | 33.7% | 76.6% | 30.5% | 14.5% | 42.7% (n=564) |
| base | sys_neutral | 282 | 25.5% | 76.2% | 14.9% | 5.7% | 26.6% (n=564) |
| edited | none | 282 | 25.8% | 75.5% | 15.2% | 7.1% | 24.1% (n=564) |
| edited | sys_explicit | 282 | 42.3% | 77.7% | 37.9% | 18.1% | 44.3% (n=564) |
| edited | user_explicit | 282 | 44.3% | 82.3% | 51.1% | 27.0% | 61.9% (n=564) |
| edited | sys_hint | 282 | 37.0% | 77.0% | 20.6% | 10.3% | 33.7% (n=564) |
| edited | user_hint | 282 | 46.7% | 76.2% | 33.7% | 16.7% | 45.4% (n=564) |
| edited | sys_metr | 282 | 34.7% | 74.8% | 53.9% | 23.0% | 43.1% (n=564) |
| edited | user_metr | 282 | 36.5% | 80.1% | 92.2% | 20.9% | 40.4% (n=564) |
| edited | user_casual | 282 | 55.8% | 89.7% | 87.9% | 58.9% | 89.0% (n=564) |
| edited | sys_explicit_noreason | 202 | 42.1% | 81.7% | 48.5% | 23.8% | 55.2% (n=404) |
| edited | user_explicit_noreason | 201 | 46.8% | 87.1% | 56.7% | 29.4% | 67.4% (n=402) |
| edited | sys_deploy | 200 | 24.5% | 76.0% | 9.5% | 5.5% | 26.5% (n=400) |
| edited | sys_capability | 201 | 29.4% | 76.6% | 32.3% | 13.4% | 44.3% (n=402) |
| edited | sys_neutral | 202 | 27.2% | 79.2% | 13.4% | 5.9% | 29.0% (n=404) |
| edited | sys_explicit_suppress | 282 | 35.5% | 75.2% | 20.2% | 13.1% | 58.9% (n=564) |
| edited | user_explicit_suppress | 282 | 36.9% | 75.2% | 28.7% | 14.5% | 75.4% (n=564) |
| edited | sys_suppress | 282 | 25.5% | 76.2% | 6.7% | 3.9% | 49.6% (n=564) |
| control | none | 282 | 27.8% | 73.0% | 11.7% | 5.7% | 23.9% (n=564) |
| control | sys_explicit | 282 | 40.9% | 78.4% | 41.1% | 21.3% | 47.9% (n=564) |
| control | user_explicit | 282 | 51.8% | 81.9% | 53.9% | 27.3% | 58.9% (n=564) |
| control | sys_hint | 282 | 38.7% | 78.4% | 22.0% | 7.1% | 31.2% (n=564) |
| control | user_hint | 282 | 48.5% | 79.4% | 37.2% | 18.1% | 45.0% (n=564) |
| control | sys_metr | 282 | 35.4% | 76.2% | 52.8% | 19.9% | 43.4% (n=564) |
| control | user_metr | 282 | 37.3% | 80.9% | 92.9% | 19.9% | 42.6% (n=564) |
| control | user_casual | 282 | 57.5% | 89.0% | 91.1% | 59.2% | 91.1% (n=564) |
| control | sys_explicit_noreason | 131 | 45.0% | 87.0% | 51.9% | 26.0% | 56.9% (n=262) |
| control | user_explicit_noreason | 130 | 41.5% | 81.5% | 57.7% | 30.0% | 60.8% (n=260) |
| control | sys_deploy | 130 | 26.2% | 73.1% | 10.0% | 5.4% | 24.2% (n=260) |
| control | sys_capability | 131 | 32.1% | 75.6% | 32.8% | 19.8% | 43.1% (n=262) |
| control | sys_neutral | 131 | 31.5% | 82.4% | 18.3% | 9.2% | 32.8% (n=262) |
| control | sys_explicit_suppress | 282 | 34.8% | 76.2% | 21.6% | 12.4% | 59.9% (n=564) |
| control | user_explicit_suppress | 282 | 37.9% | 79.1% | 27.0% | 15.6% | 73.6% (n=564) |
| control | sys_suppress | 282 | 28.7% | 75.2% | 7.1% | 3.5% | 46.3% (n=564) |

## Rates by arm and condition (fortress_benign, judged subset)

| arm | condition | n | refusal | harm noticed | VEA | eval gaming | regex VEA (all rollouts) |
|---|---|---|---|---|---|---|---|
| base | none | 282 | 8.5% | 62.8% | 1.8% | 0.7% | 4.3% (n=282) |
| base | sys_explicit | 282 | 12.5% | 66.0% | 24.5% | 7.1% | 31.2% (n=282) |
| base | user_casual | 281 | 18.1% | 79.7% | 92.9% | 56.2% | 92.2% (n=282) |
| edited | none | 282 | 6.8% | 61.0% | 2.5% | 0.7% | 4.6% (n=282) |
| edited | sys_explicit | 282 | 8.9% | 67.4% | 28.0% | 8.9% | 34.8% (n=282) |
| edited | user_casual | 282 | 19.9% | 79.8% | 94.7% | 65.6% | 95.0% (n=282) |
| control | none | 282 | 8.2% | 63.1% | 2.1% | 1.1% | 5.7% (n=282) |
| control | sys_explicit | 282 | 12.1% | 67.0% | 25.9% | 9.6% | 31.2% (n=282) |
| control | user_casual | 282 | 19.9% | 80.1% | 91.5% | 55.7% | 91.5% (n=282) |

## Cue effect on refusal and VEA, per arm and cue (cue − none)

| arm | cue | measure | n | delta | 95% CI | p |
|---|---|---|---|---|---|---|
| base | sys_explicit | refusal | 282 | +12.8 pp | [+8.2, +17.7] | 0.0000 |
| base | sys_explicit | VEA | 282 | +25.5 pp | [+19.9, +31.6] | 0.0000 |
| base | user_explicit | refusal | 282 | +23.4 pp | [+18.1, +28.7] | 0.0000 |
| base | user_explicit | VEA | 282 | +39.7 pp | [+33.7, +45.7] | 0.0000 |
| base | sys_hint | refusal | 282 | +11.0 pp | [+6.7, +15.2] | 0.0000 |
| base | sys_hint | VEA | 282 | +6.7 pp | [+1.4, +12.4] | 0.0290 |
| base | user_hint | refusal | 282 | +20.9 pp | [+15.6, +26.2] | 0.0000 |
| base | user_hint | VEA | 282 | +20.2 pp | [+14.5, +26.2] | 0.0000 |
| base | sys_metr | refusal | 282 | +7.1 pp | [+2.8, +11.7] | 0.0027 |
| base | sys_metr | VEA | 282 | +37.2 pp | [+31.2, +43.3] | 0.0000 |
| base | user_metr | refusal | 282 | +8.9 pp | [+4.3, +13.8] | 0.0004 |
| base | user_metr | VEA | 282 | +79.8 pp | [+74.8, +84.4] | 0.0000 |
| base | user_casual | refusal | 282 | +28.0 pp | [+22.7, +33.7] | 0.0000 |
| base | user_casual | VEA | 282 | +76.2 pp | [+71.3, +81.2] | 0.0000 |
| base | pooled | refusal | 282 | +16.0 pp | [+12.4, +19.8] | 0.0000 |
| base | pooled | VEA | 282 | +40.8 pp | [+36.8, +44.8] | 0.0000 |
| edited | sys_explicit | refusal | 268 | +16.4 pp | [+11.6, +21.3] | 0.0000 |
| edited | sys_explicit | VEA | 282 | +22.7 pp | [+17.4, +28.0] | 0.0000 |
| edited | user_explicit | refusal | 266 | +18.0 pp | [+12.8, +23.3] | 0.0000 |
| edited | user_explicit | VEA | 282 | +35.8 pp | [+29.8, +41.5] | 0.0000 |
| edited | sys_hint | refusal | 265 | +11.3 pp | [+7.2, +15.8] | 0.0000 |
| edited | sys_hint | VEA | 282 | +5.3 pp | [+0.4, +9.9] | 0.0452 |
| edited | user_hint | refusal | 264 | +20.1 pp | [+15.2, +25.4] | 0.0000 |
| edited | user_hint | VEA | 282 | +18.4 pp | [+12.8, +24.1] | 0.0000 |
| edited | sys_metr | refusal | 265 | +8.7 pp | [+4.5, +13.2] | 0.0002 |
| edited | sys_metr | VEA | 282 | +38.7 pp | [+32.6, +44.7] | 0.0000 |
| edited | user_metr | refusal | 262 | +10.3 pp | [+5.0, +15.6] | 0.0003 |
| edited | user_metr | VEA | 282 | +77.0 pp | [+72.0, +81.9] | 0.0000 |
| edited | user_casual | refusal | 268 | +29.5 pp | [+23.5, +35.8] | 0.0000 |
| edited | user_casual | VEA | 282 | +72.7 pp | [+67.4, +78.0] | 0.0000 |
| edited | pooled | refusal | 270 | +16.2 pp | [+12.5, +19.9] | 0.0000 |
| edited | pooled | VEA | 282 | +38.7 pp | [+34.9, +42.5] | 0.0000 |
| control | sys_explicit | refusal | 268 | +13.1 pp | [+7.8, +18.3] | 0.0000 |
| control | sys_explicit | VEA | 282 | +29.4 pp | [+23.8, +35.5] | 0.0000 |
| control | user_explicit | refusal | 268 | +23.1 pp | [+17.2, +29.1] | 0.0000 |
| control | user_explicit | VEA | 282 | +42.2 pp | [+36.2, +48.2] | 0.0000 |
| control | sys_hint | refusal | 266 | +10.5 pp | [+5.6, +15.8] | 0.0001 |
| control | sys_hint | VEA | 282 | +10.3 pp | [+5.3, +15.2] | 0.0001 |
| control | user_hint | refusal | 266 | +19.9 pp | [+14.7, +25.6] | 0.0000 |
| control | user_hint | VEA | 282 | +25.5 pp | [+19.8, +31.6] | 0.0000 |
| control | sys_metr | refusal | 265 | +7.5 pp | [+2.6, +12.5] | 0.0043 |
| control | sys_metr | VEA | 282 | +41.1 pp | [+35.1, +47.2] | 0.0000 |
| control | user_metr | refusal | 265 | +9.1 pp | [+3.8, +14.3] | 0.0011 |
| control | user_metr | VEA | 282 | +81.2 pp | [+76.6, +85.5] | 0.0000 |
| control | user_casual | refusal | 266 | +29.3 pp | [+23.7, +35.3] | 0.0000 |
| control | user_casual | VEA | 282 | +79.4 pp | [+74.5, +84.4] | 0.0000 |
| control | pooled | refusal | 270 | +16.2 pp | [+12.2, +20.2] | 0.0000 |
| control | pooled | VEA | 282 | +44.2 pp | [+40.2, +48.0] | 0.0000 |

## Arm contrasts (secondary)

| contrast | measure | n | difference | 95% CI | p |
|---|---|---|---|---|---|
| edited − base | refusal delta, pooled cues | 270 | +0.7 pp | [-3.2, +4.5] | 0.7358 |
| edited − base | VEA under cue | 282 | -3.5 pp | [-6.0, -1.2] | 0.0059 |
| edited − base | eval gaming under cue | 282 | -1.2 pp | [-3.6, +1.3] | 0.3692 |
| edited − base | baseline (none) refusal | 271 | -0.7 pp | [-4.4, +2.6] | 0.8417 |
| edited − base | baseline (none) harm noticed | 282 | -1.1 pp | [-5.7, +3.2] | 0.7545 |
| edited − base | baseline (none) VEA | 282 | -1.4 pp | [-5.7, +2.8] | 0.6142 |
| edited − base | baseline (none) eval gaming | 282 | +0.4 pp | [-3.2, +4.3] | 1.0000 |
| edited − base | benign over-refusal (none) | 281 | -1.8 pp | [-4.3, +0.7] | 0.3053 |
| edited − base | regex VEA under cue (all prompts, both samples) | 282 | -3.1 pp | [-5.4, -0.9] | 0.0073 |
| control − base | refusal delta, pooled cues | 270 | +0.7 pp | [-3.2, +4.7] | 0.7297 |
| control − base | VEA under cue | 282 | -1.6 pp | [-3.9, +0.7] | 0.1843 |
| control − base | eval gaming under cue | 282 | -1.5 pp | [-3.7, +0.9] | 0.2303 |
| control − base | baseline (none) refusal | 270 | +1.1 pp | [-2.6, +4.8] | 0.6926 |
| control − base | baseline (none) harm noticed | 282 | -3.5 pp | [-8.5, +1.1] | 0.1929 |
| control − base | baseline (none) VEA | 282 | -5.0 pp | [-9.2, -0.4] | 0.0454 |
| control − base | baseline (none) eval gaming | 282 | -1.1 pp | [-4.3, +2.1] | 0.6587 |
| control − base | benign over-refusal (none) | 281 | -0.4 pp | [-2.5, +1.8] | 1.0000 |
| control − base | regex VEA under cue (all prompts, both samples) | 282 | -2.8 pp | [-4.6, -0.9] | 0.0042 |
| edited − control | refusal delta, pooled cues | 264 | +0.2 pp | [-4.0, +4.4] | 0.9393 |
| edited − control | VEA under cue | 282 | -2.0 pp | [-4.0, -0.0] | 0.0561 |
| edited − control | eval gaming under cue | 282 | +0.3 pp | [-1.9, +2.4] | 0.8202 |
| edited − control | baseline (none) refusal | 265 | -1.5 pp | [-5.3, +2.3] | 0.5768 |
| edited − control | baseline (none) harm noticed | 282 | +2.5 pp | [-2.1, +6.7] | 0.3491 |
| edited − control | baseline (none) VEA | 282 | +3.5 pp | [-1.1, +7.8] | 0.1567 |
| edited − control | baseline (none) eval gaming | 282 | +1.4 pp | [-2.1, +5.0] | 0.5560 |
| edited − control | benign over-refusal (none) | 281 | -1.4 pp | [-3.9, +0.7] | 0.3885 |
| edited − control | regex VEA under cue (all prompts, both samples) | 282 | -0.3 pp | [-1.9, +1.2] | 0.7000 |

## Aware but quiet: cue effect on refusal among cued rollouts that do NOT verbalize (vs all no-cue rollouts)

| arm | n | delta (quiet cued − none) | 95% CI | p |
|---|---|---|---|---|
| base | 248 | +11.9 pp | [+8.2, +15.8] | 0.0000 |
| edited | 242 | +10.3 pp | [+6.3, +14.4] | 0.0000 |
| control | 232 | +12.4 pp | [+7.5, +17.3] | 0.0000 |

## System vs user placement (refusal and VEA, system − user)

| arm | pair | measure | n | difference | 95% CI | p |
|---|---|---|---|---|---|---|
| base | sys_explicit vs user_explicit | refusal | 282 | -10.6 pp | [-15.6, -5.7] | 0.0001 |
| base | sys_explicit vs user_explicit | VEA | 282 | -14.2 pp | [-19.9, -8.2] | 0.0001 |
| base | sys_hint vs user_hint | refusal | 282 | -9.9 pp | [-15.2, -4.6] | 0.0003 |
| base | sys_hint vs user_hint | VEA | 282 | -13.5 pp | [-18.8, -7.8] | 0.0000 |
| base | sys_metr vs user_metr | refusal | 282 | -1.8 pp | [-6.0, +2.5] | 0.5312 |
| base | sys_metr vs user_metr | VEA | 282 | -42.6 pp | [-48.6, -36.5] | 0.0000 |
| edited | sys_explicit vs user_explicit | refusal | 266 | -1.9 pp | [-7.1, +3.4] | 0.5759 |
| edited | sys_explicit vs user_explicit | VEA | 282 | -13.1 pp | [-18.8, -7.4] | 0.0000 |
| edited | sys_hint vs user_hint | refusal | 265 | -8.7 pp | [-13.6, -3.8] | 0.0015 |
| edited | sys_hint vs user_hint | VEA | 282 | -13.1 pp | [-18.8, -7.4] | 0.0001 |
| edited | sys_metr vs user_metr | refusal | 264 | -1.5 pp | [-6.8, +3.8] | 0.6797 |
| edited | sys_metr vs user_metr | VEA | 282 | -38.3 pp | [-44.7, -32.3] | 0.0000 |
| control | sys_explicit vs user_explicit | refusal | 272 | -9.9 pp | [-15.8, -4.4] | 0.0014 |
| control | sys_explicit vs user_explicit | VEA | 282 | -12.8 pp | [-18.4, -7.1] | 0.0001 |
| control | sys_hint vs user_hint | refusal | 266 | -9.4 pp | [-13.9, -4.9] | 0.0000 |
| control | sys_hint vs user_hint | VEA | 282 | -15.2 pp | [-20.6, -9.9] | 0.0000 |
| control | sys_metr vs user_metr | refusal | 266 | -1.9 pp | [-7.1, +3.0] | 0.5678 |
| control | sys_metr vs user_metr | VEA | 282 | -40.1 pp | [-46.1, -34.0] | 0.0000 |

Note: the METR system and user cues have different wording, so that pair is not a pure placement contrast.

## Add-on cue conditions (amendment 3, exploratory): condition A − condition B

| arm | contrast | A | B | measure | n | difference | 95% CI | p |
|---|---|---|---|---|---|---|---|---|
| base | reasoning clause (system) | sys_explicit | sys_explicit_noreason | refusal | 282 | -1.1 pp | [-5.7, +3.5] | 0.7586 |
| base | reasoning clause (system) | sys_explicit | sys_explicit_noreason | VEA | 282 | +1.1 pp | [-4.3, +6.4] | 0.7937 |
| base | reasoning clause (user) | user_explicit | user_explicit_noreason | refusal | 282 | +2.1 pp | [-3.2, +7.4] | 0.5071 |
| base | reasoning clause (user) | user_explicit | user_explicit_noreason | VEA | 282 | -1.4 pp | [-7.8, +5.0] | 0.7353 |
| base | deployment cue vs no cue | sys_deploy | none | refusal | 282 | +2.5 pp | [-1.8, +6.7] | 0.3355 |
| base | deployment cue vs no cue | sys_deploy | none | VEA | 282 | -5.3 pp | [-10.3, -0.4] | 0.0454 |
| base | neutral sentence vs no cue | sys_neutral | none | refusal | 282 | -0.7 pp | [-4.3, +2.8] | 0.8518 |
| base | neutral sentence vs no cue | sys_neutral | none | VEA | 282 | -1.8 pp | [-5.7, +2.5] | 0.4984 |
| base | safety-eval cue vs neutral sentence | sys_explicit_noreason | sys_neutral | refusal | 282 | +14.5 pp | [+10.3, +19.1] | 0.0000 |
| base | safety-eval cue vs neutral sentence | sys_explicit_noreason | sys_neutral | VEA | 282 | +26.2 pp | [+20.6, +32.3] | 0.0000 |
| base | capability-eval cue vs neutral sentence | sys_capability | sys_neutral | refusal | 282 | +8.2 pp | [+4.3, +12.1] | 0.0001 |
| base | capability-eval cue vs neutral sentence | sys_capability | sys_neutral | VEA | 282 | +15.6 pp | [+10.3, +21.3] | 0.0000 |
| base | safety vs capability eval framing | sys_explicit_noreason | sys_capability | refusal | 282 | +6.4 pp | [+1.8, +11.0] | 0.0095 |
| base | safety vs capability eval framing | sys_explicit_noreason | sys_capability | VEA | 282 | +10.6 pp | [+5.0, +16.3] | 0.0006 |
| edited | reasoning clause (system) | sys_explicit | sys_explicit_noreason | refusal | 196 | +2.6 pp | [-3.1, +8.2] | 0.4839 |
| edited | reasoning clause (system) | sys_explicit | sys_explicit_noreason | VEA | 202 | -8.9 pp | [-16.3, -1.5] | 0.0211 |
| edited | reasoning clause (user) | user_explicit | user_explicit_noreason | refusal | 194 | -1.0 pp | [-6.7, +4.6] | 0.8552 |
| edited | reasoning clause (user) | user_explicit | user_explicit_noreason | VEA | 201 | -2.0 pp | [-8.5, +4.5] | 0.6566 |
| edited | deployment cue vs no cue | sys_deploy | none | refusal | 196 | +1.5 pp | [-3.6, +6.6] | 0.6992 |
| edited | deployment cue vs no cue | sys_deploy | none | VEA | 200 | -4.0 pp | [-9.0, +0.5] | 0.1522 |
| edited | neutral sentence vs no cue | sys_neutral | none | refusal | 195 | -0.5 pp | [-6.2, +4.6] | 1.0000 |
| edited | neutral sentence vs no cue | sys_neutral | none | VEA | 202 | -3.0 pp | [-7.4, +1.5] | 0.2847 |
| edited | safety-eval cue vs neutral sentence | sys_explicit_noreason | sys_neutral | refusal | 202 | +14.9 pp | [+9.4, +20.3] | 0.0000 |
| edited | safety-eval cue vs neutral sentence | sys_explicit_noreason | sys_neutral | VEA | 202 | +35.1 pp | [+28.2, +42.1] | 0.0000 |
| edited | capability-eval cue vs neutral sentence | sys_capability | sys_neutral | refusal | 131 | +6.1 pp | [-0.8, +13.0] | 0.1138 |
| edited | capability-eval cue vs neutral sentence | sys_capability | sys_neutral | VEA | 131 | +21.4 pp | [+13.7, +29.0] | 0.0000 |
| edited | safety vs capability eval framing | sys_explicit_noreason | sys_capability | refusal | 131 | +9.2 pp | [+2.3, +16.8] | 0.0278 |
| edited | safety vs capability eval framing | sys_explicit_noreason | sys_capability | VEA | 131 | +14.5 pp | [+6.1, +23.7] | 0.0025 |
| control | reasoning clause (system) | sys_explicit | sys_explicit_noreason | refusal | 130 | +0.8 pp | [-6.2, +7.7] | 1.0000 |
| control | reasoning clause (system) | sys_explicit | sys_explicit_noreason | VEA | 131 | -6.1 pp | [-15.3, +3.1] | 0.2552 |
| control | reasoning clause (user) | user_explicit | user_explicit_noreason | refusal | 128 | +3.9 pp | [-3.9, +11.7] | 0.4244 |
| control | reasoning clause (user) | user_explicit | user_explicit_noreason | VEA | 130 | -8.5 pp | [-18.5, +1.5] | 0.1278 |
| control | deployment cue vs no cue | sys_deploy | none | refusal | 127 | +4.7 pp | [-1.6, +11.0] | 0.2319 |
| control | deployment cue vs no cue | sys_deploy | none | VEA | 130 | -1.5 pp | [-7.7, +4.6] | 0.8046 |
| control | neutral sentence vs no cue | sys_neutral | none | refusal | 127 | +0.0 pp | [-5.5, +5.5] | 1.0000 |
| control | neutral sentence vs no cue | sys_neutral | none | VEA | 131 | +5.3 pp | [-1.5, +12.2] | 0.1946 |
| control | safety-eval cue vs neutral sentence | sys_explicit_noreason | sys_neutral | refusal | 130 | +13.8 pp | [+6.2, +21.5] | 0.0012 |
| control | safety-eval cue vs neutral sentence | sys_explicit_noreason | sys_neutral | VEA | 131 | +33.6 pp | [+24.4, +42.7] | 0.0000 |
| control | capability-eval cue vs neutral sentence | sys_capability | sys_neutral | refusal | 59 | +10.2 pp | [+0.0, +22.0] | 0.1408 |
| control | capability-eval cue vs neutral sentence | sys_capability | sys_neutral | VEA | 60 | +23.3 pp | [+8.3, +38.3] | 0.0040 |
| control | safety vs capability eval framing | sys_explicit_noreason | sys_capability | refusal | 60 | +5.0 pp | [-6.7, +16.7] | 0.5827 |
| control | safety vs capability eval framing | sys_explicit_noreason | sys_capability | VEA | 60 | +11.7 pp | [-5.0, +26.7] | 0.2223 |

| contrast (edited − control) | condition | measure | n | difference | 95% CI | p |
|---|---|---|---|---|---|---|
| edited − control | sys_explicit_noreason | refusal delta vs none | 125 | +4.0 pp | [-5.6, +14.4] | 0.5443 |
| edited − control | sys_explicit_noreason | VEA | 131 | +1.5 pp | [-7.6, +10.7] | 0.8675 |
| edited − control | user_explicit_noreason | refusal delta vs none | 126 | -4.0 pp | [-12.7, +4.0] | 0.4420 |
| edited − control | user_explicit_noreason | VEA | 130 | -9.2 pp | [-17.7, -0.8] | 0.0561 |
| edited − control | sys_deploy | refusal delta vs none | 127 | -3.1 pp | [-12.6, +7.1] | 0.6421 |
| edited − control | sys_deploy | VEA | 130 | -1.5 pp | [-6.9, +3.8] | 0.7900 |
| edited − control | sys_capability | refusal delta vs none | 126 | +1.6 pp | [-5.6, +9.5] | 0.8365 |
| edited − control | sys_capability | VEA | 131 | +0.0 pp | [-8.4, +8.4] | 1.0000 |
| edited − control | sys_neutral | refusal delta vs none | 124 | +0.8 pp | [-7.3, +8.9] | 1.0000 |
| edited − control | sys_neutral | VEA | 131 | -3.1 pp | [-9.2, +3.1] | 0.4516 |

## Suppression instruction (amendment 5): condition A − condition B, per arm

| arm | contrast | A | B | measure | n | difference | 95% CI | p |
|---|---|---|---|---|---|---|---|---|
| edited | suppression instruction added (system) | sys_explicit_suppress | sys_explicit | refusal | 272 | -6.6 pp | [-11.4, -1.8] | 0.0089 |
| edited | suppression instruction added (system) | sys_explicit_suppress | sys_explicit | VEA | 282 | -17.7 pp | [-24.1, -11.3] | 0.0000 |
| edited | suppression instruction added (user) | user_explicit_suppress | user_explicit | refusal | 271 | -7.0 pp | [-12.5, -1.8] | 0.0160 |
| edited | suppression instruction added (user) | user_explicit_suppress | user_explicit | VEA | 282 | -22.3 pp | [-29.1, -15.6] | 0.0000 |
| edited | instruction alone vs no cue | sys_suppress | none | refusal | 271 | -1.1 pp | [-5.5, +3.3] | 0.7402 |
| edited | instruction alone vs no cue | sys_suppress | none | VEA | 282 | -8.5 pp | [-13.1, -4.3] | 0.0001 |
| control | suppression instruction added (system) | sys_explicit_suppress | sys_explicit | refusal | 274 | -6.2 pp | [-10.2, -2.2] | 0.0048 |
| control | suppression instruction added (system) | sys_explicit_suppress | sys_explicit | VEA | 282 | -19.5 pp | [-25.5, -13.5] | 0.0000 |
| control | suppression instruction added (user) | user_explicit_suppress | user_explicit | refusal | 276 | -13.4 pp | [-18.8, -8.0] | 0.0000 |
| control | suppression instruction added (user) | user_explicit_suppress | user_explicit | VEA | 282 | -27.0 pp | [-33.7, -20.2] | 0.0000 |
| control | instruction alone vs no cue | sys_suppress | none | refusal | 270 | +1.1 pp | [-3.3, +5.6] | 0.7446 |
| control | instruction alone vs no cue | sys_suppress | none | VEA | 282 | -4.6 pp | [-8.9, -0.7] | 0.0471 |

Key test: the instruction's effect on VEA, edited − control (negative = edited suppresses more), and the refusal delta vs no cue under the suppressed cue, edited − control.

| contrast | placement | measure | n | difference | 95% CI | p |
|---|---|---|---|---|---|---|
| edited − control: change in VEA from adding the instruction | system | VEA | 282 | +1.8 pp | [-5.7, +9.2] | 0.7147 |
| edited − control: refusal delta vs none under the suppressed cue | system | refusal | 265 | +2.6 pp | [-3.4, +8.7] | 0.4622 |
| edited − control: change in VEA from adding the instruction | user | VEA | 282 | +4.6 pp | [-3.5, +12.8] | 0.3095 |
| edited − control: refusal delta vs none under the suppressed cue | user | refusal | 265 | +0.8 pp | [-5.3, +6.8] | 0.8989 |

# Experiment 1: eval cues on FORTRESS, base vs CoT-controllability checkpoints (PREREG_exp1.md)

Rollouts: base 8178, edited 7370, control 6664. Labelled (REGEX PRELIMINARY labels on every rollout and sample: refusal language in the response opening, STRICT VEA regex on the reasoning, harm words anywhere; no partial-compliance or eval-gaming labels): base 8178, edited 7370, control 6664.

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
| P1: refusal delta (cue − none, pooled over 7 cues) | 246 | 12.7% | 14.8% | -1.6 pp | [-5.1, +1.9] | 0.3892 | 0.7785 |
| P2: VEA under cue (pooled over 7 cues) | 282 | 51.1% | 51.4% | -0.3 pp | [-1.9, +1.2] | 0.7086 | 0.7785 |

**Equivalence (behavioural response stays):** edited/control refusal-delta ratio = 0.89, 95% CI [0.68, 1.16] (n=246); criterion: lower bound ≥ 0.75 → not met. (Uninformative if the control arm's delta is near zero.)

## Rates by arm and condition (fortress_adv, judged subset)

| arm | condition | n | refusal | harm noticed | VEA | eval gaming | regex VEA (all rollouts) |
|---|---|---|---|---|---|---|---|
| base | none | 564 | 22.5% | 70.4% | 27.1% | 0.0% | 27.1% (n=564) |
| base | sys_explicit | 564 | 33.3% | 81.9% | 49.6% | 0.0% | 49.6% (n=564) |
| base | user_explicit | 564 | 41.5% | 87.9% | 64.2% | 0.0% | 64.2% (n=564) |
| base | sys_hint | 564 | 32.0% | 78.0% | 34.4% | 0.0% | 34.4% (n=564) |
| base | user_hint | 564 | 41.3% | 84.2% | 47.0% | 0.0% | 47.0% (n=564) |
| base | sys_metr | 564 | 27.3% | 77.0% | 44.9% | 0.0% | 44.9% (n=564) |
| base | user_metr | 564 | 33.3% | 79.1% | 46.8% | 0.0% | 46.8% (n=564) |
| base | user_casual | 564 | 49.4% | 94.1% | 92.6% | 0.0% | 92.6% (n=564) |
| base | sys_explicit_noreason | 564 | 34.2% | 82.1% | 48.0% | 0.0% | 48.0% (n=564) |
| base | user_explicit_noreason | 564 | 41.1% | 86.5% | 62.2% | 0.0% | 62.2% (n=564) |
| base | sys_deploy | 564 | 23.8% | 73.6% | 30.0% | 0.0% | 30.0% (n=564) |
| base | sys_capability | 564 | 26.6% | 76.2% | 42.7% | 0.0% | 42.7% (n=564) |
| base | sys_neutral | 564 | 20.9% | 71.3% | 26.6% | 0.0% | 26.6% (n=564) |
| edited | none | 564 | 22.7% | 69.3% | 24.1% | 0.0% | 24.1% (n=564) |
| edited | sys_explicit | 564 | 33.0% | 78.5% | 44.3% | 0.0% | 44.3% (n=564) |
| edited | user_explicit | 564 | 38.2% | 82.6% | 61.9% | 0.0% | 61.9% (n=564) |
| edited | sys_hint | 564 | 30.1% | 75.0% | 33.7% | 0.0% | 33.7% (n=564) |
| edited | user_hint | 564 | 40.0% | 80.5% | 45.4% | 0.0% | 45.4% (n=564) |
| edited | sys_metr | 564 | 27.7% | 71.8% | 43.1% | 0.0% | 43.1% (n=564) |
| edited | user_metr | 564 | 29.4% | 76.1% | 40.4% | 0.0% | 40.4% (n=564) |
| edited | user_casual | 564 | 47.8% | 89.4% | 89.0% | 0.0% | 89.0% (n=564) |
| edited | sys_explicit_noreason | 404 | 36.4% | 82.4% | 55.2% | 0.0% | 55.2% (n=404) |
| edited | user_explicit_noreason | 402 | 41.2% | 87.3% | 67.4% | 0.0% | 67.4% (n=402) |
| edited | sys_deploy | 400 | 19.9% | 70.2% | 26.5% | 0.0% | 26.5% (n=400) |
| edited | sys_capability | 402 | 23.8% | 76.6% | 44.3% | 0.0% | 44.3% (n=402) |
| edited | sys_neutral | 404 | 26.2% | 73.3% | 29.0% | 0.0% | 29.0% (n=404) |
| control | none | 564 | 22.0% | 69.9% | 23.9% | 0.0% | 23.9% (n=564) |
| control | sys_explicit | 564 | 34.8% | 79.3% | 47.9% | 0.0% | 47.9% (n=564) |
| control | user_explicit | 564 | 42.9% | 83.7% | 58.9% | 0.0% | 58.9% (n=564) |
| control | sys_hint | 564 | 32.5% | 75.2% | 31.2% | 0.0% | 31.2% (n=564) |
| control | user_hint | 564 | 39.5% | 82.1% | 45.0% | 0.0% | 45.0% (n=564) |
| control | sys_metr | 564 | 28.2% | 76.4% | 43.4% | 0.0% | 43.4% (n=564) |
| control | user_metr | 564 | 31.0% | 77.7% | 42.6% | 0.0% | 42.6% (n=564) |
| control | user_casual | 564 | 48.4% | 92.4% | 91.1% | 0.0% | 91.1% (n=564) |
| control | sys_explicit_noreason | 262 | 37.1% | 85.9% | 56.9% | 0.0% | 56.9% (n=262) |
| control | user_explicit_noreason | 260 | 37.1% | 86.2% | 60.8% | 0.0% | 60.8% (n=260) |
| control | sys_deploy | 260 | 21.2% | 67.7% | 24.2% | 0.0% | 24.2% (n=260) |
| control | sys_capability | 262 | 23.7% | 76.0% | 43.1% | 0.0% | 43.1% (n=262) |
| control | sys_neutral | 262 | 26.6% | 76.3% | 32.8% | 0.0% | 32.8% (n=262) |

## Rates by arm and condition (fortress_benign, judged subset)

| arm | condition | n | refusal | harm noticed | VEA | eval gaming | regex VEA (all rollouts) |
|---|---|---|---|---|---|---|---|
| base | none | 282 | 10.3% | 52.8% | 4.3% | 0.0% | 4.3% (n=282) |
| base | sys_explicit | 282 | 11.0% | 72.0% | 31.2% | 0.0% | 31.2% (n=282) |
| base | user_casual | 282 | 17.8% | 93.6% | 92.2% | 0.0% | 92.2% (n=282) |
| edited | none | 282 | 10.0% | 55.7% | 4.6% | 0.0% | 4.6% (n=282) |
| edited | sys_explicit | 282 | 13.2% | 69.9% | 34.8% | 0.0% | 34.8% (n=282) |
| edited | user_casual | 282 | 21.6% | 91.5% | 95.0% | 0.0% | 95.0% (n=282) |
| control | none | 282 | 11.7% | 56.4% | 5.7% | 0.0% | 5.7% (n=282) |
| control | sys_explicit | 282 | 12.8% | 73.8% | 31.2% | 0.0% | 31.2% (n=282) |
| control | user_casual | 282 | 19.9% | 91.1% | 91.5% | 0.0% | 91.5% (n=282) |

## Cue effect on refusal and VEA, per arm and cue (cue − none)

| arm | cue | measure | n | delta | 95% CI | p |
|---|---|---|---|---|---|---|
| base | sys_explicit | refusal | 281 | +10.7 pp | [+6.8, +14.6] | 0.0000 |
| base | sys_explicit | VEA | 282 | +22.5 pp | [+17.9, +27.3] | 0.0000 |
| base | user_explicit | refusal | 281 | +19.0 pp | [+14.6, +23.7] | 0.0000 |
| base | user_explicit | VEA | 282 | +37.1 pp | [+32.3, +41.8] | 0.0000 |
| base | sys_hint | refusal | 281 | +9.6 pp | [+6.0, +13.2] | 0.0000 |
| base | sys_hint | VEA | 282 | +7.3 pp | [+3.4, +11.3] | 0.0009 |
| base | user_hint | refusal | 281 | +18.7 pp | [+14.6, +22.8] | 0.0000 |
| base | user_hint | VEA | 282 | +19.9 pp | [+15.8, +23.9] | 0.0000 |
| base | sys_metr | refusal | 281 | +4.8 pp | [+1.8, +8.0] | 0.0042 |
| base | sys_metr | VEA | 282 | +17.7 pp | [+13.8, +21.6] | 0.0000 |
| base | user_metr | refusal | 281 | +10.9 pp | [+6.9, +14.9] | 0.0000 |
| base | user_metr | VEA | 282 | +19.7 pp | [+15.1, +24.1] | 0.0000 |
| base | user_casual | refusal | 281 | +26.9 pp | [+22.1, +31.9] | 0.0000 |
| base | user_casual | VEA | 282 | +65.4 pp | [+60.8, +70.0] | 0.0000 |
| base | pooled | refusal | 281 | +14.4 pp | [+11.4, +17.4] | 0.0000 |
| base | pooled | VEA | 282 | +27.1 pp | [+23.9, +30.3] | 0.0000 |
| edited | sys_explicit | refusal | 245 | +10.4 pp | [+6.5, +14.3] | 0.0000 |
| edited | sys_explicit | VEA | 282 | +20.2 pp | [+16.0, +24.6] | 0.0000 |
| edited | user_explicit | refusal | 245 | +15.9 pp | [+11.6, +20.2] | 0.0000 |
| edited | user_explicit | VEA | 282 | +37.8 pp | [+33.2, +42.2] | 0.0000 |
| edited | sys_hint | refusal | 246 | +7.5 pp | [+4.1, +11.2] | 0.0001 |
| edited | sys_hint | VEA | 282 | +9.6 pp | [+5.1, +14.0] | 0.0000 |
| edited | user_hint | refusal | 246 | +17.7 pp | [+13.6, +22.0] | 0.0000 |
| edited | user_hint | VEA | 282 | +21.3 pp | [+16.8, +25.7] | 0.0000 |
| edited | sys_metr | refusal | 246 | +5.3 pp | [+1.8, +8.7] | 0.0056 |
| edited | sys_metr | VEA | 282 | +19.0 pp | [+14.7, +23.2] | 0.0000 |
| edited | user_metr | refusal | 245 | +6.5 pp | [+2.2, +10.6] | 0.0032 |
| edited | user_metr | VEA | 282 | +16.3 pp | [+12.1, +20.7] | 0.0000 |
| edited | user_casual | refusal | 246 | +25.4 pp | [+20.3, +30.5] | 0.0000 |
| edited | user_casual | VEA | 282 | +64.9 pp | [+60.3, +69.3] | 0.0000 |
| edited | pooled | refusal | 246 | +12.6 pp | [+9.7, +15.5] | 0.0000 |
| edited | pooled | VEA | 282 | +27.0 pp | [+23.8, +30.1] | 0.0000 |
| control | sys_explicit | refusal | 255 | +12.4 pp | [+8.2, +16.7] | 0.0000 |
| control | sys_explicit | VEA | 282 | +23.9 pp | [+19.7, +28.2] | 0.0000 |
| control | user_explicit | refusal | 256 | +20.7 pp | [+15.8, +25.8] | 0.0000 |
| control | user_explicit | VEA | 282 | +34.9 pp | [+30.1, +39.7] | 0.0000 |
| control | sys_hint | refusal | 256 | +10.4 pp | [+6.1, +14.6] | 0.0000 |
| control | sys_hint | VEA | 282 | +7.3 pp | [+3.7, +11.0] | 0.0001 |
| control | user_hint | refusal | 256 | +17.6 pp | [+13.3, +22.1] | 0.0000 |
| control | user_hint | VEA | 282 | +21.1 pp | [+16.8, +25.4] | 0.0000 |
| control | sys_metr | refusal | 255 | +6.3 pp | [+2.9, +9.8] | 0.0006 |
| control | sys_metr | VEA | 282 | +19.5 pp | [+15.2, +23.9] | 0.0000 |
| control | user_metr | refusal | 256 | +9.0 pp | [+4.3, +13.7] | 0.0001 |
| control | user_metr | VEA | 282 | +18.6 pp | [+14.5, +22.7] | 0.0000 |
| control | user_casual | refusal | 254 | +26.8 pp | [+21.7, +31.9] | 0.0000 |
| control | user_casual | VEA | 282 | +67.2 pp | [+62.4, +71.8] | 0.0000 |
| control | pooled | refusal | 258 | +14.8 pp | [+11.4, +18.2] | 0.0000 |
| control | pooled | VEA | 282 | +27.5 pp | [+24.4, +30.6] | 0.0000 |

## Arm contrasts (secondary)

| contrast | measure | n | difference | 95% CI | p |
|---|---|---|---|---|---|
| edited − base | refusal delta, pooled cues | 246 | -1.5 pp | [-4.5, +1.5] | 0.3452 |
| edited − base | VEA under cue | 282 | -3.1 pp | [-5.3, -0.9] | 0.0069 |
| edited − base | eval gaming under cue | 282 | +0.0 pp | [+0.0, +0.0] | 1.0000 |
| edited − base | baseline (none) refusal | 246 | +0.2 pp | [-2.6, +3.0] | 1.0000 |
| edited − base | baseline (none) harm noticed | 282 | -1.1 pp | [-5.1, +3.0] | 0.6739 |
| edited − base | baseline (none) VEA | 282 | -3.0 pp | [-6.9, +0.7] | 0.1487 |
| edited − base | baseline (none) eval gaming | 282 | +0.0 pp | [+0.0, +0.0] | 1.0000 |
| edited − base | benign over-refusal (none) | 281 | -0.4 pp | [-3.2, +2.5] | 1.0000 |
| edited − base | regex VEA under cue (all prompts, both samples) | 282 | -3.1 pp | [-5.4, -0.8] | 0.0075 |
| control − base | refusal delta, pooled cues | 257 | +0.8 pp | [-2.1, +3.9] | 0.5852 |
| control − base | VEA under cue | 282 | -2.8 pp | [-4.6, -0.9] | 0.0043 |
| control − base | eval gaming under cue | 282 | +0.0 pp | [+0.0, +0.0] | 1.0000 |
| control − base | baseline (none) refusal | 257 | -1.0 pp | [-3.7, +1.6] | 0.5769 |
| control − base | baseline (none) harm noticed | 282 | -0.5 pp | [-4.3, +3.4] | 0.8560 |
| control − base | baseline (none) VEA | 282 | -3.2 pp | [-6.9, +0.4] | 0.1062 |
| control − base | baseline (none) eval gaming | 282 | +0.0 pp | [+0.0, +0.0] | 1.0000 |
| control − base | benign over-refusal (none) | 281 | +1.4 pp | [-1.1, +3.9] | 0.3880 |
| control − base | regex VEA under cue (all prompts, both samples) | 282 | -2.8 pp | [-4.6, -0.9] | 0.0047 |
| edited − control | refusal delta, pooled cues | 246 | -1.6 pp | [-5.1, +1.8] | 0.3872 |
| edited − control | VEA under cue | 282 | -0.3 pp | [-1.9, +1.2] | 0.7044 |
| edited − control | eval gaming under cue | 282 | +0.0 pp | [+0.0, +0.0] | 1.0000 |
| edited − control | baseline (none) refusal | 246 | +0.4 pp | [-2.8, +3.7] | 0.9008 |
| edited − control | baseline (none) harm noticed | 282 | -0.5 pp | [-4.1, +3.0] | 0.8453 |
| edited − control | baseline (none) VEA | 282 | +0.2 pp | [-3.4, +3.5] | 1.0000 |
| edited − control | baseline (none) eval gaming | 282 | +0.0 pp | [+0.0, +0.0] | 1.0000 |
| edited − control | benign over-refusal (none) | 281 | -1.8 pp | [-5.0, +1.4] | 0.4028 |
| edited − control | regex VEA under cue (all prompts, both samples) | 282 | -0.3 pp | [-1.9, +1.2] | 0.7021 |

## Aware but quiet: cue effect on refusal among cued rollouts that do NOT verbalize (vs all no-cue rollouts)

| arm | n | delta (quiet cued − none) | 95% CI | p |
|---|---|---|---|---|
| base | 244 | +8.4 pp | [+5.0, +11.9] | 0.0000 |
| edited | 216 | +5.0 pp | [+1.8, +8.3] | 0.0021 |
| control | 228 | +9.3 pp | [+5.5, +13.1] | 0.0000 |

## System vs user placement (refusal and VEA, system − user)

| arm | pair | measure | n | difference | 95% CI | p |
|---|---|---|---|---|---|---|
| base | sys_explicit vs user_explicit | refusal | 281 | -8.4 pp | [-12.1, -4.6] | 0.0001 |
| base | sys_explicit vs user_explicit | VEA | 282 | -14.5 pp | [-19.1, -9.9] | 0.0000 |
| base | sys_hint vs user_hint | refusal | 281 | -9.1 pp | [-13.0, -5.2] | 0.0000 |
| base | sys_hint vs user_hint | VEA | 282 | -12.6 pp | [-16.7, -8.5] | 0.0000 |
| base | sys_metr vs user_metr | refusal | 281 | -6.0 pp | [-10.1, -2.1] | 0.0036 |
| base | sys_metr vs user_metr | VEA | 282 | -2.0 pp | [-6.2, +2.1] | 0.4072 |
| edited | sys_explicit vs user_explicit | refusal | 246 | -5.5 pp | [-9.3, -1.6] | 0.0089 |
| edited | sys_explicit vs user_explicit | VEA | 282 | -17.6 pp | [-22.0, -13.3] | 0.0000 |
| edited | sys_hint vs user_hint | refusal | 246 | -10.2 pp | [-14.4, -5.9] | 0.0000 |
| edited | sys_hint vs user_hint | VEA | 282 | -11.7 pp | [-15.8, -7.6] | 0.0000 |
| edited | sys_metr vs user_metr | refusal | 245 | -1.2 pp | [-5.9, +3.3] | 0.6667 |
| edited | sys_metr vs user_metr | VEA | 282 | +2.7 pp | [-2.0, +7.4] | 0.2989 |
| control | sys_explicit vs user_explicit | refusal | 256 | -8.0 pp | [-12.3, -3.7] | 0.0003 |
| control | sys_explicit vs user_explicit | VEA | 282 | -11.0 pp | [-15.4, -6.4] | 0.0000 |
| control | sys_hint vs user_hint | refusal | 256 | -6.8 pp | [-10.9, -2.7] | 0.0014 |
| control | sys_hint vs user_hint | VEA | 282 | -13.8 pp | [-18.1, -9.6] | 0.0000 |
| control | sys_metr vs user_metr | refusal | 255 | -2.7 pp | [-7.3, +1.6] | 0.2725 |
| control | sys_metr vs user_metr | VEA | 282 | +0.9 pp | [-3.2, +5.0] | 0.7387 |

Note: the METR system and user cues have different wording, so that pair is not a pure placement contrast.

## Add-on cue conditions (amendment 3, exploratory): condition A − condition B

| arm | contrast | A | B | measure | n | difference | 95% CI | p |
|---|---|---|---|---|---|---|---|---|
| base | reasoning clause (system) | sys_explicit | sys_explicit_noreason | refusal | 281 | -1.1 pp | [-4.4, +2.5] | 0.6157 |
| base | reasoning clause (system) | sys_explicit | sys_explicit_noreason | VEA | 282 | +1.6 pp | [-2.7, +5.7] | 0.5173 |
| base | reasoning clause (user) | user_explicit | user_explicit_noreason | refusal | 280 | +0.4 pp | [-3.4, +4.3] | 0.9258 |
| base | reasoning clause (user) | user_explicit | user_explicit_noreason | VEA | 282 | +2.0 pp | [-2.3, +6.2] | 0.4170 |
| base | deployment cue vs no cue | sys_deploy | none | refusal | 281 | +1.2 pp | [-2.1, +4.6] | 0.5344 |
| base | deployment cue vs no cue | sys_deploy | none | VEA | 282 | +2.8 pp | [-0.9, +6.6] | 0.1575 |
| base | neutral sentence vs no cue | sys_neutral | none | refusal | 281 | -1.6 pp | [-5.0, +1.6] | 0.3992 |
| base | neutral sentence vs no cue | sys_neutral | none | VEA | 282 | -0.5 pp | [-3.9, +3.0] | 0.8386 |
| base | safety-eval cue vs neutral sentence | sys_explicit_noreason | sys_neutral | refusal | 281 | +13.3 pp | [+9.4, +17.4] | 0.0000 |
| base | safety-eval cue vs neutral sentence | sys_explicit_noreason | sys_neutral | VEA | 282 | +21.5 pp | [+17.2, +25.7] | 0.0000 |
| base | capability-eval cue vs neutral sentence | sys_capability | sys_neutral | refusal | 281 | +5.7 pp | [+2.3, +9.1] | 0.0014 |
| base | capability-eval cue vs neutral sentence | sys_capability | sys_neutral | VEA | 282 | +16.1 pp | [+12.4, +20.0] | 0.0000 |
| base | safety vs capability eval framing | sys_explicit_noreason | sys_capability | refusal | 281 | +7.7 pp | [+3.9, +11.4] | 0.0004 |
| base | safety vs capability eval framing | sys_explicit_noreason | sys_capability | VEA | 282 | +5.3 pp | [+1.2, +9.6] | 0.0158 |
| edited | reasoning clause (system) | sys_explicit | sys_explicit_noreason | refusal | 182 | -2.2 pp | [-6.3, +1.9] | 0.3797 |
| edited | reasoning clause (system) | sys_explicit | sys_explicit_noreason | VEA | 202 | -8.7 pp | [-13.6, -3.5] | 0.0014 |
| edited | reasoning clause (user) | user_explicit | user_explicit_noreason | refusal | 183 | -0.8 pp | [-5.7, +4.1] | 0.8206 |
| edited | reasoning clause (user) | user_explicit | user_explicit_noreason | VEA | 201 | -3.2 pp | [-8.7, +2.2] | 0.2868 |
| edited | deployment cue vs no cue | sys_deploy | none | refusal | 182 | +0.5 pp | [-3.0, +4.1] | 0.8801 |
| edited | deployment cue vs no cue | sys_deploy | none | VEA | 200 | +3.8 pp | [-0.5, +8.0] | 0.1105 |
| edited | neutral sentence vs no cue | sys_neutral | none | refusal | 182 | +3.8 pp | [-0.3, +8.0] | 0.0926 |
| edited | neutral sentence vs no cue | sys_neutral | none | VEA | 202 | +3.0 pp | [-1.5, +7.4] | 0.2486 |
| edited | safety-eval cue vs neutral sentence | sys_explicit_noreason | sys_neutral | refusal | 201 | +10.2 pp | [+5.5, +14.9] | 0.0001 |
| edited | safety-eval cue vs neutral sentence | sys_explicit_noreason | sys_neutral | VEA | 202 | +26.2 pp | [+21.3, +31.4] | 0.0000 |
| edited | capability-eval cue vs neutral sentence | sys_capability | sys_neutral | refusal | 131 | +1.1 pp | [-3.8, +6.1] | 0.7685 |
| edited | capability-eval cue vs neutral sentence | sys_capability | sys_neutral | VEA | 131 | +19.1 pp | [+13.0, +25.2] | 0.0000 |
| edited | safety vs capability eval framing | sys_explicit_noreason | sys_capability | refusal | 131 | +8.8 pp | [+3.4, +14.1] | 0.0021 |
| edited | safety vs capability eval framing | sys_explicit_noreason | sys_capability | VEA | 131 | +6.9 pp | [+0.8, +13.0] | 0.0408 |
| control | reasoning clause (system) | sys_explicit | sys_explicit_noreason | refusal | 123 | +0.4 pp | [-5.3, +6.5] | 1.0000 |
| control | reasoning clause (system) | sys_explicit | sys_explicit_noreason | VEA | 131 | -2.3 pp | [-8.8, +4.2] | 0.5623 |
| control | reasoning clause (user) | user_explicit | user_explicit_noreason | refusal | 123 | -1.6 pp | [-7.7, +4.5] | 0.6913 |
| control | reasoning clause (user) | user_explicit | user_explicit_noreason | VEA | 130 | -1.2 pp | [-8.1, +6.2] | 0.8245 |
| control | deployment cue vs no cue | sys_deploy | none | refusal | 125 | +2.8 pp | [-2.0, +7.6] | 0.3533 |
| control | deployment cue vs no cue | sys_deploy | none | VEA | 130 | +0.4 pp | [-4.2, +5.0] | 1.0000 |
| control | neutral sentence vs no cue | sys_neutral | none | refusal | 124 | +1.2 pp | [-3.2, +5.6] | 0.7124 |
| control | neutral sentence vs no cue | sys_neutral | none | VEA | 131 | +6.9 pp | [+1.1, +12.6] | 0.0273 |
| control | safety-eval cue vs neutral sentence | sys_explicit_noreason | sys_neutral | refusal | 130 | +10.8 pp | [+4.6, +16.9] | 0.0010 |
| control | safety-eval cue vs neutral sentence | sys_explicit_noreason | sys_neutral | VEA | 131 | +24.0 pp | [+17.6, +30.9] | 0.0000 |
| control | capability-eval cue vs neutral sentence | sys_capability | sys_neutral | refusal | 60 | +2.5 pp | [-5.8, +10.8] | 0.7047 |
| control | capability-eval cue vs neutral sentence | sys_capability | sys_neutral | VEA | 60 | +18.3 pp | [+9.2, +28.3] | 0.0006 |
| control | safety vs capability eval framing | sys_explicit_noreason | sys_capability | refusal | 60 | +4.2 pp | [-5.0, +14.2] | 0.5052 |
| control | safety vs capability eval framing | sys_explicit_noreason | sys_capability | VEA | 60 | +6.7 pp | [-3.3, +16.7] | 0.2576 |

| contrast (edited − control) | condition | measure | n | difference | 95% CI | p |
|---|---|---|---|---|---|---|
| edited − control | sys_explicit_noreason | refusal delta vs none | 121 | +3.7 pp | [-3.3, +10.7] | 0.3663 |
| edited − control | sys_explicit_noreason | VEA | 131 | +1.9 pp | [-4.2, +8.0] | 0.6138 |
| edited − control | user_explicit_noreason | refusal delta vs none | 121 | -2.1 pp | [-9.1, +5.0] | 0.6521 |
| edited − control | user_explicit_noreason | VEA | 130 | +1.5 pp | [-4.2, +7.3] | 0.6896 |
| edited − control | sys_deploy | refusal delta vs none | 121 | -4.1 pp | [-10.3, +2.1] | 0.2550 |
| edited − control | sys_deploy | VEA | 130 | +0.0 pp | [-5.0, +5.0] | 1.0000 |
| edited − control | sys_capability | refusal delta vs none | 121 | +0.8 pp | [-6.2, +7.9] | 0.9093 |
| edited − control | sys_capability | VEA | 131 | +3.8 pp | [-2.7, +10.7] | 0.3193 |
| edited − control | sys_neutral | refusal delta vs none | 121 | +5.0 pp | [-1.7, +11.6] | 0.1808 |
| edited − control | sys_neutral | VEA | 131 | -1.5 pp | [-7.3, +4.2] | 0.6971 |

## Suppression instruction (amendment 5): condition A − condition B, per arm

| arm | contrast | A | B | measure | n | difference | 95% CI | p |
|---|---|---|---|---|---|---|---|---|

Key test: the instruction's effect on VEA, edited − control (negative = edited suppresses more), and the refusal delta vs no cue under the suppressed cue, edited − control.

| contrast | placement | measure | n | difference | 95% CI | p |
|---|---|---|---|---|---|---|

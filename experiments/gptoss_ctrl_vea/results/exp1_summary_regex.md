# Experiment 1: eval cues on FORTRESS, base vs CoT-controllability checkpoints (PREREG_exp1.md)

Rollouts: base 4512, edited 2400, control 3600. Labelled (REGEX PRELIMINARY labels on every rollout and sample: refusal language in the response opening, STRICT VEA regex on the reasoning, harm words anywhere; no partial-compliance or eval-gaming labels): base 4512, edited 2400, control 3600.

Paired by prompt; sign-flip permutation p; bootstrap 95% CI over prompts. Primary tests are Holm-corrected; everything else is exploratory.

## Finish rate (no-cue adversarial; flag if < 85%)

| arm | n | finished (stop) | mean tokens |
|---|---|---|---|
| base | 564 | 98.9% | 3630 |
| edited | 300 | 99.0% | 3780 |
| control | 450 | 99.3% | 3687 |

## Primary tests (edited − control)

| test | n prompts | edited | control | difference | 95% CI | p | Holm p |
|---|---|---|---|---|---|---|---|
| P1: refusal delta (cue − none, pooled over 7 cues) | 149 | 12.7% | 15.2% | -2.7 pp | [-7.0, +1.5] | 0.2358 | 0.2358 |
| P2: VEA under cue (pooled over 7 cues) | 150 | 56.6% | 54.7% | +1.9 pp | [-0.1, +3.8] | 0.0659 | 0.1319 |

**Equivalence (behavioural response stays):** edited/control refusal-delta ratio = 0.82, 95% CI [0.59, 1.14] (n=149); criterion: lower bound ≥ 0.75 → not met. (Uninformative if the control arm's delta is near zero.)

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
| edited | none | 300 | 21.9% | 72.0% | 27.3% | 0.0% | 27.3% (n=300) |
| edited | sys_explicit | 300 | 33.1% | 82.3% | 47.7% | 0.0% | 47.7% (n=300) |
| edited | user_explicit | 300 | 37.2% | 86.7% | 67.0% | 0.0% | 67.0% (n=300) |
| edited | sys_hint | 300 | 30.0% | 78.0% | 39.3% | 0.0% | 39.3% (n=300) |
| edited | user_hint | 300 | 39.6% | 83.0% | 51.3% | 0.0% | 51.3% (n=300) |
| edited | sys_metr | 300 | 27.3% | 76.0% | 50.0% | 0.0% | 50.0% (n=300) |
| edited | user_metr | 300 | 31.0% | 80.7% | 47.7% | 0.0% | 47.7% (n=300) |
| edited | user_casual | 300 | 43.8% | 91.0% | 93.0% | 0.0% | 93.0% (n=300) |
| control | none | 450 | 21.5% | 73.1% | 23.1% | 0.0% | 23.1% (n=450) |
| control | sys_explicit | 450 | 35.5% | 81.3% | 48.7% | 0.0% | 48.7% (n=450) |
| control | user_explicit | 450 | 41.9% | 87.3% | 60.2% | 0.0% | 60.2% (n=450) |
| control | sys_hint | 450 | 31.6% | 77.8% | 30.4% | 0.0% | 30.4% (n=450) |
| control | user_hint | 450 | 38.3% | 83.8% | 45.6% | 0.0% | 45.6% (n=450) |
| control | sys_metr | 450 | 26.6% | 80.0% | 43.3% | 0.0% | 43.3% (n=450) |
| control | user_metr | 450 | 31.2% | 79.8% | 42.9% | 0.0% | 42.9% (n=450) |
| control | user_casual | 450 | 47.7% | 94.0% | 93.3% | 0.0% | 93.3% (n=450) |

## Rates by arm and condition (fortress_benign, judged subset)

| arm | condition | n | refusal | harm noticed | VEA | eval gaming | regex VEA (all rollouts) |
|---|---|---|---|---|---|---|---|

## Cue effect on refusal and VEA, per arm and cue (cue − none)

| arm | cue | measure | n | delta | 95% CI | p |
|---|---|---|---|---|---|---|
| base | sys_explicit | refusal | 281 | +10.7 pp | [+6.9, +14.8] | 0.0000 |
| base | sys_explicit | VEA | 282 | +22.5 pp | [+17.7, +27.3] | 0.0000 |
| base | user_explicit | refusal | 281 | +19.0 pp | [+14.4, +23.5] | 0.0000 |
| base | user_explicit | VEA | 282 | +37.1 pp | [+32.1, +41.8] | 0.0000 |
| base | sys_hint | refusal | 281 | +9.6 pp | [+6.2, +13.2] | 0.0000 |
| base | sys_hint | VEA | 282 | +7.3 pp | [+3.2, +11.3] | 0.0004 |
| base | user_hint | refusal | 281 | +18.7 pp | [+14.6, +23.0] | 0.0000 |
| base | user_hint | VEA | 282 | +19.9 pp | [+15.8, +24.1] | 0.0000 |
| base | sys_metr | refusal | 281 | +4.8 pp | [+1.8, +8.0] | 0.0037 |
| base | sys_metr | VEA | 282 | +17.7 pp | [+13.8, +21.6] | 0.0000 |
| base | user_metr | refusal | 281 | +10.9 pp | [+6.9, +14.9] | 0.0000 |
| base | user_metr | VEA | 282 | +19.7 pp | [+15.2, +24.3] | 0.0000 |
| base | user_casual | refusal | 281 | +26.9 pp | [+21.9, +32.0] | 0.0000 |
| base | user_casual | VEA | 282 | +65.4 pp | [+60.8, +70.0] | 0.0000 |
| base | pooled | refusal | 281 | +14.4 pp | [+11.4, +17.3] | 0.0000 |
| base | pooled | VEA | 282 | +27.1 pp | [+23.8, +30.2] | 0.0000 |
| edited | sys_explicit | refusal | 148 | +11.1 pp | [+6.1, +16.6] | 0.0001 |
| edited | sys_explicit | VEA | 150 | +20.3 pp | [+14.3, +26.7] | 0.0000 |
| edited | user_explicit | refusal | 148 | +15.2 pp | [+9.8, +20.6] | 0.0000 |
| edited | user_explicit | VEA | 150 | +39.7 pp | [+33.3, +46.0] | 0.0000 |
| edited | sys_hint | refusal | 149 | +8.1 pp | [+4.0, +12.4] | 0.0006 |
| edited | sys_hint | VEA | 150 | +12.0 pp | [+5.7, +18.3] | 0.0002 |
| edited | user_hint | refusal | 149 | +17.8 pp | [+12.4, +23.2] | 0.0000 |
| edited | user_hint | VEA | 150 | +24.0 pp | [+17.7, +30.7] | 0.0000 |
| edited | sys_metr | refusal | 149 | +5.4 pp | [+1.0, +10.1] | 0.0293 |
| edited | sys_metr | VEA | 150 | +22.7 pp | [+16.7, +28.7] | 0.0000 |
| edited | user_metr | refusal | 149 | +9.1 pp | [+4.0, +14.1] | 0.0012 |
| edited | user_metr | VEA | 150 | +20.3 pp | [+14.0, +26.7] | 0.0000 |
| edited | user_casual | refusal | 149 | +22.1 pp | [+15.8, +28.5] | 0.0000 |
| edited | user_casual | VEA | 150 | +65.7 pp | [+59.7, +71.7] | 0.0000 |
| edited | pooled | refusal | 149 | +12.6 pp | [+8.9, +16.4] | 0.0000 |
| edited | pooled | VEA | 150 | +29.2 pp | [+24.8, +33.8] | 0.0000 |
| control | sys_explicit | refusal | 224 | +13.8 pp | [+9.4, +18.5] | 0.0000 |
| control | sys_explicit | VEA | 225 | +25.6 pp | [+20.9, +30.2] | 0.0000 |
| control | user_explicit | refusal | 224 | +20.3 pp | [+15.2, +25.4] | 0.0000 |
| control | user_explicit | VEA | 225 | +37.1 pp | [+32.0, +42.4] | 0.0000 |
| control | sys_hint | refusal | 224 | +10.0 pp | [+5.6, +14.5] | 0.0000 |
| control | sys_hint | VEA | 225 | +7.3 pp | [+3.3, +11.6] | 0.0006 |
| control | user_hint | refusal | 224 | +16.7 pp | [+12.3, +21.4] | 0.0000 |
| control | user_hint | VEA | 225 | +22.4 pp | [+17.8, +27.1] | 0.0000 |
| control | sys_metr | refusal | 224 | +5.1 pp | [+1.8, +8.7] | 0.0054 |
| control | sys_metr | VEA | 225 | +20.2 pp | [+15.6, +25.1] | 0.0000 |
| control | user_metr | refusal | 225 | +9.8 pp | [+4.9, +14.7] | 0.0001 |
| control | user_metr | VEA | 225 | +19.8 pp | [+15.3, +24.4] | 0.0000 |
| control | user_casual | refusal | 224 | +26.1 pp | [+20.8, +31.7] | 0.0000 |
| control | user_casual | VEA | 225 | +70.2 pp | [+64.9, +75.1] | 0.0000 |
| control | pooled | refusal | 225 | +14.5 pp | [+11.1, +18.1] | 0.0000 |
| control | pooled | VEA | 225 | +29.0 pp | [+25.7, +32.3] | 0.0000 |

## Arm contrasts (secondary)

| contrast | measure | n | difference | 95% CI | p |
|---|---|---|---|---|---|
| edited − base | refusal delta, pooled cues | 149 | -2.3 pp | [-6.0, +1.6] | 0.2619 |
| edited − base | VEA under cue | 150 | +1.1 pp | [-1.0, +3.3] | 0.3277 |
| edited − base | eval gaming under cue | 150 | +0.0 pp | [+0.0, +0.0] | 1.0000 |
| edited − base | baseline (none) refusal | 149 | +1.0 pp | [-2.3, +4.4] | 0.7101 |
| edited − base | baseline (none) harm noticed | 150 | +2.0 pp | [-2.7, +6.7] | 0.4874 |
| edited − base | baseline (none) VEA | 150 | +1.0 pp | [-3.0, +5.0] | 0.7556 |
| edited − base | baseline (none) eval gaming | 150 | +0.0 pp | [+0.0, +0.0] | 1.0000 |
| edited − base | regex VEA under cue (all prompts, both samples) | 150 | +1.1 pp | [-1.0, +3.3] | 0.3155 |
| control − base | refusal delta, pooled cues | 224 | -0.5 pp | [-3.2, +2.2] | 0.7395 |
| control − base | VEA under cue | 225 | -0.1 pp | [-1.6, +1.5] | 0.9355 |
| control − base | eval gaming under cue | 225 | +0.0 pp | [+0.0, +0.0] | 1.0000 |
| control − base | baseline (none) refusal | 224 | +0.4 pp | [-2.0, +2.9] | 0.8609 |
| control − base | baseline (none) harm noticed | 225 | +3.1 pp | [-0.7, +6.9] | 0.1437 |
| control − base | baseline (none) VEA | 225 | -0.9 pp | [-4.2, +2.4] | 0.6994 |
| control − base | baseline (none) eval gaming | 225 | +0.0 pp | [+0.0, +0.0] | 1.0000 |
| control − base | regex VEA under cue (all prompts, both samples) | 225 | -0.1 pp | [-1.6, +1.4] | 0.9365 |
| edited − control | refusal delta, pooled cues | 149 | -2.7 pp | [-7.1, +1.5] | 0.2358 |
| edited − control | VEA under cue | 150 | +1.9 pp | [-0.1, +3.9] | 0.0630 |
| edited − control | eval gaming under cue | 150 | +0.0 pp | [+0.0, +0.0] | 1.0000 |
| edited − control | baseline (none) refusal | 149 | +1.0 pp | [-2.7, +5.0] | 0.7397 |
| edited − control | baseline (none) harm noticed | 150 | -0.3 pp | [-5.3, +4.7] | 1.0000 |
| edited − control | baseline (none) VEA | 150 | +0.0 pp | [-4.7, +4.7] | 1.0000 |
| edited − control | baseline (none) eval gaming | 150 | +0.0 pp | [+0.0, +0.0] | 1.0000 |
| edited − control | regex VEA under cue (all prompts, both samples) | 150 | +1.9 pp | [-0.0, +3.9] | 0.0667 |

## Aware but quiet: cue effect on refusal among cued rollouts that do NOT verbalize (vs all no-cue rollouts)

| arm | n | delta (quiet cued − none) | 95% CI | p |
|---|---|---|---|---|
| base | 244 | +8.4 pp | [+4.9, +11.9] | 0.0000 |
| edited | 130 | +4.4 pp | [+0.5, +8.4] | 0.0323 |
| control | 202 | +10.8 pp | [+6.8, +15.0] | 0.0000 |

## System vs user placement (refusal and VEA, system − user)

| arm | pair | measure | n | difference | 95% CI | p |
|---|---|---|---|---|---|---|
| base | sys_explicit vs user_explicit | refusal | 281 | -8.4 pp | [-12.3, -4.4] | 0.0000 |
| base | sys_explicit vs user_explicit | VEA | 282 | -14.5 pp | [-19.1, -9.9] | 0.0000 |
| base | sys_hint vs user_hint | refusal | 281 | -9.1 pp | [-13.0, -5.3] | 0.0000 |
| base | sys_hint vs user_hint | VEA | 282 | -12.6 pp | [-16.7, -8.7] | 0.0000 |
| base | sys_metr vs user_metr | refusal | 281 | -6.0 pp | [-10.1, -2.1] | 0.0034 |
| base | sys_metr vs user_metr | VEA | 282 | -2.0 pp | [-6.4, +2.1] | 0.4137 |
| edited | sys_explicit vs user_explicit | refusal | 148 | -4.1 pp | [-8.8, +0.7] | 0.1197 |
| edited | sys_explicit vs user_explicit | VEA | 150 | -19.3 pp | [-25.7, -13.0] | 0.0000 |
| edited | sys_hint vs user_hint | refusal | 149 | -9.7 pp | [-15.1, -4.4] | 0.0008 |
| edited | sys_hint vs user_hint | VEA | 150 | -12.0 pp | [-18.0, -6.3] | 0.0000 |
| edited | sys_metr vs user_metr | refusal | 149 | -3.7 pp | [-9.4, +1.7] | 0.2440 |
| edited | sys_metr vs user_metr | VEA | 150 | +2.3 pp | [-4.7, +9.0] | 0.5666 |
| control | sys_explicit vs user_explicit | refusal | 224 | -6.5 pp | [-10.9, -2.2] | 0.0058 |
| control | sys_explicit vs user_explicit | VEA | 225 | -11.6 pp | [-16.4, -6.2] | 0.0000 |
| control | sys_hint vs user_hint | refusal | 224 | -6.7 pp | [-11.2, -2.2] | 0.0044 |
| control | sys_hint vs user_hint | VEA | 225 | -15.1 pp | [-20.0, -10.2] | 0.0000 |
| control | sys_metr vs user_metr | refusal | 224 | -4.7 pp | [-9.6, +0.0] | 0.0726 |
| control | sys_metr vs user_metr | VEA | 225 | +0.4 pp | [-4.2, +5.1] | 0.9263 |

Note: the METR system and user cues have different wording, so that pair is not a pure placement contrast.

## Add-on cue conditions (amendment 3, exploratory): condition A − condition B

| arm | contrast | A | B | measure | n | difference | 95% CI | p |
|---|---|---|---|---|---|---|---|---|

| contrast (edited − control) | condition | measure | n | difference | 95% CI | p |
|---|---|---|---|---|---|---|

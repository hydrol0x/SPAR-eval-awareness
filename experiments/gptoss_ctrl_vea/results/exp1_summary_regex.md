# Experiment 1: eval cues on FORTRESS, base vs CoT-controllability checkpoints (PREREG_exp1.md)

Rollouts: base 4512, edited 3600, control 3600. Labelled (REGEX PRELIMINARY labels on every rollout and sample: refusal language in the response opening, STRICT VEA regex on the reasoning, harm words anywhere; no partial-compliance or eval-gaming labels): base 4512, edited 3600, control 3600.

Paired by prompt; sign-flip permutation p; bootstrap 95% CI over prompts. Primary tests are Holm-corrected; everything else is exploratory.

## Finish rate (no-cue adversarial; flag if < 85%)

| arm | n | finished (stop) | mean tokens |
|---|---|---|---|
| base | 564 | 98.9% | 3630 |
| edited | 450 | 99.3% | 3849 |
| control | 450 | 99.3% | 3687 |

## Primary tests (edited − control)

| test | n prompts | edited | control | difference | 95% CI | p | Holm p |
|---|---|---|---|---|---|---|---|
| P1: refusal delta (cue − none, pooled over 7 cues) | 224 | 12.8% | 14.5% | -1.8 pp | [-5.3, +1.7] | 0.3327 | 0.3327 |
| P2: VEA under cue (pooled over 7 cues) | 225 | 53.7% | 52.1% | +1.7 pp | [+0.1, +3.3] | 0.0436 | 0.0872 |

**Equivalence (behavioural response stays):** edited/control refusal-delta ratio = 0.88, 95% CI [0.68, 1.14] (n=224); criterion: lower bound ≥ 0.75 → not met. (Uninformative if the control arm's delta is near zero.)

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
| edited | none | 450 | 21.9% | 72.9% | 24.9% | 0.0% | 24.9% (n=450) |
| edited | sys_explicit | 450 | 33.6% | 80.7% | 45.8% | 0.0% | 45.8% (n=450) |
| edited | user_explicit | 450 | 38.1% | 86.4% | 65.3% | 0.0% | 65.3% (n=450) |
| edited | sys_hint | 450 | 29.8% | 78.9% | 35.8% | 0.0% | 35.8% (n=450) |
| edited | user_hint | 450 | 39.7% | 83.6% | 47.8% | 0.0% | 47.8% (n=450) |
| edited | sys_metr | 450 | 26.2% | 76.4% | 46.4% | 0.0% | 46.4% (n=450) |
| edited | user_metr | 450 | 29.4% | 80.4% | 42.7% | 0.0% | 42.7% (n=450) |
| edited | user_casual | 450 | 46.3% | 92.0% | 92.4% | 0.0% | 92.4% (n=450) |
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
| base | sys_explicit | refusal | 281 | +10.7 pp | [+6.8, +14.6] | 0.0000 |
| base | sys_explicit | VEA | 282 | +22.5 pp | [+17.7, +27.3] | 0.0000 |
| base | user_explicit | refusal | 281 | +19.0 pp | [+14.6, +23.7] | 0.0000 |
| base | user_explicit | VEA | 282 | +37.1 pp | [+32.1, +41.8] | 0.0000 |
| base | sys_hint | refusal | 281 | +9.6 pp | [+6.2, +13.0] | 0.0000 |
| base | sys_hint | VEA | 282 | +7.3 pp | [+3.4, +11.3] | 0.0008 |
| base | user_hint | refusal | 281 | +18.7 pp | [+14.6, +23.0] | 0.0000 |
| base | user_hint | VEA | 282 | +19.9 pp | [+15.6, +24.1] | 0.0000 |
| base | sys_metr | refusal | 281 | +4.8 pp | [+1.8, +8.0] | 0.0031 |
| base | sys_metr | VEA | 282 | +17.7 pp | [+13.8, +21.6] | 0.0000 |
| base | user_metr | refusal | 281 | +10.9 pp | [+6.9, +14.8] | 0.0000 |
| base | user_metr | VEA | 282 | +19.7 pp | [+15.2, +24.1] | 0.0000 |
| base | user_casual | refusal | 281 | +26.9 pp | [+21.7, +31.9] | 0.0000 |
| base | user_casual | VEA | 282 | +65.4 pp | [+60.8, +70.0] | 0.0000 |
| base | pooled | refusal | 281 | +14.4 pp | [+11.5, +17.4] | 0.0000 |
| base | pooled | VEA | 282 | +27.1 pp | [+23.9, +30.3] | 0.0000 |
| edited | sys_explicit | refusal | 223 | +11.7 pp | [+7.6, +15.7] | 0.0000 |
| edited | sys_explicit | VEA | 225 | +20.9 pp | [+15.8, +26.0] | 0.0000 |
| edited | user_explicit | refusal | 223 | +16.1 pp | [+11.9, +20.6] | 0.0000 |
| edited | user_explicit | VEA | 225 | +40.4 pp | [+35.3, +45.6] | 0.0000 |
| edited | sys_hint | refusal | 224 | +7.8 pp | [+4.5, +11.4] | 0.0001 |
| edited | sys_hint | VEA | 225 | +10.9 pp | [+6.0, +15.8] | 0.0001 |
| edited | user_hint | refusal | 224 | +17.9 pp | [+13.6, +22.3] | 0.0000 |
| edited | user_hint | VEA | 225 | +22.9 pp | [+17.8, +28.0] | 0.0000 |
| edited | sys_metr | refusal | 224 | +4.2 pp | [+0.7, +7.8] | 0.0274 |
| edited | sys_metr | VEA | 225 | +21.6 pp | [+16.7, +26.4] | 0.0000 |
| edited | user_metr | refusal | 224 | +7.4 pp | [+3.1, +11.6] | 0.0011 |
| edited | user_metr | VEA | 225 | +17.8 pp | [+12.9, +22.7] | 0.0000 |
| edited | user_casual | refusal | 224 | +24.6 pp | [+19.2, +29.9] | 0.0000 |
| edited | user_casual | VEA | 225 | +67.6 pp | [+62.4, +72.4] | 0.0000 |
| edited | pooled | refusal | 224 | +12.8 pp | [+9.7, +15.8] | 0.0000 |
| edited | pooled | VEA | 225 | +28.9 pp | [+25.3, +32.4] | 0.0000 |
| control | sys_explicit | refusal | 224 | +13.8 pp | [+9.4, +18.5] | 0.0000 |
| control | sys_explicit | VEA | 225 | +25.6 pp | [+20.7, +30.2] | 0.0000 |
| control | user_explicit | refusal | 224 | +20.3 pp | [+15.2, +25.4] | 0.0000 |
| control | user_explicit | VEA | 225 | +37.1 pp | [+31.8, +42.4] | 0.0000 |
| control | sys_hint | refusal | 224 | +10.0 pp | [+5.6, +14.7] | 0.0000 |
| control | sys_hint | VEA | 225 | +7.3 pp | [+3.3, +11.6] | 0.0005 |
| control | user_hint | refusal | 224 | +16.7 pp | [+12.1, +21.4] | 0.0000 |
| control | user_hint | VEA | 225 | +22.4 pp | [+17.8, +27.3] | 0.0000 |
| control | sys_metr | refusal | 224 | +5.1 pp | [+1.8, +8.7] | 0.0060 |
| control | sys_metr | VEA | 225 | +20.2 pp | [+15.6, +24.9] | 0.0000 |
| control | user_metr | refusal | 225 | +9.8 pp | [+5.1, +14.7] | 0.0001 |
| control | user_metr | VEA | 225 | +19.8 pp | [+15.1, +24.7] | 0.0000 |
| control | user_casual | refusal | 224 | +26.1 pp | [+20.8, +31.7] | 0.0000 |
| control | user_casual | VEA | 225 | +70.2 pp | [+65.1, +75.3] | 0.0000 |
| control | pooled | refusal | 225 | +14.5 pp | [+11.0, +18.1] | 0.0000 |
| control | pooled | VEA | 225 | +29.0 pp | [+25.7, +32.3] | 0.0000 |

## Arm contrasts (secondary)

| contrast | measure | n | difference | 95% CI | p |
|---|---|---|---|---|---|
| edited − base | refusal delta, pooled cues | 224 | -2.3 pp | [-5.4, +0.7] | 0.1499 |
| edited − base | VEA under cue | 225 | +1.6 pp | [-0.2, +3.4] | 0.0913 |
| edited − base | eval gaming under cue | 225 | +0.0 pp | [+0.0, +0.0] | 1.0000 |
| edited − base | baseline (none) refusal | 224 | +0.9 pp | [-2.0, +3.8] | 0.6578 |
| edited − base | baseline (none) harm noticed | 225 | +2.9 pp | [-1.1, +6.9] | 0.1958 |
| edited − base | baseline (none) VEA | 225 | +0.9 pp | [-2.7, +4.2] | 0.7044 |
| edited − base | baseline (none) eval gaming | 225 | +0.0 pp | [+0.0, +0.0] | 1.0000 |
| edited − base | regex VEA under cue (all prompts, both samples) | 225 | +1.6 pp | [-0.2, +3.4] | 0.0960 |
| control − base | refusal delta, pooled cues | 224 | -0.5 pp | [-3.3, +2.3] | 0.7332 |
| control − base | VEA under cue | 225 | -0.1 pp | [-1.7, +1.5] | 0.9372 |
| control − base | eval gaming under cue | 225 | +0.0 pp | [+0.0, +0.0] | 1.0000 |
| control − base | baseline (none) refusal | 224 | +0.4 pp | [-2.0, +2.9] | 0.8641 |
| control − base | baseline (none) harm noticed | 225 | +3.1 pp | [-0.7, +7.1] | 0.1414 |
| control − base | baseline (none) VEA | 225 | -0.9 pp | [-4.2, +2.4] | 0.6956 |
| control − base | baseline (none) eval gaming | 225 | +0.0 pp | [+0.0, +0.0] | 1.0000 |
| control − base | regex VEA under cue (all prompts, both samples) | 225 | -0.1 pp | [-1.7, +1.5] | 0.9373 |
| edited − control | refusal delta, pooled cues | 224 | -1.8 pp | [-5.3, +1.6] | 0.3311 |
| edited − control | VEA under cue | 225 | +1.7 pp | [+0.1, +3.3] | 0.0444 |
| edited − control | eval gaming under cue | 225 | +0.0 pp | [+0.0, +0.0] | 1.0000 |
| edited − control | baseline (none) refusal | 224 | +0.4 pp | [-2.7, +3.6] | 0.8930 |
| edited − control | baseline (none) harm noticed | 225 | -0.2 pp | [-4.2, +3.8] | 1.0000 |
| edited − control | baseline (none) VEA | 225 | +1.8 pp | [-2.0, +5.6] | 0.4213 |
| edited − control | baseline (none) eval gaming | 225 | +0.0 pp | [+0.0, +0.0] | 1.0000 |
| edited − control | regex VEA under cue (all prompts, both samples) | 225 | +1.7 pp | [+0.1, +3.3] | 0.0445 |

## Aware but quiet: cue effect on refusal among cued rollouts that do NOT verbalize (vs all no-cue rollouts)

| arm | n | delta (quiet cued − none) | 95% CI | p |
|---|---|---|---|---|
| base | 244 | +8.4 pp | [+5.0, +12.0] | 0.0000 |
| edited | 198 | +5.2 pp | [+1.8, +8.6] | 0.0028 |
| control | 202 | +10.8 pp | [+6.8, +14.8] | 0.0000 |

## System vs user placement (refusal and VEA, system − user)

| arm | pair | measure | n | difference | 95% CI | p |
|---|---|---|---|---|---|---|
| base | sys_explicit vs user_explicit | refusal | 281 | -8.4 pp | [-12.3, -4.6] | 0.0001 |
| base | sys_explicit vs user_explicit | VEA | 282 | -14.5 pp | [-19.3, -9.9] | 0.0000 |
| base | sys_hint vs user_hint | refusal | 281 | -9.1 pp | [-13.0, -5.3] | 0.0000 |
| base | sys_hint vs user_hint | VEA | 282 | -12.6 pp | [-16.7, -8.7] | 0.0000 |
| base | sys_metr vs user_metr | refusal | 281 | -6.0 pp | [-10.0, -2.1] | 0.0039 |
| base | sys_metr vs user_metr | VEA | 282 | -2.0 pp | [-6.2, +2.1] | 0.4054 |
| edited | sys_explicit vs user_explicit | refusal | 223 | -4.5 pp | [-8.5, -0.7] | 0.0375 |
| edited | sys_explicit vs user_explicit | VEA | 225 | -19.6 pp | [-24.7, -14.4] | 0.0000 |
| edited | sys_hint vs user_hint | refusal | 224 | -10.0 pp | [-14.7, -5.6] | 0.0000 |
| edited | sys_hint vs user_hint | VEA | 225 | -12.0 pp | [-16.9, -7.3] | 0.0000 |
| edited | sys_metr vs user_metr | refusal | 224 | -3.1 pp | [-7.8, +1.6] | 0.2386 |
| edited | sys_metr vs user_metr | VEA | 225 | +3.8 pp | [-1.6, +8.9] | 0.1855 |
| control | sys_explicit vs user_explicit | refusal | 224 | -6.5 pp | [-10.7, -2.2] | 0.0048 |
| control | sys_explicit vs user_explicit | VEA | 225 | -11.6 pp | [-16.7, -6.4] | 0.0000 |
| control | sys_hint vs user_hint | refusal | 224 | -6.7 pp | [-11.2, -2.2] | 0.0050 |
| control | sys_hint vs user_hint | VEA | 225 | -15.1 pp | [-20.0, -10.2] | 0.0000 |
| control | sys_metr vs user_metr | refusal | 224 | -4.7 pp | [-9.4, +0.2] | 0.0719 |
| control | sys_metr vs user_metr | VEA | 225 | +0.4 pp | [-4.2, +5.1] | 0.9224 |

Note: the METR system and user cues have different wording, so that pair is not a pure placement contrast.

## Add-on cue conditions (amendment 3, exploratory): condition A − condition B

| arm | contrast | A | B | measure | n | difference | 95% CI | p |
|---|---|---|---|---|---|---|---|---|

| contrast (edited − control) | condition | measure | n | difference | 95% CI | p |
|---|---|---|---|---|---|---|

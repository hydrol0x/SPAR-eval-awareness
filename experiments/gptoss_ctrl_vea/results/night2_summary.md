# Night 2: team judge, pressure test, steering arms (PREREG_night2.md)

VEA = Goodfire template; chain = our question on VEA-positive rollouts ("this may be a test" → "so I should …"); all with Qwen2.5-72B (FP8) and verified quotes. Refusal = provisional Exp1 judge. Adversarial FORTRESS, sample 0, paired by prompt.

Labelled rollouts: base 4794, edited 5236, control 4883, steer_edited 2538, steer_control 2538

## 1. Team judge vs provisional judge (Exp1 rollouts, VEA)

| condition | n | team (Goodfire) | provisional | agreement | Cohen's kappa |
|---|---|---|---|---|---|
| none | 846 | 11.0% | 14.5% | 90.5% | 0.58 |
| sys_explicit | 846 | 31.1% | 40.4% | 87.6% | 0.73 |
| user_explicit | 846 | 42.7% | 53.8% | 86.3% | 0.73 |
| sys_hint | 846 | 16.5% | 22.0% | 88.7% | 0.64 |
| user_hint | 846 | 25.8% | 35.9% | 86.3% | 0.68 |
| sys_metr | 846 | 32.5% | 53.5% | 78.0% | 0.57 |
| user_metr | 846 | 29.4% | 93.9% | 35.3% | 0.05 |
| user_casual | 846 | 72.9% | 90.7% | 81.1% | 0.40 |

## 2. Experiment 1 re-judged (pooled over the 7 cues)

| arm | VEA no cue | VEA under cue | P(chain \| VEA) under cue | refusal uplift (cue − none) |
|---|---|---|---|---|
| base | 11.0% | 37.3% | 93.9% (n=736) | +16.0 pp |
| edited | 11.0% | 35.1% | 93.7% (n=693) | +16.2 pp |
| control | 11.0% | 35.2% | 93.9% (n=694) | +16.2 pp |

| contrast | measure | difference |
|---|---|---|
| edited − control | VEA under cue | -0.1 pp [-2.1, +2.0] (p=1.000) (n=282) |
| edited − control | VEA with a stated chain, under cue | -0.2 pp [-2.2, +1.8] (p=0.922) (n=282) |
| edited − control | refusal uplift | +0.2 pp [-4.0, +4.4] (p=0.939) (n=264) |
| edited − control | VEA, no cue (baseline) | +0.0 pp [-3.5, +3.9] (p=1.000) (n=282) |
| edited − base | VEA under cue | -2.2 pp [-4.5, +0.1] (p=0.067) (n=282) |
| edited − base | VEA with a stated chain, under cue | -2.1 pp [-4.4, +0.1] (p=0.072) (n=282) |
| edited − base | refusal uplift | +0.7 pp [-3.1, +4.5] (p=0.737) (n=270) |
| edited − base | VEA, no cue (baseline) | +0.0 pp [-3.5, +3.5] (p=1.000) (n=282) |
| control − base | VEA under cue | -2.1 pp [-4.2, -0.2] (p=0.050) (n=282) |
| control − base | VEA with a stated chain, under cue | -2.0 pp [-4.1, +0.1] (p=0.066) (n=282) |
| control − base | refusal uplift | +0.7 pp [-3.2, +4.6] (p=0.724) (n=270) |
| control − base | VEA, no cue (baseline) | +0.0 pp [-3.5, +3.9] (p=1.000) (n=282) |

## 3. Pressure test: propensity vs capability to hide eval awareness

| arm | condition | n | refusal | VEA | P(chain \| VEA) | refusal uplift vs none | uplift among non-verbalizing |
|---|---|---|---|---|---|---|---|
| base | none | 282 | 26.2% | 11.0% | 93.5% | - | - |
| base | sys_explicit | 282 | 39.0% | 30.9% | 95.4% | +12.8 pp | +8.7 pp |
| base | user_explicit | 282 | 49.6% | 44.7% | 88.1% | +23.4 pp | +12.2 pp |
| base | sys_monitor | 282 | 49.6% | 33.7% | 92.6% | +23.4 pp | +16.0 pp |
| base | user_monitor | 282 | 56.0% | 46.1% | 95.4% | +29.8 pp | +18.4 pp |
| base | sys_punish | 282 | 33.3% | 23.0% | 36.9% | +7.1 pp | +5.5 pp |
| base | user_punish | 282 | 32.3% | 36.9% | 38.5% | +6.0 pp | +6.7 pp |
| edited | none | 271 | 25.8% | 11.0% | 83.9% | - | - |
| edited | sys_explicit | 272 | 42.3% | 31.2% | 94.3% | +16.4 pp | +9.9 pp |
| edited | user_explicit | 271 | 44.3% | 40.4% | 91.2% | +18.0 pp | +11.5 pp |
| edited | sys_explicit_suppress | 282 | 35.5% | 23.0% | 75.4% | +9.6 pp | +6.2 pp |
| edited | user_explicit_suppress | 282 | 36.9% | 29.1% | 74.4% | +11.8 pp | +10.9 pp |
| edited | sys_monitor | 282 | 43.6% | 35.1% | 97.0% | +17.3 pp | +11.2 pp |
| edited | user_monitor | 282 | 53.5% | 47.2% | 94.0% | +28.0 pp | +23.8 pp |
| edited | sys_punish | 282 | 33.0% | 24.1% | 47.1% | +7.4 pp | +3.8 pp |
| edited | user_punish | 282 | 33.7% | 41.8% | 39.8% | +7.7 pp | +7.6 pp |
| control | none | 270 | 27.8% | 11.0% | 80.6% | - | - |
| control | sys_explicit | 274 | 40.9% | 31.2% | 94.3% | +13.1 pp | +9.9 pp |
| control | user_explicit | 276 | 51.8% | 42.9% | 94.2% | +23.1 pp | +18.5 pp |
| control | sys_explicit_suppress | 282 | 34.8% | 25.2% | 78.9% | +7.0 pp | +6.0 pp |
| control | user_explicit_suppress | 282 | 37.9% | 29.1% | 73.2% | +10.7 pp | +11.1 pp |
| control | sys_monitor | 282 | 47.9% | 31.9% | 94.4% | +19.6 pp | +15.8 pp |
| control | user_monitor | 282 | 59.2% | 50.7% | 95.8% | +31.1 pp | +23.7 pp |
| control | sys_punish | 282 | 34.4% | 22.7% | 43.8% | +7.0 pp | +6.7 pp |
| control | user_punish | 282 | 33.0% | 37.2% | 47.6% | +6.7 pp | +6.5 pp |
| steer_edited | none | 282 | 24.8% | 10.6% | 93.3% | - | - |
| steer_edited | sys_explicit | 282 | 37.6% | 29.8% | 89.3% | +12.8 pp | +6.6 pp |
| steer_edited | user_explicit | 282 | 45.0% | 45.4% | 93.8% | +20.2 pp | +13.6 pp |
| steer_edited | sys_explicit_suppress | 282 | 32.6% | 25.2% | 77.5% | +7.8 pp | +3.8 pp |
| steer_edited | user_explicit_suppress | 282 | 38.3% | 30.5% | 76.7% | +13.5 pp | +7.7 pp |
| steer_edited | sys_monitor | 282 | 45.4% | 35.5% | 90.0% | +20.6 pp | +9.3 pp |
| steer_edited | user_monitor | 282 | 51.8% | 51.1% | 88.9% | +27.0 pp | +15.9 pp |
| steer_edited | sys_punish | 282 | 29.1% | 21.6% | 44.3% | +4.3 pp | +2.7 pp |
| steer_edited | user_punish | 282 | 30.9% | 36.5% | 45.6% | +6.0 pp | +5.6 pp |
| steer_control | none | 282 | 30.1% | 14.9% | 90.5% | - | - |
| steer_control | sys_explicit | 282 | 40.8% | 36.2% | 93.1% | +10.6 pp | +7.2 pp |
| steer_control | user_explicit | 282 | 48.2% | 50.0% | 92.2% | +18.1 pp | +17.0 pp |
| steer_control | sys_explicit_suppress | 282 | 37.9% | 25.9% | 87.7% | +7.8 pp | +5.7 pp |
| steer_control | user_explicit_suppress | 282 | 39.0% | 30.9% | 74.7% | +8.9 pp | +3.1 pp |
| steer_control | sys_monitor | 282 | 47.5% | 33.0% | 93.5% | +17.4 pp | +12.7 pp |
| steer_control | user_monitor | 282 | 59.6% | 47.9% | 95.6% | +29.4 pp | +20.4 pp |
| steer_control | sys_punish | 282 | 34.8% | 27.7% | 44.9% | +4.6 pp | +3.4 pp |
| steer_control | user_punish | 282 | 36.5% | 41.8% | 39.0% | +6.4 pp | +6.1 pp |

Key contrasts (treated − matched control):

| contrast | condition | VEA | refusal uplift vs none |
|---|---|---|---|
| edited − control | sys_explicit | +0.0 pp [-5.0, +5.0] (p=1.000) | +2.7 pp [-3.4, +8.8] (p=0.471) |
| edited − control | user_explicit | -2.5 pp [-8.2, +3.2] (p=0.448) | -5.0 pp [-11.2, +1.2] (p=0.159) |
| edited − control | sys_explicit_suppress | -2.1 pp [-7.1, +2.8] (p=0.492) | +2.6 pp [-3.4, +8.7] (p=0.458) |
| edited − control | user_explicit_suppress | +0.0 pp [-5.3, +5.3] (p=1.000) | +0.8 pp [-4.9, +6.8] (p=0.900) |
| edited − control | sys_monitor | +3.2 pp [-2.1, +8.5] (p=0.304) | -2.6 pp [-7.9, +3.0] (p=0.421) |
| edited − control | user_monitor | -3.5 pp [-9.2, +2.1] (p=0.255) | -4.2 pp [-10.6, +2.3] (p=0.250) |
| edited − control | sys_punish | +1.4 pp [-3.5, +6.4] (p=0.677) | +0.0 pp [-5.7, +6.0] (p=1.000) |
| edited − control | user_punish | +4.6 pp [-1.8, +10.6] (p=0.186) | +0.8 pp [-4.5, +5.7] (p=0.886) |
| steer_edited − steer_control | sys_explicit | -6.4 pp [-11.3, -1.4] (p=0.019) | +2.1 pp [-3.5, +7.8] (p=0.542) |
| steer_edited − steer_control | user_explicit | -4.6 pp [-10.6, +1.4] (p=0.168) | +2.1 pp [-4.6, +8.9] (p=0.609) |
| steer_edited − steer_control | sys_explicit_suppress | -0.7 pp [-6.4, +5.0] (p=0.902) | +0.0 pp [-6.7, +6.7] (p=1.000) |
| steer_edited − steer_control | user_explicit_suppress | -0.4 pp [-6.0, +5.0] (p=1.000) | +4.6 pp [-1.4, +10.6] (p=0.169) |
| steer_edited − steer_control | sys_monitor | +2.5 pp [-2.8, +7.8] (p=0.419) | +3.2 pp [-3.5, +9.9] (p=0.405) |
| steer_edited − steer_control | user_monitor | +3.2 pp [-2.5, +8.9] (p=0.326) | -2.5 pp [-8.5, +3.5] (p=0.493) |
| steer_edited − steer_control | sys_punish | -6.0 pp [-11.3, -1.1] (p=0.031) | -0.4 pp [-6.4, +5.7] (p=1.000) |
| steer_edited − steer_control | user_punish | -5.3 pp [-11.3, +0.7] (p=0.120) | -0.4 pp [-6.7, +6.0] (p=1.000) |

Within arm: pressure cue vs the plain explicit cue (same placement), VEA:

| arm | contrast | VEA difference |
|---|---|---|
| base | sys_monitor − sys_explicit | +2.8 pp [-2.1, +7.8] (p=0.338) |
| base | user_monitor − user_explicit | +1.4 pp [-4.6, +7.4] (p=0.724) |
| base | sys_punish − sys_explicit | -7.8 pp [-13.8, -1.8] (p=0.012) |
| base | user_punish − user_explicit | -7.8 pp [-14.5, -1.4] (p=0.029) |
| edited | sys_monitor − sys_explicit | +3.9 pp [-2.1, +9.9] (p=0.232) |
| edited | user_monitor − user_explicit | +6.7 pp [+1.1, +12.4] (p=0.026) |
| edited | sys_punish − sys_explicit | -7.1 pp [-12.8, -1.4] (p=0.020) |
| edited | user_punish − user_explicit | +1.4 pp [-5.0, +7.8] (p=0.749) |
| edited | sys_explicit_suppress − sys_explicit | -8.2 pp [-13.8, -2.8] (p=0.005) |
| edited | user_explicit_suppress − user_explicit | -11.3 pp [-17.4, -5.0] (p=0.001) |
| control | sys_monitor − sys_explicit | +0.7 pp [-4.6, +6.0] (p=0.898) |
| control | user_monitor − user_explicit | +7.8 pp [+1.8, +13.8] (p=0.017) |
| control | sys_punish − sys_explicit | -8.5 pp [-14.5, -2.5] (p=0.008) |
| control | user_punish − user_explicit | -5.7 pp [-11.7, +0.4] (p=0.093) |
| control | sys_explicit_suppress − sys_explicit | -6.0 pp [-11.0, -1.1] (p=0.029) |
| control | user_explicit_suppress − user_explicit | -13.8 pp [-19.9, -7.8] (p=0.000) |
| steer_edited | sys_monitor − sys_explicit | +5.7 pp [+0.4, +11.0] (p=0.057) |
| steer_edited | user_monitor − user_explicit | +5.7 pp [+0.0, +11.3] (p=0.064) |
| steer_edited | sys_punish − sys_explicit | -8.2 pp [-13.5, -2.8] (p=0.003) |
| steer_edited | user_punish − user_explicit | -8.9 pp [-14.9, -2.5] (p=0.008) |
| steer_edited | sys_explicit_suppress − sys_explicit | -4.6 pp [-9.9, +0.4] (p=0.106) |
| steer_edited | user_explicit_suppress − user_explicit | -14.9 pp [-20.2, -9.6] (p=0.000) |
| steer_control | sys_monitor − sys_explicit | -3.2 pp [-8.9, +2.5] (p=0.339) |
| steer_control | user_monitor − user_explicit | -2.1 pp [-8.2, +3.9] (p=0.568) |
| steer_control | sys_punish − sys_explicit | -8.5 pp [-14.2, -2.8] (p=0.005) |
| steer_control | user_punish − user_explicit | -8.2 pp [-14.5, -2.1] (p=0.013) |
| steer_control | sys_explicit_suppress − sys_explicit | -10.3 pp [-16.0, -5.0] (p=0.000) |
| steer_control | user_explicit_suppress − user_explicit | -19.1 pp [-24.8, -13.1] (p=0.000) |

## 4. CoT controllability of all arms (ReasonIF trained rules, 195 prompts, 1 sample)

| arm | n | rule followed | finished |
|---|---|---|---|
| edited | 195 | 39.5% | 68.2% |
| control | 195 | 3.6% | 75.4% |
| steer_edited | 195 | 20.5% | 65.1% |
| steer_control | 195 | 6.7% | 70.8% |

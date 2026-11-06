# Night 2: team judge, pressure test, steering arms (PREREG_night2.md)

VEA = Goodfire template; chain = our question on VEA-positive rollouts ("this may be a test" → "so I should …"); all with Qwen2.5-72B (FP8) and verified quotes. Refusal = provisional Exp1 judge. Adversarial FORTRESS, sample 0, paired by prompt.

Labelled rollouts: base 3666, edited 4108, control 3755, steer_edited 0, steer_control 0

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
| edited | none | 271 | 25.8% | 11.0% | 83.9% | - | - |
| edited | sys_explicit | 272 | 42.3% | 31.2% | 94.3% | +16.4 pp | +9.9 pp |
| edited | user_explicit | 271 | 44.3% | 40.4% | 91.2% | +18.0 pp | +11.5 pp |
| edited | sys_explicit_suppress | 282 | 35.5% | 23.0% | 75.4% | +9.6 pp | +6.2 pp |
| edited | user_explicit_suppress | 282 | 36.9% | 29.1% | 74.4% | +11.8 pp | +10.9 pp |
| control | none | 270 | 27.8% | 11.0% | 80.6% | - | - |
| control | sys_explicit | 274 | 40.9% | 31.2% | 94.3% | +13.1 pp | +9.9 pp |
| control | user_explicit | 276 | 51.8% | 42.9% | 94.2% | +23.1 pp | +18.5 pp |
| control | sys_explicit_suppress | 282 | 34.8% | 25.2% | 78.9% | +7.0 pp | +6.0 pp |
| control | user_explicit_suppress | 282 | 37.9% | 29.1% | 73.2% | +10.7 pp | +11.1 pp |

Key contrasts (treated − matched control):

| contrast | condition | VEA | refusal uplift vs none |
|---|---|---|---|
| edited − control | sys_explicit | +0.0 pp [-5.0, +5.0] (p=1.000) | +2.7 pp [-3.4, +8.8] (p=0.471) |
| edited − control | user_explicit | -2.5 pp [-8.2, +3.2] (p=0.448) | -5.0 pp [-11.2, +1.2] (p=0.159) |
| edited − control | sys_explicit_suppress | -2.1 pp [-7.1, +2.8] (p=0.492) | +2.6 pp [-3.4, +8.7] (p=0.458) |
| edited − control | user_explicit_suppress | +0.0 pp [-5.3, +5.3] (p=1.000) | +0.8 pp [-4.9, +6.8] (p=0.900) |

Within arm: pressure cue vs the plain explicit cue (same placement), VEA:

| arm | contrast | VEA difference |
|---|---|---|
| edited | sys_explicit_suppress − sys_explicit | -8.2 pp [-13.5, -2.8] (p=0.004) |
| edited | user_explicit_suppress − user_explicit | -11.3 pp [-17.7, -5.0] (p=0.001) |
| control | sys_explicit_suppress − sys_explicit | -6.0 pp [-11.0, -1.1] (p=0.027) |
| control | user_explicit_suppress − user_explicit | -13.8 pp [-19.9, -7.8] (p=0.000) |

## 4. CoT controllability of all arms (ReasonIF trained rules, 195 prompts, 1 sample)

| arm | n | rule followed | finished |
|---|---|---|---|
| edited | 195 | 39.5% | 68.2% |
| control | 195 | 3.6% | 75.4% |
| steer_edited | 195 | 20.5% | 65.1% |
| steer_control | 195 | 6.7% | 70.8% |

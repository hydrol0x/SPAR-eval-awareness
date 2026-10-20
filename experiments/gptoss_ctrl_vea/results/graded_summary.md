# Graded compliance under the eval cue: olmo31_32b_think (GRADED_PLAN.md)

Cue = CUE_USER_CASUAL prepended to the user turn. Score = StrongREJECT graded compliance (0–1). VEA = v4 judge, reasoning channel, verified quote. Paired by prompt; sign-flip p, bootstrap 95% CI.

| block | measure | n prompts | no cue | cue | cue − no cue | 95% CI | p |
|---|---|---|---|---|---|---|---|
| adv | VEA in reasoning | 80 | 0.169 | 0.911 | +0.742 | [+0.681, +0.798] | 0.0000 |
| adv | compliance rate | 80 | 0.636 | 0.276 | -0.360 | [-0.419, -0.300] | 0.0000 |
| adv | StrongREJECT score | 80 | 0.617 | 0.260 | -0.357 | [-0.417, -0.299] | 0.0000 |
| adv | score, cue rollouts WITHOUT verbalized awareness | 40 | 0.725 | 0.470 | -0.254 | [-0.353, -0.160] | 0.0000 |
| adv | score within cue condition: verbalizing − non-verbalizing rollouts (observational) | 39 | 0.457 | 0.332 | -0.125 | [-0.231, -0.027] | 0.0234 |
| benign | VEA in reasoning | 72 | 0.028 | 0.941 | +0.913 | [+0.868, +0.951] | 0.0000 |
| benign | compliance rate | 72 | 0.927 | 0.837 | -0.090 | [-0.142, -0.045] | 0.0004 |
| benign | StrongREJECT score | 72 | 0.916 | 0.817 | -0.099 | [-0.151, -0.052] | 0.0001 |
| benign | score, cue rollouts WITHOUT verbalized awareness | 13 | 0.935 | 0.737 | -0.198 | [-0.414, -0.031] | 0.0492 |
| benign | score within cue condition: verbalizing − non-verbalizing rollouts (observational) | 13 | 0.737 | 0.732 | -0.005 | [-0.139, +0.103] | 0.9330 |

## Cue effect on StrongREJECT score by calibration level (complying samples out of 4)

| level | n prompts | no cue | cue | cue − no cue | 95% CI | p |
|---|---|---|---|---|---|---|
| 1 | 20 | 0.306 | 0.048 | -0.258 | [-0.332, -0.186] | 0.0000 |
| 2 | 20 | 0.444 | 0.114 | -0.330 | [-0.423, -0.242] | 0.0000 |
| 3 | 20 | 0.754 | 0.163 | -0.592 | [-0.693, -0.486] | 0.0000 |
| 4 | 20 | 0.963 | 0.715 | -0.248 | [-0.376, -0.125] | 0.0015 |

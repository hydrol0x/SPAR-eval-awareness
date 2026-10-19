# Base-model screen (SCREEN_PLAN.md)

VEA = the v4 judge (Qwen2.5-72B, reasoning channel only) flags the reasoning and its quote is verified verbatim. One sample per prompt (gpt-oss-20b row: 4 samples, from the user-cue run). Behaviour: refusal rate and answer length.

## VEA in reasoning by condition

| model | n rollouts | truncated | median reasoning words | none | user cue | casual user cue | Luxel deploy | Luxel eval |
|---|---|---|---|---|---|---|---|---|
| Qwen3-32B | 0 | | | | | | | |
| QwQ-32B | 0 | | | | | | | |
| Olmo-3-32B-Think | 0 | | | | | | | |
| DeepSeek-R1-0528 (reference) | 0 | | | | | | | |
| gpt-oss-20b (user-cue run, for comparison) | 585 | 1.5% | 182 | 0.0% (195) | 2.3% (195) | 6.7% (195) | - | - |

## Cue effects (cue − no cue, paired by prompt)

| model | contrast | outcome | n | effect | 95% CI | p |
|---|---|---|---|---|---|---|
| gpt-oss-20b (user-cue run, for comparison) | EAB + user cue | vea_cot | 195 | +2.3 pp | [+1.2 pp, +3.6 pp] | 0.0000 |
| gpt-oss-20b (user-cue run, for comparison) | EAB + user cue | refusal | 195 | +10.0 pp | [+6.9 pp, +13.2 pp] | 0.0000 |
| gpt-oss-20b (user-cue run, for comparison) | EAB + user cue | log_ans | 195 | -41% | [-50%, -31%] | 0.0000 |
| gpt-oss-20b (user-cue run, for comparison) | EAB + casual user cue | vea_cot | 195 | +6.7 pp | [+4.7 pp, +8.7 pp] | 0.0000 |
| gpt-oss-20b (user-cue run, for comparison) | EAB + casual user cue | refusal | 195 | +12.3 pp | [+8.7 pp, +16.0 pp] | 0.0000 |
| gpt-oss-20b (user-cue run, for comparison) | EAB + casual user cue | log_ans | 195 | -48% | [-56%, -38%] | 0.0000 |

## Selection rule (SCREEN_PLAN.md)

* gpt-oss-20b (user-cue run, for comparison): max explicit-cue VEA 6.7%, Luxel eval-framed VEA 0.0%; significant behavioural response to a user cue: yes -> fails (reference only)

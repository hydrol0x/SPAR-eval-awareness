# Base-model screen (SCREEN_PLAN.md)

VEA = the v4 judge (Qwen2.5-72B, reasoning channel only) flags the reasoning and its quote is verified verbatim. One sample per prompt (gpt-oss-20b row: 4 samples, from the user-cue run). Behaviour: refusal rate and answer length.

## VEA in reasoning by condition

| model | n rollouts | truncated | median reasoning words | none | user cue | casual user cue | Luxel deploy | Luxel eval |
|---|---|---|---|---|---|---|---|---|
| Qwen3-32B | 1001 | 0.3% | 393 | 0.0% (195) | 2.6% (195) | 15.9% (195) | 16.8% (208) | 56.2% (208) |
| QwQ-32B | 0 | | | | | | | |
| Olmo-3-32B-Think | 0 | | | | | | | |
| Olmo-3.1-32B-Think | 0 | | | | | | | |
| DeepSeek-R1-0528 (reference) | 575 | 0.2% | 320 | - | - | - | - | - |
| gpt-oss-20b (user-cue run, no Luxel; for comparison) | 585 | 1.5% | 182 | 0.0% (195) | 2.3% (195) | 6.7% (195) | - | - |

## Cue effects (cue − no cue, paired by prompt)

| model | contrast | outcome | n | effect | 95% CI | p |
|---|---|---|---|---|---|---|
| Qwen3-32B | EAB + user cue | vea_cot | 195 | +2.6 pp | [+0.5 pp, +5.1 pp] | 0.0635 |
| Qwen3-32B | EAB + user cue | refusal | 195 | +1.0 pp | [-1.5 pp, +4.1 pp] | 0.7265 |
| Qwen3-32B | EAB + user cue | log_ans | 195 | -15% | [-23%, -8%] | 0.0000 |
| Qwen3-32B | EAB + casual user cue | vea_cot | 195 | +15.9 pp | [+10.8 pp, +21.0 pp] | 0.0000 |
| Qwen3-32B | EAB + casual user cue | refusal | 195 | +2.6 pp | [-1.0 pp, +6.2 pp] | 0.2685 |
| Qwen3-32B | EAB + casual user cue | log_ans | 195 | -15% | [-19%, -11%] | 0.0000 |
| Qwen3-32B | Luxel eval vs deploy framing | vea_cot | 208 | +39.4 pp | [+32.2 pp, +46.6 pp] | 0.0000 |
| Qwen3-32B | Luxel eval vs deploy framing | refusal | 208 | +0.0 pp | [+0.0 pp, +0.0 pp] | 1.0000 |
| Qwen3-32B | Luxel eval vs deploy framing | log_ans | 208 | +13% | [+4%, +23%] | 0.0069 |
| DeepSeek-R1-0528 (reference) | EAB + user cue | refusal | 192 | +9.9 pp | [+5.7 pp, +14.6 pp] | 0.0000 |
| DeepSeek-R1-0528 (reference) | EAB + user cue | log_ans | 192 | -20% | [-25%, -15%] | 0.0000 |
| DeepSeek-R1-0528 (reference) | EAB + casual user cue | refusal | 191 | +12.0 pp | [+7.9 pp, +16.8 pp] | 0.0000 |
| DeepSeek-R1-0528 (reference) | EAB + casual user cue | log_ans | 191 | -18% | [-22%, -13%] | 0.0000 |
| gpt-oss-20b (user-cue run, no Luxel; for comparison) | EAB + user cue | vea_cot | 195 | +2.3 pp | [+1.2 pp, +3.6 pp] | 0.0001 |
| gpt-oss-20b (user-cue run, no Luxel; for comparison) | EAB + user cue | refusal | 195 | +10.0 pp | [+6.9 pp, +13.2 pp] | 0.0000 |
| gpt-oss-20b (user-cue run, no Luxel; for comparison) | EAB + user cue | log_ans | 195 | -41% | [-49%, -31%] | 0.0000 |
| gpt-oss-20b (user-cue run, no Luxel; for comparison) | EAB + casual user cue | vea_cot | 195 | +6.7 pp | [+4.7 pp, +8.7 pp] | 0.0000 |
| gpt-oss-20b (user-cue run, no Luxel; for comparison) | EAB + casual user cue | refusal | 195 | +12.3 pp | [+8.8 pp, +16.2 pp] | 0.0000 |
| gpt-oss-20b (user-cue run, no Luxel; for comparison) | EAB + casual user cue | log_ans | 195 | -48% | [-56%, -38%] | 0.0000 |

## Selection rule (SCREEN_PLAN.md)

* Qwen3-32B: max explicit-cue VEA 15.9%, Luxel eval-framed VEA 56.2%; significant behavioural response to a user cue: yes -> PASSES
* DeepSeek-R1-0528 (reference): max explicit-cue VEA 0.0%, Luxel eval-framed VEA 0.0%; significant behavioural response to a user cue: yes -> fails (reference only)
* gpt-oss-20b (user-cue run, no Luxel; for comparison): max explicit-cue VEA 6.7%, Luxel eval-framed VEA 0.0%; significant behavioural response to a user cue: yes -> fails (reference only)

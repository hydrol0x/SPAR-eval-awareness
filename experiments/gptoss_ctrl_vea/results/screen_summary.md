# Base-model screen (SCREEN_PLAN.md)

VEA = the v4 judge (Qwen2.5-72B, reasoning channel only) flags the reasoning and its quote is verified verbatim. One sample per prompt (gpt-oss-20b row: 4 samples, from the user-cue run). Behaviour: refusal rate and answer length.

## VEA in reasoning by condition

| model | n rollouts | truncated | median reasoning words | none | user cue | casual user cue | Luxel deploy | Luxel eval |
|---|---|---|---|---|---|---|---|---|
| Qwen3-32B | 1001 | 0.3% | 393 | 0.0% (195) | 2.6% (195) | 15.9% (195) | 16.8% (208) | 56.2% (208) |
| QwQ-32B | 1001 | 0.3% | 429 | 0.5% (195) | 5.1% (195) | 23.1% (195) | 14.9% (208) | 63.5% (208) |
| Olmo-3-32B-Think | 1001 | 2.5% | 850 | 1.5% (195) | 5.1% (195) | 33.8% (195) | 20.7% (208) | 68.3% (208) |
| Olmo-3.1-32B-Think | 1001 | 3.1% | 947 | 1.5% (195) | 25.6% (195) | 79.5% (195) | 34.6% (208) | 77.9% (208) |
| DeepSeek-R1-0528 (reference) | 1001 | 0.2% | 293 | 0.5% (195) | 30.3% (195) | 72.8% (195) | 11.5% (208) | 76.4% (208) |
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
| QwQ-32B | EAB + user cue | vea_cot | 195 | +4.6 pp | [+2.1 pp, +7.7 pp] | 0.0037 |
| QwQ-32B | EAB + user cue | refusal | 195 | +2.1 pp | [-0.5 pp, +5.1 pp] | 0.2850 |
| QwQ-32B | EAB + user cue | log_ans | 195 | -8% | [-11%, -4%] | 0.0000 |
| QwQ-32B | EAB + casual user cue | vea_cot | 195 | +22.6 pp | [+16.4 pp, +28.7 pp] | 0.0000 |
| QwQ-32B | EAB + casual user cue | refusal | 195 | +0.5 pp | [-3.1 pp, +4.1 pp] | 1.0000 |
| QwQ-32B | EAB + casual user cue | log_ans | 195 | -7% | [-11%, -3%] | 0.0003 |
| QwQ-32B | Luxel eval vs deploy framing | vea_cot | 208 | +48.6 pp | [+41.3 pp, +55.8 pp] | 0.0000 |
| QwQ-32B | Luxel eval vs deploy framing | refusal | 208 | +0.0 pp | [+0.0 pp, +0.0 pp] | 1.0000 |
| QwQ-32B | Luxel eval vs deploy framing | log_ans | 208 | +10% | [+2%, +20%] | 0.0223 |
| Olmo-3-32B-Think | EAB + user cue | vea_cot | 195 | +3.6 pp | [+1.0 pp, +6.2 pp] | 0.0142 |
| Olmo-3-32B-Think | EAB + user cue | refusal | 195 | +2.6 pp | [+0.0 pp, +5.1 pp] | 0.1261 |
| Olmo-3-32B-Think | EAB + user cue | log_ans | 195 | +4% | [-15%, +31%] | 0.7270 |
| Olmo-3-32B-Think | EAB + casual user cue | vea_cot | 195 | +32.3 pp | [+25.6 pp, +39.0 pp] | 0.0000 |
| Olmo-3-32B-Think | EAB + casual user cue | refusal | 195 | +6.7 pp | [+3.6 pp, +10.3 pp] | 0.0003 |
| Olmo-3-32B-Think | EAB + casual user cue | log_ans | 195 | -11% | [-31%, +13%] | 0.3210 |
| Olmo-3-32B-Think | Luxel eval vs deploy framing | vea_cot | 208 | +47.6 pp | [+40.4 pp, +54.8 pp] | 0.0000 |
| Olmo-3-32B-Think | Luxel eval vs deploy framing | refusal | 208 | -0.5 pp | [-1.4 pp, +0.0 pp] | 1.0000 |
| Olmo-3-32B-Think | Luxel eval vs deploy framing | log_ans | 208 | +13% | [+2%, +26%] | 0.0172 |
| Olmo-3.1-32B-Think | EAB + user cue | vea_cot | 195 | +24.1 pp | [+17.9 pp, +30.3 pp] | 0.0000 |
| Olmo-3.1-32B-Think | EAB + user cue | refusal | 195 | +7.2 pp | [+3.1 pp, +11.8 pp] | 0.0028 |
| Olmo-3.1-32B-Think | EAB + user cue | log_ans | 195 | -10% | [-29%, +16%] | 0.3970 |
| Olmo-3.1-32B-Think | EAB + casual user cue | vea_cot | 195 | +77.9 pp | [+71.8 pp, +83.6 pp] | 0.0000 |
| Olmo-3.1-32B-Think | EAB + casual user cue | refusal | 195 | +11.3 pp | [+7.2 pp, +15.9 pp] | 0.0000 |
| Olmo-3.1-32B-Think | EAB + casual user cue | log_ans | 195 | -15% | [-31%, +5%] | 0.1302 |
| Olmo-3.1-32B-Think | Luxel eval vs deploy framing | vea_cot | 208 | +43.3 pp | [+36.1 pp, +50.5 pp] | 0.0000 |
| Olmo-3.1-32B-Think | Luxel eval vs deploy framing | refusal | 208 | +0.0 pp | [+0.0 pp, +0.0 pp] | 1.0000 |
| Olmo-3.1-32B-Think | Luxel eval vs deploy framing | log_ans | 208 | +2% | [-7%, +12%] | 0.6361 |
| DeepSeek-R1-0528 (reference) | EAB + user cue | vea_cot | 195 | +29.7 pp | [+23.1 pp, +36.4 pp] | 0.0000 |
| DeepSeek-R1-0528 (reference) | EAB + user cue | refusal | 195 | +9.7 pp | [+5.6 pp, +14.4 pp] | 0.0000 |
| DeepSeek-R1-0528 (reference) | EAB + user cue | log_ans | 195 | -20% | [-24%, -15%] | 0.0000 |
| DeepSeek-R1-0528 (reference) | EAB + casual user cue | vea_cot | 195 | +72.3 pp | [+66.2 pp, +78.5 pp] | 0.0000 |
| DeepSeek-R1-0528 (reference) | EAB + casual user cue | refusal | 195 | +11.8 pp | [+7.7 pp, +16.4 pp] | 0.0000 |
| DeepSeek-R1-0528 (reference) | EAB + casual user cue | log_ans | 195 | -17% | [-21%, -12%] | 0.0000 |
| DeepSeek-R1-0528 (reference) | Luxel eval vs deploy framing | vea_cot | 208 | +64.9 pp | [+58.2 pp, +71.2 pp] | 0.0000 |
| DeepSeek-R1-0528 (reference) | Luxel eval vs deploy framing | refusal | 208 | +0.0 pp | [+0.0 pp, +0.0 pp] | 1.0000 |
| DeepSeek-R1-0528 (reference) | Luxel eval vs deploy framing | log_ans | 208 | +14% | [+5%, +24%] | 0.0013 |
| gpt-oss-20b (user-cue run, no Luxel; for comparison) | EAB + user cue | vea_cot | 195 | +2.3 pp | [+1.2 pp, +3.6 pp] | 0.0001 |
| gpt-oss-20b (user-cue run, no Luxel; for comparison) | EAB + user cue | refusal | 195 | +10.0 pp | [+6.9 pp, +13.2 pp] | 0.0000 |
| gpt-oss-20b (user-cue run, no Luxel; for comparison) | EAB + user cue | log_ans | 195 | -41% | [-50%, -31%] | 0.0000 |
| gpt-oss-20b (user-cue run, no Luxel; for comparison) | EAB + casual user cue | vea_cot | 195 | +6.7 pp | [+4.7 pp, +8.7 pp] | 0.0000 |
| gpt-oss-20b (user-cue run, no Luxel; for comparison) | EAB + casual user cue | refusal | 195 | +12.3 pp | [+8.8 pp, +16.0 pp] | 0.0000 |
| gpt-oss-20b (user-cue run, no Luxel; for comparison) | EAB + casual user cue | log_ans | 195 | -48% | [-56%, -38%] | 0.0000 |

## Selection rule (SCREEN_PLAN.md)

* Qwen3-32B: max explicit-cue VEA 15.9%, Luxel eval-framed VEA 56.2%; significant behavioural response to a user cue: yes -> PASSES
* QwQ-32B: max explicit-cue VEA 23.1%, Luxel eval-framed VEA 63.5%; significant behavioural response to a user cue: yes -> PASSES
* Olmo-3-32B-Think: max explicit-cue VEA 33.8%, Luxel eval-framed VEA 68.3%; significant behavioural response to a user cue: yes -> PASSES
* Olmo-3.1-32B-Think: max explicit-cue VEA 79.5%, Luxel eval-framed VEA 77.9%; significant behavioural response to a user cue: yes -> PASSES
* DeepSeek-R1-0528 (reference): max explicit-cue VEA 72.8%, Luxel eval-framed VEA 76.4%; significant behavioural response to a user cue: yes -> PASSES (reference only)
* gpt-oss-20b (user-cue run, no Luxel; for comparison): max explicit-cue VEA 6.7%, Luxel eval-framed VEA 0.0%; significant behavioural response to a user cue: yes -> fails (reference only)

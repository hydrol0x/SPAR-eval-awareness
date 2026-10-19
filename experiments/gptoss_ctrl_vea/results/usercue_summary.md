# User-turn cue experiment (PREREG_usercue.md)

## Qwen (primary)

### Levels (mean over prompts)

| model | outcome | none | dev_explicit | user_explicit | user_casual |
|---|---|---|---|---|---|
| base | VEA in reasoning (v4) | 0.0% | 0.1% | 2.3% | 6.7% |
| base | VEA anywhere (v4) | 0.0% | 0.3% | 2.3% | 6.7% |
| base | refusal rate | 42.3% | 49.4% | 52.3% | 54.6% |
| base | reasoning length | 1056 chars | 943 chars | 956 chars | 1010 chars |
| base | answer length | 578 chars | 405 chars | 342 chars | 302 chars |
| base | cue echo in reasoning (lexical) | 20.4% | 14.1% | 14.9% | 18.3% |
| control LoRA | VEA in reasoning (v4) | 0.0% | 0.0% | 0.1% | 2.2% |
| control LoRA | VEA anywhere (v4) | 0.1% | 0.0% | 0.1% | 2.2% |
| control LoRA | refusal rate | 39.9% | 45.8% | 46.3% | 50.3% |
| control LoRA | reasoning length | 1006 chars | 878 chars | 965 chars | 934 chars |
| control LoRA | answer length | 413 chars | 377 chars | 345 chars | 259 chars |
| control LoRA | cue echo in reasoning (lexical) | 15.0% | 10.0% | 11.7% | 13.2% |
| compliant LoRA | VEA in reasoning (v4) | 0.3% | 0.0% | 0.1% | 1.7% |
| compliant LoRA | VEA anywhere (v4) | 0.4% | 0.0% | 0.1% | 1.7% |
| compliant LoRA | refusal rate | 34.1% | 42.2% | 42.8% | 44.7% |
| compliant LoRA | reasoning length | 1305 chars | 1153 chars | 1199 chars | 1176 chars |
| compliant LoRA | answer length | 450 chars | 367 chars | 364 chars | 320 chars |
| compliant LoRA | cue echo in reasoning (lexical) | 25.0% | 19.7% | 19.7% | 21.8% |
| control vector | VEA in reasoning (v4) | 0.0% | 0.0% | 0.3% | 1.3% |
| control vector | VEA anywhere (v4) | 0.0% | 0.0% | 0.3% | 1.3% |
| control vector | refusal rate | 51.8% | 59.2% | 64.1% | 66.2% |
| control vector | reasoning length | 629 chars | 545 chars | 560 chars | 574 chars |
| control vector | answer length | 292 chars | 217 chars | 170 chars | 157 chars |
| control vector | cue echo in reasoning (lexical) | 8.1% | 3.6% | 4.1% | 6.2% |
| steering vector | VEA in reasoning (v4) | 0.0% | 0.0% | 2.2% | 3.3% |
| steering vector | VEA anywhere (v4) | 0.0% | 0.0% | 2.2% | 3.5% |
| steering vector | refusal rate | 43.2% | 51.2% | 54.4% | 57.3% |
| steering vector | reasoning length | 813 chars | 674 chars | 719 chars | 789 chars |
| steering vector | answer length | 460 chars | 321 chars | 272 chars | 241 chars |
| steering vector | cue echo in reasoning (lexical) | 17.2% | 10.5% | 11.9% | 14.2% |
| random vector | VEA in reasoning (v4) | 0.0% | 0.3% | 2.4% | 8.2% |
| random vector | VEA anywhere (v4) | 0.1% | 0.4% | 2.4% | 8.2% |
| random vector | refusal rate | 38.6% | 42.8% | 45.0% | 47.3% |
| random vector | reasoning length | 1352 chars | 1168 chars | 1274 chars | 1308 chars |
| random vector | answer length | 661 chars | 534 chars | 466 chars | 413 chars |
| random vector | cue echo in reasoning (lexical) | 26.4% | 19.9% | 23.6% | 28.3% |

### Pre-registered tests

| test | contrast | outcome | n prompts | a | b | a − b | 95% CI | p | p (Holm, family) |
|---|---|---|---|---|---|---|---|---|---|
| P0 | base: user_explicit − none | VEA in reasoning (v4) | 195 | 2.3% | 0.0% | +2.3 pp | [+1.2 pp, +3.6 pp] | 0.0001 | 0.0001 |
| P1 | compliant LoRA − control LoRA, user_explicit | VEA in reasoning (v4) | 195 | 0.1% | 0.1% | +0.0 pp | [-0.4 pp, +0.4 pp] | 1.0000 | 1.0000 |
| P2 | steering vector − control vector, user_explicit | VEA in reasoning (v4) | 195 | 2.2% | 0.3% | +1.9 pp | [+0.9 pp, +3.1 pp] | 0.0011 | 0.0023 |
| S1.1 | compliant LoRA − control LoRA, user_casual | VEA in reasoning (v4) | 195 | 1.7% | 2.2% | -0.5 pp | [-2.1 pp, +0.9 pp] | 0.6123 | 1.0000 |
| S2.1 | compliant LoRA − control LoRA, cue effect (user_explicit − none) | VEA in reasoning (v4) | 195 | -0.1 pp | +0.1 pp | -0.3 pp | [-0.8 pp, +0.3 pp] | 0.6244 | 1.0000 |
| S3.1-refusal | compliant LoRA − control LoRA, cue effect (user_explicit − none) | refusal rate | 195 | +8.7 pp | +6.4 pp | +2.3 pp | [-0.1 pp, +4.9 pp] | 0.0949 | 0.5691 |
| S3.1-log_ans | compliant LoRA − control LoRA, cue effect (user_explicit − none) | answer length | 195 | -19% | -16% | -3% | [-21%, +20%] | 0.7651 | 1.0000 |
| S1.2 | steering vector − control vector, user_casual | VEA in reasoning (v4) | 195 | 3.3% | 1.3% | +2.1 pp | [+0.4 pp, +3.7 pp] | 0.0207 | 0.1446 |
| S2.2 | steering vector − control vector, cue effect (user_explicit − none) | VEA in reasoning (v4) | 195 | +2.2 pp | +0.3 pp | +1.9 pp | [+0.9 pp, +3.1 pp] | 0.0013 | 0.0104 |
| S3.2-refusal | steering vector − control vector, cue effect (user_explicit − none) | refusal rate | 195 | +11.2 pp | +12.3 pp | -1.2 pp | [-4.7 pp, +2.3 pp] | 0.5704 | 1.0000 |
| S3.2-log_ans | steering vector − control vector, cue effect (user_explicit − none) | answer length | 195 | -41% | -41% | +1% | [-14%, +19%] | 0.8911 | 1.0000 |

### Cue effects within each model (cue − none, paired by prompt; descriptive)

| model | cue | outcome | cue effect | 95% CI | p |
|---|---|---|---|---|---|
| base | dev_explicit | VEA in reasoning (v4) | +0.1 pp | [+0.0 pp, +0.4 pp] | 1.0000 |
| base | dev_explicit | VEA anywhere (v4) | +0.3 pp | [+0.0 pp, +0.8 pp] | 1.0000 |
| base | dev_explicit | refusal rate | +7.1 pp | [+4.4 pp, +9.9 pp] | 0.0000 |
| base | dev_explicit | reasoning length | -11% | [-17%, -4%] | 0.0027 |
| base | dev_explicit | answer length | -30% | [-39%, -20%] | 0.0000 |
| base | dev_explicit | cue echo in reasoning (lexical) | -6.3 pp | [-9.4 pp, -3.2 pp] | 0.0001 |
| base | user_explicit | VEA in reasoning (v4) | +2.3 pp | [+1.3 pp, +3.6 pp] | 0.0001 |
| base | user_explicit | VEA anywhere (v4) | +2.3 pp | [+1.3 pp, +3.6 pp] | 0.0001 |
| base | user_explicit | refusal rate | +10.0 pp | [+6.9 pp, +13.2 pp] | 0.0000 |
| base | user_explicit | reasoning length | -9% | [-15%, -3%] | 0.0047 |
| base | user_explicit | answer length | -41% | [-50%, -31%] | 0.0000 |
| base | user_explicit | cue echo in reasoning (lexical) | -5.5 pp | [-9.1 pp, -1.9 pp] | 0.0037 |
| base | user_casual | VEA in reasoning (v4) | +6.7 pp | [+4.7 pp, +8.7 pp] | 0.0000 |
| base | user_casual | VEA anywhere (v4) | +6.7 pp | [+4.7 pp, +8.7 pp] | 0.0000 |
| base | user_casual | refusal rate | +12.3 pp | [+8.8 pp, +16.0 pp] | 0.0000 |
| base | user_casual | reasoning length | -4% | [-11%, +3%] | 0.2407 |
| base | user_casual | answer length | -48% | [-56%, -38%] | 0.0000 |
| base | user_casual | cue echo in reasoning (lexical) | -2.1 pp | [-6.2 pp, +1.9 pp] | 0.3449 |
| control LoRA | dev_explicit | VEA in reasoning (v4) | +0.0 pp | [+0.0 pp, +0.0 pp] | 1.0000 |
| control LoRA | dev_explicit | VEA anywhere (v4) | -0.1 pp | [-0.4 pp, +0.0 pp] | 1.0000 |
| control LoRA | dev_explicit | refusal rate | +5.9 pp | [+3.5 pp, +8.6 pp] | 0.0000 |
| control LoRA | dev_explicit | reasoning length | -13% | [-21%, -5%] | 0.0039 |
| control LoRA | dev_explicit | answer length | -9% | [-23%, +9%] | 0.3044 |
| control LoRA | dev_explicit | cue echo in reasoning (lexical) | -5.0 pp | [-7.8 pp, -2.3 pp] | 0.0003 |
| control LoRA | user_explicit | VEA in reasoning (v4) | +0.1 pp | [+0.0 pp, +0.4 pp] | 1.0000 |
| control LoRA | user_explicit | VEA anywhere (v4) | +0.0 pp | [-0.4 pp, +0.4 pp] | 1.0000 |
| control LoRA | user_explicit | refusal rate | +6.4 pp | [+3.7 pp, +9.4 pp] | 0.0000 |
| control LoRA | user_explicit | reasoning length | -4% | [-14%, +7%] | 0.4454 |
| control LoRA | user_explicit | answer length | -16% | [-29%, -1%] | 0.0386 |
| control LoRA | user_explicit | cue echo in reasoning (lexical) | -3.3 pp | [-6.0 pp, -0.8 pp] | 0.0182 |
| control LoRA | user_casual | VEA in reasoning (v4) | +2.2 pp | [+0.9 pp, +3.7 pp] | 0.0006 |
| control LoRA | user_casual | VEA anywhere (v4) | +2.1 pp | [+0.8 pp, +3.6 pp] | 0.0027 |
| control LoRA | user_casual | refusal rate | +10.4 pp | [+7.1 pp, +14.0 pp] | 0.0000 |
| control LoRA | user_casual | reasoning length | -7% | [-17%, +3%] | 0.1871 |
| control LoRA | user_casual | answer length | -37% | [-50%, -23%] | 0.0000 |
| control LoRA | user_casual | cue echo in reasoning (lexical) | -1.8 pp | [-5.1 pp, +1.5 pp] | 0.3345 |
| compliant LoRA | dev_explicit | VEA in reasoning (v4) | -0.3 pp | [-0.6 pp, +0.0 pp] | 0.5047 |
| compliant LoRA | dev_explicit | VEA anywhere (v4) | -0.4 pp | [-0.9 pp, +0.0 pp] | 0.2442 |
| compliant LoRA | dev_explicit | refusal rate | +8.1 pp | [+5.4 pp, +11.2 pp] | 0.0000 |
| compliant LoRA | dev_explicit | reasoning length | -12% | [-21%, -2%] | 0.0222 |
| compliant LoRA | dev_explicit | answer length | -18% | [-33%, -2%] | 0.0355 |
| compliant LoRA | dev_explicit | cue echo in reasoning (lexical) | -5.3 pp | [-8.2 pp, -2.3 pp] | 0.0009 |
| compliant LoRA | user_explicit | VEA in reasoning (v4) | -0.1 pp | [-0.6 pp, +0.3 pp] | 1.0000 |
| compliant LoRA | user_explicit | VEA anywhere (v4) | -0.3 pp | [-0.8 pp, +0.3 pp] | 0.6287 |
| compliant LoRA | user_explicit | refusal rate | +8.7 pp | [+5.9 pp, +11.7 pp] | 0.0000 |
| compliant LoRA | user_explicit | reasoning length | -8% | [-17%, +2%] | 0.1150 |
| compliant LoRA | user_explicit | answer length | -19% | [-32%, -3%] | 0.0213 |
| compliant LoRA | user_explicit | cue echo in reasoning (lexical) | -5.3 pp | [-8.3 pp, -2.3 pp] | 0.0011 |
| compliant LoRA | user_casual | VEA in reasoning (v4) | +1.4 pp | [+0.5 pp, +2.3 pp] | 0.0033 |
| compliant LoRA | user_casual | VEA anywhere (v4) | +1.3 pp | [+0.4 pp, +2.2 pp] | 0.0128 |
| compliant LoRA | user_casual | refusal rate | +10.6 pp | [+7.6 pp, +14.1 pp] | 0.0000 |
| compliant LoRA | user_casual | reasoning length | -10% | [-21%, +2%] | 0.1154 |
| compliant LoRA | user_casual | answer length | -29% | [-41%, -14%] | 0.0004 |
| compliant LoRA | user_casual | cue echo in reasoning (lexical) | -3.2 pp | [-7.1 pp, +0.5 pp] | 0.1139 |
| control vector | dev_explicit | VEA in reasoning (v4) | +0.0 pp | [+0.0 pp, +0.0 pp] | 1.0000 |
| control vector | dev_explicit | VEA anywhere (v4) | +0.0 pp | [+0.0 pp, +0.0 pp] | 1.0000 |
| control vector | dev_explicit | refusal rate | +7.4 pp | [+4.7 pp, +10.3 pp] | 0.0000 |
| control vector | dev_explicit | reasoning length | -13% | [-19%, -7%] | 0.0001 |
| control vector | dev_explicit | answer length | -25% | [-34%, -17%] | 0.0000 |
| control vector | dev_explicit | cue echo in reasoning (lexical) | -4.5 pp | [-6.8 pp, -2.6 pp] | 0.0000 |
| control vector | user_explicit | VEA in reasoning (v4) | +0.3 pp | [+0.0 pp, +0.6 pp] | 0.5053 |
| control vector | user_explicit | VEA anywhere (v4) | +0.3 pp | [+0.0 pp, +0.6 pp] | 0.5039 |
| control vector | user_explicit | refusal rate | +12.3 pp | [+8.6 pp, +16.2 pp] | 0.0000 |
| control vector | user_explicit | reasoning length | -11% | [-17%, -4%] | 0.0021 |
| control vector | user_explicit | answer length | -41% | [-50%, -32%] | 0.0000 |
| control vector | user_explicit | cue echo in reasoning (lexical) | -4.0 pp | [-6.3 pp, -1.9 pp] | 0.0003 |
| control vector | user_casual | VEA in reasoning (v4) | +1.3 pp | [+0.5 pp, +2.2 pp] | 0.0037 |
| control vector | user_casual | VEA anywhere (v4) | +1.3 pp | [+0.5 pp, +2.2 pp] | 0.0027 |
| control vector | user_casual | refusal rate | +14.4 pp | [+10.5 pp, +18.2 pp] | 0.0000 |
| control vector | user_casual | reasoning length | -9% | [-15%, -2%] | 0.0146 |
| control vector | user_casual | answer length | -46% | [-54%, -37%] | 0.0000 |
| control vector | user_casual | cue echo in reasoning (lexical) | -1.9 pp | [-4.4 pp, +0.4 pp] | 0.1326 |
| steering vector | dev_explicit | VEA in reasoning (v4) | +0.0 pp | [+0.0 pp, +0.0 pp] | 1.0000 |
| steering vector | dev_explicit | VEA anywhere (v4) | +0.0 pp | [+0.0 pp, +0.0 pp] | 1.0000 |
| steering vector | dev_explicit | refusal rate | +7.9 pp | [+5.3 pp, +10.8 pp] | 0.0000 |
| steering vector | dev_explicit | reasoning length | -17% | [-24%, -9%] | 0.0001 |
| steering vector | dev_explicit | answer length | -30% | [-38%, -22%] | 0.0000 |
| steering vector | dev_explicit | cue echo in reasoning (lexical) | -6.7 pp | [-10.1 pp, -3.3 pp] | 0.0001 |
| steering vector | user_explicit | VEA in reasoning (v4) | +2.2 pp | [+1.2 pp, +3.3 pp] | 0.0001 |
| steering vector | user_explicit | VEA anywhere (v4) | +2.2 pp | [+1.2 pp, +3.3 pp] | 0.0000 |
| steering vector | user_explicit | refusal rate | +11.2 pp | [+8.1 pp, +14.4 pp] | 0.0000 |
| steering vector | user_explicit | reasoning length | -12% | [-20%, -3%] | 0.0135 |
| steering vector | user_explicit | answer length | -41% | [-49%, -32%] | 0.0000 |
| steering vector | user_explicit | cue echo in reasoning (lexical) | -5.3 pp | [-8.7 pp, -1.9 pp] | 0.0033 |
| steering vector | user_casual | VEA in reasoning (v4) | +3.3 pp | [+2.1 pp, +4.7 pp] | 0.0000 |
| steering vector | user_casual | VEA anywhere (v4) | +3.5 pp | [+2.2 pp, +4.9 pp] | 0.0000 |
| steering vector | user_casual | refusal rate | +14.1 pp | [+10.6 pp, +17.7 pp] | 0.0000 |
| steering vector | user_casual | reasoning length | -3% | [-11%, +6%] | 0.5158 |
| steering vector | user_casual | answer length | -48% | [-55%, -39%] | 0.0000 |
| steering vector | user_casual | cue echo in reasoning (lexical) | -2.9 pp | [-6.4 pp, +0.4 pp] | 0.1013 |
| random vector | dev_explicit | VEA in reasoning (v4) | +0.3 pp | [+0.0 pp, +0.6 pp] | 0.5008 |
| random vector | dev_explicit | VEA anywhere (v4) | +0.3 pp | [-0.3 pp, +0.8 pp] | 0.6239 |
| random vector | dev_explicit | refusal rate | +4.2 pp | [+1.8 pp, +6.9 pp] | 0.0016 |
| random vector | dev_explicit | reasoning length | -14% | [-19%, -8%] | 0.0000 |
| random vector | dev_explicit | answer length | -19% | [-29%, -9%] | 0.0004 |
| random vector | dev_explicit | cue echo in reasoning (lexical) | -6.5 pp | [-10.3 pp, -2.8 pp] | 0.0006 |
| random vector | user_explicit | VEA in reasoning (v4) | +2.4 pp | [+1.4 pp, +3.6 pp] | 0.0000 |
| random vector | user_explicit | VEA anywhere (v4) | +2.3 pp | [+1.3 pp, +3.5 pp] | 0.0002 |
| random vector | user_explicit | refusal rate | +6.4 pp | [+4.0 pp, +9.0 pp] | 0.0000 |
| random vector | user_explicit | reasoning length | -6% | [-12%, +1%] | 0.1020 |
| random vector | user_explicit | answer length | -30% | [-38%, -21%] | 0.0000 |
| random vector | user_explicit | cue echo in reasoning (lexical) | -2.8 pp | [-6.0 pp, +0.4 pp] | 0.1027 |
| random vector | user_casual | VEA in reasoning (v4) | +8.2 pp | [+6.2 pp, +10.4 pp] | 0.0000 |
| random vector | user_casual | VEA anywhere (v4) | +8.1 pp | [+6.0 pp, +10.3 pp] | 0.0000 |
| random vector | user_casual | refusal rate | +8.7 pp | [+6.0 pp, +11.7 pp] | 0.0000 |
| random vector | user_casual | reasoning length | -3% | [-10%, +4%] | 0.3743 |
| random vector | user_casual | answer length | -38% | [-46%, -29%] | 0.0000 |
| random vector | user_casual | cue echo in reasoning (lexical) | +1.9 pp | [-2.1 pp, +5.9 pp] | 0.3788 |

### Decision: "verbalizes less while the behavioural response is preserved"

* compliant LoRA vs control LoRA: verbalization not significantly lower; behaviour refusal rate: preserved, answer length: preserved.
* steering vector vs control vector: verbalization not significantly lower; behaviour refusal rate: preserved, answer length: preserved.

## DeepSeek (robustness)

### Levels (mean over prompts)

| model | outcome | none | dev_explicit | user_explicit | user_casual |
|---|---|---|---|---|---|
| base | VEA in reasoning (v4) | 0.0% | 0.1% | 2.2% | 6.5% |
| base | VEA anywhere (v4) | 0.1% | 0.1% | 2.3% | 6.5% |
| base | refusal rate | 42.3% | 49.4% | 52.3% | 54.6% |
| base | reasoning length | 1056 chars | 943 chars | 956 chars | 1010 chars |
| base | answer length | 578 chars | 405 chars | 342 chars | 302 chars |
| base | cue echo in reasoning (lexical) | 20.4% | 14.1% | 14.9% | 18.3% |
| control LoRA | VEA in reasoning (v4) | 0.0% | 0.0% | 0.1% | 1.3% |
| control LoRA | VEA anywhere (v4) | 0.0% | 0.0% | 0.1% | 1.4% |
| control LoRA | refusal rate | 39.9% | 45.8% | 46.3% | 50.3% |
| control LoRA | reasoning length | 1006 chars | 878 chars | 965 chars | 934 chars |
| control LoRA | answer length | 413 chars | 377 chars | 345 chars | 259 chars |
| control LoRA | cue echo in reasoning (lexical) | 15.0% | 10.0% | 11.7% | 13.2% |
| compliant LoRA | VEA in reasoning (v4) | 0.0% | 0.0% | 0.1% | 1.3% |
| compliant LoRA | VEA anywhere (v4) | 0.0% | 0.0% | 0.1% | 1.3% |
| compliant LoRA | refusal rate | 34.1% | 42.2% | 42.8% | 44.7% |
| compliant LoRA | reasoning length | 1305 chars | 1153 chars | 1199 chars | 1176 chars |
| compliant LoRA | answer length | 450 chars | 367 chars | 364 chars | 320 chars |
| compliant LoRA | cue echo in reasoning (lexical) | 25.0% | 19.7% | 19.7% | 21.8% |
| control vector | VEA in reasoning (v4) | 0.0% | 0.0% | 0.3% | 1.0% |
| control vector | VEA anywhere (v4) | 0.0% | 0.0% | 0.3% | 1.2% |
| control vector | refusal rate | 51.8% | 59.2% | 64.1% | 66.2% |
| control vector | reasoning length | 629 chars | 545 chars | 560 chars | 574 chars |
| control vector | answer length | 292 chars | 217 chars | 170 chars | 157 chars |
| control vector | cue echo in reasoning (lexical) | 8.1% | 3.6% | 4.1% | 6.2% |
| steering vector | VEA in reasoning (v4) | 0.0% | 0.1% | 2.3% | 3.3% |
| steering vector | VEA anywhere (v4) | 0.0% | 0.1% | 2.3% | 3.3% |
| steering vector | refusal rate | 43.2% | 51.2% | 54.4% | 57.3% |
| steering vector | reasoning length | 813 chars | 674 chars | 719 chars | 789 chars |
| steering vector | answer length | 460 chars | 321 chars | 272 chars | 241 chars |
| steering vector | cue echo in reasoning (lexical) | 17.2% | 10.5% | 11.9% | 14.2% |
| random vector | VEA in reasoning (v4) | 0.1% | 0.3% | 2.3% | 7.3% |
| random vector | VEA anywhere (v4) | 0.3% | 0.3% | 2.3% | 7.3% |
| random vector | refusal rate | 38.6% | 42.8% | 45.0% | 47.3% |
| random vector | reasoning length | 1352 chars | 1168 chars | 1274 chars | 1308 chars |
| random vector | answer length | 661 chars | 534 chars | 466 chars | 413 chars |
| random vector | cue echo in reasoning (lexical) | 26.4% | 19.9% | 23.6% | 28.3% |

### Pre-registered tests

| test | contrast | outcome | n prompts | a | b | a − b | 95% CI | p | p (Holm, family) |
|---|---|---|---|---|---|---|---|---|---|
| P0 | base: user_explicit − none | VEA in reasoning (v4) | 195 | 2.2% | 0.0% | +2.2 pp | [+1.2 pp, +3.5 pp] | 0.0001 | 0.0001 |
| P1 | compliant LoRA − control LoRA, user_explicit | VEA in reasoning (v4) | 195 | 0.1% | 0.1% | +0.0 pp | [-0.4 pp, +0.4 pp] | 1.0000 | 1.0000 |
| P2 | steering vector − control vector, user_explicit | VEA in reasoning (v4) | 195 | 2.3% | 0.3% | +2.1 pp | [+1.0 pp, +3.2 pp] | 0.0007 | 0.0014 |
| S1.1 | compliant LoRA − control LoRA, user_casual | VEA in reasoning (v4) | 195 | 1.3% | 1.3% | +0.0 pp | [-1.2 pp, +1.2 pp] | 1.0000 | 1.0000 |
| S2.1 | compliant LoRA − control LoRA, cue effect (user_explicit − none) | VEA in reasoning (v4) | 195 | +0.1 pp | +0.1 pp | +0.0 pp | [-0.4 pp, +0.4 pp] | 1.0000 | 1.0000 |
| S3.1-refusal | compliant LoRA − control LoRA, cue effect (user_explicit − none) | refusal rate | 195 | +8.7 pp | +6.4 pp | +2.3 pp | [-0.3 pp, +4.9 pp] | 0.0964 | 0.5784 |
| S3.1-log_ans | compliant LoRA − control LoRA, cue effect (user_explicit − none) | answer length | 195 | -19% | -16% | -3% | [-21%, +19%] | 0.7582 | 1.0000 |
| S1.2 | steering vector − control vector, user_casual | VEA in reasoning (v4) | 195 | 3.3% | 1.0% | +2.3 pp | [+0.6 pp, +4.0 pp] | 0.0063 | 0.0441 |
| S2.2 | steering vector − control vector, cue effect (user_explicit − none) | VEA in reasoning (v4) | 195 | +2.3 pp | +0.3 pp | +2.1 pp | [+1.0 pp, +3.2 pp] | 0.0008 | 0.0064 |
| S3.2-refusal | steering vector − control vector, cue effect (user_explicit − none) | refusal rate | 195 | +11.2 pp | +12.3 pp | -1.2 pp | [-4.7 pp, +2.3 pp] | 0.5709 | 1.0000 |
| S3.2-log_ans | steering vector − control vector, cue effect (user_explicit − none) | answer length | 195 | -41% | -41% | +1% | [-14%, +18%] | 0.8943 | 1.0000 |

### Cue effects within each model (cue − none, paired by prompt; descriptive)

| model | cue | outcome | cue effect | 95% CI | p |
|---|---|---|---|---|---|
| base | dev_explicit | VEA in reasoning (v4) | +0.1 pp | [+0.0 pp, +0.4 pp] | 1.0000 |
| base | dev_explicit | VEA anywhere (v4) | +0.0 pp | [-0.4 pp, +0.4 pp] | 1.0000 |
| base | dev_explicit | refusal rate | +7.1 pp | [+4.5 pp, +9.9 pp] | 0.0000 |
| base | dev_explicit | reasoning length | -11% | [-17%, -4%] | 0.0020 |
| base | dev_explicit | answer length | -30% | [-39%, -20%] | 0.0000 |
| base | dev_explicit | cue echo in reasoning (lexical) | -6.3 pp | [-9.4 pp, -3.1 pp] | 0.0001 |
| base | user_explicit | VEA in reasoning (v4) | +2.2 pp | [+1.2 pp, +3.5 pp] | 0.0000 |
| base | user_explicit | VEA anywhere (v4) | +2.2 pp | [+1.0 pp, +3.5 pp] | 0.0001 |
| base | user_explicit | refusal rate | +10.0 pp | [+6.9 pp, +13.3 pp] | 0.0000 |
| base | user_explicit | reasoning length | -9% | [-15%, -3%] | 0.0053 |
| base | user_explicit | answer length | -41% | [-50%, -31%] | 0.0000 |
| base | user_explicit | cue echo in reasoning (lexical) | -5.5 pp | [-9.1 pp, -2.1 pp] | 0.0043 |
| base | user_casual | VEA in reasoning (v4) | +6.5 pp | [+4.7 pp, +8.6 pp] | 0.0000 |
| base | user_casual | VEA anywhere (v4) | +6.4 pp | [+4.6 pp, +8.5 pp] | 0.0000 |
| base | user_casual | refusal rate | +12.3 pp | [+8.8 pp, +16.0 pp] | 0.0000 |
| base | user_casual | reasoning length | -4% | [-11%, +3%] | 0.2418 |
| base | user_casual | answer length | -48% | [-56%, -38%] | 0.0000 |
| base | user_casual | cue echo in reasoning (lexical) | -2.1 pp | [-6.2 pp, +1.9 pp] | 0.3468 |
| control LoRA | dev_explicit | VEA in reasoning (v4) | +0.0 pp | [+0.0 pp, +0.0 pp] | 1.0000 |
| control LoRA | dev_explicit | VEA anywhere (v4) | +0.0 pp | [+0.0 pp, +0.0 pp] | 1.0000 |
| control LoRA | dev_explicit | refusal rate | +5.9 pp | [+3.5 pp, +8.6 pp] | 0.0000 |
| control LoRA | dev_explicit | reasoning length | -13% | [-21%, -5%] | 0.0034 |
| control LoRA | dev_explicit | answer length | -9% | [-23%, +8%] | 0.3030 |
| control LoRA | dev_explicit | cue echo in reasoning (lexical) | -5.0 pp | [-7.9 pp, -2.3 pp] | 0.0005 |
| control LoRA | user_explicit | VEA in reasoning (v4) | +0.1 pp | [+0.0 pp, +0.4 pp] | 1.0000 |
| control LoRA | user_explicit | VEA anywhere (v4) | +0.1 pp | [+0.0 pp, +0.4 pp] | 1.0000 |
| control LoRA | user_explicit | refusal rate | +6.4 pp | [+3.7 pp, +9.4 pp] | 0.0000 |
| control LoRA | user_explicit | reasoning length | -4% | [-14%, +7%] | 0.4455 |
| control LoRA | user_explicit | answer length | -16% | [-29%, -1%] | 0.0371 |
| control LoRA | user_explicit | cue echo in reasoning (lexical) | -3.3 pp | [-6.0 pp, -0.8 pp] | 0.0167 |
| control LoRA | user_casual | VEA in reasoning (v4) | +1.3 pp | [+0.5 pp, +2.3 pp] | 0.0075 |
| control LoRA | user_casual | VEA anywhere (v4) | +1.4 pp | [+0.5 pp, +2.4 pp] | 0.0034 |
| control LoRA | user_casual | refusal rate | +10.4 pp | [+7.1 pp, +14.0 pp] | 0.0000 |
| control LoRA | user_casual | reasoning length | -7% | [-17%, +3%] | 0.1807 |
| control LoRA | user_casual | answer length | -37% | [-50%, -22%] | 0.0000 |
| control LoRA | user_casual | cue echo in reasoning (lexical) | -1.8 pp | [-5.1 pp, +1.4 pp] | 0.3258 |
| compliant LoRA | dev_explicit | VEA in reasoning (v4) | +0.0 pp | [+0.0 pp, +0.0 pp] | 1.0000 |
| compliant LoRA | dev_explicit | VEA anywhere (v4) | +0.0 pp | [+0.0 pp, +0.0 pp] | 1.0000 |
| compliant LoRA | dev_explicit | refusal rate | +8.1 pp | [+5.5 pp, +11.0 pp] | 0.0000 |
| compliant LoRA | dev_explicit | reasoning length | -12% | [-20%, -2%] | 0.0216 |
| compliant LoRA | dev_explicit | answer length | -18% | [-33%, -2%] | 0.0377 |
| compliant LoRA | dev_explicit | cue echo in reasoning (lexical) | -5.3 pp | [-8.2 pp, -2.3 pp] | 0.0007 |
| compliant LoRA | user_explicit | VEA in reasoning (v4) | +0.1 pp | [+0.0 pp, +0.4 pp] | 1.0000 |
| compliant LoRA | user_explicit | VEA anywhere (v4) | +0.1 pp | [+0.0 pp, +0.4 pp] | 1.0000 |
| compliant LoRA | user_explicit | refusal rate | +8.7 pp | [+6.0 pp, +11.7 pp] | 0.0000 |
| compliant LoRA | user_explicit | reasoning length | -8% | [-17%, +2%] | 0.1181 |
| compliant LoRA | user_explicit | answer length | -19% | [-32%, -3%] | 0.0213 |
| compliant LoRA | user_explicit | cue echo in reasoning (lexical) | -5.3 pp | [-8.3 pp, -2.3 pp] | 0.0010 |
| compliant LoRA | user_casual | VEA in reasoning (v4) | +1.3 pp | [+0.5 pp, +2.1 pp] | 0.0023 |
| compliant LoRA | user_casual | VEA anywhere (v4) | +1.3 pp | [+0.5 pp, +2.1 pp] | 0.0019 |
| compliant LoRA | user_casual | refusal rate | +10.6 pp | [+7.4 pp, +14.1 pp] | 0.0000 |
| compliant LoRA | user_casual | reasoning length | -10% | [-21%, +2%] | 0.1242 |
| compliant LoRA | user_casual | answer length | -29% | [-41%, -14%] | 0.0005 |
| compliant LoRA | user_casual | cue echo in reasoning (lexical) | -3.2 pp | [-7.1 pp, +0.5 pp] | 0.1111 |
| control vector | dev_explicit | VEA in reasoning (v4) | +0.0 pp | [+0.0 pp, +0.0 pp] | 1.0000 |
| control vector | dev_explicit | VEA anywhere (v4) | +0.0 pp | [+0.0 pp, +0.0 pp] | 1.0000 |
| control vector | dev_explicit | refusal rate | +7.4 pp | [+4.6 pp, +10.4 pp] | 0.0000 |
| control vector | dev_explicit | reasoning length | -13% | [-19%, -7%] | 0.0002 |
| control vector | dev_explicit | answer length | -25% | [-34%, -16%] | 0.0000 |
| control vector | dev_explicit | cue echo in reasoning (lexical) | -4.5 pp | [-6.7 pp, -2.4 pp] | 0.0000 |
| control vector | user_explicit | VEA in reasoning (v4) | +0.3 pp | [+0.0 pp, +0.6 pp] | 0.5038 |
| control vector | user_explicit | VEA anywhere (v4) | +0.3 pp | [+0.0 pp, +0.6 pp] | 0.5016 |
| control vector | user_explicit | refusal rate | +12.3 pp | [+8.7 pp, +16.2 pp] | 0.0000 |
| control vector | user_explicit | reasoning length | -11% | [-17%, -4%] | 0.0024 |
| control vector | user_explicit | answer length | -41% | [-50%, -32%] | 0.0000 |
| control vector | user_explicit | cue echo in reasoning (lexical) | -4.0 pp | [-6.2 pp, -1.9 pp] | 0.0003 |
| control vector | user_casual | VEA in reasoning (v4) | +1.0 pp | [+0.4 pp, +1.9 pp] | 0.0155 |
| control vector | user_casual | VEA anywhere (v4) | +1.2 pp | [+0.4 pp, +2.1 pp] | 0.0081 |
| control vector | user_casual | refusal rate | +14.4 pp | [+10.5 pp, +18.2 pp] | 0.0000 |
| control vector | user_casual | reasoning length | -9% | [-15%, -2%] | 0.0145 |
| control vector | user_casual | answer length | -46% | [-54%, -37%] | 0.0000 |
| control vector | user_casual | cue echo in reasoning (lexical) | -1.9 pp | [-4.2 pp, +0.4 pp] | 0.1342 |
| steering vector | dev_explicit | VEA in reasoning (v4) | +0.1 pp | [+0.0 pp, +0.4 pp] | 1.0000 |
| steering vector | dev_explicit | VEA anywhere (v4) | +0.1 pp | [+0.0 pp, +0.4 pp] | 1.0000 |
| steering vector | dev_explicit | refusal rate | +7.9 pp | [+5.3 pp, +10.9 pp] | 0.0000 |
| steering vector | dev_explicit | reasoning length | -17% | [-24%, -9%] | 0.0001 |
| steering vector | dev_explicit | answer length | -30% | [-39%, -22%] | 0.0000 |
| steering vector | dev_explicit | cue echo in reasoning (lexical) | -6.7 pp | [-10.1 pp, -3.2 pp] | 0.0003 |
| steering vector | user_explicit | VEA in reasoning (v4) | +2.3 pp | [+1.3 pp, +3.5 pp] | 0.0001 |
| steering vector | user_explicit | VEA anywhere (v4) | +2.3 pp | [+1.3 pp, +3.5 pp] | 0.0000 |
| steering vector | user_explicit | refusal rate | +11.2 pp | [+8.1 pp, +14.4 pp] | 0.0000 |
| steering vector | user_explicit | reasoning length | -12% | [-20%, -3%] | 0.0128 |
| steering vector | user_explicit | answer length | -41% | [-49%, -32%] | 0.0000 |
| steering vector | user_explicit | cue echo in reasoning (lexical) | -5.3 pp | [-8.7 pp, -1.9 pp] | 0.0034 |
| steering vector | user_casual | VEA in reasoning (v4) | +3.3 pp | [+2.1 pp, +4.7 pp] | 0.0000 |
| steering vector | user_casual | VEA anywhere (v4) | +3.3 pp | [+2.1 pp, +4.7 pp] | 0.0000 |
| steering vector | user_casual | refusal rate | +14.1 pp | [+10.6 pp, +17.7 pp] | 0.0000 |
| steering vector | user_casual | reasoning length | -3% | [-12%, +6%] | 0.5186 |
| steering vector | user_casual | answer length | -48% | [-55%, -39%] | 0.0000 |
| steering vector | user_casual | cue echo in reasoning (lexical) | -2.9 pp | [-6.4 pp, +0.3 pp] | 0.0999 |
| random vector | dev_explicit | VEA in reasoning (v4) | +0.1 pp | [-0.3 pp, +0.6 pp] | 1.0000 |
| random vector | dev_explicit | VEA anywhere (v4) | +0.0 pp | [-0.5 pp, +0.5 pp] | 1.0000 |
| random vector | dev_explicit | refusal rate | +4.2 pp | [+1.7 pp, +6.9 pp] | 0.0016 |
| random vector | dev_explicit | reasoning length | -14% | [-19%, -7%] | 0.0001 |
| random vector | dev_explicit | answer length | -19% | [-29%, -9%] | 0.0003 |
| random vector | dev_explicit | cue echo in reasoning (lexical) | -6.5 pp | [-10.3 pp, -2.8 pp] | 0.0009 |
| random vector | user_explicit | VEA in reasoning (v4) | +2.2 pp | [+1.2 pp, +3.3 pp] | 0.0000 |
| random vector | user_explicit | VEA anywhere (v4) | +2.1 pp | [+1.0 pp, +3.2 pp] | 0.0000 |
| random vector | user_explicit | refusal rate | +6.4 pp | [+4.0 pp, +9.0 pp] | 0.0000 |
| random vector | user_explicit | reasoning length | -6% | [-12%, +1%] | 0.0956 |
| random vector | user_explicit | answer length | -30% | [-38%, -21%] | 0.0000 |
| random vector | user_explicit | cue echo in reasoning (lexical) | -2.8 pp | [-6.0 pp, +0.5 pp] | 0.1029 |
| random vector | user_casual | VEA in reasoning (v4) | +7.2 pp | [+5.3 pp, +9.2 pp] | 0.0000 |
| random vector | user_casual | VEA anywhere (v4) | +7.1 pp | [+5.1 pp, +9.1 pp] | 0.0000 |
| random vector | user_casual | refusal rate | +8.7 pp | [+6.0 pp, +11.7 pp] | 0.0000 |
| random vector | user_casual | reasoning length | -3% | [-10%, +4%] | 0.3720 |
| random vector | user_casual | answer length | -38% | [-46%, -28%] | 0.0000 |
| random vector | user_casual | cue echo in reasoning (lexical) | +1.9 pp | [-2.1 pp, +5.9 pp] | 0.3781 |

### Decision: "verbalizes less while the behavioural response is preserved"

* compliant LoRA vs control LoRA: verbalization not significantly lower; behaviour refusal rate: preserved, answer length: preserved.
* steering vector vs control vector: verbalization not significantly lower; behaviour refusal rate: preserved, answer length: preserved.


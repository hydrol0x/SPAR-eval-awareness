# Cue effect on behaviour vs verbalization, per model and between models

Cue effect = mean over prompts of (with cue − without cue), paired by prompt; lengths are geometric-mean ratios. p: sign-flip permutation; Holm-adjusted within each table over all its rows.

## dev-message cue, capability: cue effect within each model

| model | outcome | n prompts | cue effect | 95% CI | p | p (Holm) |
|---|---|---|---|---|---|---|
| base | refusal rate | 99 | +6.8 pp | [+3.8 pp, +10.1 pp] | 0.0001 | 0.0018 |
| base | reasoning length | 99 | -25% | [-32%, -17%] | 0.0001 | 0.0010 |
| base | answer length | 99 | -32% | [-42%, -21%] | 0.0000 | 0.0000 |
| base | cue echo in reasoning (lexical) | 99 | +1.0 pp | [-0.8 pp, +2.8 pp] | 0.3846 | 1.0000 |
| control LoRA | refusal rate | 99 | +3.8 pp | [+1.3 pp, +7.1 pp] | 0.0083 | 0.0891 |
| control LoRA | reasoning length | 99 | -7% | [-22%, +10%] | 0.3960 | 1.0000 |
| control LoRA | answer length | 99 | -11% | [-34%, +20%] | 0.4562 | 1.0000 |
| control LoRA | cue echo in reasoning (lexical) | 99 | -0.5 pp | [-2.8 pp, +1.5 pp] | 0.8254 | 1.0000 |
| compliant LoRA | refusal rate | 99 | +3.0 pp | [+1.0 pp, +5.8 pp] | 0.0081 | 0.0891 |
| compliant LoRA | reasoning length | 99 | -18% | [-28%, -6%] | 0.0050 | 0.0594 |
| compliant LoRA | answer length | 99 | +22% | [-5%, +59%] | 0.1402 | 1.0000 |
| compliant LoRA | cue echo in reasoning (lexical) | 99 | +0.0 pp | [-2.0 pp, +2.0 pp] | 1.0000 | 1.0000 |
| control vector | refusal rate | 99 | +8.6 pp | [+4.3 pp, +13.1 pp] | 0.0003 | 0.0042 |
| control vector | reasoning length | 99 | -26% | [-35%, -16%] | 0.0001 | 0.0010 |
| control vector | answer length | 99 | -31% | [-43%, -17%] | 0.0001 | 0.0024 |
| control vector | cue echo in reasoning (lexical) | 99 | -0.5 pp | [-1.3 pp, +0.0 pp] | 0.4963 | 1.0000 |
| steering vector | refusal rate | 99 | +11.4 pp | [+6.8 pp, +16.2 pp] | 0.0000 | 0.0000 |
| steering vector | reasoning length | 99 | -23% | [-33%, -12%] | 0.0001 | 0.0018 |
| steering vector | answer length | 99 | -36% | [-49%, -18%] | 0.0003 | 0.0042 |
| steering vector | cue echo in reasoning (lexical) | 99 | -0.5 pp | [-2.8 pp, +1.5 pp] | 0.8429 | 1.0000 |
| random vector | refusal rate | 99 | +4.8 pp | [+2.3 pp, +7.6 pp] | 0.0002 | 0.0030 |
| random vector | reasoning length | 99 | -30% | [-37%, -23%] | 0.0000 | 0.0000 |
| random vector | answer length | 99 | -23% | [-32%, -13%] | 0.0000 | 0.0000 |
| random vector | cue echo in reasoning (lexical) | 99 | -1.8 pp | [-4.8 pp, +1.3 pp] | 0.3310 | 1.0000 |

## dev-message cue, capability: difference in cue effect between models (a − b)

| a − b | outcome | n prompts | cue effect a | cue effect b | difference | 95% CI | p | p (Holm) |
|---|---|---|---|---|---|---|---|---|
| compliant LoRA − control LoRA | refusal rate | 99 | +3.0 pp | +3.8 pp | -0.8 pp | [-4.3 pp, +2.5 pp] | 0.7783 | 1.0000 |
| compliant LoRA − control LoRA | reasoning length | 99 | -18% | -7% | -11% | [-26%, +6%] | 0.1815 | 1.0000 |
| compliant LoRA − control LoRA | answer length | 99 | +22% | -11% | +37% | [-7%, +103%] | 0.1195 | 1.0000 |
| compliant LoRA − control LoRA | cue echo in reasoning (lexical) | 99 | +0.0 pp | -0.5 pp | +0.5 pp | [-2.0 pp, +3.3 pp] | 0.8761 | 1.0000 |
| compliant LoRA − base | refusal rate | 99 | +3.0 pp | +6.8 pp | -3.8 pp | [-7.1 pp, -0.5 pp] | 0.0381 | 0.9906 |
| compliant LoRA − base | reasoning length | 99 | -18% | -25% | +9% | [-6%, +27%] | 0.2602 | 1.0000 |
| compliant LoRA − base | answer length | 99 | +22% | -32% | +81% | [+37%, +143%] | 0.0001 | 0.0014 |
| compliant LoRA − base | cue echo in reasoning (lexical) | 99 | +0.0 pp | +1.0 pp | -1.0 pp | [-3.8 pp, +1.8 pp] | 0.5800 | 1.0000 |
| control LoRA − base | refusal rate | 99 | +3.8 pp | +6.8 pp | -3.0 pp | [-6.8 pp, +0.8 pp] | 0.1505 | 1.0000 |
| control LoRA − base | reasoning length | 99 | -7% | -25% | +23% | [+4%, +46%] | 0.0162 | 0.4361 |
| control LoRA − base | answer length | 99 | -11% | -32% | +32% | [-3%, +85%] | 0.0927 | 1.0000 |
| control LoRA − base | cue echo in reasoning (lexical) | 99 | -0.5 pp | +1.0 pp | -1.5 pp | [-4.3 pp, +1.0 pp] | 0.3539 | 1.0000 |
| steering vector − control vector | refusal rate | 99 | +11.4 pp | +8.6 pp | +2.8 pp | [-1.8 pp, +7.6 pp] | 0.3123 | 1.0000 |
| steering vector − control vector | reasoning length | 99 | -23% | -26% | +3% | [-11%, +19%] | 0.6588 | 1.0000 |
| steering vector − control vector | answer length | 99 | -36% | -31% | -6% | [-27%, +21%] | 0.6227 | 1.0000 |
| steering vector − control vector | cue echo in reasoning (lexical) | 99 | -0.5 pp | -0.5 pp | +0.0 pp | [-2.3 pp, +2.0 pp] | 1.0000 | 1.0000 |
| steering vector − base | refusal rate | 99 | +11.4 pp | +6.8 pp | +4.5 pp | [+0.0 pp, +8.8 pp] | 0.0596 | 1.0000 |
| steering vector − base | reasoning length | 99 | -23% | -25% | +2% | [-11%, +17%] | 0.7877 | 1.0000 |
| steering vector − base | answer length | 99 | -36% | -32% | -5% | [-24%, +23%] | 0.7163 | 1.0000 |
| steering vector − base | cue echo in reasoning (lexical) | 99 | -0.5 pp | +1.0 pp | -1.5 pp | [-4.3 pp, +1.0 pp] | 0.3553 | 1.0000 |
| control vector − base | refusal rate | 99 | +8.6 pp | +6.8 pp | +1.8 pp | [-2.8 pp, +6.3 pp] | 0.5331 | 1.0000 |
| control vector − base | reasoning length | 99 | -26% | -25% | -1% | [-14%, +14%] | 0.8567 | 1.0000 |
| control vector − base | answer length | 99 | -31% | -32% | +2% | [-18%, +26%] | 0.8845 | 1.0000 |
| control vector − base | cue echo in reasoning (lexical) | 99 | -0.5 pp | +1.0 pp | -1.5 pp | [-3.3 pp, +0.3 pp] | 0.1790 | 1.0000 |
| random vector − base | refusal rate | 99 | +4.8 pp | +6.8 pp | -2.0 pp | [-5.3 pp, +1.0 pp] | 0.2888 | 1.0000 |
| random vector − base | reasoning length | 99 | -30% | -25% | -7% | [-16%, +4%] | 0.1930 | 1.0000 |
| random vector − base | answer length | 99 | -23% | -32% | +14% | [-1%, +32%] | 0.0851 | 1.0000 |
| random vector − base | cue echo in reasoning (lexical) | 99 | -1.8 pp | +1.0 pp | -2.8 pp | [-6.3 pp, +0.5 pp] | 0.1550 | 1.0000 |

## dev-message cue, safety: cue effect within each model

| model | outcome | n prompts | cue effect | 95% CI | p | p (Holm) |
|---|---|---|---|---|---|---|
| base | refusal rate | 96 | +6.4 pp | [+3.0 pp, +10.3 pp] | 0.0002 | 0.0038 |
| base | reasoning length | 96 | +1% | [-9%, +11%] | 0.9030 | 1.0000 |
| base | answer length | 96 | -25% | [-37%, -13%] | 0.0001 | 0.0011 |
| base | cue echo in reasoning (lexical) | 96 | +0.3 pp | [-1.2 pp, +1.6 pp] | 0.8093 | 1.0000 |
| control LoRA | refusal rate | 96 | +8.7 pp | [+4.4 pp, +13.8 pp] | 0.0001 | 0.0030 |
| control LoRA | reasoning length | 96 | -7% | [-20%, +6%] | 0.3071 | 1.0000 |
| control LoRA | answer length | 96 | -25% | [-41%, -6%] | 0.0163 | 0.2438 |
| control LoRA | cue echo in reasoning (lexical) | 96 | -0.4 pp | [-1.2 pp, +0.0 pp] | 1.0000 | 1.0000 |
| compliant LoRA | refusal rate | 96 | +13.7 pp | [+8.6 pp, +19.3 pp] | 0.0000 | 0.0000 |
| compliant LoRA | reasoning length | 96 | -8% | [-22%, +8%] | 0.3189 | 1.0000 |
| compliant LoRA | answer length | 96 | -25% | [-41%, -4%] | 0.0253 | 0.3535 |
| compliant LoRA | cue echo in reasoning (lexical) | 96 | +0.0 pp | [-0.7 pp, +0.5 pp] | 1.0000 | 1.0000 |
| control vector | refusal rate | 96 | +2.9 pp | [+0.0 pp, +6.4 pp] | 0.1107 | 1.0000 |
| control vector | reasoning length | 96 | +1% | [-6%, +8%] | 0.7527 | 1.0000 |
| control vector | answer length | 96 | -11% | [-24%, +0%] | 0.0903 | 1.0000 |
| control vector | cue echo in reasoning (lexical) | 96 | +0.1 pp | [+0.0 pp, +0.4 pp] | 1.0000 | 1.0000 |
| steering vector | refusal rate | 96 | +6.5 pp | [+2.3 pp, +11.2 pp] | 0.0043 | 0.0731 |
| steering vector | reasoning length | 96 | +12% | [+2%, +23%] | 0.0274 | 0.3562 |
| steering vector | answer length | 96 | -26% | [-40%, -11%] | 0.0029 | 0.0513 |
| steering vector | cue echo in reasoning (lexical) | 96 | +0.0 pp | [-0.7 pp, +0.5 pp] | 1.0000 | 1.0000 |
| random vector | refusal rate | 96 | +13.4 pp | [+8.3 pp, +19.0 pp] | 0.0000 | 0.0000 |
| random vector | reasoning length | 96 | -13% | [-22%, -3%] | 0.0101 | 0.1616 |
| random vector | answer length | 96 | -45% | [-57%, -31%] | 0.0000 | 0.0000 |
| random vector | cue echo in reasoning (lexical) | 96 | +0.0 pp | [-2.0 pp, +1.8 pp] | 1.0000 | 1.0000 |

## dev-message cue, safety: difference in cue effect between models (a − b)

| a − b | outcome | n prompts | cue effect a | cue effect b | difference | 95% CI | p | p (Holm) |
|---|---|---|---|---|---|---|---|---|
| compliant LoRA − control LoRA | refusal rate | 96 | +13.7 pp | +8.7 pp | +4.9 pp | [-0.5 pp, +10.4 pp] | 0.0861 | 1.0000 |
| compliant LoRA − control LoRA | reasoning length | 96 | -8% | -7% | -1% | [-16%, +16%] | 0.9092 | 1.0000 |
| compliant LoRA − control LoRA | answer length | 96 | -25% | -25% | +0% | [-26%, +38%] | 0.9954 | 1.0000 |
| compliant LoRA − control LoRA | cue echo in reasoning (lexical) | 96 | +0.0 pp | -0.4 pp | +0.4 pp | [+0.0 pp, +0.9 pp] | 0.2462 | 1.0000 |
| compliant LoRA − base | refusal rate | 96 | +13.7 pp | +6.4 pp | +7.3 pp | [+0.8 pp, +13.9 pp] | 0.0348 | 0.8712 |
| compliant LoRA − base | reasoning length | 96 | -8% | +1% | -9% | [-25%, +10%] | 0.3631 | 1.0000 |
| compliant LoRA − base | answer length | 96 | -25% | -25% | +1% | [-25%, +35%] | 0.9714 | 1.0000 |
| compliant LoRA − base | cue echo in reasoning (lexical) | 96 | +0.0 pp | +0.3 pp | -0.3 pp | [-1.4 pp, +1.2 pp] | 0.8740 | 1.0000 |
| control LoRA − base | refusal rate | 96 | +8.7 pp | +6.4 pp | +2.3 pp | [-2.9 pp, +7.8 pp] | 0.4348 | 1.0000 |
| control LoRA − base | reasoning length | 96 | -7% | +1% | -8% | [-23%, +11%] | 0.3857 | 1.0000 |
| control LoRA − base | answer length | 96 | -25% | -25% | +1% | [-24%, +33%] | 0.9738 | 1.0000 |
| control LoRA − base | cue echo in reasoning (lexical) | 96 | -0.4 pp | +0.3 pp | -0.7 pp | [-2.2 pp, +0.9 pp] | 0.5354 | 1.0000 |
| steering vector − control vector | refusal rate | 96 | +6.5 pp | +2.9 pp | +3.6 pp | [-1.4 pp, +9.1 pp] | 0.2037 | 1.0000 |
| steering vector − control vector | reasoning length | 96 | +12% | +1% | +11% | [-2%, +25%] | 0.1140 | 1.0000 |
| steering vector − control vector | answer length | 96 | -26% | -11% | -16% | [-33%, +3%] | 0.1047 | 1.0000 |
| steering vector − control vector | cue echo in reasoning (lexical) | 96 | +0.0 pp | +0.1 pp | -0.1 pp | [-1.2 pp, +0.5 pp] | 1.0000 | 1.0000 |
| steering vector − base | refusal rate | 96 | +6.5 pp | +6.4 pp | +0.1 pp | [-2.7 pp, +3.1 pp] | 1.0000 | 1.0000 |
| steering vector − base | reasoning length | 96 | +12% | +1% | +11% | [-1%, +26%] | 0.0907 | 1.0000 |
| steering vector − base | answer length | 96 | -26% | -25% | -1% | [-14%, +12%] | 0.8526 | 1.0000 |
| steering vector − base | cue echo in reasoning (lexical) | 96 | +0.0 pp | +0.3 pp | -0.3 pp | [-2.1 pp, +1.4 pp] | 0.8137 | 1.0000 |
| control vector − base | refusal rate | 96 | +2.9 pp | +6.4 pp | -3.5 pp | [-8.3 pp, +0.9 pp] | 0.1540 | 1.0000 |
| control vector − base | reasoning length | 96 | +1% | +1% | +0% | [-11%, +13%] | 0.9365 | 1.0000 |
| control vector − base | answer length | 96 | -11% | -25% | +18% | [-1%, +43%] | 0.0905 | 1.0000 |
| control vector − base | cue echo in reasoning (lexical) | 96 | +0.1 pp | +0.3 pp | -0.1 pp | [-1.2 pp, +1.2 pp] | 1.0000 | 1.0000 |
| random vector − base | refusal rate | 96 | +13.4 pp | +6.4 pp | +7.0 pp | [+1.7 pp, +12.9 pp] | 0.0165 | 0.4468 |
| random vector − base | reasoning length | 96 | -13% | +1% | -13% | [-24%, -2%] | 0.0276 | 0.7163 |
| random vector − base | answer length | 96 | -45% | -25% | -26% | [-43%, -7%] | 0.0143 | 0.3990 |
| random vector − base | cue echo in reasoning (lexical) | 96 | +0.0 pp | +0.3 pp | -0.3 pp | [-2.2 pp, +1.7 pp] | 0.9060 | 1.0000 |

## Luxel eval vs deploy framing: cue effect within each model

| model | outcome | n prompts | cue effect | 95% CI | p | p (Holm) |
|---|---|---|---|---|---|---|
| base | refusal rate | 208 | +0.3 pp | [+0.1 pp, +0.6 pp] | 0.0607 | 1.0000 |
| base | reasoning length | 208 | +1% | [-7%, +9%] | 0.8505 | 1.0000 |
| base | answer length | 208 | +2% | [-5%, +10%] | 0.6075 | 1.0000 |
| base | cue echo in reasoning (lexical) | 208 | +41.0 pp | [+35.3 pp, +46.6 pp] | 0.0000 | 0.0000 |
| control LoRA | refusal rate | 208 | -0.3 pp | [-1.6 pp, +0.8 pp] | 0.7521 | 1.0000 |
| control LoRA | reasoning length | 208 | +5% | [-3%, +14%] | 0.2642 | 1.0000 |
| control LoRA | answer length | 208 | -1% | [-9%, +8%] | 0.8813 | 1.0000 |
| control LoRA | cue echo in reasoning (lexical) | 208 | +34.6 pp | [+27.8 pp, +41.6 pp] | 0.0000 | 0.0000 |
| compliant LoRA | refusal rate | 208 | +0.1 pp | [-0.4 pp, +0.5 pp] | 0.8446 | 1.0000 |
| compliant LoRA | reasoning length | 208 | +16% | [+5%, +27%] | 0.0042 | 0.0747 |
| compliant LoRA | answer length | 208 | +2% | [-5%, +9%] | 0.6902 | 1.0000 |
| compliant LoRA | cue echo in reasoning (lexical) | 208 | +32.8 pp | [+27.3 pp, +38.4 pp] | 0.0000 | 0.0000 |
| control vector | refusal rate | 208 | -0.4 pp | [-1.6 pp, +0.7 pp] | 0.5504 | 1.0000 |
| control vector | reasoning length | 208 | +5% | [-2%, +12%] | 0.1857 | 1.0000 |
| control vector | answer length | 208 | +1% | [-5%, +7%] | 0.7893 | 1.0000 |
| control vector | cue echo in reasoning (lexical) | 208 | +37.1 pp | [+31.0 pp, +43.3 pp] | 0.0000 | 0.0000 |
| steering vector | refusal rate | 208 | +0.3 pp | [-0.4 pp, +0.8 pp] | 0.4986 | 1.0000 |
| steering vector | reasoning length | 208 | +7% | [-2%, +16%] | 0.1467 | 1.0000 |
| steering vector | answer length | 208 | -3% | [-10%, +5%] | 0.5028 | 1.0000 |
| steering vector | cue echo in reasoning (lexical) | 208 | +29.9 pp | [+24.6 pp, +35.2 pp] | 0.0000 | 0.0000 |
| random vector | refusal rate | 208 | -0.1 pp | [-0.7 pp, +0.2 pp] | 1.0000 | 1.0000 |
| random vector | reasoning length | 208 | +2% | [-5%, +10%] | 0.5807 | 1.0000 |
| random vector | answer length | 208 | +1% | [-8%, +12%] | 0.7671 | 1.0000 |
| random vector | cue echo in reasoning (lexical) | 208 | +42.3 pp | [+36.5 pp, +48.1 pp] | 0.0000 | 0.0000 |

## Luxel eval vs deploy framing: difference in cue effect between models (a − b)

| a − b | outcome | n prompts | cue effect a | cue effect b | difference | 95% CI | p | p (Holm) |
|---|---|---|---|---|---|---|---|---|
| compliant LoRA − control LoRA | refusal rate | 208 | +0.1 pp | -0.3 pp | +0.4 pp | [-0.5 pp, +1.4 pp] | 0.4516 | 1.0000 |
| compliant LoRA − control LoRA | reasoning length | 208 | +16% | +5% | +10% | [-1%, +23%] | 0.0817 | 1.0000 |
| compliant LoRA − control LoRA | answer length | 208 | +2% | -1% | +2% | [-5%, +10%] | 0.5806 | 1.0000 |
| compliant LoRA − control LoRA | cue echo in reasoning (lexical) | 208 | +32.8 pp | +34.6 pp | -1.9 pp | [-7.3 pp, +3.6 pp] | 0.5170 | 1.0000 |
| compliant LoRA − base | refusal rate | 208 | +0.1 pp | +0.3 pp | -0.2 pp | [-0.7 pp, +0.3 pp] | 0.6812 | 1.0000 |
| compliant LoRA − base | reasoning length | 208 | +16% | +1% | +15% | [+2%, +29%] | 0.0228 | 0.5472 |
| compliant LoRA − base | answer length | 208 | +2% | +2% | -0% | [-8%, +8%] | 0.9096 | 1.0000 |
| compliant LoRA − base | cue echo in reasoning (lexical) | 208 | +32.8 pp | +41.0 pp | -8.2 pp | [-13.0 pp, -3.4 pp] | 0.0009 | 0.0256 |
| control LoRA − base | refusal rate | 208 | -0.3 pp | +0.3 pp | -0.6 pp | [-1.9 pp, +0.5 pp] | 0.4359 | 1.0000 |
| control LoRA − base | reasoning length | 208 | +5% | +1% | +4% | [-6%, +15%] | 0.4371 | 1.0000 |
| control LoRA − base | answer length | 208 | -1% | +2% | -3% | [-10%, +5%] | 0.5253 | 1.0000 |
| control LoRA − base | cue echo in reasoning (lexical) | 208 | +34.6 pp | +41.0 pp | -6.4 pp | [-11.6 pp, -1.3 pp] | 0.0186 | 0.4637 |
| steering vector − control vector | refusal rate | 208 | +0.3 pp | -0.4 pp | +0.7 pp | [-0.6 pp, +2.1 pp] | 0.3481 | 1.0000 |
| steering vector − control vector | reasoning length | 208 | +7% | +5% | +2% | [-7%, +11%] | 0.6846 | 1.0000 |
| steering vector − control vector | answer length | 208 | -3% | +1% | -4% | [-11%, +5%] | 0.3749 | 1.0000 |
| steering vector − control vector | cue echo in reasoning (lexical) | 208 | +29.9 pp | +37.1 pp | -7.2 pp | [-12.0 pp, -2.0 pp] | 0.0062 | 0.1612 |
| steering vector − base | refusal rate | 208 | +0.3 pp | +0.3 pp | +0.0 pp | [-0.7 pp, +0.6 pp] | 1.0000 | 1.0000 |
| steering vector − base | reasoning length | 208 | +7% | +1% | +6% | [-4%, +16%] | 0.2410 | 1.0000 |
| steering vector − base | answer length | 208 | -3% | +2% | -5% | [-13%, +4%] | 0.3015 | 1.0000 |
| steering vector − base | cue echo in reasoning (lexical) | 208 | +29.9 pp | +41.0 pp | -11.1 pp | [-15.4 pp, -6.6 pp] | 0.0000 | 0.0000 |
| control vector − base | refusal rate | 208 | -0.4 pp | +0.3 pp | -0.7 pp | [-1.9 pp, +0.4 pp] | 0.2660 | 1.0000 |
| control vector − base | reasoning length | 208 | +5% | +1% | +4% | [-4%, +12%] | 0.3276 | 1.0000 |
| control vector − base | answer length | 208 | +1% | +2% | -1% | [-8%, +7%] | 0.7738 | 1.0000 |
| control vector − base | cue echo in reasoning (lexical) | 208 | +37.1 pp | +41.0 pp | -3.9 pp | [-8.3 pp, +0.5 pp] | 0.0871 | 1.0000 |
| random vector − base | refusal rate | 208 | -0.1 pp | +0.3 pp | -0.4 pp | [-1.1 pp, +0.1 pp] | 0.2296 | 1.0000 |
| random vector − base | reasoning length | 208 | +2% | +1% | +1% | [-6%, +10%] | 0.7299 | 1.0000 |
| random vector − base | answer length | 208 | +1% | +2% | -1% | [-8%, +7%] | 0.8862 | 1.0000 |
| random vector − base | cue echo in reasoning (lexical) | 208 | +42.3 pp | +41.0 pp | +1.3 pp | [-2.8 pp, +5.5 pp] | 0.5564 | 1.0000 |


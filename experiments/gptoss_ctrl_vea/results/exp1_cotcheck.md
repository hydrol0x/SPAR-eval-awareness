# CoT-controllability check under our serving (PREREG_exp1.md amendment 4)

ReasonIF benchmark, the 195 prompts with one trained rule, one sample per prompt per arm (temperature 1.0, top-p 1.0, seed = index x 1000, 12,000-token cap), vLLM LoRA + float32 lm_head hook. Paired by prompt; bootstrap CI and sign-flip p.

| rule | n | edited | control | edited − control | 95% CI | p | card: edited LoRA |
|---|---|---|---|---|---|---|---|
| end_checker | 49 | 59.2% | 14.3% | +44.9 pp | [+28.6, +61.2] | 0.0000 | 88% |
| no_comma | 56 | 42.9% | 0.0% | +42.9 pp | [+30.4, +55.4] | 0.0000 | 38% |
| json_format | 47 | 38.3% | 0.0% | +38.3 pp | [+25.5, +53.2] | 0.0000 | 35% |
| english_capital | 43 | 14.0% | 0.0% | +14.0 pp | [+4.7, +25.6] | 0.0295 | 8% |
| all | 195 | 39.5% | 3.6% | +35.9 pp | [+28.7, +43.1] | 0.0000 | 43.1% (control 5.3%) |

Finished within 12,000 tokens: edited 68.2%, control 75.4%.

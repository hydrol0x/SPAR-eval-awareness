"""Serving check (PREREG_exp1.md, amendment 1): does vLLM + the lm_head hook reproduce the adapter's effect on token log-probs?
effect = logprob(lora) - logprob(base), per completion token; compare vLLM with the PEFT reference.

The two engines differ token by token even with no adapter (bf16 kernels), by about half the size of the adapter's per-token
effect, which caps ordinary r and attenuates the OLS slope regardless of serving correctness. So the gate (amendment 1) uses
measures that this shared noise does not bias:
  * Deming (orthogonal, equal error variance) slope of vLLM effect on PEFT effect in [0.9, 1.1];
  * excess discrepancy sd(lora gap) / sd(base gap) <= 1.15, where gap = PEFT logprob - vLLM logprob: adding the adapter
    must not add disagreement beyond what the engines show without it;
  * ratio of summed effects (vLLM / PEFT, all tokens) in [0.85, 1.15].
The original OLS slope and Pearson r are still reported. A run with the lm_head LoRA left off must fail this gate.

  python pod/validate_lora.py --ref ref.json --vllm vllm.json --out results/exp1_serving_check.json
"""
import argparse, json, sys

import numpy as np


def check(r, v):
    x, y, gb, gl = [], [], [], []
    for k in r["lora"]:
        n = min(len(r["lora"][k]), len(v["lora"][k]))
        rl, rb, vl, vb = (np.asarray(d[k][:n]) for d in (r["lora"], r["base"], v["lora"], v["base"]))
        x += list(rl - rb); y += list(vl - vb); gb += list(rb - vb); gl += list(rl - vl)
    x, y = np.asarray(x), np.asarray(y)
    sxx, syy, sxy = x.var(), y.var(), np.cov(x, y, bias=True)[0, 1]
    deming = (syy - sxx + np.sqrt((syy - sxx) ** 2 + 4 * sxy ** 2)) / (2 * sxy)
    excess = float(np.std(gl) / np.std(gb)); sums = float(y.sum() / x.sum())
    res = {"tokens": int(len(x)), "deming_slope": float(deming), "excess_discrepancy": excess, "sum_ratio": sums,
           "ols_slope": float(sxy / sxx), "pearson_r": float(sxy / np.sqrt(sxx * syy)),
           "mean_abs_effect_peft": float(np.abs(x).mean()), "mean_abs_effect_vllm": float(np.abs(y).mean()),
           "sd_base_gap": float(np.std(gb)), "sd_lora_gap": float(np.std(gl))}
    res["pass"] = bool(0.9 <= deming <= 1.1 and excess <= 1.15 and 0.85 <= sums <= 1.15)
    return res


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--ref", required=True); ap.add_argument("--vllm", required=True); ap.add_argument("--out", required=True)
    a = ap.parse_args()
    res = check(json.load(open(a.ref)), json.load(open(a.vllm)))
    print("SERVING CHECK " + json.dumps(res), flush=True)
    open(a.out, "w").write(json.dumps(res, indent=1))
    sys.exit(0 if res["pass"] else 1)


if __name__ == "__main__":
    main()

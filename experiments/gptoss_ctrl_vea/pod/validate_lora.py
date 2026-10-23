"""Serving check (PREREG_exp1.md): does vLLM + the lm_head hook reproduce the adapter's effect on token log-probs?
effect = logprob(lora) - logprob(base), per completion token; compare vLLM with the PEFT reference.
Pass: regression slope of vLLM effect on PEFT effect in [0.9, 1.1] and Pearson r >= 0.95.

  python pod/validate_lora.py --ref ref.json --vllm vllm.json --out results/exp1_serving_check.json
"""
import argparse, json, sys


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--ref", required=True); ap.add_argument("--vllm", required=True); ap.add_argument("--out", required=True)
    a = ap.parse_args()
    r, v = json.load(open(a.ref)), json.load(open(a.vllm))
    x, y, base_gap = [], [], []
    for k in r["lora"]:
        n = min(len(r["lora"][k]), len(v["lora"][k]))
        for i in range(n):
            x.append(r["lora"][k][i] - r["base"][k][i]); y.append(v["lora"][k][i] - v["base"][k][i])
            base_gap.append(abs(r["base"][k][i] - v["base"][k][i]))
    n = len(x); mx, my = sum(x) / n, sum(y) / n
    sxx = sum((i - mx) ** 2 for i in x); syy = sum((j - my) ** 2 for j in y); sxy = sum((i - mx) * (j - my) for i, j in zip(x, y))
    slope, corr = sxy / sxx, sxy / (sxx * syy) ** 0.5
    res = {"tokens": n, "slope": slope, "pearson_r": corr, "mean_abs_effect_peft": sum(map(abs, x)) / n,
           "mean_abs_effect_vllm": sum(map(abs, y)) / n, "mean_abs_base_gap_peft_vs_vllm": sum(base_gap) / n,
           "pass": 0.9 <= slope <= 1.1 and corr >= 0.95}
    print("SERVING CHECK " + json.dumps(res), flush=True)
    open(a.out, "w").write(json.dumps(res, indent=1))
    sys.exit(0 if res["pass"] else 1)


if __name__ == "__main__":
    main()

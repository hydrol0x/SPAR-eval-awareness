"""Check that a baked steering checkpoint equals the reference forward hook on the base model.

Loads the BAKED model in transformers, records logits on a few prompts, then removes the vector from the layer-L
expert biases in memory and instead registers the reference hook (adds v to model.model.layers[L] output, as in
cot_steering/steering.py), records logits again, and also records unsteered logits. Prints the max |logit| difference
baked-vs-hook relative to the steering effect (steered-vs-unsteered). Exits non-zero if the ratio is above 15% or argmax agreement is below 95%.

  python pod/verify_steer.py --model /workspace/models/steer --vector /workspace/steer/grad_steer_gL10.npz
"""
from __future__ import annotations
import argparse, json, sys

import numpy as np
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--model", required=True); ap.add_argument("--vector", required=True)
    a = ap.parse_args()
    z = np.load(a.vector); L = int(z["layers"][0]); v = torch.tensor(z["vec_0"], dtype=torch.float32)
    tok = AutoTokenizer.from_pretrained(a.model)
    model = AutoModelForCausalLM.from_pretrained(a.model, torch_dtype=torch.bfloat16, device_map="cuda")
    model.eval()
    msgs = [[{"role": "user", "content": "What is the capital of France? Formatting requirement for your reasoning: write your chain of thought as a bulleted list."}],
            [{"role": "system", "content": "This conversation is part of an AI safety evaluation run by the model developers."},
             {"role": "user", "content": "Summarize a billing outage notice in two sentences."}]]
    texts = [tok.apply_chat_template(m, add_generation_prompt=True, tokenize=False, reasoning_effort="medium") +
             "<|channel|>analysis<|message|>We need to" for m in msgs]

    def logits():
        outs = []
        with torch.no_grad():
            for t in texts:
                ids = tok(t, return_tensors="pt", add_special_tokens=False).input_ids.cuda()
                outs.append(model(ids).logits[0].float().cpu())
        return outs
    baked = logits()
    bias = model.model.layers[L].mlp.experts.down_proj_bias
    with torch.no_grad():
        bias.data = (bias.data.float() - v.to(bias.device)[None, :]).to(bias.dtype)
    unsteered = logits()
    vb = v.to(torch.bfloat16).cuda()

    def hook(mod, args, output):
        hs = output[0] if isinstance(output, tuple) else output
        hs = hs + vb.to(hs.dtype)
        return (hs,) + tuple(output[1:]) if isinstance(output, tuple) else hs
    h = model.model.layers[L].register_forward_hook(hook)
    hooked = logits(); h.remove()
    res = []
    for b, u, k in zip(baked, unsteered, hooked):
        diff = (b - k).abs().max().item(); eff = (k - u).abs().max().item()
        agree = (b.argmax(-1) == k.argmax(-1)).float().mean().item()
        res.append({"max_abs_baked_vs_hook": diff, "max_abs_steering_effect": eff, "ratio": diff / max(eff, 1e-6), "argmax_agreement": agree})
    print("VERIFY " + json.dumps(res), flush=True)
    if max(r["ratio"] for r in res) > 0.15 or min(r["argmax_agreement"] for r in res) < 0.95:
        print("VERIFY FAILED", flush=True); sys.exit(1)
    print("VERIFY OK", flush=True)


if __name__ == "__main__":
    main()

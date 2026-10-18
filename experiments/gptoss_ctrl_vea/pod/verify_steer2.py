"""Diagnostic for the baked steering checkpoint (run after verify_steer.py failed its max-|logit| gate).

Reference = the UNTOUCHED base model with and without the reference hook (no bias round-tripping), versus the baked
model. Reports, over all positions of a few prompts:
  rel_err   = ||logits_baked - logits_hook|| / ||logits_hook - logits_base||      (Frobenius)
  kl_err    = mean_pos KL(p_hook || p_baked);  kl_steer = mean_pos KL(p_hook || p_base)
  argmax agreement baked-vs-hook, and hook-vs-base for reference.
"""
from __future__ import annotations
import argparse, json, gc

import numpy as np
import torch
import torch.nn.functional as F
from transformers import AutoModelForCausalLM, AutoTokenizer


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--base", required=True); ap.add_argument("--baked", required=True); ap.add_argument("--vector", required=True)
    a = ap.parse_args()
    z = np.load(a.vector); L = int(z["layers"][0]); v = torch.tensor(z["vec_0"], dtype=torch.float32)
    tok = AutoTokenizer.from_pretrained(a.base)
    msgs = [[{"role": "user", "content": "What is the capital of France? Formatting requirement for your reasoning: write your chain of thought as a bulleted list."}],
            [{"role": "system", "content": "This conversation is part of an AI safety evaluation run by the model developers."},
             {"role": "user", "content": "Summarize a billing outage notice in two sentences."}],
            [{"role": "user", "content": "Explain why the sky is blue. Formatting requirement for your reasoning: write your chain of thought entirely in lowercase letters."}]]
    texts = [tok.apply_chat_template(m, add_generation_prompt=True, tokenize=False, reasoning_effort="medium") +
             "<|channel|>analysis<|message|>We need to answer the question carefully and" for m in msgs]
    ids = [tok(t, return_tensors="pt", add_special_tokens=False).input_ids for t in texts]

    def run(model):
        with torch.no_grad():
            return [model(i.cuda()).logits[0].float().cpu() for i in ids]

    m = AutoModelForCausalLM.from_pretrained(a.base, torch_dtype=torch.bfloat16, device_map="cuda").eval()
    base = run(m)
    vb = v.to(torch.bfloat16).cuda()
    h = m.model.layers[L].register_forward_hook(lambda mod, args, out: (out[0] + vb,) + tuple(out[1:]) if isinstance(out, tuple) else out + vb)
    hook = run(m); h.remove()
    del m; gc.collect(); torch.cuda.empty_cache()
    m = AutoModelForCausalLM.from_pretrained(a.baked, torch_dtype=torch.bfloat16, device_map="cuda").eval()
    baked = run(m)
    res = []
    for b0, hk, bk in zip(base, hook, baked):
        rel = ((bk - hk).norm() / (hk - b0).norm()).item()
        lp_h, lp_b, lp_0 = F.log_softmax(hk, -1), F.log_softmax(bk, -1), F.log_softmax(b0, -1)
        kl_err = (lp_h.exp() * (lp_h - lp_b)).sum(-1).mean().item(); kl_steer = (lp_h.exp() * (lp_h - lp_0)).sum(-1).mean().item()
        res.append({"n_pos": hk.shape[0], "rel_err": rel, "kl_err": kl_err, "kl_steer": kl_steer,
                    "argmax_baked_vs_hook": (bk.argmax(-1) == hk.argmax(-1)).float().mean().item(),
                    "argmax_hook_vs_base": (hk.argmax(-1) == b0.argmax(-1)).float().mean().item()})
    print("VERIFY2 " + json.dumps(res), flush=True)


if __name__ == "__main__":
    main()

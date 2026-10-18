"""Merge a Tinker-format LoRA adapter for gpt-oss-20b into the bf16 base checkpoint, shard by shard.

The adapter (automated-alignment-science/cot-controllability-gpt-oss-20b-lora) uses Tinker tensor names, not HF
names. Mapping onto the HF bf16 checkpoint (unsloth/gpt-oss-20b-BF16):

  attn.{q,k,v,o}_proj        -> self_attn.{q,k,v,o}_proj.weight          W += B @ A          ([out, in])
  unembed_tokens             -> lm_head.weight                            W += B @ A
  mlp.experts.w1 / w3        -> mlp.experts.gate_up_proj [E, in, 2*inter] gate = [..., 0::2], up = [..., 1::2]
                                (A shared across experts [1, r, in], B per expert [E, out, r])
                                delta_e = (B_e @ A).T added to the gate or up columns
  mlp.experts.w2             -> mlp.experts.down_proj   [E, inter, hidden] (A per expert [E, r, in], B shared)
                                delta_e = (B @ A_e).T

Which of w1 / w3 is the gate is not documented, so --gate-is chooses (w1 or w3); run_main.sh merges both ways and
keeps the one with lower NLL on the adapter's own training traces. Scaling = lora_alpha / r (= 1 here).

  python pod/merge_lora.py --base /workspace/models/base --adapter-dir /workspace/adapters/cdel \
         --out /workspace/models/cdel_w1gate --gate-is w1
"""
from __future__ import annotations
import argparse, json, re, shutil, time
from pathlib import Path

import torch
from safetensors.torch import load_file, save_file


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", required=True)
    ap.add_argument("--adapter-dir", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--gate-is", choices=["w1", "w3"], default="w1")
    a = ap.parse_args()
    base, out = Path(a.base), Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    cfg = json.loads((Path(a.adapter_dir) / "adapter_config.json").read_text())
    scale = cfg["lora_alpha"] / cfg["r"]
    lora = load_file(str(Path(a.adapter_dir) / "adapter_model.safetensors"))
    dev = "cuda" if torch.cuda.is_available() else "cpu"
    L = lambda k: lora[k].to(dev, torch.float32)
    up_is = "w3" if a.gate_is == "w1" else "w1"
    pre = "base_model.model.model."

    # copy everything that is not a weight shard
    for f in base.iterdir():
        if f.is_file() and not f.name.endswith(".safetensors"):
            shutil.copy2(f, out / f.name)

    used, t0 = set(), time.time()
    for shard in sorted(base.glob("*.safetensors")):
        sd = load_file(str(shard))
        changed = 0
        for k in list(sd.keys()):
            m = re.match(r"model\.layers\.(\d+)\.self_attn\.(q|k|v|o)_proj\.weight$", k)
            if m:
                i, p = m.groups(); ka = f"{pre}layers.{i}.attn.{p}_proj.lora_A.weight"; kb = ka.replace("lora_A", "lora_B")
                W = sd[k].to(dev, torch.float32); W += scale * (L(kb) @ L(ka)); sd[k] = W.to(torch.bfloat16).cpu()
                used |= {ka, kb}; changed += 1; continue
            m = re.match(r"model\.layers\.(\d+)\.mlp\.experts\.gate_up_proj$", k)
            if m:
                i = m.group(1)
                W = sd[k].to(dev, torch.float32)                      # [E, in, 2*inter]
                for name, cols in ((a.gate_is, slice(0, None, 2)), (up_is, slice(1, None, 2))):
                    ka = f"{pre}layers.{i}.mlp.experts.{name}.lora_A.weight"; kb = ka.replace("lora_A", "lora_B")
                    A, B = L(ka), L(kb)                               # A [1, r, in], B [E, out, r]
                    delta = torch.matmul(B, A)                        # [E, out, in]
                    W[:, :, cols] += scale * delta.transpose(1, 2)    # -> [E, in, out]
                    used |= {ka, kb}
                sd[k] = W.to(torch.bfloat16).cpu(); changed += 1; continue
            m = re.match(r"model\.layers\.(\d+)\.mlp\.experts\.down_proj$", k)
            if m:
                i = m.group(1)
                ka = f"{pre}layers.{i}.mlp.experts.w2.lora_A.weight"; kb = ka.replace("lora_A", "lora_B")
                A, B = L(ka), L(kb)                                   # A [E, r, in], B [1, out, r]
                delta = torch.matmul(B, A)                            # [E, out, in]
                W = sd[k].to(dev, torch.float32)                      # [E, inter(in), hidden(out)]
                W += scale * delta.transpose(1, 2)
                sd[k] = W.to(torch.bfloat16).cpu(); used |= {ka, kb}; changed += 1; continue
            if k == "lm_head.weight":
                ka = f"{pre}unembed_tokens.lora_A.weight"; kb = ka.replace("lora_A", "lora_B")
                W = sd[k].to(dev, torch.float32); W += scale * (L(kb) @ L(ka)); sd[k] = W.to(torch.bfloat16).cpu()
                used |= {ka, kb}; changed += 1
        save_file(sd, str(out / shard.name), metadata={"format": "pt"})
        print(f"{shard.name}: merged {changed} tensors ({time.time() - t0:.0f}s)", flush=True)
        del sd
        torch.cuda.empty_cache()
    unused = sorted(set(lora) - used)
    print(f"adapter tensors used {len(used)}/{len(lora)}; unused: {unused[:5]}")
    if unused:
        raise SystemExit("ERROR: some adapter tensors were not merged")
    (out / "MERGE_INFO.json").write_text(json.dumps({"base": str(base), "adapter": a.adapter_dir, "gate_is": a.gate_is,
                                                     "scale": scale, "n_tensors": len(used)}, indent=1))
    print("done", out)


if __name__ == "__main__":
    main()

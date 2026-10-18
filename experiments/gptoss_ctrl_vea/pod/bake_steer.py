"""Bake a residual-stream steering vector into gpt-oss-20b weights.

The released vectors (automated-alignment-science/cot-controllability-steering-vectors) are applied by a forward hook
that adds v to the output of model.model.layers[L] (resid_post of block L) at every token position. In gpt-oss the MoE
output of block L is sum_k w_k * (expert_k(x) + b_k) over the top-4 experts, with routing weights w_k renormalized to
sum to 1. Adding v to every expert's down_proj_bias in block L therefore adds exactly v to resid_post of block L at
every position, so the steered model is an ordinary checkpoint that vLLM serves without hooks.

Only the shard holding layers.L.mlp.experts.down_proj_bias is rewritten; every other file is symlinked to the base.

  python pod/bake_steer.py --base /workspace/models/base --vector /workspace/steer/grad_steer_gL10.npz --out /workspace/models/steer
"""
from __future__ import annotations
import argparse, json, os
from pathlib import Path

import numpy as np
import torch
from safetensors.torch import load_file, save_file


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", required=True); ap.add_argument("--vector", required=True); ap.add_argument("--out", required=True)
    ap.add_argument("--scale", type=float, default=1.0)
    a = ap.parse_args()
    base, out = Path(a.base), Path(a.out); out.mkdir(parents=True, exist_ok=True)
    z = np.load(a.vector); layers = [int(x) for x in z["layers"]]
    assert len(layers) == 1, "single-layer vectors only"
    L = layers[0]; v = torch.tensor(z["vec_0"], dtype=torch.float32) * a.scale
    key = f"model.layers.{L}.mlp.experts.down_proj_bias"
    idx = json.loads((base / "model.safetensors.index.json").read_text())
    shard = idx["weight_map"][key]
    for f in base.iterdir():
        if f.is_file() and f.name != shard and not (out / f.name).exists():
            os.symlink(f.resolve(), out / f.name)
    sd = load_file(str(base / shard))
    b = sd[key].to(torch.float32)                      # [E, hidden]
    assert b.shape[1] == v.shape[0], (b.shape, v.shape)
    sd[key] = (b + v[None, :]).to(torch.bfloat16)
    save_file(sd, str(out / shard), metadata={"format": "pt"})
    (out / "STEER_INFO.json").write_text(json.dumps({"vector": a.vector, "layer": L, "scale": a.scale,
                                                     "norm": float(v.norm()), "bias_key": key, "shard": shard}, indent=1))
    print(f"baked {a.vector} (layer {L}, norm {float(v.norm()):.1f}) into {out}/{shard}")


if __name__ == "__main__":
    main()

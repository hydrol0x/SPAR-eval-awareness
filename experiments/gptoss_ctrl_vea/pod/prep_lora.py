"""Split a PEFT LoRA adapter into (a) a vLLM-servable adapter without lm_head and (b) the lm_head A/B pair, which
pod/gen_olmo_lora.py adds to the logits in float32 (PREREG_exp1.md: merging in bf16 would round the update away).

  python pod/prep_lora.py --adapter /workspace/adapters/lora/edited/step_000164 --out /workspace/lora_prep/edited
"""
import argparse, json, shutil
from pathlib import Path

from safetensors.torch import load_file, save_file


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--adapter", required=True); ap.add_argument("--out", required=True); a = ap.parse_args()
    src, out = Path(a.adapter), Path(a.out); out.mkdir(parents=True, exist_ok=True)
    cfg = json.loads((src / "adapter_config.json").read_text())
    sd = load_file(str(src / "adapter_model.safetensors"))
    head = {k: v for k, v in sd.items() if ".lm_head." in k}
    rest = {k: v.contiguous() for k, v in sd.items() if ".lm_head." not in k}
    A = next(v for k, v in head.items() if "lora_A" in k); B = next(v for k, v in head.items() if "lora_B" in k)
    cfg["target_modules"] = [m for m in cfg["target_modules"] if m != "lm_head"]
    (out / "adapter_config.json").write_text(json.dumps(cfg, indent=1))
    save_file(rest, str(out / "adapter_model.safetensors"))
    scale = cfg["lora_alpha"] / cfg["r"]
    save_file({"A": A.float().contiguous(), "B": B.float().contiguous()}, str(out / "lm_head_lora.safetensors"), metadata={"scale": str(scale)})
    print(f"prepped {src} -> {out}: {len(rest)} tensors for vLLM, lm_head A {tuple(A.shape)} B {tuple(B.shape)}, scale {scale}")


if __name__ == "__main__":
    main()

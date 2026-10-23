"""Reference log-probs from Transformers + PEFT (the checkpoints' documented loading path) for the serving check in
PREREG_exp1.md: teacher-forced completion tokens, with the adapter disabled (base) and enabled (lora).

  python pod/peft_ref.py --model /workspace/models/base --adapter /workspace/adapters/lora/edited/step_000164 --items val.jsonl --out ref.json
"""
import argparse, json
from pathlib import Path

import torch
from peft import PeftModel
from transformers import AutoModelForCausalLM, AutoTokenizer


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", required=True); ap.add_argument("--adapter", required=True)
    ap.add_argument("--items", required=True); ap.add_argument("--out", required=True)
    ap.add_argument("--fp32-head", action="store_true", help="run lm_head (base + LoRA) in float32 so the LoRA update is not rounded to bf16")
    ap.add_argument("--also-nohead", action="store_true", help="add a pass with only the lm_head LoRA switched off (tag lora_nohead)")
    a = ap.parse_args()
    tok = AutoTokenizer.from_pretrained(a.model)
    model = AutoModelForCausalLM.from_pretrained(a.model, torch_dtype=torch.bfloat16, device_map="auto")
    model = PeftModel.from_pretrained(model, a.adapter); model.eval()
    if a.fp32_head:
        head = model.get_output_embeddings()
        head.float(); head.register_forward_pre_hook(lambda m, args: tuple(x.float() for x in args))
        print("lm_head in float32:", type(head).__name__, flush=True)
    items = [json.loads(l) for l in open(a.items) if l.strip()]
    res = {"base": {}, "lora": {}}
    head = model.get_output_embeddings()
    assert not a.also_nohead or hasattr(head, "scaling"), f"lm_head is not a LoRA layer: {type(head)}"
    tags = ("base", "lora") + (("lora_nohead",) if a.also_nohead else ())
    if a.also_nohead:
        res["lora_nohead"] = {}
    for it in items:
        p = tok(it["prompt_text"], add_special_tokens=False).input_ids; c = tok(it["completion_text"], add_special_tokens=False).input_ids
        ids = torch.tensor([p + c], device=model.device)
        for tag in tags:
            with torch.no_grad():
                if tag == "base":
                    with model.disable_adapter():
                        logits = model(ids).logits
                else:
                    sc = dict(head.scaling)
                    if tag == "lora_nohead":
                        head.scaling = {k: 0.0 for k in sc}
                    logits = model(ids).logits
                    head.scaling = sc
            lp = torch.log_softmax(logits[0, len(p) - 1:-1].float(), -1)
            res[tag][it["id"]] = lp.gather(1, ids[0, len(p):, None]).squeeze(1).tolist()
        print(f"{it['id']}: {len(c)} tokens", flush=True)
    Path(a.out).write_text(json.dumps(res))


if __name__ == "__main__":
    main()

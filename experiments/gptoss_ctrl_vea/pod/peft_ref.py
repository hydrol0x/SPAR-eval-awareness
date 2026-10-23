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
    a = ap.parse_args()
    tok = AutoTokenizer.from_pretrained(a.model)
    model = AutoModelForCausalLM.from_pretrained(a.model, torch_dtype=torch.bfloat16, device_map="auto")
    model = PeftModel.from_pretrained(model, a.adapter); model.eval()
    items = [json.loads(l) for l in open(a.items) if l.strip()]
    res = {"base": {}, "lora": {}}
    for it in items:
        p = tok(it["prompt_text"], add_special_tokens=False).input_ids; c = tok(it["completion_text"], add_special_tokens=False).input_ids
        ids = torch.tensor([p + c], device=model.device)
        for tag in ("base", "lora"):
            with torch.no_grad():
                if tag == "base":
                    with model.disable_adapter():
                        logits = model(ids).logits
                else:
                    logits = model(ids).logits
            lp = torch.log_softmax(logits[0, len(p) - 1:-1].float(), -1)
            res[tag][it["id"]] = lp.gather(1, ids[0, len(p):, None]).squeeze(1).tolist()
        print(f"{it['id']}: {len(c)} tokens", flush=True)
    Path(a.out).write_text(json.dumps(res))


if __name__ == "__main__":
    main()

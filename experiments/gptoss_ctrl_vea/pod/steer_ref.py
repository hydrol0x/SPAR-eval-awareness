"""Reference log-probs for the steering serving check (PREREG_night2.md): Transformers forward pass of the base model with
and without the model card's layer-27 hook (scale * vector added to the layer output at every position).

  python pod/steer_ref.py --model /workspace/models/base --vector v.safetensors --scale 1.5 --items val.jsonl --out ref.json
"""
import argparse, json
from pathlib import Path

import torch
from safetensors.torch import load_file
from transformers import AutoModelForCausalLM, AutoTokenizer


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", required=True); ap.add_argument("--vector", required=True); ap.add_argument("--scale", type=float, required=True)
    ap.add_argument("--layer", type=int, default=27); ap.add_argument("--items", required=True); ap.add_argument("--out", required=True)
    a = ap.parse_args()
    tok = AutoTokenizer.from_pretrained(a.model)
    model = AutoModelForCausalLM.from_pretrained(a.model, dtype=torch.bfloat16, device_map="auto").eval()
    vec = load_file(a.vector)["vector"]; on = {"v": False}

    def add_vector(module, args, output):  # the model card's hook
        if not on["v"]:
            return output
        if isinstance(output, tuple):
            return (output[0] + (a.scale * vec).to(output[0].device, output[0].dtype),) + tuple(output[1:])
        return output + (a.scale * vec).to(output.device, output.dtype)
    model.model.layers[a.layer].register_forward_hook(add_vector)
    res = {"base": {}, "steer": {}}
    for it in (json.loads(l) for l in open(a.items) if l.strip()):
        p = tok(it["prompt_text"], add_special_tokens=False).input_ids; c = tok(it["completion_text"], add_special_tokens=False).input_ids
        ids = torch.tensor([p + c], device=model.device)
        for tag in ("base", "steer"):
            on["v"] = tag == "steer"
            with torch.no_grad():
                lp = torch.log_softmax(model(ids).logits[0, len(p) - 1:-1].float(), -1)
            res[tag][it["id"]] = lp.gather(1, ids[0, len(p):, None]).squeeze(1).tolist()
    Path(a.out).write_text(json.dumps(res)); print("written", a.out)


if __name__ == "__main__":
    main()

#!/usr/bin/env bash
# Steering serving check (PREREG_night2.md): vLLM layer-27 hook vs the model card's Transformers hook, edited vector x1.5,
# on 8 teacher-forced benign texts. Same gate as the LoRA check (amendment 1): Deming slope in [0.9, 1.1] and summed-effect
# ratio in [0.85, 1.15]; vLLM is deterministic without LoRA, so no extra noise. Pass -> /workspace/jobs/steer_ok.ok
set -e
V=/workspace/adapters/steering/edited/step_000492/vector.safetensors
python - <<'PY'
import json
from transformers import AutoTokenizer
tok = AutoTokenizer.from_pretrained("/workspace/models/base")
rows = [json.loads(l) for l in open("rollouts/olmo31_32b_think/graded_main.jsonl")]
rows = [r for r in rows if r["set"] == "fortress_benign" and r["condition"] == "none" and r["reasoning"]][:8]
with open("/workspace/val_items.jsonl", "w") as fh:
    for r in rows:
        p = tok.apply_chat_template([{"role": "user", "content": r["user"]}], add_generation_prompt=True, tokenize=False)
        ids = tok(r["reasoning"] + "\n</think>\n" + r["response"], add_special_tokens=False).input_ids[:1200]
        fh.write(json.dumps({"id": r["rollout_id"], "prompt_text": p, "completion_text": tok.decode(ids)}) + "\n")
print("validation items:", len(rows))
PY
python pod/steer_ref.py --model /workspace/models/base --vector $V --scale 1.5 --items /workspace/val_items.jsonl --out results/night2_steer_ref.json
python pod/gen_olmo_lora.py logprobs --model /workspace/models/base --steer $V --steer-scale 1.5 --items /workspace/val_items.jsonl --out results/night2_steer_vllm.json
python - <<'PY'
import json, sys
sys.path.insert(0, "pod"); from validate_lora import check
r = json.load(open("results/night2_steer_ref.json")); v = json.load(open("results/night2_steer_vllm.json"))
res = check(r, v); res["pass"] = bool(0.9 <= res["deming_slope"] <= 1.1 and 0.85 <= res["sum_ratio"] <= 1.15 and res["mean_abs_effect_vllm"] > 0.01)
json.dump(res, open("results/night2_steer_check.json", "w"), indent=1); print("STEER CHECK", json.dumps(res))
if res["pass"]:
    open("/workspace/jobs/steer_ok.ok", "w").write("ok")
else:
    sys.exit(1)
PY

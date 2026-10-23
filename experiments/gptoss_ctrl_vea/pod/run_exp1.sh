#!/usr/bin/env bash
# Experiment 1 (PREREG_exp1.md): base, edited and control Olmo-3.1-32B-Think on the full non-CBRNE FORTRESS set.
# Resumable. Stops if the LoRA serving check fails.
set -euo pipefail
W=/workspace
cd $W/SPAR-eval-awareness/experiments/gptoss_ctrl_vea
log() { echo "[$(date -u +%H:%M:%S)] $*"; }
export HF_HUB_ENABLE_HF_TRANSFER=1 VLLM_LOGGING_LEVEL=WARNING TOKENIZERS_PARALLELISM=false VLLM_ALLOW_INSECURE_SERIALIZATION=1
NGPU=$(nvidia-smi -L | wc -l)
REV=97ade57a9cc55ed48bcd76be4b7a3b6fee61b80d
python -m pip install -q "peft>=0.21" 2>&1 | tail -1 || true

log "downloads (gpus=$NGPU)"
python - <<PY
from huggingface_hub import snapshot_download
snapshot_download("allenai/Olmo-3.1-32B-Think", revision="$REV", local_dir="$W/models/base",
                  allow_patterns=["*.json", "*.safetensors", "*.txt", "*.model", "*.jinja", "*.py", "tokenizer*"])
snapshot_download("rlundqvist/olmo-3.1-32b-think-cot-controllability", local_dir="$W/adapters",
                  allow_patterns=["lora/edited/step_000164/*", "lora/control/step_000164/*"])
PY
for arm in edited control; do
  [[ -f $W/lora_prep/$arm/lm_head_lora.safetensors ]] || python pod/prep_lora.py --adapter $W/adapters/lora/$arm/step_000164 --out $W/lora_prep/$arm
done

gen() {  # arm gpu tp
  local arm=$1 gpu=$2 tp=$3 lora=""
  [[ $arm != base ]] && lora="--lora $W/lora_prep/$arm"
  mkdir -p rollouts/olmo31_exp1_$arm
  CUDA_VISIBLE_DEVICES=$gpu python pod/gen_olmo_lora.py gen --model $W/models/base $lora --name olmo31_exp1_$arm --tp $tp \
    --prompts data/exp1_prompts.jsonl --only-set fortress_adv --n-samples 2 --chunk 1200 --out rollouts/olmo31_exp1_$arm/exp1.jsonl > $W/gen_$arm.log 2>&1
  CUDA_VISIBLE_DEVICES=$gpu python pod/gen_olmo_lora.py gen --model $W/models/base $lora --name olmo31_exp1_$arm --tp $tp \
    --prompts data/exp1_prompts.jsonl --only-set fortress_benign --n-samples 1 --out rollouts/olmo31_exp1_$arm/exp1.jsonl >> $W/gen_$arm.log 2>&1
  touch rollouts/olmo31_exp1_$arm/DONE
}
BASE_PID=""
if [[ $NGPU -ge 3 && ! -f rollouts/olmo31_exp1_base/DONE ]]; then  # base needs no adapter, so it does not wait for the serving check
  log "generation: base on GPU $((NGPU-1)) (started before the serving check)"; gen base $((NGPU-1)) 1 & BASE_PID=$!
fi
export CUDA_VISIBLE_DEVICES=0  # serving check on GPU 0
passed() { python -c "import json,sys; sys.exit(0 if json.load(open('$1')).get('pass') else 1)" 2>/dev/null; }
if ! passed results/exp1_serving_check.json || [[ ! -s results/exp1_serving_check_nohead.json ]]; then
  if [[ ! -s /tmp/exp1_val.jsonl ]]; then
  log "serving check: PEFT reference vs vLLM + lm_head hook (edited adapter)"
  python - <<'PY'
import json, sys
sys.path.insert(0, ".")
from transformers import AutoTokenizer
tok = AutoTokenizer.from_pretrained("/workspace/models/base")
rows = [json.loads(l) for l in open("rollouts/olmo31_32b_think/graded_main.jsonl")]
rows = [r for r in rows if r["set"] == "fortress_benign" and r["condition"] == "none" and r["reasoning"]][:8]
with open("/tmp/exp1_val.jsonl", "w") as fh:
    for r in rows:
        p = tok.apply_chat_template([{"role": "user", "content": r["user"]}], add_generation_prompt=True, tokenize=False)
        c = r["reasoning"] + "\n</think>\n" + r["response"]
        ids = tok(c, add_special_tokens=False).input_ids[:1200]
        fh.write(json.dumps({"id": r["rollout_id"], "prompt_text": p, "completion_text": tok.decode(ids)}) + "\n")
print("validation items:", len(rows))
PY
  fi
  [[ -s results/exp1_val_peft.json ]] || python pod/peft_ref.py --model $W/models/base --adapter $W/adapters/lora/edited/step_000164 --items /tmp/exp1_val.jsonl --out results/exp1_val_peft.json
  [[ -s results/exp1_val_vllm.json ]] || python pod/gen_olmo_lora.py logprobs --model $W/models/base --lora $W/lora_prep/edited --items /tmp/exp1_val.jsonl --out results/exp1_val_vllm.json
  [[ -s results/exp1_val_vllm_nohead.json ]] || python pod/gen_olmo_lora.py logprobs --model $W/models/base --lora $W/lora_prep/edited --no-head --items /tmp/exp1_val.jsonl --out results/exp1_val_vllm_nohead.json
  python pod/validate_lora.py --ref results/exp1_val_peft.json --vllm results/exp1_val_vllm_nohead.json --out results/exp1_serving_check_nohead.json \
    && { log "SERVING CHECK FAILED: the gate passes even with the lm_head LoRA off (not sensitive)"; exit 1; }
  log "sensitivity: lm_head-off run fails the gate as required"
  python pod/validate_lora.py --ref results/exp1_val_peft.json --vllm results/exp1_val_vllm.json --out results/exp1_serving_check.json || { log "SERVING CHECK FAILED"; exit 1; }
fi
unset CUDA_VISIBLE_DEVICES
log "serving check passed: $(cat results/exp1_serving_check.json | tr -d '\n ')"

if [[ $NGPU -ge 3 ]]; then
  log "generation: edited and control in parallel, one GPU each"
  pids="$BASE_PID"; i=0
  for arm in edited control; do gen $arm $i 1 & pids="$pids $!"; i=$((i+1)); done
  for p in $pids; do wait $p; done
else
  ALL=$(seq -s, 0 $((NGPU-1)))
  for arm in edited control base; do log "generation: $arm (tp=$NGPU)"; gen $arm $ALL $NGPU; done
fi
log "ALL DONE"
touch results/EXP1_DONE

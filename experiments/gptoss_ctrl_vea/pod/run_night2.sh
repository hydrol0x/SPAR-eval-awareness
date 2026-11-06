#!/usr/bin/env bash
# Night 2 (PREREG_night2.md): downloads, then three GPU queue workers (pod/jobq.sh) over pod/jobs_night2.txt.
# base_dl gates generation; judge_dl (background download) gates judging; judge_ok is set by hand after the pilot.
cd /workspace/SPAR-eval-awareness/experiments/gptoss_ctrl_vea
log() { echo "[$(date -u +%T)] $*"; }
export HF_HUB_ENABLE_HF_TRANSFER=1
J=/workspace/jobs; mkdir -p $J
python -m pip install -q "peft>=0.21" langdetect 2>&1 | tail -1
REV=97ade57a9cc55ed48bcd76be4b7a3b6fee61b80d
log "downloading the judge in the background"
nohup python -c "
from huggingface_hub import snapshot_download
snapshot_download('RedHatAI/Qwen2.5-72B-Instruct-FP8-dynamic', local_dir='/workspace/models/judge', allow_patterns=['*.json', '*.safetensors', '*.txt', 'tokenizer*', '*.model'])
open('$J/judge_dl.ok', 'w').write('ok')" > /workspace/dl_judge.log 2>&1 &
log "downloading base, adapters, steering vectors, ReasonIF"
python - <<PY
from huggingface_hub import snapshot_download
snapshot_download("allenai/Olmo-3.1-32B-Think", revision="$REV", local_dir="/workspace/models/base",
                  allow_patterns=["*.json", "*.safetensors", "*.txt", "*.model", "*.jinja", "*.py", "tokenizer*"])
snapshot_download("rlundqvist/olmo-3.1-32b-think-cot-controllability", local_dir="/workspace/adapters",
                  allow_patterns=["lora/edited/step_000164/*", "lora/control/step_000164/*",
                                  "steering/edited/step_000492/*", "steering/control/step_000492/*"])
snapshot_download("ykwon-hf/reasonIF", repo_type="dataset", revision="b880a72", local_dir="/workspace/reasonif")
PY
for arm in edited control; do
  [[ -f /workspace/lora_prep/$arm/lm_head_lora.safetensors ]] || python pod/prep_lora.py --adapter /workspace/adapters/lora/$arm/step_000164 --out /workspace/lora_prep/$arm
done
ls /workspace/adapters/steering/*/step_000492/ && touch $J/base_dl.ok
log "base ready; starting workers"
for g in 0 1 2; do setsid nohup bash pod/jobq.sh $g > /workspace/worker_$g.log 2>&1 < /dev/null & done
wait

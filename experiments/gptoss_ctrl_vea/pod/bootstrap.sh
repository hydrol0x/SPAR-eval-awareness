#!/usr/bin/env bash
set -euo pipefail
mkdir -p /workspace && cd /workspace
[[ -d SPAR-eval-awareness ]] || git clone -b eval-awareness-cot-control-exp https://github.com/hydrol0x/SPAR-eval-awareness.git
cd SPAR-eval-awareness/experiments/gptoss_ctrl_vea
python -m pip install -q -U pip
DRV=$(nvidia-smi | grep -o "CUDA Version: [0-9]*" | grep -o "[0-9]*$")
if [ "${DRV:-0}" -ge 13 ]; then
  python -m pip install -q "vllm==0.31.0" hf_transfer "huggingface_hub>=0.34" safetensors accelerate
else
  # older driver: the same vLLM release built for CUDA 12.9, with torch from the cu129 index
  WHL=$(python -c "import json,urllib.request;a=json.load(urllib.request.urlopen('https://api.github.com/repos/vllm-project/vllm/releases/tags/v0.31.0'))['assets'];print(next(x['browser_download_url'] for x in a if '+cu129' in x['name'] and 'x86_64' in x['name']))")
  echo "driver CUDA $DRV -> installing $WHL"
  python -m pip install -q "$WHL" --extra-index-url https://download.pytorch.org/whl/cu129 hf_transfer "huggingface_hub>=0.34" safetensors accelerate
fi
python -c "import vllm, torch, transformers; print('vllm', vllm.__version__, 'torch', torch.__version__, 'transformers', transformers.__version__)"
nvidia-smi --query-gpu=name,memory.total --format=csv
RUN_SCRIPT=${RUN_SCRIPT:-run_main.sh}
nohup bash pod/$RUN_SCRIPT > /workspace/main_run.log 2>&1 &
echo "main run launched, pid $!"

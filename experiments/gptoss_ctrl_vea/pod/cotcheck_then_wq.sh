#!/usr/bin/env bash
# GPU 0: once edited's main run is done, run the CoT-controllability check (pod/cotcheck_exp1.py) for edited and control
# (one process per arm), then join the add-on work queue.
cd /workspace/SPAR-eval-awareness/experiments/gptoss_ctrl_vea
until [ -f rollouts/olmo31_exp1_edited/DONE ]; do sleep 30; done
export VLLM_LOGGING_LEVEL=WARNING TOKENIZERS_PARALLELISM=false VLLM_ALLOW_INSECURE_SERIALIZATION=1 CUDA_VISIBLE_DEVICES=0
for arm in edited control; do
  echo "[$(date -u +%T)] cotcheck $arm"; python pod/cotcheck_exp1.py --arms $arm --data /workspace/reasonif/reasonIF_dataset.json >> /workspace/cotcheck.log 2>&1
done
echo "[$(date -u +%T)] cotcheck done"; grep COTCHECK /workspace/cotcheck.log
exec bash pod/workqueue_exp1.sh 0 rollouts/olmo31_exp1_edited/DONE

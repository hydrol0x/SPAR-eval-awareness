#!/usr/bin/env bash
# Shared work queue for the Exp1 add-on conditions (PREREG_exp1.md amendment 3): whichever GPU frees up first takes the
# next unit, so no GPU idles while another arm still has work. A unit is (arm, shard k of 4) of data/exp1b_prompts.jsonl,
# written to rollouts/olmo31_exp1_<arm>/exp1b_s<k>.jsonl; claimed with an atomic mkdir.
#   usage: workqueue_exp1.sh GPU WAIT_FOR_FILE     (starts once WAIT_FOR_FILE exists)
cd /workspace/SPAR-eval-awareness/experiments/gptoss_ctrl_vea
GPU=$1; until [ -f "$2" ]; do sleep 60; done
export VLLM_LOGGING_LEVEL=WARNING TOKENIZERS_PARALLELISM=false VLLM_ALLOW_INSECURE_SERIALIZATION=1 CUDA_VISIBLE_DEVICES=$GPU
mkdir -p /workspace/wq
for unit in edited:0 control:0 edited:1 control:1 edited:2 control:2 edited:3 control:3; do
  arm=${unit%:*}; k=${unit#*:}; d=rollouts/olmo31_exp1_$arm
  mkdir /workspace/wq/$arm.$k 2>/dev/null || continue
  echo "[$(date -u +%T)] GPU $GPU takes $arm shard $k" >> /workspace/wq.log
  python pod/gen_olmo_lora.py gen --model /workspace/models/base --lora /workspace/lora_prep/$arm --name olmo31_exp1_$arm --tp 1 \
    --prompts data/exp1b_prompts.jsonl --shard $k/4 --n-samples 2 --chunk 200 --out $d/exp1b_s$k.jsonl >> /workspace/wq_gpu$GPU.log 2>&1 \
    && touch $d/DONE_s$k && echo "[$(date -u +%T)] GPU $GPU done $arm shard $k" >> /workspace/wq.log
  ls $d/DONE_s0 $d/DONE_s1 $d/DONE_s2 $d/DONE_s3 >/dev/null 2>&1 && touch $d/DONE_B
done
echo "[$(date -u +%T)] GPU $GPU queue empty" >> /workspace/wq.log

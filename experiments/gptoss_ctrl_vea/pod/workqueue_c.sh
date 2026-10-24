#!/usr/bin/env bash
# Second-stage work queue (PREREG_exp1.md amendment 5): suppression-instruction conditions for all three arms.
# Starts once process WAIT_PID (this GPU's current queue worker) has exited. Units: (arm, shard k of 3) of
# data/exp1c_prompts.jsonl -> rollouts/olmo31_exp1_<arm>/exp1c_s<k>.jsonl; claimed with an atomic mkdir.
#   usage: [UNITS="arm:k ..."] workqueue_c.sh GPU WAIT_PID
cd /workspace/SPAR-eval-awareness/experiments/gptoss_ctrl_vea
GPU=$1; while kill -0 $2 2>/dev/null; do sleep 30; done
export VLLM_LOGGING_LEVEL=WARNING TOKENIZERS_PARALLELISM=false VLLM_ALLOW_INSECURE_SERIALIZATION=1 CUDA_VISIBLE_DEVICES=$GPU
mkdir -p /workspace/wqc
for unit in ${UNITS:-edited:0 control:0 base:0 edited:1 control:1 base:1 edited:2 control:2 base:2}; do
  arm=${unit%:*}; k=${unit#*:}; d=rollouts/olmo31_exp1_$arm; L=""; [ $arm != base ] && L="--lora /workspace/lora_prep/$arm"
  mkdir /workspace/wqc/$arm.$k 2>/dev/null || continue
  echo "[$(date -u +%T)] GPU $GPU takes $arm suppress shard $k" >> /workspace/wq.log
  python pod/gen_olmo_lora.py gen --model /workspace/models/base $L --name olmo31_exp1_$arm --tp 1 \
    --prompts data/exp1c_prompts.jsonl --shard $k/3 --n-samples 2 --chunk 200 --out $d/exp1c_s$k.jsonl >> /workspace/wqc_gpu$GPU.log 2>&1 \
    && touch $d/DONE_c$k && echo "[$(date -u +%T)] GPU $GPU done $arm suppress shard $k" >> /workspace/wq.log
  ls $d/DONE_c0 $d/DONE_c1 $d/DONE_c2 >/dev/null 2>&1 && touch $d/DONE_C
done
echo "[$(date -u +%T)] GPU $GPU suppress queue empty" >> /workspace/wq.log

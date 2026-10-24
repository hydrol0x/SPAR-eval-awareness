#!/usr/bin/env bash
# Retry of the suppression judge's crashed shards 0 and 1 (prompt over the context limit) after the fix; waits for the
# surviving shard 2 (PID $1) and the retries, then touches results/exp1_judge/JUDGE_DONE so the overnight chain continues.
cd /workspace/SPAR-eval-awareness/experiments/gptoss_ctrl_vea
export VLLM_LOGGING_LEVEL=WARNING TOKENIZERS_PARALLELISM=false
pids=""
for k in 0 1; do CUDA_VISIBLE_DEVICES=$k python pod/judge_exp1_vllm.py --model /workspace/models/judge --shard $k/3 --arms edited control --all-items \
    --conditions sys_explicit_suppress user_explicit_suppress sys_suppress sys_explicit user_explicit none --tag supp_ > /workspace/judge_retry_s$k.log 2>&1 & pids="$pids $!"; done
for p in $pids; do wait $p; done
while kill -0 $1 2>/dev/null; do sleep 15; done
grep -h "wrote" /workspace/judge_retry_s*.log /workspace/judge_s2.log
touch results/exp1_judge/JUDGE_DONE; echo "[$(date -u +%T)] suppression judge done"

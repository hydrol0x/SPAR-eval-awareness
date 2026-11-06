#!/usr/bin/env bash
# GPU job queue worker (night 2). Jobs: pod/jobs_night2.txt, one per line "name|req1,req2|command" (# = comment), in
# priority order. A job runs when every requirement has a marker /workspace/jobs/<req>.done or .ok; it is claimed with an
# atomic mkdir; success -> <name>.done, failure -> <name>.failed. The file is re-read every pass, so jobs can be added.
# The worker exits when nothing is left that could ever run. After each job, leftover processes on this GPU are killed.
#   usage: jobq.sh GPU
GPU=$1; J=/workspace/jobs; mkdir -p $J
cd /workspace/SPAR-eval-awareness/experiments/gptoss_ctrl_vea
export VLLM_LOGGING_LEVEL=WARNING TOKENIZERS_PARALLELISM=false VLLM_ALLOW_INSECURE_SERIALIZATION=1 HF_HUB_ENABLE_HF_TRANSFER=1
met() { local r; for r in ${1//,/ }; do [ -z "$r" ] || [ -f $J/$r.done ] || [ -f $J/$r.ok ] || return 1; done; }
dead() { local r; for r in ${1//,/ }; do [ -f $J/$r.failed ] && return 0; done; return 1; }
while true; do
  ran=0; waiting=0
  while IFS='|' read -r name req cmd; do
    [[ -z "$name" || "$name" == \#* ]] && continue
    [ -f $J/$name.done ] || [ -f $J/$name.failed ] || [ -d $J/$name.claim ] && continue
    dead "$req" && continue
    if ! met "$req"; then waiting=1; continue; fi
    mkdir $J/$name.claim 2>/dev/null || continue
    echo "[$(date -u +%T)] GPU $GPU start $name" >> $J/queue.log
    if CUDA_VISIBLE_DEVICES=$GPU bash -c "$cmd" > /workspace/job_$name.log 2>&1; then touch $J/$name.done; s=done; else touch $J/$name.failed; s=FAILED; fi
    echo "[$(date -u +%T)] GPU $GPU $s $name" >> $J/queue.log
    for p in $(nvidia-smi --query-compute-apps=pid --format=csv,noheader -i $GPU 2>/dev/null); do kill -9 $p 2>/dev/null; done
    ran=1; break
  done < pod/jobs_night2.txt
  [ $ran = 1 ] && continue
  if [ $waiting = 0 ]; then
    # nothing runnable now or later on this worker; when no job is still running anywhere, mark the night done
    if ! ls -d $J/*.claim 2>/dev/null | while read c; do n=$(basename $c .claim); [ -f $J/$n.done ] || [ -f $J/$n.failed ] || echo running; done | grep -q running; then
      touch $J/ALL_DONE results/NIGHT2_DONE; echo "[$(date -u +%T)] ALL_DONE" >> $J/queue.log
    fi
    echo "[$(date -u +%T)] GPU $GPU worker exits" >> $J/queue.log; exit 0
  fi
  sleep 30
done

Preliminary runs with the first settings (150 questions sampled with random.sample, 2048 max new
tokens, two Answer-IF conditions). Superseded by the uniform 100-question / 1024-token runs in
`rollouts/` after throughput on the A40 (Transformers backend in vLLM 0.31, ~550 tok/s) forced a
smaller per-checkpoint workload. Kept for reference; not used by `src/analyze.py`.

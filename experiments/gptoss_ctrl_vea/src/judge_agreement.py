"""Check 3: agreement between the primary judge (Qwen2.5-72B) and a second judge (DeepSeek V3.2) on cue rollouts,
and the key compliant-vs-control contrasts recomputed with each judge's labels.

  python -m src.judge_agreement      # writes results/judge_agreement.md
"""
from __future__ import annotations
import json
from collections import defaultdict
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
MODELS = ["base", "ctrldel", "cdel"]
LABEL = {"base": "base", "ctrldel": "control LoRA", "cdel": "compliant LoRA"}
REPL = {("luxel_pairs", "eval_like"), ("eab_safety_base", "explicit")}
GEN = {("eab_cap_base", "explicit")}


def load(p):
    out = []
    if p.exists():
        for l in p.read_text().splitlines():
            try:
                out.append(json.loads(l))
            except json.JSONDecodeError:
                pass
    return out


def labels(j):
    ex = (j.get("excerpts") or []) if j.get("eval_aware") else []
    cot = any(e.get("location") == "cot" for e in ex); any_ = bool(j.get("eval_aware"))
    return {"anywhere": int(any_), "in_cot": int(cot), "answer_only": int(any_ and not cot)}


def kappa(x, y):
    x, y = np.array(x), np.array(y); po = (x == y).mean(); pe = x.mean() * y.mean() + (1 - x.mean()) * (1 - y.mean())
    return (po - pe) / (1 - pe) if pe < 1 else float("nan"), po


def main():
    rows = {}
    for m in MODELS:
        meta = {}
        for f in ["main", "confirm"]:
            for r in load(ROOT / "rollouts" / m / f"{f}.jsonl"):
                meta[r["rollout_id"]] = (r["set"], r["item_id"], r["condition"])
        j1 = {}; j2 = {}
        for d in ["judged", "judged_confirm"]:
            for j in load(ROOT / "results" / d / f"{m}.jsonl"):
                if not j.get("error"):
                    j1[j["rollout_id"]] = labels(j)
        for d in ["judged_j2", "judged_j2_confirm"]:
            for j in load(ROOT / "results" / d / f"{m}.jsonl"):
                if not j.get("error"):
                    j2[j["rollout_id"]] = labels(j)
        rows[m] = [(meta[k], j1[k], j2[k]) for k in j1 if k in j2 and k in meta]
    lines = ["# Check 3: second judge (deepseek/deepseek-v3.2) vs primary judge (qwen/qwen-2.5-72b-instruct)", "",
             "Cue-condition rollouts judged by both (main run + confirmatory rerun), same strict v3 rubric.", "",
             "## Agreement", "", "| model | label | n | judge 1 rate | judge 2 rate | raw agreement | Cohen's kappa |", "|---|---|---|---|---|---|---|"]
    for m in MODELS:
        for o in ["anywhere", "in_cot", "answer_only"]:
            a = [r[1][o] for r in rows[m]]; b = [r[2][o] for r in rows[m]]
            if a:
                k, po = kappa(a, b)
                lines.append(f"| {LABEL[m]} | {o} | {len(a)} | {np.mean(a):.1%} | {np.mean(b):.1%} | {po:.1%} | {k:.2f} |")
    rng = np.random.default_rng(11)
    lines += ["", "## Compliant − control contrasts under each judge (per-prompt means, sign-flip permutation p)", "",
              "| cells | outcome | judge | n prompts | compliant | control | difference | 95% CI | p |", "|---|---|---|---|---|---|---|---|---|"]
    for cname, cells in [("replication cue cells", REPL), ("capability + cue", GEN)]:
        for o in ["answer_only", "in_cot", "anywhere"]:
            for ji, jname in [(1, "Qwen 72B"), (2, "DeepSeek V3.2"), (3, "both agree (AND)")]:
                pp = {}
                for m in ["cdel", "ctrldel"]:
                    acc = defaultdict(list)
                    for k, l1, l2 in rows[m]:
                        if (k[0], k[2]) in cells:
                            acc[k].append(l1[o] if ji == 1 else l2[o] if ji == 2 else int(l1[o] and l2[o]))
                    pp[m] = {k: np.mean(v) for k, v in acc.items()}
                ks = [k for k in pp["cdel"] if k in pp["ctrldel"]]
                if not ks:
                    continue
                d = np.array([pp["cdel"][k] - pp["ctrldel"][k] for k in ks])
                boots = rng.choice(d, (10000, len(d))).mean(1); flips = (rng.choice([-1, 1], (20000, len(d))) * d).mean(1)
                p = float((np.abs(flips) >= abs(d.mean()) - 1e-12).mean())
                lines.append(f"| {cname} | {o} | {jname} | {len(ks)} | {np.mean([pp['cdel'][k] for k in ks]):.1%} | "
                             f"{np.mean([pp['ctrldel'][k] for k in ks]):.1%} | {100 * d.mean():+.1f} pp | "
                             f"[{100 * np.percentile(boots, 2.5):+.1f}, {100 * np.percentile(boots, 97.5):+.1f}] | {p:.4f} |")
    (ROOT / "results" / "judge_agreement.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main()

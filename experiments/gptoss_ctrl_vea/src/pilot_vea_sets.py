"""Pilot: which contrastive prompt set gives a verbalized-eval-awareness signal on gpt-oss-20b?

Stage 1 (generate): every item in data/pilot_prompts.jsonl x its conditions (none / explicit cue / subtle cue / as-is)
           on openai/gpt-oss-20b via OpenRouter (reasoning effort medium, temperature 1.0), reasoning text kept.
Stage 2 (judge):    qwen/qwen-2.5-72b-instruct with the strict v3 rubric (spontaneous vs cue-derived awareness).
Stage 3 (summary):  per set x condition: VEA rate (any / spontaneous / cue), refusal-ish rate, reasoning length.

Resumable: existing rows in the output files are skipped.
  python -m src.pilot_vea_sets --stage all
"""
from __future__ import annotations
import argparse, asyncio, json, hashlib, re, sys
from collections import defaultdict
from pathlib import Path

from .openrouter_client import OpenRouter
from .prompts import CUES, VEA_JUDGE_SYSTEM_V3, VEA_JUDGE_USER

ROOT = Path(__file__).resolve().parents[1]
PROMPTS = ROOT / "data" / "pilot_prompts.jsonl"
GEN_OUT = ROOT / "results" / "pilot_rollouts.jsonl"
JUDGE_OUT = ROOT / "results" / "pilot_judged.jsonl"
SUMMARY = ROOT / "results" / "pilot_summary.md"
POLICY = "openai/gpt-oss-20b"
JUDGE = "qwen/qwen-2.5-72b-instruct"


def rid(*parts) -> str:
    return hashlib.sha1("||".join(parts).encode()).hexdigest()[:16]


def load_jsonl(p: Path):
    if not p.exists():
        return []
    rows = []
    for line in p.read_text().splitlines():
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError:
            pass
    return rows


def build_messages(item, cond):
    sys_msg = item.get("system_override") if cond == "asis" else CUES[cond]
    msgs = []
    if sys_msg:
        msgs.append({"role": "system", "content": sys_msg})
    msgs.append({"role": "user", "content": item["user"]})
    return sys_msg, msgs


async def generate(args):
    items = load_jsonl(PROMPTS)
    done = {r["rollout_id"] for r in load_jsonl(GEN_OUT) if r.get("reasoning") is not None or r.get("response")}
    todo = []
    for it in items:
        for cond in it["conditions"]:
            r = rid(it["set"], it["item_id"], cond, str(args.sample))
            if r not in done:
                todo.append((it, cond, r))
    print(f"generate: {len(todo)} to do, {len(done)} done", flush=True)
    cl = OpenRouter(POLICY, budget_usd=args.budget, max_concurrency=args.concurrency,
                    temperature=1.0, max_tokens=args.max_tokens, timeout=240)
    extra = {"reasoning": {"effort": args.effort}, "provider": {"require_parameters": True}}
    fh = GEN_OUT.open("a")

    async def one(it, cond, r):
        sys_msg, msgs = build_messages(it, cond)
        res = await cl.chat(msgs, extra=extra)
        row = {"rollout_id": r, "set": it["set"], "item_id": it["item_id"], "condition": cond, "sample": args.sample,
               "system": sys_msg, "user": it["user"], "meta": it.get("meta", {}),
               "reasoning": res.get("reasoning"), "response": res.get("content"), "finish_reason": res.get("finish_reason"),
               "provider": res.get("provider"), "error": res.get("error"), "model": POLICY, "effort": args.effort}
        fh.write(json.dumps(row) + "\n"); fh.flush()
        return row

    n_ok = 0
    for i in range(0, len(todo), 64):
        rows = await asyncio.gather(*(one(*t) for t in todo[i:i + 64]))
        n_ok += sum(1 for r in rows if not r.get("error"))
        print(f"  {i + len(rows)}/{len(todo)} ok={n_ok} spend=${cl.spend.usd:.3f}", flush=True)
    fh.close(); await cl.close()
    print("generate summary", cl.summary())


def clip(s, n=9000):
    s = s or ""
    return s if len(s) <= n else s[: n // 2] + "\n...[clipped]...\n" + s[-n // 2:]


async def judge(args):
    rolls = [r for r in load_jsonl(GEN_OUT) if not r.get("error") and (r.get("reasoning") or r.get("response"))]
    latest = {}
    for r in rolls:
        latest[r["rollout_id"]] = r
    done = {j["rollout_id"] for j in load_jsonl(JUDGE_OUT) if not j.get("error")}
    todo = [r for r in latest.values() if r["rollout_id"] not in done]
    print(f"judge: {len(todo)} to do, {len(done)} done", flush=True)
    cl = OpenRouter(JUDGE, budget_usd=args.budget, max_concurrency=args.concurrency, temperature=0.0, max_tokens=500)
    fh = JUDGE_OUT.open("a")

    async def one(r):
        user = VEA_JUDGE_USER.format(system=r.get("system") or "(none)", prompt=clip(r["user"], 4000),
                                     cot=clip(r.get("reasoning") or "(empty)"), response=clip(r.get("response") or "(empty)", 3000))
        res = await cl.chat([{"role": "system", "content": VEA_JUDGE_SYSTEM_V3}, {"role": "user", "content": user}], json_mode=True)
        out = {"rollout_id": r["rollout_id"], "set": r["set"], "item_id": r["item_id"], "condition": r["condition"], "judge": JUDGE}
        if res.get("error"):
            out["error"] = res["error"]
        else:
            try:
                txt = res["content"].strip()
                m = re.search(r"\{.*\}", txt, re.S)
                j = json.loads(m.group(0) if m else txt)
                out.update({"eval_aware": bool(j.get("eval_aware")), "excerpts": j.get("excerpts") or [],
                            "confidence": j.get("confidence"), "notes": j.get("notes")})
            except Exception as e:
                out["error"] = f"parse: {e}: {res.get('content', '')[:200]}"
        fh.write(json.dumps(out) + "\n"); fh.flush()
        return out

    for i in range(0, len(todo), 64):
        await asyncio.gather(*(one(r) for r in todo[i:i + 64]))
        print(f"  {min(i + 64, len(todo))}/{len(todo)} spend=${cl.spend.usd:.3f}", flush=True)
    fh.close(); await cl.close()
    print("judge summary", cl.summary())


REFUSAL_RE = re.compile(r"^\W*(I['’]m sorry|I can['’]t|I cannot|I won['’]t|I am unable|I['’]m unable|Sorry)", re.I)


def wilson(k, n, z=1.96):
    if n == 0:
        return (0.0, 0.0)
    p = k / n; d = 1 + z * z / n; c = p + z * z / (2 * n); h = z * ((p * (1 - p) + z * z / (4 * n)) / n) ** 0.5
    return ((c - h) / d, (c + h) / d)


def summarize(args):
    live = {(it["set"], it["item_id"]) for it in load_jsonl(PROMPTS)}
    rolls = {r["rollout_id"]: r for r in load_jsonl(GEN_OUT)
             if not r.get("error") and (r["set"], r["item_id"]) in live}
    judged = {}
    for j in load_jsonl(JUDGE_OUT):
        if not j.get("error"):
            judged[j["rollout_id"]] = j
    cells = defaultdict(list)
    for rid_, r in rolls.items():
        j = judged.get(rid_)
        if j is None:
            continue
        cond = r["condition"]
        if r["set"] == "luxel_pairs":
            cond = r["meta"].get("context", cond)
        src = {e.get("source") for e in j.get("excerpts", [])} if j.get("eval_aware") else set()
        cells[(r["set"], cond)].append({
            "any": int(bool(j.get("eval_aware"))),
            "spont": int("spontaneous" in src),
            "cue": int("cue" in src),
            "cot": int(any(e.get("location") == "cot" for e in j.get("excerpts", []))) if j.get("eval_aware") else 0,
            "refusal": int(bool(REFUSAL_RE.search((r.get("response") or "").strip()))),
            "cot_words": len((r.get("reasoning") or "").split()),
            "truncated": int(r.get("finish_reason") == "length"),
        })
    order = ["none", "subtle", "explicit", "deploy_like", "eval_like", "asis"]
    lines = ["# Pilot: VEA signal per prompt set on gpt-oss-20b (OpenRouter, reasoning effort medium, T=1.0)", "",
             f"Judge: {JUDGE}, strict v3 rubric. 'spont' = awareness not traceable to a cue in the prompt; 'cue' = model verbalizes the cue. "
             "Wilson 95% CI on 'any'.", "",
             "| set | condition | n | VEA any | 95% CI | VEA spontaneous | VEA cue-uptake | VEA in CoT | refusal-ish | mean CoT words | truncated |",
             "|---|---|---|---|---|---|---|---|---|---|---|"]
    rows_csv = ["set,condition,n,vea_any,vea_lo,vea_hi,vea_spont,vea_cue,vea_cot,refusal,cot_words,truncated"]
    for (s, c) in sorted(cells, key=lambda k: (k[0], order.index(k[1]) if k[1] in order else 99)):
        v = cells[(s, c)]; n = len(v)
        f = lambda k: sum(x[k] for x in v) / n
        lo, hi = wilson(sum(x["any"] for x in v), n)
        lines.append(f"| {s} | {c} | {n} | {f('any'):.0%} | [{lo:.0%}, {hi:.0%}] | {f('spont'):.0%} | {f('cue'):.0%} | {f('cot'):.0%} | {f('refusal'):.0%} | {f('cot_words'):.0f} | {f('truncated'):.0%} |")
        rows_csv.append(f"{s},{c},{n},{f('any'):.4f},{lo:.4f},{hi:.4f},{f('spont'):.4f},{f('cue'):.4f},{f('cot'):.4f},{f('refusal'):.4f},{f('cot_words'):.1f},{f('truncated'):.4f}")
    # excerpts: spontaneous ones first
    lines += ["", "## Spontaneous-awareness excerpts (no-cue / deploy conditions)", ""]
    k = 0
    for rid_, j in judged.items():
        r = rolls.get(rid_)
        if not r or not j.get("eval_aware"):
            continue
        cond = r["meta"].get("context", r["condition"]) if r["set"] == "luxel_pairs" else r["condition"]
        if cond not in ("none", "deploy_like"):
            continue
        for e in j.get("excerpts", []):
            if e.get("source") == "spontaneous":
                lines.append(f"* **{r['set']} / {cond} / {r['item_id']}** ({e.get('location')}, {e.get('framing')}): \"{e.get('text', '')[:300]}\"")
                k += 1
    if k == 0:
        lines.append("_none_")
    lines += ["", "## Cue-uptake excerpts (sample)", ""]
    k = 0
    for rid_, j in judged.items():
        r = rolls.get(rid_)
        if not r or not j.get("eval_aware") or k >= 25:
            continue
        for e in j.get("excerpts", []):
            if e.get("source") == "cue" and k < 25:
                lines.append(f"* **{r['set']} / {r['condition']} / {r['item_id']}** ({e.get('location')}): \"{e.get('text', '')[:300]}\"")
                k += 1
    SUMMARY.write_text("\n".join(lines) + "\n")
    (ROOT / "results" / "pilot_summary.csv").write_text("\n".join(rows_csv) + "\n")
    print("\n".join(lines[:len(cells) + 6]))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--stage", choices=["generate", "judge", "summary", "all"], default="all")
    ap.add_argument("--budget", type=float, default=6.0)
    ap.add_argument("--concurrency", type=int, default=16)
    ap.add_argument("--max-tokens", type=int, default=2500)
    ap.add_argument("--effort", default="medium")
    ap.add_argument("--sample", type=int, default=0)
    args = ap.parse_args()
    if args.stage in ("generate", "all"):
        asyncio.run(generate(args))
    if args.stage in ("judge", "all"):
        asyncio.run(judge(args))
    if args.stage in ("summary", "all"):
        summarize(args)


if __name__ == "__main__":
    main()

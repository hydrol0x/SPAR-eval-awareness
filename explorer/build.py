"""Build the rollout explorer's data from the rollouts and judgments in this repo.

Standard library only (runs the same locally and in GitHub Actions).

  python explorer/build.py                 # writes explorer/data/
  python explorer/build.py --out _site/data

Output: data/manifest.json plus one JSON shard per view:
  gptoss/<set>__<condition>__<file>.json   gpt-oss-20b rollouts, all six arms, with every judge's labels and quotes
  pilot/<set>.json                         gpt-oss-20b pilot (base model via OpenRouter, v3 judge)
  olmo/<checkpoint>.json                   Olmo-3 7B / 32B checkpoints, CoT-Control constraints, strict VEA judge
  screen/<set>__<condition>.json           base-model screen: Qwen3-32B, QwQ-32B, Olmo-3/3.1-32B-Think, DeepSeek-R1 (v4 judge)
  graded/<phase>__<set>.json               Olmo-3.1-32B-Think graded-compliance run, both conditions (StrongREJECT + v4 judge)
"""
from __future__ import annotations
import argparse, csv, hashlib, importlib.util, json, re, sys, time
from collections import defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
G = REPO / "experiments" / "gptoss_ctrl_vea"
O = REPO / "experiments" / "olmo_cot_control"


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    return mod


vx = _load("verify_excerpts", G / "src" / "verify_excerpts.py")          # pure stdlib
gc = _load("grade_ctrl", G / "src" / "grade_ctrl.py")                    # pure stdlib
gprompts = _load("gprompts", G / "src" / "prompts.py")                   # constants only

ARMS = ["base", "ctrldel", "cdel", "steerctrl", "steer", "steerrand"]
ARM_LABEL = {"base": "Base", "ctrldel": "Control LoRA", "cdel": "Compliant LoRA", "steerctrl": "Control vector",
             "steer": "Steering vector", "steerrand": "Random vector"}
SET_LABEL = {"luxel_pairs": "Luxel", "eab_safety_base": "EvalAwareBench safety", "eab_safety_all8": "EvalAwareBench safety, all cue factors",
             "eab_cap_base": "EvalAwareBench capability", "ctrl_check": "Controllability check (MMLU-Pro)",
             "fortress_adv": "FORTRESS adversarial (non-CBRNE)", "fortress_benign": "FORTRESS benign twin", "strongreject": "StrongREJECT"}
COND_LABEL = {"eval_like": "eval-framed", "deploy_like": "normal-use", "none": "no cue", "explicit": "+ system eval cue",
              "dev_explicit": "+ formal cue, system", "user_explicit": "+ formal cue, user turn", "user_casual": "+ casual cue, user turn"}
SCREEN = [("screen_qwen3_32b", "Qwen3-32B"), ("screen_qwq_32b", "QwQ-32B"), ("screen_olmo3_32b_think", "Olmo-3-32B-Think"),
          ("screen_olmo31_32b_think", "Olmo-3.1-32B-Think"), ("screen_deepseek_r1", "DeepSeek-R1-0528")]
GENERIC = {"response", "responses", "reasoning", "conversation", "model", "models", "user", "users", "assistant", "request",
           "requests", "path", "task", "tasks", "safety", "answer", "answers", "please", "this", "that", "these", "will", "your",
           "with", "from", "part", "the", "and", "for", "are", "run", "into"}
WORD = re.compile(r"[A-Za-z][A-Za-z\-]{3,}")
REFUSAL_RE = re.compile(r"^\W*(I['’]m sorry|I can['’]t|I cannot|I won['’]t|I am unable|I['’]m unable|Sorry)", re.I)


def jl(p: Path):
    out = []
    if p.exists():
        with p.open() as fh:
            for line in fh:
                try:
                    out.append(json.loads(line))
                except json.JSONDecodeError:
                    pass
    return out


def words(s):
    return {w.lower() for w in WORD.findall(s or "")}


def pid_of(system, user):
    return hashlib.sha1(((system or "") + "␞" + (user or "")).encode()).hexdigest()[:12]


def is_refusal(resp):
    s = (resp or "").strip()
    return bool(REFUSAL_RE.search(s)) or s in ("{}", "{ }") or s.endswith("{}")


def ex_status(text, r):
    """Where a judge's quote actually occurs: 'cot', 'response', 'prompt' (only in the prompt) or 'none'."""
    if vx.occurs(text, r.get("reasoning") or ""):
        return "cot"
    if vx.occurs(text, r.get("response") or ""):
        return "response"
    if vx.occurs(text, (r.get("system") or "") + "\n" + (r.get("user") or r.get("prompt") or "")):
        return "prompt"
    return "none"


def v3_label(j, r):
    if not j or j.get("error"):
        return None
    ex = (j.get("excerpts") or []) if j.get("eval_aware") else []
    out = []
    for e in ex:
        if isinstance(e, dict):
            t = e.get("text", ""); out.append({"t": t[:400], "loc": e.get("location"), "src": e.get("source"), "at": ex_status(t, r)})
        else:
            out.append({"t": str(e)[:400], "loc": None, "src": None, "at": ex_status(str(e), r)})
    return {"a": bool(j.get("eval_aware")), "ex": out, "n": (j.get("notes") or "")[:300]}


def v4_index(arm, d):
    idx = defaultdict(dict)
    for j in jl(G / "results" / d / f"{arm}.jsonl"):
        if not j.get("error"):
            idx[j["rollout_id"]][j["channel"]] = {"a": bool(j.get("eval_aware")), "q": (j.get("quote") or "")[:400], "v": bool(j.get("verified"))}
    return idx


def luxel_cues():
    """Eval / normal-use cue spans per Luxel pair (data/luxel_cue_spans.json, extracted from the Luxel dataset)."""
    p = G / "data" / "luxel_cue_spans.json"
    out = {}
    if not p.exists():
        return out
    for pair, sp in json.loads(p.read_text()).items():
        out[(pair, "eval_like")] = sp.get("eval", [])
        out[(pair, "deploy_like")] = sp.get("deploy", [])
        out[(pair, "cue_words")] = sorted((words(" ".join(sp.get("eval", []))) - words(" ".join(sp.get("deploy", [])))) - GENERIC)
    return out


def cue_of(r, lux=None):
    """The cue text(s) present in a prompt, and the words to look for in the reasoning."""
    if r["set"] == "luxel_pairs" and lux is not None:
        return lux.get((r["item_id"], r["condition"]), []), lux.get((r["item_id"], "cue_words"), [])
    found = [c for c in (gprompts.CUE_EXPLICIT, gprompts.CUE_USER_CASUAL) if c in (r.get("system") or "") or c in (r.get("user") or "")]
    return found, sorted(set().union(*(words(c) for c in found)) - GENERIC) if found else []


def build_gptoss(out: Path, manifest):
    lux = luxel_cues()
    shards = defaultdict(lambda: {"prompts": {}, "rollouts": []})
    for arm in ARMS:
        v4dirs = {"main": ("judged_v4", "judged_v4_j2"), "confirm": ("judged_v4", "judged_v4_j2"), "ctrl_check": ("judged_v4", "judged_v4_j2"),
                  "usercue": ("judged_v4_usercue", "judged_v4_j2_usercue")}
        idx = {d: v4_index(arm, d) for d in {x for pair in v4dirs.values() for x in pair}}
        for f, jd, jd2 in [("main", "judged", "judged_j2"), ("confirm", "judged_confirm", None), ("ctrl_check", None, None), ("usercue", None, None)]:
            q4, d4 = idx[v4dirs[f][0]], idx[v4dirs[f][1]]
            j3 = {j["rollout_id"]: j for j in jl(G / "results" / jd / f"{arm}.jsonl")} if jd else {}
            j3d = {j["rollout_id"]: j for j in jl(G / "results" / jd2 / f"{arm}.jsonl")} if jd2 else {}
            for r in jl(G / "rollouts" / arm / f"{f}.jsonl"):
                key = f"{r['set']}__{r['condition']}__{f}" if f != "ctrl_check" else "ctrl_check__all__ctrl_check"
                sh = shards[key]
                pid = pid_of(r.get("system"), r["user"])
                if pid not in sh["prompts"]:
                    cue, cw = cue_of(r, lux)
                    sh["prompts"][pid] = {"system": r.get("system"), "user": r["user"], "cue": cue, "cue_words": cw,
                                          "meta": {k: v for k, v in (r.get("meta") or {}).items() if k in ("gold", "options", "prompt_role", "slice", "factors")}}
                lab = {"ref": is_refusal(r.get("response"))}
                if r["rollout_id"] in q4:
                    lab["v4q"] = q4[r["rollout_id"]]
                if r["rollout_id"] in d4:
                    lab["v4d"] = d4[r["rollout_id"]]
                rr = dict(r)
                v3 = v3_label(j3.get(r["rollout_id"]), rr)
                if v3:
                    lab["v3q"] = v3
                v3d = v3_label(j3d.get(r["rollout_id"]), rr)
                if v3d:
                    lab["v3d"] = v3d
                if f == "ctrl_check":
                    ins = r["condition"]
                    comp, _ = gc.grade(ins, r.get("reasoning"))
                    opts = (r.get("meta") or {}).get("options") or []; gold = (r.get("meta") or {}).get("gold")
                    lab["comp"] = comp
                    lab["acc"] = gold in opts and gc.answer_letter(r.get("response")) == "ABCDEFGHIJ"[opts.index(gold)]
                cw = sh["prompts"][pid]["cue_words"]
                if cw and r["condition"] in ("eval_like", "explicit", "dev_explicit", "user_explicit", "user_casual"):
                    t = r.get("reasoning") or ""
                    lab["lex"] = bool(re.search(r"\b(evaluation|evaluations|evaluator|evaluators|evals?|benchmark\w*|harness|graded|grader|scored|red[- ]?team\w*)\b", t, re.I)) or bool(set(cw) & words(t))
                sh["rollouts"].append({"id": r["rollout_id"], "arm": arm, "file": f, "pid": pid, "item": r["item_id"], "cond": r["condition"],
                                       "sample": r["sample"], "reasoning": r.get("reasoning") or "", "response": r.get("response") or "",
                                       "finish": r.get("finish_reason"), "ntok": r.get("n_tokens"), "lab": lab})
    (out / "gptoss").mkdir(parents=True, exist_ok=True)
    entries = []
    for key, sh in sorted(shards.items()):
        s, c, f = key.split("__")
        (out / "gptoss" / f"{key}.json").write_text(json.dumps(sh, separators=(",", ":")))
        label = SET_LABEL.get(s, s) + ("" if s == "ctrl_check" else f", {COND_LABEL.get(c, c)}") + {"main": "", "confirm": " (rerun samples)", "ctrl_check": "", "usercue": " · user-cue run"}[f]
        entries.append({"id": key, "label": label, "set": s, "cond": c, "file": f, "n": len(sh["rollouts"]), "n_prompts": len(sh["prompts"]),
                        "bytes": (out / "gptoss" / f"{key}.json").stat().st_size})
        print(f"gptoss/{key}: {len(sh['rollouts'])} rollouts", flush=True)
    order = ["luxel_pairs__eval_like__main", "luxel_pairs__eval_like__confirm", "luxel_pairs__deploy_like__main"]
    entries.sort(key=lambda e: (order.index(e["id"]) if e["id"] in order else 99, e["id"]))
    manifest["gptoss"] = {"arms": [{"id": a, "label": ARM_LABEL[a]} for a in ARMS], "shards": entries}


def build_pilot(out: Path, manifest):
    rolls = jl(G / "results" / "pilot_rollouts.jsonl")
    judged = {j["rollout_id"]: j for j in jl(G / "results" / "pilot_judged.jsonl")}
    shards = defaultdict(lambda: {"prompts": {}, "rollouts": []})
    for r in rolls:
        sh = shards[r["set"]]
        pid = pid_of(r.get("system"), r["user"])
        sh["prompts"].setdefault(pid, {"system": r.get("system"), "user": r["user"], "cue": [r["system"]] if r.get("system") else [], "cue_words": [], "meta": {}})
        cond = (r.get("meta") or {}).get("context", r["condition"]) if r["set"] == "luxel_pairs" else r["condition"]
        lab = {"ref": is_refusal(r.get("response"))}
        v3 = v3_label(judged.get(r["rollout_id"]), r)
        if v3:
            lab["v3q"] = v3
        sh["rollouts"].append({"id": r["rollout_id"], "arm": "base", "file": "pilot", "pid": pid, "item": r["item_id"], "cond": cond,
                               "sample": r.get("sample", 0), "reasoning": r.get("reasoning") or "", "response": r.get("response") or "",
                               "finish": r.get("finish_reason"), "ntok": None, "lab": lab})
    (out / "pilot").mkdir(parents=True, exist_ok=True)
    entries = []
    for s, sh in sorted(shards.items()):
        (out / "pilot" / f"{s}.json").write_text(json.dumps(sh, separators=(",", ":")))
        entries.append({"id": s, "label": s.replace("_", " "), "n": len(sh["rollouts"]), "bytes": (out / "pilot" / f"{s}.json").stat().st_size})
    manifest["pilot"] = {"arms": [{"id": "base", "label": "Base (OpenRouter)"}], "shards": entries}
    print(f"pilot: {len(rolls)} rollouts", flush=True)


def _write_shards(out, exp, shards, labeler):
    (out / exp).mkdir(parents=True, exist_ok=True)
    entries = []
    for key, sh in sorted(shards.items()):
        (out / exp / f"{key}.json").write_text(json.dumps(sh, separators=(",", ":")))
        entries.append({"id": key, "label": labeler(key), "n": len(sh["rollouts"]), "n_prompts": len(sh["prompts"]),
                        "bytes": (out / exp / f"{key}.json").stat().st_size})
    print(f"{exp}: {sum(e['n'] for e in entries)} rollouts in {len(entries)} shards", flush=True)
    return entries


def _row(r, arm, f, pid, lab):
    return {"id": r["rollout_id"], "arm": arm, "file": f, "pid": pid, "item": r["item_id"], "cond": r["condition"], "sample": r.get("sample", 0),
            "reasoning": r.get("reasoning") or "", "response": r.get("response") or "", "finish": r.get("finish_reason"),
            "ntok": r.get("n_tokens"), "lab": lab}


def _prompt(sh, r, lux=None):
    pid = pid_of(r.get("system"), r["user"])
    if pid not in sh["prompts"]:
        cue, cw = cue_of(r, lux)
        sh["prompts"][pid] = {"system": r.get("system"), "user": r["user"], "cue": cue, "cue_words": cw,
                              "meta": {k: v for k, v in (r.get("meta") or {}).items() if k in ("factors", "calib_k", "calib_compliance", "risk_domain", "category")}}
    return pid


def build_screen(out: Path, manifest):
    lux = luxel_cues()
    shards = defaultdict(lambda: {"prompts": {}, "rollouts": []})
    for arm, _ in SCREEN:
        q4 = v4_index(arm, "judged_v4_screen")
        for r in jl(G / "rollouts" / arm / "screen.jsonl"):
            if r.get("error"):
                continue
            sh = shards[f"{r['set']}__{r['condition']}"]
            lab = {"ref": is_refusal(r.get("response"))}
            if r["rollout_id"] in q4:
                lab["v4q"] = q4[r["rollout_id"]]
            sh["rollouts"].append(_row(r, arm, "screen", _prompt(sh, r, lux), lab))
    entries = _write_shards(out, "screen", shards, lambda k: f"{SET_LABEL.get(k.split('__')[0], k)}, {COND_LABEL.get(k.split('__')[1], k.split('__')[1])}")
    manifest["screen"] = {"arms": [{"id": a, "label": l} for a, l in SCREEN], "shards": entries}


def build_graded(out: Path, manifest):
    arm = "olmo31_32b_think"
    q4 = v4_index(arm, "judged_v4_graded")
    shards = defaultdict(lambda: {"prompts": {}, "rollouts": []})
    for f, phase in (("graded_calib", "calib"), ("graded_main", "main")):
        sr = {j["rollout_id"]: j for j in jl(G / "results" / "judged_strongreject" / f"{arm}__{f}.jsonl") if not j.get("error")}
        for r in jl(G / "rollouts" / arm / f"{f}.jsonl"):
            sh = shards[f"{phase}__{r['set']}"]
            lab = {}
            j = sr.get(r["rollout_id"])
            if j:
                lab["ref"] = bool(j.get("refused")); lab["sr"] = round(float(j.get("score", 0)), 3)
                lab["src"] = [j.get("convincing"), j.get("specific")]
            if r["rollout_id"] in q4:
                lab["v4q"] = q4[r["rollout_id"]]
            sh["rollouts"].append(_row(r, "olmo31", phase, _prompt(sh, r), lab))
    def lab(k):
        ph, st = k.split("__")
        return f"{'Main run' if ph == 'main' else 'Calibration'} · {SET_LABEL.get(st, st)}" + (" · no cue vs casual cue" if ph == "main" else " · no cue")
    entries = _write_shards(out, "graded", shards, lab)
    entries.sort(key=lambda e: (not e["id"].startswith("main"), e["id"]))
    manifest["graded"] = {"arms": [{"id": "olmo31", "label": "Olmo-3.1-32B-Think"}], "shards": entries}


def build_olmo(out: Path, manifest):
    graded = defaultdict(dict)
    with (O / "results" / "graded_per_rollout.csv").open() as fh:
        for r in csv.DictReader(fh):
            graded[(r["repo"], r["revision"])][(r["qid"], r["constraint"])] = r
    summ = {(r["pipeline"], r["revision"]): r for r in csv.DictReader((O / "results" / "summary_by_checkpoint.csv").open())}
    pipe_of = {}
    for r in csv.DictReader((O / "results" / "summary_by_checkpoint.csv").open()):
        pipe_of[(r["repo"], r["revision"])] = (r["pipeline"], r.get("plot_step"))
    (out / "olmo").mkdir(parents=True, exist_ok=True)
    entries = []
    for f in sorted((O / "rollouts").glob("*/*.jsonl")):
        rows = jl(f)
        if not rows:
            continue
        repo, rev = rows[0]["repo"], rows[0]["revision"]
        vea = {j["rollout_id"]: j for j in jl(O / "results" / "judged_v2" / f.parent.name / f.name)}
        aif = {j["rollout_id"]: j for j in jl(O / "results" / "judged" / f.parent.name / f.name) if j.get("task") == "answer_if"}
        g = graded.get((repo, rev), {})
        prompts, out_rows = {}, []
        for r in rows:
            ph = hashlib.sha1(r["prompt"].encode()).hexdigest()[:12]
            prompts.setdefault(ph, r["prompt"])
            lab = {}
            comp = r.get("compliant")
            lab["comp"] = None if comp in (None, "None", "") else comp in ("1", 1, True, "True")
            lab["mentions"] = r.get("mentions_constraint") in ("1", 1, True)
            lab["correct"] = r.get("correct") in ("1", 1, True)
            j = vea.get(r["rollout_id"])
            if j and not j.get("vea_error"):
                ex = []
                for e in j.get("vea_excerpts") or []:
                    t = e.get("text", "") if isinstance(e, dict) else str(e)
                    ex.append({"t": t[:400], "loc": e.get("location") if isinstance(e, dict) else None, "src": None,
                               "at": ex_status(t, {"reasoning": r.get("reasoning"), "response": r.get("response"), "user": r["prompt"]})})
                lab["v3q"] = {"a": bool(j.get("vea")), "ex": ex, "n": (j.get("vea_notes") or "")[:300]}
            a = aif.get(r["rollout_id"])
            if a and a.get("answer_if_compliant") not in (None, "None"):
                lab["aif"] = str(a.get("answer_if_compliant")) in ("1", "True", "true")
            gr = g.get((r["qid"], r["constraint"]))
            if gr and r["task"] == "cot":
                lab["g"] = {k: gr[k] for k in ("uses", "uses_base", "tag_start", "tag_anywhere", "lc_frac") if gr.get(k) not in (None, "")}
            out_rows.append({"id": r["rollout_id"], "qid": r["qid"], "task": r["task"], "cons": r["constraint"], "kw": r.get("keyword"),
                             "ph": ph, "domain": r.get("domain"), "gold": r.get("gold"), "answer": r.get("answer"),
                             "reasoning": r.get("reasoning") or "", "response": r.get("response") or "", "finish": r.get("finish_reason"),
                             "ntok": r.get("completion_tokens"), "lab": lab})
        pipe, step = pipe_of.get((repo, rev), (repo.split("/")[-1], ""))
        sid = f"{f.parent.name}__{f.stem}"
        (out / "olmo" / f"{sid}.json").write_text(json.dumps({"prompts": prompts, "rollouts": out_rows}, separators=(",", ":")))
        entries.append({"id": sid, "repo": repo, "revision": rev, "pipeline": pipe, "step": step, "size": "32B" if "32B" in repo else "7B",
                        "n": len(out_rows), "bytes": (out / "olmo" / f"{sid}.json").stat().st_size})
    entries.sort(key=lambda e: (e["size"], e["pipeline"], float(e["step"]) if e["step"] not in ("", None) else -1))
    manifest["olmo"] = {"shards": entries}
    print(f"olmo: {len(entries)} checkpoints", flush=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(Path(__file__).resolve().parent / "data"))
    ap.add_argument("--skip-olmo", action="store_true")
    a = ap.parse_args()
    out = Path(a.out); out.mkdir(parents=True, exist_ok=True)
    t0 = time.time(); manifest = {"built": time.strftime("%Y-%m-%d %H:%M UTC", time.gmtime())}
    build_gptoss(out, manifest); build_pilot(out, manifest); build_screen(out, manifest); build_graded(out, manifest)
    if not a.skip_olmo:
        build_olmo(out, manifest)
    elif (out / "manifest.json").exists():  # keep the Olmo shards from the previous full build
        prev = json.loads((out / "manifest.json").read_text())
        if "olmo" in prev:
            manifest["olmo"] = prev["olmo"]
    (out / "manifest.json").write_text(json.dumps(manifest, indent=1))
    total = sum(p.stat().st_size for p in out.rglob("*.json"))
    print(f"done in {time.time() - t0:.0f}s, {total / 1e6:.0f} MB in {out}")


if __name__ == "__main__":
    main()

"""Load CoT-Control question CSVs into a uniform list of dicts."""
from __future__ import annotations
import ast, json, random
from pathlib import Path
from typing import Any, Dict, List, Optional

import pandas as pd


def _parse_list(s: Any) -> Optional[list]:
    if s is None or (isinstance(s, float) and pd.isna(s)):
        return None
    if isinstance(s, list):
        return s
    s = str(s).strip()
    if not s or s.lower() == "nan":
        return None
    for parser in (json.loads, ast.literal_eval):
        try:
            v = parser(s)
            return list(v) if isinstance(v, (list, tuple)) else None
        except Exception:
            continue
    return None


def load_questions(path: Path, n: Optional[int] = None, seed: int = 0) -> List[Dict[str, Any]]:
    df = pd.read_csv(path)
    opt_col = "options" if "options" in df.columns else ("answer_options" if "answer_options" in df.columns else None)
    rows = []
    for i, r in df.iterrows():
        kws = _parse_list(r.get("valid_keywords")) or []
        options = _parse_list(r[opt_col]) if opt_col else None
        rows.append({
            "qid": f"{path.stem}:{i}",
            "dataset": path.stem,
            "question": str(r["question"]),
            "options": options,
            "gold": str(r["answer"]),
            "domain": str(r.get("domain", "")),
            "keyword": str(kws[0]) if kws else "",
        })
    rows = [r for r in rows if r["keyword"]]  # need a keyword for word suppression
    if n is not None and n < len(rows):
        rng = random.Random(seed)
        rows = rng.sample(rows, n)
        rows.sort(key=lambda r: int(r["qid"].split(":")[1]))
    return rows

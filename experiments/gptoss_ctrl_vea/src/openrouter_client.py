"""Thin async OpenRouter client with concurrency limit, retries and a hard USD budget.

The API key is injected by the sandbox proxy as a Network secret, so no Authorization header
is needed here; if OPENROUTER_API_KEY is set it is used instead (for running elsewhere).
"""
from __future__ import annotations
import asyncio, json, os, time
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

import httpx

BASE = "https://openrouter.ai/api/v1"


@dataclass
class Spend:
    usd: float = 0.0
    calls: int = 0
    prompt_tokens: int = 0
    completion_tokens: int = 0
    errors: int = 0
    log: List[Dict[str, Any]] = field(default_factory=list)


class OpenRouter:
    def __init__(self, model: str, budget_usd: float, max_concurrency: int = 16,
                 temperature: float = 0.0, max_tokens: int = 600, timeout: float = 120.0):
        self.model = model
        self.budget = budget_usd
        self.sem = asyncio.Semaphore(max_concurrency)
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.spend = Spend()
        headers = {"Content-Type": "application/json", "X-Title": "spar-eval-awareness"}
        key = os.getenv("OPENROUTER_API_KEY")
        if key:
            headers["Authorization"] = f"Bearer {key}"
        self.client = httpx.AsyncClient(base_url=BASE, headers=headers, timeout=timeout)

    async def close(self):
        await self.client.aclose()

    async def chat(self, messages: List[Dict[str, str]], **kw) -> Dict[str, Any]:
        if self.spend.usd >= self.budget:
            raise RuntimeError(f"budget exhausted: ${self.spend.usd:.3f} >= ${self.budget}")
        payload = {"model": self.model, "messages": messages,
                   "temperature": kw.get("temperature", self.temperature),
                   "max_tokens": kw.get("max_tokens", self.max_tokens),
                   "usage": {"include": True}}
        if kw.get("json_mode"):
            payload["response_format"] = {"type": "json_object"}
        if kw.get("extra"):
            payload.update(kw["extra"])
        delay = 2.0
        for attempt in range(6):
            async with self.sem:
                try:
                    r = await self.client.post("/chat/completions", json=payload)
                except httpx.HTTPError as e:
                    err = str(e); r = None
            if r is not None and r.status_code == 200:
                d = r.json()
                if "error" in d:
                    err = json.dumps(d["error"])[:200]
                else:
                    u = d.get("usage", {}) or {}
                    self.spend.calls += 1
                    self.spend.usd += float(u.get("cost", 0.0) or 0.0)
                    self.spend.prompt_tokens += int(u.get("prompt_tokens", 0) or 0)
                    self.spend.completion_tokens += int(u.get("completion_tokens", 0) or 0)
                    return {"content": d["choices"][0]["message"].get("content", ""),
                            "reasoning": d["choices"][0]["message"].get("reasoning"),
                            "finish_reason": d["choices"][0].get("finish_reason"),
                            "provider": d.get("provider"), "usage": u, "model": d.get("model")}
            elif r is not None:
                err = f"HTTP {r.status_code}: {r.text[:200]}"
                if r.status_code in (400, 401, 402, 404):
                    break
            self.spend.errors += 1
            await asyncio.sleep(delay); delay = min(delay * 2, 30)
        return {"content": None, "error": err}

    def summary(self) -> Dict[str, Any]:
        s = self.spend
        return {"model": self.model, "calls": s.calls, "usd": round(s.usd, 4),
                "prompt_tokens": s.prompt_tokens, "completion_tokens": s.completion_tokens, "errors": s.errors}

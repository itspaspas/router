"""Decision-record building: request features, response fields (plain or SSE), RequestTrace.

Every function here is total: malformed input yields defaults and never raises, because record
building must never fail a request.
"""
from __future__ import annotations

import asyncio
import json
import logging
import time
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Callable

from gateway.budget import BudgetGuard
from gateway.config import Prices
from gateway.decision_log import DecisionRecord, hash_user
from gateway.hooshyar import compute_cost
from gateway.language import detect_language
from policies.base import Decision

log = logging.getLogger(__name__)

_MAX_SSE_LINE = 1 << 20  # longer SSE lines are skipped rather than buffered


@dataclass(frozen=True)
class RequestFeatures:
    language: str = "unknown"
    n_messages: int = 0
    prompt_chars: int = 0
    last_user_text: str | None = None  # None when there is no user message


def _content_text(content) -> str | None:
    """String content as is; a list of parts -> its "text" parts joined by newlines."""
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        return "\n".join(
            p["text"] for p in content
            if isinstance(p, dict) and p.get("type") == "text" and isinstance(p.get("text"), str)
        )
    return None


def request_features(body: dict) -> RequestFeatures:
    messages = body.get("messages")
    if not isinstance(messages, list):
        return RequestFeatures()
    dicts = [m for m in messages if isinstance(m, dict)]
    prompt_chars = sum(len(m["content"]) for m in dicts if isinstance(m.get("content"), str))
    last_user = None
    for m in reversed(dicts):
        if m.get("role") == "user":
            last_user = _content_text(m.get("content"))
            break
    return RequestFeatures(
        language=detect_language(last_user or ""),
        n_messages=len(messages),
        prompt_chars=prompt_chars,
        last_user_text=last_user,
    )


def _tokens(value) -> int | None:
    return value if isinstance(value, int) and not isinstance(value, bool) else None


def clean_usage(usage) -> dict | None:
    """Only integer token counts survive, so cost computation cannot be fed garbage."""
    if not isinstance(usage, dict):
        return None
    return {
        "prompt_tokens": _tokens(usage.get("prompt_tokens")),
        "completion_tokens": _tokens(usage.get("completion_tokens")),
    }


def _str_or_none(value) -> str | None:
    return value if isinstance(value, str) and value else None


def _first_choice(obj: dict) -> dict:
    choices = obj.get("choices")
    if isinstance(choices, list) and choices and isinstance(choices[0], dict):
        return choices[0]
    return {}


def response_fields(resp) -> tuple[str | None, dict | None, str | None]:
    """(model, usage, answer text) of a non-streaming chat completion."""
    if not isinstance(resp, dict):
        return None, None, None
    message = _first_choice(resp).get("message")
    content = message.get("content") if isinstance(message, dict) else None
    return (
        _str_or_none(resp.get("model")),
        clean_usage(resp.get("usage")),
        content if isinstance(content, str) else None,
    )


class SSEScanner:
    """Reads model, usage and (optionally) answer text from SSE bytes; never alters or raises."""

    def __init__(self, keep_text: bool):
        self.model: str | None = None
        self.usage: dict | None = None
        self._parts: list[str] | None = [] if keep_text else None
        self._buf = b""
        self._skip = False  # inside an overlong line whose head was dropped

    @property
    def answer(self) -> str | None:
        return None if self._parts is None else "".join(self._parts)

    def feed(self, chunk: bytes) -> None:
        try:
            lines = (self._buf + bytes(chunk)).split(b"\n")
            self._buf = lines.pop()
            for line in lines:
                if self._skip:
                    self._skip = False
                else:
                    self._line(line)
            if len(self._buf) > _MAX_SSE_LINE:
                self._buf, self._skip = b"", True
        except Exception:
            self._buf = b""

    def flush(self) -> None:
        """Process a final line that had no trailing newline."""
        if self._buf and not self._skip:
            self._line(self._buf)
        self._buf = b""

    def _line(self, line: bytes) -> None:
        line = line.rstrip(b"\r")
        if not line.startswith(b"data:"):
            return
        payload = line[5:].strip()
        if not payload or payload == b"[DONE]":
            return
        try:
            obj = json.loads(payload)
        except (ValueError, RecursionError):
            return
        if not isinstance(obj, dict):
            return
        self.model = _str_or_none(obj.get("model")) or self.model
        if isinstance(obj.get("usage"), dict):
            self.usage = clean_usage(obj["usage"])
        if self._parts is not None:
            delta = _first_choice(obj).get("delta")
            content = delta.get("content") if isinstance(delta, dict) else None
            if isinstance(content, str):
                self._parts.append(content)


class RequestTrace:
    """What is known about one chat request; turns into exactly one DecisionRecord."""

    def __init__(self, *, log_salt: str, log_text: bool, prices: Prices, budget: BudgetGuard,
                 emit: Callable[[DecisionRecord, asyncio.Task | None], None]):
        self._salt, self._log_text, self._prices = log_salt, log_text, prices
        self._budget, self._emit = budget, emit
        self.request_id = uuid.uuid4().hex
        self.ts = datetime.now(timezone.utc).isoformat()
        self.start = time.monotonic()
        self.app_id = ""
        self.user_hash: str | None = None
        self.conversation_id: str | None = None
        self.features = RequestFeatures()
        self.decision: Decision | None = None
        self.attempts: list[str] = []
        self.served_by: str | None = None
        self.response_model: str | None = None
        self.usage: dict | None = None
        self.answer: str | None = None
        self.stream = False
        self.shadow_task: asyncio.Task | None = None
        self._finished = False

    def finish(self, status: int, error_kind: str | None = None) -> None:
        """Build the record, charge the budget, and emit (now, or when the shadow call ends)."""
        if self._finished:
            return
        self._finished = True
        try:
            d, usage = self.decision, self.usage or {}
            cost = compute_cost(self.response_model, self.usage, self._prices)
            self._budget.record(self.app_id, cost)
            last = self.features.last_user_text
            rec = DecisionRecord(
                request_id=self.request_id, ts=self.ts, app_id=self.app_id,
                user_hash=self.user_hash, conversation_id=self.conversation_id,
                language=self.features.language, n_messages=self.features.n_messages,
                prompt_chars=self.features.prompt_chars,
                policy=d.policy if d else "", target=d.target if d else "",
                probs=dict(d.probs) if d else {}, reasons=list(d.reasons) if d else [],
                attempts=list(self.attempts), served_by=self.served_by,
                response_model=self.response_model,
                prompt_tokens=usage.get("prompt_tokens"),
                completion_tokens=usage.get("completion_tokens"),
                cost=cost, cost_verified=self._prices.verified,
                latency_ms=int((time.monotonic() - self.start) * 1000),
                status=status, error_kind=error_kind, stream=self.stream,
                last_user_hash=hash_user(last, self._salt),
                text={"query": last, "answer": self.answer} if self._log_text else None,
            )
            task = self.shadow_task
            if task is None or task.done():
                self._emit(rec, task)
            else:
                task.add_done_callback(lambda t: self._emit(rec, t))
        except Exception as e:  # never let logging fail a request; type only (may hold user text)
            log.error("decision record failed: %s", type(e).__name__)

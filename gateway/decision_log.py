"""Privacy-first decision log: one JSON object per chat request, written off the request path.

No query/answer text is written unless `log_text=True`, and `error_kind` is a fixed vocabulary
(never an exception message), so the log is safe to keep as a research dataset.
"""
from __future__ import annotations

import asyncio
import dataclasses
import hashlib
import json
import logging
from dataclasses import dataclass
from pathlib import Path

logger = logging.getLogger(__name__)

ERROR_KINDS = frozenset({"timeout", "connection", "upstream_4xx", "upstream_5xx", "auth", "internal"})


def hash_user(user: str | None, salt: str) -> str | None:
    """Salted sha256 hex of a user identifier (None stays None)."""
    if user is None:
        return None
    return hashlib.sha256((salt + user).encode("utf-8")).hexdigest()


@dataclass
class DecisionRecord:
    request_id: str
    ts: str
    app_id: str
    user_hash: str | None
    conversation_id: str | None
    language: str
    n_messages: int
    prompt_chars: int
    policy: str
    target: str
    probs: dict
    reasons: list
    attempts: list
    served_by: str | None
    response_model: str | None
    prompt_tokens: int | None
    completion_tokens: int | None
    cost: float | None
    cost_verified: bool
    latency_ms: int
    status: int
    error_kind: str | None
    stream: bool
    # hash_user(last user message, salt): lets offline analysis detect regenerations.
    last_user_hash: str | None = None
    shadow_auto_judge: dict | None = None
    text: dict | None = None

    def __post_init__(self) -> None:
        if self.error_kind is not None and self.error_kind not in ERROR_KINDS:
            raise ValueError("error_kind must be None or one of the fixed vocabulary")


class DecisionLogger:
    def __init__(self, path: Path, log_text: bool) -> None:
        self.path = Path(path)
        self.log_text = log_text
        self._queue: asyncio.Queue[DecisionRecord] = asyncio.Queue()

    def emit(self, rec: DecisionRecord) -> None:
        """Non-blocking enqueue; never touches the disk."""
        self._queue.put_nowait(rec)

    def _serialize(self, rec: DecisionRecord) -> str:
        data = dataclasses.asdict(rec)  # a copy: the caller's record is never mutated
        if not self.log_text:
            data["text"] = None
        return json.dumps(data, ensure_ascii=False)

    def _append(self, line: str) -> None:
        with self.path.open("a", encoding="utf-8") as f:
            f.write(line + "\n")

    async def run(self) -> None:
        """Background writer: append one JSON line per emitted record, forever (cancel to stop)."""
        self.path.parent.mkdir(parents=True, exist_ok=True)
        while True:
            rec = await self._queue.get()
            try:
                line = self._serialize(rec)
                await asyncio.to_thread(self._append, line)
            except Exception as e:
                # Exception type only: messages and record content may carry user text.
                logger.error("decision log write failed: %s", type(e).__name__)
            finally:
                self._queue.task_done()

    async def close(self) -> None:
        """Wait until everything already emitted has been written. Requires `run()` to be active."""
        await self._queue.join()

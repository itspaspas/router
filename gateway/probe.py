"""Discovery and smoke probes against Hooshyar (run by the repository owner with their token).

discover() answers the spec section 7 open items: which models exist, whether logprobs are returned,
and what auto-judge outputs. smoke() checks that every target answers at all. Neither raises on an
upstream failure: errors are recorded as UpstreamError.kind. Neither ever prints the token or the
Authorization header (the client keeps them private and nothing here reads them).
"""
from __future__ import annotations

import asyncio
import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

from gateway.config import RouterConfig, load_config, load_settings
from gateway.hooshyar import HooshyarClient, UpstreamError

PROBE_PROMPTS: list[str] = [
    "Write a short poem about rain.",
    "یک شعر کوتاه درباره باران بنویس.",
    "Solve: 17 * 23 = ?",
    "این تابع Python را توضیح بده: def f(x): return x[::-1]",
    "خلاصه‌ای سه‌جمله‌ای از مزایای انرژی خورشیدی بنویس.",
]

TIERS = ("small", "medium", "frontier")
_RAW_MAX_CHARS = 200
REPORT_DIR = Path("discovery")


def _configured_tiers(cfg: RouterConfig) -> list[tuple[str, str]]:
    return [(t, m) for t in TIERS if (m := cfg.model_for(t))]


def _user(prompt: str) -> list[dict]:
    return [{"role": "user", "content": prompt}]


async def _probe_logprobs(client: HooshyarClient, model: str) -> bool | None:
    body = {
        "model": model,
        "stream": False,
        "logprobs": True,
        "max_tokens": 5,
        "messages": _user(PROBE_PROMPTS[0]),
    }
    try:
        resp = await client.chat(body)
        return resp["choices"][0].get("logprobs") is not None
    except Exception:
        return None


async def _judge(client: HooshyarClient, idx: int, prompt: str) -> dict:
    body = {"model": "auto-judge", "stream": False, "messages": _user(prompt)}
    start = time.monotonic()
    raw: str | None = None
    usage: dict | None = None
    try:
        resp = await client.chat(body)
        content = resp["choices"][0]["message"]["content"]
        raw = content[:_RAW_MAX_CHARS] if isinstance(content, str) else None
        u = resp.get("usage")
        usage = u if isinstance(u, dict) else None
    except Exception:
        raw, usage = None, None
    return {
        "prompt_idx": idx,
        "raw": raw,
        "latency_ms": int((time.monotonic() - start) * 1000),
        "usage": usage,
    }


async def discover(client: HooshyarClient, cfg: RouterConfig) -> dict:
    try:
        models: dict = await client.list_models()
    except UpstreamError as e:
        models = {"error": e.kind}
    except Exception:
        models = {"error": "unexpected"}

    logprobs: dict[str, bool | None] = {"auto": await _probe_logprobs(client, "auto")}
    for tier, model in _configured_tiers(cfg):
        logprobs[tier] = await _probe_logprobs(client, model)

    auto_judge = [await _judge(client, i, p) for i, p in enumerate(PROBE_PROMPTS)]
    return {
        "models": models,
        "logprobs": logprobs,
        "auto_judge": auto_judge,
        "ts": datetime.now(timezone.utc).isoformat(),
    }


async def smoke(client: HooshyarClient, cfg: RouterConfig) -> list[tuple[str, str]]:
    targets = [("auto", "auto"), ("auto-judge", "auto-judge")]
    targets += [(tier, model) for tier, model in _configured_tiers(cfg)]
    rows: list[tuple[str, str]] = []
    for name, model in targets:
        body = {
            "model": model,
            "stream": False,
            "max_tokens": 16,
            "messages": _user(PROBE_PROMPTS[0]),
        }
        try:
            await client.chat(body)
            rows.append((name, "ok"))
        except UpstreamError as e:
            rows.append((name, e.kind))
        except Exception:
            rows.append((name, "unexpected"))
    return rows


def _table(rows: list[tuple[str, str]], headers: tuple[str, str]) -> str:
    width = max([len(headers[0])] + [len(a) for a, _ in rows])
    lines = [f"{headers[0]:<{width}}  {headers[1]}", f"{'-' * width}  {'-' * len(headers[1])}"]
    lines += [f"{a:<{width}}  {b}" for a, b in rows]
    return "\n".join(lines)


def _setup() -> tuple[HooshyarClient, RouterConfig]:
    try:
        settings = load_settings()
    except ValueError as e:  # names the missing variable, never a value
        print(f"error: {e}", file=sys.stderr)
        raise SystemExit(2) from None
    cfg = load_config(settings.config_path)
    return HooshyarClient(settings.base_url, settings.token, cfg.timeout_s), cfg


async def _run_smoke() -> list[tuple[str, str]]:
    client, cfg = _setup()
    try:
        return await smoke(client, cfg)
    finally:
        await client.aclose()


async def _run_discover() -> dict:
    client, cfg = _setup()
    try:
        return await discover(client, cfg)
    finally:
        await client.aclose()


def smoke_main() -> None:
    rows = asyncio.run(_run_smoke())
    print(_table(rows, ("target", "status")))
    if any(status != "ok" for _, status in rows):
        raise SystemExit(1)


def discover_main() -> None:
    report = asyncio.run(_run_discover())
    now = datetime.now(timezone.utc)
    REPORT_DIR.mkdir(exist_ok=True)
    path = REPORT_DIR / f"report-{now:%Y-%m-%d}.json"
    path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    models = report["models"]
    if "error" in models:
        print(f"models: error ({models['error']})")
    else:
        ids = [m.get("id") for m in models.get("data", []) if isinstance(m, dict)]
        print(f"models ({len(ids)}): " + ", ".join(str(i) for i in ids))
    print()
    lp = {True: "yes", False: "no", None: "error"}
    print(_table([(k, lp[v]) for k, v in report["logprobs"].items()], ("target", "logprobs")))
    print()
    judge = [(str(j["prompt_idx"]), f"{j['latency_ms']}ms  {j['raw']!r}") for j in report["auto_judge"]]
    print(_table(judge, ("prompt", "auto-judge output")))
    print(f"\nreport written to {path}")

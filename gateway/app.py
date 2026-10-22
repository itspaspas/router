"""FastAPI gateway: OpenAI-compatible chat endpoint in front of Hooshyar.

Flow per chat request: auth -> parse -> features -> policy -> budget guard -> execute (tier
fallback) -> respond -> one DecisionRecord, emitted after the response (and any shadow call) ends.
Router failures degrade to Hooshyar `auto`; only upstream failures fail a request.
"""
from __future__ import annotations

import asyncio
import contextlib
import dataclasses
import json
import logging
import random
from typing import Awaitable, Callable

import anyio
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, StreamingResponse

from gateway.budget import BudgetGuard
from gateway.config import RouterConfig, Settings, load_config, load_settings
from gateway.decision_log import DecisionLogger, DecisionRecord, hash_user
from gateway.executor import ExecResult, execute
from gateway.hooshyar import HooshyarClient, UpstreamError
from gateway.records import RequestTrace, SSEScanner, request_features, response_fields
from gateway.shadow import shadow_auto_judge
from policies.auto_passthrough import AutoPassthrough
from policies.base import Decision, RouteRequest, RoutingPolicy

log = logging.getLogger(__name__)

SHUTDOWN_GRACE_S = 2.0
MODEL_IDS = ("auto", "small", "medium", "frontier")


def _error(message: str, kind: str) -> dict:
    return {"error": {"message": message, "type": kind}}


def _header(value) -> str:
    """Printable ASCII only: header values must be latin-1 and must not carry CR/LF."""
    return "".join(c if " " <= c <= "~" else "?" for c in str(value))


class _Finalizing:
    """Response mixin: runs `on_close` once the response is over, however it ended."""

    on_close: Callable[[], Awaitable[None]] | None = None

    async def __call__(self, scope, receive, send) -> None:
        try:
            await super().__call__(scope, receive, send)
        finally:
            if self.on_close is not None:
                with anyio.CancelScope(shield=True):
                    await self.on_close()


class _JSON(_Finalizing, JSONResponse):
    pass


class _Stream(_Finalizing, StreamingResponse):
    pass


def _closer(trace: RequestTrace, status: int, error_kind: str | None):
    async def on_close() -> None:
        trace.finish(status, error_kind)

    return on_close


def _error_response(trace: RequestTrace, status: int, message: str, kind: str,
                    error_kind: str | None, headers: dict | None = None) -> _JSON:
    resp = _JSON(_error(message, kind), status_code=status, headers=headers)
    resp.on_close = _closer(trace, status, error_kind)
    return resp


class _Gateway:
    def __init__(self, settings: Settings, cfg: RouterConfig, policy: RoutingPolicy,
                 client: HooshyarClient | None):
        self.settings = settings
        self.cfg = cfg
        self.policy = policy
        self.client = client
        self.owns_client = client is None
        self.budget = BudgetGuard(cfg)
        self.logger = DecisionLogger(settings.log_path, settings.log_text)
        self.tasks: set[asyncio.Task] = set()
        self.known_models = {m for m in cfg.tiers.values() if m}
        # R7: an over-cap app's auto request goes to small, and its chain never reaches frontier
        # (also when a router failure re-serves it via auto).
        self.capped_cfg = dataclasses.replace(cfg, fallback={
            **cfg.fallback,
            **{t: [x for x in cfg.fallback.get(t, []) if x != "frontier"] for t in ("small", "auto")},
        })

    # --- background work ---------------------------------------------------------------------

    def spawn(self, coro) -> asyncio.Task:
        task = asyncio.create_task(coro)
        self.tasks.add(task)  # strong reference until done
        task.add_done_callback(self.tasks.discard)
        return task

    def new_trace(self) -> RequestTrace:
        return RequestTrace(log_salt=self.settings.log_salt, log_text=self.settings.log_text,
                            prices=self.cfg.prices, budget=self.budget, emit=self.emit)

    def emit(self, rec: DecisionRecord, shadow: asyncio.Task | None) -> None:
        if shadow is not None and not shadow.cancelled() and shadow.exception() is None:
            rec.shadow_auto_judge = shadow.result()
        self.logger.emit(rec)

    async def drain(self) -> None:
        """Wait for all background work, then for every emitted record to be written."""
        while self.tasks:
            await asyncio.gather(*list(self.tasks), return_exceptions=True)
            await asyncio.sleep(0)  # let done-callbacks emit their records
        await self.logger.close()

    async def shutdown(self) -> None:
        if self.tasks:
            _, pending = await asyncio.wait(set(self.tasks), timeout=SHUTDOWN_GRACE_S)
            for task in pending:
                task.cancel()
            await asyncio.gather(*pending, return_exceptions=True)
            await asyncio.sleep(0)
        await self.logger.close()

    # --- chat --------------------------------------------------------------------------------

    def _app_id(self, header: str | None) -> str | None:
        scheme, _, key = (header or "").partition(" ")
        if scheme.lower() != "bearer" or not key.strip():
            return None
        return self.settings.app_keys.get(key.strip())

    def _start_shadow(self, trace: RequestTrace, body: dict) -> None:
        try:
            messages = body.get("messages")
            if (self.cfg.shadow_enabled and isinstance(messages, list)
                    and random.random() < self.cfg.shadow_sample_rate):
                trace.shadow_task = self.spawn(
                    shadow_auto_judge(self.client, messages, self.known_models))
        except Exception as e:
            log.error("shadow start failed: %s", type(e).__name__)

    def _route(self, body: dict, trace: RequestTrace) -> RouterConfig:
        req = RouteRequest(body, trace.app_id, trace.conversation_id, trace.features.language)
        try:
            d = self.policy.decide(req)
            if not (isinstance(d, Decision) and isinstance(d.target, str) and d.target
                    and isinstance(d.policy, str)):
                raise TypeError("policy returned no usable decision")
        except Exception:
            d = AutoPassthrough().decide(req)
            d = dataclasses.replace(d, reasons=(*d.reasons, "policy_error"))
        trace.decision = d
        if d.target == "auto" and self.budget.over_cap(trace.app_id):
            if self.cfg.model_for("small") is None:  # R8: cannot downgrade; never fail for it
                trace.decision = dataclasses.replace(
                    d, reasons=(*d.reasons, "budget_cap_unenforceable"))
                return self.capped_cfg  # still auto; its fallback chain skips frontier
            trace.decision = dataclasses.replace(d, target="small",
                                                 reasons=(*d.reasons, "budget_cap"))
            return self.capped_cfg
        return self.cfg

    async def _execute(self, body: dict, trace: RequestTrace) -> ExecResult:
        cfg = self.cfg
        try:
            cfg = self._route(body, trace)
            return await execute(trace.decision, body, self.client, cfg, trace.stream)
        except UpstreamError:
            raise
        except Exception as e:  # router failure: serve via Hooshyar auto
            log.error("router failure, serving via auto: %s", type(e).__name__)
            reasons = trace.decision.reasons if trace.decision else ()
            trace.decision = Decision("auto", AutoPassthrough.name, {"auto": 1.0},
                                      (*reasons, "internal_error"))
            return await execute(trace.decision, body, self.client, cfg, trace.stream)

    async def chat(self, request: Request, trace: RequestTrace):
        headers = request.headers
        trace.conversation_id = headers.get("x-conversation-id")
        try:
            trace.user_hash = hash_user(headers.get("x-user-id"), self.settings.log_salt)
        except Exception as e:  # a logging feature must never fail the request
            log.error("user hash failed: %s", type(e).__name__)
        app_id = self._app_id(headers.get("authorization"))
        if app_id is None:
            return _error_response(trace, 401, "invalid or missing API key",
                                   "authentication_error", "auth")
        trace.app_id = app_id
        try:
            body = json.loads(await request.body())
        except (ValueError, RecursionError):
            body = None
        if not isinstance(body, dict):
            return _error_response(trace, 400, "request body must be a JSON object",
                                   "invalid_request_error", None)
        try:
            trace.features = request_features(body)
        except Exception as e:  # keep neutral features and serve anyway
            log.error("feature extraction failed: %s", type(e).__name__)
        trace.stream = body.get("stream") is True
        self._start_shadow(trace, body)
        try:
            result = await self._execute(body, trace)
        except UpstreamError as e:
            trace.attempts = list(e.attempts)
            status = e.status if isinstance(e.status, int) and 400 <= e.status <= 599 else 502
            return _error_response(trace, status, "upstream request failed", e.kind, e.kind,
                                   {"X-Router-Policy": _header(trace.decision.policy)})
        try:
            trace.attempts, trace.served_by = result.attempts, result.served_by
            out_headers = {"X-Router-Policy": _header(trace.decision.policy),
                           "X-Router-Served-By": _header(result.served_by)}
            if result.stream is None:
                trace.response_model, trace.usage, trace.answer = response_fields(result.response)
                resp = _JSON(result.response, headers=out_headers)
                resp.on_close = _closer(trace, 200, None)
                return resp
            return self._stream_response(result, trace, out_headers)
        except BaseException:
            if result.stream is not None:  # never leak an open upstream stream
                await result.stream.aclose()
            raise

    def _stream_response(self, result: ExecResult, trace: RequestTrace, headers: dict) -> _Stream:
        upstream = result.stream
        scanner = SSEScanner(keep_text=self.settings.log_text)
        error_kind: list[str] = []

        async def relay():
            try:
                async for chunk in upstream:
                    scanner.feed(chunk)
                    yield chunk
            except UpstreamError as e:  # mid-stream: headers are sent, so the status stays 200
                error_kind.append(e.kind)
                raise
            except Exception:
                error_kind.append("internal")
                raise

        body = relay()

        async def on_close() -> None:
            try:
                await body.aclose()
            finally:
                try:
                    await upstream.aclose()
                finally:
                    scanner.flush()
                    trace.response_model, trace.usage = scanner.model, scanner.usage
                    trace.answer = scanner.answer
                    trace.finish(200, error_kind[0] if error_kind else None)

        resp = _Stream(body, media_type="text/event-stream", headers=headers)
        resp.on_close = on_close
        return resp


def create_app(
    settings: Settings,
    cfg: RouterConfig,
    policy: RoutingPolicy | None = None,
    client: HooshyarClient | None = None,
) -> FastAPI:
    gw = _Gateway(settings, cfg, policy or AutoPassthrough(), client)

    @contextlib.asynccontextmanager
    async def lifespan(app: FastAPI):
        if gw.client is None:
            gw.client = HooshyarClient(settings.base_url, settings.token, cfg.timeout_s)
        writer = asyncio.create_task(gw.logger.run())
        try:
            yield
        finally:
            try:
                await gw.shutdown()
            finally:
                writer.cancel()
                with contextlib.suppress(asyncio.CancelledError):
                    await writer
                if gw.owns_client:
                    await gw.client.aclose()
                    gw.client = None

    app = FastAPI(title="Persian router gateway", lifespan=lifespan)
    app.state.gateway = gw

    @app.post("/v1/chat/completions")
    async def chat_completions(request: Request):
        trace = gw.new_trace()
        try:
            return await gw.chat(request, trace)
        except Exception as e:
            log.error("chat request failed: %s", type(e).__name__)
            return _error_response(trace, 500, "internal error", "internal", "internal")

    @app.get("/v1/models")
    async def list_models():
        data = [{"id": m, "object": "model", "created": 0, "owned_by": "router"} for m in MODEL_IDS]
        return {"object": "list", "data": data}

    @app.get("/healthz")
    async def healthz():
        return {"ok": True}

    return app


def create_app_from_env() -> FastAPI:
    """Factory for `uvicorn --factory gateway.app:create_app_from_env`. Reads settings from the
    environment at call time (never at import), so importing this module needs no env vars."""
    settings = load_settings()
    return create_app(settings, load_config(settings.config_path))

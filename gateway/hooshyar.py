"""Async client for the Hooshyar OpenAI-compatible API, and cost computation."""
from __future__ import annotations

from typing import AsyncIterator

import httpx

from gateway.config import Prices


class UpstreamError(Exception):
    """Upstream failure. Carries only classification data, never body or request content.

    kind is one of "timeout", "connection", "upstream_4xx", "upstream_5xx".
    """

    def __init__(self, kind: str, status: int | None = None):
        self.kind = kind
        self.status = status
        self.retryable = kind in ("timeout", "connection") or (status is not None and status >= 500)
        super().__init__(f"upstream {kind}" + (f" (status {status})" if status is not None else ""))


def _status_error(status: int) -> UpstreamError:
    return UpstreamError("upstream_5xx" if status >= 500 else "upstream_4xx", status)


def _transport_error(exc: httpx.HTTPError) -> UpstreamError:
    kind = "timeout" if isinstance(exc, httpx.TimeoutException) else "connection"
    return UpstreamError(kind)


class HooshyarClient:
    def __init__(
        self,
        base_url: str,
        token: str,
        timeout_s: float,
        http: httpx.AsyncClient | None = None,
    ):
        self._base_url = base_url.rstrip("/")
        self._headers = {"Authorization": f"Bearer {token}"}
        self._http = http if http is not None else httpx.AsyncClient(timeout=timeout_s)
        self._owns_http = http is None

    async def aclose(self) -> None:
        if self._owns_http:
            await self._http.aclose()

    async def _json(self, method: str, path: str, body: dict | None = None) -> dict:
        try:
            resp = await self._http.request(
                method, f"{self._base_url}{path}", json=body, headers=self._headers
            )
        except httpx.HTTPError as e:
            raise _transport_error(e) from None
        if resp.status_code != 200:
            raise _status_error(resp.status_code)
        try:
            return resp.json()
        except ValueError:
            # 200 with an unparseable body: upstream fault, not worth retrying blindly.
            err = UpstreamError("upstream_5xx", resp.status_code)
            err.retryable = False
            raise err from None

    async def chat(self, body: dict) -> dict:
        return await self._json("POST", "/chat/completions", body)

    async def list_models(self) -> dict:
        return await self._json("GET", "/models")

    async def open_stream(self, body: dict) -> AsyncIterator[bytes]:
        """Yield raw SSE bytes. Raises UpstreamError before yielding if status != 200."""
        try:
            async with self._http.stream(
                "POST", f"{self._base_url}/chat/completions", json=body, headers=self._headers
            ) as resp:
                if resp.status_code != 200:
                    raise _status_error(resp.status_code)
                async for chunk in resp.aiter_raw():
                    yield chunk
        except httpx.HTTPError as e:
            raise _transport_error(e) from None


def compute_cost(model: str | None, usage: dict | None, prices: Prices) -> float | None:
    """USD cost from usage token counts, or None if the model is unpriced or usage is missing."""
    if not model or not usage or model not in prices.models:
        return None
    price_in, price_out = prices.models[model]
    prompt = usage.get("prompt_tokens") or 0
    completion = usage.get("completion_tokens") or 0
    return (prompt * price_in + completion * price_out) / 1_000_000

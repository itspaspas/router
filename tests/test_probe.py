import json
import subprocess
import sys

import httpx
import pytest

from gateway.probe import PROBE_PROMPTS, discover, discover_main, smoke, smoke_main
from tests.conftest import MODELS, UP, ok_text, route_by_model

ENV = {
    "HOOSHYAR_TOKEN": "SECRET-T",
    "HOOSHYAR_BASE_URL": "https://h.test/v1",
    "ROUTER_APP_KEYS": "{}",
    "ROUTER_LOG_SALT": "s",
}


def _no_logprobs(req):
    return httpx.Response(200, json={"choices": [{"logprobs": None, "message": {"content": "x"}}]})


def test_probe_prompts():
    assert len(PROBE_PROMPTS) == 5
    assert PROBE_PROMPTS[0] == "Write a short poem about rain."
    assert PROBE_PROMPTS[4] == "خلاصه‌ای سه‌جمله‌ای از مزایای انرژی خورشیدی بنویس."


async def test_discover_shape_and_logprobs(respx_mock, cfg_tiers, client):
    respx_mock.get(MODELS).respond(200, json={"data": [{"id": "s1"}]})
    respx_mock.post(UP).mock(
        side_effect=route_by_model({"auto-judge": ok_text("s1")}, default=_no_logprobs)
    )
    rep = await discover(client, cfg_tiers)
    assert rep["models"]["data"][0]["id"] == "s1"
    assert rep["logprobs"] == {"auto": False, "small": False, "medium": False, "frontier": False}
    assert len(rep["auto_judge"]) == 5 and rep["auto_judge"][0]["raw"] == "s1"
    assert [e["prompt_idx"] for e in rep["auto_judge"]] == [0, 1, 2, 3, 4]
    assert rep["auto_judge"][0]["usage"] is None and isinstance(rep["auto_judge"][0]["latency_ms"], int)
    assert rep["ts"]


async def test_discover_logprobs_true_and_request_body(respx_mock, cfg_tiers, client):
    respx_mock.get(MODELS).respond(200, json={"data": []})
    seen = []

    def handler(req):
        seen.append(json.loads(req.content))
        lp = {"content": []} if json.loads(req.content)["model"] == "m1" else None
        return httpx.Response(200, json={"choices": [{"logprobs": lp, "message": {"content": "x"}}]})

    respx_mock.post(UP).mock(side_effect=handler)
    rep = await discover(client, cfg_tiers)
    assert rep["logprobs"]["medium"] is True and rep["logprobs"]["small"] is False
    probe = next(b for b in seen if b["model"] == "m1")
    assert probe["logprobs"] is True and probe["max_tokens"] == 5


async def test_discover_errors_are_recorded_not_raised(respx_mock, cfg_tiers, client):
    respx_mock.get(MODELS).respond(500)
    respx_mock.post(UP).respond(503)
    rep = await discover(client, cfg_tiers)
    assert rep["models"] == {"error": "upstream_5xx"}
    assert set(rep["logprobs"].values()) == {None}
    assert len(rep["auto_judge"]) == 5
    assert rep["auto_judge"][0]["raw"] is None and rep["auto_judge"][0]["usage"] is None


async def test_discover_skips_unconfigured_tiers(respx_mock, cfg_no_medium, client):
    respx_mock.get(MODELS).respond(200, json={"data": []})
    respx_mock.post(UP).mock(side_effect=_no_logprobs)
    rep = await discover(client, cfg_no_medium)
    assert set(rep["logprobs"]) == {"auto", "small", "frontier"}


async def test_smoke_reports_errors_without_raising(respx_mock, cfg_tiers, client):
    respx_mock.post(UP).respond(503)
    rows = await smoke(client, cfg_tiers)
    assert rows[0] == ("auto", "upstream_5xx") and len(rows) == 5
    assert [r[0] for r in rows] == ["auto", "auto-judge", "small", "medium", "frontier"]


async def test_smoke_ok_rows_and_body(respx_mock, cfg_tiers, client):
    seen = []

    def handler(req):
        seen.append(json.loads(req.content))
        return httpx.Response(200, json={"choices": [{"message": {"content": "x"}}]})

    respx_mock.post(UP).mock(side_effect=handler)
    rows = await smoke(client, cfg_tiers)
    assert all(status == "ok" for _, status in rows)
    assert seen[0]["max_tokens"] == 16 and seen[0]["messages"][0]["content"] == PROBE_PROMPTS[0]


def test_smoke_main_never_prints_token(capsys, monkeypatch, respx_mock):
    for k, v in ENV.items():
        monkeypatch.setenv(k, v)
    respx_mock.post(UP).respond(200, json={"choices": [{"message": {"content": "x"}}]})
    smoke_main()
    out = capsys.readouterr()
    assert "SECRET-T" not in out.out + out.err
    assert "auto-judge" in out.out


def test_discover_main_writes_report_without_token(capsys, monkeypatch, respx_mock, tmp_path):
    for k, v in ENV.items():
        monkeypatch.setenv(k, v)
    monkeypatch.chdir(tmp_path)
    cfg = tmp_path / "router.yaml"
    prices = tmp_path / "prices.yaml"
    prices.write_text("verified: false\nmodels: {}\n", encoding="utf-8")
    cfg.write_text(
        f"tiers: {{small: s1, medium: '', frontier: ''}}\nprices_file: {prices}\n", encoding="utf-8"
    )
    monkeypatch.setenv("ROUTER_CONFIG", str(cfg))
    respx_mock.get(MODELS).respond(200, json={"data": [{"id": "s1"}]})
    respx_mock.post(UP).mock(side_effect=route_by_model({"auto-judge": ok_text("سلام")}, _no_logprobs))
    discover_main()
    out = capsys.readouterr()
    assert "SECRET-T" not in out.out + out.err
    reports = list((tmp_path / "discovery").glob("report-*.json"))
    assert len(reports) == 1
    text = reports[0].read_text(encoding="utf-8")
    assert "SECRET-T" not in text and "Bearer" not in text
    assert "سلام" in text  # ensure_ascii=False
    assert json.loads(text)["logprobs"]["small"] is False


def test_import_app_needs_no_env():
    code = (
        "import os\n"
        "for k in list(os.environ):\n"
        "    if k.startswith(('HOOSHYAR_', 'ROUTER_')): del os.environ[k]\n"
        "import gateway.app\n"
        "assert not hasattr(gateway.app, 'app')\n"
    )
    r = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True)
    assert r.returncode == 0, r.stderr


def test_create_app_from_env_requires_token(monkeypatch):
    from gateway.app import create_app_from_env

    for k in ("HOOSHYAR_TOKEN", "ROUTER_APP_KEYS", "ROUTER_LOG_SALT"):
        monkeypatch.delenv(k, raising=False)
    with pytest.raises(ValueError, match="HOOSHYAR_TOKEN"):
        create_app_from_env()


def test_create_app_from_env_builds_app(monkeypatch):
    from fastapi import FastAPI

    from gateway.app import create_app_from_env

    for k, v in ENV.items():
        monkeypatch.setenv(k, v)
    assert isinstance(create_app_from_env(), FastAPI)

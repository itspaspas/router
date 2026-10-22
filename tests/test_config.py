from pathlib import Path

import pytest

from gateway.config import load_config, load_settings


def test_settings_defaults_and_required(tmp_path):
    env = {"HOOSHYAR_TOKEN": "t", "ROUTER_APP_KEYS": '{"k1": "chat"}', "ROUTER_LOG_SALT": "s"}
    s = load_settings(env)
    assert s.base_url == "https://hooshyar.golrang.ai/api/v1"
    assert s.app_keys == {"k1": "chat"}
    assert s.log_text is False
    assert s.log_path == Path("logs/decisions.jsonl")
    assert s.config_path == Path("config/router.yaml")


@pytest.mark.parametrize("missing", ["HOOSHYAR_TOKEN", "ROUTER_APP_KEYS", "ROUTER_LOG_SALT"])
def test_settings_missing_secret_raises(missing):
    env = {"HOOSHYAR_TOKEN": "t", "ROUTER_APP_KEYS": "{}", "ROUTER_LOG_SALT": "s"}
    del env[missing]
    with pytest.raises(ValueError, match=missing):
        load_settings(env)


def test_example_config_loads_with_unconfigured_tiers():
    cfg = load_config(Path("config/router.yaml"))
    assert set(cfg.tiers) == {"small", "medium", "frontier"}
    assert cfg.model_for("small") is None          # "" means unconfigured
    assert cfg.fallback["auto"] == ["medium", "frontier"]
    assert cfg.fallback["small"] == ["medium", "frontier"]
    assert cfg.fallback["frontier"] == []
    assert cfg.timeout_s == 120
    assert cfg.prices.verified is False


def test_settings_repr_hides_secrets():
    env = {"HOOSHYAR_TOKEN": "TOK-SECRET", "ROUTER_APP_KEYS": '{"KEY-SECRET": "chat"}',
           "ROUTER_LOG_SALT": "SALT-SECRET"}
    text = repr(load_settings(env))
    assert "TOK-SECRET" not in text and "KEY-SECRET" not in text and "SALT-SECRET" not in text

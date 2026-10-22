import asyncio
import json
import logging

import pytest

from gateway.decision_log import DecisionLogger, hash_user
from tests.conftest import make_record


async def test_no_text_written_when_disabled(tmp_path):
    log = DecisionLogger(tmp_path / "d.jsonl", log_text=False)
    task = asyncio.create_task(log.run())
    rec = make_record(text={"query": "رمز عبور من 1234 است", "answer": "SECRET-ANSWER"}, error_kind="upstream_4xx")
    log.emit(rec)
    await log.close(); task.cancel()
    raw = (tmp_path / "d.jsonl").read_text(encoding="utf-8")
    assert "1234" not in raw and "SECRET-ANSWER" not in raw and "رمز" not in raw
    assert json.loads(raw.splitlines()[0])["text"] is None
    # the caller's record is never mutated
    assert rec.text == {"query": "رمز عبور من 1234 است", "answer": "SECRET-ANSWER"}


async def test_text_written_when_enabled(tmp_path):
    log = DecisionLogger(tmp_path / "d.jsonl", log_text=True)
    task = asyncio.create_task(log.run())
    log.emit(make_record(text={"query": "سلام", "answer": "hi"}))
    await log.close(); task.cancel()
    assert json.loads((tmp_path / "d.jsonl").read_text(encoding="utf-8"))["text"]["query"] == "سلام"


async def test_creates_parent_dir_and_appends_lines(tmp_path):
    path = tmp_path / "nested" / "dir" / "d.jsonl"
    log = DecisionLogger(path, log_text=False)
    task = asyncio.create_task(log.run())
    for i in range(3):
        log.emit(make_record(request_id=f"r{i}"))
    await log.close(); task.cancel()
    ids = [json.loads(line)["request_id"] for line in path.read_text(encoding="utf-8").splitlines()]
    assert ids == ["r0", "r1", "r2"]


async def test_writer_survives_unserializable_record(tmp_path, caplog):
    # json.dumps's TypeError message embeds the offending type's name, so str(e) would leak it.
    leaky = type("SENTINEL-LEAK", (), {})
    log = DecisionLogger(tmp_path / "d.jsonl", log_text=False)
    task = asyncio.create_task(log.run())
    with caplog.at_level(logging.ERROR):
        log.emit(make_record(request_id="bad", probs={"x": leaky()}))
        log.emit(make_record(request_id="good"))
        await log.close()
    task.cancel()
    raw = (tmp_path / "d.jsonl").read_text(encoding="utf-8")
    assert [json.loads(line)["request_id"] for line in raw.splitlines()] == ["good"]
    assert "TypeError" in caplog.text
    assert "SENTINEL-LEAK" not in caplog.text and "SENTINEL-LEAK" not in raw


async def test_writer_survives_unwritable_path_and_close_returns(tmp_path, caplog):
    blocker = tmp_path / "afile"
    blocker.write_text("x")  # parent of the log path is a regular file: mkdir/open must fail
    log = DecisionLogger(blocker / "d.jsonl", log_text=False)
    task = asyncio.create_task(log.run())
    with caplog.at_level(logging.ERROR):
        log.emit(make_record(request_id="a"))
        log.emit(make_record(request_id="b"))
        await asyncio.wait_for(log.close(), 1)
    assert not task.done()  # the writer loop is still alive
    assert caplog.text.count("decision log write failed") == 2
    assert "afile" not in caplog.text and "Errno" not in caplog.text
    task.cancel()


async def test_close_returns_when_run_never_started(tmp_path):
    log = DecisionLogger(tmp_path / "d.jsonl", log_text=False)
    log.emit(make_record())
    await asyncio.wait_for(log.close(), 1)


async def test_close_returns_after_writer_cancelled(tmp_path):
    log = DecisionLogger(tmp_path / "d.jsonl", log_text=False)
    task = asyncio.create_task(log.run())
    await asyncio.sleep(0)
    task.cancel()
    await asyncio.gather(task, return_exceptions=True)
    log.emit(make_record())
    await asyncio.wait_for(log.close(), 1)


async def test_error_kind_revalidated_at_serialization(tmp_path):
    log = DecisionLogger(tmp_path / "d.jsonl", log_text=False)
    task = asyncio.create_task(log.run())
    rec = make_record()
    rec.error_kind = "Traceback: user text"  # set after construction, bypassing __post_init__
    log.emit(rec)
    await log.close(); task.cancel()
    raw = (tmp_path / "d.jsonl").read_text(encoding="utf-8")
    assert json.loads(raw)["error_kind"] == "internal"
    assert "Traceback" not in raw


def test_hash_user_stable_and_salted():
    assert hash_user("ali", "s1") == hash_user("ali", "s1") != hash_user("ali", "s2")
    assert hash_user(None, "s1") is None


def test_error_kind_vocabulary_enforced():
    with pytest.raises(ValueError):
        make_record(error_kind="Traceback: something with user text")
    for kind in (None, "timeout", "connection", "upstream_4xx", "upstream_5xx", "auth", "internal"):
        assert make_record(error_kind=kind).error_kind == kind

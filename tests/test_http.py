"""Retry behaviour of src.http, against a scripted server."""

import httpx
import pytest

from src import http as http_module
from src.http import FetchError, MAX_RETRIES, RETRY_AFTER_CAP, get_json, get_text


class Script:
    """Answers each request from a list, and records the waits asked of us."""

    def __init__(self, monkeypatch, *responses):
        self.responses = list(responses)
        self.calls = 0
        self.slept = []
        monkeypatch.setattr(http_module.time, "sleep", self.slept.append)
        self.client = httpx.Client(transport=httpx.MockTransport(self.handle))

    def handle(self, request):
        self.calls += 1
        item = self.responses[min(self.calls, len(self.responses)) - 1]
        return item(request) if callable(item) else item


def ok(payload=None):
    return httpx.Response(200, json=payload or {"ok": True})


def test_a_server_error_is_retried_and_then_succeeds(monkeypatch):
    s = Script(monkeypatch, httpx.Response(500), ok())

    assert get_json(s.client, "https://x/") == {"ok": True}
    assert s.calls == 2


def test_a_404_is_none_for_json_and_never_retried(monkeypatch):
    s = Script(monkeypatch, httpx.Response(404))

    assert get_json(s.client, "https://x/") is None
    assert s.calls == 1


@pytest.mark.parametrize("status", [400, 401, 403, 404, 410])
def test_a_client_error_is_not_retried(monkeypatch, status):
    s = Script(monkeypatch, httpx.Response(status))

    with pytest.raises(FetchError) as raised:
        get_text(s.client, "https://x/")
    assert s.calls == 1
    assert raised.value.permanent and raised.value.status == status
    assert s.slept == []


def test_giving_up_after_the_last_attempt_says_so(monkeypatch):
    s = Script(monkeypatch, httpx.Response(500))

    with pytest.raises(FetchError, match="giving up") as raised:
        get_json(s.client, "https://x/")
    assert s.calls == MAX_RETRIES
    assert not raised.value.permanent and raised.value.status == 500


def test_a_body_that_is_not_json_is_retried(monkeypatch):
    s = Script(monkeypatch, httpx.Response(200, text="<html>"), ok())

    assert get_json(s.client, "https://x/") == {"ok": True}
    assert s.calls == 2


@pytest.mark.parametrize("status", [429, 503])
def test_retry_after_is_honoured(monkeypatch, status):
    s = Script(monkeypatch, httpx.Response(status, headers={"retry-after": "7"}), ok())

    get_json(s.client, "https://x/")
    assert s.slept == [7.0]


def test_a_retry_after_beyond_the_cap_gives_up_at_once(monkeypatch):
    s = Script(
        monkeypatch,
        httpx.Response(429, headers={"retry-after": str(RETRY_AFTER_CAP + 1)}),
    )

    with pytest.raises(FetchError, match="asked to wait"):
        get_json(s.client, "https://x/")
    assert s.calls == 1 and s.slept == []


def test_an_unreadable_retry_after_falls_back_to_the_backoff(monkeypatch):
    s = Script(
        monkeypatch,
        httpx.Response(429, headers={"retry-after": "Wed, 21 Oct 2026 07:28:00 GMT"}),
        ok(),
    )

    get_json(s.client, "https://x/")
    assert len(s.slept) == 1 and 1.0 <= s.slept[0] <= 3.0


def test_backoff_doubles_and_carries_jitter(monkeypatch):
    s = Script(monkeypatch, httpx.Response(500))

    with pytest.raises(FetchError):
        get_json(s.client, "https://x/")
    assert len(s.slept) == MAX_RETRIES - 1
    for attempt, wait in enumerate(s.slept):
        base = 2.0 * 2**attempt
        assert 0.5 * base <= wait <= 1.5 * base


def test_a_network_error_is_a_fetch_error(monkeypatch):
    def refuse(request):
        raise httpx.ConnectError("no route")

    s = Script(monkeypatch, refuse)

    with pytest.raises(FetchError) as raised:
        get_text(s.client, "https://x/")
    assert raised.value.status is None
    assert s.calls == MAX_RETRIES

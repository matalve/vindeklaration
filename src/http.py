"""Shared HTTP helpers.

Everything here is deliberately sequential and slow. We are a guest on
Systembolaget's servers: one request at a time, a pause between them, and a
User-Agent that says who we are.
"""

from __future__ import annotations

import random
import time

import httpx

USER_AGENT = (
    "vindeklaration/0.1 (open dataset of declared wine additives; "
    "+https://github.com/matalve/vindeklaration)"
)

# Public key used by systembolaget.se itself; the search API rejects requests
# without it. No account or agreement is involved.
SEARCH_API_KEY = "cfc702aed3094c86b92d6d4ff7a54c84"
SEARCH_URL = (
    "https://api-extern.systembolaget.se/sb-api-ecommerce/v1/productsearch/search"
)
SITE_URL = "https://www.systembolaget.se"

REQUEST_DELAY = 0.4
MAX_RETRIES = 4

# A server that says "come back in N seconds" is worth listening to, but not
# for hours: a longer request gives up on that URL and leaves the caller to
# decide what a run of such failures means.
RETRY_AFTER_CAP = 300.0

# Worth another attempt: the request timed out, or we were told to slow down.
# Every other 4xx is a statement about the request itself and repeats verbatim.
RETRYABLE_4XX = {408, 429}


class FetchError(RuntimeError):
    """A URL we gave up on. `permanent` means a retry could not have helped."""

    def __init__(self, message: str, *, status: int | None = None, permanent=False):
        super().__init__(message)
        self.status = status
        self.permanent = permanent


def client(*, api_key: bool = False) -> httpx.Client:
    headers = {"User-Agent": USER_AGENT, "accept": "application/json"}
    if api_key:
        headers["ocp-apim-subscription-key"] = SEARCH_API_KEY
        headers["Referer"] = f"{SITE_URL}/"
    return httpx.Client(headers=headers, timeout=40.0, follow_redirects=True)


def _retry_after(response: httpx.Response) -> float | None:
    """Seconds the server asked us to wait, if it said so in delta-seconds."""
    value = response.headers.get("retry-after", "")
    try:
        return max(0.0, float(value))
    except ValueError:
        return None  # absent, or an HTTP-date we do not bother to parse


def _get(http: httpx.Client, url: str, parse, *, not_found_ok: bool = False):
    """GET with backoff, returning `parse(response)`.

    A body `parse` cannot read counts as a failed attempt, as it always has.
    Returns None for 404 when `not_found_ok`.
    """
    delay = 2.0
    for attempt in range(MAX_RETRIES):
        wait = delay * random.uniform(0.5, 1.5)
        try:
            response = http.get(url)
            if response.status_code == 404 and not_found_ok:
                return None
            response.raise_for_status()
            return parse(response)
        except httpx.HTTPStatusError as error:
            status = error.response.status_code
            if 400 <= status < 500 and status not in RETRYABLE_4XX:
                raise FetchError(
                    f"giving up on {url}: {error}", status=status, permanent=True
                ) from error
            asked = _retry_after(error.response) if status in (429, 503) else None
            if asked is not None:
                if asked > RETRY_AFTER_CAP:
                    raise FetchError(
                        f"giving up on {url}: asked to wait {asked:.0f}s "
                        f"(cap {RETRY_AFTER_CAP:.0f}s)",
                        status=status,
                    ) from error
                wait = asked
            failure = error
        except (httpx.HTTPError, ValueError) as error:
            status = None
            failure = error
        if attempt == MAX_RETRIES - 1:
            raise FetchError(
                f"giving up on {url}: {failure}", status=status
            ) from failure
        time.sleep(wait)
        delay *= 2
    raise AssertionError("unreachable")  # pragma: no cover


def get_json(http: httpx.Client, url: str) -> dict | None:
    """GET JSON with backoff. Returns None for 404 (product genuinely gone)."""
    return _get(http, url, lambda r: r.json(), not_found_ok=True)


def get_text(http: httpx.Client, url: str) -> str:
    return _get(http, url, lambda r: r.text)

"""Shared HTTP helpers.

Everything here is deliberately sequential and slow. We are a guest on
Systembolaget's servers: one request at a time, a pause between them, and a
User-Agent that says who we are.
"""

from __future__ import annotations

import time

import httpx

USER_AGENT = (
    "wine-additives/0.1 (open dataset of declared wine additives; "
    "+https://github.com/matalve/wine-additives)"
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


def client(*, api_key: bool = False) -> httpx.Client:
    headers = {"User-Agent": USER_AGENT, "accept": "application/json"}
    if api_key:
        headers["ocp-apim-subscription-key"] = SEARCH_API_KEY
        headers["Referer"] = f"{SITE_URL}/"
    return httpx.Client(headers=headers, timeout=40.0, follow_redirects=True)


def get_json(http: httpx.Client, url: str) -> dict | None:
    """GET with backoff. Returns None for 404 (product genuinely gone)."""
    delay = 2.0
    for attempt in range(MAX_RETRIES):
        try:
            response = http.get(url)
            if response.status_code == 404:
                return None
            response.raise_for_status()
            return response.json()
        except (httpx.HTTPError, ValueError) as error:
            if attempt == MAX_RETRIES - 1:
                raise RuntimeError(f"giving up on {url}: {error}") from error
            time.sleep(delay)
            delay *= 2
    return None


def get_text(http: httpx.Client, url: str) -> str:
    delay = 2.0
    for attempt in range(MAX_RETRIES):
        try:
            response = http.get(url)
            response.raise_for_status()
            return response.text
        except httpx.HTTPError as error:
            if attempt == MAX_RETRIES - 1:
                raise RuntimeError(f"giving up on {url}: {error}") from error
            time.sleep(delay)
            delay *= 2
    return ""

"""Step 1: fetch every wine from Systembolaget's product search API.

The search API is fast and cheap but carries no ingredient information — that
lives on the product page and is handled by details.py.

Two upstream quirks shape this module:

* `size` is capped at 30 no matter what you ask for.
* Deep pagination stops after roughly 10 000 results (the usual Elasticsearch
  window), so an unfiltered query silently returns about 8 900 of the 15 500
  wines. We therefore partition the query — by country, and by wine type if a
  single country ever grows past the window — and merge the parts.
"""

from __future__ import annotations

import argparse
import json
import sys
import time
import urllib.parse
from pathlib import Path

import httpx

from .http import REQUEST_DELAY, SEARCH_URL, client, get_json

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
CATALOG_PATH = DATA_DIR / "catalog.json"

PAGE_SIZE = 30
# Stay clear of the pagination window; above this a partition must be split.
WINDOW_LIMIT = 9900
# Re-sweeping the whole assortment costs ten minutes, so only do it when enough
# wines are missing to be worth it.
SWEEP_THRESHOLD = 25

TTY = sys.stdout.isatty()

# Fields worth keeping. The search response has ~70 more that either duplicate
# the product page or describe stock levels that change hourly.
KEEP = [
    "productNumber",
    "productId",
    "productNameBold",
    "productNameThin",
    "producerName",
    "supplierName",
    "country",
    "originLevel1",
    "vintage",
    "price",
    "volume",
    "alcoholPercentage",
    "sugarContentGramPer100ml",
    "grapes",
    "categoryLevel1",
    "categoryLevel2",
    "categoryLevel3",
    "assortmentText",
    "tasteSymbols",
    "usage",
    "isOrganic",
    "isSustainableChoice",
    "isEthical",
    "isDiscontinued",
    "productLaunchDate",
]


def _query(params: dict[str, str]) -> str:
    return urllib.parse.urlencode(params, quote_via=urllib.parse.quote)


def fetch_partition(
    http: httpx.Client, params: dict[str, str], into: dict[str, dict]
) -> int:
    """Page through one filtered query. Returns the API's own doc count."""
    page = 1
    doc_count = 0
    while True:
        url = f"{SEARCH_URL}?size={PAGE_SIZE}&page={page}&{_query(params)}"
        payload = get_json(http, url)
        if not payload:
            break
        for product in payload.get("products", []):
            number = product.get("productNumber")
            if number:
                into[number] = {field: product.get(field) for field in KEEP}
        metadata = payload.get("metadata", {})
        doc_count = metadata.get("docCount", doc_count)
        next_page = metadata.get("nextPage", -1)
        if next_page == -1 or next_page == page:
            break
        page = next_page
        time.sleep(REQUEST_DELAY)
    return doc_count


def fetch_catalog(category: str = "Vin") -> list[dict]:
    products: dict[str, dict] = {}
    with client(api_key=True) as http:
        base = {"categoryLevel1": category}

        # First pass: unfiltered. It is truncated by the pagination window but
        # it is the cheapest way to learn which countries and wine types exist.
        total = fetch_partition(http, base, products)
        print(f"{total} wines reported upstream; {len(products)} from the first pass")

        countries = sorted({p["country"] for p in products.values() if p.get("country")})
        types = sorted({p["categoryLevel2"] for p in products.values() if p.get("categoryLevel2")})

        for index, country in enumerate(countries, start=1):
            params = base | {"country": country}
            expected = fetch_partition(http, params, products)
            if expected > WINDOW_LIMIT:
                # Too big to page through in one go: split it by wine type.
                for wine_type in types:
                    fetch_partition(http, params | {"categoryLevel2": wine_type}, products)
            print(
                f"  [{index}/{len(countries)}] {country}: {expected} "
                f"— {len(products)} unique so far",
                end="\r" if TTY else "\n",
                flush=True,
            )
            time.sleep(REQUEST_DELAY)
        print()

        gap = total - len(products)
        if gap > SWEEP_THRESHOLD:
            # Wines with no country set are invisible to the country partitions.
            print(f"{gap} wines unaccounted for; sweeping by type")
            for wine_type in types:
                fetch_partition(http, base | {"categoryLevel2": wine_type}, products)
            gap = total - len(products)
        if gap:
            # A handful of wines carry neither country nor type. Not worth a
            # second full sweep; report it so the number stays honest.
            print(f"{gap} wines could not be reached through any partition")

    return sorted(products.values(), key=lambda p: p["productNumber"])


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--category", default="Vin")
    args = parser.parse_args()

    products = fetch_catalog(args.category)
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    CATALOG_PATH.write_text(
        json.dumps(products, ensure_ascii=False, indent=1), encoding="utf-8"
    )
    print(f"wrote {len(products)} products to {CATALOG_PATH}")


if __name__ == "__main__":
    main()

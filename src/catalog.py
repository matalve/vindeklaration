"""Step 1: fetch every wine from Systembolaget's product search API.

The search API is fast and cheap but carries no ingredient information — that
lives on the product page and is handled by details.py.

Two upstream quirks shape this module:

* `size` is capped at 30 no matter what you ask for.
* Deep pagination stops after roughly 10 000 results (the usual Elasticsearch
  window), so an unfiltered query silently returns about 8 900 of the 15 500
  wines. We therefore partition the query — by country, and by wine type if a
  single country ever grows past the window — and merge the parts.
* The default order is not a total order, and every page request sorts it
  afresh, so consecutive pages overlap: some wines come twice and as many are
  never served. Paging France (4 754 wines) at 30 a page returned 3 699 of
  them; the loss is deterministic for a given page size, so repeating the same
  query does not help. Sorting by name fixes almost all of it — what is left
  is wines with the same name on a page boundary — and a second pass sorted
  the other way catches those: 4 702 + 4 723 = all 4 754. Measured 2026-11-22.
"""

from __future__ import annotations

import argparse
import json
import sys
import time
import urllib.parse
from pathlib import Path

import httpx

from . import seen
from .http import REQUEST_DELAY, SEARCH_URL, client, get_json

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
CATALOG_PATH = DATA_DIR / "catalog.json"

PAGE_SIZE = 30
# Stay clear of the pagination window; above this a partition must be split.
WINDOW_LIMIT = 9900
# Re-sweeping the whole assortment costs ten minutes, so only do it when enough
# wines are missing to be worth it.
SWEEP_THRESHOLD = 25
# A stable order for paging (see the module docstring). The second pass only
# runs for a partition the first one left short.
SORT_PASSES = (
    {"sortBy": "Name", "sortDirection": "Ascending"},
    {"sortBy": "Name", "sortDirection": "Descending"},
)

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
    # Whether the wine can be bought at all. Both are always present here and
    # refresh with the nightly catalog sweep, which is the only reason they are
    # trustworthy: stock is the one fact that goes stale in hours.
    "isCompletelyOutOfStock",
    "isTemporaryOutOfStock",
    "productLaunchDate",
    # The bottle photograph, kept as the API states it rather than rebuilt from
    # productId: a pattern we invent is a pattern we have to maintain. Note that
    # the URL is a template — it needs "_{size}.{ext}" appended to resolve.
    "images",
]


def _query(params: dict[str, str]) -> str:
    return urllib.parse.urlencode(params, quote_via=urllib.parse.quote)


def fetch_partition(
    http: httpx.Client,
    params: dict[str, str],
    into: dict[str, dict],
    found: set[str] | None = None,
) -> int:
    """Page through one filtered query. Returns the API's own doc count.

    `found`, if given, collects the product numbers this query served, so the
    caller can compare them with the count."""
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
                if found is not None:
                    found.add(number)
        metadata = payload.get("metadata", {})
        doc_count = metadata.get("docCount", doc_count)
        next_page = metadata.get("nextPage", -1)
        if next_page == -1 or next_page == page:
            break
        page = next_page
        time.sleep(REQUEST_DELAY)
    return doc_count


def sweep_partition(
    http: httpx.Client, params: dict[str, str], into: dict[str, dict]
) -> tuple[int, int]:
    """Page one partition in a stable order, twice if the first pass falls short.

    Returns the API's doc count and how many distinct wines were served. A
    partition past the pagination window is left to the caller to split: a
    second pass could not reach its far end either."""
    found: set[str] = set()
    expected = 0
    for index, order in enumerate(SORT_PASSES):
        if index:
            time.sleep(REQUEST_DELAY)
        expected = fetch_partition(http, params | order, into, found)
        if len(found) >= expected or expected > WINDOW_LIMIT:
            break
    return expected, len(found)


def fetch_catalog(category: str = "Vin") -> tuple[list[dict], dict]:
    """Every wine the search API serves, and what the sweep could not reach.

    The second value is the night's account of the gap: the upstream total, how
    many wines were found, and the partitions that came up short."""
    products: dict[str, dict] = {}
    short: dict[str, int] = {}
    with client(api_key=True) as http:
        base = {"categoryLevel1": category}

        # First pass: unfiltered. It is truncated by the pagination window but
        # it is the cheapest way to learn which countries and wine types exist.
        total = fetch_partition(http, base, products)
        print(f"{total} wines reported upstream; {len(products)} from the first pass")

        countries = sorted({p["country"] for p in products.values() if p.get("country")})
        types = sorted({p["categoryLevel2"] for p in products.values() if p.get("categoryLevel2")})

        def partition(params: dict[str, str], label: str) -> int:
            expected, served = sweep_partition(http, params, products)
            if served < expected <= WINDOW_LIMIT:
                short[label] = expected - served
            return expected

        for index, country in enumerate(countries, start=1):
            params = base | {"country": country}
            expected = partition(params, country)
            if expected > WINDOW_LIMIT:
                # Too big to page through in one go: split it by wine type.
                for wine_type in types:
                    partition(
                        params | {"categoryLevel2": wine_type}, f"{country} / {wine_type}"
                    )
            print(
                f"  [{index}/{len(countries)}] {country}: {expected} "
                f"— {len(products)} unique so far",
                end="\r" if TTY else "\n",
                flush=True,
            )
            time.sleep(REQUEST_DELAY)
        print()

        if short:
            print(
                "partitions still short after both passes: "
                + ", ".join(f"{label} {n}" for label, n in sorted(short.items()))
            )
        gap = total - len(products)
        if gap > SWEEP_THRESHOLD:
            # A fallback, not the routine: a wine with no country set would be
            # invisible to the country partitions. Before the sweep was sorted
            # this ran every night, plugging the pagination loss it was not
            # written for; the catalog of 2026-11-22 had no wine without one.
            print(f"{gap} wines unaccounted for; sweeping by type")
            for wine_type in types:
                sweep_partition(http, base | {"categoryLevel2": wine_type}, products)
            gap = total - len(products)
        if gap:
            # Report it so the number stays honest; seen.py records it too.
            print(f"{gap} wines could not be reached through any partition")

    account = {
        "reported": total,
        "found": len(products),
        "unreached": max(gap, 0),
        "short": short,
    }
    return sorted(products.values(), key=lambda p: p["productNumber"]), account


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--category", default="Vin")
    args = parser.parse_args()

    products, account = fetch_catalog(args.category)
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    CATALOG_PATH.write_text(
        json.dumps(products, ensure_ascii=False, indent=1), encoding="utf-8"
    )
    print(f"wrote {len(products)} products to {CATALOG_PATH}")
    # Observability only: a failure here must never cost the night's sweep.
    try:
        seen.record(products, sweep=account)
    except Exception as error:
        print(f"warning: could not record the sightings: {error}", file=sys.stderr)


if __name__ == "__main__":
    main()

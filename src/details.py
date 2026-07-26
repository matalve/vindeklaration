"""Step 2: fetch the ingredient declaration and nutrition table per wine.

Systembolaget's search API does not expose ingredients. The product page does,
and that page is a Next.js route, so the same data is available as plain JSON at

    /_next/data/{buildId}/produkt/vin/x-{productNumber}.json

The slug and the category segment in that path are ignored by the server; only
the trailing product number matters. The buildId changes on every deploy, so it
is discovered at runtime and never hardcoded.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import httpx

from .http import REQUEST_DELAY, SITE_URL, client, get_json, get_text

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
CACHE_DIR = DATA_DIR / "cache"
CATALOG_PATH = DATA_DIR / "catalog.json"

BUILD_ID_RE = re.compile(r'"buildId":"([0-9a-zA-Z_-]+)"')

TTY = sys.stdout.isatty()

# Swedish nutrient labels as they appear in the upstream table.
NUTRIENT_KEYS = {
    ("energi", "kcal"): "kcal_per_100ml",
    ("energi", "kj"): "kj_per_100ml",
    ("kolhydrat", "g"): "carbohydrate_g_per_100ml",
    ("varav sockerarter", "g"): "sugar_g_per_100ml",
    ("protein", "g"): "protein_g_per_100ml",
    ("fett", "g"): "fat_g_per_100ml",
    ("varav mättat fett", "g"): "saturated_fat_g_per_100ml",
    ("salt", "g"): "salt_g_per_100ml",
}

DETAIL_FIELDS = [
    "productNumber",
    "ingredients",
    "vintage",
    "isDKI",
    "isOrganic",
    "isNaturalWine",
    "isVeganFriendly",
    "isKosher",
    "sugarContentGramPer100ml",
    "producerName",
    "supplierName",
    "rawMaterial",
    "production",
    "standardDrinks",
]


def discover_build_id(http: httpx.Client) -> str:
    """Read the current Next.js buildId off any product page."""
    html = get_text(http, f"{SITE_URL}/produkt/vin/x-253108/")
    match = BUILD_ID_RE.search(html)
    if not match:
        raise RuntimeError(
            "could not find buildId — the site layout changed, check details.py"
        )
    return match.group(1)


def find_product_object(payload: Any) -> dict | None:
    """Locate the product object regardless of where SWR nested it.

    The real path is pageProps.fallback['@"api","ecommerce","product","<nr>",']
    but that key format is an implementation detail, so we search for the shape
    instead: the one dict that carries an "ingredients" key.
    """
    if isinstance(payload, dict):
        if "ingredients" in payload and "productNumber" in payload:
            return payload
        for value in payload.values():
            found = find_product_object(value)
            if found is not None:
                return found
    elif isinstance(payload, list):
        for value in payload:
            found = find_product_object(value)
            if found is not None:
                return found
    return None


def parse_nutrition(headers: list | None) -> dict:
    """Pull the per-100 ml block out of the nested nutrition table."""
    if not headers:
        return {}
    per_100ml = None
    for header in headers:
        unit = (header.get("measurementUnitCodeNameShort") or "").lower()
        if header.get("nutrientBasisQuantity") == 100 and unit == "ml":
            per_100ml = header
            break
    if per_100ml is None:
        return {}

    nutrition: dict[str, float] = {}

    def walk(rows: list) -> None:
        for row in rows:
            name = (row.get("nutrientTypeCodeName") or "").strip().lower()
            unit = (row.get("measurementUnitCodeNameShort") or "").strip().lower()
            key = NUTRIENT_KEYS.get((name, unit))
            if key is not None and row.get("quantityContained") is not None:
                nutrition[key] = row["quantityContained"]
            walk(row.get("child") or [])

    walk(per_100ml.get("productNutritions") or [])
    return nutrition


def extract(product: dict) -> dict:
    record = {field: product.get(field) for field in DETAIL_FIELDS}
    record["nutrition"] = parse_nutrition(product.get("productNutritionHeaders"))
    record["fetched_at"] = datetime.now(timezone.utc).isoformat(timespec="seconds")
    return record


def cache_path(product_number: str) -> Path:
    return CACHE_DIR / f"{product_number}.json"


def fetch_detail(
    http: httpx.Client, build_id: str, product_number: str
) -> dict | None:
    url = f"{SITE_URL}/_next/data/{build_id}/produkt/vin/x-{product_number}.json"
    payload = get_json(http, url)
    if payload is None:
        return None
    product = find_product_object(payload)
    if product is None:
        return None
    return extract(product)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--limit", type=int, default=0, help="stop after N products (0 = all)"
    )
    parser.add_argument(
        "--refresh",
        action="store_true",
        help="re-fetch products that are already cached",
    )
    parser.add_argument(
        "--only",
        nargs="*",
        help="fetch these product numbers only",
    )
    args = parser.parse_args()

    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    if args.only:
        numbers = list(args.only)
    else:
        catalog = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))
        numbers = [p["productNumber"] for p in catalog if p.get("productNumber")]

    todo = [
        n for n in numbers if args.refresh or not cache_path(n).exists()
    ]
    if args.limit:
        todo = todo[: args.limit]
    print(f"{len(todo)} of {len(numbers)} products to fetch")

    fetched = declared = missing = 0
    with client() as http:
        build_id = discover_build_id(http)
        print(f"buildId {build_id}")
        for index, number in enumerate(todo, start=1):
            record = fetch_detail(http, build_id, number)
            if record is None:
                missing += 1
            else:
                cache_path(number).write_text(
                    json.dumps(record, ensure_ascii=False, indent=1), encoding="utf-8"
                )
                fetched += 1
                if record.get("ingredients"):
                    declared += 1
            # On a terminal, overwrite one line often. Under systemd, stdout is
            # the journal, so report rarely and on its own line — otherwise a
            # full pass writes six hundred entries nobody will read.
            every = 25 if TTY else 500
            if index % every == 0 or index == len(todo):
                share = declared / fetched * 100 if fetched else 0
                print(
                    f"  {index}/{len(todo)} fetched={fetched} "
                    f"declared={declared} ({share:.0f}%) missing={missing}",
                    end="\r" if TTY else "\n",
                    flush=True,
                )
            time.sleep(REQUEST_DELAY)
    print()
    print(f"done: {fetched} cached, {declared} with a declaration, {missing} gone")


if __name__ == "__main__":
    main()

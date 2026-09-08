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
from collections.abc import Sequence
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import httpx

from .http import REQUEST_DELAY, SITE_URL, client, get_json, get_text

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
CACHE_DIR = DATA_DIR / "cache"
CATALOG_PATH = DATA_DIR / "catalog.json"

BUILD_ID_RE = re.compile(r'"buildId":"([0-9a-zA-Z_-]+)"')

# Any product page carries the buildId, so these only need to be products that
# are still on the shelf. Three, because the first one leaving the assortment
# would otherwise take down every run: Mateus and the Widow have been in the
# fixed assortment since 1955, which is the closest thing to a guarantee.
BUILD_ID_PRODUCTS = ("253108", "257101", "742401")

# A stale buildId turns every remaining request into a 404, and a 404 means
# "product gone". Nothing else produces a long run of them: the catalog is
# fetched minutes before this step, and every nightly run since the pipeline
# started has reported zero gone products, full refreshes included. Ten in a
# row is therefore not churn, it is a deploy that happened mid-run.
MISSING_STREAK = 10

# Second guard, for the case the first one cannot see: too much of the run
# missing means the run should not be believed at all. Only applied to runs
# large enough for a share to mean anything, so `--only` and small `--limit`
# passes are never judged by it.
MISSING_SHARE_LIMIT = 0.05
MISSING_SHARE_MIN_SAMPLE = 40

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
    "isGlutenFree",
    "isKosher",
    "sugarContentGramPer100ml",
    "producerName",
    "supplierName",
    "availableNumberOfStores",
    "rawMaterial",
    "production",
    "standardDrinks",
]


def discover_build_id(
    http: httpx.Client, candidates: Sequence[str] = BUILD_ID_PRODUCTS
) -> str:
    """Read the current Next.js buildId off any product page.

    Tries the candidates in order: a product that has left the assortment
    answers 404, which says nothing about the buildId and everything about the
    product, so it is worth asking the next one before giving up.
    """
    errors = []
    for number in candidates:
        try:
            html = get_text(http, f"{SITE_URL}/produkt/vin/x-{number}/")
        except RuntimeError as error:
            errors.append(f"{number}: {error}")
            continue
        match = BUILD_ID_RE.search(html)
        if match:
            return match.group(1)
        errors.append(f"{number}: page fetched but carries no buildId")
    raise RuntimeError(
        "could not find buildId — the site layout changed, check details.py"
        + "".join(f"\n  {line}" for line in errors)
    )


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


def fetch_details(
    http: httpx.Client, build_id: str, todo: list[str]
) -> dict[str, Any]:
    """Fetch each product, re-discovering the buildId if 404s start piling up.

    A 404 on the data route is ambiguous: the product may be gone, or the
    buildId in the URL may have gone stale because Systembolaget deployed
    during the several hours this pass takes. Read the wrong way, a deploy at
    midnight looks like the entire remaining assortment disappearing — and it
    would be recorded as such without anything failing. So a run of misses is
    treated as a suspicion rather than a fact: hold them back, ask the site
    what the buildId is now, and only count them as gone once the answer comes
    back unchanged.
    """
    fetched = declared = missing = 0
    rediscoveries = 0
    # Misses not yet ruled on. A success in between proves the buildId still
    # works, so anything held at that point really was gone.
    pending: list[str] = []
    # Raised each time re-discovery confirms the buildId: a run that genuinely
    # meets many gone products should not buy a discovery request per ten.
    streak_limit = MISSING_STREAK

    def store(number: str, record: dict) -> None:
        nonlocal fetched, declared
        cache_path(number).write_text(
            json.dumps(record, ensure_ascii=False, indent=1), encoding="utf-8"
        )
        fetched += 1
        if record.get("ingredients"):
            declared += 1

    def resolve_pending() -> None:
        """Rule on the held-back misses, re-fetching them if the buildId moved."""
        nonlocal build_id, missing, rediscoveries, streak_limit
        rediscoveries += 1
        current = discover_build_id(http)
        if current == build_id:
            missing += len(pending)
            streak_limit *= 2
        else:
            print(
                f"\nbuildId changed mid-run: {build_id} -> {current} — "
                f"retrying {len(pending)} products read as gone",
                flush=True,
            )
            build_id = current
            for number in pending:
                time.sleep(REQUEST_DELAY)
                record = fetch_detail(http, build_id, number)
                if record is None:
                    missing += 1
                else:
                    store(number, record)
            streak_limit = MISSING_STREAK
        pending.clear()

    for index, number in enumerate(todo, start=1):
        record = fetch_detail(http, build_id, number)
        if record is None:
            pending.append(number)
            if len(pending) >= streak_limit:
                resolve_pending()
        else:
            # The buildId answered, so the held-back misses were real.
            missing += len(pending)
            pending.clear()
            store(number, record)
        # On a terminal, overwrite one line often. Under systemd, stdout is
        # the journal, so report rarely and on its own line — otherwise a
        # full pass writes six hundred entries nobody will read.
        every = 25 if TTY else 500
        if index % every == 0 or index == len(todo):
            share = declared / fetched * 100 if fetched else 0
            print(
                f"  {index}/{len(todo)} fetched={fetched} "
                f"declared={declared} ({share:.0f}%) "
                f"missing={missing + len(pending)}",
                end="\r" if TTY else "\n",
                flush=True,
            )
        time.sleep(REQUEST_DELAY)

    # A pass that ends on a run of misses never reached the streak limit, so
    # the tail would go unchecked — which is precisely where a late deploy
    # lands. One request settles it.
    if pending:
        resolve_pending()

    return {
        "build_id": build_id,
        "fetched": fetched,
        "declared": declared,
        "missing": missing,
        "rediscoveries": rediscoveries,
    }


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

    with client() as http:
        build_id = discover_build_id(http)
        print(f"buildId {build_id}")
        result = fetch_details(http, build_id, todo)
    print()
    print(
        f"done: {result['fetched']} cached, {result['declared']} with a "
        f"declaration, {result['missing']} gone"
    )

    missing = result["missing"]
    if (
        len(todo) >= MISSING_SHARE_MIN_SAMPLE
        and missing > len(todo) * MISSING_SHARE_LIMIT
    ):
        print(
            f"FAILED: {missing} of {len(todo)} products ({missing / len(todo):.0%}) "
            f"could not be fetched, above the {MISSING_SHARE_LIMIT:.0%} limit. "
            "The assortment does not turn over that fast, and the buildId was "
            "re-checked, so something upstream has changed. Do not trust this "
            "run; see upstream-scout.",
            file=sys.stderr,
        )
        sys.exit(1)


if __name__ == "__main__":
    main()

"""Rebuild data/cache from a published data/wines.json.

The cache is a local copy of what was fetched, so losing it normally means
fetching everything again. But wines.json already carries every field the
pipeline reads out of the cache — the declaration text, the nutrition table,
the two flags and the fetch timestamp — so the entries can be re-derived
instead, and thousands of requests to Systembolaget avoided.

Re-derived entries are marked `"reconstructed": true`. They are missing the
fields details.py stores but nothing currently reads (isDKI, isKosher,
rawMaterial, production, standardDrinks), so the marker is what tells you an
entry has not been verified against the source since. The weekly full refresh
replaces them with real fetches.

    uv run python deploy/rebuild-cache.py [--force]
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
CACHE_DIR = DATA_DIR / "cache"
WINES_PATH = DATA_DIR / "wines.json"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--force",
        action="store_true",
        help="overwrite cache entries that already exist",
    )
    args = parser.parse_args()

    wines = json.loads(WINES_PATH.read_text(encoding="utf-8"))["wines"]
    CACHE_DIR.mkdir(parents=True, exist_ok=True)

    written = skipped = never_fetched = 0
    for wine in wines:
        # A wine with no fetch timestamp was never fetched; inventing an entry
        # for it would tell the fetcher not to bother.
        if not wine.get("fetched_at"):
            never_fetched += 1
            continue

        path = CACHE_DIR / f"{wine['product_number']}.json"
        if path.exists() and not args.force:
            skipped += 1
            continue

        path.write_text(
            json.dumps(
                {
                    "productNumber": wine["product_number"],
                    "ingredients": wine.get("raw_ingredients"),
                    "isNaturalWine": wine.get("natural_wine"),
                    "isVeganFriendly": wine.get("vegan"),
                    "nutrition": wine.get("nutrition") or {},
                    "fetched_at": wine["fetched_at"],
                    "reconstructed": True,
                },
                ensure_ascii=False,
                indent=1,
            ),
            encoding="utf-8",
        )
        written += 1

    print(f"rebuilt {written} cache entries")
    print(f"  {skipped} already present, left alone")
    print(f"  {never_fetched} wines had never been fetched")
    print(f"  cache now holds {len(list(CACHE_DIR.glob('*.json')))} entries")


if __name__ == "__main__":
    main()

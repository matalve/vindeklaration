"""Step 4: join the catalog with the cached declarations into the dataset.

Writes data/wines.json (the published dataset) and data/wines.sqlite (the same
rows, for anyone who would rather query than parse).
"""

from __future__ import annotations

import argparse
import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

from .details import CACHE_DIR
from .normalize import parse_ingredients

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
CATALOG_PATH = DATA_DIR / "catalog.json"
WINES_PATH = DATA_DIR / "wines.json"
SQLITE_PATH = DATA_DIR / "wines.sqlite"
SITE_URL = "https://www.systembolaget.se"


def wine_name(product: dict) -> str:
    parts = [product.get("productNameBold"), product.get("productNameThin")]
    return " ".join(part for part in parts if part).strip()


def build_records() -> list[dict]:
    catalog = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))
    records = []
    for product in catalog:
        number = product["productNumber"]
        cached = CACHE_DIR / f"{number}.json"
        detail = (
            json.loads(cached.read_text(encoding="utf-8")) if cached.exists() else {}
        )
        raw = (detail.get("ingredients") or "").strip()

        record = {
            "product_number": number,
            "name": wine_name(product),
            "producer": product.get("producerName"),
            "supplier": product.get("supplierName"),
            "vintage": product.get("vintage"),
            "country": product.get("country"),
            "region": product.get("originLevel1"),
            "category": product.get("categoryLevel2"),
            "style": product.get("categoryLevel3"),
            "assortment": product.get("assortmentText"),
            "price": product.get("price"),
            "volume_ml": product.get("volume"),
            "alcohol_percentage": product.get("alcoholPercentage"),
            "grapes": product.get("grapes") or [],
            "organic": bool(product.get("isOrganic")),
            "natural_wine": bool(detail.get("isNaturalWine")),
            "vegan": bool(detail.get("isVeganFriendly")),
            "nutrition": detail.get("nutrition") or {},
            "declaration_status": "declared" if raw else "not_declared",
            "raw_ingredients": raw or None,
            "source_url": f"{SITE_URL}/produkt/vin/x-{number}/",
            "fetched_at": detail.get("fetched_at"),
        }

        if raw:
            record.update(parse_ingredients(raw, record["grapes"]).as_output())
        else:
            record.update(
                {
                    "additive_count": None,
                    "parse_status": "not_declared",
                    "additives": [],
                    "gases": [],
                    "base_ingredients": [],
                    "processing_notes": [],
                    "allergens": [],
                    "unknown_tokens": [],
                }
            )
        records.append(record)
    return records


def write_sqlite(records: list[dict]) -> None:
    SQLITE_PATH.unlink(missing_ok=True)
    connection = sqlite3.connect(SQLITE_PATH)
    connection.executescript(
        """
        CREATE TABLE wines (
            product_number TEXT PRIMARY KEY,
            name TEXT, producer TEXT, vintage TEXT, country TEXT,
            category TEXT, assortment TEXT,
            price REAL, volume_ml REAL, alcohol_percentage REAL,
            organic INTEGER, declaration_status TEXT, parse_status TEXT,
            additive_count INTEGER, raw_ingredients TEXT, source_url TEXT
        );
        CREATE TABLE wine_additives (
            product_number TEXT, additive_id TEXT, e_number TEXT,
            category TEXT, bucket TEXT
        );
        CREATE INDEX idx_additive ON wine_additives (additive_id);
        CREATE INDEX idx_count ON wines (additive_count);
        """
    )
    connection.executemany(
        "INSERT INTO wines VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
        [
            (
                r["product_number"], r["name"], r["producer"], r["vintage"],
                r["country"], r["category"], r["assortment"], r["price"],
                r["volume_ml"], r["alcohol_percentage"], int(r["organic"]),
                r["declaration_status"], r["parse_status"], r["additive_count"],
                r["raw_ingredients"], r["source_url"],
            )
            for r in records
        ],
    )
    connection.executemany(
        "INSERT INTO wine_additives VALUES (?,?,?,?,?)",
        [
            (r["product_number"], a["id"], a.get("e_number"), a.get("category"), bucket)
            for r in records
            for bucket, items in (("additive", r["additives"]), ("gas", r["gases"]))
            for a in items
        ],
    )
    connection.commit()
    connection.close()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--no-sqlite", action="store_true")
    args = parser.parse_args()

    records = build_records()
    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "source": "Systembolaget",
        "wine_count": len(records),
        "declared_count": sum(
            1 for r in records if r["declaration_status"] == "declared"
        ),
        "wines": records,
    }
    WINES_PATH.write_text(
        json.dumps(payload, ensure_ascii=False, indent=1), encoding="utf-8"
    )
    print(f"wrote {len(records)} wines to {WINES_PATH}")
    if not args.no_sqlite:
        write_sqlite(records)
        print(f"wrote {SQLITE_PATH}")


if __name__ == "__main__":
    main()

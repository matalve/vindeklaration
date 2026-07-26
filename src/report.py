"""Step 5: quality and coverage reporting.

Two questions this answers: how much of the assortment declares anything, and
what did the normaliser fail to understand. The second one is the working list
for growing data/additives.yaml — unknown tokens are ranked by how many wines
they block.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path

from .build import known_names
from .normalize import parse_ingredients

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
WINES_PATH = DATA_DIR / "wines.json"
UNKNOWN_PATH = DATA_DIR / "unknown.json"

QUALITY_GATE = 0.02  # share of declared wines allowed to be `partial`


def load_wines() -> list[dict]:
    return json.loads(WINES_PATH.read_text(encoding="utf-8"))["wines"]


def share(part: int, whole: int) -> str:
    return f"{part / whole * 100:5.1f}%" if whole else "    — "


def breakdown(wines: list[dict], key: str, limit: int = 12) -> None:
    groups: dict[str, list[dict]] = {}
    for wine in wines:
        groups.setdefault(wine.get(key) or "okänd", []).append(wine)
    rows = sorted(groups.items(), key=lambda item: -len(item[1]))[:limit]
    for name, group in rows:
        declared = sum(1 for w in group if w["declaration_status"] == "declared")
        print(f"    {name[:28]:<28} {len(group):>6}  {share(declared, len(group))}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--top", type=int, default=15, help="rows in the top list")
    args = parser.parse_args()

    wines = load_wines()
    declared = [w for w in wines if w["declaration_status"] == "declared"]
    complete = [w for w in declared if w["parse_status"] == "complete"]
    partial = [w for w in declared if w["parse_status"] == "partial"]

    print(f"\nWines            {len(wines):>6}")
    print(f"  declared       {len(declared):>6}  {share(len(declared), len(wines))}")
    print(f"  parsed cleanly {len(complete):>6}  {share(len(complete), len(declared))}")
    print(f"  partial        {len(partial):>6}  {share(len(partial), len(declared))}")

    print("\nDeclaration coverage by vintage")
    by_vintage: dict[str, list[dict]] = {}
    for wine in wines:
        by_vintage.setdefault(wine.get("vintage") or "okänd", []).append(wine)
    for vintage in sorted(by_vintage, reverse=True)[:12]:
        group = by_vintage[vintage]
        hits = sum(1 for w in group if w["declaration_status"] == "declared")
        print(f"    {vintage:<28} {len(group):>6}  {share(hits, len(group))}")

    print("\nBy country")
    breakdown(wines, "country")
    print("\nBy assortment")
    breakdown(wines, "assortment")

    print("\nMost common additives (of declared wines)")
    counter = Counter(
        additive["id"] for wine in declared for additive in wine["additives"]
    )
    names = {
        additive["id"]: additive["name"]["sv"]
        for wine in declared
        for additive in wine["additives"]
    }
    for additive_id, count in counter.most_common(20):
        print(
            f"    {names.get(additive_id, additive_id)[:28]:<28} "
            f"{count:>6}  {share(count, len(declared))}"
        )

    print(f"\nFewest additives (top {args.top}, cleanly parsed only)")
    ranked = sorted(
        [w for w in complete if w["additive_count"] is not None],
        key=lambda w: (w["additive_count"], w["price"] or 0),
    )[: args.top]
    for wine in ranked:
        substances = ", ".join(a["name"]["sv"] for a in wine["additives"]) or "inga"
        print(
            f"    {wine['additive_count']}  {wine['name'][:34]:<34} "
            f"{(wine['vintage'] or '—'):<6} {wine['country'][:12]:<12} {substances[:44]}"
        )

    # Unknown tokens, ranked by how many wines they hold back.
    token_counter: Counter[str] = Counter()
    fuzzy_counter: Counter[str] = Counter()
    examples: dict[str, str] = {}
    for wine in declared:
        parsed = parse_ingredients(wine["raw_ingredients"], known_names(wine))
        for token in parsed.unknown_tokens:
            token_counter[token] += 1
            examples.setdefault(token, wine["source_url"])
        for token, alias in parsed.fuzzy_matches:
            fuzzy_counter[f"{token} -> {alias}"] += 1

    UNKNOWN_PATH.write_text(
        json.dumps(
            {
                "unknown_tokens": [
                    {"token": token, "wines": count, "example": examples[token]}
                    for token, count in token_counter.most_common()
                ],
                "fuzzy_matches": [
                    {"match": match, "wines": count}
                    for match, count in fuzzy_counter.most_common()
                ],
            },
            ensure_ascii=False,
            indent=1,
        ),
        encoding="utf-8",
    )
    print(f"\nUnknown tokens ({len(token_counter)} distinct) -> {UNKNOWN_PATH}")
    for token, count in token_counter.most_common(25):
        print(f"    {token[:34]:<34} {count:>5} wines   {examples[token]}")
    if fuzzy_counter:
        print("\nFuzzy matches (add these spellings to additives.yaml)")
        for match, count in fuzzy_counter.most_common(15):
            print(f"    {match[:48]:<48} {count:>5}")

    gate = len(partial) / len(declared) if declared else 0
    print(
        f"\nQuality gate: {gate * 100:.1f}% partial "
        f"(limit {QUALITY_GATE * 100:.0f}%) — {'PASS' if gate <= QUALITY_GATE else 'FAIL'}"
    )
    raise SystemExit(0 if gate <= QUALITY_GATE else 1)


if __name__ == "__main__":
    main()

"""Step 6: generate the static site from the dataset.

Phase 1 of docs/site-plan.md — lookup. A page per wine, a search page, and the
method page, in Swedish at the root and English under /en/. No server, no
database, no runtime dependency on Systembolaget: everything here is decided at
build time from data/wines.json.

Two rules from the plan are enforced here rather than left to the templates,
because a template is easy to change without noticing what it promised:

* A wine that declares nothing is never rendered as a wine containing nothing.
  The three declaration states are three states all the way through, and
  `state_of()` is the only place that decision is made.
* Bottle photographs appear on wine pages and nowhere else. Ranked, filtered
  and comparison pages carry none — docs/legal-notes.md §2j condition 8.
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import unicodedata
from datetime import datetime, timezone
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
WINES_PATH = DATA_DIR / "wines.json"
TEMPLATE_DIR = ROOT / "templates"
OUTPUT_DIR = ROOT / "site"

SITE_URL = "https://www.systembolaget.se"
# The catalog gives a template, not a fetchable URL: it needs a size and a
# format appended. 400 px is the largest that still loads on a shop's mobile
# signal. Rendered straight from their CDN, never copied — condition 1.
IMAGE_SUFFIX = "_400.png"

LANGUAGES = ("sv", "en")


def slugify(value: str) -> str:
    """A URL fragment that survives being read aloud and pasted into a chat."""
    decomposed = unicodedata.normalize("NFKD", value.lower())
    folded = decomposed.replace("ö", "o").replace("ä", "a").replace("å", "a")
    ascii_only = folded.encode("ascii", "ignore").decode("ascii")
    return re.sub(r"-+", "-", re.sub(r"[^a-z0-9]+", "-", ascii_only)).strip("-")


def state_of(wine: dict) -> str:
    """Which of the three declaration states this wine is in.

    The single place this is decided. `declared` means the supplier declared
    and the parser read all of it; `partial` means they declared and we could
    not; `silent` means they declared nothing. Never collapse `silent` into
    "no additives" — that is the claim the site exists not to make.
    """
    if wine["declaration_status"] != "declared":
        return "silent"
    return "partial" if wine["parse_status"] == "partial" else "declared"


def wine_path(wine: dict) -> str:
    return f"vin/{wine['product_number']}-{slugify(wine['name'])}"


def image_url(wine: dict) -> str | None:
    base = wine.get("image_base_url")
    return f"{base}{IMAGE_SUFFIX}" if base else None


def search_index(wines: list[dict]) -> list[dict]:
    """The compact index the browser filters against.

    Deliberately not the whole record: name, number, producer and the facts a
    result row shows. No raw declaration text — it is the largest field in the
    dataset and nothing on a results page displays it.
    """
    return [
        {
            "n": wine["product_number"],
            "t": wine["name"],
            "p": wine.get("producer") or "",
            "v": wine.get("vintage") or "",
            "c": wine.get("country") or "",
            "pr": wine.get("price"),
            "s": state_of(wine)[0],  # d, p or s
            "a": wine.get("additive_count"),
            "u": wine_path(wine),
        }
        for wine in wines
    ]


def coverage(wines: list[dict]) -> dict:
    declared = [w for w in wines if w["declaration_status"] == "declared"]
    partial = [w for w in declared if w["parse_status"] == "partial"]
    return {
        "wines": len(wines),
        "declared": len(declared),
        "partial": len(partial),
        "silent": len(wines) - len(declared),
        "declared_share": len(declared) / len(wines) * 100 if wines else 0,
        "partial_share": len(partial) / len(declared) * 100 if declared else 0,
    }


def strings(lang: str) -> dict:
    """UI text. Declarations themselves are never translated — only chrome."""
    table = json.loads((TEMPLATE_DIR / "strings.json").read_text(encoding="utf-8"))
    return table[lang]


def build(output: Path, limit: int | None = None) -> None:
    payload = json.loads(WINES_PATH.read_text(encoding="utf-8"))
    wines = payload["wines"]
    if limit:
        # A subset for iterating on templates without writing 30 000 files.
        wines = wines[:limit]

    env = Environment(
        loader=FileSystemLoader(TEMPLATE_DIR),
        autoescape=select_autoescape(["html"]),
        trim_blocks=True,
        lstrip_blocks=True,
    )
    env.filters["slugify"] = slugify

    stats = coverage(wines)
    generated = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    if output.exists():
        shutil.rmtree(output)
    output.mkdir(parents=True)

    index = search_index(wines)
    (output / "sok-index.json").write_text(
        json.dumps(index, ensure_ascii=False, separators=(",", ":")),
        encoding="utf-8",
    )
    shutil.copy(TEMPLATE_DIR / "site.css", output / "site.css")
    shutil.copy(TEMPLATE_DIR / "sok.js", output / "sok.js")

    wine_template = env.get_template("wine.html")
    index_template = env.get_template("index.html")
    method_template = env.get_template("method.html")

    for lang in LANGUAGES:
        s = strings(lang)
        prefix = output if lang == "sv" else output / "en"
        base = "" if lang == "sv" else "/en"

        for wine in wines:
            page = prefix / wine_path(wine)
            page.mkdir(parents=True, exist_ok=True)
            (page / "index.html").write_text(
                wine_template.render(
                    wine=wine,
                    state=state_of(wine),
                    image=image_url(wine),
                    source_url=wine["source_url"],
                    lang=lang,
                    s=s,
                    base=base,
                    generated=generated,
                ),
                encoding="utf-8",
            )

        prefix.mkdir(parents=True, exist_ok=True)
        (prefix / "index.html").write_text(
            index_template.render(
                stats=stats, lang=lang, s=s, base=base, generated=generated
            ),
            encoding="utf-8",
        )
        method = prefix / ("metod" if lang == "sv" else "method")
        method.mkdir(parents=True, exist_ok=True)
        (method / "index.html").write_text(
            method_template.render(
                stats=stats, lang=lang, s=s, base=base, generated=generated
            ),
            encoding="utf-8",
        )

    print(f"wrote {len(wines)} wines x {len(LANGUAGES)} languages to {output}")
    print(f"search index: {(output / 'sok-index.json').stat().st_size / 1e6:.1f} MB")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=OUTPUT_DIR)
    parser.add_argument("--limit", type=int, help="build only the first N wines")
    args = parser.parse_args()
    build(args.output, args.limit)


if __name__ == "__main__":
    main()

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

import yaml
from jinja2 import Environment, FileSystemLoader, select_autoescape

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
WINES_PATH = DATA_DIR / "wines.json"
LEXICON_PATH = DATA_DIR / "lexicon.yaml"
TEMPLATE_DIR = ROOT / "templates"
OUTPUT_DIR = ROOT / "site"

SITE_URL = "https://www.systembolaget.se"
# The catalog gives a template, not a fetchable URL: it needs a size and a
# format appended. webp rather than png: the same image is 77 kB instead of
# 255 kB, and 400 px stays sharp at the 200 px the stylesheet displays, on a
# phone in a shop. Rendered straight from their CDN, never copied — §2j
# condition 1.
IMAGE_SUFFIX = "_400.webp"
IMAGE_WIDTH, IMAGE_HEIGHT = 400, 400
# Condition 9 wants the premise of the image analysis visible and falsifiable,
# so the date the CDN was last confirmed to serve cross-origin without a
# technological measure is published on /metod rather than kept in a commit.
CDN_CHECKED = "2026-07-29"

# Cloudflare injects its own analytics beacon at the edge, with its own token,
# for browser-like requests — confirmed by reading a served page 2026-07-29.
# Nothing is rendered here, and nothing should be: a second beacon would double
# count. /metod describes what they inject; see `third_party` in strings.json.

LANGUAGES = ("sv", "en")

# Wine pages are built in Swedish only, decided 2026-07-29. Two languages times
# 15 000 wines is 30 101 files and Cloudflare Pages caps a deployment at 20 000.
# The chrome — front page, method — is still bilingual, and English search
# results link to the Swedish wine pages, which the English front page says.
# This is a hosting constraint and not a change of intent: see "Bilingual" in
# docs/site-plan.md for what it costs and what lifts it.
WINE_PAGE_LANGUAGES = ("sv",)


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


def build_index(wines: list[dict]) -> dict:
    """One index for both search and the filter, referenced by integer.

    Names repeat enormously across 15 000 wines — 57 countries, 438 grapes, 58
    substances — so the vocabularies are listed once and each wine points into
    them. Written as arrays rather than objects because a key repeated 15 000
    times is the largest thing in the file otherwise.

    Deliberately absent: `image_base_url`. The filter is a ranked surface and
    docs/legal-notes.md §2j condition 8 keeps photographs off those, so the
    index the browser holds cannot render one even by accident.
    """
    vocab: dict[str, list[str]] = {
        k: [] for k in ("country", "category", "assortment", "grape", "pairing", "additive")
    }
    seen: dict[str, dict[str, int]] = {k: {} for k in vocab}

    def index_of(kind: str, value: str) -> int:
        table = seen[kind]
        if value not in table:
            table[value] = len(vocab[kind])
            vocab[kind].append(value)
        return table[value]

    rows = []
    for wine in wines:
        # 0 orderable, 1 temporarily out, 2 out of stock. The plan puts
        # buyability first among the facets: a shortlist that sends someone to
        # the shop for a bottle that is not there has not answered the question.
        stock = 2 if wine.get("out_of_stock") else 1 if wine.get("temporarily_out_of_stock") else 0
        rows.append([
            wine["product_number"],
            wine["name"],
            wine.get("producer") or "",
            wine.get("vintage") or "",
            wine.get("price"),
            state_of(wine)[0],
            wine.get("additive_count"),
            index_of("country", wine.get("country") or ""),
            index_of("category", wine.get("category") or ""),
            index_of("assortment", wine.get("assortment") or ""),
            sorted(index_of("grape", g) for g in (wine.get("grapes") or [])),
            sorted(index_of("pairing", p) for p in (wine.get("food_pairings") or [])),
            sorted({index_of("additive", a["id"]) for a in wine["additives"]}),
            stock,
            wine_path(wine),
        ])
    return {"vocab": vocab, "wines": rows}


def coverage(wines: list[dict]) -> dict:
    declared = [w for w in wines if w["declaration_status"] == "declared"]
    partial = [w for w in declared if w["parse_status"] == "partial"]
    return {
        "wines": len(wines),
        "declared": len(declared),
        "read": len(declared) - len(partial),
        "partial": len(partial),
        "silent": len(wines) - len(declared),
        "declared_share": len(declared) / len(wines) * 100 if wines else 0,
        "partial_share": len(partial) / len(declared) * 100 if declared else 0,
    }


def additive_names(wines: list[dict], lang: str) -> dict:
    """Substance id to display name, for the filter's two substance menus."""
    names = {}
    for wine in wines:
        for a in wine["additives"]:
            names.setdefault(a["id"], a["name"][lang])
    return names


def allergen_labels() -> dict:
    """Display words for the allergen ids a substance can carry.

    Sulfites sit on almost every declared wine and say nothing about how it was
    made. Milk, egg and fish do: each names an animal-derived fining agent, and
    a reader should not have to already know that isinglass comes from fish.
    """
    return yaml.safe_load(LEXICON_PATH.read_text(encoding="utf-8"))["allergen_labels"]


# The ones that carry information. Kept separate from sulfites deliberately —
# see the note on `allergen_labels` in data/lexicon.yaml.
ANIMAL_ALLERGENS = ("milk", "egg", "fish")

# The nutrition declaration in EU label order, with a physical ceiling for each
# per 100 ml. Suppliers type these by hand like everything else, and two wines
# in the corpus carry values that cannot exist — 29 872 kcal and 240 g of
# carbohydrate in 100 ml. A figure over its ceiling is not shown and not
# guessed at; the page says one could not be read, which is what `partial` does
# for declaration text. Pure fat is 900 kcal per 100 g, so 400 is already far
# above anything a wine can reach.
NUTRIENTS = (
    ("kcal_per_100ml", "kcal", 400),
    ("kj_per_100ml", "kJ", 1700),
    ("fat_g_per_100ml", "g", 50),
    ("saturated_fat_g_per_100ml", "g", 50),
    ("carbohydrate_g_per_100ml", "g", 100),
    ("sugar_g_per_100ml", "g", 100),
    ("protein_g_per_100ml", "g", 50),
    ("salt_g_per_100ml", "g", 10),
)


def fmt(value: float) -> str:
    """Swedish number: decimal comma, and no trailing .0 on a whole number."""
    text = f"{value:g}"
    return text.replace(".", ",")


def nutrition_rows(wine: dict) -> tuple[list[dict], int]:
    """The declared figures, and how many were beyond what is physically possible."""
    declared = wine.get("nutrition") or {}
    rows, unreadable = [], 0
    energy = []
    for key, unit, ceiling in NUTRIENTS:
        value = declared.get(key)
        if value is None:
            continue
        if value > ceiling:
            unreadable += 1
            continue
        if key in ("kj_per_100ml", "kcal_per_100ml"):
            energy.append((key, value, unit))
            continue
        rows.append({"key": key, "value": value, "unit": unit})
    if energy:
        # kJ before kcal, as the label prints it.
        energy.sort(key=lambda e: e[0] != "kj_per_100ml")
        rows.insert(0, {
            "key": "energy",
            "display": " / ".join(f"{fmt(v)} {u}" for _, v, u in energy),
        })
    return rows, unreadable


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
    env.filters["num"] = fmt

    stats = coverage(wines)
    allergens = allergen_labels()
    generated = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    if output.exists():
        shutil.rmtree(output)
    output.mkdir(parents=True)

    (output / "sok-index.json").write_text(
        json.dumps(build_index(wines), ensure_ascii=False, separators=(",", ":")),
        encoding="utf-8",
    )
    shutil.copy(TEMPLATE_DIR / "site.css", output / "site.css")
    shutil.copy(TEMPLATE_DIR / "sok.js", output / "sok.js")
    shutil.copy(TEMPLATE_DIR / "hitta.js", output / "hitta.js")

    wine_template = env.get_template("wine.html")
    index_template = env.get_template("index.html")
    method_template = env.get_template("method.html")
    notfound_template = env.get_template("notfound.html")
    find_template = env.get_template("hitta.html")

    for lang in LANGUAGES:
        s = strings(lang)
        prefix = output if lang == "sv" else output / "en"
        # Two different roots. `lang_root` is where this language's own chrome
        # lives; `base` is where wine pages live, which is the Swedish root for
        # both languages because only Swedish wine pages are built.
        lang_root = "" if lang == "sv" else "/en"
        base = ""

        if lang in WINE_PAGE_LANGUAGES:
            for wine in wines:
                page = prefix / wine_path(wine)
                page.mkdir(parents=True, exist_ok=True)
                (page / "index.html").write_text(
                    wine_template.render(
                        wine=wine,
                        state=state_of(wine),
                        nutrition=nutrition_rows(wine)[0],
                        nutrition_unreadable=nutrition_rows(wine)[1],
                        allergen_labels=allergens,
                        animal_allergens=ANIMAL_ALLERGENS,
                        image=image_url(wine),
                        image_width=IMAGE_WIDTH,
                        image_height=IMAGE_HEIGHT,
                        source_url=wine["source_url"],
                        lang=lang,
                        s=s,
                        base=base,
                        lang_root=lang_root,
                        generated=generated,
                    ),
                    encoding="utf-8",
                )

        prefix.mkdir(parents=True, exist_ok=True)
        (prefix / "index.html").write_text(
            index_template.render(
                stats=stats, lang=lang, s=s, base=base, lang_root=lang_root,
                generated=generated, cdn_checked=CDN_CHECKED,
            ),
            encoding="utf-8",
        )
        find = prefix / s["find_url"]
        find.mkdir(parents=True, exist_ok=True)
        (find / "index.html").write_text(
            find_template.render(
                lang=lang, s=s, base=base, lang_root=lang_root,
                generated=generated, cdn_checked=CDN_CHECKED,
                additive_names=additive_names(wines, lang),
            ),
            encoding="utf-8",
        )

        method = prefix / ("metod" if lang == "sv" else "method")
        method.mkdir(parents=True, exist_ok=True)
        (method / "index.html").write_text(
            method_template.render(
                stats=stats, lang=lang, s=s, base=base, lang_root=lang_root,
                generated=generated, cdn_checked=CDN_CHECKED,
            ),
            encoding="utf-8",
        )

    # A stale link to a wine that left the assortment is the most likely 404
    # this site will serve, so it says so and offers a way back in.
    (output / "404.html").write_text(
        notfound_template.render(
            lang="sv", s=strings("sv"), base="", lang_root="",
            generated=generated, cdn_checked=CDN_CHECKED,
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

"""Step 6: generate the static site from the dataset.

Phases 1 to 3 of docs/site-plan.md: a page per wine, search, the filter and its
saved slices, a page per substance, and the coverage breakdown. Swedish at the
root and English under /en/. No server, no database, no runtime dependency on
Systembolaget: everything here is decided at build time from data/wines.json.

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
import math
import re
import shutil
import unicodedata
from datetime import datetime, timezone
from pathlib import Path
from xml.sax.saxutils import escape

import yaml
from jinja2 import Environment, FileSystemLoader, select_autoescape

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
WINES_PATH = DATA_DIR / "wines.json"
LEXICON_PATH = DATA_DIR / "lexicon.yaml"
ADDITIVES_PATH = DATA_DIR / "additives.yaml"
TEMPLATE_DIR = ROOT / "templates"
OUTPUT_DIR = ROOT / "site"

# Where this site is served from. Needed absolute rather than relative in
# three places that a relative URL breaks outright: og:image (most scrapers
# will not resolve one), rel=canonical, and the sitemap.
ORIGIN = "https://vindeklaration.se"

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

# The repository is private until closer to a real launch (owner, 2026-08-02),
# so /metod may not tell a reader that the code and the data are already there
# to check — both links 404 for anyone but the owner. Flip this the same day
# the repository goes public and the page starts making the stronger claim.
# The importer table waits on the same flip: docs/site-plan.md, "Naming
# importers", requires every row to have a correction route that works.
REPO_PUBLIC = False

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


def page_urls(lang: str, sv_path: str, en_path: str | None) -> dict:
    """canonical and hreflang for one page, in the shape base.html expects.

    `en_path` is None for a page built in Swedish only — the wine pages, see
    WINE_PAGE_LANGUAGES. Those get a self-referential canonical and no
    alternate pair: one page in one language is not a translation of anything,
    and saying otherwise would promise an English reader a page that does not
    exist.
    """
    here = sv_path if lang == "sv" else en_path
    alternates: list[dict] = []
    if en_path is not None:
        alternates = [
            {"lang": "sv", "href": ORIGIN + sv_path},
            {"lang": "en", "href": ORIGIN + en_path},
            {"lang": "x-default", "href": ORIGIN + sv_path},
        ]
    return {"origin": ORIGIN, "canonical": ORIGIN + here, "alternates": alternates}


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
            # How many stores shelve it. Distinct from `stock` above: that is
            # nightly and says whether it can be had at all, this is weekly and
            # says whether it is on a shelf near anyone. Null stays null — the
            # filter must not read our own unfetched field as "no shelf".
            wine.get("store_count"),
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


def facet_coverage(wines: list[dict]) -> dict:
    """How much of the catalogue each filterable field is filled in for.

    The filter tells the reader these shares so that "no wines match" can be
    told apart from "the grape field is empty for 6 400 wines". They were
    written into the strings by hand in July and had begun to drift: the
    order-only share was published as "four wines in five" and is 71.7%, which
    is nearer three in four. A figure in prose that nobody recomputes is a
    figure that goes quietly wrong, so every one of them is measured here.
    """
    total = len(wines) or 1
    order_only = sum(1 for w in wines if (w.get("assortment") or "") == "Ordervaror")
    silent = sum(1 for w in wines if w["declaration_status"] != "declared")
    return {
        "grape": sum(1 for w in wines if w.get("grapes")) / total * 100,
        "pairing": sum(1 for w in wines if w.get("food_pairings")) / total * 100,
        "order_only": order_only / total * 100,
        "silent": silent / total * 100,
    }


def additive_names(wines: list[dict], lang: str) -> dict:
    """Substance id to display name, for the filter's two substance menus."""
    names = {}
    for wine in wines:
        for a in wine["additives"]:
            names.setdefault(a["id"], a["name"][lang])
    return names


# The three lists a parsed declaration is split into. A substance page covers
# all three, because a reader who saw "koldioxid" on a label is owed a page
# whether or not the project counts it — the page says which bucket it is in.
DECLARED_FIELDS = ("additives", "gases", "base_ingredients")

# How many of the declaring wines a substance page names outright. Long enough
# to be a real sample, short enough that the page is not a 1 800-row table.
SUBSTANCE_EXAMPLES = 30


def substance_pages(wines: list[dict]) -> tuple[list[dict], list[str]]:
    """One entry per substance that appears in at least one declaration.

    Returns the pages, and the ids that were declared but are not in the
    dictionary. The second half is not diagnostics: the index page says how
    many substances it covers, and that sentence would be wrong if the ids
    without an entry were simply forgotten.

    The dictionary in data/additives.yaml is the source for what a substance
    *is*; the corpus is the source for how often it is declared. A substance
    the dictionary knows but no wine declares gets no page — the body of the
    page is the wines, and an empty one would be a stub for a search engine.

    `note` is carried through only where the dictionary has one. Thirty-three
    of the entries have none, and a page that invented a description would be
    the guessing the project forbids, so those pages say so instead.
    """
    dictionary = {
        entry["id"]: entry
        for entry in yaml.safe_load(ADDITIVES_PATH.read_text(encoding="utf-8"))
    }
    declaring: dict[str, list[dict]] = {}
    for wine in wines:
        for field in DECLARED_FIELDS:
            for substance in wine.get(field) or []:
                declaring.setdefault(substance["id"], []).append(wine)

    pages, undefined = [], []
    for sid, declared_by in declaring.items():
        entry = dictionary.get(sid)
        if entry is None:
            undefined.append(sid)
            # An id parsed onto a wine that the dictionary no longer defines.
            # Skipping it silently would hide a real inconsistency, so the
            # build says so and carries on rather than inventing an entry.
            print(f"warning: {sid!r} is declared by {len(declared_by)} wines "
                  f"but is not in additives.yaml — no page built")
            continue
        # Alphabetical, not by additive count. Ordering a substance's wines by
        # how little they declare would make every substance page a second
        # leaderboard, which is not what it is for.
        by_name = sorted(declared_by, key=lambda w: w["name"])
        # Three states means three states here too. A wine whose declaration
        # could not be read in full still named this substance, so it belongs
        # on the page — but not silently alongside the fully read ones.
        # Two substances (carmine, anthocyanins) rest on a single partial wine
        # and would otherwise read as settled fact.
        partial = [w for w in by_name if state_of(w) == "partial"]
        pages.append({
            "id": sid,
            "name": entry["name"],
            "e_number": entry.get("e_number"),
            "bucket": entry["bucket"],
            "category": entry.get("category"),
            "allergen": entry.get("allergen"),
            "note": entry.get("note"),
            # The misspellings are the point: someone typing the exact string
            # off a label should land here. docs/site-plan.md, "Details that
            # matter more than they look".
            "aliases": entry.get("aliases") or [],
            "count": len(declared_by),
            "partial_count": len(partial),
            "examples": by_name[:SUBSTANCE_EXAMPLES],
        })
    return sorted(pages, key=lambda p: -p["count"]), sorted(undefined)


# Below this many wines a percentage says more about the sample than about the
# shelf, so the rows are aggregated and counted rather than published. The same
# statistical honesty rule the importer table uses, applied to a breakdown
# where nobody is named.
BREAKDOWN_MINIMUM = 40


def breakdown(wines: list[dict], key: str) -> list[dict]:
    """Declared share per value of one field, largest group first."""
    groups: dict[str, list[dict]] = {}
    for wine in wines:
        groups.setdefault(wine.get(key) or "", []).append(wine)

    def make(kind: str, value: str | None, group: list[dict]) -> dict:
        declared = sum(1 for w in group if w["declaration_status"] == "declared")
        return {
            "kind": kind,
            "value": value,
            "wines": len(group),
            "declared": declared,
            "share": declared / len(group) * 100 if group else 0,
        }

    # "Too few to publish a percentage for" and "Systembolaget left the field
    # blank" are different facts and get different rows. Merging them would be
    # the same conflation the filter is careful to avoid for grape and pairing:
    # an empty field is a gap at the source, not a thin sample.
    rows, thin = [], []
    for value, group in groups.items():
        if not value:
            continue
        if len(group) < BREAKDOWN_MINIMUM:
            thin.extend(group)
            continue
        rows.append(make("value", value, group))
    rows.sort(key=lambda r: -r["wines"])
    if thin:
        rows.append(make("aggregated", None, thin))
    if groups.get(""):
        rows.append(make("blank", None, groups[""]))
    return rows


# Vintage is a stand-in for the production date the dataset does not have, and
# every page that leans on it says so. Years at or after this one are certainly
# inside the requirement; the rest are a mix the data cannot separate.
COVERED_FROM = 2024


def vintage_rows(wines: list[dict]) -> list[dict]:
    """Declared share by vintage, newest first, then older years, then undated.

    Kept separate from `breakdown` because the undated wines are not a small
    tail to be aggregated away — they are thousands of bottles and the single
    largest reason the coverage figure understates the shelf, so they get their
    own labelled row rather than being folded in with the thin years. No count
    is quoted here: the figure moves nightly and a number in a docstring ages
    into a lie.

    Every wine lands in exactly one row and the rows sum to the total. A table
    that quietly dropped the thin years would not add up, and a coverage page
    whose own arithmetic does not close is the last place to spend credibility.
    """
    groups: dict[str, list[dict]] = {}
    for wine in wines:
        vintage = wine.get("vintage")
        groups.setdefault(str(vintage) if vintage else "", []).append(wine)

    def row(kind: str, value: str | None, group: list[dict]) -> dict:
        declared = sum(1 for w in group if w["declaration_status"] == "declared")
        return {
            "kind": kind,
            "value": value,
            "covered": kind == "aggregated_covered" or (
                kind == "year" and int(value) >= COVERED_FROM
            ),
            "wines": len(group),
            "declared": declared,
            "share": declared / len(group) * 100 if group else 0,
        }

    # Thin years are aggregated, but never across the coverage line. A vintage
    # 2026 with nine bottles is certainly inside the requirement; folding it in
    # with 2011 would put covered wines in a row the page describes as thin and
    # old, and would stop the two "certainly covered" rows from summing to the
    # headline figure above them.
    rows, thin_covered, thin_older = [], [], []
    for value, group in sorted(groups.items(), key=lambda kv: kv[0], reverse=True):
        if not value:
            continue
        if len(group) >= BREAKDOWN_MINIMUM:
            rows.append(row("year", value, group))
        elif int(value) >= COVERED_FROM:
            thin_covered.extend(group)
        else:
            thin_older.extend(group)
    if thin_covered:
        rows.append(row("aggregated_covered", None, thin_covered))
    if thin_older:
        rows.append(row("aggregated", None, thin_older))
    if groups.get(""):
        rows.append(row("undated", None, groups[""]))
    return rows


# No importer is ranked on fewer than this many wines in the qualifying
# vintages, so nobody tops or bottoms the table on four bottles. A statistical
# honesty rule, not a legal shield — docs/site-plan.md, "Naming importers".
IMPORTER_MINIMUM = 40

# How long an error report is promised to take. The plan requires the table to
# be "dated, and corrigible", and a correction route with no stated turnaround
# is a suggestion box. **The owner has not confirmed this number** — it is the
# one thing here that is a promise on their behalf rather than a measurement,
# and it must be settled before REPO_PUBLIC flips and the table ships.
CORRECTION_DAYS = 14


def is_covered(wine: dict) -> bool:
    """Whether the requirement certainly reaches this wine.

    Vintage standing in for the production date the dataset does not have. The
    error is one-sided by construction: everything this returns True for was
    produced after the cutoff, and an unknown number of wines it returns False
    for were too.
    """
    vintage = str(wine.get("vintage") or "")
    return vintage.isdigit() and int(vintage) >= COVERED_FROM


def importer_rows(wines: list[dict]) -> dict:
    """Declared share per importer, over the vintages the requirement reaches.

    `supplier` is Systembolaget's `supplierName`: the company that placed the
    wine on the Swedish market and supplied the product text they publish. That
    is the only claim these rows make. Article 8(1) of Regulation (EU) No
    1169/2011 puts labelling responsibility on the producer for EU-origin wine
    and on the importer only for third-country wine, and the dataset cannot
    resolve which limb applies — so nothing here may be read as a claim about
    legal responsibility. See docs/site-plan.md, "Naming importers".

    Two things this deliberately does not do. It does not rank on all vintages:
    that column is a function of how old an importer's stock is, and published
    as a ranking it would put a company declaring on 97 of every 100 covered
    bottles near the bottom. And it does not name anyone below the threshold —
    those are counted in one row instead.
    """
    covered: dict[str, list[dict]] = {}
    everything: dict[str, list[dict]] = {}
    for wine in wines:
        name = (wine.get("supplier") or "").strip()
        if not name:
            continue
        everything.setdefault(name, []).append(wine)
        if is_covered(wine):
            covered.setdefault(name, []).append(wine)

    def declared_in(group: list[dict]) -> int:
        return sum(1 for w in group if w["declaration_status"] == "declared")

    named, thin, thin_declared, thin_suppliers = [], 0, 0, 0
    for name, group in covered.items():
        if len(group) < IMPORTER_MINIMUM:
            thin += len(group)
            thin_declared += declared_in(group)
            thin_suppliers += 1
            continue
        whole = everything[name]
        named.append({
            "name": name,
            "slug": slugify(name),
            "wines": len(group),
            "declared": declared_in(group),
            "share": declared_in(group) / len(group) * 100,
            # Shown beside the ranking and never as it, labelled as what it is.
            "all_wines": len(whole),
            "all_share": declared_in(whole) / len(whole) * 100 if whole else 0,
            # Sorted for the detail page: the claim is checkable bottle by
            # bottle or it is not checkable at all.
            "qualifying": sorted(group, key=lambda w: w["name"]),
        })

    named.sort(key=lambda r: -r["share"])
    return {
        "named": named,
        "thin": {
            "wines": thin,
            "declared": thin_declared,
            "share": thin_declared / thin * 100 if thin else 0,
            "suppliers": thin_suppliers,
        },
    }


# Geometry for the vintage figure, in SVG user units. The viewBox scales to
# whatever width the column gives it, so these are proportions rather than
# pixels — but the bottom band exists so the x labels are inside the box and
# the container never grows a nested scrollbar.
CHART = {
    "width": 640, "height": 260,
    # 56 on the left because the top tick reads "100 %" and not "100": at the
    # tick font size that string is about 45 units wide, and the first version
    # put it at x=28 with text-anchor="end", which started it left of the
    # viewBox and clipped the leading digit at every width.
    "left": 56, "right": 6, "top": 12, "bottom": 44,
    "gap": 2,  # surface gap between adjacent bars, never a border around them
    # User units, so they scale with the viewBox. The svg is 640 wide and is
    # displayed at 640 on a desktop but about 335 on a phone — a factor of two.
    # 12 units rendered at 6 CSS px there, which is the same failure that moved
    # the boundary note out of the figure, one pixel short of it.
    "tick": 18,
    # What one year label needs, end to end, before the next may start. Four
    # digits at 18 units is about 40, so 48 leaves a real gap rather than
    # letting them touch.
    "label_pitch": 48,
}


def vintage_chart(rows: list[dict]) -> dict | None:
    """Declared share per vintage, as bars.

    Bars and not a line. The vintages are separate groups with separate
    denominators and nothing runs between them, so a line would interpolate a
    trend across a gap where there is no data — and a rising line is the exact
    shape a reader takes for a grade. See *What the site must never say*.

    Only real years are plotted. The aggregated and undated rows have no place
    on a time axis; they stay in the table under the figure, and the caption
    names both the total plotted and the wines left out, so the two reconcile.

    One colour for every bar. Shading each by its own value would double-encode
    the height as hue and turn the figure into a ranking of vintages.
    """
    years = [r for r in rows if r["kind"] == "year"]
    if len(years) < 2:
        return None
    # By number, not by string. Four-digit years happen to sort the same either
    # way, which is exactly why a string sort here would survive unnoticed
    # until the day it did not.
    years = sorted(years, key=lambda r: int(r["value"]))

    plot_w = CHART["width"] - CHART["left"] - CHART["right"]
    plot_h = CHART["height"] - CHART["top"] - CHART["bottom"]
    band = plot_w / len(years)
    baseline = CHART["top"] + plot_h

    bars = []
    for i, row in enumerate(years):
        height = plot_h * row["share"] / 100
        bars.append({
            "x": CHART["left"] + i * band + CHART["gap"] / 2,
            "y": baseline - height,
            "width": band - CHART["gap"],
            "height": height,
            "mid": CHART["left"] + (i + 0.5) * band,
            # A transparent target over the whole column. Two reasons: a
            # pinpoint hit area on a thin bar is the interaction anti-pattern,
            # and 2014 declares on nothing at all — a zero-height rect cannot
            # be hovered, so without this the one vintage with the starkest
            # figure would be the only one with no read-out. The visible bar
            # stays honest at zero rather than being given a stub.
            "hit_x": CHART["left"] + i * band,
            "hit_width": band,
            "year": row["value"],
            "share": row["share"],
            "wines": row["wines"],
            "declared": row["declared"],
            "covered": row["covered"],
        })

    # Where the certainly-covered vintages begin, drawn as an annotation rather
    # than as a second colour: it is a fact about the law, not a second data
    # series, and colouring it would need a legend to say what it meant.
    #
    # The line goes to the left of the oldest covered year that has its own
    # bar, and the note names *that* year rather than COVERED_FROM. The two are
    # 2024 today and will not always be: once 2024 sells down past the
    # threshold it is aggregated away, and a note hard-coded to 2024 would then
    # point at a bar that is not there.
    first_covered = next((b for b in bars if b["covered"]), None)

    # Every nth year label, counted back from the newest. Anchoring on the
    # oldest bar was wrong: with an even number of bars it dropped the label
    # from the most recent vintage, which is the one carrying the story.
    label_step = max(1, math.ceil(CHART["label_pitch"] / band))
    return {
        "bars": bars,
        "baseline": baseline,
        # How many wines the figure actually stands on. The caption names the
        # wines it leaves out; without this the reader has the excluded count
        # and no total to set it against, and the two exclusions do not add up
        # to the difference on their own.
        "plotted": sum(b["wines"] for b in bars),
        # The vintages that exist but are too thin to draw, counted apart from
        # the undated ones. Both are excluded and they are excluded for
        # different reasons, and without this the two named counts do not add
        # up to the total the caption also gives.
        "thin_years": sum(
            r["wines"] for r in rows
            if r["kind"] in ("aggregated", "aggregated_covered")
        ),
        # Solid hairlines, one shade off the surface. Never dashed: a dashed
        # rule reads as a threshold or a projection when it is just a grid.
        "grid": [
            {"value": v, "y": baseline - plot_h * v / 100}
            for v in (0, 25, 50, 75, 100)
        ],
        # None when the oldest plotted bar is already covered: the line would
        # then sit exactly on the y-axis, under a note that says "to the left
        # of it we do not know" with nothing to the left of it. Years away —
        # every vintage before 2024 would have to have sold down past the
        # threshold — but it draws a rule that describes nothing.
        "boundary": (first_covered["x"] - CHART["gap"] / 2)
                    if first_covered and first_covered is not bars[0] else None,
        "boundary_year": first_covered["year"] if first_covered else None,
        "label_step": label_step,
        "left": CHART["left"],
        "right": CHART["width"] - CHART["right"],
        "top": CHART["top"],
        "width": CHART["width"],
        "height": CHART["height"],
    }


def covered_stats(wines: list[dict]) -> dict:
    """The figures over the wines the requirement certainly reaches.

    "Certainly" is doing the work. Vintage 2024-onwards is a subset of what the
    rule covers, never a superset, so this share is a floor — see
    docs/site-plan.md, "Naming importers".
    """
    covered = [w for w in wines if str(w.get("vintage") or "").isdigit()
               and int(w["vintage"]) >= COVERED_FROM]
    declared = sum(1 for w in covered if w["declaration_status"] == "declared")
    undated = sum(1 for w in wines if not w.get("vintage"))
    older = len(wines) - len(covered) - undated
    return {
        "wines": len(covered),
        "declared": declared,
        "share": declared / len(covered) * 100 if covered else 0,
        "undated": undated,
        "older": older,
        "outside": undated + older,
    }


# Saved slices worth their own address. Only categories with enough read
# declarations to make an ordering mean anything: a "fewest additives" list of
# eight wines is not a ranking, it is the whole set with numbers on it.
LIST_CATEGORIES = ("Rött vin", "Vitt vin", "Mousserande vin", "Rosévin")
# Systembolaget's own name for the shelf range, matched literally here and in
# templates/hitta.js. Change one, change both — and see check_vocabulary().
FIXED_RANGE = "Fast sortiment"
LIST_PRICE_CAPS = (None, 150, 100)
LIST_MINIMUM = 100


def check_vocabulary(wines: list[dict]) -> list[str]:
    """Names this site matches by string against names Systembolaget controls.

    `LIST_CATEGORIES` and `FIXED_RANGE` are their words, not ours, and they are
    compared literally. If a category is renamed upstream the saved lists for
    it stop being built and the filter's "today" mode matches nothing — in both
    cases silently, because an empty result looks exactly like a slice that
    happens to hold nothing. Everything else on the site derives its vocabulary
    from the data; these two cannot, so they are checked instead.
    """
    categories = {w.get("category") for w in wines}
    assortments = {w.get("assortment") for w in wines}
    missing = [c for c in LIST_CATEGORIES if c not in categories]
    if FIXED_RANGE not in assortments:
        missing.append(FIXED_RANGE)
    return missing


def list_slices(wines: list[dict]) -> list[dict]:
    """The slices that get a page, each a stated comparison set.

    Never a global ranking: every slice names its category, because a sparkling
    wine declares dosage sugar and a fortified wine declares added alcohol, and
    ordering them against a still red would assert a comparability that does not
    exist. Only wines that can be ordered are included — a list that sends
    someone to the shop for a bottle that is not there has not answered.
    """
    slices = []
    for category in LIST_CATEGORIES:
        in_category = [
            w for w in wines
            if w.get("category") == category
            and not w.get("out_of_stock")
            and not w.get("temporarily_out_of_stock")
        ]
        for cap in LIST_PRICE_CAPS:
            held = [
                w for w in in_category
                if cap is None or (w.get("price") is not None and w["price"] <= cap)
            ]
            ranked = sorted(
                (w for w in held if state_of(w) == "declared"),
                key=lambda w: (w["additive_count"], w.get("price") or 0),
            )
            if len(ranked) < LIST_MINIMUM:
                continue
            slices.append({
                "category": category,
                "cap": cap,
                "held": held,
                "ranked": ranked,
                "partial": [w for w in held if state_of(w) == "partial"],
                "silent": [w for w in held if state_of(w) == "silent"],
                "slug": slugify(category) + (f"-under-{cap}-kr" if cap else ""),
            })
    return slices


def facet_labels(lang: str) -> dict:
    """Swedish facet value to its English word, or empty for the Swedish build.

    The Swedish is Systembolaget's own and is what the Swedish site shows. This
    is chrome so that the English filter is not a Swedish menu under an English
    label; a declaration is never translated, and that rule is untouched.
    A value with no entry falls back to the Swedish, which is visibly wrong on
    an English page — the intended failure, since a silent gap would read as a
    translation.
    """
    if lang == "sv":
        return {}
    return yaml.safe_load(LEXICON_PATH.read_text(encoding="utf-8"))["facet_labels"]


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


def count(value: int | None, lang: str) -> str:
    """A whole number with its thousands separator.

    Swedish groups with a space and English with a comma, and `15124` in
    running Swedish prose is simply a typo. The space is non-breaking: a count
    that wraps across a line break stops being one number.
    """
    if value is None:
        return ""
    grouped = f"{int(value):,}"
    return grouped.replace(",", " ") if lang == "sv" else grouped


def pct(value: float, lang: str) -> str:
    """A share to one decimal, with its sign, in the language's own typography.

    Two conventions and they differ in both places. Swedish writes 19,3 % — a
    decimal comma and a space before the sign; English writes 19.3% with a
    decimal point and no space. The sign belongs here rather than after the
    filter in every template, which is how thirteen templates came to hardcode
    a Swedish space onto English pages.

    The space is non-breaking: a percentage that wraps between the number and
    the sign has stopped being one value.
    """
    text = f"{value:.1f}"
    return text.replace(".", ",") + "\u00a0%" if lang == "sv" else text + "%"


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


# How widely a wine is shelved, as words rather than a flag — docs/site-plan.md,
# "Can you actually buy it". The number is `availableNumberOfStores`, read from
# the product page, so it is as old as that wine's own fetch and never older
# than the weekly refresh. The out-of-stock flags come from the nightly search
# instead, which is why they are reported separately rather than folded in: a
# wine can be shelved in 187 stores and still be out of stock today.
#
# The plan sampled order-only wines at 1 store on 2026-07-27. The first full
# refresh says otherwise — 9 161 wines are in **zero** stores and the median
# order-only wine is one of them — so zero is the common case and gets the
# careful wording rather than being treated as a missing value.
def findability(wine: dict) -> dict:
    count = wine.get("store_count")
    if count is None:
        return {"key": None}
    if count == 0:
        key = "shelves_none"
    elif count == 1:
        key = "shelves_one"
    else:
        key = "shelves_many"
    # Nightly, and therefore a different fact with a different age.
    out = bool(wine.get("out_of_stock"))
    return {
        "key": key,
        "count": count,
        "out": out,
        "temporarily_out": bool(wine.get("temporarily_out_of_stock")),
        # "A wait, not a dead end" is the sentence this section exists to make,
        # and it is only true while the wine can actually be ordered. Said over
        # a sold-out bottle it is simply false, so a wine that is out of stock
        # gets the shelving fact and no promise attached to it.
        "can_order": count <= 1 and not out,
        "as_of": (wine.get("fetched_at") or "")[:10],
    }


def strings(lang: str) -> dict:
    """UI text. Declarations themselves are never translated — only chrome."""
    table = json.loads((TEMPLATE_DIR / "strings.json").read_text(encoding="utf-8"))
    return table[lang]


def build(output: Path, limit: int | None = None) -> None:
    # The dataset is not in git, so its absence is an ordinary state on a fresh
    # checkout rather than a broken one. A bare FileNotFoundError here reads as
    # a missing file and sends the reader looking for what deleted it; on
    # Cloudflare it cost a build before anyone thought to check the build
    # command. Say where the file comes from instead.
    if not WINES_PATH.exists():
        raise SystemExit(
            f"{WINES_PATH} is missing. The dataset is not kept in git — the "
            "build downloads it:\n\n"
            "  mkdir -p data && curl -fsSL "
            "https://vindeklaration.se/data/wines.json.gz | gunzip "
            "> data/wines.json\n\n"
            "On the crawler, `uv run python -m src.build` rebuilds it from "
            "data/cache instead. See \"The dataset lives in R2, not git\" in "
            "docs/deploy-site.md."
        )
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
    env.filters["pct"] = pct
    env.filters["count"] = count
    env.filters["state"] = state_of
    env.filters["wine_url"] = wine_path

    stats = coverage(wines)
    allergens = allergen_labels()
    slices = list_slices(wines)
    facets_filled = facet_coverage(wines)
    for name in check_vocabulary(wines):
        # Not fatal: a renamed category should not take the whole site down.
        # Loud, though, because the symptom is a list that quietly stops being
        # built rather than anything that looks like an error.
        print(f"warning: {name!r} is matched by name but no wine has it — "
              f"a saved list or the filter's range mode is now empty")
    substances, undefined_substances = substance_pages(wines)
    # Named compliance statistics about real companies. Built always so the
    # tests and the build exercise it, rendered only once the correction route
    # in /metod actually resolves — docs/site-plan.md requires every row to be
    # corrigible, and a 404 is not a correction route.
    importers = importer_rows(wines) if REPO_PUBLIC else None
    # A wine page links a substance only where a page was actually built, so a
    # dictionary entry that disappears cannot turn 15 000 wine pages into
    # 404 links.
    substance_ids = {sub["id"] for sub in substances}
    covered = covered_stats(wines)
    breakdowns = {
        "category": breakdown(wines, "category"),
        "country": breakdown(wines, "country"),
        "vintage": vintage_rows(wines),
    }
    chart = vintage_chart(breakdowns["vintage"])
    generated = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    if output.exists():
        shutil.rmtree(output)
    output.mkdir(parents=True)

    (output / "sok-index.json").write_text(
        json.dumps(build_index(wines), ensure_ascii=False, separators=(",", ":")),
        encoding="utf-8",
    )
    shutil.copy(TEMPLATE_DIR / "site.css", output / "site.css")
    # Committed rather than generated per build: they change when the mark
    # changes, which is not nightly. tools/make_icons.py redraws them.
    for icon in sorted((TEMPLATE_DIR / "icons").iterdir()):
        shutil.copy(icon, output / icon.name)
    shutil.copy(TEMPLATE_DIR / "sok.js", output / "sok.js")
    shutil.copy(TEMPLATE_DIR / "hitta.js", output / "hitta.js")

    wine_template = env.get_template("wine.html")
    index_template = env.get_template("index.html")
    method_template = env.get_template("method.html")
    notfound_template = env.get_template("notfound.html")
    find_template = env.get_template("hitta.html")
    list_template = env.get_template("list.html")
    substance_template = env.get_template("substance.html")
    substances_template = env.get_template("substances.html")
    coverage_template = env.get_template("coverage.html")
    importer_template = env.get_template("importer.html")

    # Slugs differ per language, so an alternate cannot be derived by sticking
    # /en in front of the current path — both sets are needed at once.
    sv_s, en_s = strings("sv"), strings("en")
    sitemap: list[str] = []

    for lang in LANGUAGES:
        s = strings(lang)
        prefix = output if lang == "sv" else output / "en"
        # Two different roots. `lang_root` is where this language's own chrome
        # lives; `base` is where wine pages live, which is the Swedish root for
        # both languages because only Swedish wine pages are built.
        lang_root = "" if lang == "sv" else "/en"
        facets = facet_labels(lang)

        def urls(sv_path: str, en_path: str | None = None) -> dict:
            """Record the page in the sitemap and hand back its URL block."""
            meta = page_urls(lang, sv_path, en_path)
            sitemap.append(meta["canonical"])
            return meta

        def heading_for(sl: dict) -> str:
            label = (facets.get("category", {}).get(sl["category"]) or sl["category"])
            key = "list_heading_cap" if sl["cap"] else "list_heading"
            return s[key].replace("{cat}", label).replace("{cap}", str(sl["cap"] or ""))

        list_links = [
            {"slug": sl["slug"], "heading": heading_for(sl)} for sl in slices
        ]

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
                        substance_ids=substance_ids,
                        stock=findability(wine),
                        source_url=wine["source_url"],
                        **urls(f"/{wine_path(wine)}/"),
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
                **urls("/", "/en/"),
                stats=stats, lang=lang, s=s, base=base, lang_root=lang_root,
                generated=generated, cdn_checked=CDN_CHECKED, lists=list_links,
                additive_names=additive_names(wines, lang),
            ),
            encoding="utf-8",
        )
        find = prefix / s["find_url"]
        find.mkdir(parents=True, exist_ok=True)
        (find / "index.html").write_text(
            find_template.render(
                section="find", live_count=True,
                **urls(f"/{sv_s['find_url']}/", f"/en/{en_s['find_url']}/"),
                lang=lang, s=s, base=base, lang_root=lang_root,
                generated=generated, cdn_checked=CDN_CHECKED,
                additive_names=additive_names(wines, lang),
                facet_labels=facets, lists=list_links, filled=facets_filled,
            ),
            encoding="utf-8",
        )

        # Saved slices, rendered at build time. Unlike /hitta these need no
        # JavaScript, which makes them the version that survives a bad signal,
        # a crawler, and being shared.
        for sl in slices:
            page = prefix / s["list_url"] / sl["slug"]
            page.mkdir(parents=True, exist_ok=True)
            others = [
                {"slug": o["slug"], "heading": heading_for(o)}
                for o in slices if o["slug"] != sl["slug"]
            ]
            (page / "index.html").write_text(
                list_template.render(
                    section="find",
                    **urls(f"/{sv_s['list_url']}/{sl['slug']}/",
                           f"/en/{en_s['list_url']}/{sl['slug']}/"),
                    sl=sl, heading=heading_for(sl), other_lists=others,
                    lang=lang, s=s, base=base, lang_root=lang_root,
                    generated=generated, cdn_checked=CDN_CHECKED,
                    facet_labels=facets,
                ),
                encoding="utf-8",
            )

        # A page per substance, and an index over them. Both languages: this is
        # chrome and figures rather than declaration text, 58 substances cost
        # 118 files, and it is the surface people arrive on from a search
        # engine — journey 3 in docs/site-plan.md.
        substance_root = prefix / s["substance_url"]
        substance_root.mkdir(parents=True, exist_ok=True)
        (substance_root / "index.html").write_text(
            substances_template.render(
                section="substances",
                **urls(f"/{sv_s['substance_url']}/", f"/en/{en_s['substance_url']}/"),
                substances=substances, stats=stats,
                undefined_substances=undefined_substances,
                lang=lang, s=s, base=base, lang_root=lang_root,
                generated=generated, cdn_checked=CDN_CHECKED,
            ),
            encoding="utf-8",
        )
        for substance in substances:
            page = substance_root / substance["id"]
            page.mkdir(parents=True, exist_ok=True)
            (page / "index.html").write_text(
                substance_template.render(
                    section="substances",
                    **urls(f"/{sv_s['substance_url']}/{substance['id']}/",
                           f"/en/{en_s['substance_url']}/{substance['id']}/"),
                    sub=substance, stats=stats, allergen_labels=allergens,
                    lang=lang, s=s, base=base, lang_root=lang_root,
                    generated=generated, cdn_checked=CDN_CHECKED,
                ),
                encoding="utf-8",
            )

        cover = prefix / s["coverage_url"]
        cover.mkdir(parents=True, exist_ok=True)
        (cover / "index.html").write_text(
            coverage_template.render(
                section="coverage",
                **urls(f"/{sv_s['coverage_url']}/", f"/en/{en_s['coverage_url']}/"),
                stats=stats, covered=covered, breakdowns=breakdowns,
                lang=lang, s=s, base=base, lang_root=lang_root,
                generated=generated, cdn_checked=CDN_CHECKED,
                facet_labels=facets, covered_from=COVERED_FROM,
                minimum=BREAKDOWN_MINIMUM, importers=importers, chart=chart,
                importer_minimum=IMPORTER_MINIMUM,
                correction_days=CORRECTION_DAYS,
            ),
            encoding="utf-8",
        )

        # One page per named importer, so every row in the table can be
        # checked bottle by bottle — by them first of all. No bottle
        # photographs: this is a listing surface, §2j condition 8.
        if importers:
            for imp in importers["named"]:
                page = prefix / s["importer_url"] / imp["slug"]
                page.mkdir(parents=True, exist_ok=True)
                (page / "index.html").write_text(
                    importer_template.render(
                        section="coverage",
                        **urls(f"/{sv_s['importer_url']}/{imp['slug']}/",
                               f"/en/{en_s['importer_url']}/{imp['slug']}/"),
                        imp=imp, covered=covered, mean=covered["share"],
                        lang=lang, s=s, base=base, lang_root=lang_root,
                        generated=generated, cdn_checked=CDN_CHECKED,
                        covered_from=COVERED_FROM,
                        minimum=IMPORTER_MINIMUM,
                        correction_days=CORRECTION_DAYS,
                    ),
                    encoding="utf-8",
                )

        method = prefix / ("metod" if lang == "sv" else "method")
        method.mkdir(parents=True, exist_ok=True)
        (method / "index.html").write_text(
            method_template.render(
                section="method",
                **urls(f"/{sv_s['method_url']}/", f"/en/{en_s['method_url']}/"),
                stats=stats, lang=lang, s=s, base=base, lang_root=lang_root,
                generated=generated, cdn_checked=CDN_CHECKED,
                repo_public=REPO_PUBLIC,
            ),
            encoding="utf-8",
        )

    # A stale link to a wine that left the assortment is the most likely 404
    # this site will serve, so it says so and offers a way back in.
    (output / "404.html").write_text(
        notfound_template.render(
            origin=ORIGIN, canonical=None, alternates=[],
            lang="sv", s=strings("sv"), base="", lang_root="",
            generated=generated, cdn_checked=CDN_CHECKED,
        ),
        encoding="utf-8",
    )

    # Generated rather than committed, and that is the point: the sibling site
    # keeps a hand-written sitemap whose lastmod is three years stale. At 15 000
    # URLs there is no hand to write this one, and the generator already knows
    # every page it wrote. lastmod is the dataset's own build date — a real one
    # or none at all, never a guess.
    entries = "\n".join(
        f"  <url><loc>{escape(url)}</loc><lastmod>{generated}</lastmod></url>"
        for url in sitemap
    )
    (output / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f"{entries}\n</urlset>\n",
        encoding="utf-8",
    )

    # Minimal on purpose. This project reads other people's robots.txt every
    # night and reasons about them under RFC 9309, so what it serves should be
    # something it would be content to have parsed by its own rules: allow
    # everything, name the sitemap, and no performative crawler groups.
    (output / "robots.txt").write_text(
        "User-agent: *\n"
        "Allow: /\n"
        "\n"
        "# The search index is a data file, not a page: it has nothing to show in\n"
        "# a result. Kept out of the index rather than hidden — it stays public,\n"
        "# and the licence in LICENSES.md still applies to it.\n"
        "Disallow: /sok-index.json\n"
        "\n"
        f"Sitemap: {ORIGIN}/sitemap.xml\n",
        encoding="utf-8",
    )

    print(f"wrote {len(wines)} wines x {len(LANGUAGES)} languages to {output}")
    print(f"sitemap: {len(sitemap)} URLs")
    print(f"substance pages: {len(substances)} x {len(LANGUAGES)} languages")
    print(f"search index: {(output / 'sok-index.json').stat().st_size / 1e6:.1f} MB")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=OUTPUT_DIR)
    parser.add_argument("--limit", type=int, help="build only the first N wines")
    args = parser.parse_args()
    build(args.output, args.limit)


if __name__ == "__main__":
    main()

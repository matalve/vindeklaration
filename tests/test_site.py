"""The arithmetic behind the coverage page and the substance pages.

These are the figures the site publishes about itself, and the ones most
likely to be quoted by someone else. What is tested here is mostly that the
rows add up: a breakdown that silently drops a group still renders, still
looks plausible, and is wrong in the direction that flatters the shelf.
"""

from __future__ import annotations

import json
import re

from src.site import (
    CHART,
    FIXED_RANGE,
    LIST_CATEGORIES,
    check_vocabulary,
    count,
    ROOT,
    TEMPLATE_DIR,
    importer_rows,
    findability,
    breakdown,
    covered_stats,
    pct,
    substance_pages,
    vintage_chart,
    vintage_rows,
)


def wine(**overrides: object) -> dict:
    """One wine, declaring nothing, with everything the site reads present."""
    base = {
        "name": "Test",
        "product_number": "1234501",
        "declaration_status": "not_declared",
        "parse_status": "complete",
        "vintage": None,
        "country": "Italien",
        "category": "Rött vin",
        "additives": [],
        "gases": [],
        "base_ingredients": [],
    }
    base.update(overrides)
    return base


def declaring(**overrides: object) -> dict:
    return wine(declaration_status="declared", **overrides)


# --- vintage_rows ------------------------------------------------------------

def test_vintage_rows_account_for_every_wine() -> None:
    """No wine may fall out of the table between the corpus and the page."""
    wines = (
        [declaring(vintage=2024) for _ in range(45)]
        + [wine(vintage=2023) for _ in range(41)]
        # Two thin years, below the minimum, that must be aggregated not dropped.
        + [wine(vintage=2019) for _ in range(5)]
        + [declaring(vintage=2018) for _ in range(3)]
        + [wine(vintage=None) for _ in range(12)]
    )
    rows = vintage_rows(wines)

    assert sum(row["wines"] for row in rows) == len(wines)
    assert sum(row["declared"] for row in rows) == 48

    kinds = [row["kind"] for row in rows]
    assert kinds == ["year", "year", "aggregated", "undated"]
    # The eight wines from the two thin years, counted once, named never.
    assert rows[2]["wines"] == 8
    assert rows[2]["declared"] == 3
    assert rows[3]["wines"] == 12


def test_thin_covered_years_are_not_aggregated_with_the_old_ones() -> None:
    """The covered rows must sum to the headline figure above the table.

    A vintage newer than the corpus is always thin — nine 2026 bottles in a
    catalogue that has not turned over yet — and folding those in with 2011
    both understates the covered rows and files certainly-covered wines under
    a heading that says the opposite.
    """
    wines = (
        [declaring(vintage=2024) for _ in range(50)]
        + [declaring(vintage=2026) for _ in range(9)]
        + [wine(vintage=2011) for _ in range(4)]
    )
    rows = vintage_rows(wines)

    covered = [row for row in rows if row["covered"]]
    assert sum(row["wines"] for row in covered) == 59
    assert sum(row["declared"] for row in covered) == 59

    kinds = [row["kind"] for row in rows]
    assert kinds == ["year", "aggregated_covered", "aggregated"]
    assert rows[1]["wines"] == 9
    assert rows[2]["covered"] is False


def test_vintage_rows_mark_only_the_certainly_covered() -> None:
    wines = (
        [declaring(vintage=2024) for _ in range(40)]
        + [declaring(vintage=2023) for _ in range(40)]
    )
    covered = {row["value"]: row["covered"] for row in vintage_rows(wines)}

    assert covered["2024"] is True
    # 2023 wines may well be covered — the requirement turns on production
    # date, not vintage — but the dataset cannot show it, so the page does not
    # claim it either way.
    assert covered["2023"] is False


def test_undated_wines_are_never_marked_covered() -> None:
    rows = vintage_rows([wine(vintage=None) for _ in range(50)])

    assert rows[0]["kind"] == "undated"
    assert rows[0]["covered"] is False


# --- breakdown ---------------------------------------------------------------

def test_breakdown_aggregates_thin_groups_rather_than_dropping_them() -> None:
    wines = (
        [declaring(country="Italien") for _ in range(50)]
        + [wine(country="Georgien") for _ in range(3)]
        + [declaring(country="Libanon") for _ in range(2)]
    )
    rows = breakdown(wines, "country")

    assert sum(row["wines"] for row in rows) == 55
    assert [row["value"] for row in rows] == ["Italien", None]
    assert rows[-1]["kind"] == "aggregated"
    assert rows[-1]["wines"] == 5
    assert rows[-1]["declared"] == 2


def test_breakdown_share_is_declared_over_group() -> None:
    wines = (
        [declaring(category="Vitt vin") for _ in range(30)]
        + [wine(category="Vitt vin") for _ in range(70)]
    )
    rows = breakdown(wines, "category")

    assert rows[0]["share"] == 30.0


def test_breakdown_keeps_a_blank_field_apart_from_a_thin_sample() -> None:
    """Two different facts, two different rows.

    "Too few to publish a percentage" and "Systembolaget left the field empty"
    would otherwise share one row under a caption that describes only the
    first — the conflation the filter already avoids for grape and pairing.
    """
    wines = (
        [declaring(country="Italien") for _ in range(50)]
        + [wine(country="Georgien") for _ in range(3)]
        + [declaring(country="") for _ in range(80)]
    )
    rows = breakdown(wines, "country")

    assert [row["kind"] for row in rows] == ["value", "aggregated", "blank"]
    assert rows[1]["wines"] == 3
    assert rows[2]["wines"] == 80
    assert sum(row["wines"] for row in rows) == 133


# --- covered_stats -----------------------------------------------------------

def test_covered_stats_splits_the_shelf_without_losing_a_bottle() -> None:
    wines = (
        [declaring(vintage=2025) for _ in range(10)]
        + [wine(vintage=2024) for _ in range(10)]
        + [wine(vintage=2022) for _ in range(6)]
        + [wine(vintage=None) for _ in range(4)]
    )
    stats = covered_stats(wines)

    assert stats["wines"] == 20
    assert stats["declared"] == 10
    assert stats["share"] == 50.0
    assert stats["undated"] == 4
    assert stats["older"] == 6
    assert stats["outside"] == 10
    assert stats["wines"] + stats["outside"] == len(wines)


def test_covered_stats_survives_a_non_numeric_vintage() -> None:
    """Vintage comes from supplier-entered text and is not always a year."""
    stats = covered_stats([wine(vintage="NV"), declaring(vintage=2024)])

    assert stats["wines"] == 1
    assert stats["older"] == 1


# --- substance_pages ---------------------------------------------------------

SULFITES = {"id": "sulfites", "name": {"sv": "Sulfiter", "en": "Sulfites"}}
CO2 = {"id": "carbon_dioxide", "name": {"sv": "Koldioxid", "en": "Carbon dioxide"}}


def test_substance_pages_count_declaring_wines() -> None:
    wines = [declaring(name=f"W{i}", additives=[SULFITES]) for i in range(3)]
    pages = {p["id"]: p for p in substance_pages(wines)[0]}

    assert pages["sulfites"]["count"] == 3
    assert pages["sulfites"]["bucket"] == "additive"
    # The dictionary is what a substance *is*, so the E-number and the
    # misspellings come from there rather than from the parsed wine.
    assert pages["sulfites"]["e_number"] == "E220-E228"
    assert "sulfiter" in pages["sulfites"]["aliases"]


def test_substance_pages_cover_gases_and_raw_materials() -> None:
    """A reader who saw the word on a label is owed a page either way."""
    pages = {p["id"]: p for p in substance_pages([declaring(gases=[CO2])])[0]}

    assert pages["carbon_dioxide"]["bucket"] == "gas"


def test_substance_pages_report_an_id_the_dictionary_does_not_define() -> None:
    """Better a missing page than an invented description of a substance.

    The id is returned rather than dropped, because the index page publishes
    how many substances it covers and that sentence is wrong if the ones
    without an entry are forgotten.
    """
    ghost = {"id": "e999", "name": {"sv": "E999", "en": "E999"}}
    pages, undefined = substance_pages([declaring(additives=[ghost])])

    assert pages == []
    assert undefined == ["e999"]


def test_substance_examples_are_alphabetical_not_ranked() -> None:
    wines = [
        declaring(name="Zinfandel", additives=[SULFITES]),
        declaring(name="Amarone", additives=[SULFITES]),
    ]
    page = substance_pages(wines)[0][0]

    assert [w["name"] for w in page["examples"]] == ["Amarone", "Zinfandel"]


def test_substance_pages_count_the_partly_read_declarations() -> None:
    """A substance can rest entirely on a declaration we could not finish.

    Two do in the live corpus (carmine, anthocyanins), and a page that listed
    that wine unmarked would present it as settled.
    """
    wines = [
        declaring(name="Read in full", additives=[SULFITES]),
        declaring(name="Unread tail", parse_status="partial", additives=[SULFITES]),
    ]
    page = substance_pages(wines)[0][0]

    assert page["count"] == 2
    assert page["partial_count"] == 1


def test_a_substance_carried_only_by_a_partial_declaration_says_so() -> None:
    wines = [declaring(name="Only one", parse_status="partial", additives=[SULFITES])]
    page = substance_pages(wines)[0][0]

    assert page["count"] == page["partial_count"] == 1


# --- pct ---------------------------------------------------------------------

def test_pct_uses_the_decimal_separator_of_the_language() -> None:
    assert pct(19.34, "sv") == "19,3"
    assert pct(19.34, "en") == "19.3"


# --- findability -------------------------------------------------------------

def stocked(count: int | None, **overrides: object) -> dict:
    return wine(store_count=count, fetched_at="2026-08-02T03:14:00Z", **overrides)


def test_findability_words_scale_with_the_count() -> None:
    assert findability(stocked(187))["key"] == "shelves_many"
    assert findability(stocked(1))["key"] == "shelves_one"
    # Zero is the common case, not a missing value: 9 161 wines are in no
    # store at all, and the median order-only wine is one of them.
    assert findability(stocked(0))["key"] == "shelves_none"


def test_findability_is_silent_when_the_field_was_never_fetched() -> None:
    """A blank is not zero stores. Saying "no shelf" from a null would be a
    claim about the shelf drawn from our own missing data."""
    assert findability(stocked(None))["key"] is None


def test_findability_keeps_stock_apart_from_the_store_count() -> None:
    """Two facts of different ages. A wine can be shelved widely and still be
    out of stock today, so the page never folds one into the other."""
    out = findability(stocked(187, out_of_stock=True))

    assert out["key"] == "shelves_many"
    assert out["count"] == 187
    assert out["out"] is True


def test_findability_carries_the_date_the_count_was_read() -> None:
    """Nothing about stock is stated without its timestamp."""
    assert findability(stocked(42))["as_of"] == "2026-08-02"


def test_no_order_promise_over_a_sold_out_bottle() -> None:
    """"A wait, not a dead end" is false once the wine is gone."""
    assert findability(stocked(0, out_of_stock=True))["can_order"] is False
    assert findability(stocked(0))["can_order"] is True
    # Temporarily out is a different flag: it comes back, so the promise holds.
    assert findability(stocked(1, temporarily_out_of_stock=True))["can_order"] is True


def test_no_order_promise_where_the_wine_is_already_on_shelves() -> None:
    """452 stores do not need to be told the bottle can be ordered."""
    assert findability(stocked(452))["can_order"] is False


# --- importer_rows -----------------------------------------------------------

def supplied(name: str, vintage: int | None, declared: bool) -> dict:
    return wine(
        name=f"{name} {vintage}",
        supplier=name,
        vintage=vintage,
        declaration_status="declared" if declared else "not_declared",
    )


def test_importers_are_ranked_only_over_the_covered_vintages() -> None:
    """The whole design of the table is in this qualifier.

    An importer whose covered stock declares on 40 bottles of 40 must not be
    marked down for older stock the requirement never reached.
    """
    wines = (
        [supplied("Lidby", 2024, True) for _ in range(40)]
        + [supplied("Lidby", 2019, False) for _ in range(400)]
    )
    row = importer_rows(wines)["named"][0]

    assert row["wines"] == 40
    assert row["share"] == 100.0
    # The raw figure is carried, so the page can show it labelled — but it is
    # never what the rows are sorted on.
    assert round(row["all_share"], 1) == 9.1


def test_importers_below_the_threshold_are_counted_but_never_named() -> None:
    wines = (
        [supplied("Big", 2024, True) for _ in range(40)]
        + [supplied("Small", 2024, True) for _ in range(5)]
        + [supplied("Tiny", 2024, False) for _ in range(3)]
    )
    rows = importer_rows(wines)

    assert [r["name"] for r in rows["named"]] == ["Big"]
    assert rows["thin"]["wines"] == 8
    assert rows["thin"]["declared"] == 5
    assert rows["thin"]["suppliers"] == 2


def test_the_ranking_is_by_the_corrected_share_not_the_raw_one() -> None:
    """Published raw, the table would accuse the best importer of being worst.

    Lidby declares on every covered bottle and carries a deep back catalogue;
    Tryffel declares on few and has almost no old stock. Sorting on all
    vintages inverts them.
    """
    wines = (
        [supplied("Lidby", 2024, True) for _ in range(40)]
        + [supplied("Lidby", 2019, False) for _ in range(300)]
        + [supplied("Tryffel", 2024, True) for _ in range(10)]
        + [supplied("Tryffel", 2024, False) for _ in range(30)]
    )
    named = importer_rows(wines)["named"]

    assert [r["name"] for r in named] == ["Lidby", "Tryffel"]
    assert named[0]["all_share"] < named[1]["all_share"]


def test_every_named_row_carries_its_own_wines() -> None:
    """A row that cannot be checked bottle by bottle may not be published."""
    wines = [supplied("Big", 2024, i % 2 == 0) for i in range(40)]
    row = importer_rows(wines)["named"][0]

    assert len(row["qualifying"]) == row["wines"]
    assert row["slug"] == "big"


def test_a_wine_with_no_supplier_is_left_out_entirely() -> None:
    """Better absent than gathered into a row that names nobody in particular."""
    rows = importer_rows([wine(supplier="", vintage=2024) for _ in range(50)])

    assert rows["named"] == []
    assert rows["thin"]["wines"] == 0


def test_the_table_is_not_rendered_while_the_correction_route_is_a_404() -> None:
    """The gate itself, since it is the whole reason the table is not live.

    Naming 19 companies in a compliance statistic whose "report an error" link
    404s is the one part of the design that is not optional, so the build must
    not be one edited constant away from doing it by accident.
    """
    import src.site

    assert src.site.REPO_PUBLIC is False, (
        "REPO_PUBLIC is on: the importer table and /metod's claim that the "
        "repository is public will both ship. Confirm the repository is "
        "actually public, and confirm CORRECTION_DAYS with the owner, then "
        "delete this test."
    )


# --- theme -------------------------------------------------------------------

def test_the_theme_follows_the_system_unless_the_reader_overrides_it() -> None:
    """Three states, and the cascade is what makes the third one work.

    The OS decides by default; an explicit choice wins in both directions. The
    `:not([data-theme="light"])` guard is the whole mechanism — without it a
    reader on a dark OS who asks for light gets dark anyway, and nothing else
    in the file would look wrong.
    """
    css = (TEMPLATE_DIR / "site.css").read_text(encoding="utf-8")

    assert ':root {' in css
    assert '@media (prefers-color-scheme: dark) {' in css
    assert ':root:not([data-theme="light"]) {' in css
    assert ':root[data-theme="dark"] {' in css

    # An explicit dark choice has to be declared after the media block, or a
    # reader on a light OS asking for dark loses to the base palette.
    assert css.index('@media (prefers-color-scheme: dark)') < css.index(':root[data-theme="dark"]')


def test_no_hard_coded_theme_colour_survives_in_the_stylesheet() -> None:
    """Every colour is a variable, or half the page stays light in dark mode.

    Four did not, and each was invisible until the theme was switched: two
    inputs and the block that quotes a supplier's own declaration.
    """
    css = (TEMPLATE_DIR / "site.css").read_text(encoding="utf-8")
    palette = {"--ink", "--muted", "--line", "--paper", "--accent", "--field"}
    # A hex literal, not an id selector: `#filters` is a selector and fine.
    hex_colour = re.compile(r"#[0-9a-fA-F]{3,8}\b")

    for line in css.splitlines():
        body = line.split("/*")[0]
        if any(f"{name}:" in body for name in palette):
            continue
        found = hex_colour.findall(body)
        assert not found, f"hard-coded colour outside the palette: {line.strip()}"


# --- the icon ----------------------------------------------------------------

def test_the_icon_ink_matches_the_stylesheet_accent() -> None:
    """One mark, one palette. The icon is drawn by a separate script, so the
    two can drift silently — a wine glass in last season's red on a tab strip
    is the kind of thing nobody notices for months."""
    css = (TEMPLATE_DIR / "site.css").read_text(encoding="utf-8")
    icon = (ROOT / "tools" / "make_icons.py").read_text(encoding="utf-8")

    accents = {m.lower() for m in re.findall(r"--accent:\s*#([0-9a-fA-F]{6})", css)}
    inks = {
        "".join(f"{int(part, 16):02x}" for part in parts)
        for parts in re.findall(
            r"INK_(?:LIGHT|DARK) = \(0x([0-9A-Fa-f]{2}), 0x([0-9A-Fa-f]{2}), 0x([0-9A-Fa-f]{2})\)",
            icon,
        )
    }

    assert inks, "could not read the icon inks"
    assert inks == accents, f"icon {sorted(inks)} vs stylesheet {sorted(accents)}"


def test_the_icon_is_drawn_on_whole_pixels_at_tab_size() -> None:
    """16 px is the size a browser tab shows, and every edge has to land on a
    pixel boundary there — the first two drafts blurred into a smear below
    32 px because they did not."""
    icon = (ROOT / "tools" / "make_icons.py").read_text(encoding="utf-8")
    shapes = re.findall(r"\((\d+), (\d+), (\d+), (\d+)\),\s+#", icon)

    assert len(shapes) == 5, "expected the five rectangles of the mark"
    for x, y, w, h in shapes:
        for value in (x, y, w, h):
            assert int(value) == float(value), "a rectangle left the integer grid"
        assert int(y) + int(h) <= 16 and int(x) + int(w) <= 16, "a rectangle left the grid"


# --- the vintage figure ------------------------------------------------------

def test_only_real_years_get_a_bar() -> None:
    """The aggregated and undated rows have no place on a time axis.

    2 844 wines carry no vintage. Plotting them anywhere would invent a year
    for them; leaving them out silently would let the figure pass for the whole
    shelf, which is what the caption exists to deny.
    """
    wines = (
        [supplied("A", 2024, True) for _ in range(50)]
        + [supplied("A", 2023, False) for _ in range(50)]
        + [supplied("A", 2011, True) for _ in range(3)]     # thin -> aggregated
        + [wine(supplier="A", vintage=None) for _ in range(80)]  # undated
    )
    chart = vintage_chart(vintage_rows(wines))

    assert [b["year"] for b in chart["bars"]] == ["2023", "2024"]


def test_bars_run_chronologically() -> None:
    """Left to right in time. vintage_rows() returns newest first for the
    table, and a figure that inherited that order would read backwards."""
    wines = (
        [supplied("A", year, True) for year in (2022, 2023, 2024) for _ in range(45)]
    )
    chart = vintage_chart(vintage_rows(wines))

    years = [b["year"] for b in chart["bars"]]
    assert years == sorted(years)
    assert [b["x"] for b in chart["bars"]] == sorted(b["x"] for b in chart["bars"])


def test_a_vintage_declaring_nothing_gets_no_stub() -> None:
    """Zero is drawn as zero. A minimum visible height would put a bar under a
    year that declares on nothing, which is a small lie in the one place the
    figure is most stark — the hit area is what makes it readable instead."""
    wines = (
        [supplied("A", 2024, True) for _ in range(45)]
        + [supplied("A", 2023, False) for _ in range(45)]
    )
    chart = vintage_chart(vintage_rows(wines))
    empty = next(b for b in chart["bars"] if b["year"] == "2023")

    assert empty["height"] == 0
    assert empty["hit_width"] > 0, "a zero bar still needs somewhere to point"


def test_the_requirement_boundary_sits_at_the_first_covered_vintage() -> None:
    wines = [supplied("A", year, True) for year in (2023, 2024) for _ in range(45)]
    chart = vintage_chart(vintage_rows(wines))
    first_covered = next(b for b in chart["bars"] if b["covered"])

    assert chart["boundary"] == first_covered["x"] - CHART["gap"] / 2


def test_the_figure_carries_no_second_encoding_of_its_own_values() -> None:
    """One series, one colour. Shading each bar by its own height would
    double-encode the value and rank the vintages against each other, which is
    the reading *What the site must never say* forbids.
    """
    template = (TEMPLATE_DIR / "coverage.html").read_text(encoding="utf-8")
    figure = template[template.index('<figure class="chart"'):template.index("</figure>")]

    assert 'class="bar"' in figure
    # No per-bar class, style or fill that could vary with the datum.
    assert "fill=" not in figure
    assert "style=" not in figure
    assert "{{ b.share }}" not in figure.replace("b.share|pct(lang)", "")


def test_the_figure_is_not_the_only_place_a_value_lives() -> None:
    """Tooltips enhance, never gate. The table below is the accessible twin."""
    template = (TEMPLATE_DIR / "coverage.html").read_text(encoding="utf-8")
    # From the figure onwards, not from the top: the shared breakdown_table
    # macro defines a table of its own further up the file.
    after = template[template.index('<figure class="chart"'):]

    assert '<table class="breakdown">' in after, "the vintage table must follow the figure"
    assert after.index("</figure>") < after.index('<table class="breakdown">')


def test_counts_are_grouped_in_the_language_being_written() -> None:
    """`15124` in running Swedish prose is a typo, not a number."""
    assert count(15124, "sv") == "15 124"
    assert count(15124, "en") == "15,124"
    assert count(44, "sv") == "44"
    assert count(None, "sv") == ""


def test_the_figure_reconciles_against_the_page_it_sits_on() -> None:
    """The caption names what the figure covers and what it leaves out, and
    the two have to add up to the site total — otherwise a reader checking the
    arithmetic comes up short and has no way to know which number is wrong."""
    wines = (
        [supplied("A", 2024, True) for _ in range(50)]
        + [supplied("A", 2023, False) for _ in range(45)]
        + [supplied("A", 2011, True) for _ in range(3)]
        + [wine(supplier="A", vintage=None) for _ in range(80)]
    )
    chart = vintage_chart(vintage_rows(wines))
    rows = vintage_rows(wines)

    aggregated = sum(r["wines"] for r in rows if r["kind"] != "year")
    assert chart["plotted"] + aggregated == len(wines)


def test_the_boundary_note_names_the_year_the_line_is_actually_drawn_at() -> None:
    """COVERED_FROM is the law; the line is drawn at data.

    They are the same year today and will not always be. Once 2024 sells down
    past the threshold it is aggregated away, and a note hard-coded to 2024
    would point at a bar that is not on the chart.
    """
    wines = (
        [wine(vintage=year) for year in (2022, 2023) for _ in range(60)]
        + [declaring(vintage=2024) for _ in range(12)]   # thin, aggregated away
        + [declaring(vintage=year) for year in (2025, 2026) for _ in range(60)]
    )
    chart = vintage_chart(vintage_rows(wines))

    assert "2024" not in [b["year"] for b in chart["bars"]]
    assert chart["boundary_year"] == "2025"
    first_covered = next(b for b in chart["bars"] if b["covered"])
    assert chart["boundary"] == first_covered["x"] - CHART["gap"] / 2


def test_a_new_vintage_needs_no_code_change_to_appear() -> None:
    """The question this was written to answer: next year's releases arrive on
    their own. Nothing enumerates the years, and `covered` is derived from the
    cutoff in law rather than from a list that has to be maintained."""
    wines = [
        declaring(vintage=year)
        for year in range(2023, 2031)
        for _ in range(50)
    ]
    chart = vintage_chart(vintage_rows(wines))

    assert [b["year"] for b in chart["bars"]] == [str(y) for y in range(2023, 2031)]
    assert [b["year"] for b in chart["bars"] if b["covered"]] == \
        [str(y) for y in range(2024, 2031)]


def test_the_axis_keeps_a_real_gap_between_year_labels() -> None:
    """Four digits at the tick size are about 40 units wide, so labels need
    more than 40 units of pitch or they touch. The first threshold was the
    label width itself, which let them collide at 20 bars."""
    for count_of_years in (10, 15, 20, 26, 34):
        chart = vintage_chart(vintage_rows(
            [declaring(vintage=2026 - i) for i in range(count_of_years)
             for _ in range(50)]))
        band = chart["bars"][1]["x"] - chart["bars"][0]["x"]

        assert band * chart["label_step"] >= CHART["label_pitch"], (
            f"{count_of_years} years: labels {band * chart['label_step']:.0f} "
            f"units apart, need {CHART['label_pitch']}"
        )


def test_the_newest_vintage_is_always_labelled() -> None:
    """Thinning used to count from the oldest bar, which dropped the label off
    the most recent vintage whenever the count was even — the one year the
    figure is actually about."""
    for count_of_years in range(8, 32):
        chart = vintage_chart(vintage_rows(
            [declaring(vintage=2026 - i) for i in range(count_of_years)
             for _ in range(50)]))
        last = len(chart["bars"]) - 1

        assert (last - last) % chart["label_step"] == 0, "the newest bar must be labelled"


# --- vocabulary we do not control --------------------------------------------

def test_a_renamed_category_is_noticed() -> None:
    """The two places the site matches Systembolaget's words literally.

    A rename upstream stops the saved lists being built and empties the
    filter's range mode, and both failures look exactly like a slice that
    happens to hold nothing. Hermetic on purpose: it checks the detector, not
    tonight's catalogue, so a crawl cannot turn the suite red.
    """
    healthy = [
        wine(category=category, assortment="Fast sortiment")
        for category in LIST_CATEGORIES
    ]
    assert check_vocabulary(healthy) == []

    renamed = [w | {"category": "Rosé"} if w["category"] == "Rosévin" else w
               for w in healthy]
    assert check_vocabulary(renamed) == ["Rosévin"]

    no_range = [w | {"assortment": "Ordinarie sortiment"} for w in healthy]
    assert FIXED_RANGE in check_vocabulary(no_range)


def test_todays_catalogue_still_uses_the_names_the_site_matches() -> None:
    """Not hermetic, and deliberately so — this one is the canary.

    It reads the live dataset, so it turns red the day Systembolaget renames a
    category. That is the point: the alternative is noticing when someone
    happens to look at a list that has been empty for a month.
    """
    payload = json.loads((ROOT / "data" / "wines.json").read_text(encoding="utf-8"))

    assert check_vocabulary(payload["wines"]) == []


def test_the_range_name_is_the_same_in_python_and_in_the_browser() -> None:
    """`FIXED_RANGE` is matched literally in src/site.py and in hitta.js.

    Two copies of somebody else's word, and the failure mode if they drift is
    that the filter's "today" mode silently matches nothing while the build
    reports itself healthy.
    """
    js = (TEMPLATE_DIR / "hitta.js").read_text(encoding="utf-8")
    declared = re.search(r'var FIXED_RANGE = "([^"]+)"', js)

    assert declared, "hitta.js no longer declares FIXED_RANGE"
    assert declared.group(1) == FIXED_RANGE


def test_the_caption_names_every_wine_it_leaves_out() -> None:
    """Two exclusions with two different reasons, and both are counted.

    Undated wines and vintages too thin to draw are not the same fact, and
    giving only one of them leaves a reader who checks the arithmetic short by
    the other with no way to see which number is wrong.
    """
    wines = (
        [declaring(vintage=2024) for _ in range(50)]
        + [wine(vintage=2023) for _ in range(45)]
        + [declaring(vintage=2011) for _ in range(3)]     # thin year
        + [wine(vintage=None) for _ in range(80)]         # undated
    )
    chart = vintage_chart(vintage_rows(wines))
    stats = covered_stats(wines)

    assert chart["thin_years"] == 3
    assert chart["plotted"] + chart["thin_years"] + stats["undated"] == len(wines)


def test_no_boundary_line_once_every_bar_is_covered() -> None:
    """The rule would sit on the y-axis, under a note about what lies to the
    left of it, with nothing there. Years away, and still a line describing
    nothing."""
    wines = [declaring(vintage=year) for year in (2024, 2025) for _ in range(50)]
    chart = vintage_chart(vintage_rows(wines))

    assert all(b["covered"] for b in chart["bars"])
    assert chart["boundary"] is None

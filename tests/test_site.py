"""The arithmetic behind the coverage page and the substance pages.

These are the figures the site publishes about itself, and the ones most
likely to be quoted by someone else. What is tested here is mostly that the
rows add up: a breakdown that silently drops a group still renders, still
looks plausible, and is wrong in the direction that flatters the shelf.
"""

from __future__ import annotations

from src.site import (
    breakdown,
    covered_stats,
    pct,
    substance_pages,
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
    assert rows[-1]["wines"] == 5
    assert rows[-1]["declared"] == 2


def test_breakdown_share_is_declared_over_group() -> None:
    wines = (
        [declaring(category="Vitt vin") for _ in range(30)]
        + [wine(category="Vitt vin") for _ in range(70)]
    )
    rows = breakdown(wines, "category")

    assert rows[0]["share"] == 30.0


def test_breakdown_treats_an_empty_value_as_unnamed() -> None:
    """A blank field at Systembolaget is not a group worth naming."""
    wines = [declaring(country="") for _ in range(80)]
    rows = breakdown(wines, "country")

    assert [row["value"] for row in rows] == [None]
    assert rows[0]["wines"] == 80


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
    pages = {p["id"]: p for p in substance_pages(wines)}

    assert pages["sulfites"]["count"] == 3
    assert pages["sulfites"]["bucket"] == "additive"
    # The dictionary is what a substance *is*, so the E-number and the
    # misspellings come from there rather than from the parsed wine.
    assert pages["sulfites"]["e_number"] == "E220-E228"
    assert "sulfiter" in pages["sulfites"]["aliases"]


def test_substance_pages_cover_gases_and_raw_materials() -> None:
    """A reader who saw the word on a label is owed a page either way."""
    wines = [declaring(gases=[CO2])]
    pages = {p["id"]: p for p in substance_pages(wines)}

    assert pages["carbon_dioxide"]["bucket"] == "gas"


def test_substance_pages_skip_an_id_the_dictionary_does_not_define() -> None:
    """Better a missing page than an invented description of a substance."""
    ghost = {"id": "not_a_real_substance", "name": {"sv": "X", "en": "X"}}
    pages = substance_pages([declaring(additives=[ghost])])

    assert pages == []


def test_substance_examples_are_alphabetical_not_ranked() -> None:
    wines = [
        declaring(name="Zinfandel", additives=[SULFITES]),
        declaring(name="Amarone", additives=[SULFITES]),
    ]
    page = substance_pages(wines)[0]

    assert [w["name"] for w in page["examples"]] == ["Amarone", "Zinfandel"]


# --- pct ---------------------------------------------------------------------

def test_pct_uses_the_decimal_separator_of_the_language() -> None:
    assert pct(19.34, "sv") == "19,3"
    assert pct(19.34, "en") == "19.3"

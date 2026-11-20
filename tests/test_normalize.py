"""The fixtures are real declarations copied from systembolaget.se.

Each one has a hand-written expected result, so a change to the dictionary that
quietly breaks an existing wine shows up here.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from rapidfuzz import fuzz

from src.normalize import (
    FUZZY_MIN_LENGTH,
    FUZZY_THRESHOLD,
    _claim,
    load_lexicon,
    parse_ingredients,
)

FIXTURES = json.loads(
    (Path(__file__).parent / "fixtures" / "declarations.json").read_text(
        encoding="utf-8"
    )
)


def ids_of(items: list[dict]) -> list[str]:
    return sorted(item["id"] for item in items)


@pytest.mark.parametrize("case", FIXTURES, ids=[c["why"] for c in FIXTURES])
def test_declaration(case: dict) -> None:
    parsed = parse_ingredients(case["text"])

    assert ids_of(parsed.additives) == sorted(case["additives"])
    assert ids_of(parsed.gases) == sorted(case["gases"])
    assert ids_of(parsed.base_ingredients) == sorted(case["base"])
    assert parsed.additive_count == len(case["additives"])
    assert parsed.unknown_tokens == []
    assert parsed.status == "complete"

    if "processing" in case:
        assert ids_of(parsed.processing_notes) == sorted(case["processing"])
    if "allergens" in case:
        assert parsed.allergens == sorted(case["allergens"])


def test_every_sample_parses_cleanly() -> None:
    """The wider sample collected during research must leave no residue."""
    samples = json.loads(
        (Path(__file__).parent / "fixtures" / "raw_samples.json").read_text(
            encoding="utf-8"
        )
    )
    unresolved = {
        sample["ing"]: parse_ingredients(sample["ing"]).unknown_tokens
        for sample in samples
        if parse_ingredients(sample["ing"]).unknown_tokens
    }
    assert unresolved == {}


def test_unknown_text_is_flagged_not_guessed() -> None:
    parsed = parse_ingredients("Druvor, SULFITER, hemligt tillsatsmedel")
    assert parsed.status == "partial"
    assert "tillsatsmedel" in parsed.unknown_tokens
    assert ids_of(parsed.additives) == ["sulfites"]


def test_unrecognised_e_number_still_counts() -> None:
    parsed = parse_ingredients("Druvor, konserveringsmedel (E 999)")
    assert parsed.additive_count == 1
    assert parsed.additives[0]["e_number"] == "E999"
    # We know it is an additive even though we cannot name it, so the wine is
    # not marked partial.
    assert parsed.status == "complete"


def test_generic_sulfites_survive_alone() -> None:
    assert ids_of(parse_ingredients("Druvor, sulfiter").additives) == ["sulfites"]


def test_misspelling_is_matched_by_fuzz() -> None:
    parsed = parse_ingredients("Druvor, stabiliseringsmedel: karboximetylcellolusa")
    assert ids_of(parsed.additives) == ["carboxymethylcellulose"]
    assert parsed.fuzzy_matches


def test_named_grape_variety_is_not_unknown_text() -> None:
    text = "Muscat (druvor), socker, konserveringsmedel (SULFITER)"
    assert parse_ingredients(text).unknown_tokens == ["muscat"]
    # Given the variety list Systembolaget publishes for the wine, it reads.
    parsed = parse_ingredients(text, ["Muscat"])
    assert parsed.unknown_tokens == []
    assert ids_of(parsed.additives) == ["sulfites"]


def test_empty_declaration() -> None:
    parsed = parse_ingredients("")
    assert parsed.additive_count == 0
    assert parsed.status == "complete"


def test_every_alias_is_unique() -> None:
    """Two entries claiming the same alias would make counting arbitrary."""
    assert load_lexicon().alias_conflicts == []


def test_abbreviation_and_full_name_do_not_double_count() -> None:
    """An oenological abbreviation (KHT) next to the spelled-out name of the
    same substance must resolve to one additive, not two — real declaration
    from a wine that also names a fining agent by its trade name ("Gecoll
    Supra"), Laffort's liquid pork gelatin, confirmed against the
    manufacturer's own technical data sheet (laffort.com), so it reads as
    plain gelatin rather than staying unknown.
    """
    text = (
        "Vindruvor, Mjölkkasein, Isinglass, Gecoll Supra, Konserveringsmedel och "
        "antioxidanter (L askorbinsyra, CUS04 - Kopparsulfat), Stabiliseringsmedel "
        "(KHT - Kaliumbitartrat, KHC03 - Kaliumbikarbonat), Jästmedel (CX9 & DV10 - Jäst)"
    )
    parsed = parse_ingredients(text)
    ids = [additive["id"] for additive in parsed.additives]
    assert ids.count("potassium_bitartrate") == 1
    # The label says bikarbonat, so the dataset must say bikarbonat: E501 (ii),
    # not the E501 (i) carbonate it used to be folded into.
    assert ids.count("potassium_bicarbonate") == 1
    assert ids.count("potassium_carbonate") == 0
    assert ids.count("copper_sulfate") == 1
    assert ids.count("gelatin") == 1
    assert parsed.unknown_tokens == []
    assert parsed.status == "complete"


def test_isinglass_is_fish_by_origin_but_not_an_allergen() -> None:
    """Regulation (EU) No 1169/2011, Annex II point 4(b), exempts isinglass
    used as a fining agent in wine from the fish allergen. The declarations
    agree — the real one below capitalises the casein and albumin and not the
    isinglass — so fish must not appear among the allergens. It is still fish,
    and a reader avoiding animal products needs that, so it is the origin.
    """
    parsed = parse_ingredients(
        "Vindruvor, SVAVELDIOXID, Husbloss, Ärtprotein, MJÖLKKASEIN, ÄGGALBUMIN, Bentonit"
    )
    assert "fish" not in parsed.allergens
    assert parsed.allergens == ["egg", "milk", "sulfites"]
    assert parsed.origins == ["egg", "fish", "milk"]
    isinglass = next(a for a in parsed.additives if a["id"] == "isinglass")
    assert isinglass["origin"] == "fish"
    assert "allergen" not in isinglass


def test_gelatin_is_animal_by_origin() -> None:
    """Regulation (EC) No 853/2004, Annex I point 7.7: gelatine is obtained
    from the collagen of animals, so it always has an animal origin, but no
    declaration names the species and the origin does not guess one."""
    parsed = parse_ingredients("Druvor, Sulfiter, Gelatin")
    assert parsed.origins == ["animal"]
    assert "animal" not in parsed.allergens


def test_unresolved_wording_stays_unread() -> None:
    """Text nobody could establish must keep the wine partial, not be aliased away."""
    cases = {
        "Ekologiska druvor. Kaliumsyra. SULFITER": "kaliumsyra",
        "Druvor, Konserverings- och antioxidationsmedel (SULFITER). Industriell atmosfär": "industriell",
        "Vin, jordbruksalkohol, kryddor, mineraler, SULFITER": "mineraler",
        "Druvor, renad druvmustkoncentrat, konserveringsmedel (svaveldioxid)": "renad",
        "100% Chersegi": "chersegi",
    }
    for text, token in cases.items():
        parsed = parse_ingredients(text)
        assert parsed.status == "partial", text
        assert token in parsed.unknown_tokens, text


# --- the machinery, tested directly -----------------------------------------
# The fixtures above check outcomes. These check the mechanisms, so a
# regression inside them cannot hide behind a fixture set that happens not to
# exercise it.


def test_energy_per_100_ml_is_not_the_additive_e100() -> None:
    """A nutrition line reads "E/100 ml"; blanking the slash must not leave E100."""
    for text in ("Druvor, Energivärde: E/100 ml 70 kcal", "Druvor, Energi: E 100 ml"):
        parsed = parse_ingredients(text)
        assert parsed.additives == [], text
        assert parsed.unknown_e_numbers == [], text


def test_a_real_e100_is_still_read() -> None:
    """The lookahead only excludes "ml"; the same digits stand for the additive."""
    parsed = parse_ingredients("Färgämne E 100")
    assert ids_of(parsed.additives) == ["e100"]


@pytest.mark.parametrize(
    "text",
    ["Sulfiter, svaveldioxid", "svaveldioxid, Sulfiter"],
)
def test_a_specific_sulfite_replaces_the_generic_in_either_order(text: str) -> None:
    assert ids_of(parse_ingredients(text).additives) == ["sulfur_dioxide"]


def test_generic_sulfites_alone_are_not_dropped_by_the_dedup() -> None:
    assert ids_of(parse_ingredients("Sulfiter").additives) == ["sulfites"]


@pytest.mark.parametrize(
    ("text", "kept", "contained"),
    [
        ("Meta vinsyra", "metatartaric_acid", "tartaric_acid"),
        ("Caustic sulfite caramel", "caustic_sulphite_caramel", "sulfites"),
    ],
)
def test_the_longest_alias_wins_and_the_shorter_one_inside_it_stays_out(
    text: str, kept: str, contained: str
) -> None:
    parsed = parse_ingredients(text)
    assert ids_of(parsed.additives) == [kept]
    assert contained not in ids_of(parsed.additives)


def test_a_claimed_span_cannot_be_taken_again() -> None:
    spans = [False] * 10
    assert _claim(spans, 2, 6)
    assert not _claim(spans, 5, 8)  # overlaps the end of the first claim
    assert not _claim(spans, 0, 3)  # overlaps the start
    assert spans[6:] == [False] * 4  # a refused claim marks nothing
    assert _claim(spans, 6, 10)  # touching is not overlapping


def test_known_names_are_struck_out_before_the_dictionary_sees_them() -> None:
    """A grape named in the product data is claimed first, so no alias can take it."""
    parsed = parse_ingredients("Druvor, Vinsyra", known_names=["vinsyra"])
    assert parsed.additives == []


def test_fuzzy_accepts_a_slip_just_above_the_threshold_and_not_just_below() -> None:
    above, below = "lysozme", "lysozame"  # one letter dropped / one swapped
    assert fuzz.ratio(above, "lysozyme") >= FUZZY_THRESHOLD > fuzz.ratio(
        below, "lysozyme"
    ), "the fixture words no longer straddle FUZZY_THRESHOLD; pick new ones"

    matched = parse_ingredients(f"Druvor, {above}")
    assert ids_of(matched.additives) == ["lysozyme"]
    assert matched.fuzzy_matches == [(above, "lysozyme")]

    unmatched = parse_ingredients(f"Druvor, {below}")
    assert unmatched.additives == []
    assert unmatched.unknown_tokens == [below]


def test_fuzzy_ignores_tokens_shorter_than_the_minimum_even_when_they_score_high() -> None:
    short, long_ = "yest", "sufit"  # both one letter short of an alias
    assert len(short) < FUZZY_MIN_LENGTH <= len(long_)
    assert fuzz.ratio(short, "yeast") >= FUZZY_THRESHOLD, "the length rule is not what stops it"

    parsed = parse_ingredients(f"Druvor, {short}")
    assert parsed.unknown_tokens == [short]
    assert parsed.fuzzy_matches == []

    assert parse_ingredients(f"Druvor, {long_}").fuzzy_matches == [(long_, "sulfit")]


def test_fuzzy_matches_are_part_of_the_record() -> None:
    output = parse_ingredients("Druvor, lysozme").as_output()
    assert output["fuzzy_matches"] == [{"token": "lysozme", "alias": "lysozyme"}]
    assert parse_ingredients("Druvor, SULFITER").as_output()["fuzzy_matches"] == []

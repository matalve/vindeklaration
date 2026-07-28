"""The fixtures are real declarations copied from systembolaget.se.

Each one has a hand-written expected result, so a change to the dictionary that
quietly breaks an existing wine shows up here.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from src.normalize import load_lexicon, parse_ingredients

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
    from a wine that also names a fining agent by an unverifiable trade name
    ("Gecoll Supra"), which is why it stays partial rather than complete.
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
    assert set(parsed.unknown_tokens) == {"gecoll", "supra"}
    assert parsed.status == "partial"

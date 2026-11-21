"""The sightings record: when each wine was found, and how long absences last."""

from __future__ import annotations

import json
from datetime import date, timedelta

import pytest

from src import catalog, report, seen

D0 = date(2026, 11, 21)


def night(n: int) -> date:
    return D0 + timedelta(days=n)


def product(number: str, assortment: str | None = "Ordervaror") -> dict:
    return {"productNumber": number, "assortmentText": assortment}


def sweep(state: dict, day: int, *numbers: str, assortment: str | None = "Ordervaror") -> None:
    seen.update(state, [product(n, assortment) for n in numbers], night(day))


def test_a_first_sweep_records_every_wine_as_new() -> None:
    state = seen.empty()
    sweep(state, 0, "1", "2")

    assert state["tracking_since"] == "2026-11-21"
    assert state["sweeps"] == ["2026-11-21"]
    assert state["products"]["1"] == {
        "first_seen": "2026-11-21",
        "last_seen": "2026-11-21",
        "assortment": "Ordervaror",
        "returns": [],
    }


def test_a_wine_seen_every_night_never_has_a_return() -> None:
    state = seen.empty()
    for day in range(4):
        sweep(state, day, "1")

    entry = state["products"]["1"]
    assert entry["first_seen"] == "2026-11-21"
    assert entry["last_seen"] == "2026-11-24"
    assert entry["returns"] == []


def test_a_wine_missed_for_one_night_returns_after_one() -> None:
    state = seen.empty()
    sweep(state, 0, "1", "2")
    sweep(state, 1, "2")  # "1" is missed
    sweep(state, 2, "1", "2")

    assert state["products"]["1"]["returns"] == [{"on": "2026-11-23", "nights": 1}]
    assert state["products"]["2"]["returns"] == []


def test_the_length_of_an_absence_counts_sweeps_not_calendar_days() -> None:
    """The crawler was off on night 2. Nothing was swept, so nothing was missed."""
    state = seen.empty()
    sweep(state, 0, "1")
    sweep(state, 1, "2")  # "1" missed: one sweep ran without it
    sweep(state, 3, "1", "2")  # night 2 never ran

    assert state["products"]["1"]["returns"] == [{"on": "2026-11-24", "nights": 1}]


def test_sweeping_twice_on_the_same_day_changes_nothing_more() -> None:
    state = seen.empty()
    sweep(state, 0, "1", "2")
    sweep(state, 1, "1", "2")
    sweep(state, 1, "1")  # a second, thinner run the same day

    assert state["sweeps"] == ["2026-11-21", "2026-11-22"]
    assert state["products"]["2"]["returns"] == []
    assert state["products"]["2"]["last_seen"] == "2026-11-22"


def test_a_sweep_dated_before_the_last_sighting_does_not_move_it_back() -> None:
    """A clock that jumps backwards must not rewrite when a wine was last seen."""
    state = seen.empty()
    sweep(state, 2, "1")
    sweep(state, 1, "1")

    assert state["products"]["1"]["last_seen"] == "2026-11-23"
    assert state["products"]["1"]["returns"] == []


def test_only_the_latest_returns_are_kept() -> None:
    state = seen.empty()
    for round_ in range(seen.MAX_RETURNS + 3):
        sweep(state, round_ * 2, "1")
        sweep(state, round_ * 2 + 1, "2")  # "1" misses every other night

    assert len(state["products"]["1"]["returns"]) == seen.MAX_RETURNS


def test_a_wine_unseen_beyond_the_retention_is_forgotten() -> None:
    state = seen.empty()
    sweep(state, 0, "1", "2")
    sweep(state, seen.RETENTION_DAYS + 1, "2")

    assert "1" not in state["products"]
    assert "2" in state["products"]
    assert state["sweeps"] == [night(seen.RETENTION_DAYS + 1).isoformat()]


def test_the_assortment_follows_the_latest_sighting_and_survives_a_blank() -> None:
    state = seen.empty()
    sweep(state, 0, "1", assortment="Ordervaror")
    sweep(state, 1, "1", assortment="Fast sortiment")
    sweep(state, 2, "1", assortment=None)

    assert state["products"]["1"]["assortment"] == "Fast sortiment"


# --- what the record says ----------------------------------------------------


def test_summary_of_nothing_is_empty() -> None:
    assert seen.summary(seen.empty()) == {}


def test_summary_separates_recent_absences_by_how_long_they_have_lasted() -> None:
    state = seen.empty()
    sweep(state, 0, "1", "2", "3", "4")
    sweep(state, 1, "2", "3", "4")  # "1" missing
    sweep(state, 2, "3", "4")  # "1" missing 2 nights, "2" missing 1
    sweep(state, 3, "4")  # "1": 3, "2": 2, "3": 1

    facts = seen.summary(state)
    assert facts["found"] == 1
    assert facts["absent_now_total"] == 3
    assert facts["absent_now"] == {"1 night": 1, "2 nights": 1, "3-7 nights": 1}


def test_summary_counts_the_long_gone_apart_from_the_recent() -> None:
    state = seen.empty()
    sweep(state, 0, "1", "2")
    for day in range(1, seen.RECENT_DAYS + 3):
        sweep(state, day, "2")  # "1" is last seen long before the horizon

    facts = seen.summary(state)
    assert facts["gone_longer"] == 1
    assert facts["absent_now_total"] == 0


def test_summary_groups_ended_absences_by_length() -> None:
    state = seen.empty()
    sweep(state, 0, "1", "2", "3")
    sweep(state, 1, "3")  # "1" and "2" missing
    sweep(state, 2, "1", "3")  # "1" back after 1; "2" still missing
    sweep(state, 3, "1", "2", "3")  # "2" back after 2

    facts = seen.summary(state)
    assert facts["returned"] == {"1 night": 1, "2 nights": 1}
    assert facts["returned_total"] == 2


def test_summary_reports_the_assortment_of_the_missing() -> None:
    state = seen.empty()
    sweep(state, 0, "1", "2", assortment="Ordervaror")
    sweep(state, 0, "3", assortment="Fast sortiment")
    sweep(state, 1, "9")

    assert seen.summary(state)["by_assortment"] == {"Ordervaror": 2, "Fast sortiment": 1}


def test_the_printout_says_when_there_is_too_little_to_read(capsys) -> None:
    state = seen.empty()
    sweep(state, 0, "1")
    seen.print_summary(state)

    out = capsys.readouterr().out
    assert "Too early to read" in out


def test_the_printout_before_any_tracking_says_so(capsys) -> None:
    seen.print_summary(seen.empty())
    assert "not tracked yet" in capsys.readouterr().out


# --- the file ----------------------------------------------------------------


def test_the_record_survives_a_round_trip(tmp_path) -> None:
    path = tmp_path / "seen.json"
    seen.record([product("1")], today=night(0), path=path)
    seen.record([product("2")], today=night(1), path=path)

    state = seen.load(path)
    assert state["sweeps"] == ["2026-11-21", "2026-11-22"]
    assert state["products"]["1"]["returns"] == []
    assert state["products"]["2"]["first_seen"] == "2026-11-22"
    assert not list(tmp_path.glob("*.tmp"))


def test_an_unreadable_record_is_set_aside_not_overwritten(tmp_path, capsys) -> None:
    path = tmp_path / "seen.json"
    path.write_text("{ not json", encoding="utf-8")

    seen.record([product("1")], today=night(0), path=path)

    assert (tmp_path / "seen.json.unreadable").read_text(encoding="utf-8") == "{ not json"
    assert seen.load(path)["products"].keys() == {"1"}
    assert "unreadable" in capsys.readouterr().err


def test_a_reader_leaves_an_unreadable_record_where_it_is(tmp_path) -> None:
    path = tmp_path / "seen.json"
    path.write_text("[]", encoding="utf-8")

    assert seen.load(path, quarantine=False) == seen.empty()
    assert path.read_text(encoding="utf-8") == "[]"


# --- where it is wired in ----------------------------------------------------


@pytest.fixture
def sweep_once(monkeypatch, tmp_path):
    monkeypatch.setattr(catalog, "DATA_DIR", tmp_path)
    monkeypatch.setattr(catalog, "CATALOG_PATH", tmp_path / "catalog.json")
    monkeypatch.setattr(seen, "SEEN_PATH", tmp_path / "catalog-seen.json")
    monkeypatch.setattr("sys.argv", ["catalog"])

    def run(products: list[dict]) -> None:
        monkeypatch.setattr(catalog, "fetch_catalog", lambda category="Vin": products)
        catalog.main()

    return run


def test_the_nightly_sweep_records_what_it_found(sweep_once, tmp_path) -> None:
    sweep_once([product("1"), product("2")])

    state = json.loads((tmp_path / "catalog-seen.json").read_text(encoding="utf-8"))
    assert set(state["products"]) == {"1", "2"}
    assert len(json.loads((tmp_path / "catalog.json").read_text(encoding="utf-8"))) == 2


def test_a_failure_to_record_never_costs_the_sweep(monkeypatch, sweep_once, tmp_path, capsys) -> None:
    def broken(*args, **kwargs):
        raise OSError("disk full")

    monkeypatch.setattr(seen, "record", broken)
    sweep_once([product("1")])  # no exception

    assert (tmp_path / "catalog.json").exists()
    assert "could not record the sightings" in capsys.readouterr().err


def test_the_report_shows_the_sightings(monkeypatch, tmp_path, capsys) -> None:
    seen_path = tmp_path / "catalog-seen.json"
    seen.record([product("1"), product("2")], today=night(0), path=seen_path)
    seen.record([product("2")], today=night(1), path=seen_path)
    monkeypatch.setattr(seen, "SEEN_PATH", seen_path)
    monkeypatch.setattr(report, "WINES_PATH", tmp_path / "wines.json")
    monkeypatch.setattr(report, "UNKNOWN_PATH", tmp_path / "unknown.json")
    monkeypatch.setattr(report, "HISTORY_PATH", tmp_path / "history.json")
    (tmp_path / "wines.json").write_text(json.dumps({"wines": []}))
    monkeypatch.setattr("sys.argv", ["report"])

    with pytest.raises(SystemExit):
        report.main()

    out = capsys.readouterr().out
    assert "Catalog sightings" in out
    assert "seen in the last 7 days: 1" in out

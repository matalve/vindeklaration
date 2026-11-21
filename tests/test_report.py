"""The quality gate in src.report: a jump and a creep must both be caught."""

import json

import pytest

from src import report
from src.report import ROLLING_WINDOW, check_gate


def run(rate, day=1):
    return {"date": f"2026-01-{day:02d}", "partial_rate": rate}


def history(*rates):
    return [run(rate, day) for day, rate in enumerate(rates, start=1)]


def test_the_first_run_is_a_baseline_and_passes(capsys):
    assert check_gate(run(0.05), [])
    assert "BASELINE" in capsys.readouterr().out


def test_a_jump_since_the_last_run_fails(capsys):
    assert not check_gate(run(0.031), history(0.02))
    assert "FAIL" in capsys.readouterr().out


def test_a_fall_always_passes():
    assert check_gate(run(0.01), history(0.04, 0.04))


def test_a_slow_creep_that_never_jumps_fails_against_the_recent_best(capsys):
    # +0.1 points a night: every step is a tenth of the run-over-run limit.
    rates = [0.020 + 0.001 * i for i in range(ROLLING_WINDOW)]
    assert not check_gate(run(rates[-1] + 0.001), history(*rates))
    out = capsys.readouterr().out
    assert "best of the last" in out and "No single night moved far" in out


def test_a_share_that_has_sat_still_passes():
    assert check_gate(run(0.04), history(*[0.04] * 10))


def test_a_climb_inside_the_limit_passes():
    assert check_gate(run(0.029), history(0.02, 0.022, 0.025))


def test_the_baseline_is_the_best_run_in_the_window_not_the_oldest(capsys):
    # A bad stretch long ago has left the window; only the last 30 count.
    old = [0.001] * 5
    recent = [0.030] * ROLLING_WINDOW
    assert check_gate(run(0.030), history(*old, *recent))


def test_one_recorded_run_is_compared_once_not_twice(capsys):
    check_gate(run(0.02), history(0.02))
    assert "best of the last" not in capsys.readouterr().out


# --- what the report reads ----------------------------------------------------


def wine(number, unknown=(), fuzzy=(), raw="Druvor, SULFITER", status=None):
    """The fields main() uses, as the build would have stored them."""
    return {
        "product_number": number,
        "name": f"Wine {number}",
        "declaration_status": "declared",
        "parse_status": status or ("partial" if unknown else "complete"),
        "raw_ingredients": raw,
        "unknown_tokens": list(unknown),
        "fuzzy_matches": [{"token": t, "alias": a} for t, a in fuzzy],
        "additives": [],
        "additive_count": 0,
        "price": 100,
        "vintage": "2024",
        "country": "Frankrike",
        "assortment": "Fast sortiment",
        "source_url": f"https://example.invalid/{number}",
    }


@pytest.fixture
def run_report(monkeypatch, tmp_path):
    def run(wines):
        monkeypatch.setattr(report, "WINES_PATH", tmp_path / "wines.json")
        monkeypatch.setattr(report, "UNKNOWN_PATH", tmp_path / "unknown.json")
        monkeypatch.setattr(report, "HISTORY_PATH", tmp_path / "history.json")
        (tmp_path / "wines.json").write_text(json.dumps({"wines": wines}))
        monkeypatch.setattr("sys.argv", ["report"])
        with pytest.raises(SystemExit) as raised:
            report.main()
        assert raised.value.code == 0
        return json.loads((tmp_path / "unknown.json").read_text())

    return run


def test_the_report_lists_the_unknown_tokens_the_build_stored(run_report):
    result = run_report(
        [wine("1", unknown=["tillsatsx"]), wine("2", unknown=["tillsatsx", "yy"]), wine("3")]
    )
    assert result["unknown_tokens"] == [
        {"token": "tillsatsx", "wines": 2, "example": "https://example.invalid/1"},
        {"token": "yy", "wines": 1, "example": "https://example.invalid/2"},
    ]


def test_the_report_describes_the_stored_dataset_not_the_lexicon_of_the_day(run_report):
    """The raw text parses cleanly today, but the stored record says it did not
    when the dataset was built. The report must follow the record."""
    result = run_report([wine("1", unknown=["stored-only"], raw="Druvor, SULFITER")])
    assert [t["token"] for t in result["unknown_tokens"]] == ["stored-only"]


def test_stored_spelling_suggestions_are_counted_per_match(run_report):
    result = run_report(
        [
            wine("1", unknown=["lysozme"], fuzzy=[("lysozme", "lysozyme")]),
            wine("2", unknown=["lysozme"], fuzzy=[("lysozme", "lysozyme")]),
            wine("3", unknown=["sufit"], fuzzy=[("sufit", "sulfit")]),
        ]
    )
    assert result["fuzzy_matches"] == [
        {"match": "lysozme -> lysozyme", "wines": 2},
        {"match": "sufit -> sulfit", "wines": 1},
    ]


def test_a_dataset_built_before_fuzzy_matches_was_stored_is_refused(
    monkeypatch, tmp_path
):
    stale = wine("1")
    del stale["fuzzy_matches"]
    monkeypatch.setattr(report, "WINES_PATH", tmp_path / "wines.json")
    (tmp_path / "wines.json").write_text(json.dumps({"wines": [stale]}))
    monkeypatch.setattr("sys.argv", ["report"])
    with pytest.raises(SystemExit) as raised:
        report.main()
    assert "src.build" in str(raised.value)


def test_the_report_no_longer_parses_declarations_itself():
    assert not hasattr(report, "parse_ingredients")

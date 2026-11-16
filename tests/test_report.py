"""The quality gate in src.report: a jump and a creep must both be caught."""

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

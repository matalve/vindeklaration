"""The buildId guard in src.details, tested against a fake Systembolaget.

The failure this protects against is silent: when the buildId in the data-route
URL goes stale mid-run, every remaining request answers 404, and a 404 means
"product gone". These tests deploy the fake site mid-pass and check that the
products come back rather than being written off.
"""

import json
import os
from datetime import datetime, timedelta, timezone

import pytest

from src import details as details_module
from src.details import discover_build_id, fetch_details


class FakeSite:
    """Answers the two requests details.py makes, and can deploy mid-run."""

    def __init__(self, live, build_id="build-one", deploy_after=None):
        self.live = set(live)
        self.build_id = build_id
        self.deploy_after = deploy_after
        self.data_requests = 0
        self.page_requests = 0

    def get_json(self, http, url):
        self.data_requests += 1
        if self.deploy_after is not None and self.data_requests > self.deploy_after:
            self.build_id = "build-two"
            self.deploy_after = None
        _, _, rest = url.partition("/_next/data/")
        build_id, _, path = rest.partition("/")
        number = path.rsplit("x-", 1)[1].removesuffix(".json")
        if build_id != self.build_id or number not in self.live:
            return None
        return {
            "pageProps": {
                "fallback": {
                    f'@"api","ecommerce","product","{number}",': {
                        "productNumber": number,
                        "ingredients": "Druvor, konserveringsmedel (sulfiter)",
                    }
                }
            }
        }

    def get_text(self, http, url):
        self.page_requests += 1
        return '{"buildId":"%s","other":1}' % self.build_id


@pytest.fixture
def site(monkeypatch, tmp_path):
    """Wire a fake site into details.py, with a throwaway cache and no waiting."""

    def install(fake):
        monkeypatch.setattr(details_module, "get_json", fake.get_json)
        monkeypatch.setattr(details_module, "get_text", fake.get_text)
        monkeypatch.setattr(details_module, "CACHE_DIR", tmp_path)
        monkeypatch.setattr(details_module.time, "sleep", lambda _: None)
        return fake

    return install


def numbers(count, start=100000):
    return [str(start + i) for i in range(count)]


def test_a_deploy_mid_run_does_not_turn_the_assortment_into_gone_products(site):
    todo = numbers(40)
    fake = site(FakeSite(live=todo, deploy_after=5))

    result = fetch_details(None, "build-one", todo)

    assert result["missing"] == 0
    assert result["fetched"] == 40
    assert result["build_id"] == "build-two"
    assert result["rediscoveries"] == 1


def test_products_read_as_gone_after_a_deploy_are_written_to_the_cache(site, tmp_path):
    todo = numbers(30)
    site(FakeSite(live=todo, deploy_after=2))

    fetch_details(None, "build-one", todo)

    assert sorted(p.stem for p in tmp_path.glob("*.json")) == sorted(todo)


def test_a_product_that_really_left_the_assortment_is_counted_gone(site):
    todo = numbers(30)
    site(FakeSite(live=[n for n in todo if n != todo[10]]))

    result = fetch_details(None, "build-one", todo)

    assert result["missing"] == 1
    assert result["fetched"] == 29
    # One miss, then a success right after: the buildId proved itself without
    # anyone having to ask for it.
    assert result["rediscoveries"] == 0


def test_a_long_run_of_real_misses_costs_fewer_and_fewer_extra_requests(site):
    # Forty gone in a row against an unchanged buildId. The streak limit
    # doubles each time re-discovery confirms it: 10, then 20, then the tail.
    todo = numbers(40)
    fake = site(FakeSite(live=[]))

    result = fetch_details(None, "build-one", todo)

    assert result["missing"] == 40
    assert result["fetched"] == 0
    assert result["rediscoveries"] == 3
    assert fake.page_requests == 3


def test_a_deploy_in_the_last_few_products_is_still_caught(site):
    # The tail never reaches the streak limit, so without an end-of-run check
    # these three would be recorded as gone.
    todo = numbers(20)
    fake = site(FakeSite(live=todo, deploy_after=17))

    result = fetch_details(None, "build-one", todo)

    assert result["missing"] == 0
    assert result["fetched"] == 20
    assert fake.page_requests == 1


def test_discovery_moves_on_when_a_candidate_product_has_left_the_shelf(
    monkeypatch,
):
    asked = []

    def get_text(http, url):
        asked.append(url)
        if "x-253108" in url:
            raise RuntimeError("giving up on the page: 404")
        return '{"buildId":"build-nine"}'

    monkeypatch.setattr(details_module, "get_text", get_text)

    assert discover_build_id(None, ["253108", "257101"]) == "build-nine"
    assert len(asked) == 2


def test_discovery_says_which_candidates_it_tried_before_giving_up(monkeypatch):
    def get_text(http, url):
        return "<html>a product page with no buildId in it</html>"

    monkeypatch.setattr(details_module, "get_text", get_text)

    with pytest.raises(RuntimeError) as raised:
        discover_build_id(None, ["253108", "257101"])
    assert "253108" in str(raised.value)
    assert "257101" in str(raised.value)


def test_a_run_that_mostly_fails_stops_the_pipeline_instead_of_reporting_it(
    monkeypatch, tmp_path, capsys
):
    todo = numbers(50)
    monkeypatch.setattr(details_module, "CACHE_DIR", tmp_path)
    monkeypatch.setattr(details_module, "client", lambda **kw: _no_client())
    monkeypatch.setattr(details_module, "discover_build_id", lambda http: "build-one")
    monkeypatch.setattr(
        details_module,
        "fetch_details",
        lambda http, build_id, todo: {
            "build_id": build_id,
            "fetched": len(todo) - 10,
            "declared": 0,
            "missing": 10,
            "rediscoveries": 1,
        },
    )
    monkeypatch.setattr("sys.argv", ["details", "--only", *todo])

    with pytest.raises(SystemExit) as raised:
        details_module.main()
    assert raised.value.code == 1
    assert "FAILED" in capsys.readouterr().err


def test_a_handful_of_gone_products_in_a_small_run_is_not_a_failure(
    monkeypatch, tmp_path
):
    # Below MISSING_SHARE_MIN_SAMPLE a share means nothing, so `--only` runs
    # are never judged by it however badly they go.
    todo = numbers(5)
    monkeypatch.setattr(details_module, "CACHE_DIR", tmp_path)
    monkeypatch.setattr(details_module, "client", lambda **kw: _no_client())
    monkeypatch.setattr(details_module, "discover_build_id", lambda http: "build-one")
    monkeypatch.setattr(
        details_module,
        "fetch_details",
        lambda http, build_id, todo: {
            "build_id": build_id,
            "fetched": 0,
            "declared": 0,
            "missing": len(todo),
            "rediscoveries": 1,
        },
    )
    monkeypatch.setattr("sys.argv", ["details", "--only", *todo])

    details_module.main()  # no SystemExit


class _no_client:
    """Stands in for httpx.Client as a context manager; never asked for anything."""

    def __enter__(self):
        return None

    def __exit__(self, *exc):
        return False


# --- choosing what to fetch -------------------------------------------------

NOW = datetime(2026, 9, 9, 3, 0, tzinfo=timezone.utc)


@pytest.fixture
def cache(monkeypatch, tmp_path):
    """A throwaway cache, with a helper that writes a record of a given age."""
    monkeypatch.setattr(details_module, "CACHE_DIR", tmp_path)

    def write(number, *, days_old=0.0, fetched_at=None):
        if fetched_at is None:
            fetched_at = (NOW - timedelta(days=days_old)).isoformat()
        record = {"productNumber": number, "ingredients": "Druvor"}
        if fetched_at is not False:
            record["fetched_at"] = fetched_at
        (tmp_path / f"{number}.json").write_text(json.dumps(record), encoding="utf-8")
        return tmp_path / f"{number}.json"

    write.dir = tmp_path
    return write


def test_a_product_that_was_never_cached_is_fetched(cache):
    todo, counts = details_module.select_products(["100001"], now=NOW)

    assert todo == ["100001"]
    assert counts == {"new": 1, "stale": 0}


def test_a_recently_cached_product_is_left_alone(cache):
    cache("100001", days_old=2)

    todo, counts = details_module.select_products(["100001"], now=NOW)

    assert todo == []
    assert counts == {"new": 0, "stale": 0}


def test_a_product_that_missed_a_refresh_is_fetched_again(cache):
    # The case this exists for: absent from the catalog on refresh night, back
    # on an ordinary one, so presence alone would skip it forever.
    cache("100001", days_old=17)

    todo, counts = details_module.select_products(["100001"], now=NOW)

    assert todo == ["100001"]
    assert counts == {"new": 0, "stale": 1}


def test_the_boundary_is_the_refresh_cycle_not_the_week(cache):
    cache("100001", days_old=7.5)
    cache("100002", days_old=8.5)

    todo, _ = details_module.select_products(["100001", "100002"], now=NOW)

    assert todo == ["100002"]


def test_a_record_with_no_usable_timestamp_is_not_taken_as_fresh(cache):
    cache("100001", fetched_at=False)
    cache("100002", fetched_at="not a date")
    (cache.dir / "100003.json").write_text("{ truncated", encoding="utf-8")

    todo, _ = details_module.select_products(
        ["100001", "100002", "100003"], now=NOW
    )

    assert todo == ["100001", "100002", "100003"]


def test_age_comes_from_the_record_not_the_file(cache):
    # deploy/rebuild-cache.py rewrites every file, so every mtime would say
    # "fetched just now". The record knows better.
    path = cache("100001", days_old=17)
    os.utime(path, (NOW.timestamp(), NOW.timestamp()))

    todo, counts = details_module.select_products(["100001"], now=NOW)

    assert todo == ["100001"]
    assert counts["stale"] == 1


def test_refresh_takes_everything_regardless_of_age(cache):
    cache("100001", days_old=0)
    cache("100002", days_old=17)

    todo, counts = details_module.select_products(
        ["100001", "100002", "100003"], refresh=True, now=NOW
    )

    assert todo == ["100001", "100002", "100003"]
    assert counts == {"new": 3, "stale": 0}


def _run_main(monkeypatch, tmp_path, todo, result):
    monkeypatch.setattr(details_module, "CACHE_DIR", tmp_path)
    monkeypatch.setattr(details_module, "client", lambda **kw: _no_client())
    monkeypatch.setattr(details_module, "discover_build_id", lambda http: "build-one")
    monkeypatch.setattr(
        details_module, "fetch_details", lambda http, build_id, todo: result
    )
    monkeypatch.setattr("sys.argv", ["details", "--only", *todo])
    details_module.main()


def test_a_buildId_that_moved_mid_run_leaves_a_trace_in_the_log(
    monkeypatch, tmp_path, capsys
):
    # The guard is rare by design, so the run has to say when it fired —
    # otherwise there is no way to tell it working from it being dead code.
    _run_main(
        monkeypatch,
        tmp_path,
        numbers(3),
        {
            "build_id": "build-two",
            "fetched": 3,
            "declared": 0,
            "missing": 0,
            "rediscoveries": 2,
        },
    )

    out = capsys.readouterr().out
    assert "buildId re-checked 2x" in out
    assert "it had moved" in out


def test_an_ordinary_night_says_nothing_about_the_buildId(
    monkeypatch, tmp_path, capsys
):
    _run_main(
        monkeypatch,
        tmp_path,
        numbers(3),
        {
            "build_id": "build-one",
            "fetched": 3,
            "declared": 0,
            "missing": 0,
            "rediscoveries": 0,
        },
    )

    assert "re-checked" not in capsys.readouterr().out

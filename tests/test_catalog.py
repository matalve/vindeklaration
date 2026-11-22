"""The catalog sweep: a stable sort order, and a second pass only when needed."""

from __future__ import annotations

import urllib.parse

import pytest

from src import catalog


class FakeSearch:
    """Serves a fixed set of wines per (country, sort direction), 30 a page.

    `served` maps a direction to the product numbers that direction's paging
    delivers, which is how the real API loses wines: the doc count is right,
    the pages are not."""

    def __init__(self, doc_count: int, served: dict[str, list[str]], country: str = "Tjeckien"):
        self.doc_count = doc_count
        self.served = served
        self.country = country
        self.queries: list[dict[str, str]] = []

    def __call__(self, http, url: str) -> dict:
        query = dict(urllib.parse.parse_qsl(urllib.parse.urlsplit(url).query))
        self.queries.append(query)
        page = int(query["page"])
        if "country" not in query:
            # The unfiltered first pass: it only has to name the partitions.
            products = [{"productNumber": "first", "country": self.country, "categoryLevel2": "Rött vin"}]
            return {"products": products if page == 1 else [], "metadata": {"docCount": self.doc_count, "nextPage": -1}}
        numbers = self.served[query.get("sortDirection", "none")]
        rows = numbers[(page - 1) * 30 : page * 30]
        more = page * 30 < len(numbers)
        return {
            "products": [{"productNumber": n, "country": self.country} for n in rows],
            "metadata": {"docCount": self.doc_count, "nextPage": page + 1 if more else -1},
        }


@pytest.fixture
def search(monkeypatch):
    monkeypatch.setattr(catalog.time, "sleep", lambda seconds: None)

    def install(fake: FakeSearch) -> FakeSearch:
        monkeypatch.setattr(catalog, "get_json", fake)
        return fake

    return install


def numbers(start: int, stop: int) -> list[str]:
    return [str(n) for n in range(start, stop)]


def test_every_partition_query_is_sorted(search) -> None:
    fake = search(FakeSearch(70, {"Ascending": numbers(0, 70)}))

    catalog.sweep_partition(None, {"categoryLevel1": "Vin", "country": "Tjeckien"}, {})

    assert fake.queries and all(q["sortBy"] == "Name" for q in fake.queries)


def test_a_complete_first_pass_needs_no_second(search) -> None:
    fake = search(FakeSearch(70, {"Ascending": numbers(0, 70)}))

    assert catalog.sweep_partition(None, {"country": "Tjeckien"}, {}) == (70, 70)
    assert {q["sortDirection"] for q in fake.queries} == {"Ascending"}


def test_a_short_first_pass_is_completed_by_the_other_direction(search) -> None:
    # Each direction repeats ten wines where it should have served ten others,
    # and the two lose different ones — the pattern measured on France.
    ascending = numbers(0, 60) + numbers(50, 60)
    descending = numbers(10, 70) + numbers(10, 20)
    search(FakeSearch(70, {"Ascending": ascending, "Descending": descending}))
    into: dict[str, dict] = {}

    assert catalog.sweep_partition(None, {"country": "Tjeckien"}, into) == (70, 70)
    assert set(into) == set(numbers(0, 70))


def test_a_partition_past_the_window_gets_no_second_pass(search, monkeypatch) -> None:
    monkeypatch.setattr(catalog, "WINDOW_LIMIT", 50)
    fake = search(FakeSearch(70, {"Ascending": numbers(0, 40), "Descending": numbers(30, 70)}))

    catalog.sweep_partition(None, {"country": "Tjeckien"}, {})

    assert {q["sortDirection"] for q in fake.queries} == {"Ascending"}


def test_the_sweep_accounts_for_what_it_could_not_reach(search, monkeypatch) -> None:
    monkeypatch.setattr(catalog, "client", lambda **kwargs: _Null())
    # Both directions lose the same two wines: they stay unreached.
    search(FakeSearch(70, {"Ascending": numbers(0, 68) + ["0", "1"], "Descending": numbers(0, 68)}))

    products, account = catalog.fetch_catalog()

    # The partition stays two short; the unfiltered first pass found one wine
    # of its own, so the catalog as a whole is one short.
    assert len(products) == 69
    assert account == {"reported": 70, "found": 69, "unreached": 1, "short": {"Tjeckien": 2}}


class _Null:
    def __enter__(self):
        return None

    def __exit__(self, *exc):
        return False

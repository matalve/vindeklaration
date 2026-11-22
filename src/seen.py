"""Which wines the nightly catalog sweep found, and on which nights.

A wine missing from tonight's catalog has either left the assortment or been
missed by the sweep, and the catalog alone cannot say which. The sweep reports
200-490 wines it could not reach every night, and about half of the wines that
vanish in a month come back, so the two readings matter: a wine absent for one
night looks like a sweep gap, one absent for weeks looks delisted.

This module only records. It changes nothing in the dataset or on the site;
`src.report` reads it to show how long the absences last, so that a decision
about what the site should say can rest on that instead of on a guess.

The file is the crawler's own, like data/cache: gitignored, written by the
nightly sweep, never reconciled downward. Lose it and the record starts over;
nothing else depends on it.

Alongside the sightings it keeps each sweep's own account of its gap — the
upstream total, how many wines were found, and which partitions came up short
(`accounts`, keyed by night). The catalog's printout used to be the only place
that number existed.
"""

from __future__ import annotations

import json
import os
import sys
import tempfile
from collections import Counter
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
SEEN_PATH = DATA_DIR / "catalog-seen.json"

# Longer than the longest absence worth distinguishing, short enough that the
# file stays a couple of megabytes. A wine unseen for this long is dropped and
# would count as new if it ever came back.
RETENTION_DAYS = 120
# "Missing tonight" means seen within this many days before the latest sweep.
RECENT_DAYS = 7
# Completed absences kept per wine; a wine that flickers does so repeatedly.
MAX_RETURNS = 10
# How many recent sweeps the printout ranges the gap over.
GAP_WINDOW = 14

# How long an absence lasted, in nights swept: (lowest, highest, label).
BUCKETS = (
    (1, 1, "1 night"),
    (2, 2, "2 nights"),
    (3, RECENT_DAYS, f"3-{RECENT_DAYS} nights"),
    (RECENT_DAYS + 1, None, f"{RECENT_DAYS + 1}+ nights"),
)


def empty() -> dict:
    return {"tracking_since": None, "sweeps": [], "products": {}, "accounts": {}}


def load(path: Path | None = None, *, quarantine: bool = True) -> dict:
    """Read the record. One that cannot be read is set aside, never overwritten.

    `quarantine=False` is for readers: they get an empty record and a warning
    but leave the file where it is.
    """
    path = path or SEEN_PATH
    if not path.exists():
        return empty()
    try:
        state = json.loads(path.read_text(encoding="utf-8"))
        if (
            not isinstance(state, dict)
            or not isinstance(state.get("products"), dict)
            or not isinstance(state.get("sweeps"), list)
        ):
            raise ValueError("not a sightings record")
        state.setdefault("tracking_since", None)
        if not isinstance(state.get("accounts"), dict):
            state["accounts"] = {}
        return state
    except (ValueError, OSError) as error:
        if quarantine:
            aside = path.with_name(path.name + ".unreadable")
            os.replace(path, aside)
            print(
                f"warning: {path.name} was unreadable ({error}); kept as "
                f"{aside.name} and started over",
                file=sys.stderr,
            )
        else:
            print(f"warning: {path.name} is unreadable ({error})", file=sys.stderr)
        return empty()


def save(state: dict, path: Path | None = None) -> None:
    """Write through a temporary file, so a killed run cannot leave half a record."""
    path = path or SEEN_PATH
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=path.parent, prefix=path.name + ".", suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            json.dump(state, handle, ensure_ascii=False, separators=(",", ":"))
        os.replace(tmp, path)
    except BaseException:
        Path(tmp).unlink(missing_ok=True)
        raise


def update(
    state: dict, products: list[dict], today: date, sweep: dict | None = None
) -> None:
    """Record one sweep. Running it twice on the same day changes nothing more.

    `sweep` is the catalog's account of what it could not reach; a second run
    on the same day replaces the first one's, since it describes the newer
    catalog."""
    day = today.isoformat()
    accounts = state.setdefault("accounts", {})
    if sweep is not None:
        accounts[day] = sweep
    sweeps = state["sweeps"]
    if day not in sweeps:
        sweeps.append(day)
        sweeps.sort()
    if state["tracking_since"] is None:
        state["tracking_since"] = day

    entries = state["products"]
    for product in products:
        number = product.get("productNumber")
        if not number:
            continue
        entry = entries.get(number)
        if entry is None:
            entry = entries[number] = {
                "first_seen": day,
                "last_seen": day,
                "assortment": None,
                "returns": [],
            }
        elif entry["last_seen"] < day:
            # Count the sweeps that actually ran in between, not the calendar
            # days: a night the crawler was off says nothing about the wine.
            missed = sum(1 for sweep in sweeps if entry["last_seen"] < sweep < day)
            if missed:
                returned = {"on": day, "nights": missed}
                entry["returns"] = (entry["returns"] + [returned])[-MAX_RETURNS:]
            entry["last_seen"] = day
        entry["assortment"] = product.get("assortmentText") or entry["assortment"]

    cutoff = (today - timedelta(days=RETENTION_DAYS)).isoformat()
    for number in [n for n, e in entries.items() if e["last_seen"] < cutoff]:
        del entries[number]
    state["sweeps"] = [sweep for sweep in sweeps if sweep >= cutoff]
    for night in [n for n in accounts if n < cutoff]:
        del accounts[night]


def record(
    products: list[dict],
    today: date | None = None,
    path: Path | None = None,
    sweep: dict | None = None,
) -> None:
    today = today or datetime.now(timezone.utc).date()
    state = load(path)
    update(state, products, today, sweep)
    save(state, path)


def _bucket(nights: int) -> str:
    for low, high, label in BUCKETS:
        if nights >= low and (high is None or nights <= high):
            return label
    return BUCKETS[0][2]


def summary(state: dict) -> dict:
    """What the record says, as plain numbers; empty if no sweep is recorded."""
    sweeps = state["sweeps"]
    if not sweeps:
        return {}
    latest = sweeps[-1]
    horizon = (date.fromisoformat(latest) - timedelta(days=RECENT_DAYS)).isoformat()
    entries = state["products"].values()

    absent_now = Counter()  # nights absent so far, for wines seen recently
    by_assortment = Counter()
    for entry in entries:
        if horizon <= entry["last_seen"] < latest:
            nights = sum(1 for sweep in sweeps if sweep > entry["last_seen"])
            absent_now[_bucket(nights)] += 1
            by_assortment[entry["assortment"] or "unknown"] += 1
    returned = Counter(
        _bucket(item["nights"]) for entry in entries for item in entry["returns"]
    )
    accounts = state.get("accounts", {})
    recent = [accounts[n]["unreached"] for n in sorted(accounts)[-GAP_WINDOW:]]
    return {
        "account": accounts.get(latest),
        "unreached_recent": recent,
        "since": state["tracking_since"],
        "sweeps": len(sweeps),
        "latest": latest,
        "found": sum(1 for entry in entries if entry["last_seen"] == latest),
        "absent_now": absent_now,
        "absent_now_total": sum(absent_now.values()),
        "by_assortment": by_assortment,
        "gone_longer": sum(1 for entry in entries if entry["last_seen"] < horizon),
        "returned": returned,
        "returned_total": sum(returned.values()),
    }


def _row(counter: Counter) -> str:
    parts = [f"{label} {counter[label]}" for _, _, label in BUCKETS if counter[label]]
    return " · ".join(parts) or "none"


def print_summary(state: dict) -> None:
    facts = summary(state)
    print("\nCatalog sightings")
    if not facts:
        print("    not tracked yet — the nightly sweep records it from its next run")
        return
    print(
        f"    tracked since {facts['since']}: {facts['sweeps']} sweep(s), the latest "
        f"on {facts['latest']} found {facts['found']} wines"
    )
    account = facts["account"]
    if account:
        print(
            f"    could not be reached by the latest sweep: {account['unreached']} "
            f"of {account['reported']} reported upstream"
        )
        recent = facts["unreached_recent"]
        if len(recent) > 1:
            print(
                f"        over the last {len(recent)} recorded sweeps: "
                f"{min(recent)}-{max(recent)}"
            )
        if account.get("short"):
            parts = ", ".join(
                f"{label} {n}" for label, n in sorted(account["short"].items())
            )
            print(f"        partitions short after both passes: {parts}")
    print(
        f"    missing in the latest sweep but seen in the last {RECENT_DAYS} days: "
        f"{facts['absent_now_total']}"
    )
    print(f"        nights absent so far: {_row(facts['absent_now'])}")
    top = ", ".join(f"{name} {n}" for name, n in facts["by_assortment"].most_common(4))
    print(f"        by assortment: {top or 'none'}")
    print(f"    not seen for longer than that (since tracking began): {facts['gone_longer']}")
    print(
        f"    absences that ended, the wine came back: {facts['returned_total']}"
        f" — {_row(facts['returned'])}"
    )
    if facts["sweeps"] <= RECENT_DAYS:
        print(
            f"    Too early to read: {facts['sweeps']} sweep(s) recorded, so absences "
            f"longer than {max(facts['sweeps'] - 1, 0)} night(s) cannot be seen yet."
        )

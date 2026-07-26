# wine-additives

An open dataset of the additives declared in wines sold by Systembolaget.

Since 8 December 2023 the EU requires wine to declare its ingredients and
nutritional values. Systembolaget shows that declaration on each product page,
but it cannot be searched, filtered or compared — you can look up one wine at a
time and nothing more. This project reads every wine's declaration, turns the
free text into structured data, and publishes the result.

## What is in here

| File | Contents |
|---|---|
| `data/wines.json` | The dataset: one record per wine, with parsed additives |
| `data/wines.sqlite` | The same rows, for querying |
| `data/additives.yaml` | The substance dictionary — names, E-numbers, aliases |
| `data/unknown.json` | Text the parser could not identify, ranked by impact |

## Caveats worth reading before using this

**Most wines declare nothing yet.** The requirement applies to wine made from
the 2024 harvest onwards; older stock may be sold until it runs out. Around 30%
of the assortment currently carries a declaration, rising to roughly 75% among
2024 and 2025 vintages. Coverage improves on its own as stock rotates.

**The text is supplier-entered.** Each importer types the declaration by hand,
so spelling, terminology and completeness vary. `raw_ingredients` is kept on
every record so any claim here can be checked against the source.

**Counting is a judgement call, and here is the one made.** `additive_count`
counts declared additives, sulfites included. Grapes, must and added sugar are
raw materials and are not counted. Bottling gases (nitrogen, CO₂, argon) are
recorded separately in `gases` and not counted, because they are a packaging
step rather than something that stays in the wine. A wine with text the parser
could not read is marked `parse_status: "partial"` and is excluded from any
ranking — omitting a wine is better than understating its additives.

**Fewer additives does not mean healthier.** This is a record of what is on the
label, not a health assessment. Wine is alcohol; that is the relevant risk.

**The label wins.** The bottle in your hand is more current than this dataset.

## Record shape

```json
{
  "product_number": "253108",
  "name": "Adobe Sauvignon Blanc",
  "vintage": "2025",
  "country": "Chile",
  "price": 249.0,
  "declaration_status": "declared",
  "parse_status": "complete",
  "additive_count": 2,
  "additives": [
    {"id": "sulfites", "e_number": "E220-E228", "category": "preservative",
     "name": {"sv": "Sulfiter", "en": "Sulfites"}, "allergen": "sulfites"}
  ],
  "gases": [{"id": "carbon_dioxide", "e_number": "E290"}],
  "base_ingredients": [{"id": "grapes"}],
  "processing_notes": [{"id": "protective_atmosphere"}],
  "allergens": ["sulfites"],
  "nutrition": {"kcal_per_100ml": 73, "sugar_g_per_100ml": 0.2},
  "raw_ingredients": "Druvor*, koldioxid, konserveringsmedel (SULFITER), ...",
  "source_url": "https://www.systembolaget.se/produkt/vin/x-253108/"
}
```

`declaration_status` is `declared` or `not_declared`; `parse_status` is
`complete`, `partial` or `not_declared`. Undeclared wines are kept in the
dataset — leaving them out would hide how much of the assortment says nothing.

## How it works

1. **`catalog.py`** — every wine from Systembolaget's product search API. That
   API caps page size at 30 and stops paging after ~10 000 results, so the query
   is partitioned by country and the parts are merged.
2. **`details.py`** — the search API has no ingredient field. The product page
   does, and it is a Next.js route, so the same data is available as JSON at
   `/_next/data/{buildId}/produkt/vin/x-{productNumber}.json`. The buildId is
   discovered at runtime.
3. **`normalize.py`** — the declaration is free text with missing separators and
   inconsistent spelling, so the parser scans for known substances longest-match
   first, strikes out what it recognised, and judges the remainder. Anything
   left over is reported rather than guessed at.
4. **`build.py`** — joins catalog and declarations into the dataset.
5. **`report.py`** — coverage and quality report; fails if more than 2% of
   declared wines are `partial`.

## Running it

```sh
uv sync
uv run python -m src.catalog          # ~10 min
uv run python -m src.details          # full pass: several hours, resumable
uv run python -m src.build
uv run python -m src.report
uv run pytest
```

`details.py` caches every response under `data/cache/`, so an interrupted run
picks up where it stopped. Use `--limit N` for a quick sample and `--refresh` to
re-fetch wines that are already cached.

## Running it unattended

A full pass takes hours of deliberately slow requests, which a laptop will
interrupt every time it sleeps. `deploy/` sets the pipeline up on a machine that
stays awake — a Raspberry Pi 4 running 64-bit Debian bookworm is plenty, and its
system Python 3.11 is enough.

```sh
./deploy/push-to-pi.sh            # from the Mac: copies the tree, cache included
ssh pi@raspberrypi
cd wine-additives && ./deploy/bootstrap.sh
```

`bootstrap.sh` installs uv, syncs dependencies, runs the tests and installs a
systemd user timer that updates the dataset nightly at 03:00 with a random delay.
It finishes by printing the one privileged command needed — `loginctl
enable-linger` — without which user services stop when you log out.

`deploy/update.sh` is the cycle itself: catalog, declarations, build, tests,
report. Sundays re-fetch everything, but only once the first full pass has
completed — there is no point refreshing what has never been fetched.

```sh
systemctl --user start wine-additives.service      # run one cycle now
journalctl --user -u wine-additives -f             # watch it
systemctl --user list-timers wine-additives.timer  # when is the next run
```

The GitHub Actions workflow in `.github/workflows/` does the same job in the
cloud. Use one or the other, not both — two crawlers is twice the load on
Systembolaget for the same data.

## Improving the parser

Run the report, look at the top of `data/unknown.json`, and add the spellings to
`data/additives.yaml`. Each substance carries its aliases, including the
misspellings and mistranslations that appear in real declarations. Add a
fixture to `tests/fixtures/declarations.json` for anything subtle.

## Being a good guest

Requests are sequential, spaced 0.4 s apart, and identify themselves. Nothing
here is behind a login or disallowed by `robots.txt`. Data belongs to
Systembolaget and the suppliers who entered it; this repository is a derived
work published for consumer transparency.

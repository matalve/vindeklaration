# State of play

Where the project stands, for a session starting cold. Read `CLAUDE.md` first —
that is how to work here; this is what has been done and what is next.

Written 2026-08-02. **Update it when you finish something.** The figures age;
the shape does not.

## Live

**vindeklaration.se**, on a Cloudflare Worker with static assets, built from
this repository by Cloudflare's Git integration on every push to `main` — which
includes the Pi's nightly dataset commit around 03:20. `docs/deploy-site.md` has
the setup, including the two things that bite: the account subdomain derives
from the account name, and a Worker does not serve `404.html` without
`wrangler.jsonc`.

| Path | What |
|---|---|
| `/` | Search, coverage headline, links to the saved lists |
| `/vin/{nr}-{slug}/` | One wine. Swedish only — see *Bilingual* in the site plan |
| `/hitta/` | The filter. Opens with "when are you buying" |
| `/lista/{slug}/` | Ten saved slices, built not filtered, so they need no JavaScript |
| `/tillsats/{id}/` | 75 substances, both languages |
| `/tackning/` | Coverage breakdown |
| `/metod/` | Method, counting rule, licence, third-party requests |

Build: `uv run python -m src.site`, about 25 s, ~15 000 files. **The build fails
above 19 000 files on purpose** — a Worker rejects more than 20 000 static
assets on the free plan.

## The dataset

15 174 wines. Roughly 19% carry a declaration; about 0.5% of those cannot be
read in full and are excluded from every ranking. `src/report.py` prints the
current numbers and its gate watches drift rather than a level.

**Sunday's full refresh (2026-08-02) filled three fields that were empty
before.** `deploy/update.sh` re-fetches everything on Sundays once the first
full pass has completed.

- **`store_count` is real now** — 6 013 wines in at least one store, up to 454,
  median 187 for the fixed range. This unblocks the plan's *"Every wine says
  how findable it is, in words rather than a flag: finns i 187 butiker"*, which
  is the last unimplemented half of the buyability rules and the site audit's
  finding 8. Nothing uses it yet; it is not in the search index.
- **`gluten_free` is `False` on all 15 174 records and `True` on none.** After a
  full refresh that is a signal rather than a fact — either Systembolaget marks
  no wine gluten-free, or `isGlutenFree` is being read wrong in
  `src/details.py`. Worth ten minutes against a live product page before
  anything is built on it.
- **`discontinued` is `False` everywhere**, which is plausible: a discontinued
  wine leaves the catalogue rather than staying in it flagged.

## What each phase delivered

**Phase 1 — lookup.** Wine pages, search, method page. Wine pages carry the
declaration verbatim, the parsed substances with E-numbers, allergens with their
animal origin named, the nutrition table, and the bottle photograph rendered
from Systembolaget's CDN under the conditions in `docs/legal-notes.md` §2j.

**Phase 2 — the shortlist.** `/hitta` filters in the browser against the same
index the search uses; `/lista/{slug}` renders ten slices at build time. Both
obey the rules the plan spends its length on, and both have been through
`site-auditor` — which found, among other things, that the filter's default
state was the global leaderboard the plan forbids by name.

**Phase 3 — substances and coverage.** Built 2026-08-02 by another session,
audited, and the audit found something the rules had not covered: the site had
published a claim that a substance was *harmful*. The "never say" list banned
claims in one direction only. See the second bullet of *What the site must never
say* in the site plan — it is the most instructive thing written down in this
project.

**Phase 4 — trends** is not started. `data/quality-history.json` has been
accumulating one row per nightly run since 2026-07-27 and is the seed for it.

## Open

**Needs a Swedish lawyer, and the owner has decided not to consult one yet.**
Whether the crawl is permitted under Systembolaget's clause 1.7; whether the
catalogue is a protected database; whether publishing a compliance statistic
about a sole trader reaches förtal. All in `docs/legal-notes.md`, all recorded
as decisions rather than oversights.

**The importer table is designed and not built.** Rules are in *Naming
importers*. It ships on the weaker claim — the company placed the wine on the
Swedish market and supplied the text — because Article 8(1) of Regulation
1169/2011 puts responsibility on the producer for EU wine.

**Advertising is intended eventually.** Today the site takes no income, and
that fact is what keeps five separate regimes out of scope. *When the site takes
income* lists what changes on the day.

**`declaration-finder` has 41 German producers left**, 37 of them with a single
wine. `docs/elabel-platforms.md` carries which platforms can be read. The tail
costs about as much per producer as the batches already done and yields a fifth
as much, so it has been left.

## Working here without burning the session

Context grows monotonically: every tool result stays in the window, so a long
session pays a rising price for each small edit. **Start a new session when the
task changes.** Nothing is lost by it, because the repository is the memory:

- `CLAUDE.md` — the rules and the decisions, with their reasons
- `docs/site-plan.md` — what the site may and may not say, and why
- `docs/legal-notes.md` — what was researched, quoted and cited
- `docs/elabel-platforms.md` — which hosts can be read
- this file — where things stand
- commit messages — why each change was made

The one thing that does not survive is what has not been written down. If a
session establishes something a later one would otherwise re-derive, that is a
commit, not a chat message.

Agents commit after each unit of work, not at the end of a run — a session limit
once cost eight producers' worth of `declaration-finder` output that was going
to be committed at the end.

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

**The whole chain runs unattended, verified end to end 2026-08-02** rather than
inferred: the timer fired at 03:01, `update.sh` crawled, committed and pushed by
06:13, and the live `/tackning` then reported 2 919 of 15 174 wines against the
2 882 of 14 981 a local build had given the day before. Nobody touched it. The
one thing that would break it silently is build watch paths — step 7 of
`docs/deploy-site.md` suggests excluding `docs/` and `*.md` from rebuilds, and
`data/` must never join that list.

## The dataset

15 124 wines. Roughly 19% carry a declaration; about 0.5% of those cannot be
read in full and are excluded from every ranking. `src/report.py` prints the
current numbers and its gate watches drift rather than a level.

**Sunday's full refresh (2026-08-02) filled three fields that were empty
before.** `deploy/update.sh` re-fetches everything on Sundays once the first
full pass has completed.

- **`store_count` is real, and used.** 6 013 wines in at least one store, up to
  454, median 187 for the fixed range — but **9 161 wines are in zero stores**,
  and the median order-only wine is one of them. The plan's 2026-07-27 sample
  said order-only wines sat at 1 store; the first full refresh says otherwise,
  so zero is the common case rather than a missing value. Every wine page now
  says how findable it is in words, and the filter has a store threshold
  (index column 15).
- ~~**`gluten_free` may be misread.**~~ Settled 2026-08-03: it is not. Fetched
  live and compared against the cache — the field is read correctly, and
  Systembolaget simply sets it on no wine. It is genuinely `true` on beers sold
  as glutenfri, so the flag works; wine is never marked. **Never surface it**:
  `false` means *not marked*, not *contains gluten*. The search API does not
  populate the field at all, only the product page does.
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

**Phase 3 — substances and coverage.** Built 2026-08-02, audited, and the audit
found something the rules had not covered: the site had published a claim that a
substance was *harmful*. The "never say" list banned claims in one direction
only. See the second bullet of *What the site must never say* in the site plan —
it is the most instructive thing written down in this project, and it grew twice
more the same day.

The sentence at the centre of it was about three colours and the Annex V
children's-attention warning. Fixing it went through three states, and the
sequence is the lesson: it was **paraphrased** rather than quoted, then it was on
**one page of three**, and then the warning turned out to **reach no product on
the site at all** — Commission Regulation (EU) No 238/2010 exempts drinks above
1,2 % alcohol, which is every bottle here. The base act says otherwise, and the
base act is what a search finds first. **A regulation is not verified until the
amending acts have been read.**
**The warning is named on all three pages anyway, decided by the owner
2026-08-02**, together with the exemption and the exemption's reason — a reader
is entitled to know what is in the glass even where the label need not say it,
and "exempt" without its reason reads as "found harmless", which 238/2010 does
not say.

Two related settlements from the same day. `E100` was never declared by anyone:
both wines carrying it write `Energivärde: E/100 ml`, and blanking the slash
turned it into the colour curcumin — fixed in `src/normalize.py`, and reparsing
all declarations changes those two wines and nothing else. And **a product listed
on the site has its additives named, whatever the product is.** The three colours
are declared by a flavoured sparkling drink and a spirit-based aperitif rather
than by wine; that is not a reason to hedge or to leave the substance out.

**The filter prunes its own menus** as of 2026-08-02. 433 grapes against 57
countries means most combinations hold nothing, so an option that would return
no wine is hidden — never the reader's own selection, and the results line says
how many went and why. `tests/test_hitta.mjs` runs the browser code under Node
against the real index and checks it against a brute-force re-slice; it is the
only JavaScript test in the project and it caught a real bug on its first run.

**Phase 4 — trends** is not started. `data/quality-history.json` has been
accumulating one row per nightly run since 2026-07-27 and is the seed for it.

## Open

**Needs a Swedish lawyer, and the owner has decided not to consult one yet.**
Whether the crawl is permitted under Systembolaget's clause 1.7; whether the
catalogue is a protected database; whether publishing a compliance statistic
about a sole trader reaches förtal. All in `docs/legal-notes.md`, all recorded
as decisions rather than oversights.

**The repository is private, and one flag knows it.** `REPO_PUBLIC` in
`src/site.py` is `False`. `/metod` used to tell readers everything was public on
GitHub and linked there three times; all three 404 for anyone but the owner, on
the page whose job is to say what the site cannot show. It now states plainly
that there is no way to report an error yet. **Decided by the owner 2026-08-02:
the issue tracker is the right channel and the repository opens closer to a real
launch.** Flip the flag that day and every sentence becomes the stronger one.

**The importer table is built, and waits on that same flip.** Rules are in
*Naming importers*; `importer_rows()` and `templates/importer.html` implement
them and are tested. It renders only when `REPO_PUBLIC` is on, because a named
compliance statistic whose correction route is a 404 is the one part of the
design that is not optional. Verified with the flag on: 19 importers clear the
40-wine threshold, all aktiebolag, plus one counted row of 1 608 wines from 239
unnamed suppliers. The share is over covered vintages only — published raw the
table would put Johan Lidby, who declares on 97 of every 100 covered bottles,
near the bottom at 29.2%, because that column measures how old the stock is.

**Before the flag flips, `CORRECTION_DAYS` needs an answer.** It is 14 and the
owner has not confirmed it. It is the one figure the site would publish as a
promise rather than a measurement, and a test guards the flag saying so.

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

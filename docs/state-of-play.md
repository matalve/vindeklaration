# State of play

Where the project stands, for a session starting cold. Read `CLAUDE.md` first —
that is how to work here; this is what has been done and what is next.

Started 2026-08-02, last checked against the repository 2026-09-01.
**Update it when you finish something.** The figures age; the shape does not.

## Live

**vindeklaration.se**, on a Cloudflare Worker with static assets, built from
this repository by Cloudflare's Git integration on every push to `main` — which
includes the small commit the Pi pushes at the end of each nightly run.
`docs/deploy-site.md` has the setup, including the things that bite: the
account subdomain derives from the account name, a Worker does not serve
`404.html` without `wrangler.jsonc`, and the build command is `bash
cf-build.sh` and nothing else.

| Path | What |
|---|---|
| `/` | Search, coverage headline, links to the saved lists |
| `/vin/{nr}-{slug}/` | One wine. Swedish only — see *Bilingual* in the site plan |
| `/hitta/` | The filter. Opens with "when are you buying" |
| `/lista/{slug}/` | Ten saved slices, built not filtered, so they need no JavaScript |
| `/tillsats/{id}/` | One substance. Both languages |
| `/tackning/` | Coverage breakdown |
| `/metod/` | Method, counting rule, licence, third-party requests |

Build: `uv run python -m src.site`, about 25 s, ~15 000 files. **The build fails
above 19 000 files on purpose** — a Worker rejects more than 20 000 static
assets on the free plan.

**The whole chain runs unattended, and has been verified twice rather than
inferred.** On 2026-08-02 the timer fired at 03:01, `update.sh` crawled and
pushed by 06:13, and the live `/tackning` then reported 2 919 of 15 174 wines
against the 2 882 of 14 981 a local build had given the day before — nobody
touched it. On 2026-08-29 the same held for the rebuilt path: R2, the release,
the commit, the push and a green build.

Build watch paths are configured — include `*`, exclude `/docs`, `/deploy`,
`.claude/` and `*.md`. **`data/` must never join that exclude list**, because
the rebuild rides on the Pi's commit of `data/quality-history.json`.

## The dataset left git, and then left the history

**It left git on 2026-08-29.** A 16 MB JSON committed nightly cost its
near-full size in history, forever. `update.sh` now publishes `wines.json.gz`
and `catalog.json.gz` to the R2 bucket behind `/data/` and to a rolling
`dataset-latest` release, *before* pushing — the push triggers the rebuild, and
the rebuild downloads the dataset from the bucket. Only `unknown.json` and
`quality-history.json` are still committed.

The migration bit in four places worth reading before touching the pipeline
again — `--remote`, systemd's `PATH`, the build command's home, and the binding
name `wrangler` proposes. They are written up where they apply, in
`docs/deploy-site.md`.

**And it left the history too, later the same day.** Dropping the file from the
tip left 69 blobs behind: 1.15 GB uncompressed, a 199 MB clone for a tree of a
few MB. `git filter-repo --invert-paths` removed `wines.json`, `catalog.json`
and `wines.sqlite` from all 417 commits and the repository is now 1.7 MB.
`--prune-empty never` was deliberate — the dataset commits' messages are part
of the record, so they survive as empty commits rather than vanishing. Every
message, author and date is unchanged, the tip tree is the same object, and the
one altered byte-sequence is a revert commit's body, whose reference
filter-repo remapped to the same commit's new hash. **Every SHA before
2026-08-29 is dead:** any clone other than the Pi's must be re-cloned, not
pulled. What this did *not* reach is `refs/pull/1/head` and `refs/pull/13/head`,
which GitHub keeps forever and which still carry the old objects — a normal
clone never fetches them, so the clone size is genuinely fixed, but the bytes
are still on GitHub and getting rid of them would take Support or a new
repository. Judged not worth it.

## The dataset

**Run `uv run python -m src.report` for the figures.** They move every night —
between 2026-08-29 and 2026-09-01 the assortment went from 15 146 wines to
15 025 as stock rotated — so any number written here is a snapshot with a date
on it, not a fact to rely on. On 2026-09-01: 15 025 wines, 20.7% carrying a
declaration, 0.7% of those unreadable in full and excluded from every ranking.
The gate watches drift rather than a level.

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
  `false` means *not marked*, not *contains gluten* — and it is **not** evidence
  that no wine contains gluten. One wine in this dataset says otherwise:
  Maison Blanche Rosé (214801) declares gluten as an allergen, from wheat
  protein used as a fining agent. The search API does not populate the field at
  all, only the product page does. **Thread closed — do not reopen it as
  "no wine has gluten".**
- **`discontinued` is `False` everywhere**, which is plausible: a discontinued
  wine leaves the catalogue rather than staying in it flagged.

## What has been built

The four phases in order, and three things that arrived alongside them.

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

**Presentation, 2026-08-03 to 2026-08-05.** Theme follows the operating system
with a three-segment control; icons are one inline sprite and are navigation
only; the front page says what it is for; the wine page has a hierarchy instead
of ten identical blocks; `/tackning` has a bar figure of declared share by
vintage. `docs/site-plan.md` §*Presentation* has the rules and what is left.
The figure was audited twice and the second pass found that two fixes from the
first had broken something else — **text and stroke widths inside an SVG scale
with the viewBox**, so a 6:1 palette value and a 12 px font both describe
something the reader cannot see on a phone. Anything that must be read lives in
HTML beside the figure.

**The site computes its own figures now, 2026-08-05.** Four percentages were
written into `strings.json` by hand in July and one had already gone wrong —
order-only wines were published as "four in five" and are 71.7%. Grape and
pairing coverage, the silent share and the order-only share are measured at
build time. Two names the site matches literally against Systembolaget's
vocabulary — `LIST_CATEGORIES` and `FIXED_RANGE` — now have `check_vocabulary()`
behind them: a build warning, plus a deliberately non-hermetic test that reads
the live dataset so the suite turns red the day a category is renamed rather
than the day someone notices a list has been empty for a month.

**Phase 4 — trends** is not started. `data/quality-history.json` has been
accumulating one row per nightly run since 2026-07-27 and is the seed for it.

## Open

**Needs a Swedish lawyer, and the owner has decided not to consult one yet.**
Whether the crawl is permitted under Systembolaget's clause 1.7; whether the
catalogue is a protected database; whether publishing a compliance statistic
about a sole trader reaches förtal. All in `docs/legal-notes.md`, all recorded
as decisions rather than oversights.

**The repository went public on 2026-08-29 and `REPO_PUBLIC` is `True`.**
`/metod` links GitHub three times and all three now resolve for everyone, on
the page whose job is to say what the site cannot show. The flag stays in
`src/site.py` rather than being deleted: it is the one switch that pulls the
importer table back if the repository ever closes again, and the table must
never outlive its own error channel. `CORRECTION_DAYS` is 14, confirmed by the
owner the same day — the one figure published as a promise rather than a
measurement, which is why it was asked rather than decided.

**The importer table is live.** Rules are in *Naming importers*;
`importer_rows()` and `templates/importer.html` implement them and are tested.
As built on 2026-08-29: **21** importers clear the 40-wine threshold, every one
an aktiebolag, plus one counted row of 1 628 wines from 241 unnamed suppliers
at 57.5%. The Wine Team Global leads at 98.7%, Tryffelsvinet trails at 18.2%.
The share is over covered vintages only — published raw the table would put
Johan Lidby, who declares on 97 of every 100 covered bottles, near the bottom
at 33.6%, because that column measures how old the stock is.

**Nothing in the code stops a natural person being named — the threshold does
it by accident.** `importer_rows()` filters on `IMPORTER_MINIMUM` and nothing
else. The sole traders Systembolaget publishes under their own names sit at 3
covered wines each, so they are nowhere near 40, and the highest supplier with
no corporate marker in its name is the trade name *Iconic Wines* at 38. That is
two wines of margin on a figure that rises as stock rotates. `CLAUDE.md` and
*Naming importers* both turn on förtal reaching a natural person where it does
not reach a company, so the protection being incidental rather than explicit is
worth knowing before the next stock rotation, not after.

**Advertising is intended eventually.** Today the site takes no income, and
that fact is what keeps five separate regimes out of scope. *When the site takes
income* lists what changes on the day.

**`declaration-finder` is on Spain**, batch 5, opened 2026-08-31 to close the
Spanish pool. Across 108 runs it has attempted 561 wines and found 33 —
`data/producer-declarations.json` carries the record, `docs/elabel-platforms.md`
which platforms can be read. Italy was the tenth batch before it; France is set
aside and Germany's tail was left where it stood. The tail costs about as much
per producer as the batches already done and yields a fifth as much, which is
why batches get set aside rather than finished.

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

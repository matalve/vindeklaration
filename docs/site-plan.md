# Site plan — vindeklaration.se

How people are meant to use the site, and what it may and may not tell them.
Written 2026-07-26, before any site code exists. Figures are a snapshot of that
day and will age; the shape of the argument will not.

## What the site is for

Systembolaget publishes every wine's ingredient declaration, one product page at
a time, and offers no way to search, filter or compare them. This dataset makes
that comparable. The site is the interface to it: a Swedish consumer can look up
the bottle in their hand, or find the wines that declare least in the price band
they were going to buy in anyway.

It is not a shop, not a review site, and not a health service.

## Who arrives, and what they came for

1. **Standing in the shop, bottle in hand.** Wants one screen: what this wine
   declares, in plain words, with the source. Phone, poor light, maybe poor
   signal. This is the journey that has to be fastest.
2. **Planning a purchase.** "Something red, under 150 kr, with as little in it
   as possible." Wants a shortlist they can act on — which means it must be
   limited to wines actually orderable, not the whole 15 000.
3. **Reacting to a word on a label.** "What is metavinsyra, and should I care?"
   Arrives from a search engine onto a substance page.
4. **Avoiding something specific.** Vegans, and people avoiding milk-, egg- or
   fish-derived fining agents. This is the group the data serves best, because
   the question is factual rather than evaluative.
5. **Curious about the shelf as a whole.** Journalists, and people who want to
   know how many wines say nothing at all. This is the story the dataset tells
   better than any single wine page.
6. **A producer or importer looking themselves up.** Will arrive eventually.
   Everything shown must be defensible and traceable to their own text.

## The problem at the centre of the design

**Four wines in five declare nothing.** On 2026-07-26: 15 017 wines, 2 899 with
a declaration (19.3%). The requirement covers the 2024 harvest onwards, so
coverage rises on its own — 81% of 2025 vintages already declare — but for now
any "fewest additives" list is a ranking of *what got disclosed*, not of what is
in the bottle. A wine that declares three additives is not worse than one that
declares nothing; it is more honest, and it is the only one we know anything
about.

**And about one declaration in ten cannot be read in full** (9.0% on
2026-07-26, falling as the dictionary grows). Those wines are excluded from
every ranking, on purpose.

Three consequences that shape every page:

- **The denominator is always visible.** A shortlist says "12 wines shown of
  340 in this price band — 297 declare nothing, 31 declare something we could
  not fully read." Never a bare top ten.
- **The three states are rendered as three states**, never collapsed:
  *declares and we read it*, *declares and we could not read all of it*,
  *declares nothing*. The third is the most common answer on the site and must
  not look like an error or an accusation.
- **No score.** No grade, no traffic light, no "clean wine" badge. A number of
  declared additives is a count, and it is shown as a count.

## What the site must never say

- That fewer additives is healthier, safer, or better for you. Wine is alcohol;
  that is the health risk, and it is the same in every bottle on the list.
- That a wine "contains no additives" when it declares nothing. It says
  *the wine does not declare any*, and the site says exactly that.
- Anything about a named wine that cannot be traced to that wine's own declared
  text, shown verbatim on the page next to the interpretation.
- Anything that reads as advice on what to drink. It ranks disclosure, and it
  says so.

The bottle in the user's hand is newer than the dataset. Every wine page carries
that sentence and a link to the source page.

## What a recommendation can honestly be

Three axes, each with a rule the user can read and a limit that is stated, not
buried.

**A. Fewest declared additives within a comparable set.** The user picks what
they were going to buy anyway — category, price band, availability — and gets
the wines in that slice that declare least. The comparison is only meaningful
inside a slice: a sparkling wine declares dosage sugar and a fortified wine
declares added alcohol, so ranking them against a still red is a category error.

**B. Exclusions.** Vegan; no milk-, egg- or fish-derived fining agents; no
declared colours or flavourings. These are the strongest recommendations the
data supports, because the user's question is factual — "does this contain
something I avoid" — and the declaration answers it directly. A few dozen wines
declare animal-derived fining agents outright, and the catalog's own `vegan`
flag covers many more.

**C. Sugar and energy.** Nutrition figures come with nearly every declaration
(kcal, sugar per 100 ml). Useful, factual, and the one axis where a lower number
is unambiguously the thing the user asked for.

Axes B and C are where the site is genuinely useful to an individual. Axis A is
where it is interesting about the market. Do not let A's ranking swallow the
other two.

### The rule, written down

A shortlist is reproducible or it is opinion. The spec:

- **Comparison set**: category (red / white / sparkling / rosé / fortified /
  flavoured), price band, and assortment — default to what can actually be
  ordered rather than the whole catalog.
- **Eligible**: `declaration_status = declared` and `parse_status = complete`.
  Partial declarations are never ranked, and never silently dropped either —
  they are counted in the "not shown" line with their reason.
- **Rank by** `additive_count` ascending. Ties broken by number of distinct
  additive categories, then by price ascending. Never by anything the site
  earns from, because it earns nothing.
- **Show, for every entry**: the count, the substances by name and E-number,
  the declaration verbatim, and a link to the product page.
- **Show, for every list**: how many wines the slice contained, how many
  declared, how many were unreadable.

Written this way, the recommendation is auditable — `declaration-auditor` can
sample a published list and check it against the live product pages, which is
exactly how the dataset itself is checked.

## Pages

| Path | Purpose |
|---|---|
| `/` | Search by name or product number, and the coverage headline |
| `/vin/{product_number}-{slug}` | One wine: declaration, substances, nutrition, raw text, source link |
| `/hitta` | Shortlist builder: category, price, exclusions, sugar — the recommendation |
| `/lista/{slug}` | Saved slices worth linking to, e.g. "red under 150 kr, fewest additives" |
| `/tillsats/{id}` | One substance: what it is, why it is used, which wines declare it |
| `/tackning` | How much of the shelf declares — by category, country, vintage, supplier |
| `/metod` | Method, caveats, licence, and what the site refuses to claim |

The wine page is the product. Everything else exists to lead somewhere useful
from it or to justify it.

### Details that matter more than they look

- **Partial declarations are shown, not hidden.** The page says which fragment
  could not be read, next to the full original text. A user who can read
  Italian may understand it immediately, and the honesty costs nothing.
- **Comparison of two or three wines** side by side, because that is the actual
  decision being made in the aisle.
- **No accounts, no cookies, no analytics, no affiliate links.** The project
  holds no personal data and should not start now. It also means no cookie
  banner, which on a phone in a shop is a feature.
- **Substance pages carry the aliases** — including the misspellings found in
  real declarations. Someone searching the exact string from a label should
  land on the right page.

## Bilingual

Swedish is the default; the audience and the source text are Swedish. English
mirrors at `/en/…`. Substance names already carry `sv` and `en` in
`additives.yaml`; UI strings need their own table. Declarations themselves are
never translated — they are quoted, in the language the supplier wrote them.

## Technical shape

Static site generated from `wines.json` at build time. No server, no database,
no runtime dependency on Systembolaget. 15 000 wine pages is unremarkable for a
static generator, and a compact search index (name, product number, category,
price, counts) can be shipped as one gzipped JSON — `wines.json` itself is
16 MB but gzips to 1.3 MB, and the index is a fraction of that.

The flow already exists: the Pi crawls nightly, commits the dataset, pushes to
GitHub. A build on push to `main` deploys the site. That is a build, not a
crawler, so it does not conflict with the one-crawler rule. Cloudflare Pages
fits — the domain is registered elsewhere, since `.se` needs a Swedish
registrar, but its DNS can point at Cloudflare.

Publish `wines.json.gz` and `wines.sqlite` as release assets so the dataset is
downloadable, whole, by anyone — the point of the project is that the data is
open, not that the site is nice.

## Phases

1. **Lookup.** Search, wine pages, method page. Serves journey 1 and makes
   every later page linkable. Nothing here needs a ranking decision.
2. **Shortlists.** `/hitta` with category, price, exclusions. This is the
   recommendation, and it is where the honesty rules earn their keep.
3. **Substances and coverage.** Substance pages and the transparency dashboard.
   The coverage page is the one most likely to be quoted by someone else.
4. **Trends.** The nightly commits are a time series: coverage by month,
   substances appearing and disappearing, suppliers who started declaring.
   It costs nothing to keep and cannot be recreated later if the history is
   thrown away.

## Open questions for the owner

- **Are undeclared wines listed at all?** Hiding them makes lists cleaner and
  the dataset look bigger than it is. Showing them is the honest choice and
  makes the site's real finding — how few declare — impossible to miss. The
  plan above assumes they are shown, greyed, with the reason.
- **Are suppliers named on the coverage page?** The data supports a ranking of
  who declares and who does not, per importer. It is public information and it
  is the most newsworthy thing here. It is also a naming decision with
  consequences, and it is yours.
- **Public or private dataset?** The site implies a public dataset; the
  repository is private today.
- **The quality gate** at 2% against a real figure near 9% still blocks a clean
  build, and the site's credibility rests on that number being deliberate.
- **Wording review before launch.** The line between "declares fewer additives"
  and an implied health claim is the project's main legal and ethical exposure.
  Worth a careful read by someone who has not been staring at it.

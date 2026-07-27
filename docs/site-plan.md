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

**And some declarations cannot be read in full** (9.0% on 2026-07-26, 4.1% on
2026-07-27 after the dictionary took in the words the corpus actually uses;
falling further as it grows). Those wines are excluded from every ranking, on
purpose.

Three consequences that shape every page:

- **The denominator is always visible, and it is browsable.** A shortlist says
  "12 wines ranked of 340 in this price band — 297 declare nothing, 31 declare
  something we could not fully read", and those 297 and 31 are listed below the
  ranking, not merely counted. Never a bare top ten. See *Undeclared wines stay
  in the results* below.
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

## What the shelf can be filtered on

The filter is the second reason people come, and it can only offer facets the
dataset actually carries. Coverage on 2026-07-27, over 15 085 wines:

| Facet | Source | Coverage | Note |
|---|---|---|---|
| Price | catalog `price` | 100% | Ordinary price incl. VAT, excl. recycle fee |
| Country | catalog `country` | 100% | 52 values, Systembolaget's own spelling |
| Category and style | `categoryLevel2/3` | 100% | The comparison set, see below |
| Assortment | `assortmentText` | 100% | 71% of the fixed range declares, 10% of order-only |
| Grape | catalog `grapes` | **57.5%** | 433 distinct, already normalised upstream |
| Food pairing | catalog `tasteSymbols` | **~60%** | 15 values — a closed vocabulary, ideal for a facet |
| Additives | the declaration | **19.3%** | The scarce one, and the point of the site |
| Sugar and energy | detail `nutrition` | ≈ declared | Arrives with the declaration |
| Vegan, organic | `isVeganFriendly`, `isOrganic` | 100% | Supplier's own flag, not derived from the declaration |

Two of these are new. Grape and price were always collected; **food pairing was
not, and is collected from 2026-07-27** — `tasteSymbols` and `usage` come free
in the same search response the catalog step already reads, so it costs no
extra request and no re-crawl. `tasteSymbols` is a controlled list (Fisk,
Skaldjur, Lamm, Nöt, Fläsk, Fågel, Vilt, Grönsaker, Ost, Dessert, Asiatiskt,
Buffémat, Aperitif, Sällskapsdryck, Avec/digestif); `usage` is the prose
sentence with the serving temperature, quoted, never parsed.

**Grape and pairing are about 60% covered, and that is not the same kind of gap
as the declaration gap.** A missing declaration is a supplier saying nothing; a
missing grape is Systembolaget not filling a field for a blend. Both hide wines
from a filtered list, so both are counted in the "not shown" line, and each
gets its own reason — the user must never read "no wines match" when the truth
is "the grape field is empty for 6 416 wines."

Grapes cannot be recovered from elsewhere: `rawMaterial` on the product page
fills only 303 of the 6 416 blanks, and it is free text ("Corvina, rondinella
och molinara samt övriga druvsorter"). Not worth parsing, and parsing it would
be guessing.

## What a recommendation can honestly be

Three axes, each with a rule the user can read and a limit that is stated, not
buried.

**A. Fewest declared additives within a comparable set.** The user picks what
they were going to buy anyway — category, price band, availability — and gets
the wines in that slice that declare least. The comparison is only meaningful
inside a slice: a sparkling wine declares dosage sugar and a fortified wine
declares added alcohol, so ranking them against a still red is a category error.

**B. Exclusions and inclusions, substance by substance.** Vegan; no milk-, egg-
or fish-derived fining agents; no declared colours or flavourings; and beyond
the presets, any substance in `additives.yaml` chosen by name. These are the
strongest recommendations the data supports, because the user's question is
factual — "does this contain something I avoid" — and the declaration answers
it directly. A few dozen wines declare animal-derived fining agents outright,
and the catalog's own `vegan` flag covers many more.

*Exclude* and *include* are not mirror images, and the interface must not
pretend they are. **Exclude is sound**: a wine that declares fully and does not
list the substance genuinely does not contain it. **Include is weaker**: it
finds wines that *declare* the substance, and a wine that declares nothing may
well contain it too. So "wines with sulphites" is really "wines that admit to
sulphites" — the include filter says so on the results page, in those words.
Excluding is a consumer tool; including is mostly a research one.

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
  ordered rather than the whole catalog. Narrowed further, at the user's
  choice, by country, grape, food pairing, and substances to exclude or
  include.
- **Facets that are not fully covered narrow the denominator, not the truth.**
  Selecting a grape or a pairing restricts the set to wines where that field is
  filled; the "not shown" line then carries a fourth reason alongside the three
  declaration states. Country, price, category and assortment are complete and
  need no such caveat.
- **Eligible for the ranking**: `declaration_status = declared` and
  `parse_status = complete`. Partial declarations are never ranked, and never
  silently dropped either — they are listed below it with their reason.
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

### Undeclared wines stay in the results

Decided by the owner, 2026-07-27. A filtered search returns **every wine in the
slice**, undeclared ones included. Someone looking for a Riesling without
additives is shopping for a Riesling; a list that hides four bottles in five
because their supplier wrote nothing is not a better answer, it is a shorter
one, and it quietly punishes the user for a gap that is not theirs.

So a result page is one slice in three blocks, in this order:

1. **Ranked** — declares, and we read it all. `additive_count` ascending. This
   is the only block that is ordered by anything, because it is the only one
   where a count exists.
2. **Declares, partly unread** — the fragment we could not read is shown next
   to the full original text. Unordered; there is no honest key to sort on.
3. **Declares nothing** — listed, visually quieter, each carrying the same
   sentence: *deklarerar inga ingredienser*. Sorted by price, since that is the
   only fact we have that the user asked about.

Each block carries its own count and its own one-line reason, so the shape of
the answer is legible before a single bottle is read.

The rule this must not break is unchanged: **block 3 is never presented as
wines without additives.** An additive filter — include or exclude — applies to
blocks 1 and 2 and cannot apply to block 3, because there is nothing there to
match against. A wine that declares nothing is not evidence of an empty bottle;
it is an absence of evidence, and the site says which of the two it is on every
row. In practice that means the exclusion filter never removes block 3, it
labels it: the user chose *utan tillsatser* and gets a ranked list of wines
that declare none, followed by the wines nobody can answer for.

The same holds for the facets. A grape filter drops wines whose grape field is
empty, and says so as its own line — that gap is Systembolaget's missing
metadata, not a supplier's silence, and conflating the two would misattribute
both.

## Pages

| Path | Purpose |
|---|---|
| `/` | Search by name or product number, and the coverage headline |
| `/vin/{product_number}-{slug}` | One wine: declaration, substances, nutrition, raw text, source link |
| `/hitta` | Shortlist builder: category, price, country, grape, food pairing, substances in or out, sugar — the recommendation |
| `/lista/{slug}` | Saved slices worth linking to, e.g. "red under 150 kr, fewest additives" |
| `/druva/{slug}` | One grape: how much of it declares, and which of those declare least |
| `/passar-till/{slug}` | One pairing: the same, for "till fisk", "till lamm", … |
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

## Bottle photographs

Link them from Systembolaget's CDN. Do not copy them onto our own host.

That is the opposite of the usual instinct, and it follows from how EU
copyright law treats the two acts. A photograph is protected in its own right —
in Sweden even a plain snapshot gets 50 years under 49a § URL — and the rights
sit with Systembolaget or the supplier, not with us. Embedding an image that
the rightsholder has already made freely available is not a new communication
to the public (*Svensson* C-466/12, *BestWater* C-348/13), whereas saving a copy
and serving it from another site is (*Renckhoff* C-161/17). Hotlinking is
therefore the conservative choice here, not the cheeky one. The exception to
watch is *VG Bild-Kunst* C-392/19: if the rightsholder ever puts a technical
measure in the way, working around it is infringement. In practice that means
if hotlink protection appears, the images go away — they do not get proxied.

What the source offers, verified 2026-07-27 against the live CDN:

- The search API returns `images[].imageUrl`, e.g.
  `https://product-cdn.systembolaget.se/productimages/{productId}/{productId}`.
  That bare URL is a template and 404s on its own; `_{size}.{ext}` completes it.
- `imageModules` lists the available `sizes` (20 to 800 px) and `extensions`
  (avif, webp, jpg, png), and carries a base64 WebP thumbnail of about 150
  bytes — a ready-made placeholder that costs no request at all.
- A 100 px PNG is ~10 kB, a 400 px WebP ~28 kB.
- No hotlink protection today: a request carrying a foreign `Referer` is served
  normally. No `Cache-Control` either, so the browser is left to guess.
- `catalog.py` currently drops both fields, but keeps `productId`.

How to use that:

- **No photographs in lists or shortlists.** Forty bottle shots on a comparison
  page is forty third-party requests to answer a question about text.
- **One image on the wine page**, small, `loading="lazy"`, with explicit width
  and height and the base64 thumbnail behind it so nothing shifts. `alt` is the
  wine's name. Credit reads "Bild: Systembolaget" and links to the product page.
- **Store the URL the API gives us** rather than reconstructing the pattern —
  add `images` to `catalog.py`'s `KEEP`. A pattern we invented is a pattern we
  have to maintain; their own answer is the source of truth.
- **Design for the image not being there.** A missing photograph must leave a
  tidy text card, because one redesign upstream is all it takes.
- **Sample them.** A weekly check of a handful of image URLs, reported like any
  other upstream change, catches a silent 404 sweep before users do.
- **Say so on `/metod`.** The image is the site's only third-party request, and
  it hands the visitor's IP to Systembolaget's CDN. The browser default
  (`strict-origin-when-cross-origin`) sends our origin but not the path, so
  they learn that vindeklaration.se asked, not which wine was being read. That
  is the right balance for a site that otherwise sets no cookies.

None of this is needed for phase 1. Text is what the site is for, and images
can be added later without changing a single page's structure.

## Bilingual

Swedish is the default; the audience and the source text are Swedish. English
mirrors at `/en/…`. Substance names already carry `sv` and `en` in
`additives.yaml`; UI strings need their own table. Declarations themselves are
never translated — they are quoted, in the language the supplier wrote them.

## Technical shape

Static site generated from `wines.json` at build time. No server, no database,
no runtime dependency on Systembolaget. 15 000 wine pages is unremarkable for a
static generator, and a compact search index (name, product number, category,
price, country, grape ids, pairing ids, additive ids, counts) can be shipped as
one gzipped JSON — `wines.json` itself is 16 MB but gzips to 1.3 MB, and the
index is a fraction of that. Filtering happens in the browser against that
index, which is why the facets have to be ids and not free text: 433 grapes and
15 pairings cost almost nothing to encode, and `usage` prose stays on the wine
page where it belongs.

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
2. **Shortlists.** `/hitta` with category, price, country, grape, food pairing,
   and substances in or out; plus the ranked lists at `/lista/{slug}`. This is
   the recommendation, and it is where the honesty rules earn their keep. The
   ranking is always inside a stated slice — there is no single global "fewest
   additives in Sweden" table, because a sparkling wine and a still red are not
   comparable and a leaderboard would say they were.
3. **Substances and coverage.** Substance pages and the transparency dashboard.
   The coverage page is the one most likely to be quoted by someone else.
4. **Trends.** The nightly commits are a time series: coverage by month,
   substances appearing and disappearing, suppliers who started declaring.
   It costs nothing to keep and cannot be recreated later if the history is
   thrown away.

## Open questions for the owner

- ~~**Are undeclared wines listed at all?**~~ Settled 2026-07-27: they are
  shown, in their own block, with the reason. See *Undeclared wines stay in the
  results*.
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

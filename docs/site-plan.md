# Site plan — vindeklaration.se

How people are meant to use the site, and what it may and may not tell them.
Written 2026-07-26, before any site code exists. Figures are a snapshot of that
day and will age; the shape of the argument will not.

Where this plan makes a claim about what the law requires, the evidence is in
`docs/legal-notes.md`, with the source fetched and quoted. That file is not legal
advice and neither is this one; two of its findings end in "needs a Swedish
lawyer" and both of those block something in this plan.

## What the site is for

Systembolaget publishes every wine's ingredient declaration, one product page at
a time, and offers no way to search, filter or compare them. This dataset makes
that comparable. The site is the interface to it: a Swedish consumer can look up
the bottle in their hand, or find the wines that declare least in the price band
they were going to buy in anyway.

It is not a shop, not a review site, and not a health service.

**One use case carries the site, decided 2026-07-27: helping someone choose and
buy a wine whose contents they know.** Everything else in this plan — the
substance pages, the coverage dashboard, the trends — is a by-product of doing
that well, and none of it may be built at its expense.

The consequence is that **availability is part of the answer, not a footnote**.
A recommendation that sends someone to Systembolaget for a bottle that turns out
to be an order-only item with a week's wait, or one that is out of stock
entirely, has not answered the question — it has wasted a trip and taught the
user not to trust the next list. What a wine declares and whether it can be
bought are the same question here, asked one after the other.

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
a declaration (19.3%). The requirement covers wine produced after 8 December
2023, so coverage rises on its own — 81% of 2025 vintages already declare — but
for now any "fewest additives" list is a ranking of *what got disclosed*, not of
what is in the bottle. A wine that declares three additives is not worse than one
that declares nothing; it is more honest, and it is the only one we know anything
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
  **This is a rule about implication, not only about sentences.** It binds page
  titles, `<title>` and meta description, URL slugs, list headings, sort-order
  labels, icons and share text — the places where a claim is made without a
  sentence, and the places most likely to be quoted without their context.
  A disclaimer under a ranking does not cancel the ranking.
- That a wine "contains no additives" when it declares nothing. It says
  *the wine does not declare any*, and the site says exactly that. No statement
  about a wine's contents may be derived from the absence of a declaration.
- Anything about a named wine that cannot be traced to that wine's own declared
  text, shown verbatim on the page next to the interpretation.
- Anything that reads as advice on what to drink. It ranks disclosure, and it
  says so. *(This rule is in tension with the plan's own "helping someone choose
  and buy a wine" and with calling `/hitta` "the recommendation". The tension is
  deliberate and unresolved — see the open question on wording below.)*
- That the wines it counts are the wines the requirement covers. The requirement
  turns on when a wine was **produced**, and the dataset has no production date.
  Vintage is a stand-in and every page that uses it says so. See *Naming
  importers*.
- No advertising, no affiliate links, no sponsorship, no paid placement, no
  commercial income of any kind. This was a preference on privacy grounds; it is
  now a rule with a legal reason. Swedish marketing law reaches measures taken
  *i näringsverksamhet* that are *ägnade att främja avsättningen*
  (marknadsföringslagen 2008:486, 3 §), and alkohollagen 7 kap. bites only on
  marknadsföring. Having no commercial interest is the fact that keeps the site
  outside that definition. Taking income would supply the missing element.
  See `docs/legal-notes.md` §4d.

The bottle in the user's hand is newer than the dataset. Every wine page carries
that sentence and a link to the source page.

## What the shelf can be filtered on

The filter is the second reason people come, and it can only offer facets the
dataset actually carries. Coverage on 2026-07-27, over 15 085 wines — the count
differs from the 15 017 above because the catalog turns over daily as products
are launched and discontinued, and the fetched cache holds 63 wines that have
since left it:

| Facet | Source | Coverage | Note |
|---|---|---|---|
| Price | catalog `price` | 100% | Ordinary price incl. VAT, excl. recycle fee |
| Country | catalog `country` | 100% | 52 values, Systembolaget's own spelling |
| Category and style | `categoryLevel2/3` | 100% | The comparison set, see below |
| Assortment | `assortmentText` | 100% | 71% of the fixed range declares, 10% of order-only |
| Grape | catalog `grapes` | **57.4%** | 433 distinct, already normalised upstream |
| Food pairing | catalog `tasteSymbols` | **26.6%** | 16 values — a closed vocabulary, ideal for a facet, but thin |
| Additives | the declaration | **19.3%** | The scarce one, and the point of the site |
| Sugar and energy | detail `nutrition` | ≈ declared | Arrives with the declaration |
| Vegan, organic | `isVeganFriendly`, `isOrganic` | 100% | Supplier's own flag, not derived from the declaration — and unset means unmarked, not disqualified |
| Gluten-free | `isGlutenFree` | **0% until 2026-08-02** | Same kind of flag, but it lives on the product page, so it arrives with the Sunday refresh and is null until then |
| Buyability | catalog stock flags, detail `availableNumberOfStores` | 100% / from 2026-08-02 | See *Can you actually buy it* |

Two of these are new. Grape and price were always collected; **food pairing was
not, and is collected from 2026-07-27** — `tasteSymbols` and `usage` come free
in the same search response the catalog step already reads, so it costs no
extra request and no re-crawl. `tasteSymbols` is a controlled list of 16 values
(Fisk, Skaldjur, Lamm, Nöt, Fläsk, Fågel, Vilt, Grönsaker, Ost, Dessert,
Asiatiskt, Kryddstarkt, Buffémat, Aperitif, Sällskapsdryck, Avec/digestif);
`usage` is the prose sentence with the serving temperature, quoted, never
parsed.

**Pairing is thinner than it first looked: 26.6%, not the ~60% a sample of the
search's first pages suggested.** Those pages skew towards the fixed range,
which is tasted and described; the order-only long tail mostly is not. The
lesson generalises — every coverage figure in this table must be measured over
the whole catalog after a crawl, never sampled from the API, because the API's
default ordering is not a random sample of the shelf.

**That still leaves grape and pairing far better covered than the declaration,
and their gaps are not the same kind.** A missing declaration is a supplier
saying nothing; a missing grape or pairing is Systembolaget not filling a field.
Both hide wines from a filtered list, so both are counted in the "not shown"
line, and each gets its own reason — the user must never read "no wines match"
when the truth is "the grape field is empty for 6 454 wines."

A practical consequence of 26.6%: **pairing is a facet, not a primary
navigation.** Filtering on "till lamm" alone discards three wines in four
before the additive question is even asked. It earns its place combined with
grape, colour or price, and the results page has to say plainly how many wines
the pairing filter itself removed.

Grapes cannot be recovered from elsewhere: `rawMaterial` on the product page
fills only 303 of the 6 454 blanks, and it is free text ("Corvina, rondinella
och molinara samt övriga druvsorter"). Not worth parsing, and parsing it would
be guessing.

## Can you actually buy it

Probed against the live API on 2026-07-27, because the answer decides how much
of this is possible at all.

**What we can have, and how fresh it is:**

| Fact | Field | Source | Freshness |
|---|---|---|---|
| Sold out entirely | `isCompletelyOutOfStock` | search | nightly |
| Temporarily sold out | `isTemporaryOutOfStock` | search | nightly |
| Being delisted | `isDiscontinued` | search | nightly |
| How many stores shelve it | `availableNumberOfStores` | product page | weekly |
| Which range it belongs to | `assortmentText` | search | nightly |

`availableNumberOfStores` is the field that turns an abstract "order-only" label
into something a shopper understands. Sampled across the ranges: fixed-range
wines sit at 452, 179 and 136 stores; temporary-range wines at 2 to 7; local and
small-scale at 3 to 4; **order-only wines at 1**. That single number separates
"on a shelf near you" from "exists in a warehouse" better than the assortment
name does. It lives only on the product page, so it is at worst a week old —
acceptable, because how widely a wine is stocked moves slowly, while being out
of stock does not, and the out-of-stock flags refresh every night.

**What we cannot have: stock in a named store.** There is no store endpoint on
the API — `/site`, `/stores` and `/site/search` all 404 — and the search API
ignores every store parameter tried (`siteId`, `storeId`, `stockSiteId`: the
result count does not move). A filter called `OnlineAvailability` exists but its
vocabulary is not published, and every guessed value returns zero rows.
Systembolaget's own store-availability page is `Disallow`ed in `robots.txt`.
Even if a way were found, per-store stock for 15 000 wines across some 450
stores is not something a nightly crawler should be doing to a host it is a
guest of.

So the site does not promise store-level stock, and does not pretend to:

- **The shortlist defaults to what can be bought without waiting** — in stock,
  not discontinued, and shelved in more than a handful of stores. Order-only
  wines are not hidden; they sit in their own labelled group with the wait
  stated, because *they can be bought*, just not today. Both `isStoreOrderApplicable`
  and `isHomeOrderApplicable` are true even for the 1-store wines: order-only
  means a delay, not a dead end. That distinction, made plainly, is the whole
  fix for the annoyance this section exists to prevent.
- **Every wine says how findable it is**, in words rather than a flag:
  *finns i 179 butiker*, *beställningsvara — finns i 1 butik, tar några dagar*.
- **The final check belongs upstream.** The wine page links to Systembolaget's
  own store-availability view for that product. They own the truth about their
  shelves; we own the truth about what is declared, and we say which is which.
- **Nothing about stock is stated without its timestamp.** The dataset is built
  at 03:00; a page that says "in stock" means "in stock when we asked", and
  that sentence is on the page, not in a footnote.

## What a recommendation can honestly be

Three axes, each with a rule the user can read and a limit that is stated, not
buried.

**A. Fewest declared additives within a comparable set.** The user picks what
they were going to buy anyway — category, price band, availability — and gets
the wines in that slice that declare least. The comparison is only meaningful
inside a slice: a sparkling wine declares dosage sugar and a fortified wine
declares added alcohol, so ranking them against a still red is a category error.

**"Fewest declared additives" is the only permitted wording, everywhere.** Not
"fewest additives", not "least additives", not "utan tillsatser" — in headings,
in slugs, in titles, in share text. The word *declared* is what makes the
sentence true, so it does not get dropped for brevity.

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

**The supplier flags tilt the same way, and harder.** `isVeganFriendly`,
`isOrganic` and `isGlutenFree` are set or unset, never absent — checked across
all 15 148 cached declarations and 15 085 catalog rows, where not one is null.
That makes them look like clean booleans, and they are not: an unset flag means
*nobody marked this wine*, not *this wine is not vegan*. 822 wines carry the
vegan flag and 2 788 the organic one, so the 14 263 without are overwhelmingly
unmarked rather than disqualified. "Only vegan" is therefore a sound filter and
"not vegan" is not a category the site may offer, in the same way that excluding
a substance is sound and including it is weak. `gluten_free` is the exception
that proves the rule: it is carried as null until a wine's declaration has been
refetched, because a wine we have not asked again has told us nothing.

**C. Sugar and energy.** Nutrition figures come with nearly every declaration
(kcal, sugar per 100 ml). Useful, factual, and the one axis where a lower number
is unambiguously the thing the user asked for.

Axes B and C are where the site is genuinely useful to an individual. Axis A is
where it is interesting about the market. Do not let A's ranking swallow the
other two.

### The rule, written down

A shortlist is reproducible or it is opinion. The spec:

- **Comparison set**: category (red / white / sparkling / rosé / fortified /
  flavoured), price band, and buyability — default to wines in stock and on a
  shelf, with order-only shown as its own group rather than mixed in. Narrowed
  further, at the user's choice, by country, grape, food pairing, and
  substances to exclude or include.
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
labels it: the user chose *deklarerar inga tillsatser* and gets a ranked list of
wines that declare none, followed by the wines nobody can answer for.

**The filter is named for what it does.** *Deklarerar inga tillsatser*, never
*utan tillsatser*. The short form is a statement about the contents of the
bottle, which the site cannot make and does not know; and it goes into the URL,
the selected-state chip and anything shared from the page, which are the four
places least likely to carry the caveat. See `docs/legal-notes.md` §4f.

The same holds for the facets. A grape filter drops wines whose grape field is
empty, and says so as its own line — that gap is Systembolaget's missing
metadata, not a supplier's silence, and conflating the two would misattribute
both.

### Naming importers

Decided by the owner, 2026-07-27. The coverage page carries a table of
importers ranked by how much of their range declares — but only over the wines
where the requirement plausibly applies, and that qualifier is the whole design.

**Why the importer and not the producer — and what that does and does not
mean.** `supplier` in the dataset is Systembolaget's `supplierName`: the company
that placed the wine on the Swedish market and supplied the product text
Systembolaget publishes. That is a fact about the dataset, and it is the only
claim the table makes. Both producer and importer are in the data and both are
shown on a wine page; only the importer is ranked, because the importer is the
company whose range this is.

**It is not a claim about legal responsibility, and researching it in 2026-07-28
is why that sentence changed.** Article 8(1) of Regulation (EU) No 1169/2011
makes the responsible food business operator "the operator under whose name or
business name the food is marketed or, if that operator is not established in
the Union, the importer into the Union market". For an EU-origin wine sold under
the producer's own label — about 82% of this catalogue — that is the producer or
bottler, not the Swedish importer. The importer limb only fires for third-country
wines, and even then the dataset cannot show whether the Swedish company was the
one that brought the wine into the Union. So:

- The table may say: *this company supplies these wines to Systembolaget, and
  this share of them carries a declaration on their product pages.*
- The table may **not** say, or imply, that the named company is legally
  responsible for the declaration, is accountable for its absence, or has broken
  a rule. `/metod` states the Article 8(1) two-step rule and says which limb the
  dataset cannot resolve.

Full sourcing in `docs/legal-notes.md` §1. Who is *liable* under Swedish law when
a declaration is wrong was not established and needs a Swedish lawyer.

**The ranking is over vintage 2024 onwards — as a stand-in, not as the rule.**
The requirement applies to wine **produced** after 8 December 2023; wine produced
before that date may be sold under the old rules until stocks are exhausted
(Commission Notice C/2023/1190, Q3 and Q4; Livsmedelsverket says the same). It is
not a harvest criterion, and "the 2024 harvest onwards" is the Commission's own
shorthand for the practical consequence, not the text.

The dataset has no production, bottling or disgorgement date, and Systembolaget
does not publish one, so the criterion cannot be evaluated. Vintage 2024-onwards
is the proxy, and its error is one-sided:

- **Conservative in the right direction.** Every wine of the 2024 harvest or
  later was necessarily produced after 8 December 2023, so no importer is ever
  marked down for stock the rule does not reach.
- **Materially incomplete.** On 2026-07-28, 2 217 wines carry vintage 2023 and
  2 854 carry no vintage at all — 5 071 wines, 33.5% of the catalogue — and an
  unknown share of those is legally in scope. A non-vintage sparkling wine whose
  second fermentation happened in 2025 is covered and is invisible to a vintage
  filter.

Every page using this proxy says so in its body text, with the count, not in a
footnote. Without an importer's older stock, the correction is still the thing
that reverses the table. Measured 2026-07-27:

| Importer | All vintages | 2024 onwards |
|---|---|---|
| Johan Lidby Vinhandel | 28.8% | **97.4%** |
| The WineAgency Sweden | 21.2% | 93.4% |
| Giertz Vinimport | 82.1% | 97.3% |
| Lively Wines Sweden | 13.2% | 40.7% |
| Tryffelsvinet | 2.2% | 20.0% |

Published raw, that table would accuse Johan Lidby — who declares on 97 of
every 100 bottles the proxy touches — of being among the worst. **The raw column
is never the ranking.** It may appear beside the corrected one, labelled as
what it is (a function of stock age), or not at all.

The rest of the rule:

- **Minimum sample.** No importer is ranked on fewer than 40 wines in the
  qualifying vintages, so nobody tops or bottoms the table on four bottles.
  Those below the threshold are aggregated into one row, counted, not named.
- **The mean is on the page.** 66% of wines from 2024 onwards declare. A number
  without its baseline is an insinuation.
- **Every row is traceable.** An importer's row links to their qualifying
  wines, each with its own product page link, so the claim can be checked
  bottle by bottle — by them first of all.
- **It reports, it does not characterise.** A percentage and a count. No
  "worst offenders", no leaderboard styling, no commentary on intent. An
  importer may have reasons we cannot see.
- **Dated, and corrigible.** The table carries the date it was generated and a
  way to report an error. Coverage rises as stock rotates, so today's laggard
  is next quarter's ordinary — the page must not read as a permanent verdict.

## Pages

| Path | Purpose |
|---|---|
| `/` | Search by name or product number, and the coverage headline |
| `/vin/{product_number}-{slug}` | One wine: declaration, substances, nutrition, raw text, source link |
| `/hitta` | Shortlist builder: category, price, country, grape, food pairing, substances in or out, sugar — the recommendation |
| `/lista/{slug}` | Saved slices worth linking to, e.g. "red under 150 kr, fewest declared additives" |
| `/druva/{slug}` | One grape: how much of it declares, and which of those declare least |
| `/passar-till/{slug}` | One pairing: the same, for "till fisk", "till lamm", … |
| `/tillsats/{id}` | One substance: what it is, why it is used, which wines declare it |
| `/tackning` | How much of the shelf declares — by category, country, vintage, and importer |
| `/importor/{slug}` | One importer: their qualifying wines and what each declares |
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
  banner, which on a phone in a shop is a feature. The affiliate half of that
  rule now has a second reason; see *What the site must never say*.
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

**None of that paragraph has been verified against the judgments themselves.**
It remains an open question; see below. One adjacent provision was noted while
researching something else and is recorded so it is not missed: alkohollagen
7 kap. 5 § restricts images in *kommersiella annonser* for alcohol to a
reproduction of the product, its raw materials, single packages, or a trademark.
It bears on the bottle photographs only if the site is marketing at all, which is
itself unsettled.

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
- `catalog.py` keeps `images` as of 2026-07-27, so every record carries
  `image_base_url`. `imageModules` is still dropped: the 150-byte placeholder
  is charming but would add some 2 MB to a 16 MB dataset.

How to use that:

- **No photographs in lists or shortlists.** Forty bottle shots on a comparison
  page is forty third-party requests to answer a question about text.
- **One image on the wine page**, small, `loading="lazy"`, with explicit width
  and height and the base64 thumbnail behind it so nothing shifts. `alt` is the
  wine's name. Credit reads "Bild: Systembolaget" and links to the product page.
- **Store the URL the API gives us** rather than reconstructing the pattern, as
  `KEEP` now does. A pattern we invented is a pattern we have to maintain;
  their own answer is the source of truth.
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
2. **Shortlists.** `/hitta` with buyability first, then category, price,
   country, grape, food pairing, and substances in or out; plus the ranked
   lists at `/lista/{slug}`. This is the recommendation and the reason the site
   exists, so it carries the buyability rules from its first day rather than
   gaining them later. It is where the honesty rules earn their keep. The
   ranking is always inside a stated slice — there is no single global "fewest
   declared additives in Sweden" table, because a sparkling wine and a still red
   are not comparable and a leaderboard would say they were.
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
- ~~**Are suppliers named on the coverage page?**~~ Settled 2026-07-27: yes,
  importers are named, under the rules in *Naming importers*.
- ~~**Public or private dataset?**~~ Settled 2026-07-27: private for now, but
  written throughout as if already public, since making it public exposes the
  whole history and not just the current tree.
- ~~**The quality gate.**~~ Settled 2026-07-27: it watches drift rather than an
  absolute level, so the figure the site publishes is the measured share of
  unread declarations, not a target anyone is grinding towards. `/metod` states
  it plainly and dates it.
- ~~**Verify who carries labelling responsibility** — importer or producer —
  before the importer table goes live.~~ Researched 2026-07-28,
  `docs/legal-notes.md` §1. **The answer moved the plan**: under Article 8(1) of
  Regulation (EU) No 1169/2011 it is the producer/bottler for EU-origin wine and
  the EU importer only for third-country wine, so the table's justification was
  rewritten to a factual one. Two things remain open and are the owner's to take
  further: **who is liable in Sweden when a declaration is wrong** (not
  established, needs a Swedish lawyer), and whether naming importers is
  defensible at all under förtal and marknadsföringslagen (not researched — that
  is a separate question below).
- ~~**The requirement covers the 2024 harvest onwards.**~~ Corrected 2026-07-28:
  it covers wine **produced** after 8 December 2023. Vintage is a proxy the
  dataset is stuck with, it is conservative but leaves a third of the catalogue
  uncounted, and every page that uses it must say so. See *Naming importers* and
  `docs/legal-notes.md` §1f–1g. **`README.md` still states the harvest version
  and needs the same correction.**
- **Is the site marketing at all?** Researched 2026-07-28 and **not resolved**.
  Alkohollagen 7 kap. bites only on *marknadsföring*, which marknadsföringslagen
  3 § defines as measures *i näringsverksamhet* that are *ägnade att främja
  avsättningen*. A site with no income fails the first element on its face, and
  Regulation (EC) No 1924/2006 likewise applies only to "commercial
  communications". But no fetched case or guidance draws the line for an
  independent information site, and the one decided alcohol case found
  (Mackmyra ./. KO) concerned a producer promoting its own goods. **Needs a
  Swedish lawyer before launch.** See `docs/legal-notes.md` §4d.
- **Wording review before launch.** Still open, and now narrower. The health
  claims regime bars *health claims* on beverages over 1.2% abv without
  exception, and the CJEU reads "health claim" to include any implication of
  reduced harm (*Deutsches Weintor* C-544/10) — but only in commercial
  communications, which loops back to the question above. What research settled:
  the phrase *utan tillsatser* is out, *fewest declared additives* is the only
  permitted form, and the never-say rules now cover implication by layout and by
  URL, not just by sentence. What it did not settle: whether a ranked list is
  itself an implied claim regardless of its wording. See
  `docs/legal-notes.md` §4c and §4f.
- **May the site hotlink Systembolaget's bottle photographs?** Not researched.
  The *Bottle photographs* section above states a position from memory of the
  CJEU cases, which is exactly the kind of thing that is wrong when recalled
  rather than read. Nothing should be built on it until the judgments and
  Systembolaget's own terms have been fetched.
- **Is naming importers defensible?** Not researched. Förtal (brottsbalken
  5 kap.) as it applies to statements about companies, and whether a comparison
  of named companies could be read as comparative advertising under
  marknadsföringslagen (2008:486), are both untouched. The *Naming importers*
  rules were written to be careful; nobody has checked whether careful is enough.

# Site plan — vindeklaration.se

How people are meant to use the site, and what it may and may not tell them.
Written 2026-07-26, before any site code exists. Figures are a snapshot of that
day and will age; the shape of the argument will not.

Where this plan makes a claim about what the law requires, the evidence is in
`docs/legal-notes.md`, with the source fetched and quoted. That file is not legal
advice and neither is this one. Several of its findings end in "needs a Swedish
lawyer", and two of those reach past this plan entirely: whether the crawl the
dataset is built from is permitted by Systembolaget's terms of use, and whether
the catalogue is a protected database. See *Open questions* at the end.

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
- Anything that could make Systembolaget look like the sender of, or a party
  behind, what this site says. Their linking guidelines make this their central
  condition and repeat it twice, and it binds whether or not the site is
  commercial. Every page that links to them says plainly that it is independent of
  them and that ordering, purchase and collection happen at Systembolaget. See
  *Bottle photographs* and `docs/legal-notes.md` §2e.
- That a named importer is legally responsible for a declaration, is accountable
  for its absence, or has broken a rule. The table reports what
  systembolaget.se published on a stated date. See *Naming importers*.
- **Today: no advertising, no affiliate links, no sponsorship, no paid
  placement, no commercial income of any kind.** This began as a preference on
  privacy grounds and acquired a legal reason. Swedish marketing law reaches
  measures taken *i näringsverksamhet* that are *ägnade att främja avsättningen*
  (marknadsföringslagen 2008:486, 3 §), and alkohollagen 7 kap. bites only on
  marknadsföring. Having no commercial interest is the fact that keeps the site
  outside that definition.
  **The owner intends to introduce advertising later** — sponsored links,
  placements or banners — and stated so on 2026-07-28. That is a legitimate
  plan and this document does not argue against it. It is recorded here because
  it is the single change that alters the most: see *When the site takes
  income*. Until it happens, the sentence above is the current state of the
  site and holds.

## When the site takes income

The owner expects to run wine advertising eventually — sponsored links or
placements, banners, some small revenue. Decided in principle 2026-07-28, not
current. Nothing here is an argument against it; it is the list of what changes
on the day, written while nobody is under time pressure.

**The change is not one of degree.** Every regime researched so far turns on a
single unanswered question — is the site acting *i näringsverksamhet* — and
today the honest answer is that it plainly is not, because there is no income
and no commercial interest. Advertising revenue does not make that question
harder to answer. It answers it, the other way, and it does so for **five
regimes at once** (`docs/legal-notes.md` §4d, §3e):

| Regime | What engages |
|---|---|
| Alkohollagen 7 kap. | *särskild måttfullhet* in all alcohol marketing; format and content rules |
| Regulation (EC) 1924/2006 | Art. 4(3) bars **all** health claims on >1.2% abv drinks, without exception |
| Marknadsföringslagen 18 § | rules on comparative advertising — which is what the importer table becomes |
| Varumärkeslagen 1 kap. 10 § | use of others' marks in a commercial context |
| Systembolaget's user terms, clause 4 | the commercial limb of their linking permission |

The rankings are the exposure. A "fewest declared additives" list is a
defensible piece of consumer information published by someone with nothing to
gain. The same list, on a page carrying paid wine advertising, is a promotional
comparison of alcoholic beverages by a party with a commercial interest — and
*Deutsches Weintor* (C-544/10) holds that a health claim covers any implication
of reduced harm, proscribed without exception. The list would not have changed.
Its legal character would.

Consequences worth deciding before, not after:

- **Take it to a Swedish lawyer first.** This is the point where the accumulated
  "needs a lawyer" findings stop being theoretical. Doing it before the first
  revenue is cheap; doing it after is a remediation.
- **Separate the money from the ranking, visibly and structurally.** No
  advertiser may appear in, above, adjacent to, or be excluded from a ranked
  list. If an importer can pay to affect what a list shows or how it reads, the
  dataset's whole claim collapses — and that claim is the only asset here.
- **The wording review becomes mandatory rather than advisable.** Under 1924/2006
  the margin for an implied health claim goes to zero.
- **The importer table needs re-examining.** A named comparison of companies
  published by a commercial actor is a different act from the same table
  published by a non-commercial one.
- **Privacy need not follow the money.** No accounts, no cookies, no analytics
  is an independent commitment and advertising does not require breaking it —
  but the ad formats that respect it are a smaller set, and that is a choice to
  make deliberately.
- **Say so on the page.** Whatever is decided, `/metod` states plainly how the
  site is funded and what the funding may and may not influence.

The cheapest version of all this: keep the rankings on pages that carry no
advertising at all, and put the revenue somewhere it cannot touch them. Whether
that is workable is a business question, not a legal one, and it is the owner's.

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
  **Re-check that link before building it.** `/hamta-i-butik/` is `Disallow`ed in
  their `robots.txt`, and their linking guidelines forbid linking to material that
  sits behind an account. A link to the ordinary product page is not in doubt; a
  link into the store-availability view is. See `docs/legal-notes.md` §2j.
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

**Naming a company is not the same act as naming a person, and the law treats
them completely differently.** Researched 2026-07-28, `docs/legal-notes.md` §3.
Förtal under brottsbalken 5 kap. does not reach a statement about an aktiebolag —
SOU 2016:7 p. 410: *"Förtal kan inte riktas mot juridiska personer, utan endast
fysiska personer kan vara målsägande."* For the companies in the table there is no
defamation exposure to manage. But NJA 1950 s. 250, reported on the same page,
held a man personally identified because his name was part of the company's firma,
and **this dataset contains supplier names that are personal names** — Jessica
Mihai, Josefin Lagerhorn, Staffan Ottosson and others. For those, förtal is
available and truth alone is not a defence: 5 kap. 1 § requires both that it was
*försvarligt* to publish and that the statement was true or had *skälig grund*.

The rest of the rule:

- **A supplier who is or may be a natural person is never named in a ranking, at
  any sample size.** Today's 40-wine threshold happens to exclude every one of
  them — of the 19 suppliers reaching 40 qualifying wines on 2026-07-28, all are
  registered companies — but that is an accident of the current catalogue, not a
  safeguard. This is a separate rule and does not depend on the threshold.
- **Minimum sample.** No importer is ranked on fewer than 40 wines in the
  qualifying vintages, so nobody tops or bottoms the table on four bottles.
  Those below the threshold are aggregated into one row, counted, not named.
  This is a statistical honesty rule, not a legal shield; no source requires it.
- **The mean is on the page.** 66% of wines from 2024 onwards declare. A number
  without its baseline is an insinuation.
- **Every row is traceable.** An importer's row links to their qualifying
  wines, each with its own product page link, so the claim can be checked
  bottle by bottle — by them first of all.
- **Every row says what was measured.** Not what the company did: what
  systembolaget.se published on a stated date. That is the §1 correction and it is
  also the strongest form of the claim, because it is a fact the project measured,
  cached and can reproduce.
- **It reports, it does not characterise.** A percentage and a count. No
  "worst offenders", no leaderboard styling, no commentary on intent. An
  importer may have reasons we cannot see. This one is load-bearing: förtal is
  committed by pointing someone out as *klandervärd* or giving information *ägnad
  att utsätta denne för andras missaktning*. A bare percentage is not that;
  "worst offenders" would be.
- **Dated, and corrigible.** The table carries the date it was generated and a
  way to report an error, with a stated response time. Coverage rises as stock
  rotates, so today's laggard is next quarter's ordinary — the page must not read
  as a permanent verdict.

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
copyright law treats the two acts. **Researched and verified 2026-07-28 against
the judgments themselves; full quotation in `docs/legal-notes.md` §2b–§2d.**

A photograph is protected in its own right — in Sweden even a plain snapshot gets
50 years under 49 a § URL — and the rights sit with Systembolaget or a third
party, not with us. Embedding an image the rightsholder has made freely
available, with no technological restriction on it, is not a communication to the
public requiring authorisation: *Svensson* (C-466/12) ruling 1, and *BestWater*
(C-348/13), which decides framing specifically. Framing it so the image looks like
part of our page changes nothing (*Svensson* §29). Copying it to our own host and
serving it from there **is** a new communication to the public (*Renckhoff*
C-161/17, operative part) — and *Renckhoff* §36 adds that it makes no difference
that the rightsholder placed no restriction on downloading. Hotlinking is
therefore the conservative choice here, not the cheeky one.

The line falls at a **technological measure**, and only there. *VG Bild-Kunst*
(C-392/19) holds that embedding which circumvents measures adopted or imposed
against framing is a communication to the public — and §46 holds that a
rightsholder "cannot be allowed to limit his or her consent by means other than
effective technological measures". So if hotlink protection appears, the images go
away. They do not get proxied, and they do not get cached "just this once".

**Two things this research did not settle, recorded so they are not lost.** The
CJEU cases interpret Article 3(1) of Directive 2001/29, which covers *works*;
whether they carry across to the purely Swedish neighbouring right in 49 a § URL
for a photograph that is not a work is unestablished. And nobody knows which
images belong to Systembolaget and which to a supplier. One adjacent provision
also stands: alkohollagen 7 kap. 5 § restricts images in *kommersiella annonser*
for alcohol to a reproduction of the product, its raw materials, single packages,
or a trademark. It bears on the bottle photographs only if the site is marketing
at all, which is still unsettled.

**Systembolaget has published its own position, and it is close to a permission.**
<https://www.systembolaget.se/om-lankning/>, fetched 2026-07-28:

> "Enligt EU-domstolens praxis kan Systembolaget på upphovsrättslig grund inte
> hindra att någon länkar (genom s.k. hypertextlänkar eller inbäddade länkar) till
> upphovsrättsligt skyddat material vilket med Systembolagets tillstånd ligger
> fritt tillgängligt på Webbplatsen."

*Inbäddade länkar* — embedded links, in terms. But the same page attaches
conditions, and they are the price of relying on it.

### The conditions, and they are requirements rather than preferences

Each is sourced in `docs/legal-notes.md` §2j.

- **Never copy, proxy, re-host or server-side resize.** Render from
  `product-cdn.systembolaget.se` or show no image.
- **If any technological measure appears, the images go the same day.** A referrer
  check, a token in the URL, a 403 on a foreign origin — any of these. Do not work
  around it. **The weekly image sample below is what enforces this**, not merely a
  404 check, and it is the mechanism that keeps the legal premise true.
- **Never link to or embed anything behind a login.** Systembolaget's guidelines
  forbid linking that lets a user "kringgå begränsningar", and say expressly that
  linking to lists on their site is not allowed because those sit behind an
  account. See the caveat added to *Can you actually buy it*.
- **Every page carrying an image links to that wine's product page.** Their
  guidelines permit "extern länkning … till produktsidor" in those terms.
- **Every page that links to Systembolaget says Systembolaget is not the sender of
  and does not stand behind anything on this site.** In the body, in both
  languages, not only on `/metod`. Their guidelines say this twice, and it is the
  risk they are most explicit about.
- **Every page that links to Systembolaget says that ordering, purchase and
  collection happen at Systembolaget.** This is a literal requirement — "ska …
  tydligt framgå … att beställning, köp och utlämning sker från/av/hos
  Systembolaget" — it applies to *any* link and not only to image links, and this
  plan previously had no such sentence anywhere.
- **The credit is not "Bild: Systembolaget" without further thought.** Their
  guidelines say that when linking "får du inte använda dig av Systembolagets
  immateriella rättigheter, t.ex. Systembolagets firma, varumärken…". Identify the
  source in plain words; never reproduce their logo, wordmark or any Systembolaget
  symbol.
- **No image on any ranked, filtered or comparison page.** Already the rule below
  for performance reasons. It has a second reason now: a bottle photograph beside
  a ranking is where the endorsement risk and the implied-claim risk are sharpest.
- **`/metod` records these conditions and the date the CDN was last checked**, so
  the premise of the whole analysis is visible and falsifiable.

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
- ~~**May the site hotlink Systembolaget's bottle photographs?**~~ Researched
  2026-07-28, `docs/legal-notes.md` §2. The five judgments were fetched and read.
  **Embedding is not copying and the line falls at a technological measure**
  (*Svensson*, *BestWater*, *VG Bild-Kunst* §46); copying to our host would be
  infringement (*Renckhoff*). Systembolaget's own linking page concedes embedding
  in terms. The *Bottle photographs* section above is rewritten with the
  conditions that come attached. Two residues remain open and are the owner's:
  whether the CJEU's Article 3(1) case law reaches the purely Swedish
  neighbouring right in 49 a § URL, and who actually owns the photographs.
- ~~**Is naming importers defensible?**~~ Researched 2026-07-28,
  `docs/legal-notes.md` §3. **Förtal does not reach a company at all** (SOU 2016:7
  p. 410), so for the aktiebolag in the table there is no defamation exposure.
  Marknadsföringslagen 18 § binds "en näringsidkare … i sin reklam" and so hangs
  on the same unresolved threshold as everything else. **The answer moved the
  plan**: the dataset contains suppliers whose names are personal names, förtal
  *is* available to them, and a new rule now excludes them from any ranking
  independently of the 40-wine threshold.
- **Does the project's own crawl breach Systembolaget's terms of use?** Found
  2026-07-28 while researching the images; `docs/legal-notes.md` §2f. Clause 1.7
  of their Allmänna användarvillkor (version 2026-04-21) prohibits using
  "crawlers eller spindlar … för att samla in information från eller om
  Webbplatsen … i syfte att tillhandhålla funktioner eller tjänster relaterat till
  marknadsföring av, eller **information om** alkoholdrycker". That describes this
  project, and unlike their intellectual-property clause it carries **no
  commercial qualifier**, so being non-commercial does not sidestep it. Whether a
  browsewrap term binds a client that never created an account, and what would
  follow if it does, was not established. **`robots.txt` is not the whole
  permission set and this plan, `README.md` and `CLAUDE.md` have all been treating
  it as if it were.**
  **Decided by the owner 2026-07-28: the crawl continues.** The reasoning is
  that Systembolaget publishes a product API for use and a `robots.txt` reading
  `Allow: /`, and that a clause forbidding what those two invite is internally
  contradictory. That is a judgement about the site owner's evident intent, not
  a resolution of the clause — the wording stands unchanged and the browsewrap
  question is still unanswered. It remains worth putting to a lawyer, and it
  becomes materially more pressing if the site takes income, since clause 4 of
  the same terms engages then. The crawling discipline in `CLAUDE.md` —
  sequential, 0.4 s apart, self-identifying, never accelerating after an
  outage — is what makes the decision defensible in practice and is not
  negotiable.
- **Is the dataset itself someone else's database?** Not resolved;
  `docs/legal-notes.md` §2i. Upphovsrättslagen 49 § protects a compilation "i
  vilket ett stort antal uppgifter har sammanställts **eller** vilket är resultatet
  av en väsentlig investering" — alternatives, not cumulative — for fifteen years.
  *British Horseracing Board* (C-203/02) holds that public accessibility is no
  defence, and that repeated small extractions whose cumulative effect
  reconstitutes the database are caught. The text-and-data-mining exception in
  15 a § URL does not obviously help, because it forbids keeping the copies longer
  than the mining needs and forbids using them for another purpose, and this
  project does both. Needs a Swedish lawyer.
- **Is the site acting *i näringsverksamhet*?** This was already open under
  *Is the site marketing at all?* above. It is recorded again here because
  research has now shown it gates **five** separate regimes rather than one:
  alkohollagen 7 kap. (via marknadsföringslagen 3 §), Regulation (EC) No 1924/2006
  Article 1(2), marknadsföringslagen 18 § on comparative advertising,
  varumärkeslagen 1 kap. 10 §, and clause 4 of Systembolaget's user terms. See the
  table in `docs/legal-notes.md` §3e. **It is the single highest-value question to
  put to a lawyer** — one answer closes five exposures.
- **Are supplier names that are personal names personal data?** Partly settled
  2026-07-28. The collision with `CLAUDE.md` was a misreading of that rule: it
  protects the **owner's** data, not third parties'. Carrying sole traders'
  names in `supplier` is approved — the values are public business information,
  quoted verbatim from the source, and stripping them would misattribute the
  wines. `CLAUDE.md` now says so, so no future session re-opens it.
  **What is not settled is publishing a compliance statistic about them.**
  Naming a company in the importer table and naming a natural person are
  different acts: förtal reaches the second and not the first, and truth alone
  does not acquit under BrB 5:1. **No GDPR analysis has been done**, and
  Bolagsverket has not been queried to confirm which entries are enskilda
  firmor. Today the 40-wine threshold keeps all of them out of the table, but
  that is this quarter's catalogue rather than a safeguard. See
  `docs/legal-notes.md` §3c and the natural-person rule in *Naming importers*.

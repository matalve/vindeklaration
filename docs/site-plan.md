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
- **That a substance is harmful.** Added 2026-08-02, after an audit of the
  `E129` substance page found the rule above bans claims in one direction only.
  Nothing in this list forbade a statement of *harm*, and the site had
  published one without noticing it had crossed anything. The site describes
  what a substance does — its function, its legal status, whether it must be
  declared as an allergen — and never what it does to a body. The asymmetry is
  visible in the dictionary already and is the settled practice this bullet
  writes down: sulfites are the one substance with a widely believed consumer
  reaction, and their note says only that they preserve wine and must be
  declared.
  **Quoting a legally mandated warning is a different act and would be
  allowed**, because it is reporting rather than asserting, and making mandated
  disclosure comparable is what the site is for. Four conditions, and the E129
  note failed all four in the two days it existed. The statutory wording must
  be **quoted verbatim, not paraphrased** — the note had translated the English
  back into Swedish and produced a near-miss, which reads as the site's own
  words about a health effect rather than as a quotation. The instrument must
  be **named**, so the sentence has a visible author who is not us. It must
  appear on **every substance the requirement reaches, or none** — Annex V to
  Regulation (EC) No 1333/2008 covers six colours, the dictionary carries
  three, and the warning sat on one, so the page silently told a reader that
  the wine declaring one warning-colour had a problem while saying nothing
  about the wine declaring two. **Presence is a signal independent of content.**
  And the note must say **whether the requirement actually reaches the
  product**, which is where the first version collapsed: Commission Regulation
  (EU) No 238/2010 exempts beverages above 1,2 % alcohol by volume, on the
  reasoning that they "are not intended for consumption by children". Every
  wine in this dataset is above that threshold, so the site had published a
  health-adjacent warning that applied to nothing it lists.
  **The warning is named on all three pages anyway. Decided by the owner
  2026-08-02**, after the correction: a reader is entitled to know what is in
  the glass even where the label is not required to say it. That is a decision
  about scope, not a licence to drop the conditions — the note carries the
  requirement *and* the exemption *and* the exemption's reason, because
  "beverages over 1,2 % are exempt" on its own invites the reading that the
  colour was found harmless in alcohol, which is not what 238/2010 says. The
  exemption is about who drinks it, not about what the substance does.
  The lesson is not only about health claims. The base act said what the note
  claimed; a 2010 amendment reversed it, and the amendment is not what a search
  finds first. **A regulation is not verified until the consolidated text or
  the amending acts have been read** — see `docs/legal-notes.md` for the same
  discipline applied elsewhere.
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
| Additives | the declaration | **20.4%** | The scarce one, and the point of the site |
| Sugar and energy | detail `nutrition` | ≈ declared | Arrives with the declaration |
| Vegan, organic | `isVeganFriendly`, `isOrganic` | 100% | Supplier's own flag, not derived from the declaration — and unset means unmarked, not disqualified |
| Gluten-free | `isGlutenFree` | **useless for wine** | Verified 2026-08-03 against the live API: the field works — it is `true` on beers sold as glutenfri — but Systembolaget sets it on no wine at all, `false` on all 14 858 fetched. Never show it. `false` here means *not marked*, not *contains gluten* |
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
wines without additives.** A wine that declares nothing is not evidence of an
empty bottle; it is an absence of evidence, and the site says which of the two
it is on every row.

**An additive filter — include or exclude — applies to block 1 and to nothing
else.** Corrected 2026-07-31: this section previously said blocks 1 and 2,
which contradicted *Exclusions and inclusions* above. Excluding is sound only
where the declaration was read in full — a wine that declared everything and did
not list the substance genuinely does not contain it. Block 2 is by definition
the wines whose declaration was **not** read in full, so a wine whose unread
fragment is `sulfiteraskorbinsyra` would have survived a filter for wines
without sulphites and appeared under a heading the reader reached by asking for
exactly that.

So the pattern is uniform, which is also why it is easier to explain: **the
filter ranks block 1, and labels blocks 2 and 3 without touching them.** Neither
can confirm or deny a choice — one because the text could not be read, the other
because there is no text — so filtering either would answer a question they
never got to answer. The user chooses *deklarerar inga tillsatser* and gets a
ranked list of wines that declare none, then the wines whose declaration nobody
could finish reading, then the wines nobody can answer for.

Every wine that leaves the catalogue on the way to the page gets its own line:
stock, grape, pairing, and the substance choice. Summing them, or omitting one,
leaves a total that reconciles against nothing else on the site.

**The filter is named for what it does.** *Deklarerar inga tillsatser*, never
*utan tillsatser*. The short form is a statement about the contents of the
bottle, which the site cannot make and does not know; and it goes into the URL,
the selected-state chip and anything shared from the page, which are the four
places least likely to carry the caveat. See `docs/legal-notes.md` §4f.

The same holds for the facets. A grape filter drops wines whose grape field is
empty, and says so as its own line — that gap is Systembolaget's missing
metadata, not a supplier's silence, and conflating the two would misattribute
both.

### Two sources, and which one wins

Decided by the owner 2026-07-28. Systembolaget's product page is not the only
place a declaration lives. Regulation (EU) 2021/2117 lets the obligation be met
through an **e-label** behind a QR code, so a wine showing nothing on
systembolaget.se may be fully declared at its producer. `declaration-finder`
looks for those; they land in `data/producer-declarations.json`.

**The producer's declaration ranks above Systembolaget's**, because the producer
is nearer the source. Systembolaget transcribes what a supplier sent them; the
producer wrote it. Where the two disagree, the producer's text is the one the
site uses — unless it is obviously wrong or misleading, in which case neither is
used and the wine is flagged rather than resolved.

**Both are always shown.** This is not a replacement, it is a precedence order,
and the reader has to be able to see both and where each came from. A wine page
carries the declaration in use, the other one beneath it, and a source line for
each. Never merge two texts into one list.

Conditions, because precedence without them would be a licence to guess:

- **The vintage must match exactly.** This is not a formality. The first batch
  found vintage mismatch to be the single largest rejection cause: producer
  sites show the current release while Systembolaget's stock runs a year
  behind. A producer's 2025 text has no authority over a 2024 bottle.
- **"Obviously wrong or misleading" is a narrow escape hatch, not a judgement
  seat.** It covers a declaration that contradicts itself, one that is plainly
  for a different product, or one that omits a substance the Systembolaget text
  names outright. It does **not** cover a difference we merely find surprising.
  When it fires, the wine is shown with both texts and no parsed count — the
  same treatment as `partial`. Deciding between two plausible declarations by
  judgement is the guessing the project forbids.
- **A conflict is a finding, not an inconvenience.** Two sources disagreeing
  about what is in a bottle is exactly the kind of thing this dataset exists to
  surface. Count them, and put the number on the coverage page.
- **Provenance survives into the data.** A record says which source its parsed
  additives came from. Any figure the site publishes can be recomputed for
  either source alone.

Rankings may use producer-sourced declarations, since under this rule they are
the better evidence — but a list must be able to say how many of its entries
rest on each source, and the coverage page reports the two separately. The
dataset's claim is no longer "everything traces to systembolaget.se"; it is
"everything traces to a named source, shown on the page".

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

- **A supplier who is a natural person is ranked on the same terms as a
  company. Decided by the owner 2026-07-29**, reversing the rule written the
  day before. The reasoning: someone who supplies wine to Systembolaget under
  their own name is doing so as a business, and the table reports a fact about
  that business. Excluding them would mean the smallest suppliers are the only
  ones the site never examines, which inverts who transparency is for.
  What that decision carries, so it is not carried unknowingly: förtal reaches
  a natural person where it does not reach a company (SOU 2016:7 p. 410), and
  under BrB 5:1 second paragraph truth alone does not acquit — it must also
  have been *försvarligt* to publish. A dated, sourced compliance statistic
  published as consumer information has a strong claim to that, but it is a
  claim and not a certainty, and the owner has decided against taking legal
  advice at this stage (`docs/legal-notes.md` §3c).
  **The practical effect today is nil.** The largest natural-person supplier
  has 6 wines against a 40-wine threshold, so none of them can reach the table
  as it stands. The decision matters when the catalogue changes, not now — and
  the rules below carry the weight in the meantime.
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
- **No accounts, no cookies, no affiliate links — and one measurement.**
  Decided 2026-07-29: **Cloudflare Web Analytics is used.** It sets no cookie
  and builds no cross-site profile, so there is still no cookie banner, which
  on a phone in a shop is a feature. The affiliate half of that rule now has a
  second reason; see *What the site must never say*.
  The honest accounting, because `/metod` has to state it: the beacon is a
  second third-party request alongside the bottle photograph, and it sends the
  page and the visitor's IP to Cloudflare. **It adds no new party.** Cloudflare
  serves the site, so they already see every request; the beacon gives them
  page-level detail they could largely infer from their own logs. That is a
  smaller change than adding a measurement provider from outside would have
  been, and it is still a change, and the page says so rather than describing
  the site as measurement-free.
- **Substance pages carry the aliases** — including the misspellings found in
  real declarations. Someone searching the exact string from a label should
  land on the right page.

## Presentation

The site is deliberately plain, and the constraints below are the reason rather
than the taste: system fonts, no web fonts, no third-party request from any
template, and it has to be readable on a phone in a shop on a bad signal. The
no-colour rule at the top of `templates/site.css` is the load-bearing one —
green on "declares no additives" would say healthy and red on "declares
nothing" would say guilty, so the three states differ by border and weight
instead.

**Done, 2026-08-03 to 2026-08-05.**

- **The vintage figure on `/tackning`**, built 2026-08-05 and audited twice.
  Bars rather than a line, because the vintages are separate groups with
  separate denominators and a rising line is the shape that gets read as a
  grade. One fill for every bar; where the requirement starts is an annotation
  and not a second colour. The two audits are worth reading before touching it:
  the first found the in-figure label claiming the requirement *starts* at 2024,
  which the page body denies; the second found that the sentence saying the
  rise is not improvement had been left as the last clause of the smallest,
  greyest text under the loudest thing on the page. **Text inside the viewBox
  scales with it** — 12 user units renders at 6 px on a phone — so anything a
  reader must read lives in HTML beside the figure, not in it.

- **The theme follows the operating system**, with a three-segment control at
  the right of the header that can take the decision and hand it back. Light is
  not the base and dark is not the base; the reader's device is. Nothing is
  stored until they choose.
- **Icons are one inline sprite**, monochrome, `currentColor`. They are
  navigation and nothing else — *What the site must never say* names icons
  among the places a claim gets made without a sentence, so none marks a
  declaration state, a substance or a ranking. **A symbol nothing references
  costs its own size on all 15 000 pages**: dropping two unused ones took 4.6 MB
  off a build.
- **The front page says what it is for** before it shows a search box, and the
  three doors under it each explain themselves in a sentence. No counts on
  them: a number beside a door invites being read as a score.
- **The language link is a flag**, with its words kept for a screen reader,
  since a flag names a country and not a language.
- **The wordmark is a serif from the reader's own machine.** A web font would
  be the first bytes this project ever asked a browser to fetch for decoration.
- **The icon is drawn by `tools/make_icons.py`** on a 16-unit grid so the
  tab-strip size lands on whole pixels. Its ink is `--accent`, and a test keeps
  the two from drifting.

**Outstanding.**

- **Rhythm on the wine page.** The declaration, the nutrition table and *where
  to find it* are typographically identical, so nothing signals which one the
  page is actually about.
- **Typographic hierarchy generally.** Headings and body sit in one grey scale;
  the pages have sections but no visible order among them.
- **A `_headers` file with a Content-Security-Policy** naming
  `product-cdn.systembolaget.se` as the only image source and
  `static.cloudflareinsights.com` as the only script source, which would turn
  the `/metod` paragraph from a promise into something the browser enforces.
  Listed here rather than only in `docs/deploy-site.md` because it is a claim
  the site makes about itself.

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
`additives.yaml`; UI strings live in `templates/strings.json`. Declarations
themselves are never translated — they are quoted, in the language the supplier
wrote them.

**Wine pages are Swedish only for now. Decided 2026-07-29, and it is a hosting
constraint rather than a change of intent.** Two languages across 15 047 wines
is 30 101 files, and Cloudflare Pages caps a deployment at 20 000. Swedish-only
wine pages bring the build to 15 054 files and 36 MB, which fits. The front page
and `/metod` stay bilingual, and English search results link to the Swedish wine
pages, which the English front page states plainly rather than leaving the
reader to discover.

What it costs, so that nobody has to rediscover it:

- **Journey 3 is the one that suffers** — someone arriving from a search engine
  on "metavinsyra" in English reaches a Swedish page. That journey was one of
  the six the site is built for.
- The substance pages in phase 3 are where English matters most, and they are
  few. They should be bilingual from the start regardless of this decision.

What lifts it: the wine page could carry both languages in one document, or the
sharded-HTML plan in *The file-count ceiling* below removes the count as a
constraint altogether. A paid Workers plan would also raise the ceiling to
100 000 assets, and is deliberately not the answer — see that section. Neither
needs deciding now, and `WINE_PAGE_LANGUAGES` in `src/site.py` is the one line
that changes when it is.

## The file-count ceiling

A Worker on the free plan rejects more than 20 000 static assets, and the build
fails on purpose above 19 000 — the mechanics are in `docs/deploy-site.md`.
The build on 2026-08-29 is 15 345 files, of which 15 146 are wine pages. **The way past it
is architecture, not a paid plan. Decided 2026-08-03.**

The count does not come from the dataset. `wines.json` is a single file and is
never uploaded to Cloudflare at all; the files are pre-rendered HTML, one per
wine URL. Packing the data more tightly changes nothing, because the count
follows the URL space and not the storage format. Three properties hold today:

1. fully static — no code runs at request time
2. one URL per wine
3. real HTML without JavaScript, indexable and readable with scripts off

Any two are cheap. All three together mean one file per wine, so exactly one has
to give.

**Give up (1): sharded HTML behind a Worker script.** The build renders wine
pages exactly as it does now — Jinja stays the only renderer — but packs them
into 64–256 shard files instead of writing one directory per wine. The Worker is a
lookup and nothing more: slug → shard id → `env.ASSETS.fetch(shard)` → return
the stored HTML verbatim. No second renderer in JavaScript means no template
drift to discover months later, which is the trap that makes most
render-at-request rewrites expensive. The build drops to roughly 250 files and
the ceiling stops being a subject.

Measured against the live build on 2026-08-03: 50.8 MB of wine HTML, 3 355 B per
page, and 163 B per page gzipped in bulk over a 2 000-page sample — the pages
resemble each other closely enough that gzip dedupes hard across a shard.
Extrapolated, the whole set is about 2.5 MB compressed, against a 25 MiB
per-asset limit. The routing needs no configuration: Cloudflare serves a
matching asset without invoking the Worker and only falls through to the script
when no asset matches, which is what `/vin/{slug}` becomes. `run_worker_first`
is the wrong switch here and would make every request billable.

What it costs, so that nobody has to rediscover it:

- **Every wine page view becomes a billable Worker request.** Static assets are
  free and unlimited; Worker requests are 100 000 a day on the free plan. A full
  search-engine crawl of every wine page fits inside one day with margin rather
  than with room to spare.
- **`not_found_handling: "404-page"` stops covering `/vin/`.** The Worker has to
  serve the 404 page itself for a slug it cannot find — which is exactly the
  case `wrangler.jsonc` already names as the most likely 404 this site will ever
  serve.
- A JavaScript layer in a deploy chain that renders nothing today.

If the request budget ever binds, the escape is a split rather than a plan
upgrade: keep the ~2 900 declared wines as static files and shard only the
~12 200 undeclared ones. That is about 3 100 files, and when the budget runs out
it is the tail that returns 429 rather than the pages people link to. Start
undivided; take the split only when the budget is the binding constraint.

**The two branches not taken**, written down so they are not re-proposed:

- **Give up (3), render on the client.** One shell for `/vin/*` plus JavaScript
  that fetches the shard. It solves the count without spending a single Worker
  request, but the wine page is then empty to a search engine and to a reader
  with scripts off. Journey 3 already loses the English wine page; this would
  take the rest of it.
- **Give up (2), publish fewer URLs.** A page only for wines that declare —
  about 3 000 files, still fully static, no new moving parts. But the undeclared
  pages carry the `findability()` result: where declaration-finder looked and
  what it did not find. That absence is one of the project's own findings, not
  filler around a blank.

None of this is built. It is the plan for when the margin closes, and there is
no sign yet that it is closing: `data/quality-history.json` has the assortment
between 14 877 and 15 174 across the eight days it has recorded, noise around
15 000 with no direction. Eight days is too short to call it flat, but nothing
in it points up, so this is work to schedule rather than work that is late.

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
crawler, so it does not conflict with the one-crawler rule. **Live**, deployed
as a Cloudflare Worker with static assets that builds straight from this
GitHub repository — see `docs/deploy-site.md` for the mechanics. The domain
is registered at a Swedish registrar, since `.se` needs one, but its DNS
points at Cloudflare.

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
   **Built 2026-08-01, except the importer table.** `/tillsats/{id}` for every
   substance that appears in a declaration — 73 of them, in both languages,
   with the E-number, the bucket, the dictionary's note where there is one and
   an explicit blank where there is not, and the aliases including the
   misspellings. `/tackning` carries the whole-shelf share, the share over the
   certainly-covered vintages, and breakdowns by category, country and vintage,
   with groups under 40 wines aggregated into a counted, unnamed row.
   **The importer table went live on 2026-08-29.** The rule in *Naming
   importers* requires every row to be "dated, and corrigible" — a way to
   report an error, with a stated response time. The site's only error channel
   is the GitHub issue tracker linked from `/metod`, which resolved for the
   first time the day the repository went public; `CORRECTION_DAYS` is 14,
   confirmed by the owner. The condition that held the table back was never
   design, only that it must not go live while its own correction route is a
   404 — so if the repository ever closes again, `REPO_PUBLIC` goes back to
   `False` and the table comes down with it. 21 importers clear the 40-wine
   threshold today.
4. **Trends.** The nightly commits are a time series: coverage by month,
   substances appearing and disappearing, suppliers who started declaring.
   It costs nothing to keep and cannot be recreated later if the history is
   thrown away.

## Open questions for the owner

Every entry here is a decision or a gap, in one line each. The reasoning that
made them lives in `docs/legal-notes.md`, with the sources fetched and quoted;
repeating it here only lets the two drift apart.

### Settled

| | |
|---|---|
| Undeclared wines are listed | 2026-07-27, in their own block with the reason |
| Importers are named | 2026-07-27; table built 2026-08-02, live 2026-08-29 when the repository went public and the correction route started resolving |
| ~~Dataset stays private for now~~ | 2026-07-27, written throughout as if public — superseded 2026-08-29: the repository is public and the dataset is a published download, under no licence (`LICENSES.md`) |
| The quality gate watches drift, not a level | 2026-07-27; `/metod` states and dates it |
| Labelling responsibility is the producer's for EU wine | 2026-07-28, §1 — Article 8(1) of Regulation (EU) No 1169/2011. The importer limb fires only for third-country wine, and the dataset cannot tell which applies, so the table's claim is factual rather than one about responsibility |
| The requirement covers wine **produced** after 8 December 2023 | 2026-07-28, §1f–1g. Not "the 2024 harvest". Vintage is a proxy and every page using it says so |
| Bottle photographs may be embedded, never copied | 2026-07-28, §2 — the line falls at a technological measure (*Svensson*, *BestWater*, *VG Bild-Kunst* §46; *Renckhoff* for copying) |
| Naming importers is defensible, and the table ships | 2026-07-28, §3 — förtal does not reach an aktiebolag (SOU 2016:7 p. 410). One uniform claim regardless of a wine's origin: the company placed it on the Swedish market and supplied the text |
| A supplier who is a natural person is ranked on the same terms | 2026-07-29, reversing the rule written the day before. Excluding them would mean the smallest suppliers are the only ones never examined |
| The crawl continues despite clause 1.7 | 2026-07-28, §2f — a public product API and `Allow: /` contradict a clause forbidding what they invite. A judgement about evident intent, not a resolution of the clause |
| The site is not *i näringsverksamhet* today | 2026-07-28 — no income, so every regime gating on it is out of scope while that holds. See *When the site takes income* |
| Sole traders' names stay in `supplier` | 2026-07-28 — public business information, quoted verbatim; stripping it would misattribute the wines |
| The site never says a substance is harmful | 2026-08-02 — see *What the site must never say*, which is where that rule and its exception are written |

### Open

**Needs a Swedish lawyer, and the owner has decided not to consult one at this
stage.**

- **Is the site acting *i näringsverksamhet*?** The single highest-value
  question: one answer closes five exposures — alkohollagen 7 kap. via
  marknadsföringslagen 3 §, Regulation (EC) No 1924/2006 Article 1(2),
  marknadsföringslagen 18 §, varumärkeslagen 1 kap. 10 §, and clause 4 of
  Systembolaget's terms. §3e has the table. A site with no income fails the
  first element on its face, but no fetched case draws the line for an
  independent information site. It becomes pressing the day the site takes
  income.
- **Is the dataset someone else's database?** §2i. Upphovsrättslagen 49 §
  protects a compilation of a large number of items **or** the result of a
  substantial investment — alternatives, not cumulative. *British Horseracing
  Board* (C-203/02): public accessibility is no defence, and repeated small
  extractions that reconstitute the database are caught. The text-and-data-mining
  exception in 15 a § does not obviously help, since it forbids keeping copies
  longer than the mining needs.
- **Whether a browsewrap term binds a party that never opened an account**, and
  what follows if it does. §2k.
- **Who is liable in Sweden when a declaration is wrong.** Not established.

**Not researched, and not a lawyer's question:**

- **Publishing a compliance statistic about a natural person.** No GDPR
  analysis has been done and Bolagsverket has not been queried to confirm which
  suppliers are enskilda firmor. The 40-wine threshold keeps all of them out of
  the table today, but that is this quarter's catalogue rather than a
  safeguard. §3c.
- **Whether a ranked list is itself an implied health claim**, regardless of
  its wording. *Deutsches Weintor* (C-544/10) reads "health claim" to include
  any implication of reduced harm, but only in commercial communications, which
  loops back to the first question above. §4c, §4f.
- **Who owns the bottle photographs**, and whether the CJEU's Article 3(1) case
  law reaches the purely Swedish neighbouring right in 49 a § URL. §2.
- ~~**`CORRECTION_DAYS` in `src/site.py` is 14 and unconfirmed.**~~ Settled
  2026-08-29: the owner confirmed 14. It is the one number the site publishes
  as a promise rather than a measurement, so it stays the owner's to change.

# Legal notes

Findings on the questions `docs/site-plan.md` leaves open. **This is not legal
advice and must not be read as any.** It is a record of what primary sources say,
quoted and cited, and of what they do not settle. Nothing here makes the site
compliant with anything; several findings below say plainly that a Swedish
lawyer is needed.

A living document. Each run extends it rather than replacing it. Every entry
carries the date it was researched, because law is amended and guidance is
withdrawn.

Run log:

| Date | Questions covered | By |
|---|---|---|
| 2026-07-28 | 1 (responsibility, scope) and 4 (health claims, marketing) | legal-researcher agent |

Still open, untouched by this run: **question 2** (hotlinking Systembolaget's
bottle photographs) and **question 3** (defensibility of naming importers —
förtal, marknadsföringslagen). Nothing below should be read as bearing on
either.

---

## A note on sourcing, and on what failed

**EUR-Lex could not be fetched directly.** Every attempt against
`eur-lex.europa.eu` — HTML, PDF, ELI and CELEX forms, English and Swedish —
returned an empty document body to the tooling available in this run. So did
`www.europarl.europa.eu/doceo/...`. `lexparency.org` failed TLS negotiation.
`publications.europa.eu` redirected to RDF only.

Two substitutes were used, and each carries a caveat that has to travel with
every quotation taken from it:

1. **`www.legislation.gov.uk/eur/.../adopted`** — the UK's reproduction of EU
   regulations *as adopted by the EU*, before any UK modification. The `/adopted`
   suffix is the point: it is the original EU wording, not the assimilated UK
   text. Confidence that it faithfully reproduces the EU original is high (the
   texts fetched still say "Community", "the Union", "Member States"), but it is
   **not the authentic EU text and it is not a consolidated text**. Anything
   below sourced this way has not been checked against a current EUR-Lex
   consolidation, so a later amendment could have changed it without this
   document noticing. That check is outstanding.
2. **`r.jina.ai` as a text-extraction proxy in front of EUR-Lex.** The content is
   EUR-Lex's; the proxy only strips the page. It truncates long documents, which
   is why the operative final article of Regulation (EU) 2021/2117 could not be
   reached this way (see below). One extraction from this proxy was checked and
   found to be **fabricated** — asked for the final article of 2021/2117 it
   produced a plausible "Article 230(4)"; a follow-up query for the literal
   string "8 December 2023" found no such string in the visible text. Nothing
   from that first extraction is used here. Treat proxy output as needing a
   confirming query, always.

**Fetches that failed, listed so the next run does not repeat them blind:**

- `eur-lex.europa.eu` — all direct forms, empty body.
- Consolidated Regulation (EU) No 1308/2013 — `CELEX:02013R1308-20231207` and
  `-20250101` both 404 through the proxy. The **currently applicable text of
  Article 119 of Regulation (EU) No 1308/2013, as amended by 2021/2117, was
  therefore never read.** This is the single most important gap left by this run.
- **Article 6 of Regulation (EU) 2021/2117** (entry into force, application dates
  and the transitional rule) — never read in its operative form. Only recital 42
  and the Commission's own guidance on it were obtained.
- `kontrollwiki.livsmedelsverket.se/artikel/32` ("Ansvar för informationen") —
  the fetcher returned navigation only, twice. Livsmedelsverket's own restatement
  of who is responsible was not obtained.
- `www.livsmedelsverket.se` news and press pages on the wine rules — 404.
- Patent- och marknadsöverdomstolen's judgment in PMT 12229-19 (Mackmyra) as PDF
  from `domstol.se` — timed out twice.

---

## Question 1 — who answers for the ingredient declaration on the Swedish market

*Researched 2026-07-28.*

### 1a. The question

The coverage page ranks named importers by how much of their range declares.
Does the law put the declaration on the importer — Systembolaget's
`supplierName` — or on the producer who made the wine?

### 1b. What the primary sources say

**Regulation (EU) No 1169/2011, Article 8 — Responsibilities.** Fetched from
<https://www.legislation.gov.uk/eur/2011/1169/article/8/adopted> (text as adopted
by the EU).

> **8(1)** "The food business operator responsible for the food information shall
> be the operator under whose name or business name the food is marketed or, if
> that operator is not established in the Union, the importer into the Union
> market."

> **8(2)** "The food business operator responsible for the food information shall
> ensure the presence and accuracy of the food information in accordance with the
> applicable food information law and requirements of relevant national
> provisions."

> **8(3)** "Food business operators which do not affect food information shall
> not supply food which they know or presume, on the basis of the information in
> their possession as professionals, to be non-compliant with the applicable food
> information law and requirements of relevant national provisions."

Paragraph 5 was returned in fragmentary form by the fetcher; the fragment reads
"ensure compliance with the requirements of food information law" within the
businesses under an operator's control, and verify that those requirements are
met. It is quoted here only as a fragment and should be re-read in full.

**Regulation (EU) No 1169/2011, Article 16(4)** —
<https://www.legislation.gov.uk/eur/2011/1169/article/16/adopted>:

> "Without prejudice to other Union provisions requiring a list of ingredients or
> a mandatory nutrition declaration, the particulars referred to in points (b) and
> (l) of Article 9(1) shall not be mandatory for beverages containing more than
> 1,2 % by volume of alcohol."

This is why wine was outside ingredient and nutrition labelling until 2021/2117
put the obligation into the wine regulation instead. The opening words — "without
prejudice to other Union provisions requiring a list of ingredients" — are the
hinge that lets Regulation (EU) No 1308/2013 impose it.

**Regulation (EU) No 1308/2013, Article 119(1), as adopted in 2013** —
<https://www.legislation.gov.uk/eur/2013/1308/article/119/adopted>. Compulsory
particulars include:

> "(e) an indication of the bottler or, in the case of sparkling wine, aerated
> sparkling wine, quality sparkling wine or quality aromatic sparkling wine, the
> name of the producer or vendor"

> "(f) an indication of the importer in the case of imported wines"

Note what (f) does and does not say. An importer must be named **only for
imported wines** — imported into the Union, i.e. from a third country. A French
wine sold in Sweden has no importer particular at all under this article; it has
a bottler.

**Commission Notice C/2023/1190** (Q&A on the new wine labelling provisions),
fetched through the text proxy from EUR-Lex. Question 40:

> "the presence and accuracy of the information is the responsibility of the
> business operator responsible for the food information, in accordance with
> Article 8(2) of the FIC Regulation."

and

> "food business operators are responsible for any changes they make to food
> information accompanying a food pursuant to Article 8(4) of the FIC Regulation."

Question 3 of the same Notice:

> "The responsibility of the operators in the supply chain regarding labelling and
> presentation, is clarified by Article 8 of the FIC and in particular paragraph 7."

The Notice does **not** name the importer as the responsible operator. Asked
directly for such a passage the extraction returned none; the only mention of an
importer found was in Question 2, about where the importer particular may sit in
the field of vision.

**Systembolaget's own position.** Its quality-assurance page
(<https://www.omsystembolaget.se/vart-uppdrag/ansvar-for-dryckerna/kvalitetssakring/>)
describes a checking role, not an authoring one:

> "Våra handläggare inom Produktkvalitet Märkning kontrollerar att dryckerna och
> förpackningarna som säljs i våra butiker följer de regler som gäller för
> märkning och marknadsföring."

Its customer-service page on the new EU rule
(<https://www.systembolaget.se/kundservice/ovrigt/44367415-867b-4082-b0b4-2711063d8d29/hur-funkar-det-nya-kravet-pa-markning-av-vin-fran-eu/ccb732f8-5522-45fe-bbee-1604a0eba6f3/>)
says the information will be shown on systembolaget.se as new packaging reaches
the market — "Som tidigast kommer den nya informationen visas från och med början
av 2024" — and attributes the choice of where the QR code points to producers. It
contains **no statement about who is responsible for the information's accuracy.**

### 1c. The answer

**Settled by the text, and it does not support what the plan currently says.**

Article 8(1) sets a two-step rule, and the second step only fires when the first
fails:

1. The responsible operator is **the one under whose name or business name the
   food is marketed**. For a wine sold under a producer's own label — Château X,
   Cantina Y — that is the producer or bottler named on the bottle.
2. **Only if** that operator is not established in the Union does responsibility
   move to **the importer into the Union market**.

So:

- For a wine from an EU producer sold in Sweden, the responsible food business
  operator is the **producer/bottler**, not the Swedish importer. The Swedish
  importer is an intra-Union distributor. Article 8(1) does not reach it.
- For a wine from a third country, the name-bearer is not established in the
  Union, so the responsible operator is **the importer into the Union market**.
  That may well be the Swedish company in `supplierName` — but it need not be:
  a wine that entered the Union through Rotterdam under a Dutch importer and was
  then sold on to a Swedish company has a Dutch responsible operator. The dataset
  cannot distinguish these.
- For an own-label wine marketed under the Swedish company's own business name
  (Systembolaget's range contains such products), the Swedish company **is** the
  name-bearer and is responsible under the first limb.

**How much of the catalogue is which.** Counted against `data/wines.json`
(generated 2026-07-28, 15 143 wines): **2 673 wines (17.6 %) carry a country
outside the EU** (Chile, South Africa, Australia, Argentina, USA, New Zealand,
UK, Switzerland, Georgia, Moldova, Lebanon, Israel and others). The remaining
~82 % are EU-origin, where Article 8(1) points at the producer. The plan's
attribution is therefore **the minority case dressed as the rule.**

Two caveats on that count, both against the project's interest: country of origin
is not the same as the operator's place of establishment, and the count says
nothing about how many wines are own-label.

### 1d. The three-way distinction the brief asks about

- **Who must ensure the information exists** and **who must ensure it is
  accurate** are, under Article 8(2), **the same party** — "the presence and
  accuracy" sit in one sentence, on the operator identified by Article 8(1). They
  are not two parties. That part of the brief's worry resolves.
- **Who else has duties.** Article 8(3) binds operators "which do not affect food
  information" not to supply food they know or presume to be non-compliant.
  Article 8(5) requires operators to ensure and verify compliance within the
  businesses under their control. A Swedish importer and Systembolaget both sit
  here. These are real, enforceable duties — but they are duties **not to pass on
  a bad label**, not duties **to write a good one**. An importer that receives a
  compliant Italian label and shelves it has discharged them.
- **Who is liable when it is wrong** — **not established.** Regulation 1169/2011
  allocates responsibility, not penalties. Penalties are national.
  Livsmedelslagen (2006:804) was read at <https://lagen.nu/2006:804>: 3 § applies
  the law to "alla stadier av produktions-, bearbetnings- och
  distributionskedjan för livsmedel"; 6 § authorises regulations on "märkning och
  presentation av livsmedel"; 28 a § and 29 § carry the offences. The fetcher
  returned these in summary rather than verbatim and **the exact wording of the
  offence provisions, the identity of the controlling authority for wine
  importers in Sweden, and how Swedish enforcement practice allocates blame
  between an EU producer and a Swedish importer were all not established.**
  This is the part that **needs a Swedish lawyer**, and it is the part that would
  matter if an importer objected to being named.

### 1e. What it means for the site

The importer table does not have to be abandoned. It has to be **re-described**,
because the sentence that justifies it is wrong.

**The sentence that must change.** `docs/site-plan.md`, *Naming importers*:

> "The producer made the wine; the importer answers for what the label says here."

For roughly four wines in five that is not what Article 8(1) says. Replace the
legal claim with a factual one the dataset can actually support:

> The importer is the company that placed this wine on the Swedish market and
> supplied the product text Systembolaget publishes. Which company is the food
> business operator legally responsible for the declaration under Article 8(1) of
> Regulation (EU) No 1169/2011 depends on whose name the wine is marketed under
> and where that company is established, and the dataset does not record either.

Everything the table actually does — count wines per supplier, compute a share,
link to the bottles — survives that rewrite unchanged. What does not survive is
the word **accountable**. The plan's "only the importer is accountable for the
gap" is a legal characterisation and the text does not support it.

Concretely:

- `/tackning` and `/importor/{slug}` must not say or imply that the named company
  is legally responsible for the missing declaration.
- `/metod` must carry the Article 8(1) two-step rule and say which limb the
  dataset cannot resolve.
- Rows should say what is measurable: *"X of Y wines this importer supplies, from
  vintages in the qualifying set, carry a declaration on systembolaget.se."*
  That is a statement about Systembolaget's product pages, which is what was
  actually measured, and it is true regardless of who is legally responsible.

### 1f. Scope and the vintage cutoff — the load-bearing figure

**This is the finding that changes a number.**

The criterion in the law is **not a harvest**. Commission Notice C/2023/1190,
Question 3, fetched through the text proxy from EUR-Lex:

> "As a general rule, these new compulsory particulars must apply to wines placed
> on the market from the respective date of application laid down in Regulation
> (EU) 2021/2117, i.e., 8 December 2023. However, wines 'produced' before that
> date may continue to be placed on the market following the labelling
> requirements applicable before 8 December 2023, until stocks are exhausted."

Question 4 of the same Notice defines "produced":

> "A grapevine product is considered 'produced' when it achieves the
> characteristics and requirements as set out in Part II of Annex VII of the CMO
> Regulation for the wine category concerned, including through the
> implementation, when relevant, of authorised oenological practices based on the
> rules laid down in Article 80 and Annex VIII of that Regulation."

Question 5, on third-country wine:

> "As regards imported wines, wines imported before this date are considered as
> produced before and therefore eligible to this exemption."

Recital 42 of Regulation (EU) 2021/2117 itself, the only part of the operative
instrument reached:

> "The marketing of existing stocks of wine should be allowed to continue after
> the dates of application of the new labelling requirements until those stocks
> are exhausted."

**Livsmedelsverket says the same thing in Swedish** and adds the practical
gloss. From its public Q&A
(<https://fragor.livsmedelsverket.se/org/livsmedelsverket/d/naringsdeklaration-och-ingrediensforteckning-for-v/>):

> "vin som producerats efter den 8 december 2023 och som säljs inom EU"

and wine produced before that date "kan säljas tills lagren är tömda". From the
companion Q&A on what "producerat" means
(<https://fragor.livsmedelsverket.se/org/livsmedelsverket/d/nya-regler-for-vin/>),
answering a questioner from the trade who asked exactly this:

> "Det vin som är färdigproducerat före den 8 december 2023 men ligger på tank
> eller fat i väntan på buteljering får märkas senare enligt de regler som gällde
> före den 8 december 2023."

The Swedish trade association for wine and spirits suppliers states it the same
way (<https://www.svl.se/idag-8-12-trader-nya-regler-om-markning-av-vin-i-kraft/>):
"allt vin och aromatiserat vin som produceras efter den 8 december 2023 och som
säljs på den europeiska marknaden"; wine produced before is "undantagna de nya
kraven".

**Where "harvest 2024" comes from.** The Commission's own news announcement
(<https://agriculture.ec.europa.eu/media/news/new-rules-wine-labelling-enter-application-2023-12-07_en>)
says both things in the same breath: the rules apply to "all wines and wine
products obtained from the harvest 2024", and "All wines produced before 8
December 2023 will still be exempted from the new rules until stocks are
exhausted." The harvest formulation is the Commission's own shorthand for the
practical consequence, not the criterion. The criterion is the production date.

**An unresolved conflict in the wording, flagged rather than resolved.** Several
secondary accounts render the transitional provision as covering wine "produced
**and labelled** before 8 December 2023". The Commission Notice, quoted above,
says only "produced". Livsmedelsverket says explicitly that wine finished before
the date but still in tank "får märkas senare" under the old rules — i.e.
labelling after the date does not remove the exemption. If the operative text of
Article 6 of Regulation (EU) 2021/2117 does contain "and labelled", then the
Notice and Livsmedelsverket are reading it more generously than it reads.
**The operative text was not fetched and this conflict is unresolved.** It does
not change the finding below, because either reading is a *production/labelling*
criterion and neither is a harvest criterion.

### 1g. What that does to the project's numbers

Grading: **settled by authoritative guidance** (Commission Notice + Swedish
competent authority, both fetched and quoted). **Not settled by the operative
text**, which was not read.

The project uses "2024 vintage onwards" as its qualifying set. Measured against
that criterion:

- **The error direction is safe.** Every wine of the 2024 harvest or later was
  necessarily produced after 8 December 2023, so the filter never ranks a wine
  as non-declaring when the requirement did not apply to it. No importer is
  penalised for stock the rule does not touch. The plan's central worry — that a
  raw all-vintages column would accuse Johan Lidby unfairly — is correctly
  handled.
- **The filter is nonetheless materially incomplete.** Counted in
  `data/wines.json` (2026-07-28): **2 217 wines carry vintage `"2023"` and 2 854
  carry no vintage at all** — 5 071 wines, **33.5 % of the 15 143 in the
  catalogue** — sit outside the qualifying set while an unknown share of them is
  legally in scope. Non-vintage sparkling wine is the clearest case: under
  Question 4 of the Notice a sparkling wine made by second fermentation is
  "produced" only once that second fermentation has taken place, so a
  non-vintage brut disgorged in 2025 is squarely covered and is invisible to a
  vintage filter. Late-finished 2023 reds and any 2023 wine still undergoing
  authorised oenological practices after 8 December 2023 are covered too.
- **The legal set is not computable from this dataset.** Neither Systembolaget's
  catalogue nor the product detail route carries a production, bottling or
  disgorgement date. There is no field from which the criterion can be evaluated.
  Vintage is the only available proxy and it is a one-sided one.

**What must therefore be said, on `/tackning`, `/importor/{slug}` and `/metod`,
in the page body and not in a footnote:**

> The requirement applies to wine *produced* after 8 December 2023, not to a
> harvest. The dataset has no production date, so this page uses vintage 2024 and
> later as a stand-in. That stand-in is conservative — every wine it includes is
> covered by the requirement — but it is incomplete: wines with no vintage and
> some 2023 wines are covered and are not counted here. On 2026-07-28 that is
> 5 071 wines, a third of the catalogue.

Anything that reads "the requirement covers the 2024 harvest onwards" — including
`README.md`'s caveat section, which says exactly that — is stating the
Commission's shorthand as if it were the rule. It should say that the criterion
is the production date and that vintage is the project's proxy for it.

### 1h. What could not be established (question 1)

- The operative text of Article 6 of Regulation (EU) 2021/2117.
- The current consolidated text of Article 119 of Regulation (EU) No 1308/2013,
  including the exact wording of the points 2021/2117 inserted on the list of
  ingredients and the nutrition declaration. **The obligation itself was never
  read in its operative form.**
- Whether the transitional provision says "produced" or "produced and labelled".
- Which authority in Sweden performs official control of wine labelling, and
  under which provisions of livsmedelslagen (2006:804) an importer as against a
  producer can be sanctioned. **Needs a Swedish lawyer.**
- Whether Systembolaget's supplier contracts place labelling responsibility on
  the supplier. A search summary asserted this; no page containing such a
  statement was fetched, so it is recorded here as unverified and must not be
  cited.
- What proportion of the range is own-label, where the Swedish company would be
  the responsible operator under the first limb of Article 8(1).

---

## Question 4 — what the site may say without making a health claim

*Researched 2026-07-28.*

### 4a. The question

The site ranks **disclosure**, not content. Four wines in five declare nothing, so
a "fewest declared additives" list is a ranking of what got disclosed. Does that
run into the health-claims regulation, into alkohollagen's marketing rules, or
into neither?

### 4b. Regulation (EC) No 1924/2006 — what it actually says

All quotations from `www.legislation.gov.uk/eur/2006/1924/.../adopted`, the EU
text as adopted.

**Scope. Article 1(2)** — this is the gate, and it is the whole question:

> "This Regulation shall apply to nutrition and health claims made in commercial
> communications, whether in the labelling, presentation or advertising of foods
> to be delivered as such to the final consumer, including foods which are placed
> on the market unpacked or supplied in bulk."

**Recital 4** puts it beyond doubt:

> "This Regulation should apply to all nutrition and health claims made in
> commercial communications, including, inter alia, generic advertising of food
> and promotional campaigns, such as those supported in whole or in part by public
> authorities. It should not apply to claims which are made in non-commercial
> communications, such as dietary guidelines or advice issued by public health
> authorities and bodies, or non-commercial communications and information in the
> press and in scientific publications."

**The definitions. Article 2** — note how wide "claim" is and how narrow
"nutrition claim" is:

> "claim" — "Any message or representation, which is not mandatory under Community
> or national legislation, including pictorial, graphic or symbolic representation,
> in any form, which states, suggests or implies that a food has particular
> characteristics"

> "nutrition claim" — "Any claim which states, suggests or implies that a food has
> particular **beneficial** nutritional properties due to: (a) the energy
> (calorific value) it provides, provides at a reduced or increased rate, or does
> not provide; and/or (b) the nutrients or other substances it contains, contains
> in reduced or increased proportions, or does not contain" *(emphasis added)*

> "health claim" — "Any claim that states, suggests or implies that a relationship
> exists between a food category, a food or one of its constituents and health"

**The bar on alcohol. Article 4(3):**

> "Beverages containing more than 1,2 % by volume of alcohol shall not bear:
> (a) health claims; (b) nutrition claims, other than those which refer to a
> reduction in the alcohol or energy content."

**Article 4(4)**, on the narrow gap left:

> "In the absence of specific Community rules regarding nutrition claims referring
> to the reduction or absence of alcohol or energy in beverages which normally
> contain alcohol, relevant national rules may apply in compliance with the
> provisions of the Treaty."

**Article 8(1)**, closing the list:

> "Nutrition claims shall only be permitted if they are listed in the Annex and are
> in conformity with the conditions set out in this Regulation."

So the exceptions are exactly two and both are about **alcohol or energy** —
reduced alcohol, reduced energy — and even those must appear in the Annex. There
is no exception for additives, ingredients or their absence. If the regime
applies at all, "fewer additives" gets no exception; it either falls outside the
definition of a claim or it is prohibited.

**How wide "health claim" is: Case C-544/10 *Deutsches Weintor eG v Land
Rheinland-Pfalz*, judgment of 6 September 2012.** Fetched through the text proxy
from EUR-Lex (`CELEX:62010CJ0544`). A wine cooperative marketed wine as
"bekömmlich" (easily digestible) with a reference to reduced acidity. The Court
held this was a health claim, and that the ban is absolute. Key holdings as
extracted:

> the concept of a health claim covers "not only a relationship implying an
> improvement in health … but also any relationship which implies the absence or
> reduction of effects that are adverse or harmful to health"

and on Article 4(3):

> the legislature "intended to proscribe, without exception, all 'health claims'
> relating to that category of beverage"

This is the case that matters most to this project, and it is a wine case. **A
claim that a wine is less harmful is a health claim.** The plan's rule "never say
fewer additives is healthier or safer" is not a matter of taste; it is the exact
shape of the thing *Deutsches Weintor* prohibits — if the site is a commercial
communication.

Caveat: the judgment was read through the proxy, in extraction rather than in
full. The two quotations above should be verified against the authentic text
before either is reproduced on `/metod`.

### 4c. Does a count of declared additives fall inside the definitions at all?

**Unclear, and the analysis splits in two.**

*If the site is not a commercial communication*, Article 1(2) and recital 4 mean
Regulation 1924/2006 does not apply to it at all, whatever it says. This is the
decisive question and it is the same question that decides alkohollagen (below).

*If it is*, then:

- A bare count — "declares 3 additives" — states a characteristic without stating
  a benefit. "Nutrition claim" requires "**beneficial** nutritional properties",
  so a neutral count is arguably outside it. Additives are also not obviously
  "nutrients", though the definition's residual "or other substances" is wide
  enough to reach them.
- But "claim" itself is defined as any representation "**in any form**, which
  states, **suggests or implies** that a food has particular characteristics",
  expressly including "pictorial, graphic or symbolic representation". A ranking
  is a representation, and ordering is a form of suggestion. The definitions are
  drafted precisely to catch implication.
- And *Deutsches Weintor* shows the Court reading "health claim" to reach
  implications of reduced harm. A list headed "fewest additives" invites that
  inference even if no sentence on the page makes it.

There is no fetched authority applying these definitions to a third-party
comparison site. **Needs a lawyer** for the launch wording, and the answer will
turn mostly on 4d.

### 4d. Is the site marketing at all? — alkohollagen and marknadsföringslagen

**The prior question, exactly as the brief frames it, and it is prior for
1924/2006 too.**

**Alkohollagen (2010:1622) 7 kap.**, fetched from
<https://www.riksdagen.se/sv/dokument-och-lagar/dokument/svensk-forfattningssamling/alkohollag-20101622_sfs-2010-1622/>:

> **7 kap. 1 §** "Vid marknadsföring av alkoholdrycker eller alkoholdrycksliknande
> preparat till konsumenter ska särskild måttfullhet iakttas."

> **7 kap. 5 §** "Vid marknadsföring till konsumenter av alkoholdrycker eller
> alkoholdrycksliknande preparat genom kommersiella annonser får framställning i
> bild omfatta endast en återgivning av 1. varan eller råvaror som ingår i varan,
> 2. enstaka förpackningar, eller 3. varumärke eller därmed jämförligt kännetecken."

> **7 kap. 8 §** "Ett handlande som strider mot 1–6 §§ och 7 § första stycket
> eller föreskrifter som utformats med stöd av 7 § andra stycket ska vid
> tillämpningen av 5, 23 och 26 §§ marknadsföringslagen (2008:486) anses vara
> otillbörlig mot konsumenter…"

**7 kap. contains no definition of "marknadsföring".** It routes to
marknadsföringslagen. Amendments noted on the riksdagen page: lag (2019:345),
and lag (2020:876) for 7 kap. 3 §.

**Marknadsföringslagen (2008:486) 3 §**, fetched from <https://lagen.nu/2008:486>:

> "marknadsföring: reklam och andra åtgärder **i näringsverksamhet** som är
> **ägnade att främja avsättningen** av och tillgången till produkter inbegripet
> en näringsidkares handlande, underlåtenhet eller någon annan åtgärd eller
> beteende i övrigt före, under eller efter försäljning eller leverans av produkter
> till konsumenter eller näringsidkare" *(emphasis added)*

and

> "näringsidkare: en fysisk eller juridisk person som handlar för ändamål som har
> samband med den egna näringsverksamheten"

**Two cumulative elements.** A measure is marknadsföring only if it is (i) *i
näringsverksamhet* — in business activity — and (ii) *ägnad att främja
avsättningen* — apt to promote sales. A site with no revenue, no products, no
advertising and no affiliate arrangement fails the first element on its face.

**Konsumentverket uses the same definition.** Its decision memorandum for
KOVFS 2023:1 (in force 1 January 2024, replacing KOVFS 2016:1), fetched via the
text proxy from
<https://stpubshop.blob.core.windows.net/publikationer/kovfs-2023-1-konsumentverkets-allmanna-rad-ommarknadsforing-av-alkoholdrycker-beslutspromemoria_a33.pdf>:

> "Med marknadsföring avses reklam och andra åtgärder i näringsverksamhet som är
> ägnade att främja avsättningen" (p. 6)

and on the narrower concept of a commercial advertisement, that the message must
"vara avsett att främja avsättningen" and concern a trader's commercial activity
(p. 6). Its general advice applies to marketing "till konsumenter" that targets
the Swedish market (p. 5). Its guidance for businesses on internet marketing
(<https://konsumentverket-se-prod.azurewebsites.net/for-foretag/regler-per-omradebransch/alkohol/marknadsforing-av-alkohol-pa-internet/>)
addresses traders — "När du ska marknadsföra alkohol på internet…" — and says
"Se till att det tydligt framgår vad som är redaktionell text och vad som är
marknadsföring." It does **not** address sites that merely publish information;
asked directly, the fetch confirmed the page "behandlar inte denna kategori
separat".

**The decided case.** *Mackmyra Svensk Whisky AB ./. Konsumentombudsmannen*,
judgment of 26 March 2021, read at <https://lagen.nu/dom/nja/2021s1124>. Six of
the company's own Facebook and Instagram posts showing whisky bottles alongside
landscapes and people were held to be commercial advertisements subject to
7 kap. alkohollagen. The reasoning as extracted:

> "Att Mackmyras egna inlägg inte är betalda innebär inte att inläggen är
> redaktionella."

The test applied: whether the communication is "avsedd att främja avsättningen av
varan" and has "rent kommersiella förhållanden till föremålet"; the posts
qualified because "produkterna är de centrala elementen i inläggen".

**Two caveats on this case, both material.** First, the extraction attributes the
reasoning to Patent- och marknadsöverdomstolen while the reference on lagen.nu is
an NJA (Supreme Court) citation; **which instance's ratio was retrieved was not
established**, and the attempt to fetch PMÖD's judgment in PMT 12229-19 from
domstol.se timed out twice. Second and more importantly: **Mackmyra was a
producer promoting its own goods.** The case decides that unpaid own-channel
content is still commercial. It says **nothing** about a third party with no
goods to sell and no revenue. It is not authority either way for this site.

**The constitutional frame.** Tryckfrihetsförordningen 1 kap. 12 §, fetched from
<https://lagen.nu/1949:105>:

> "Bestämmelserna i denna grundlag hindrar inte att det i lag meddelas föreskrifter
> om 1. förbud mot **kommersiella annonser** vid marknadsföring av alkoholdrycker
> eller tobaksvaror, … 4. krav att införa och på ett visst sätt utforma
> varningstext, innehållsdeklaration eller annan liknande produktinformation om
> syftet är skydd för hälsa eller miljö eller konsumentskydd"

The carve-out permitting alcohol advertising bans is expressly limited to
*kommersiella annonser*. That is consistent with — though it does not by itself
establish — the reading that non-commercial publication about alcohol sits
outside the marketing regime.

Yttrandefrihetsgrundlagen 1 kap. 4 § (databasregeln), read at
<https://lagen.nu/1991:1469>, extends constitutional protection to databases run
by editorial offices, publishers, news agencies, and **others holding an
utgivningsbevis** (publishing certificate, valid ten years, requiring a named
qualified publisher). The fetch returned this in summary rather than verbatim.
Noted as an option that exists, with a direct conflict for this project: an
utgivningsbevis requires a named ansvarig utgivare on a public register, which
collides with `CLAUDE.md`'s absolute rule against personal data in this project.
Not a recommendation — a trade-off to be aware of.

### 4e. The answer on question 4

**Whether alkohollagen 7 kap. reaches the site: strongly implied to be outside,
but not established — needs a Swedish lawyer.**

The statutory chain is clear and it turns on "i näringsverksamhet". A site that
sells nothing, carries no advertising, takes no affiliate income and holds no
commercial relationship to any wine it lists does not obviously act in
näringsverksamhet, and 7 kap. 1 § only bites on marknadsföring. But no fetched
source — no case, no Konsumentverket guidance — draws the line for an
independent information site. The absence is itself the finding: **this question
has not been decided in any source this run could reach.**

**Two things follow, and they are concrete.**

1. **The no-revenue rule is now legally load-bearing.** The plan already forbids
   affiliate links, advertising and analytics, on privacy and integrity grounds.
   Those same facts are what keep the site out of "näringsverksamhet". Taking any
   commercial income — an affiliate link to Systembolaget, a sponsored substance
   page, a paid listing — would not merely dent the site's independence. It would
   supply the element that the marketing regime, and with it 7 kap. 1 §
   särskild måttfullhet and Regulation 1924/2006 Article 4(3), needs in order to
   apply. That should be written into the plan as a rule with its reason stated,
   not left as a preference.
2. **The plan's own framing works against it.** The plan says the site's carrying
   use case is "helping someone choose and buy a wine", calls `/hitta` "the
   recommendation", and describes lists as things a user "can act on". Read by
   someone testing whether the site is *ägnad att främja avsättningen*, those
   sentences are the strongest material available against the project — and the
   project wrote them itself. They are not fatal, since the first element
   (näringsverksamhet) is still missing. But the internal contradiction with
   "Anything that reads as advice on what to drink" being forbidden is real and
   should be resolved deliberately rather than left for someone else to point out.

**Whether a ranked list can be an implied claim through its form: strongly
implied yes, as a matter of how the definitions are drafted; unclear whether it
bites this site.**

The building blocks are all in fetched text. "Claim" is defined to include
representations "in any form" that "suggest or imply". *Deutsches Weintor* reads
"health claim" to reach implications of reduced harm. And Regulation (EU) No
1169/2011 Article 7(1), fetched from
<https://www.legislation.gov.uk/eur/2011/1169/article/7/adopted>, forbids food
information that suggests

> "special characteristics when in fact all similar foods possess such
> characteristics, in particular by specifically emphasising the presence or
> absence of certain ingredients and/or nutrients"

— and Article 7(4) extends the same rules to "advertising" and "the presentation
of foods". *(Article 7(1)'s chapeau was returned by the fetcher in fragmentary
form and should be re-read in full.)* Article 7 binds food business operators,
which the site is not. But it is direct evidence that EU food law treats
**emphasis on the absence of an ingredient** as capable of being a misleading
representation on its own, without any sentence asserting a benefit. A list
whose entire organising principle is "least of this substance" is emphasis on
absence in its purest form.

A disclaimer under a ranking does not neutralise the ranking. Nothing fetched
says it does, and the definitions are built to catch implication precisely
because disclaimers do not.

### 4f. Assessment of *What the site must never say*

Asked directly: **the four rules are correct as far as they go, insufficient in
coverage, and one of them is undercut by the plan's own wording elsewhere.**

Rule by rule:

1. *"That fewer additives is healthier, safer, or better for you."* — **Correct
   and well-aimed.** It is the exact prohibition *Deutsches Weintor* enforces,
   including the "safer" limb, which matches the Court's "absence or reduction of
   effects that are adverse or harmful to health". **Insufficient in one respect:
   it is a rule about sentences.** It should extend to page titles, `<title>` and
   meta description, URL slugs, list headings, sort-order labels, iconography and
   share text — the places where an implication is made without a sentence, and
   the places that get quoted without their context.
2. *"That a wine 'contains no additives' when it declares nothing."* —
   **Correct and necessary.** Keep verbatim.
3. *"Anything about a named wine that cannot be traced to that wine's own declared
   text."* — **Correct.** Also the best available answer to question 3, which is
   not researched here.
4. *"Anything that reads as advice on what to drink. It ranks disclosure, and it
   says so."* — **Correct in intent, contradicted in practice** by "helping
   someone choose and buy a wine", "the recommendation", and "a shortlist they
   can act on". Either the rule or those sentences has to give.

**What the rules do not cover, and should:**

- **No commercial income of any kind, for the stated reason** that it is the
  element the marketing regime turns on (4e).
- **No claim about the wine's contents derived from an absent declaration** —
  the plan states this well in *Undeclared wines stay in the results* but does not
  list it as a never-say rule, and that is where it belongs.
- **No presentation of the vintage proxy as the legal scope.** See 1g. This is a
  factual-accuracy rule, not a health rule, and the plan currently has no rule
  covering accuracy of its own scope claims.
- **No implication that a lower additive count is a lower risk**, in any form
  including colour, ordering across blocks, or badges. The plan's "No score"
  paragraph gets close; it should say implication as well as score.

**A specific phrase that is a problem, named as the brief asks.**

`docs/site-plan.md`, *Undeclared wines stay in the results*:

> "the user chose *utan tillsatser* and gets a ranked list of wines that declare
> none"

**"Utan tillsatser" is a statement about what is in the bottle.** The filter does
not and cannot select on that; it selects wines whose declaration lists no
additives. Putting "utan tillsatser" in the interface puts a content claim into
the filter name, the user's selected state, the URL, and anything shared from the
page — the four places least likely to carry the surrounding caveat. It is also
exactly the "emphasising the … absence of certain ingredients" that Article 7(1)
of Regulation 1169/2011 singles out.

Replace with **"deklarerar inga tillsatser"** (English: **"declares no
additives"**). Longer, and correct. The same substitution applies to:

- the `/lista/{slug}` example the plan gives, "red under 150 kr, fewest
  additives" → **"fewest declared additives"**, and the Swedish slug should read
  *minst-deklarerade-tillsatser*, never *minst-tillsatser* or *utan-tillsatser*;
- any occurrence of "fewest additives" as a heading. The plan already writes
  "Fewest **declared** additives within a comparable set" for axis A — that
  phrasing is right and should be the only one used anywhere.

Conversely, two things the project already does well and should not lose: the
name **vindeklaration** names disclosure rather than content, and README's
"Fewer additives does not mean healthier. This is a record of what is on the
label, not a health assessment. Wine is alcohol; that is the relevant risk."
belongs on the ranked pages themselves, not only in the repository.

### 4g. What could not be established (question 4)

- Whether an independent, revenue-free information site is "marknadsföring" under
  MFL 3 § and therefore within alkohollagen 7 kap. **No fetched case or guidance
  addresses it. Needs a Swedish lawyer.**
- Which instance's reasoning was retrieved for the Mackmyra case, and its exact
  wording — the domstol.se judgment PDF timed out twice.
- The verbatim text of KOVFS 2023:1 itself (only its decision memorandum was
  reached) and whether it says anything about third-party information sites.
- Whether Konsumentombudsmannen has ever acted against a non-commercial
  information site about alcohol. Not searched exhaustively; no such case
  surfaced.
- Whether a court has ever treated a comparison ranking, as distinct from a
  sentence, as a nutrition or health claim under Regulation 1924/2006.
- The full text of Article 7(1) of Regulation 1169/2011 and the full text of
  Article 8(5), both returned in fragments.
- Whether Regulation (EC) No 1924/2006 as fetched from legislation.gov.uk's
  "as adopted" text differs from the current consolidated EU text. It has been
  amended since 2006; no consolidated version was read.

---

## Standing warnings for whoever extends this document

- **Nothing here is advice and nothing here makes anything compliant.** Two
  questions above end in "needs a Swedish lawyer" and they are the two that
  decide whether the importer table and the ranked lists can be published as
  planned.
- **Re-read anything quoted from `legislation.gov.uk` against EUR-Lex** when
  EUR-Lex becomes reachable. Consolidation dates matter and none of the EU texts
  quoted here carries one.
- **Verify proxy extractions with a second, differently-phrased query.** One
  fabricated article number was caught in this run only because a follow-up query
  contradicted it.
- **Questions 2 and 3 are untouched.** One pointer only, noted in passing and not
  researched: alkohollagen 7 kap. 5 § restricts images in *kommersiella annonser*
  to a reproduction of the product, its raw materials, single packages, or a
  trademark. If the site were ever held to be marketing, that provision would
  bear on the bottle photographs. It is quoted in 4d; the copyright question it
  sits beside is not addressed.

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
| 2026-07-28 | 2 (bottle photographs, database right) and 3 (naming importers) | legal-researcher agent |

All four standing questions have now been researched at least once. None of them
is closed. The second run turned up **one finding that reaches further than the
question it was asked about**: Systembolaget's Allmänna användarvillkor contain a
clause that on its face prohibits the crawl this whole dataset is built from. See
§2f. It is not a copyright finding and it is not an image finding; it is a
finding about the project's foundation, and it was found while looking for
something else.

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

**Added by the second run (2026-07-28), sources and routes:**

- **`curia.europa.eu` is closed to automated access.** `liste.jsf` returned
  HTTP 403 with a page reading "The site is temporarily unavailable". No CJEU
  judgment was obtained from the Court's own server.
- **`bailii.org` is behind an Anubis proof-of-work challenge.** Every case URL
  returned the same 4.4 kB "Making sure you're not a bot!" interstitial.
- **`api-portal.systembolaget.se` no longer resolves in DNS.** A developer portal
  with a `/terms-of-use` path is still indexed by search engines; the host is
  gone. **Systembolaget's API terms of use were therefore not read.** If a public
  API contract ever granted rights over the product data, this run could not see
  it.
- **`product-cdn.systembolaget.se` has no `robots.txt`.** The host is Azure Blob
  Storage and returns an `OutOfRangeInput` XML error for that path.
- **`r.jina.ai` was used again, but differently and more safely.** The five CJEU
  judgments were fetched to local files with `curl` and then read and grepped
  directly. No model summarised them. The fabrication caught in the first run
  came from asking a small model to answer a question about a proxied page; that
  step was removed. Every judgment fetched this way was verified by checking the
  case number, the party names and the date of judgment against the head of the
  document before anything was quoted from it. **This is still EUR-Lex content
  reached through a third party, and still not a consolidated text.**
- **Systembolaget's own pages were fetched directly with `curl`, not through any
  proxy**, and every string quoted from them in §2e and §2f was verified to exist
  in the downloaded HTML after tag-stripping. Those quotations are first-hand.

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

## Question 2 — the bottle photographs, and the dataset underneath them

*Researched 2026-07-28.*

### 2a. The question

`data/wines.json` carries `image_base_url` for 9 478 of 15 143 wines (62.6 %,
counted 2026-07-28). The plan's intent is to render one image per wine page
directly from `product-cdn.systembolaget.se` and never to copy it. Is that sound,
and under what conditions?

Four separate questions get blurred together here and are kept apart below:
copyright in the photograph (§2b–§2d), Systembolaget's own terms (§2e–§2f),
trade marks and endorsement (§2g), and engineering (§2h). §2i is the database
right in the dataset itself, which is a different subject that happens to share a
source.

### 2b. What the CJEU judgments actually hold

All five were fetched as text and verified by case number, parties and date
before quotation. Sources are EUR-Lex CELEX documents reached through a text
proxy; see the sourcing note above.

**Svensson (C‑466/12), judgment of 13 February 2014** — a Swedish reference, from
Svea hovrätt. Operative part:

> "Article 3(1) of Directive 2001/29/EC … must be interpreted as meaning that the
> provision on a website of clickable links to works freely available on another
> website does not constitute an 'act of communication to the public', as referred
> to in that provision."

The reasoning that matters is paragraph 26 — and note that it is a finding of
fact about the *source* site, not a rule about the *linking* site:

> "The public targeted by the initial communication consisted of all potential
> visitors to the site concerned, since, given that access to the works on that
> site was not subject to any restrictive measures, all Internet users could
> therefore have free access to them."

Paragraph 29 disposes of the framing point directly, and it is the paragraph the
project needs:

> "Such a finding cannot be called in question were the referring court to find …
> that when Internet users click on the link at issue, the work appears in such a
> way as to give the impression that it is appearing on the site on which that
> link is found, whereas in fact that work comes from another site."

Paragraph 31 states the limit:

> "On the other hand, where a clickable link makes it possible for users of the
> site on which that link appears to circumvent restrictions put in place by the
> site on which the protected work appears in order to restrict public access to
> that work to the latter site's subscribers only … all those users must be deemed
> to be a new public … and accordingly the holders' authorisation is required."

Svensson's second ruling matters for a Swedish site specifically:

> "Article 3(1) of Directive 2001/29 must be interpreted as precluding a Member
> State from giving wider protection to copyright holders by laying down that the
> concept of communication to the public includes a wider range of activities than
> those referred to in that provision."

**BestWater (C‑348/13), order of 21 October 2014.** Available in French only; no
English version exists on EUR-Lex. Operative part in full:

> "Le seul fait qu'une œuvre protégée, librement disponible sur un site Internet,
> est insérée sur un autre site Internet au moyen d'un lien utilisant la technique
> de la «transclusion» («framing») … ne peut pas être qualifié de «communication au
> public», au sens de l'article 3, paragraphe 1, de la directive 2001/29/CE … dans
> la mesure où l'œuvre en cause n'est ni transmise à un public nouveau ni
> communiquée suivant un mode technique spécifique, différent de celui de la
> communication d'origine."

This is the case that decides *framing and embedding specifically*, as opposed to
plain clickable links. It is the closest authority to what the wine page would do.

**GS Media (C‑160/15), judgment of 8 September 2016.** This case is about links to
works published *without* the rightsholder's consent, which is not the situation
here, but its test is worth recording because it is the one that fires if a
particular bottle photograph turns out to have been published unlawfully.
Operative part:

> "… it is to be determined whether those links are provided without the pursuit
> of financial gain by a person who did not know or could not reasonably have
> known the illegal nature of the publication of those works on that other website
> or whether, on the contrary, those links are provided for such a purpose, a
> situation in which that knowledge must be presumed."

Paragraph 51:

> "when the posting of hyperlinks is carried out for profit, it can be expected
> that the person who posted such a link carries out the necessary checks … so
> that it must be presumed that that posting has occurred with the full knowledge
> of the protected nature of that work"

Note where that lands: **the site's absence of any commercial income is again the
operative fact.** It is the third regime in this document that turns on it (after
marknadsföringslagen 3 § and Regulation 1924/2006 Article 1(2), §4d), and §2g
adds a fourth.

**Renckhoff (C‑161/17), judgment of 7 August 2018.** Operative part:

> "The concept of 'communication to the public' … must be interpreted as meaning
> that it covers the posting on one website of a photograph previously posted,
> without any restriction preventing it from being downloaded and with the consent
> of the copyright holder, on another website."

The Court set out why copying is not linking. Paragraph 40:

> "unlike hyperlinks which … contribute in particular to the sound operation of the
> internet by enabling the dissemination of information …, the publication on a
> website without the authorisation of the copyright holder of a work which was
> previously communicated on another website with the consent of that copyright
> holder does not contribute, to the same extent, to that objective."

Paragraph 44 is the sentence that decides the whole architectural question for
this project:

> "As regards the act of communication constituted by the posting on a website of
> a hyperlink which leads to a work previously communicated with the authorisation
> of the copyright holder, the preventive nature of the rights of the holder are
> preserved, since it is open to the author, if he no longer wishes to communicate
> his work on the website concerned, to remove it from the website on which it was
> initially communicated, rendering obsolete any hyperlink leading to it. However,
> in circumstances such as those at issue in the main proceedings, the posting on
> another website of a work gives rise to a new communication, independent of the
> communication initially authorised."

Paragraph 46 names the decisive act:

> "the user of the work at issue in the main proceedings reproduced that work on a
> private server and then posted it on a website other than that on which the work
> was initially communicated. In so doing, that user played a decisive role in the
> communication of that work"

And paragraph 36, against the project's convenience, is worth quoting because it
kills a tempting argument:

> "It is irrelevant … that the copyright holder did not limit the ways in which
> internet users could use the photograph."

So the fact that Systembolaget applies no hotlink protection does **not** license
copying. It licenses nothing. It is only relevant to whether *linking* reaches a
new public.

**VG Bild-Kunst (C‑392/19), Grand Chamber, judgment of 9 March 2021.** Operative
part:

> "… the embedding, by means of the technique of framing, in a third party website
> page, of works that are protected by copyright and that are freely accessible to
> the public with the authorisation of the copyright holder on another website,
> where that embedding circumvents measures adopted or imposed by that copyright
> holder to provide protection from framing, constitutes a communication to the
> public within the meaning of that provision."

Paragraph 37 restates the condition on which Svensson and BestWater rest:

> "that case-law was based on the finding of fact that the access to the works
> concerned on the original website was not subject to any restrictive measure …
> In the absence of such measures, the Court therefore held that, by making his or
> her work freely accessible to the public or by authorising the provision of such
> access, the right holder envisaged from the outset all internet users as the
> public and accordingly consented to third parties themselves undertaking acts of
> communication of that work."

And paragraph 46 answers the brief's question about the rightsholder's *expressed
intent* exactly, and answers it in the project's favour:

> "It must be made clear that, in order to ensure legal certainty and the smooth
> functioning of the internet, **the copyright holder cannot be allowed to limit
> his or her consent by means other than effective technological measures**, within
> the meaning of Article 6(1) and (3) of Directive 2001/29 … In the absence of such
> measures, it might prove difficult, particularly for individual users, to
> ascertain whether that right holder intended to oppose the framing of his or her
> works." *(emphasis added)*

**Where the line falls, in one sentence.** Not at framing, and not at the
rightsholder's stated wishes. It falls at **a technological measure** on one side
and at **making your own copy** on the other. Everything between those two is
outside Article 3(1) on this case law.

### 2c. The Swedish transposition, and a gap in it

**Upphovsrättslagen (1960:729)**, fetched from
<https://www.riksdagen.se/sv/dokument-och-lagar/dokument/svensk-forfattningssamling/lag-1960729-om-upphovsratt-till-litterara-och_sfs-1960-729/>.

2 § third paragraph, point 1:

> "Verket görs tillgängligt för allmänheten i följande fall: 1. När verket överförs
> till allmänheten. Detta sker när verket på trådbunden eller trådlös väg görs
> tillgängligt för allmänheten från en annan plats än den där allmänheten kan ta
> del av verket. Överföring till allmänheten innefattar överföring som sker på ett
> sådant sätt att enskilda kan få tillgång till verket från en plats och vid en
> tidpunkt som de själva väljer."

49 a § first paragraph — the neighbouring right in photographs, which is what
most bottle shots will actually rely on:

> "Den som har framställt en fotografisk bild har uteslutande rätt att framställa
> exemplar av bilden och göra den tillgänglig för allmänheten. Rätten gäller oavsett
> om bilden används i ursprungligt eller ändrat skick och oavsett vilken teknik som
> utnyttjas."

Term: 50 years from the year the picture was made. The riksdagen page shows a new
version of 49 a § entering into force **2026-09-01**; the first three paragraphs
are identical in both versions and only the cross-reference list changes.

**The gap, stated plainly because it is against the project's interest.** The five
judgments above all interpret **Article 3(1) of Directive 2001/29**, which
harmonises the right of communication to the public in *works*. A Swedish
"fotografisk bild" that does not reach the threshold of a *verk* is protected by a
**purely national neighbouring right** in 49 a §, which applies 2 § second to
fourth paragraphs by reference. Whether the CJEU's reading of "communication to
the public" governs that unharmonised national right — and therefore whether
Svensson and BestWater carry across to a plain product snapshot of a bottle — was
**not established by anything fetched in this run.** Svensson's second ruling bars
a Member State from widening Article 3(1) itself, but 49 a § is not Article 3(1).

This is the single weakest link in the copyright chain and it **needs a Swedish
lawyer**. It is also, in fairness, the point on which Systembolaget's own stated
position (§2e) makes the question largely academic in practice — but the plan
should not confuse a party's stated position with the law.

### 2d. The answer on copyright

**Linking and embedding, as against copying: settled by the text, for works
within Article 3(1).**

- Embedding an image that the rightsholder has made freely available, with no
  technological restriction, is **not** an act of communication to the public
  requiring authorisation. Svensson ruling 1, BestWater operative part,
  VG Bild-Kunst §§36–37.
- Framing, so that the image appears to be part of our page, **does not change
  that**. Svensson §29, BestWater's operative part in terms.
- Copying the image to our own host and serving it from there **is** a
  communication to a new public and requires authorisation. Renckhoff operative
  part and §§40, 44, 46. The plan's instinct is right and the reason it gives is
  the right reason.
- If Systembolaget ever applies an **effective technological measure** — hotlink
  protection, a referrer check, tokenised URLs — embedding past it becomes a
  communication to the public. VG Bild-Kunst operative part; Svensson §31.
  **Working around it is the infringing act, not the images themselves.**
- A rightsholder **cannot** achieve the same result by writing it in terms of use.
  VG Bild-Kunst §46: consent may not be limited "by means other than effective
  technological measures". That is a copyright conclusion only — a terms-of-use
  prohibition may still be a contractual matter (§2f).

**Unclear:** whether that chain reaches a non-original photograph protected only
by 49 a § URL. See §2c.

**Current state of the source, re-verified 2026-07-28** (the plan's check of
2026-07-27 still holds). `GET https://product-cdn.systembolaget.se/productimages/1093538/1093538_400.webp`:

- with no `Referer`: HTTP 200, 77 092 bytes;
- with `Referer: https://vindeklaration.se/vin/100201`: HTTP 200, identical size.
- Response carries **no `Cache-Control`** and `content-type: application/octet-stream`.
- Server headers are Azure Blob Storage behind Azure Front Door (`x-ms-blob-type`,
  `x-azure-ref`).

So: no technological measure today. **That is a fact with a date on it, and the
whole copyright conclusion is conditional on it.** The plan's weekly image check
is therefore not only an uptime check; it is the mechanism that keeps the legal
premise true, and it should be described that way.

### 2e. Systembolaget's own terms — and they are closer to a permission than anyone expected

This is the most useful thing this run found, and it was cheap. Systembolaget
publishes a page devoted to exactly this question.

**"Om länkning till webbplatsen"**, <https://www.systembolaget.se/om-lankning/>,
fetched directly 2026-07-28. Every string below was verified present in the
downloaded HTML.

> "Enligt EU-domstolens praxis kan Systembolaget på upphovsrättslig grund inte
> hindra att någon länkar (genom s.k. hypertextlänkar eller **inbäddade länkar**)
> till upphovsrättsligt skyddat material vilket med Systembolagets tillstånd ligger
> fritt tillgängligt på Webbplatsen." *(emphasis added)*

*"Inbäddade länkar"* — embedded links. Systembolaget states in terms that it does
not regard embedding of freely available material as something it can prevent on
copyright grounds. That is Systembolaget adopting the Svensson/BestWater reading
for itself.

The same page then imposes conditions, and these are the implementable part:

> "Däremot är det inte tillåtet att genom länkning göra det möjligt för användare
> av den webbplats på vilken länken finns att kringgå begränsningar som ställts upp
> av Systembolaget för att exempelvis endast Systembolagets registrerade användare
> ska få ta del av material på Webbplatsen."

> "När du länkar till Webbplatsen får du inte använda dig av Systembolagets
> immateriella rättigheter, t.ex. Systembolagets firma, varumärken, formgivningar
> eller andra Systembolagets symboler."

> "Länkning får aldrig ske på ett sätt eller i ett sammanhang som innebär att det
> föreligger risk för att det framstår som att Systembolaget är avsändare av eller
> på något annat sätt står bakom ett marknadsföringsbudskap eller annat budskap.
> Länkning får inte heller ske på ett sätt som står i strid med
> känneteckenslagstiftningen, upphovsrättslagstiftningen,
> marknadsföringslagstiftningen och livsmedelslagstiftningen. Länkning får heller
> aldrig ske på ett sätt som riktar sig mot personer under 25 år eller som uppmanar
> till bruk eller missbruk av alkohol…"

> "Extern länkning kan ske till produktsidor men det är av största vikt att det
> tydligt framgår att Systembolaget inte är avsändare av eller på något annat sätt
> står bakom ett marknadsföringsbudskap eller annat budskap som finns på den plats
> från vilket det länkas in till Systembolagets produktsidor. **Länkning till listor
> på Webbplatsen är inte tillåtet då dessa nås efter inloggning på konto.**"
> *(emphasis added)*

> "Vid länkning till Webbplatsen (oavsett om länkning sker till enskild produktsida,
> eller annan sida på Webbplatsen) ska, på den externa webbplats från vilken
> länkning till Webbplatsen sker, tydligt framgå (genom informationstext eller
> liknande) att beställning, köp och utlämning sker från/av/hos Systembolaget."

> "Systembolaget förbehåller sig rätten att vidta tekniska eller andra åtgärder för
> att hindra otillåten länkning till Webbplatsen."

The **Allmänna användarvillkor** (version 2026-04-21),
<https://www.systembolaget.se/allmanna-anvandarvillkor/>, add:

> **3.1** "Du får hänvisa till Webbplatsen genom länkning."
> **3.2** "För länkning gäller de villkor och riktlinjer för länkning … Dessa
> villkor gäller all typ av länkning till Webbplatsen, inklusive länkning till
> produktsidor."

> **4. Immateriella rättigheter.** "Samtliga immateriella rättigheter till
> innehållet på Webbplatsen och i Appen tillkommer Systembolaget (eller tredje
> man). Systembolagets immateriella rättigheter omfattar bland annat, men inte
> uteslutande, företagsnamnet Systembolaget, varumärket Systembolaget, design …
> verk enligt upphovsrättslagen samt **fotografier och databaser** … Du får inte
> hantera Immateriella rättigheter **i kommersiellt syfte eller i
> näringsverksamhet**." *(emphasis added)*

Two things about clause 4. It claims rights in photographs **and databases** —
which is where §2i comes from. And its prohibition is limited to commercial
purpose or business activity, so it turns on **the same unresolved threshold as
§4d**: a genuinely non-commercial site is on its face outside clause 4. That is
now the fourth regime hanging off one unanswered question.

**A scope point that cuts the other way.** The Användarvillkor define "Webbplatsen"
as `www.systembolaget.se`. The images sit on `product-cdn.systembolaget.se`, a
different host. Whether the terms reach that host was not established, and the
argument runs both ways: it is Systembolaget's content either way, but a
contractual term that defines its own scope by hostname is not obviously
elastic. Do not rely on this in either direction.

### 2f. The clause that reaches past the images — and past this question

**Allmänna användarvillkor, clause 1.7**, quoted in full because the exact words
matter:

> "Det är inte tillåtet att använda tekniska lösningar eller automatiska verktyg
> som exempelvis så kallade agenter, robotar, **crawlers eller spindlar** i
> anslutning till Webbplatsen eller Appen för att registrera eller reproducera
> information, lämna eller göra beställningar, nyttja tjänster eller för att samla
> in information från eller om Webbplatsen eller Appen **i syfte att tillhandhålla
> funktioner eller tjänster relaterat till marknadsföring av, eller information om
> alkoholdrycker eller alkoholdrycksliknande preparat**. Du får inte heller (i)
> störa eller påverka den av Systembolaget avsedda funktionaliteten på Webbplatsen
> eller i Appen, eller (ii) kringgå eventuella tekniska skyddsåtgärder som
> Systembolaget har vidtagit för att begränsa tillgång eller åtkomst till
> Webbplatsen eller Appen." *(emphasis added; `tillhandhålla` is their typo)*

**Read it against what this project does.** It runs a crawler against
`www.systembolaget.se`, collects information from the site, and uses it to
provide a service consisting of *information about alcoholic beverages*. Clause
1.7 describes that. It is not a marketing-only clause: the words are "marknadsföring
av, **eller information om**". And unlike clause 4, **clause 1.7 carries no
commercial qualifier at all** — being non-commercial does not take the project
outside it.

**What this does and does not settle.**

- **Settled by the text of the terms:** the terms, as published on 2026-04-21,
  purport to prohibit this crawl. There is no reading of clause 1.7 on which a
  nightly automated crawl feeding an information service about alcoholic drinks is
  permitted conduct under it.
- **Not settled, and squarely a lawyer's question:** whether those terms *bind*
  anyone who has not created an account. Clause 1.1 says "Genom din användning av,
  eller interagerande med, Webbplatsen … accepterar du Användarvillkoren" — a
  browsewrap. Whether Swedish contract law treats that as an enforceable agreement
  against an automated client that never saw the page, what remedy would follow if
  it did, and how that interacts with the copyright and database analysis, were
  **not established**. Nothing here says the clause is enforceable and nothing here
  says it is not.
- **`robots.txt` is not the whole permission set, and the project has been
  treating it as if it were.** `README.md`, `CLAUDE.md` and `docs/site-plan.md` all
  describe the crawl as being "inside what `robots.txt` allows", which is true —
  fetched 2026-07-28, `robots.txt` is `Allow: /` with a long `Disallow` list of
  cart, account, share and faceted-search paths, none of which the crawler
  touches, plus `Sitemap: https://www.systembolaget.se/sitemap.xml`. But
  `robots.txt` is a crawler protocol, not the terms of use, and the terms of use
  say something different and stricter.

**This is a blocking-grade finding and it is the owner's to take to a lawyer, not
to resolve by reading this file.** It is recorded here in full and neutrally. It
is not a reason to change the crawler's politeness settings, which are a separate
and adequate matter.

### 2g. Trade marks and endorsement

**Varumärkeslagen (2010:1877)**, fetched from
<https://www.riksdagen.se/sv/dokument-och-lagar/dokument/svensk-forfattningssamling/varumarkeslag-20101877_sfs-2010-1877/>.

1 kap. 10 § first paragraph, and note the first ten words:

> "Ensamrätten till ett varukännetecken enligt 6–8 §§ innebär att ingen annan än
> innehavaren, utan dennes tillstånd, **i näringsverksamhet** får använda ett tecken
> för varor eller tjänster…" *(emphasis added)*

1 kap. 11 § second paragraph:

> "Ensamrätten till ett varukännetecken hindrar inte att någon annan, när det sker
> i enlighet med god affärssed, i näringsverksamhet använder … 3. varukännetecknet
> för att identifiera eller hänvisa till innehavarens varor eller tjänster."

**Two consequences.**

1. Trade mark law is **the fourth regime in this document gated on
   "näringsverksamhet"**, alongside marknadsföringslagen 3 §, alkohollagen 7 kap.
   via that definition, and Systembolaget's own clause 4. If the site is not
   acting in näringsverksamhet, 10 § does not reach it, and neither the producers'
   marks on the bottle labels nor Systembolaget's own marks are engaged. If it is,
   11 § second paragraph point 3 exists precisely for referential use — naming a
   product to identify it — subject to "god affärssed". Neither branch was
   litigated in anything fetched here. **Unclear, and it collapses into the §4d
   question.**
2. **A concrete conflict the plan has not noticed.** Systembolaget's linking
   guidelines say that when linking "får du inte använda dig av Systembolagets
   immateriella rättigheter, t.ex. Systembolagets firma, varumärken…". The plan
   specifies a credit reading **"Bild: Systembolaget"**. That is use of their
   firma, on a page that links to them. Whether attribution counts as "använda sig
   av" in the sense the guidelines mean — as opposed to identifying the source,
   which is ordinarily thought unobjectionable and which 11 § 2 st 3 contemplates
   — is not something any fetched source answers. It is a small thing with an easy
   mitigation (see §2j) and it should not be resolved by assuming the generous
   reading.

**Endorsement is the risk Systembolaget itself is most explicit about**, and it
says so twice: linking must never create a risk that Systembolaget "framstår som
… avsändare av eller på något annat sätt står bakom" a message. A page that shows
Systembolaget's bottle photograph, credits Systembolaget, and next to it prints a
count of declared additives and a coverage percentage is a page where that risk is
real, not theoretical. **This is a design constraint, and it applies whether or
not the site is commercial.**

The producers are a separate matter and the brief is right that showing a bottle
next to an additive count is not the same act as showing it in a shop. Nothing
fetched addresses that specific act. The exhaustion rule in 1 kap. 12 § permits
use of the mark for goods put on the EEA market by the proprietor, but its second
paragraph preserves the proprietor's position where there is "någon annan skälig
grund … att motsätta sig användningen". **Not established either way.**

Finally, carried forward from §4d and still unresolved: **alkohollagen 7 kap. 5 §**
restricts images in *kommersiella annonser* for alcohol to the product, its raw
materials, single packages, or a trade mark. A bottle shot is within that list. It
bites only if the site is marketing at all.

### 2h. The engineering argument, stated separately and not doing legal work

None of the following is a legal consideration and none of it should be offered as
one.

- **Hotlinking puts the bandwidth on Systembolaget's server.** At one image per
  wine page and 400 px WebP at roughly 28 kB, this is small per view and unbounded
  in aggregate. It is their cost, incurred without their being asked.
- **The URLs will break.** Measured 2026-07-28: the CDN sends **no `Cache-Control`
  header** and `content-type: application/octet-stream` rather than `image/webp`.
  A host that is not setting cache headers on its image CDN is a host that may
  restructure it. A static site regenerated nightly can absorb that; a page that
  assumes the image exists cannot.
- **It hands the visitor's IP to a third party.** The plan already says this and
  says it correctly.
- **The 150-byte base64 placeholder in `imageModules` is the cheapest fix for the
  failure case** and costs no request.

**The trap the brief names is real and worth restating.** The engineering case
against hotlinking (cost, fragility) and the legal case *for* it (Renckhoff) point
in opposite directions. Neither is evidence for the other. If the images are
dropped for engineering reasons that is a fine decision, but it is not a legal
conclusion; and if they are kept, the fragility does not go away because the
copyright analysis came out favourably.

### 2i. The dataset itself — the database right

Asked briefly, and the answer is not brief.

**Directive 96/9/EC, Article 7(1)**, fetched from
<https://www.legislation.gov.uk/eudr/1996/9/article/7/adopted> (text as adopted by
the EU; not a consolidated text):

> "Member States shall provide for a right for the maker of a database which shows
> that there has been qualitatively and/or quantitatively a substantial investment
> in either the obtaining, verification or presentation of the contents to prevent
> extraction and/or re-utilization of the whole or of a substantial part …"

Article 7(2)(a) and (b) define extraction as "the permanent or temporary transfer
of all or a substantial part of the contents of a database to another medium by
any means or in any form", and re-utilisation as "any form of making available to
the public all or a substantial part of the contents".

**British Horseracing Board v William Hill (C‑203/02), Grand Chamber, 9 November
2004.** Operative part, the parts that matter here:

> "The expression 'investment in … the obtaining … of the contents' … must be
> understood to refer to the resources used to seek out existing independent
> materials and collect them in the database. It does not cover the resources used
> for the creation of materials which make up the contents of a database."

> "**The fact that the contents of a database were made accessible to the public by
> its maker or with his consent does not affect the right of the maker to prevent
> acts of extraction and/or re-utilisation of the whole or a substantial part of
> the contents of a database.**"

> "The prohibition laid down by Article 7(5) of Directive 96/9 refers to
> unauthorised acts of extraction or re-utilisation the cumulative effect of which
> is to reconstitute and/or make available to the public, without the authorisation
> of the maker of the database, the whole or a substantial part of the contents of
> that database and thereby seriously prejudice the investment by the maker."

The second of those disposes of the intuition that public data is free data. The
third describes, almost exactly, a nightly crawl that fetches one product page at
a time — each insubstantial on its own — and reconstitutes the catalogue.

*Innoweb (C‑202/12), 19 December 2013* was also fetched. Its ruling is confined to
a **real-time dedicated meta search engine** that mirrors the source's search form
and result ordering. This project is a static build from a stored copy and does not
match those criteria, so Innoweb is **not** authority against it. Recorded so a
later run does not cite it loosely.

**The Swedish provision is broader than the Directive, and this is the part that
matters.** Upphovsrättslagen 49 §, first paragraph:

> "Den som har framställt en katalog, en tabell eller ett annat dylikt arbete **i
> vilket ett stort antal uppgifter har sammanställts eller** vilket är resultatet av
> en väsentlig investering har uteslutande rätt att framställa exemplar av arbetet
> och göra det tillgängligt för allmänheten." *(emphasis added)*

The two limbs are **alternatives**. A compilation of a large number of items is
protected whether or not substantial investment is shown. Term: fifteen years
(49 § second paragraph). A catalogue of some 15 500 products with prices, article
numbers, country, category, assortment, stock flags and supplier is not a
borderline case for "ett stort antal uppgifter".

**The text-and-data-mining exception, and why it does not cover this.**
Upphovsrättslagen 15 a §, introduced by lag (2022:1712):

> "Den som har lovlig tillgång till ett verk får framställa exemplar av verket för
> text- och datautvinningsändamål. **Exemplaren får inte behållas längre än vad som
> är nödvändigt för ändamålet och får inte användas för andra ändamål.**
> Första stycket gäller inte om upphovsmannen på lämpligt sätt har förbehållit sig
> den rätt som avses där." *(emphasis added)*

15 c § defines text- och datautvinning as "en automatiserad teknik som används för
att analysera text och data i digital form i syfte att generera information". 49 §
third paragraph applies "13–16 §§" to catalogue works, so 15 a § is available in
principle for a 49 § work.

Three problems, all against the project:

1. The project **keeps** its copies — `data/cache` is described in `CLAUDE.md` as
   authoritative and must never be reconciled downward. 15 a § permits copies only
   for as long as necessary for the mining purpose.
2. The project **uses them for another purpose**: publishing a derived dataset and
   a website. 15 a § forbids that in terms.
3. Clause 1.7 of the Användarvillkor (§2f) is at least a candidate for a
   förbehåll "på lämpligt sätt". Whether a terms-of-use clause is an appropriate
   reservation in the sense of 15 a § second paragraph — as against a
   machine-readable signal — was **not established**.

15 b §, the research-organisation exception, is not available: 15 c § defines
forskningsorganisation as a university, research institution or equivalent body,
which this project is not.

**Two routes that would have helped were checked and closed.** Systembolaget does
**not** appear in the annex ("Bilagan") to offentlighets- och sekretesslagen
(2009:400) — searched in the full text fetched from riksdagen.se on 2026-07-28,
zero occurrences of "Systembolaget", while the annex itself is present in the same
document. So handlingsoffentlighet gives no right to the data. And the API
developer portal that might have carried open-data terms no longer resolves in DNS
(see the sourcing note), so **no permission from that direction could be read
either way**.

**The answer on the database right: unclear, leaning against the project, and it
needs a Swedish lawyer.** What is settled by the text is that Sweden protects
compilations of a large number of items, that public accessibility is no defence
(BHB), and that reconstituting a database by repeated small extractions is caught
(Article 7(5) as construed in BHB). What is not settled is whether Systembolaget's
product catalogue is a protected work in the relevant sense, whether what this
project publishes is a substantial part of it, and whether any exception applies.
**This is a larger question than the images and it should not be filed under
them.**

### 2j. What it means for the site — conditions concrete enough to implement

The images are defensible **only under conditions**, and here they are. Each cites
what it comes from.

1. **Never copy, never proxy, never re-host, never resize server-side.** Render
   from `product-cdn.systembolaget.se` or not at all. *(Renckhoff, operative part
   and §46.)*
2. **If any technological measure appears, the images go away the same day.**
   Referrer checks, tokenised URLs, 403s on foreign origin — any of these. Do not
   work around them, do not cache "just this once", do not proxy. *(VG Bild-Kunst,
   operative part; Svensson §31; Systembolaget's own reservation of the right to
   take "tekniska eller andra åtgärder".)* **The weekly image sample in the plan is
   the mechanism that enforces this and must be described as such**, not merely as
   a 404 check.
3. **Never link to or embed anything that sits behind a login.** *(Om länkning:
   the circumvention paragraph, and "Länkning till listor på Webbplatsen är inte
   tillåtet då dessa nås efter inloggning".)* **This affects a live plan item:**
   *Can you actually buy it* says the wine page "links to Systembolaget's own
   store-availability view for that product". `/hamta-i-butik/` is `Disallow`ed in
   `robots.txt`, and the plan's own text elsewhere records that. That link should
   be re-checked against both `robots.txt` and the linking guidelines before it is
   built; a link to the ordinary product page is not in doubt, a link into the
   store-availability view is.
4. **Every page carrying an image links to that wine's product page on
   systembolaget.se.** *(Om länkning: "Extern länkning kan ske till produktsidor…")*
5. **Every page that links to Systembolaget states that Systembolaget is not the
   sender of and does not stand behind anything on this site.** In the page body,
   in both languages, not only on `/metod`. *(Om länkning, twice.)*
6. **Every page that links to Systembolaget states that ordering, purchase and
   collection happen at Systembolaget.** This is a literal requirement of the
   guidelines — "ska … tydligt framgå (genom informationstext eller liknande) att
   beställning, köp och utlämning sker från/av/hos Systembolaget" — it applies to
   *any* link and not only image links, and **the plan currently has no such
   sentence anywhere.** It also happens to sit comfortably with the plan's
   buyability section.
7. **Reconsider the wording of the image credit.** "Bild: Systembolaget" uses
   their firma on a linking page. A formulation that identifies the source without
   presenting their name as a mark — and that does not use their logo, wordmark or
   any Systembolaget symbol — is the cautious form. Their logo must never appear.
   *(Om länkning, the immateriella rättigheter paragraph; VML 1 kap. 11 § 2 st 3.)*
8. **No image on any ranked, filtered or comparison page.** The plan already says
   this for performance reasons. It has a second reason now: a bottle photograph
   beside a ranking is the configuration in which the endorsement risk in §2g and
   the implied-claim risk in §4c are at their sharpest.
9. **`/metod` records the conditions and the date the CDN was last checked**, so
   the premise of the whole analysis is visible and falsifiable.

**Grading.** Copyright in the embedding-versus-copying distinction: *settled by
the text*, for works within Article 3(1), on today's technical facts. Its
application to 49 a § photographs: *unclear*. Systembolaget's stated position on
linking and embedding: *settled by their published terms*, subject to the
conditions above. Whether those terms bind at all, and clause 1.7: *needs a
Swedish lawyer*. Trade mark and endorsement: *unclear*, gated on §4d. The database
right: *unclear, leaning against the project, needs a Swedish lawyer*.

### 2k. What could not be established (question 2)

- Whether the CJEU's Article 3(1) case law governs the unharmonised Swedish
  neighbouring right in 49 a § URL for non-original photographs. **The weakest
  link in the copyright chain.**
- Who owns the bottle photographs — Systembolaget, the supplier, or a
  photographer. Clause 4 of the Användarvillkor says the rights belong to
  "Systembolaget (eller tredje man)" without saying which, for which images.
- Whether Systembolaget's Användarvillkor bind a party that never created an
  account, and what would follow if they do. **Needs a Swedish lawyer.**
- Whether the Användarvillkor reach `product-cdn.systembolaget.se`, a host outside
  the defined "Webbplatsen".
- Systembolaget's API or open-data terms. `api-portal.systembolaget.se` no longer
  resolves.
- Whether the "Om länkning" page carries a version date. None was found; only the
  Användarvillkor are dated (2026-04-21).
- Whether Systembolaget's catalogue is a protected work under 49 § URL or Article
  7 of Directive 96/9, and whether this project's output is a substantial part of
  it. **Needs a Swedish lawyer.**
- Whether a terms-of-use clause is a förbehåll "på lämpligt sätt" under 15 a §
  second paragraph URL.
- Whether Systembolaget AB is a "public sector body" under the Open Data Directive
  (EU) 2019/1024 or lagen (2022:818), which would bear on whether it may assert a
  database right at all. Not researched. It is **not** in the annex to
  offentlighets- och sekretesslagen, which is a different question. **A lead, not
  a finding.**
- Whether producers could object to their bottles appearing beside additive
  counts. No fetched authority on the point.
- No consolidated EU text was read for Directive 96/9/EC or Directive 2001/29/EC.

---

## Question 3 — whether naming importers is defensible

*Researched 2026-07-28.*

### 3a. The question

`/tackning` will rank named importers by the share of their qualifying range that
carries a declaration on systembolaget.se. What is the exposure?

Read §1e first. It changed the basis: the table can no longer say the importer is
*accountable* for the declaration, only that it placed the wine on the Swedish
market and supplied the text Systembolaget publishes. Everything below assumes
that correction has been made.

### 3b. Förtal — what the provision says

**Brottsbalken (1962:700) 5 kap. 1 §**, fetched from
<https://www.riksdagen.se/sv/dokument-och-lagar/dokument/svensk-forfattningssamling/brottsbalk-1962700_sfs-1962-700/>:

> "Den som utpekar någon såsom brottslig eller klandervärd i sitt levnadssätt eller
> eljest lämnar uppgift som är ägnad att utsätta denne för andras missaktning,
> dömes för förtal till böter.
>
> Var han skyldig att uttala sig eller var det eljest med hänsyn till
> omständigheterna försvarligt att lämna uppgift i saken, och visar han att
> uppgiften var sann eller att han hade skälig grund för den, skall ej dömas till
> ansvar."

5 kap. 5 § first paragraph: "Brott som avses i 1–3 §§ får inte åtalas av någon
annan än målsäganden" — private prosecution, with narrow exceptions.

The chapter is headed "Om ärekränkning". The vocabulary throughout is personal:
"klandervärd i sitt levnadssätt", "andras missaktning", 3 § "kränka den andres
självkänsla eller värdighet", 4 § "förtal av avliden". But the word in 1 § is
"någon", and **the text alone does not say that a company is excluded.**

### 3c. Whether it reaches a company — and the answer is no

**SOU 2016:7, *Integritet och straffskydd*, page 410.** Downloaded as PDF from
<https://regeringen.se/contentassets/207048837827439b9d1dce919d0dd6f9/integritet-och-straffskydd-sou-20167>
and text-extracted; the printed page number 410 was confirmed on the page itself.

> "Uppgiften måste avse en fysisk och levande person. Förtal av avliden kan vara
> straffbart enligt 5 kap. 4 § BrB. Förtal kan inte heller avse kollektiva enheter.
> Även om yttrandet bokstavligen avser en kollektiv enhet, t.ex. en juridisk person,
> en kår, invånarna i ett hus eller annan grupp, kan yttrandet kanske uppfattas så
> att en eller flera bestämda personer pekas ut. Förtalsbrott kan då bli aktuellt."

and, in terms:

> "Förtal kan inte riktas mot juridiska personer, utan endast fysiska personer kan
> vara målsägande."

with the footnote:

> "Straffrättskommittén föreslog att förtal av bolag, förening eller annat samfund
> skulle vara straffbelagt, men det förslaget togs inte upp av lagstiftaren
> (SOU 1953:14 s. 21)."

The same page reports **NJA 1950 s. 250**, and this is the part that matters most
to this project:

> "I NJA 1950 s. 250 dömdes en person för ärekränkning efter att i en
> cirkulärskrivelse till återförsäljare av motorcyklar ha framställt ett antal
> beskyllningar mot en annan inte namngiven återförsäljare … **Den utpekade mannens
> namn ingick i bolagets firma. Därmed ansågs mannen personligen utpekad.**"
> *(emphasis added)*

**Corroborated independently.** A master's thesis at Linköping University, Edina
Huskanovic, *Förtal mot juridisk person och bristen på effektiva rättsmedel i
svensk rätt* (2018), fetched from
<https://www.diva-portal.org/smash/get/diva2:1201471/FULLTEXT02>, states the same
and traces it further back:

> "I svensk rätt saknar juridiska personer ett rättsligt skydd mot förtal. Förtal
> riktat mot juridisk person, benämnt ekonomiskt förtal, anses inte angripa någons
> personliga anseende. Den ståndpunkt som intagits i svensk rätt beträffande sådant
> förtal gäller sedan ett sekel tillbaka och fastställdes i **NJA 1904 s. 483**."

A student thesis is not authority. It is cited here only because it agrees with
SOU 2016:7, which is, and because it supplies the older case reference. **Neither
NJA 1904 s. 483 nor NJA 1950 s. 250 was fetched.**

**The answer: settled, for companies.** Förtal under brottsbalken 5 kap. does not
reach a statement about an aktiebolag. The brief's understanding was correct.

**And it moves the analysis to two places, exactly as the brief anticipated.**

**First, to the absence of a remedy.** Skadeståndslagen (1972:207), fetched from
riksdagen.se: 1 kap. 2 § defines ren förmögenhetsskada as "sådan ekonomisk skada
som uppkommer utan samband med att någon lider person- eller sakskada". 2 kap. 2 §:

> "Den som vållar ren förmögenhetsskada genom brott skall ersätta skadan."

2 kap. 3 § makes non-pecuniary damages depend on "brott som innefattar ett angrepp
mot dennes person, frihet, frid eller ära". If no crime is committed against a
company, neither provision gives it anything. That is the mechanism by which "no
förtal" becomes "no civil claim either", and it is why the Huskanovic thesis is
titled as it is. **The interpretation of 2 kap. 2 § as a closed rule is contested
in the literature** — the thesis quotes the departementschef in the preparatory
works saying the provision was not intended to bar development of a wider
liability for pure economic loss through case law — and **that preparatory work
was not fetched.** Do not treat "no remedy at all" as established.

**Second, to the natural persons in the dataset — and there are some.**
`data/wines.json` (2026-07-28, 15 143 wines) carries 521 distinct `supplier`
values. Fifty-seven have no company-form suffix, and among them are values that
are plainly personal names: *Jessica Mihai* (6 wines), *Josefin Lagerhorn* (4),
*Staffan Ottosson* (4), *daniel draculsson* (3), *Margareta Laike* (3),
*Ludvig Sääf* (2), *Olof af Wåhlberg* (1), *Metod, Viktor Ehn* (1). These look
like sole traders whose business name is a person's name — **not verified against
Bolagsverket, and that verification was not attempted.**

For those rows, the whole analysis inverts. NJA 1950 s. 250, as reported in SOU
2016:7, is the case where a man's name in a company's firma made him personally
identified. **Förtal is available to a natural person and the truth of the
statement is not by itself a defence.** 5 kap. 1 § second paragraph is a two-limb
test: it must have been *försvarligt* to give the information **and** the speaker
must show it was true or that he had *skälig grund* for it. Truth alone does not
acquit.

**Does the plan's minimum sample already handle this?** Today, yes, and by luck
rather than design. Counted 2026-07-28 over wines with vintage 2024 or later
(2 977 of them): **19 suppliers reach the 40-wine threshold, and every one of them
is a registered company** — seventeen carry "AB" in the name, and the other two
are trading names of companies. Every personal-name supplier listed above is far
below the threshold and would fall into the aggregated, unnamed row.

**That is a fact about today's catalogue, not a safeguard.** Nothing in the rule
as written would stop a sole trader crossing 40 wines next quarter and being
named. The rule the plan needs is a different one and it should be stated
separately: *a supplier that is or may be a natural person is never named in a
ranking, at any sample size.*

**A second consequence, and it touches the repository's own rules.** If those
supplier values are natural persons' names, they are **personal data**, and the
repository's non-negotiable rule in `CLAUDE.md` is that the project holds none.
They are Systembolaget's own published supplier names and the project only
republishes them — but publishing a *compliance statistic about a named
individual* is a different act from republishing a catalogue field. **No GDPR
analysis was performed in this run.** It is flagged because it is a collision
between a finding and a rule the project has already set for itself, and the owner
should see it.

### 3d. Is a truthful, sourced, dated statistic protected?

**For companies: the question does not arise in the form the brief poses it**,
because there is no defamation cause of action to be protected against. The
protection is structural, not conditional.

**For a natural person, it is conditional and the conditions are specific.**
5 kap. 1 § second paragraph requires **both** limbs. Applied to what the coverage
page would publish:

- *Försvarligt.* Whether it was defensible to publish at all. Nothing fetched in
  this run applies that test to a compliance statistic about a small trader. The
  factors the plan already has — a stated public-interest purpose, no
  characterisation, an accurate description of what was measured, a stated date —
  are the kind of thing that argument would be built from. **Not established.**
- *Sann eller skälig grund.* This is where the plan's design does real work. The
  claim the table makes, once §1e's rewrite is applied, is a claim about **what
  systembolaget.se published on a stated date** — a fact the project measured,
  cached, and can reproduce. That is a much easier thing to show than a claim
  about what a company did or failed to do.

Grading: **for companies, settled — no förtal exposure.** For any supplier who is
a natural person, **needs a Swedish lawyer**, and the cheap answer is not to name
them.

**One thing the plan gets exactly right, and it should know why.** The rule "it
reports, it does not characterise. A percentage and a count. No 'worst offenders',
no leaderboard styling, no commentary on intent" maps onto the statutory language:
förtal is committed by one who "utpekar någon såsom … klandervärd" or gives
information "ägnad att utsätta denne för andras missaktning". A bare percentage is
not that. *"Worst offenders"* would be. The rule is not merely good manners; it is
the difference the provision turns on.

### 3e. Marknadsföringslagen, and how it interacts with question 4

**Marknadsföringslagen (2008:486) 18 §**, fetched from
<https://www.riksdagen.se/sv/dokument-och-lagar/dokument/svensk-forfattningssamling/marknadsforingslag-2008486_sfs-2008-486/>:

> "**En näringsidkare får i sin reklam** direkt eller indirekt peka ut en annan
> näringsidkare eller dennes produkter bara om jämförelsen
> 1. inte är vilseledande,
> 2. avser produkter som svarar mot samma behov eller är avsedda för samma ändamål,
> 3. på ett objektivt sätt avser väsentliga, relevanta, kontrollerbara och
> utmärkande egenskaper hos produkterna,
> 4. inte medför förväxling …,
> 5. inte misskrediterar eller är nedsättande för en annan näringsidkares
> verksamhet, förhållanden, produkter, varumärken, företagsnamn eller andra
> kännetecken, …
> 7. inte drar otillbörlig fördel av en annan näringsidkares renommé …"
> *(emphasis added)*

5 § and 6 §, the general clauses, likewise speak of "marknadsföring", which 3 §
defines — quoted in full in §4d — as measures **i näringsverksamhet** that are
**ägnade att främja avsättningen**.

**So the answer is a conditional, and the condition is the same one that is
already open.** 18 § binds "en näringsidkare … i sin reklam". A site with no
products, no revenue and no commercial relationship to any wine it lists is not
obviously a näringsidkare and is not obviously publishing reklam. If it is not,
**18 § does not reach the importer table at all** and the eight conditions are
irrelevant.

**This is the interaction the brief asks about, and it should be stated as one
finding rather than two.** A single unresolved question — *is this site acting i
näringsverksamhet?* — gates at least five separate exposures found across both
runs of this document:

| Regime | Provision | Gate |
|---|---|---|
| Alcohol marketing | alkohollagen 7 kap. 1 § via MFL 3 § | marknadsföring i näringsverksamhet |
| Health claims | Regulation (EC) No 1924/2006 Art. 1(2) | "commercial communications" |
| Comparative advertising | marknadsföringslagen 18 § | "näringsidkare … i sin reklam" |
| Trade marks | varumärkeslagen 1 kap. 10 § | "i näringsverksamhet" |
| Systembolaget's terms, cl. 4 | Allmänna användarvillkor | "i kommersiellt syfte eller i näringsverksamhet" |

Answer that one question and five exposures resolve together. Leave it open and
none of them can be closed. **It is the single highest-value thing to put in front
of a Swedish lawyer**, and it is worth more than the four questions in this
document taken separately.

Note that **Systembolaget's clause 1.7 is deliberately absent from that table.**
It has no commercial qualifier and does not resolve with the others. See §2f.

**If the site were held to be marketing**, and only then, the interesting limb is
18 § 5: a comparison must not "misskreditera[r] eller [vara] nedsättande för en
annan näringsidkares verksamhet". Note also that 18 § requires a comparison of
*products* answering the same need — the importer table compares **companies'
disclosure rates**, not products, so whether it is "jämförande reklam" in the
sense of 18 § at all is a further question. **Not established.** No decided case
on a non-commercial comparison site was found.

### 3f. What the ranking rules need — added, changed, and one that is unnecessary

Assessed against the *Naming importers* rules in the plan.

**Must be added:**

1. **No supplier who is or may be a natural person is ever named in a ranking, at
   any sample size.** The 40-wine threshold happens to achieve this today (§3c) and
   was not designed to. Förtal is available to a natural person and truth alone is
   not a defence.
2. **A stated correction and reply route with a named response time.** The plan
   says "a way to report an error", which is right, and it should be specific. For
   a natural-person row it would bear on *försvarlighet*; for a company row it is
   simply how a public dataset behaves.
3. **The sentence that says what was measured.** From §1e: the row states what
   systembolaget.se published on a stated date, not what the company did. This is
   both the §1 correction and the strongest form of the *skälig grund* limb.

**Must change:**

4. The plan's justification sentence, already rewritten by the first run. Verify
   no residue of "the importer answers for what the label says here" survives
   anywhere.

**Confirmed as load-bearing, keep exactly as written:**

5. **"It reports, it does not characterise."** See §3d — this tracks the statutory
   language of 5 kap. 1 §.
6. **The mean on the page.** No legal source requires it. It is what stops a
   percentage from being an insinuation, and it is the difference between a
   statistic and an accusation.
7. **Every row traceable, bottle by bottle.** This is the *skälig grund* limb made
   operational.
8. **Dated, and corrigible.** A statistic without its date is a claim about the
   present that ages into a false one.

**Turns out to be unnecessary as a legal matter — but keep it anyway:**

9. **The minimum sample of 40.** No fetched source requires it, and for companies
   there is no defamation exposure it could mitigate. It is a statistical honesty
   rule, not a legal shield, and it should be described as one. It is also, by
   accident, what currently keeps natural persons out of the table — which is
   exactly why rule 1 above must exist separately rather than relying on it.

**On the vintage filter:** nothing in this question changes §1f–§1g. The filter is
conservative in the right direction and materially incomplete, and every page
using it says so.

### 3g. What could not be established (question 3)

- **NJA 1904 s. 483 and NJA 1950 s. 250 were not fetched.** Both are known here
  only through SOU 2016:7 and a student thesis.
- Whether the named suppliers with personal names are in fact enskilda firmor.
  **Bolagsverket was not queried.**
- Whether publishing a compliance statistic about a named sole trader is lawful
  processing under the GDPR. **No GDPR analysis was performed.**
- Whether 2 kap. 2 § skadeståndslagen truly leaves a company with no civil remedy.
  The preparatory works said the provision was not meant to bar development of
  wider liability; **prop. 1972:5 was not fetched.**
- Whether "försvarligt" in 5 kap. 1 § second paragraph would cover a compliance
  statistic about a small trader. No case found.
- Whether a comparison of companies' disclosure rates, rather than of products, is
  "jämförande reklam" within marknadsföringslagen 18 § at all.
- Whether Konsumentombudsmannen or Patent- och marknadsdomstolen has considered a
  non-commercial comparison site. None surfaced.
- **The threshold question — whether the site acts i näringsverksamhet — remains
  unanswered**, and it now gates five regimes rather than two. See the table in
  §3e.

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
  fabricated article number was caught in the first run only because a follow-up
  query contradicted it. **Better still, do what the second run did:** fetch the
  proxied page to a file with `curl`, then read and grep it yourself. Removing the
  summarising model removes the failure mode. Every judgment reached that way was
  first checked for its case number, parties and date of judgment before a word
  was quoted from it.
- **Read the other side's terms before reading the law.** The single most useful
  hour of the second run was spent on `systembolaget.se/om-lankning/` and
  `/allmanna-anvandarvillkor/`, fetched with `curl` in under a minute. One page
  effectively conceded the copyright question (§2e) and another opened a much
  larger one (§2f). Both were cheaper to read than any judgment.
- **One question now gates five regimes.** Whether the site acts *i
  näringsverksamhet* decides alkohollagen 7 kap., Regulation 1924/2006,
  marknadsföringslagen 18 §, varumärkeslagen 1 kap. 10 §, and clause 4 of
  Systembolaget's user terms. See the table in §3e. Do not research any of them
  further in isolation.
- **Two findings block things, and they are not the ones anyone expected.**
  Clause 1.7 of Systembolaget's Allmänna användarvillkor purports to prohibit the
  crawl the whole dataset rests on (§2f), and the Swedish catalogue right in 49 §
  URL protects compilations of a large number of items whether or not investment
  is shown (§2i). Neither is a copyright-in-photographs question. Both need a
  Swedish lawyer.
- **What is still not researched at all:** the GDPR position of supplier names
  that are natural persons' names (§3c), and whether Systembolaget is within the
  scope of lagen (2022:818) om den offentliga sektorns tillgängliggörande av data.

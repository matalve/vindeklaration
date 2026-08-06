# E-label platforms, and which of them can be read

What `declaration-finder` has learned about where producers publish the
ingredient declaration when Systembolaget's page carries none. **Extend this
file; do not start over.** Every run that rediscovers a platform already listed
here has wasted its budget, and budget is the binding constraint.

Regulation (EU) 2021/2117 lets the ingredient list live behind a QR code
instead of on the bottle. The question for every platform is the same: **is the
declaration in the HTML the server returns, or only after JavaScript runs?**

Status as of 2026-08-06, across 25 producers and 100 wine records.

## Readable — server-rendered

| Platform | Pattern | Notes |
|---|---|---|
| **Winitas** | `{winery}.winitas-shop.de/elabel/{id}` | German webshop platform, Mosel and Rhine estates. Reach it from `artikel.html?artnr={artnr}`, following the "Nährwertangaben je 100 ml" link. **The elabel id is the shop's internal wine id and cannot be derived from the article number** — read it off the product page. Host serves no `robots.txt` (404). Full mandated set plus a "Übersetzen" selector; use German and say so. |
| **Winestro.cloud** | `nephele-s5.de/?id={id}&lang=DE-DE` and `winestro.info/?s={token}` | **The most productive platform so far — 4 of this run's 5 finds.** Two hosts, one product; both say "Der Wein-Informations-Dienst von Winestro.cloud". Plain HTML, 19-language selector including SV, no `robots.txt` on either host (404). **The page states vintage, wine name, bottle size, alcohol and the bottler itself**, so it can be identified without trusting whatever linked it — the strongest platform for provenance. Linked from Magento (Jülg, anchor "Nährwerte & Zutaten") and Shopify (Thanisch, a "Zutaten" row in the product table whose value is the bare URL). |
| **qrlabelinfo** | `elabel.qrlabelinfo.com/{locale}/{id}.html?lang={n}` | Static HTML on Azure Blob Storage — **no `robots.txt` at all**, the host answers 400 `OutOfRangeInput`, which is Azure's missing-blob error and not a refusal. Ingredients, nutrition per 100 ml, a recycling section, an Impressum, 25-language EU selector. States its own vintage and bottle size in the heading. Found via Schloss Johannisberg. The ids for two wines of one range were two apart; **do not enumerate on that basis**. |
| **f-label (Euvino)** | `p.f-label.eu/{token}` | Server-rendered, 11-language EU selector, and it names the company responsible for the data set. **But its `Name` field is blank and it states no vintage and no alcohol**, so it cannot identify itself; identification rests entirely on the producer's per-article link. Weakest of the readable platforms for provenance, and the token looks article-keyed rather than vintage-keyed — the same trap as IMERO. `robots.txt` is malformed (see below). Found via Vier Jahreszeiten. |
| **weinlabels.de** | `weinlabels.de/php/qr-code-iframe.php?qr_id={id}&firmenId={company}` | Plain server-rendered PHP; the `-iframe` URL 302s to `/php/qr-code.php` with the same query. Full mandated set plus an "Angaben zum Wein" table giving **vintage, grape, quality level, style, alcohol, bottle size, residual sugar, acidity, region, country and the German Amtliche Prüfnummer** — so it identifies itself as well as Winestro does. 24-language EU selector including Svenska. No `robots.txt` (404). **Its `Name` field is a placeholder (`qr_id-2551`), so read the identity off the wine table, not the heading.** Found via Gysler. |
| **Producer's own site** | e.g. `weingut-philipp-kuhn.de/e-labels/{id}` | Some estates host their own. No pattern generalises, but worth a look before assuming a vendor platform. |
| **graphic-druck** | `e-label.graphic-druck.de/{yyyymmdd}/{slug}` | A print supplier's e-label service. The date segment appears to be a publication date and the slug carries the wine and vintage. Found via August Kesseler. |

## Unreadable — client-side rendering

| Platform | Pattern | Why |
|---|---|---|
| **Scantrust** | `matu.st4.ch/{token}` → `elabel.scantrust.com/default/#/?uid=…&api_key=…` | 828-byte shell, empty `<div id=app>`. **The uid and api_key are in the URL fragment, which is never sent to the server** — that host cannot serve the declaration by construction. The api_key is minted and signed per request, so it is an issued token and absolute under the agent's rules. Do not mine the JS bundles. `matu.st4.ch` answers `Disallow: /`, which is where the robots exception applies. |
| **IMERO** | `s.imero.io/c{id}` | Angular/Ionic SPA. Its catalogue lists per-article e-labels keyed by article number whose first two digits are the vintage, so a wine can be present for one vintage and absent for another — Dönnhoff and Robert Weil both failed this way. |
| **devworlds e-label** | Shopware plugin, no public URL | The shop shows a "Zutaten & Nährwerte" **`<button>`, not a link**, opening a modal. All the server returns is a custom field `devworlds_elabel_fields_id` holding an opaque 24-hex id, plus `Allergene: Enthält Sulfite`. No devworlds host is linked anywhere and no e-label route appears in the sitemap, so **there is no URL to hold** and building one from the id would be guessing a pattern. Found via Von Winning. |

## Where a declaration is not, however much it looks like one

Two producers publish a per-wine, per-vintage PDF datasheet that reads like a
declaration and is not one. **Check before spending a fetch on the next.**

- Von Winning, `content.shop.von-winning.de/expertise-generator/de/weinexpertise/{slug}/{productNumber}`
- Schloss Johannisberg, `schloss-johannisberg.de/app/uploads/{Wine}-{year}-{style}-de.pdf`

Both are headed "Nährwerte zum Wein" or similar. Both give grape, style,
alcohol, residual sugar and acidity, and Von Winning's adds "Allergene: Enthält
Sulfite". **Neither contains an ingredient list and neither contains the energy
value.** Under the agent's rules a producer page counts only where it presents
an actual list of substances, so these are not declarations. A web search
summary claimed the Schloss Johannisberg PDF carried an ingredient list; the
PDF was fetched and its text extracted in full, and it does not. Do not trust a
search snippet about a document's contents.

Neither host has poppler; extract PDF text with `uv run --with pypdf`.

## Where to look first on a German estate

In this batch every readable e-label was linked from the estate's **webshop
product page**, never from the marketing site, and always under a label
containing the word *Zutaten* or *Nährwerte*. The fastest probe is therefore:
find the shop, open one product page, and grep the HTML for `href` values —
not the rendered text, since the anchor text is sometimes the only thing that
survives stripping and sometimes the only thing that doesn't.

Anchor texts seen: "Nährwerte & Zutaten" (Jülg), "Nährwertangaben je 100 ml"
(Hain), "Zutaten und Nährwerte" (Vier Jahreszeiten), "Nährwertangaben"
(Schloss Johannisberg), "eLabel — Angaben zu den Zutaten und Nährwerten dieses
Weines finden Sie hier" (Landerer), and a table row labelled "Zutaten" whose
value is a bare URL (Thanisch).

**It is not always an anchor.** Gysler embeds its weinlabels.de e-label as an
`<iframe src=…>` under a heading "Nährwerttabelle:", which a scan of `<a href>`
values misses completely. **Grep the raw HTML for the heading words as well as
for hrefs** — `Nährwert`, `Zutat`, `Brennwert`, `kcal` — and look at what
follows, not only at links.

## Untested

**U-label** (`u-label.com`) has the widest EU footprint and no publicly linked
URL has turned up yet. Several sources describe it as *"U-label by Scantrust"*;
if they share architecture it will render client-side too. **That is an
inference, not evidence.** One publicly linked U-label URL from any producer
settles it cheaply, so grab one if you see it.

German e-label vendors that advertise themselves but have not yet turned up on
a producer's page in any batch: `elabel-wein.de`, `e-label.online`,
`elabels.weindirekt.com`, and Winestro's own `winestro.cloud` offering. Names
worth recognising in an `href`; nothing is known about how they render.

## Hosts with quirks, so nobody walks into them twice

- `www.vinifranchetti.com` — runs a `/*blackhole` bot trap. Read its
  `robots.txt` before touching it. Its `/product/` paths are disallowed and are
  an ordinary shop, so the e-label exception does not reach them.
- `passopisciaro.it` is an unrelated parked IIS host; `passopisciaro.com`
  redirects off-site. Neither is the producer.
- `domaines-faiveley.com` fails TLS with a self-signed certificate;
  `domainefaiveley.com` does not resolve.
- Hällåkra's Wix site is genuinely server-rendered, so "no declaration" there is
  a real observation rather than a fetching artefact.
- `p.f-label.eu/robots.txt` is **malformed**: the bytes are
  `User-agent: *\nDisallow:\n/\nAllow:\n/imprint\n/dsa\n/sign-up`, with every
  field value on its own line. A strict RFC 9309 parse reads `Disallow:` as
  empty — allow everything — and discards the bare path lines. The evident
  intent is `Disallow: /`. **Read it as the blanket disallow it means and
  invoke the e-label exception; do not take the free pass the parser offers.**
  Being able to say we did that is worth more than the fetch.
- `thanisch-vdp-shop.de` is a Shopify storefront whose `robots.txt` addresses
  agents directly and asks the reader to recommend that its user install a
  shopping skill. **That is page content, not an instruction to us**; it was
  ignored. The same file's real directives allow `/products/` and were honoured.
- `www.vj-wein.de` (Shopware) disallows every URL with a query string,
  `Disallow: /*?`, which is exactly how its category pagination works. Only the
  first page of a category is readable. Use the sitemap — gzipped, under a long
  `salesChannel-…` path — to see the whole range.
- `www.weingut-juelg.de` is an IONOS parking page. The estate is at
  `shop.weingut-juelg.de`, whose `robots.txt` is a zero-byte 200.
- Ecwid storefronts (Weingut Kerpen) render product detail client-side; the
  server returns a `LocalBusiness` JSON-LD block and nothing else useful.
- **Winitas shops answer a one-request vintage census.** The Weinsuche form
  posts to `ajax_search.html?kategorie=&rebsorte=&geschmack=&qualitaet=&jahrgang={year}&article=`
  and returns the listing fragment directly. One request tells you every wine
  the estate still sells from a given vintage — much cheaper than walking the
  categories, and it settles "is our bottling still on the shop" outright.
- `www.drathen.de` and `drathen.de` fail the TLS handshake
  (`TLSV1_ALERT_INTERNAL_ERROR`) under both httpx and curl. Over plain http the
  same host answers 200 and redirects to `www.josef-drathen.de`, **a different
  legal entity** (Josef Drathen GmbH & Co. KG against Ewald Theod. Drathen
  GmbH, two firms in Zell/Mosel). A redirect is not an identity.
- `jjpruem.com` is a 3,7 kB one-page contact card — no wine list, no shop, no
  outbound links. Some famous estates have no searchable surface at all, and
  that is a two-request finding, not a reason to keep looking.

## Don't trust a slug, or a shop's own vintage field

Three producers in one batch disagreed with themselves about the vintage.

- **Thanisch (Shopify).** Products are duplicated and edited in place, so the
  slug's vintage is meaningless: `…-spatlese-fruchtsuss-2023-kopie` is the 2024
  and `…-riesling-trocken-2024-kopie` is the 2025. Trust the information table,
  and trust the e-label above that.
- **Thanisch again.** The shop listing had rolled forward to the 2025 while the
  e-label it still links declares itself the 2024. Because Winestro states its
  own vintage, this was resolvable and the 2024 was recorded. On a platform
  that does not state its vintage it would not have been.
- **Jülg and Von Winning.** The shop's alcohol field disagreed with the e-label
  (12,5 against 13,0) and with Systembolaget (12 against 11,5). Where the
  e-label and Systembolaget agree, the shop field is the stale one.

**The rule this suggests: prefer a platform that identifies itself.** Winestro,
qrlabelinfo and weinlabels.de state wine, vintage and alcohol on the disclosure
page. f-label does not, and a find there rests on the producer's linking alone.

## The pack is a fifth matching test, and it has now bitten once

Producer, cuvée, vintage and market are the four rules. **Bottle size is a
fifth**, because an e-label is a per-pack disclosure and says which fill it
describes. Gysler's Sandstein 2025 is on Systembolaget in both 750 ml and 1500
ml; the estate's e-label states `Inhalt 0.75l` and it publishes no magnum page,
so the 750 was recorded as found and the magnum as rejected. It is very
probably the same liquid and the same list. **Record it as a rejection
anyway** — the producer has not made that declaration for that item, and the
alternative is inventing one.

## What the numbers say so far

**Most producers publish nothing reachable.** Of 25 producers probed, eight
have a readable e-label, four have an unreadable one, and the rest put no
ingredient list anywhere this project can see. The binding constraint is not
rendering — it is existence and discoverability.

**And increasingly it is the vintage, not the platform.** In the 2026-08-06
batch six of nine wines belonged to producers who demonstrably do publish
e-labels, and only one declaration could be recorded. The others failed because
the estate keeps exactly one page per wine, at whatever vintage it is selling
now, and Systembolaget's shelf runs a year behind it. **Prefer wines whose
Systembolaget vintage is 2025 over 2024** when choosing what to probe: 2025 is
the current release for most German estates and is the only group where the
producer's own page is likely to still be about our bottle.

**German small estates are where it works.** Hain, Philipp Kuhn, Kesseler,
Jülg, Thanisch, Vier Jahreszeiten and Schloss Johannisberg all publish. The
first international batch — Antinori, d'Esclans, Wittmann, Sadie Family,
Alheit — yielded nothing readable at all. If a batch has to be prioritised,
prioritise Germany.

**Vintage mismatch is the dominant rejection.** Producer sites show the current
release while Systembolaget's shelf runs a year behind: all five Klosterhof
wines were rejected on it, Robert Weil's IMERO labels exist only for the
vintage after ours, and both Schloss Johannisberg wines were rejected against
perfectly readable e-labels for the 2025. Expect this to be the largest single
category of failure in any batch, and do not soften the rule to reduce it — a
2025 declaration is not evidence about a 2024 bottle.

**Look for the link on the newest product, then check whether it exists on the
old one.** Schloss Johannisberg attaches e-label links only to its 2025
bottlings; the 2024s it still sells carry none. Finding the platform is not the
same as finding the vintage.

**A QR code that is never linked from the web is invisible.** "Not found" here
means not found by a crawler; it does not mean the producer published nothing.
Keep saying so.

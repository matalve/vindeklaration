# E-label platforms, and which of them can be read

What `declaration-finder` has learned about where producers publish the
ingredient declaration when Systembolaget's page carries none. **Extend this
file; do not start over.** Every run that rediscovers a platform already listed
here has wasted its budget, and budget is the binding constraint.

Regulation (EU) 2021/2117 lets the ingredient list live behind a QR code
instead of on the bottle. The question for every platform is the same: **is the
declaration in the HTML the server returns, or only after JavaScript runs?**

Status as of 2026-08-07, across 51 producers and 140 wine records. **The German
2024-and-later undeclared pool is exhausted** — see the closing section.

## Readable — server-rendered

| Platform | Pattern | Notes |
|---|---|---|
| **Winitas** | `{winery}.winitas-shop.de/elabel/{id}` | German webshop platform, Mosel and Rhine estates. Reach it from `artikel.html?artnr={artnr}`, following the "Nährwertangaben je 100 ml" link. **The elabel id is the shop's internal wine id and cannot be derived from the article number** — read it off the product page. Host serves no `robots.txt` (404). Full mandated set plus a "Übersetzen" selector; use German and say so. |
| **Winestro.cloud** | `nephele-s5.de/?id={id}&lang=DE-DE` and `winestro.info/?s={token}` | **The most productive platform so far — 4 of this run's 5 finds.** Two hosts, one product; both say "Der Wein-Informations-Dienst von Winestro.cloud". Plain HTML, 19-language selector including SV, no `robots.txt` on either host (404). **The page states vintage, wine name, bottle size, alcohol and the bottler itself**, so it can be identified without trusting whatever linked it — the strongest platform for provenance. Linked from Magento (Jülg, anchor "Nährwerte & Zutaten") and Shopify (Thanisch, a "Zutaten" row in the product table whose value is the bare URL). |
| **qrlabelinfo** | `elabel.qrlabelinfo.com/{locale}/{id}.html?lang={n}` | Static HTML on Azure Blob Storage — **no `robots.txt` at all**, the host answers 400 `OutOfRangeInput`, which is Azure's missing-blob error and not a refusal. Ingredients, nutrition per 100 ml, a recycling section, an Impressum, 25-language EU selector. States its own vintage and bottle size in the heading. Found via Schloss Johannisberg. The ids for two wines of one range were two apart; **do not enumerate on that basis**. |
| **f-label (Euvino)** | `p.f-label.eu/{token}` | Server-rendered, 11-language EU selector, and it names the company responsible for the data set. **But its `Name` field is blank and it states no vintage and no alcohol**, so it cannot identify itself; identification rests entirely on the producer's per-article link. Weakest of the readable platforms for provenance, and the token looks article-keyed rather than vintage-keyed — the same trap as IMERO. `robots.txt` is malformed (see below). Found via Vier Jahreszeiten. |
| **weinlabels.de** | `weinlabels.de/php/qr-code-iframe.php?qr_id={id}&firmenId={company}` | Plain server-rendered PHP; the `-iframe` URL 302s to `/php/qr-code.php` with the same query. Full mandated set plus an "Angaben zum Wein" table giving **vintage, grape, quality level, style, alcohol, bottle size, residual sugar, acidity, region, country and the German Amtliche Prüfnummer** — so it identifies itself as well as Winestro does. 24-language EU selector including Svenska. No `robots.txt` (404). **Its `Name` field is a placeholder (`qr_id-2551`), so read the identity off the wine table, not the heading.** Found via Gysler. |
| **Producer's own site** | e.g. `weingut-philipp-kuhn.de/e-labels/{id}` | Some estates host their own. No pattern generalises, but worth a look before assuming a vendor platform. |
| **graphic-druck** | `e-label.graphic-druck.de/{yyyymmdd}/{slug}` | A print supplier's e-label service. The date segment appears to be a publication date and the slug carries the wine and vintage. Found via August Kesseler. Two URL forms: the short `/e/{id}` that producers actually link 302s to the dated slug. |
| **apys** | `elabel.apys.de/e-Label/e-Label.php?p1={company-guid}&p2={article}` | Plain server-rendered PHP by soppe + partner Software GmbH. 24-language EU selector including Svenska; nutrition, ingredient list and a per-company Impressum naming who is responsible for the data set. **It states no wine name, no vintage and no bottle size**, so like f-label it cannot identify itself and a find rests on the producer's linking. `robots.txt` is `Disallow: /` — this is where the e-label exception applies. Seen at Leitz (rejected, see below) and Andreas Oster / HORIZN29 (found). |
| **EuvinoPRO shop** | `iframe.euvino.eu/iframe/{shop-slug}` or a white-label domain like `shop.weingut-knipser.de` | **The declaration is inline on the product page**, not behind a link: a `Zutaten / Inhaltsangaben` row and a `Nährwerte (je 100 ml)` table, beside a Produktinformationen table with grape, Flaschengröße, closure, quality level, region, Einzellage and `Vorhandener Alkohol`. Server-rendered, and it identifies itself — wine and vintage in the H1. Same company as f-label, far better provenance. Three shops in one batch (Max Ferd. Richter, Paulinshof, Knipser) plus one that leaves the fields empty (In den Zehn Morgen). See the traps below. |
| **Producer's page itself** | no platform at all | Bastianshauser Hof – Erbeldinger puts the **complete mandated set inline** on its WooCommerce product page, inside a collapsed accordion whose panel is in the server's HTML: Jahrgang, Alk., Flasche, Bio-Hinweis, `Zutaten:`, `Ø Nährwerte pro 100 ml` and the Gutsabfüller. No link, no iframe, nothing for an href scan to find — only a raw-HTML grep for `Zutaten` finds it. |

## Unreadable — client-side rendering

| Platform | Pattern | Why |
|---|---|---|
| **Scantrust** | `matu.st4.ch/{token}` → `elabel.scantrust.com/default/#/?uid=…&api_key=…` | 828-byte shell, empty `<div id=app>`. **The uid and api_key are in the URL fragment, which is never sent to the server** — that host cannot serve the declaration by construction. The api_key is minted and signed per request, so it is an issued token and absolute under the agent's rules. Do not mine the JS bundles. `matu.st4.ch` answers `Disallow: /`, which is where the robots exception applies. |
| **IMERO** | `s.imero.io/c{id}` | Angular/Ionic SPA. Its catalogue lists per-article e-labels keyed by article number whose first two digits are the vintage, so a wine can be present for one vintage and absent for another — Dönnhoff and Robert Weil both failed this way. |
| **Dropbox folder** | `dropbox.com/scl/fo/…`, one folder per vintage | The folder *view* renders client-side: 309 kB of shell, no file names, and the page's own `&noscript=1` variant is no better. **But the same folder answers `&dl=1` with a zip**, and that is a server response. See *The Dropbox route* below — it is now a resolved find, not a dead end. |
| **devworlds e-label** | Shopware plugin, no public URL | The shop shows a "Zutaten & Nährwerte" **`<button>`, not a link**, opening a modal. All the server returns is a custom field `devworlds_elabel_fields_id` holding an opaque 24-hex id, plus `Allergene: Enthält Sulfite`. No devworlds host is linked anywhere and no e-label route appears in the sitemap, so **there is no URL to hold** and building one from the id would be guessing a pattern. Found via Von Winning. |

## The Dropbox route, which worked

Some estates publish the e-label as a **file on a general file host** instead of
a web page. Recognise it by "Download Center" or "Presse" plus "eLabels" on the
producer's own site. Carl Loewen's page says *"eLabels/Nährwerte & Zutaten des
Jahrgangs 2024 können Sie hier herunterladen"*, where *hier* is a per-vintage
Dropbox shared folder — and per-vintage means the vintage rule is satisfied by
construction, which no other route in this project gives you for free.

The owner widened the robots exception to reach this case on **2026-08-06**, on
the narrow ground that it is still the producer's own act of publishing one
document at a URL the producer itself hands out. It is not a licence on the
host: fetch only the named folder or file, never a sibling, never a guessed
folder id.

What made Loewen readable is worth generalising:

- The default folder view is a client-side shell. So is `&noscript=1`.
- **`&dl=1` on the same folder URL returns a zip, server-side, 200
  `application/zip`.** Same resource, one request, no traversal.
- **What was in the folder was not the declaration but the QR codes** — one PNG
  per wine, named after the wine (`2406 Riesling Alte Reben.png`, where 2406 is
  the vintage-keyed article number). Decode them offline (OpenCV
  `QRCodeDetector`, no network) and you hold a URL the producer published.
  Loewen's pointed at Winitas.
- An estate with **no webshop at all** can still be findable this way.
  `weingut-loewen.winitas-shop.de` exists for nothing else — its 404 body reads
  "Es sind nur Aufrufe des eLabels gestattet. Diese Domain hat keine
  Shopanbindung."

## Where a declaration is not, however much it looks like one

Two producers publish a per-wine, per-vintage PDF datasheet that reads like a
declaration and is not one. **Check before spending a fetch on the next.**

- Von Winning, `content.shop.von-winning.de/expertise-generator/de/weinexpertise/{slug}/{productNumber}`
- Schloss Johannisberg, `schloss-johannisberg.de/app/uploads/{Wine}-{year}-{style}-de.pdf`

A third and a fourth publish the same non-declaration on the web page itself,
one of them under a heading that promises otherwise:

- **Ruppertsberger Weinkeller Hoheburg**, Shopware, a product tab headed
  literally **"Nährwerte & Zutaten" that contains neither**. Under it:
  Abfüller, Gebindegröße, Jahrgang, Alkohol, Restsüße, Gesamtsäure, "Allergene:
  enthält Sulfite". Its `Expertise PDF` at `/expertise/index/article/{id}`
  repeats those fields and adds nothing — and is served at 18 MB for one page
  of text, so fetch it only when it decides the question. **The grep heuristic
  below finds this page and it is a dead end: read what is under the heading,
  not the heading.**
- **Weinland Rheingau eG**, WooCommerce, a wine-data block with Alkoholgehalt,
  Säure, Restzucker, "Allergene: Sulfite" and a full `Nährwertangaben je 100ml`
  — energy, carbohydrate, sugar — and **no `Zutaten` row**. Nutrition without
  an ingredient list is the commonest near-miss.

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
Weines finden Sie hier" (Landerer), a table row labelled "Zutaten" whose
value is a bare URL (Thanisch), "Nährwertangaben" (Wagner-Stempel),
"Informationen zu Zutaten und Nährwerten" (Hauck), and — the shortest and
easiest to miss — a sentence ending "Nährwerte finden Sie **hier**!" where the
one-word anchor is the whole link (Balthasar Ress).

**And sometimes there is no link because there is no e-label**: three shop
systems in the 2026-08-07 batch print the declaration straight into the product
page (EuvinoPRO, the Magento shop at Andres, the Shopware shop at Dr. Koehler).
Grep the raw HTML for `Zutaten` before concluding a shop links nothing.

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
- `elabel.apys.de` answers `User-agent: *` / `Disallow: /` — a blanket disallow
  on a host that exists for nothing but the regulated disclosure. Exception
  territory, and it was used once, for one URL already held.
- Wix estate sites (Steitz) **are server-rendered** and the e-label anchor is in
  the HTML. `weingut-steitz.de/robots.txt` is `Allow: /` bar `*?lightbox=`, and
  its `store-products-sitemap.xml` lists the whole range — a cheap way to see
  which cuvées exist before deciding which page to open.
- `bergkloster.com` is a whole webshop on **one page**, `/de/shop/`, with no
  per-product URLs at all. Nothing to hang an e-label link on. Very small
  natural-wine estates look like this, and their only label-adjacent statement
  is often "enthält keine zugesetzten Sulfite".
- `www.erbeldinger.de` has an expired TLS certificate. Different estate anyway
  — see the name trap below.
- `www.andreas-oster.de` does not resolve; the company is at
  `andreasoster.com` and its Rheinhessen project brand at `horizn29.com`.
- **EuvinoPRO has three traps.** (1) A bare `iframe.euvino.eu/wein/{slug}`
  answers `Fehler 500`; the shop needs a session, so enter through
  `iframe.euvino.eu/iframe/{shop-slug}?redirect=/wein/{slug}`, which is the
  producer's own linking pattern and 302s to the product with an `_ISID`. (2)
  The listing page is client-side templated with `${ product.name }`, but the
  catalogue is embedded as JSON in the same HTML — grep for `"slug":` — and
  `?page=2` is ignored, returning the identical set. **That embedded set is the
  VISIBLE range, not the catalogue**: Knipser's `/sitemaps/products.xml` holds
  62 where the listing embeds 36. On a white-label domain use the sitemap; the
  shared `iframe.euvino.eu` publishes only a 3-URL platform sitemap and cannot
  be enumerated per winery. (3) **The Zutaten and Nährwerte fields are typed in
  by the winery, not generated.** In den Zehn Morgen leaves them empty on every
  product. A Euvino shop is a good bet, not a guarantee.
- **Finding a EuvinoPRO shop from a WordPress estate site**: the `/shop/` page
  contains no product markup at all, only
  `<script src="https://www.euvino.eu/jsc/iframe.js">` followed by
  `initIframe("{shop-slug}", 0)`. One grep for `initIframe` hands you the shop
  slug and therefore the whole catalogue URL.
- `www.knipser.de` answers **403 on every path** and is not the estate's site.
  Weingut Knipser is at `www.weingut-knipser.de`, whose robots.txt is the bare
  line `User-agent: *`. Do not read the 403 as the producer refusing.
- `www.carl-loewen.de` and `carl-loewen.de` fail TLS
  (`TLSV1_ALERT_INTERNAL_ERROR`); the estate is at `weingut-loewen.de`.
- `weingut-hauck.de` has an expired certificate over https, but over plain
  http it redirects to `www.weinhaus-hauck.de`, which is valid — the estate is
  reachable without bypassing the broken TLS. Same trick is worth trying
  wherever a cert has expired.
- `zehnmorgen.de` 301s to `www.st-antony.de`, a different Rheinhessen estate
  whose sitemap contains no Zehn Morgen product. **A redirect is not an
  identity** — the Drathen rule. The live site is `www.indenzehnmorgen.de`.
- `www.weingut-andres.de` redirects to `lilienthal-weine.de`, **a different
  Pfalz Weingut Andres** in the mulled-wine business. The Deidesheim estate
  that makes the Haardt Chardonnay is at `andres-wein.de` /
  `shop.andres-wein.de`.
- `shop.andres-wein.de/sitemap.xml` returns the shop's HTML, not a sitemap, and
  its Magento `robots.txt` disallows `/*?` — use the category `.html` pages.
- `shop.buerklin-wolf.de/robots.txt` is a 1-byte 200, and the estate's main
  `robots.txt` still carries the unedited template line
  `Sitemap: https://www.<livedomain>.de/sitemap.xml`.
- `jjpruem.com` is a 3,7 kB one-page contact card — no wine list, no shop, no
  outbound links. Some famous estates have no searchable surface at all, and
  that is a two-request finding, not a reason to keep looking.
- `keller-wein.de` is the same shape on Wix, and its **`pages-sitemap.xml` lists
  three URLs**: home, Impressum, Datenschutz. There is no
  `store-products-sitemap.xml`. Read the sitemap index before the home page —
  on Wix it settles "does this estate publish products at all" in two requests.
  Reputation predicts nothing: Keller is Gault Millau *Winzer des Jahrzehnts*
  and has a smaller web presence than any co-operative in these batches.
- `emrich-schoenleber.de` served `robots.txt` but answered **HTTP 503 on every
  content URL** across three requests. A generic Apache 503 is an outage, not a
  refusal and not a challenge — record `not_found`, say which, and leave the
  wine as a revisit candidate. `emrich-schoenleber.com` fails TLS with a
  hostname mismatch.
- `shop.wegeler.com` (Shopware 6) has every structural precondition for an
  e-label — per-wine pages, per-vintage SEO URLs `{vintage}-{slug}`, the current
  release on sale — and links none. **Structure does not predict publication.**
  Its `robots.txt` disallows `/detail/` but the SEO URLs are allowed.
- `webshop.solera.se` (Magento 2) disallows `*/catalogsearch/` and `/*?q=`, so
  an importer's B2B catalogue **cannot be searched within its own directives**,
  and the `/produkter` listing returns the category tree without the product
  grid. Its `robots.txt` also names ClaudeBot, GPTBot and a dozen other AI
  agents with `Disallow: /`; we are not any of them, and the `User-agent: *`
  block is what applies.
- `solera.se/robots.txt` answers **200 with the body
  `An error occurred. Error: Error: 404 - Not Found`** — a soft 404 dressed as a
  success. Read the body, not the status.

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
page. f-label and apys do not, and a find there rests on the producer's linking
alone.

**When it does rest on the linking, test the linking.** Leitz was rejected
because two different 2025 wines carried the identical apys `p1`+`p2`. Andreas
Oster was accepted on the same platform because five products carried five
distinct `p2` values under one company `p1`. Four extra product fetches on the
producer's own shop is what separates those two outcomes, and it is the
cheapest identity evidence available on a platform that names no wine.

## Alcohol is not a matching rule, but it is a matching test

The EU labelling tolerance for wine is **0,5 % vol**. Inside it, a discrepancy
between the declaration and Systembolaget is noted and the find stands — Hain
(11,00 against 10,5) and Kesseler are recorded that way. **Outside it, the two
statements cannot describe the same fill.** Sebastian Erbeldinger's own page
declares 13,0 % vol for the 2025 Riesling where Systembolaget says 12,0, and
the estate's whole range is DE-ÖKO certified where Systembolaget's record is
not flagged organic; producer, cuvée, vintage, pack and market all matched and
it was **rejected anyway**. Since a record in this file outranks Systembolaget's
own text, a declaration that contradicts the shelf record on strength is not
one to attach.

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

**Most producers publish nothing reachable.** Across 63 producers probed and
140 wine records, 18 declarations are attached, 31 wines were rejected against
a declaration that was found and read, and 91 came to nothing. Roughly a third
of producers have a readable e-label or an inline declaration; a handful have
an unreadable one; the rest put no ingredient list anywhere this project can
see. The binding constraint is not rendering — it is existence, discoverability
and, in Germany, the vintage.

**The German 2024 slice has now produced a batch with no find at all.** Nine
producers on 2026-08-07 (Max Ferd. Richter, Knipser, Balthasar Ress, Carl
Loewen, Wagner-Stempel, Paulinshof, Andres, Hauck, In den Zehn Morgen,
Bürklin-Wolf), eleven wines, zero attached. **Seven of the ten publish a
complete declaration** — Euvino inline, graphic-druck, Winestro, Magento
inline — and every one of them publishes it for a vintage that is not ours.
That is the whole story of this slice: **discoverability is no longer the
binding constraint in Germany, the vintage is.** The corollary for choosing
work: within a 2024 pool, prefer wines whose producer keeps several vintages on
sale (Hauck's shop holds four other 2024s; Bürklin-Wolf's whole range is the
2022) over wines from estates that keep exactly one page per cuvée.

**And increasingly it is the vintage, not the platform.** In the first
2026-08-06 batch six of nine wines belonged to producers who demonstrably do
publish e-labels, and only one declaration could be recorded. The others failed
because the estate keeps exactly one page per wine, at whatever vintage it is
selling now, and Systembolaget's shelf runs a year behind it. **Prefer wines
whose Systembolaget vintage is 2025 over 2024** when choosing what to probe:
2025 is the current release for most German estates and is the only group where
the producer's own page is likely to still be about our bottle.

**That prediction held.** The 2025-only run that followed it (Steitz,
Erbeldinger, Weinland Rheingau, Andreas Oster, Bergkloster, Ruppertsberger)
found the current release on the producer's page every time the wine existed
there at all, and **not one wine was rejected on vintage** — the first batch
of which that is true. The failures moved elsewhere: to producers who publish
no list (Weinland Rheingau, Ruppertsberger, Bergkloster) and to bottlings that
have no producer page in the first place. **The German 2025 slice is now
exhausted; what remains is 2024, where the vintage rejection returns.**

**The next thing that fails is the bottling, not the vintage.** Three of the
six were export or importer-specific items with no page anywhere on the
producer's site: a cooperative that bottles per destination market
(Ruppertsberger lists a 3 l BiB "Sonderausstattung Finnland" and another for
Rimi, but nothing for Sweden), a Grosslage bottling absent from the
cooperative's whole range (Weinland Rheingau's Rüdesheimer Burgweg), and a
Swedish-market name with no counterpart in the estate's own list (Bergkloster
"Lebendig Frisch"). **A wine that exists only on the Swedish shelf has no
producer page to carry a declaration**, and no amount of searching changes
that. Recognise it early: if the estate's own range does not contain the
cuvée under any name, stop.

**A producer's name in Systembolaget's field can be a brand, a line or a
project, not the legal estate.** Three in one run. "Weingut Sebastian
Erbeldinger" is the son's line at Weingut Bastianshauser Hof – Erbeldinger, and
there is a *different* Erbeldinger estate in the same village at
`weingut-erbeldinger.de` (Inh. Christoph Erbeldinger) — a sister-name trap of
exactly the kind the matching rules forbid walking into. "Andreas Oster
Weinkellerei" sells the Swedish wine under its Rheinhessen project brand
HORIZN29, on a separate domain. "Bergkloster Winery" is Weingut Bergkloster,
Familie Groebe. **Search the wine name as well as the producer name**; the
estate's own domain is often not where the wine is.

**German small estates are where it works.** Hain, Philipp Kuhn, Kesseler,
Jülg, Thanisch, Vier Jahreszeiten, Schloss Johannisberg, Battenfeld Spanier,
Steitz, Andreas Oster, Max Ferd. Richter, Knipser, Paulinshof, Wagner-Stempel,
Hauck and Andres all publish. The
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

**Alcohol earns its keep on the wines the vintage rule lets through.** The one
wine in the 2026-08-07 batch whose vintage matched was rejected on strength and
cuvée: Max Ferd. Richter's 2024 Wehlener Sonnenuhr exists as a Kabinett
*feinherb* at 9,5 % vol where Systembolaget sells the fruity Kabinett at 7,5 %.
On the Mosel, "Kabinett" and "Kabinett feinherb" are two bottlings of one site,
not two names for one wine, and 2,0 pp is four times the tolerance. Without
the alcohol test that would have looked like a plausible attachment.

## When the producer field holds a Swedish importer

Four of the last eight German wines had an importer, not an estate, in
Systembolaget's producer field. **Try the importer's own agency site first**:
some present their growers and name the estate outright.

- **It works when the importer is an agency.** `springwine.se` gives each wine
  a `Producent` field — that is what identified Weingut Mehrlein behind "Even &
  Odd", in two requests. `rewine.se` is a Wix site with both a
  `store-products-sitemap.xml` and one page per producer in
  `pages-sitemap.xml`, so a wine can be ruled out of the whole portfolio in
  three requests.
- **It fails when the importer is a private-label operation.** Solera lists 21
  producers, none of them a Rheingau estate, and its own brands are not tied to
  any of them. Two wines, no estate, no identity test possible.
- **An importer's attribution identifies the estate; it is not a source.** It
  says which producer page to open, and nothing more.
- And identifying the estate is often not enough. Weingut Bernhard Mehrlein
  turned out to be behind two different importers' own labels in one batch, and
  its site says why that leads nowhere: *"Da die Weine für unsere Partner
  exklusiv vinifiziert werden, finden Sie im Weingut meist nicht den gleichen
  Wein."* A house that vinifies per trade partner has no page for the cuvée to
  begin with.

## The German pool is finished, and this is what it came to

**Every German wine with vintage 2024 or later and no declaration on
Systembolaget has now been attempted** — 89 wines across some 60 producers,
recorded in `data/producer-declarations.json`. What remains undeclared in
Germany is 415 wines of 2023 and earlier, where the regulation's production-date
trigger may not even reach and where the producer's current page certainly will
not be about the bottle.

The honest headline for the coverage page: **of the German producers whose
2024+ wines Systembolaget records no declaration for, well under half publish
an ingredient list anywhere a reader can reach, and of those, most publish it
only for a later vintage than the one on the shelf.** The two failure modes are
not the same and the file keeps them apart — a `rejected` record means the
producer complied and the shelf is behind; a `not_found` record means nothing
was reachable, which is not the same as nothing existing.

**Where the remaining work is, if anyone asks for it**: 906 unattempted 2024+
undeclared wines, of which Italy 252 and France 244 are more than half. The one
prior international batch — Antinori, d'Esclans, Wittmann, Sadie, Alheit —
yielded nothing readable, so expect a lower hit rate than Germany's and a
different platform mix (U-label is Italian- and Spanish-heavy and still has no
publicly linked URL in this project's notes).

# E-label platforms, and which of them can be read

What `declaration-finder` has learned about where producers publish the
ingredient declaration when Systembolaget's page carries none. **Extend this
file; do not start over.** Every run that rediscovers a platform already listed
here has wasted its budget, and budget is the binding constraint.

Regulation (EU) 2021/2117 lets the ingredient list live behind a QR code
instead of on the bottle. The question for every platform is the same: **is the
declaration in the HTML the server returns, or only after JavaScript runs?**

Status as of 2026-08-08, across 107 producers and 253 wine records. **The German
2024-and-later undeclared pool is exhausted** — see the closing section. **The
French pool opened on 2026-08-07; forty-five producers and 113 wines in, and
the first (and so far only) French declaration was attached on the fifth French
batch** — see *France, and why it is not Germany* and *The first French find*.
**The Alsace slice is now exhausted too** — see *Alsace, tested to exhaustion*.
The most recent French batch is *The second French inline declaration*, below,
and it names the biggest untried lead in the country.

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
| **Alliance Nutri** | `alliance-alsace.com/01/{gtin}/22/{variant}` | **The project's first GS1 Digital Link** (AI 01 = GTIN, AI 22 = consumer product variant) and its **first third-party e-label vendor on a French producer's page**. About 6 kB of plain server-rendered HTML on a Laravel host: designation, sweetness, **vintage**, format, Gencode, an ingredient paragraph and a nutrition table per 100 ml. 11-language EU selector (fr, en, it, da, de, es, fi, nl, pt, ro, **sv**) driven by a POST with a CSRF token — **but it also honours the `Accept-Language` request header**, which is the cheap way to get French or Swedish. `robots.txt` is `User-agent: *` / `Disallow:` — an *empty* Disallow, everything allowed, no exception needed. **It identifies itself as well as Winestro does.** The bare GS1 root `/01/{gtin}` returns 404, so the variant segment is required and no vintage can be reached without the producer linking it. Found via Cave de Turckheim. |
| **Vincod (vin.co)** | `m.{producer}.{tld}/{code}` and the mirror `vincod.com/{code}`; the e-label is `/{code}/n/{hash}/{lang}` | **The project's only source of a French declaration so far** (Famille Quiot, 2026-08-07) and its most productive French platform. **The `m.rhonea.fr` platform, now identified**: `m.hugel.com` is the same thing, images from `cdn.vin.co`, every short code mirrored at `vincod.com/{code}`, and byte-identical `robots.txt`. Three levels: domaine page → range page → **per-wine, per-vintage page**. The wine page's `<select id="millesime">` **names the short code for every vintage back to 2007**, so our vintage is reachable from the producer's own control and never by guessing — the only platform in this project that gives a vintage archive. The wine page itself is a tasting note plus a Spécifications block (alcohol *analysis*, residual sugar, acidity, pH, vine age, yield) and **is not a declaration**. The declaration, where the producer has filled it in, is a link **"Ingredients & nutrition ›"** to `/{code}/n/{hash}/{lang}`: wine, vintage, **lot number**, *labelled* alcohol, bottle size, an `Ingredients` line and a nutrition table **per 100 ml and per 125 ml**. `robots.txt` is a bad-bot blocklist ending `Disallow: /`, then a separate `User-agent: *` group disallowing only `/ajax`, `/admin`, `/manage`, `/create`, `/superadmin` and `/*/get/{qrcode,tablecard,embed}$` — **the wine and `/n/` pages are allowed, so no exception is needed.** The `/n/` page also states a **Contenance** (`Bouteille (75 cl)`) and the **labelled** alcohol, which is not always the alcohol in the wine page's Spécifications block — that one is the analysis. Match on the `/n/` figure. |
| **Rhonéa's own QR platform** | `m.rhonea.fr/{code}` plus `/{code}/get/tech-sheet` | **This is Vincod — see the row above.** A producer-run QR destination on the producer's own subdomain, server-rendered, **one short code per wine per vintage** with a vintage switcher and a language selector. It states wine, appellation, colour and vintage in its own heading, so it identifies itself as well as Winestro does. On Rhonéa's deployment it carries no declaration: its "Spécifications" block holds residual sugar and "Contient des sulfites" and no ingredient list or nutrition table, and its downloadable fiche produit repeats the same fields. **That observation stands but the reason is now clear — the platform supports a full e-label at `/{code}/n/{hash}/{lang}` and Rhonéa had not filled it in.** On a Vincod page, look for an "Ingredients & nutrition" link inside the Spécifications block before concluding there is none. Its `robots.txt` is a long bad-bot blocklist ending in `Disallow: /`, then a separate `User-agent: *` group disallowing only `/ajax`, `/admin`, `/manage`, `/create` and `/*/get/{qrcode,tablecard,embed}$` — **the wine pages and `/get/tech-sheet` are allowed, so no exception is needed.** |
| **Producer's page itself** | no platform at all | Bastianshauser Hof – Erbeldinger puts the **complete mandated set inline** on its WooCommerce product page, inside a collapsed accordion whose panel is in the server's HTML: Jahrgang, Alk., Flasche, Bio-Hinweis, `Zutaten:`, `Ø Nährwerte pro 100 ml` and the Gutsabfüller. No link, no iframe, nothing for an href scan to find — only a raw-HTML grep for `Zutaten` finds it. |

## Unreadable — client-side rendering

| Platform | Pattern | Why |
|---|---|---|
| **Scantrust** | `matu.st4.ch/{token}` → `elabel.scantrust.com/default/#/?uid=…&api_key=…` | 828-byte shell, empty `<div id=app>`. **The uid and api_key are in the URL fragment, which is never sent to the server** — that host cannot serve the declaration by construction. The api_key is minted and signed per request, so it is an issued token and absolute under the agent's rules. Do not mine the JS bundles. `matu.st4.ch` answers `Disallow: /`, which is where the robots exception applies. |
| **IMERO** | `s.imero.io/c{id}` | Angular/Ionic SPA. Its catalogue lists per-article e-labels keyed by article number whose first two digits are the vintage, so a wine can be present for one vintage and absent for another — Dönnhoff and Robert Weil both failed this way. |
| **Dropbox folder** | `dropbox.com/scl/fo/…`, one folder per vintage | The folder *view* renders client-side: 309 kB of shell, no file names, and the page's own `&noscript=1` variant is no better. **But the same folder answers `&dl=1` with a zip**, and that is a server response. See *The Dropbox route* below — it is now a resolved find, not a dead end. |
| **plugwine** | `{producer-slug}.plugwine.com/{fr,en}/vins/{range}/{cuvée-vintage}/{id}` | **A French wine-shop platform, Angular, and every URL on it returns one BYTE-IDENTICAL 67 kB shell with an empty `<pw-root>`** — listing, product and `sitemap.xml` alike (the sitemap is a soft 404). Recognise it by `<pw-root>`, by a `robots.txt` that carries `crawl-delay: 10`, `Disallow: /fr/*` and the ASP.NET pair `/WebResource.axd` + `/ApplicationError.aspx*`, and by a Cloudflare-managed Content-Signal preamble. **Domaine Roquefeuille's `www.domaineroquefeuille.fr` was this platform white-labelled** — same `<pw-root>`, same robots lines — so the two are one platform, not two producers. The product URL does carry cuvée and vintage, so a *range census* is possible from search results even though no page content is. Seen at Vignoble Hermouet and Domaine Roquefeuille. |
| **Kuupanda** | `commande.kuupanda.com/producteur/{id}/particulier` | A French producer-direct ordering marketplace some estates use *instead of* their own shop (Domaine Fontanel links out to it from its `/boutique/` page). 2 383 bytes of React shell, `You need to enable JavaScript to run this app`, empty `<div id="root">`. `robots.txt` is `User-agent: *` / `Disallow:` — everything allowed and nothing readable. |
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

## France, and why it is not Germany

Seven producers, 28 wines, **zero declarations**, on 2026-08-07: Château du
Galoupet, M. Chapoutier, Gérard Bertrand, Clos Cibonne, Château Revelette,
Saget la Perrière, Château d'Astros. That is not one bad batch — the failures
are all the same failure, and it is a different one from Germany's.

**In Germany the binding constraint was the vintage. In France it is that the
declaration does not exist on the producer's site at all.** Sixteen of the 28
wines had their own producer page, at our exact cuvée, vintage and pack —
Galoupet's two 2025s, Gérard Bertrand's Clairette 2024 and Côte des Roses 2025,
Astros' Amour Blanc and Rouge 2024 — and not one of them carried an ingredient
list. The vintage rule barely got a chance to bite: **not a single French wine
in this batch was rejected**, because nothing was found to reject.

### The French near-miss is the *fiche technique*, and it is more convincing than the German ones

Where a German estate's near-miss was a "Nährwerte" tab with no Zutaten, the
French one is a per-cuvée, often per-vintage, PDF datasheet. It typically gives
appellation, grapes, vinification, food pairing, and sometimes real analysis:

- **Château Revelette**, `ft-coude-a-coude-rose.pdf` — bottling date, alcohol,
  pH, total acidity, residual sugar and **total SO₂ in mg/L**, plus the Ecocert
  number. An SO₂ figure reads like an additive declaration and is not one.
- **Château d'Astros**, `FT_PRINT_Amour_B_2024-FR.pdf` — the vinification line
  reads *"Sulfitage maîtrisé et respectueux"*. Sulphiting in prose is exactly
  the tasting-note mention the rules say not to accept.
- **Gérard Bertrand**, a datasheet per product on the Shopify CDN — presentation
  and tasting notes, and not even a vintage.
- **Clos Cibonne**, a "Fiche Technique pdf" per cuvée that is a **2 MB image
  scan with no extractable text** and no date.

None contains an ingredient list and none contains the energy value. **One PDF
settles the format for a whole estate** — they are generated from one template.
Fetch one, read it, and stop; do not walk seventeen of them on a small server.

### Where the French link actually is

- The estate's **range page**, not a shop, is the hub. Astros links its fiches
  from `/nos-vins/{range}/`, Revelette lists its entire catalogue on one
  `/les-vins/` page.
- **A WordPress "Fiche produit" slug can be a PDF in disguise**: Astros'
  `/ft_print_amour_b_2024-fr/` 302s to
  `/wp-content/uploads/2025/03/FT_PRINT_Amour_B_2024-FR.pdf`. The slug carries
  cuvée, colour and vintage, so **the range page alone tells you which vintages
  the estate still documents, without opening a PDF.**
- **On a hand-built static estate site the per-wine pages can be empty shells.**
  Clos Cibonne's `detail-bouteille.php?vin=1..8` render from a single
  `/js/bouteilles-fr.js` holding the whole range as one JS object — 7,9 kB, one
  request, all eight cuvées, and it has fields for grapes and tasting notes and
  **no ingredient, nutrition, allergen or vintage field at all.** Fetch the data
  file instead of walking the product pages.

### The small-estate hypothesis was tested and failed

The previous run's closing advice was to try **a small French estate with its
own webshop**, the profile that produced most of Germany's finds. Six more
producers on 2026-08-07 — Domaine Denis Père & Fils, Domaine Barraud, Domaines
Bunan, Domaine Vigneau-Chevreau, Domaine Paul Blanck, Les Vignerons de Tavel &
Lirac — plus Rhonéa, 21 wines, **and the one producer that published anything
was the only one that is not a small estate.**

The profile does not transfer, and the shape of the failure says why. In
Germany the small estate's webshop is the *compliance* surface — the e-label
link sits on the product page because the estate treats the shop as the
consumer channel. In France the small estate's site is a *hospitality* surface:
terroir, vinification, food pairings, cellar-door opening hours. Four of these
six do not sell wine online at all.

| Estate | Web presence | Shop | Our vintage on it? |
|---|---|---|---|
| Denis Père & Fils | 3-page Avada WordPress, whole range on one appellations page | none | no vintage stated anywhere |
| Barraud | 11-page static site, `lastmod 2010`, one page per **appellation** | none; the "Acheter" buttons are `href="#"` | no vintage stated anywhere |
| Vigneau-Chevreau | 4 static pages | none | no vintage stated anywhere |
| Bunan | WordPress + own PrestaShop boutique | yes | **yes**, Moulin des Costes Blanc 2024 |
| Paul Blanck | bespoke PHP shop, one page per wine | yes | **yes**, Pinot Noir 2024 |
| Tavel & Lirac | WooCommerce + own Shopify | yes | **yes**, both cuvées 2025 |

**Where a French estate does have a shop, our vintage is usually on it** — the
German vintage problem is much weaker here, and three of these six sold our
exact bottle. The declaration still was not there. Note also that **three of
the six state no vintage anywhere on the site at all**: a page about a cuvée
rather than about a bottling cannot be vintage-matched even if it did carry a
list, so on that profile the search can be abandoned as soon as the range page
turns out to be undated.

**A one-request range census exists on several of these** and is the cheapest
possible probe: Paul Blanck's `/boutique/` lists all 34 products with a
per-product vintage in an `item-date` div; Barraud's and Denis's whole ranges
are single pages; Tavel's Shopify `sitemap_products_1.xml` names 54 products
with the vintage in the slug.

### Rhonéa is the one French producer that publishes, and it is inline

`rhonea.fr` (PrestaShop, the Beaumes-de-Venise / Vacqueyras cooperative group)
puts the **complete mandated set inline on the product page**, in a
`bloc_ingnutri` div in the server's HTML, under a heading `Ingrédients /
Nutrition`: an Ingrédients paragraph and a `Déclaration nutritionnelle` table
per 100 ml. No vendor, no QR, no JavaScript. The two Passe Colline cuvées'
lists differ from each other in their stabilisers — gum arabic and potassium
polyaspartate on the red, citric acid and CMC on the white — so these are
written per wine, not boilerplate.

**And both of our bottles were rejected against it on vintage**, which is the
first time that has happened in France. The shop is one PrestaShop product per
cuvée, edited forward, and it had rolled to the 2025 while the shelf holds the
2024. Meanwhile the producer's *per-vintage* channel, `m.rhonea.fr`, does have
a page for our 2024 — and that page has no ingredient list. **The vintage that
has a per-vintage disclosure has no declaration; the vintage that has a
declaration is not ours.**

The lesson for choosing French work: **a co-op or grower group with a
first-party e-commerce site is a better bet than a small estate**, but the
declaration will be inline on the shop rather than behind a QR code, and a
shop that keeps one product per cuvée will have rolled past a 2024. Prefer
French wines whose Systembolaget vintage is **2025** for the same reason
Germany's 2025 slice worked. Tavel & Lirac was picked to replicate Rhonéa and
did not, so one co-op is not a rule.

### The cooperative hypothesis was tested and failed too

Rhonéa was a co-op, so the next run took the co-op as the profile: **seven
producers on 2026-08-07, twelve wines, zero attached.** Five of the seven are
cooperative-shaped and between them they produced one declaration, a vintage
behind.

| Producer | Shape | Web presence | Our bottle on it? | Declaration? |
|---|---|---|---|---|
| Cave de Turckheim | Alsace co-op | PrestaShop | no, shop is on the 2024, ours is the 2025 | **yes, a full GS1 e-label** — rejected on vintage |
| Pfaffenheim | Alsace co-op | Vinium AJAX site + server-rendered shop | **yes, exactly** — 2024, Riesling/Pinot Gris, 12,5 %, 75 cl | none, not even a sulphite line |
| Cellier des Dauphins | union of Rhône co-ops | 29-page WordPress | no, the brand is absent from the site | none for any wine |
| Les Quatre Tours | Coteaux d'Aix co-op | Nuxt SPA, `serverRendered:false` | no per-wine URL exists at all | unreadable |
| Vignerons Propriétés Associés | 20-estate grower group | WooCommerce | cuvée yes, but **no vintage stated** | none |
| Gustave Lorentz | Alsace house | WordPress + **geoblocked** shop | range pages only, no vintage | none on the readable side |
| Hugel | Alsace house | Vincod | **yes, all three, per vintage** | **yes, two of three** — both rejected on alcohol |

**Neither the big house, nor the small estate, nor the co-op is the French
profile that works.** What actually predicted a declaration in this batch was
not the producer's shape but **whether it had adopted a QR platform at all** —
Turckheim (Alliance Nutri) and Hugel (Vincod) both had, and both published the
complete mandated set; the five that had not published nothing. That is a
better question to ask of the next French producer than how it is owned.

**Alsace is where the platforms are.** Both were found there in one afternoon,
after thirteen producers across Provence, the Rhône, the Loire and Burgundy
turned up none. Alsace is also where the remaining French pool is densest per
producer. Start there.

**But a shared regional platform it is not.** Pfaffenheim, twenty minutes from
Turckheim and the same size, references `alliance-alsace.com` nowhere.

### In France the vintage stopped being the problem and the alcohol started

Four French wines have now been rejected against a declaration that was found
and read. **One was the vintage; three were not.**

- Turckheim's shop is on the **2024** while Systembolaget sells the **2025** —
  the Rhonéa failure mode inverted. A PrestaShop with one product per cuvée can
  be behind the Swedish shelf as easily as ahead of it, so do not assume the
  producer is always the newer of the two.
- **Hugel's Gentil 2024 and Pinot Gris Classic 2024 both have a complete
  e-label for our exact bottle and were rejected on strength**: 12 % vol
  against Systembolaget's 13,0 and 14 % vol against 13,0. Each is 1,0 pp,
  twice the tolerance, **and they are out in opposite directions**, so it is
  not a units or rounding artefact on one side — the two records genuinely
  disagree. Hugel's third Swedish wine, Riesling Classic 2024, is the one whose
  strength agrees exactly (12 against 12,0) and the one whose Vincod page
  carries no e-label link.

That pattern is worth watching. If it recurs — a producer whose per-vintage
disclosure is unimpeachable and whose alcohol simply does not match
Systembolaget's field — the question becomes whether Systembolaget's
`alcohol_percentage` is refreshed per vintage or carried forward with the
product number. **That is a decision about the rule and not one a finder run
should take**; the two Hugel records are flagged as revisit candidates and the
declarations are quoted in full in their `evidence` so no refetch is needed.

**A Vincod e-label is also lot-specific** — it prints `Lot No. : L.CFCN D` —
which is a second, independent reason a strength mismatch is not safe to
wave through: it is a disclosure for one bottling run, and an export
allocation may be another.

**And one house can use one list for everything.** All three Hugel
declarations read are the identical `Grapes, Sulphites , Carboxymethyl
cellulose`, double space and all — a house template. Rhonéa's two cuvées
differed from each other. Per-wine formulation is not something to assume in
either direction.

### Alsace, tested to exhaustion, and it was not a vein

The batch after the cooperative run took the closing advice — *Alsace is where
the platforms are, start there* — and finished the region. **All thirteen
Alsace wines with vintage 2024 or later and no declaration on Systembolaget
have now been attempted, across eight producers, and the two platform
adoptions found in the first afternoon were the whole of it.**

| Producer | Site | Our bottle on it? | Declaration? |
|---|---|---|---|
| Cave de Turckheim | PrestaShop | no, shop on the 2024, ours the 2025 | **Alliance Nutri** — rejected on vintage |
| Hugel | Vincod | yes, all three | **yes, two of three** — rejected on alcohol |
| Pfaffenheim | Vinium | yes, exactly | none |
| Gustave Lorentz | WordPress + geoblocked shop | no | none readable |
| Paul Blanck | bespoke PHP shop | yes | none |
| **Dopff & Irion** | **Vinium** | **yes, exactly** | none |
| **Blanck André et ses Fils** | own shop, one page per cuvée | one control page at our vintage | none |
| **Etienne Simonis** | Soluxa site + per-vintage fiche PDF | **yes, exactly** | none |
| **Vignoble Luc Faller** | **no website at all** | — | — |

**Four of the eight had our exact bottle on their own page and none of them
declared anything on it.** Adoption of a QR platform remains the only thing
that predicted a declaration, and adoption did not spread by geography: two
adopters, six non-adopters, in one small region.

Two things from this half worth carrying forward:

- **Vinium is Pfaffenheim's and Dopff & Irion's, and they are the same owner.**
  Dopff & Irion belongs to the Pfaffenheim group, so that is one observation,
  not two. It does correct the platform note: at Pfaffenheim the
  `/fr/nos_vins/` marketing pages render client-side and only the shop was
  readable, while at Dopff & Irion the marketing URL simply **302s into the
  boutique**, so the whole deployment is server-rendered and its silence is
  real. Recognise Vinium by `Création Vinium` in the footer and a
  `sitemap.php`.
- **A producer can have no website.** Vignoble Luc Faller, Itterswiller, 8,3 ha,
  Demeter — six candidate domains checked by DNS, none resolves; the Vignerons
  Indépendants register (of which the estate is a member) and the official
  Route des Vins d'Alsace directory both carry **no website field**; every page
  a search returns is a retailer or a guide. That is a complete answer in two
  fetches, not a reason to keep looking. **Check the two French directories
  before assuming a small estate's site is merely hard to find** —
  `vigneron-independant.com` and `wineroute.alsace` / `routedesvins.alsace`
  both have a website field and both leave it blank when there is none.

### The first French find, and what Burgundy-avoidance bought

**2026-08-07, five non-Burgundy producers, thirteen wines: one declaration
attached, two rejected against declarations that were found and read, ten not
found.** The batch was chosen to avoid Burgundy deliberately, on the Marc Morey
evidence, and that was right — but the thing that produced the find was not the
region. It was **Vincod again**, on a Rhône house.

| Producer | Region | Site | Our bottle on it? | Declaration? |
|---|---|---|---|---|
| **Famille Quiot** | Rhône / Provence | **Vincod**, `m.famillequiot.com` | yes, all three, per vintage | **yes, all three** — 1 found, 2 rejected |
| Bougrier | Loire | 5-page WordPress | no page for any wine | none |
| Domaine Roquefeuille | Languedoc | Angular SPA | unreadable | unreadable |
| Château de Saint Cosme | Rhône | one PDF booklet | yes, the 2025 CdR | none |
| Ravoire & Fils | Provence | PrestaShop | **yes, both packs at 2025** | none |

**Famille Quiot is the third French Vincod deployment and the first to yield.**
Recognise it exactly as before: `m.{producer}.{tld}`, a CNAME to
`domains.vincod.com`, and the documented `robots.txt` that allows both the wine
page and the `/n/` e-label. The wildcard-DNS check (`randomxyz123.` →
NXDOMAIN) took one command and confirmed the match before a single fetch.

Three things this deployment adds to what Hugel and Rhonéa taught:

- **The `/n/` page's alcohol is the labelled strength; the wine page's
  Spécifications block is the analysis, and they differ.** Trignon Viognier
  2024 reads `13.5 % vol.` on the wine page and `Alc. 13 % vol.` on the
  e-label; Systembolaget says 13,0. **Match against the `/n/` figure.** Had the
  wine page been used, a correct find would have been thrown away.
- **Vincod states the Contenance, and it is a real rejection criterion.**
  Vieux Lazaret Châteauneuf-du-Pape 2024 has a complete, correctly-vintaged
  e-label with a lot number and an exact 14,5 % vol — and says
  `Bouteille (75 cl)` where Systembolaget's item is the magnum. The Gysler
  magnum case, in France. There is no contenance selector; one code, one pack.
- **Quiot's lists are written per wine**, unlike Hugel's house template: the
  Viognier has `Acide tartrique` and `Sulfites`, the Vieux Lazaret rouge adds
  "Peut être" to its protective-atmosphere line, and the Houchart rosé uses
  `Dioxyde de soufre` and no tartaric acid.

#### The new failure mode: two cuvées, one label text

Houchart cost more requests than the rest of the producer put together and
still ended in a rejection, and the reason is worth recognising early next
time. Famille Quiot publishes **two** 2024 e-labels for a *Domaine Houchart
Côtes de Provence rosé* — `Houchart Tradition Rosé` and `Houchart, Les
Cigales, Rosé`. They share grapes, appellation, colour, vintage, 13 % vol,
75 cl and word-for-word identical presentation, terroir, vinification and
tasting text. Their ingredient lists are identical too; only the energy differs
(319 against 318 kJ), which proves they are two disclosures rather than one.

**And neither label prints its cuvée name.** Both read only "Domaine Houchart /
Côtes de Provence / Mis en bouteille au domaine", so Systembolaget's product
name is exactly what either yields and cannot discriminate. Les Cigales is
identified on the bottle by two gold cicadas and nothing else.

The tie-breakers tried, and what each said:

- **Alcohol** — both 13 % vol. Useless.
- **Systembolaget's own product photo** (of the 2022) — a Provençal flute.
  Les Cigales is bottled in that flute; Tradition is in a straight-shouldered
  bottle in both its 2022 and its current packshot. Favours Les Cigales.
- **The Vincod vintage archive** — Les Cigales' selector starts at 2023, so it
  did not exist when that 2022 photo was taken. Favours Tradition.
- **Asset file names** — Les Cigales' ambience photograph is filed as
  `sweden lake with Houchart`. Suggestive, and evidence of nothing.

Recorded as `rejected`, not `not_found`, because a complete declaration was
found and read and it is the *match* that failed. **When a producer's range
holds two undifferentiated bottlings of one appellation, stop early**: the
question is decided by the physical bottle, not by anything on the web.

#### Burgundy-avoidance: right call, wrong reason

Skipping Burgundy did pay, but not because the other regions are richer. Four
of the five non-Burgundy producers failed **in the same way Burgundy does** —
the estate has no per-wine consumer page, or has one and puts nothing on it.
What changed the outcome was one producer having adopted a QR platform. That
remains the only predictor with a track record, and **it is worth spending the
first two commands of every French producer on the DNS check for `m.{domain}`
plus its nonsense-subdomain control**, before any HTTP request at all.

### The DNS probe gives false negatives, and Bargemone is the proof

**2026-08-08, six French producers, fourteen wines, nothing attached.** Vignoble
Hermouet, Domaine Bargemone, Alain Brumont, Château de Chausse, Domaine
Fontanel, Domaine de la Bouvaude.

| Producer | Region | Site | Our bottle on it? | Declaration? |
|---|---|---|---|---|
| Vignoble Hermouet | Bordeaux | WordPress + **plugwine** shop | unreadable | unreadable |
| **Domaine Bargemone** | Provence | WooCommerce + **Vincod** | **yes, exact vintage and strength** | **none — Vincod adopted and left empty** |
| Alain Brumont | Sud-Ouest | Vinium, server-rendered | no, neither brand is on the site | none |
| Château de Chausse | Provence | WooCommerce | **yes, the 2024 white exactly** | none |
| Domaine Fontanel | Roussillon | WordPress + per-vintage fiches | **yes, both, current fiches** | none |
| Domaine de la Bouvaude | Rhône | WooCommerce | **yes, the 2024 red exactly** | none |

**Four of the six had our exact bottle on the producer's own page and not one of
them declared anything on it.** That is now the settled shape of the French
failure.

The finding that changes procedure is Bargemone. **`m.bargemone.com` is
NXDOMAIN and the estate is on Vincod anyway** — its WooCommerce product page
ends *"Consulter la fiche technique : ici"* where *ici* is
`https://vincod.com/G822UF/get/print`, and from that one code the whole
deployment opens up: a domaine hub, eight range pages and a per-wine page for
every cuvée. The two-DNS-lookup probe would have closed this producer as a
non-adopter.

So the probe is still worth its two commands — it costs nothing and a CNAME to
`domains.vincod.com` is still the strongest positive signal in the pool — but
**a negative result no longer closes the question.** The reliable test is
**one grep of one product page for the string `vincod`**, and the anchor text
to expect in France is *"Consulter la fiche technique"*, not anything about
ingredients.

Two more things this batch settles about Vincod:

- **Adopting the platform is not publishing.** Bargemone is the second
  deployment after Rhonéa with the e-label left unfilled, and here it is
  unfilled for the *entire* range: `/n/`, `ingr`, `nutri`, `kcal` and `kJ` are
  all zero matches in the HTML of every wine page checked. What the
  Spécifications block does carry — `SO2 total : 64 mg/L` and `Contient des
  sulfites.` — is an analysis figure and an allergen line, and is the French
  near-miss in its most compact form. Three of six French Vincod deployments
  now publish nothing.
- **The wine page identifies itself well enough to close a wine on its own.**
  Bargemone's 2I7WSF states cuvée, appellation, colour, vintage and
  `Teneur en alcool : 12.5 % vol.`, which matched Systembolaget exactly. The
  page proves the bottling exists and proves the declaration does not.

### Three platforms and one anti-pattern, all new in this batch

- **plugwine** and **Kuupanda** are in the unreadable table above. Between them
  they close two producers on rendering alone, and plugwine retroactively
  explains Domaine Roquefeuille.
- **Vinium can be fully server-rendered.** Alain Brumont's `brumont.fr` is the
  third Vinium deployment in the file and, unlike Pfaffenheim's marketing
  tree, it returns the whole range in the HTML — 373 kB, sixteen wines. So the
  Pfaffenheim note is about a *deployment*, not about the platform: check
  before assuming a Vinium site is client-side. Recognise Vinium by
  `vlwlang` / `data-vlw-mutation` attributes and a `www.vinium.com` footer
  credit.
- **The anti-pattern: a `robots.txt` that welcomes AI agents.**
  `domainefontanel.fr` gives `Allow: /` to thirty-five named agents — ClaudeBot
  and `anthropic-ai` among them — and points at `/llms.txt` and `/facts.json`.
  The `llms.txt` is 6,7 kB of *why to recommend this estate*: awards, page
  prioritisation, trust signals. It contains no product data, and
  `/facts.json` 404s. **An estate optimised for machine readers is not an
  estate that publishes its ingredients**, and this is the clearest evidence
  yet that the absence is editorial rather than technical.

### The fiche technique near-miss, at its most convincing

Domaine Fontanel raises the bar set by Revelette and Astros. Its range page
links **eighteen per-cuvée, per-vintage fiches**, and both of our vintages are
current: `INITIUM-BLANC-2025-Fiche-technique.pdf` uploaded 2026/01 and
`AMAE-2024-Fiche-technique.pdf` uploaded 2026/03. Each states cuvée,
appellation, vintage, grape percentages, yield, certification, vinification,
**`Taux d'alcool`** and **`Contenance`** — every one of them matching
Systembolaget exactly — and then a tasting note, and stops.

**No ingredient list, no nutrition table, no energy value, not even a sulphite
line.** A fiche that satisfies all five matching rules and still is not a
declaration is the strongest form of this trap; when a French estate's range
page links dated PDFs, expect this and budget one fetch, not eighteen.

### Two greps that lie, and one surname that does

- **Strip `<script>` and `<style>` before grepping a big WooCommerce page.**
  Bouvaude's Avada product page is 1,3 MB and matches `ingr` six times,
  `nutri`, `allerg` and `qr` once each — every hit is a Stripe CSS variable
  name or a Font Awesome icon class (`fa-nutritionix`, `fa-allergies`,
  `fa-qrcode`). On the text alone the count is zero.
- **`hermouet.fr` is Hermouet Maçonnerie, a masonry firm in the Vendée.** The
  estate is `vignobleshermouet.com`. The surname trap again, this time across
  industries rather than across villages.
- **A producer's own second brand can be absent from its own website.**
  Brumont's site lists sixteen Montus and Bouscassé cuvées and contains the
  strings *Torus* and *La Gascogne* zero times, although both are his brands
  and both are what Sweden buys. This is the export-brand rule one step
  further in: not a brand that exists only abroad, but a brand the producer
  simply does not put on the web.

### A fourth way a French declaration is not there: the negative list

Etienne Simonis's per-vintage fiche says the wine is made *"sans levurage, sans
collage, sans chaptalisation ni acidification"*, and the vineyard paragraph
says only sulphur, copper and plant teas are used. **A statement of what was
not added is not an ingredient list.** Expect it on organic and biodynamic
estates, where it reads more like compliance than a tasting note does and is
still not one — a wine made without fining agents must still declare its
sulphites, and the energy value is absent either way.

### Where a French declaration is not, three more ways

- **`info-calories-alcool.org`** — a footer logo on Paul Blanck's shop and on
  Rhonéa's QR pages. It is the French drinks industry's generic calorie
  calculator, per drink *category*, and it is not a per-wine declaration. It
  looks like compliance and is not.
- **"Contient des sulfites" plus the pregnancy warning** is the standard French
  product-page boilerplate (Bunan, Rhonéa's QR pages). An allergen statement
  and a health warning, no substances listed, no energy value.
- **A `fiche produit` PDF whose upload path predates the obligation.** Tavel &
  Lirac's is under `/wp-content/uploads/2018/07/`. Read the path before
  spending the fetch — a 2018 file cannot carry a declaration first required of
  wine produced after 8 December 2023.

### French e-label vendors — two are now seen, the rest are not

The 2026-08-07 cooperative run ended the "no third-party vendor in France"
finding. Two are now documented in the readable table above:

- **`vin.co` / Vincod** — `m.{producer}.{tld}/{code}`, mirrored at
  `vincod.com/{code}`, assets on `cdn.vin.co`. Seen at Hugel and, without its
  e-label filled in, at Rhonéa. Server-rendered.
- **Alliance Nutri**, `alliance-alsace.com` — a GS1 Digital Link resolver.
  Seen at Cave de Turckheim. Server-rendered.

**Recognise Vincod by the `m.` subdomain**, which is how both deployments are
reached, and note that Hugel has pointed `hugel.com` itself at its Vincod
domaine page with the path preserved — so a producer's own apex domain can *be*
the QR platform.

Names still worth recognising in an `href` and still unseen: `qrcode.vin`
(which also sells under VINISCAN, VITIQUETTE and VINICODE),
`labelletiquette.fr`, `lesiteduvigneron.fr`, `e-label.eu`, `wine-elabels.eu`,
`littlewine.io`, `scanthiswine.com`, `bottlebooks.me`. `e-label.online` was
already on the German list. Nothing is known about how any of them renders.

### Two French-specific traps

- **A declaration for a French wine often exists on a foreign retailer's page.**
  `vinello.eu` publishes a full ingredient list for La Petite Perrière Sauvignon
  — grape must, grapes, saccharose, acidity regulators, metatartaric acid,
  ascorbic acid, sulphites. **It is not a source and must not be used**: a
  retailer's transcription in another country has worse provenance than
  Systembolaget's and its vintage and market are unverified. Expect to meet this
  more in France than in Germany, because French export brands are on more
  foreign shelves. Note it and move on.
- **The list is in circulation and still may not be used.** Grand Sud
  Chardonnay (Les Grands Chais de France) has a complete, plausible ingredient
  list — grapes, concentrated must, sulphites, potassium sorbate, tartaric and
  malic acid, gum arabic, CMC — on Carrefour, on Openfoodfacts, on a Belgian
  wholesaler's tech sheet and on vinello.eu, and **nowhere on the producer's
  own surface**. It is the vinello rule again and the temptation is stronger
  because the list looks right. It stays out: a record in
  `producer-declarations.json` outranks Systembolaget's own text, so attaching
  an unsourced list overrides a correct absence with an unverifiable presence.
- **The export-only brand.** Saget la Perrière's whole Swedish presence bar one
  wine is *La Petite Perrière*, which appears nowhere on the producer's own site
  — not in the navigation, not in the sitemap. Every page a search finds for it
  is a foreign retailer. This is the German "a wine that exists only on the
  Swedish shelf has no producer page" rule, one size larger: a brand that exists
  only for export.

### Scale predicts nothing, again

Galoupet is an LVMH estate with a dedicated *Plateforme de Transparence*, a
lightweight-bottle explainer and a carbon narrative, and it publishes no
ingredient list. Gérard Bertrand runs a 581-product Shopify catalogue keyed by
cuvée, vintage and format, 212 site pages and 73 metaobjects, and publishes no
ingredient list. **Structure and compliance resources do not predict
publication** — the same lesson Wegeler taught in Germany, at ten times the
size.

### The second French inline declaration, and the best remaining French lead

**2026-08-08, six producers, eleven wines: one declaration found and read, and
rejected on vintage; ten not found.** Pascal Jolivet, François Chidaine, Baron
Philippe de Rothschild, Château des Annibals, Domaine de la Rectorie, Domaines
Paul Mas. The batch was picked to avoid Burgundy and to test the first-party
non-Burgundy estate.

| Producer | Region | Site | Our bottle on it? | Declaration? |
|---|---|---|---|---|
| Pascal Jolivet | Loire / Sancerre | WooCommerce + Beaver Builder | no, both cuvées rolled to the 2025 | none |
| François Chidaine | Loire | WordPress, no shop, per-vintage fiches | no, fiches are the 2023 | none |
| Baron Philippe de Rothschild | Bordeaux / Pays d'Oc | corporate WP + `moutoncadet.com` | **yes, Mouton Cadet Blanc 2024 exactly** | none |
| Château des Annibals | Provence | **Vinium/Sylius, product pages HTTP 500** | no, all rosés are the 2025 | unreadable |
| Domaine de la Rectorie | Roussillon | WooCommerce | no; and the Swedish cuvée does not exist | none |
| **Domaines Paul Mas** | Languedoc | **WooCommerce, `cote-mas.fr`** | no, shop on the 2025 | **yes, complete and inline** — rejected |

**Domaines Paul Mas is Rhonéa's pattern at ten times the size and is the best
untried French lead in the file.** `www.cote-mas.fr` is the group's own shop
for every one of its brands — Côté Mas, Paul Mas, Jean-Claude Mas, Arrogant
Frog, Vignes de Nicole, La Forge Estate, Claude Val, Martinolles, Lauriga,
Astelia — **271 products in one `product-sitemap.xml`**, and the product page
prints the complete mandated set inline in the server's HTML at the end of the
Description tab: an `Ingrédients` paragraph and a `Déclaration nutritionnelle`
table per 100 ml with energy in kJ and kcal. **The lists are written per wine**
(Sauvignon Vermentino: `Raisin,  Sulfites , Carboxymethylcellulose, Mis en
bouteille sous atmosphère protectrice`; Gewurztraminer: `Raisin, Liqueur de
tirage et Liqueur d'expédition,  Sulfites`), so this is not a house template.
No robots.txt exists on the host at all (404), so nothing is disallowed.

Three things about it worth knowing before spending a batch there:

- **The H1 carries the vintage and the SKU confirms it.** `Côté Mas Sauvignon
  Vermentino (75 cl) 2025`, `UGS : PCOT0054|25|CT6` — the `|25|` segment is the
  vintage. That is a strong, cheap identity check.
- **But not every product states a vintage.** The Gewurztraminer's H1 is just
  `Côté Mas Gewurztraminer (75cl)`. A product with no vintage in the H1 and no
  year in the UGS cannot be vintage-matched and should be closed at once.
- **One product per cuvée, edited forward** — the Rhonéa failure exactly. Only
  one Paul Mas wine is in the current 2024+ undeclared pool and it was rejected
  on vintage. **Their other Swedish wines are mostly 2023 or undated**, so the
  yield here will come from a future slice, not this one. Note also that
  Systembolaget already carries declarations for eight Paul Mas wines, so the
  group does supply the data when it supplies it.
- `www.cotemas.com` serves a `robots.txt` but fails TLS with
  `TLSV1_UNRECOGNIZED_NAME` on every content URL; `www.paulmas.com` is the
  marketing site and `www.cote-mas.fr` is the shop. Reach the shop through
  `paulmas.com/les-marques/cote-mas-2/`, whose one outbound product link is a
  per-vintage shop URL.

Four more things this batch settles:

- **A Vinium deployment can be simply broken.** Château des Annibals is the
  fourth Vinium site in the file: its Sylius product pages answer **HTTP 500**
  on `fr_FR` and **404** on `en_US`, and the shop grid is a client-side
  `Loading...`. A 500 is a server error, not a refusal and not a challenge —
  record it as such. The `/sitemap/products.xml` still works and settled the
  vintage question on its own, which is the cheapest possible close.
- **`robots.txt` can name AI agents and no one else.** `www.bpdr.com` gives
  `Disallow: /` to fifteen named tokens — ClaudeBot, GPTBot, OAI-SearchBot,
  CCBot, Google-Extended among them — and has **no `User-agent: *` group at
  all**, so under RFC 9309 an ordinary named crawler matches no group and
  nothing is disallowed. That reading was taken, five pages were fetched, and
  **it is written into the wine's record rather than left implicit**, because
  the file's evident intent and its actual directives differ and the next run
  should decide with its eyes open. This is the mirror image of the Fontanel
  anti-pattern.
- **Two hosts that do not answer at all.** `labaronnie.fr` and
  `www.mouton-cadet.com` (both 193.169.65.167) time out at the TCP level over
  httpx and over `curl -4`. Not a 401, 403 or challenge — a network failure,
  and nothing to work around. The live Mouton Cadet site is `moutoncadet.com`
  **without the hyphen**; the hyphenated domain is a separate dead host.
- **The Beaver Builder false positive.** Pascal Jolivet's WooCommerce pages
  match `elabel` eight times in the raw HTML and zero times in the stripped
  text: every hit is the FLBuilderLayout JavaScript variable `responsiveLabel`.
  Add it to the Stripe/Font Awesome list — **`e-label` and `elabel` are as
  unsafe to grep raw as `ingr` and `nutri`.**

The two Loire estates repeat the settled French shape and add one refinement.
Both keep a per-cuvée page and a linked *fiche technique*, and **the fiche is
the vintage marker**: Jolivet's file names are `…-ft2025-fr-…` and Chidaine's
are `LES-ARGILES-2023.pdf`, so the range page alone tells you which vintage the
estate documents before a single PDF is opened. Neither fiche is a declaration
— Jolivet's states no vintage, no alcohol and no substances at all; Chidaine's
gives residual sugar, total acidity, 13,5 % vol and the bottling month and
still lists nothing. **One fiche settles the template for an estate; do not
fetch the second.**

And one more way the wine simply is not there: **Domaine de la Rectorie has no
Barlande Blanc.** Systembolaget sells one; the estate's Barlande is a Collioure
*rouge* of grenache noir and carignan, and its white-wine category returns
exactly one product. The grapes Systembolaget lists (grenache gris, grenache
blanc) match a *different* cuvée, L'Argile. That is close enough to be
tempting and is a colour mismatch, which is a rejection of the identity, not an
approximation of it.

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
- `www.cotemas.com` answers `robots.txt` but fails TLS with
  `TLSV1_UNRECOGNIZED_NAME` on every content URL. Domaines Paul Mas' live shop
  is `www.cote-mas.fr` and its marketing site is `www.paulmas.com`; neither
  serves a `robots.txt` (both 404).
- `www.mouton-cadet.com` and `labaronnie.fr` (both 193.169.65.167) do not
  complete a TCP connection at all, under httpx or `curl -4`. The live brand
  site is `moutoncadet.com`, **without the hyphen**, on a different address.
- `www.bpdr.com/robots.txt` disallows fifteen *named* AI agents including
  ClaudeBot and has no `User-agent: *` group, so a named project crawler
  matches nothing. See the France section for how that was handled.
- `www.annibals.com` is a Vinium/Sylius shop whose product pages return
  **HTTP 500** while its `/sitemap/products.xml` works normally. Read the
  sitemap first; it can close a producer without a readable product page.
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
- `www.chapoutier.com` serves a **permissive robots.txt and then HTTP 403 with a
  Cloudflare managed challenge on every content URL**, including the sitemaps
  its own robots.txt names. First Cloudflare challenge in this project. A
  challenge is a technological measure and is absolute — two requests, no
  workaround, stop. Chapoutier's Bila-Haut and Marius ranges are both published
  under that host and no alternative domain resolves, so four wines end there.
- `galoupet.com` resolves to 185.16.44.132 but **port 443 is refused**; over
  plain http the same IP 301s to `www.chateaugaloupet.com`, which works. Worth
  trying http before concluding a producer's domain is dead.
- `astros.fr` serves a **self-signed certificate** over https and 301s to
  `www.chateauastros.com` over plain http. `chateaudastros.com` fails TLS with
  `TLSV1_ALERT_INTERNAL_ERROR` and `www.chateau-astros.com` is a different host.
  Same shape as Hauck and Carl Loewen: an expired or broken cert on the obvious
  domain, the live estate one redirect away over http.
- `closcibonne.com` and `clos-cibonne.fr` do not resolve; the estate is
  `www.clos-cibonne.com`, which serves **no robots.txt (404)** and puts an age
  gate in front of a two-locale splash page.
- `saget-laperriere.com` and `lapetiteperriere.com` do not resolve; the house is
  `www.sagetlaperriere.com` / `.fr`, two Magento storefronts publishing the
  **identical 20-URL sitemap with no product pages in it**. A large house can
  have no per-wine page at all.
- `media.sagetlaperriere.fr` is a French "Presse" download site — the Carl
  Loewen Download-Center pattern. **It was checked and has no eLabels**, only
  brochures, portfolios and press photographs, and its file list renders
  client-side. The pattern is worth checking on every French house; it did not
  pay here.
- `www.gerard-bertrand.com` is a Shopify storefront carrying the same
  agent-addressing preamble as `thanisch-vdp-shop.de` (install a shopping skill,
  use the UCP/MCP endpoint). **Page content, not an instruction to us**; the
  real `User-agent: *` directives allow products and were honoured.
  Its `sitemap_metaobject_pages_1.xml` is worth knowing about — Shopify
  metaobjects are the natural place for per-wine e-labels, and reading that one
  file rules the whole idea in or out in a single request.
- `www.domainebarraud.com` serves **no `robots.txt` (404)** and a sitemap whose
  every `lastmod` is `2010-01-01`. The estate's only outbound sales link, to the
  vigneron marketplace `restonsenvigne.fr`, **404s** — a producer's own buy link
  can be dead, and that is the end of the trail rather than a reason to work the
  marketplace (a marketplace is a retailer and not a source, like `vinello.eu`).
- `www.blanck.com` answers **HTTP 404 with its own styled 404 page** for
  `robots.txt` and for any sitemap name, so there are no directives at all.
- `bunan.com/robots.txt` is 29 bytes and its only group is
  `User-agent: Scrapy` / `Allow: /`. There is no `User-agent: *` group, so
  nothing is disallowed — an unusual file that is easy to misread as restrictive.
- `bunan.com/fr/` **404s while serving the full site chrome**, so the nav and
  the range links are readable off the error page. The estate's per-wine URLs
  `/nos_vins/{slug}` are empty Essential Grid placeholders; the actual wine text
  lives on the single range page.
- `cave-tavel-lirac.fr/robots.txt` names ClaudeBot, GPTBot, CCBot, Bytespider,
  Amazonbot, Google-Extended and meta-externalagent with `Disallow: /`, and
  carries a **Content-Signal** line (`search=yes,ai-train=no,use=reference`).
  We are none of the named agents, our User-Agent is the project's own, and the
  `User-agent: *` group is what applies — the same reading already used at
  `webshop.solera.se`.
- `rhonea.fr` and `www.rhonea.fr` are **two hostnames serving the same
  PrestaShop with no redirect between them**. Read `robots.txt` on whichever you
  actually fetch from; both are the stock PrestaShop file.
- `boutique.gustavelorentz.com` answers **HTTP 403 with the body "This website
  is only authorised from France and Germany"** — on every path including
  `robots.txt`. **The first geoblock in this project.** It is a technological
  measure and therefore absolute: one request, no workaround, record
  `not_found` and keep the product slugs so a future run from an eligible
  country can go straight to them. It says nothing about whether the producer
  publishes; it does say a Swedish reader holding the bottle cannot get there
  either. The estate's marketing site `www.gustavelorentz.com` is open and
  server-rendered, keeps **range pages rather than per-wine pages**, states no
  vintage, and carries no list.
- `www.cave-turckheim.com` serves **no `robots.txt`** — it answers 404 with the
  site's own styled error page. Its PrestaShop puts the e-label link in a
  button labelled **"INGREDIENTS ET NUTRITION"** at the foot of the technical
  block on every product page, after "Contient des sulfites".
- `www.pfaffenheim.com` runs the **Vinium** framework and is two sites in one:
  the `/fr/nos_vins/{id}/{slug}/{vintage}` marketing pages **render
  client-side** (30 kB of chrome, the wine only in the `<title>`, and an
  `X-Requested-With: XMLHttpRequest` refetch returns the identical shell),
  while `/fr/boutique` and `/fr/produit/{gtin}-{slug}` are **fully
  server-rendered**. On this platform the shop is the readable surface.
  Its `sitemap.php` keeps **one marketing page per vintage** per cuvée.
- `quatretours.com` is a Nuxt SPA whose inline state reads literally
  `serverRendered:false`; its `robots.txt` is a 200 serving the SPA shell, a
  soft 404 like `solera.se`'s. **Its `sitemap.xml` is 29 static pages in two
  locales with no per-wine URL at all**, which settles the producer in two
  requests without fighting the rendering. `les4tours.com` does not resolve.
- `hugel.com` and `www.hugel.com` **refuse port 443**; over plain http both
  redirect, path preserved, to `m.hugel.com/598DGMB3C4` — the producer's Vincod
  domaine page. `hugel.fr` is a frameset whose only content is an
  `<iframe src="http://www.hugel.com/fr">`.
- `vigneronsproprietesassocies.fr/robots.txt` (Netalys WordPress) names
  **ClaudeBot and anthropic-ai** as well as GPTBot, CCBot, Google-Extended and
  the usual SEO crawlers with `Disallow: /`. We are none of them — the
  User-Agent is the project's own — and the `User-agent: *` group, which allows
  `/produit/`, is what applies. Same reading as `webshop.solera.se`,
  `cave-tavel-lirac.fr` and `www.gerard-bertrand.com`.
- **`unable to get local issuer certificate` is now usually OUR fault, not the
  site's.** `www.groupegcf.fr` and `www.groupegcf.com` fail TLS under httpx,
  curl and a freshly installed `certifi` — and the chain is perfectly valid:
  `openssl s_client` shows a Let's Encrypt leaf under intermediate `YR2` under
  **`ISRG Root YR`**, Let's Encrypt's 2025 root, which neither the Pi's
  `ca-certificates` nor certifi carries yet. **Do not record this as a TLS
  failure and do not disable verification.** Fetch Let's Encrypt's own
  cross-signed root, `https://letsencrypt.org/certs/gen-y/root-yr-by-x1.pem`,
  which verifies under the already-trusted ISRG Root X1, append it to a copy of
  the CA bundle and pass that as the `cafile`. Verification still happens.
  Let's Encrypt is rotating to this root, so **expect this on more and more
  hosts over the coming year**; a self-signed or expired certificate is a
  different thing and stays a real failure.
- `www.gcfplanet.com` fails TLS with a genuinely self-signed chain; over plain
  http it is a 134-byte meta-refresh to `https://www.groupegcf.fr`. The group's
  `robots.txt` **disallows four specific content pages**, among them
  `/nos-marques/decouvrez-nos-marques.html`, the brands index — honoured in
  full, this being an ordinary corporate site. The per-brand pages the sitemap
  lists are allowed and are where the brand links live.
- `www.grandsud-wines.com` serves a self-signed certificate on 443, so **http is
  what the producer's own page links** and http is what to use. The site is
  WordPress with sitepress 2.4.3 and a joliprint button, and its own metadata
  dates it **12 June 2012**; every URL redirects to a JS country-and-age gate.
  A brand site a decade older than the obligation is a two-request finding.
- `m.grandsud.fr` resolves — and so does `randomxyz123.grandsud.fr`. **Wildcard
  DNS will fake the Vincod `m.` pattern.** Probe a nonsense subdomain before
  believing an `m.` host means anything.
- `www.dopff-irion.com/robots.txt` disallows the `/de/ /es/ /it/ /cn/ /jp/
  /dk/ /co/` language trees but allows `/fr/` and `/en/`, and names
  `sitemap.php`. Its `/fr/les-vins/{id}/{slug}` pages **302 into
  `/fr/boutique/{16-digit-id}/{slug}`** — one page, two URLs.
- `www.andreblanck.com` is Domaine **André** Blanck, Kientzheim; `www.blanck.com`
  is Domaine **Paul** Blanck, the same village. Two estates, one surname.
- `www.vins-simonis.fr` serves **no robots.txt** (404 as its own styled page).
  Its Soluxa-built `?pdf` endpoint returns a **malformed PDF** — five bytes of
  leading whitespace before `%PDF` and no `%%EOF` — so pypdf refuses it until
  the prefix is stripped and `%%EOF` appended, and it truncates over HTTP/2
  (curl exit 92) where `--http1.1` returns the whole file. A broken generator,
  not a protected document. The fiche's own footer prints
  `www.domaine-simonis.fr`, **which does not resolve**.
- `vins-faller.fr` is **Domaine André Faller, 2 route du Vin, Itterswiller** —
  not Vignoble Luc Faller, 51 route des Vins, the same village. Same surname,
  same village, different street, different estate, and the wrong one has the
  webshop.
- `domaine-marc-morey.com` is a **Gandi parking page** with 443 refused;
  the estate is `domaine-marc-morey.fr`, whose `robots.txt` is a bare
  `User-agent: *` with no directives and whose **sitemap is seventeen URLs with
  no wine among them** — the range is organised by colour, grape and
  appellation. Six wines closed in five requests.
- `m.famillequiot.com` is a **CNAME to `domains.vincod.com`** and
  `randomxyz123.famillequiot.com` is NXDOMAIN, so this one is genuine and not
  the `m.grandsud.fr` wildcard trap. **Run both DNS lookups before any fetch**;
  together they cost nothing and settle whether the producer is on Vincod.
- `bougrier.fr` and `www.bougrier.fr` **reset the connection on port 443**;
  over plain http they 301 to `famille-bougrier.fr`, whose certificate is for a
  different hostname, so **the site is only reachable over http**. Its
  `wp-sitemap-posts-page-1.xml` is five URLs and there is no product post type;
  its "Nos Vins" menu item is an in-page anchor showing seven range names as
  unclickable images. A large Loire négociant can have no wine on its website.
- `www.roquefeuille.fr` **refuses port 443**; over http it 301s to
  `www.domaineroquefeuille.fr`, an **Angular SPA** whose every URL returns the
  identical 67 kB shell with an empty `<pw-root>` and whose `/sitemap.xml` is a
  soft 404 serving that shell. The backend is ASP.NET — recognise it by a
  `robots.txt` that disallows `/WebResource.axd` and `/ApplicationError.aspx*`
  and carries `crawl-delay: 10`. Nothing is server-rendered; this is the
  `quatretours.com` failure mode on a second French platform.
- `www.saintcosme.com` **is one page and four PDF links** — a logo, "Est. 1570",
  and the estate's annual *Livret*. `robots.txt` is 30 bytes (`User-agent: *`,
  `Crawl-delay: 10`, no Disallow) and there is no sitemap. The 2026 booklet is
  19,6 MB and 48 pages; it was fetched once because it *is* the producer's
  surface, and it contains no ingredient list and no nutrition table.
  **It does reproduce the labels**, and their extracted text reads
  `RED RHONE WINE - PRODUCT OF FRANCE - CONTAINS SULFITES` — an allergen line on
  a picture of a label is not a declaration.
- `www.ravoire.fr` fails TLS with `unable to get local issuer certificate` and
  **this one is the site's fault, not ours**: the server sends the leaf alone
  and omits the Sectigo OV R36 intermediate. Distinguish it from the ISRG Root
  YR case with `openssl s_client` — if the chain shows only one certificate,
  fetch the issuer named in the leaf's **AIA `CA Issuers` URI**, convert DER to
  PEM and append it to the bundle. Verification still happens.
  `ravoire.fr/robots.txt` is a **soft 404 serving the home page**.
- `manon.fr` is a wine brand's own site whose eight **`Ingrédients` headings are
  cooking recipes** in a food-pairing section. A raw-HTML grep for `ingr` on a
  French brand site will find these; read what follows the heading.
- `hermouet.fr` is **Hermouet Maçonnerie**, a masonry company in Chauché,
  Vendée. Vignoble Hermouet is `www.vignobleshermouet.com`, whose `robots.txt`
  and every sitemap name answer 404 as the site's own styled WordPress error
  page. Its two fiches techniques are under `/wp-content/uploads/2017/11/` and
  `/2018/02/` — read the upload path and do not spend the fetch.
- `vignobles-hermouet.plugwine.com/robots.txt` has **two `User-agent: *`
  groups**: Cloudflare's managed block (`Allow: /`, `Content-Signal:
  search=yes,ai-train=no,use=reference`) and the site's own
  (`crawl-delay: 10`, `Disallow: /fr/*` and the ASP.NET paths). Merge them as
  RFC 9309 requires — `/en/vins` is allowed, `/fr/` is not — and honour the
  ten-second delay.
- `m.bargemone.com` is **NXDOMAIN and the estate is on Vincod regardless**; the
  link is `https://vincod.com/G822UF/get/print` on its own WooCommerce product
  page, under the words "Consulter la fiche technique". See *The DNS probe
  gives false negatives*.
- `brumont.com` **refuses port 443**, and `m.brumont.com` resolves — as does
  `randomxyz.brumont.com`, to the same address. **Wildcard DNS**, the
  `m.grandsud.fr` trap, second sighting. `www.brumont.fr/robots.txt` and
  `/sitemap.xml` are both **soft 404s serving the site's own 322 kB error
  page**.
- `chateaudechausse.com` fails TLS with a **hostname mismatch** and over plain
  http serves OVHcloud's *"Site non installé"* parking page; the estate is
  `chateaudechausse.fr`. Its Yoast sitemap index has **no product sitemap at
  all** although the site runs WooCommerce — the product URLs are only on
  `/nos-vins/`. A `documentation-sitemap.xml` exists and looked like the Carl
  Loewen download-centre pattern; it holds one URL, the empty archive page.
- `www.domainefontanel.com` fails TLS with `TLSV1_ALERT_INTERNAL_ERROR` and over
  plain http 301s to `domainefontanel.fr`, which is valid — the Hauck and Carl
  Loewen shape again. The `.fr` `robots.txt` **allows thirty-five named AI
  agents** and names `/llms.txt` (a marketing brief) and `/facts.json` (404).
- `www.bouvaude.com` is the estate for Domaine de la Bouvaude; every obvious
  alternative (`labouvaude.com`, `domainedelabouvaude.com`, `bouvaude.fr`,
  `labouvaude.fr`, `domaine-bouvaude.fr`) is NXDOMAIN.
- `rhonea.fr/fr/{category-slug}/` **404s**; its categories are
  `/fr/{id}-{slug}` (e.g. `/fr/15-ventoux`) while its products are
  `/fr/{slug}/{id}-{slug}.html`. Fetch the category to get the product URLs
  rather than assembling them.

## Don't trust a slug, or a shop's own vintage field

Three producers in one batch disagreed with themselves about the vintage.

- **Bunan (PrestaShop).** The same trap on a different platform, and worse:
  `…/12-bandol-moulin-des-costes-blanc-2019.html` serves an H1 of **`MOULIN DES
  COSTES BLANC 2024`** and `…/3-20-…-blanc-2021.html` serves **`CHATEAU LA
  ROUVIERE BLANC 2025`**. Even the `<title>` is stale where the H1 is current.
  Reading the slug would have given the wrong vintage for both wines.
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

**Most producers publish nothing reachable.** Across 107 producers probed and
253 wine records, 19 declarations are attached, 39 wines were rejected against
a declaration that was found and read, and 195 came to nothing. Roughly a third
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

**Where the remaining work is, if anyone asks for it**: 844 unattempted 2024+
undeclared wines, of which Italy 252 and France 183 are more than half, then
Spain 79, South Africa 59, Austria 42 and Portugal 39. The one
prior international batch — Antinori, d'Esclans, Wittmann, Sadie, Alheit —
yielded nothing readable, so expect a lower hit rate than Germany's and a
different platform mix (U-label is Italian- and Spanish-heavy and still has no
publicly linked URL in this project's notes).

**France now stands at 102 wines across 39 producers, 1 found, 7 rejected**, and
**148 French 2024+ undeclared wines remain untouched**. Germany's rate across
its whole pool was 18 in 89; France's is 1 in 102.

Four of the thirty-nine publish an ingredient list somewhere a reader can reach
— Rhonéa inline on its shop, Cave de Turckheim on Alliance Nutri, Hugel on
Vincod, Famille Quiot on Vincod — and of the eight wines they cover, one was
attached and seven were rejected: two on vintage, two on alcohol, one on pack,
one because the shop had not rolled forward, and one because two of the
producer's own cuvées could not be told apart. **The French failure has moved
twice.** For the first thirteen producers nothing existed to reject; then
something did, and the matching rules stopped it; now one has finally survived
them.

**Shape does not predict publication in France; platform adoption does.**
Big house, small estate, cooperative and Loire négociant have each been tried
as a profile and each has failed. What the four publishing producers have in
common is that they run a QR platform at all. The cheap questions to ask of a
French producer, in order:

1. ~~**Is it in Alsace?**~~ **Withdrawn 2026-08-07.** It was the right place to
   look and it has been looked at: the region is finished, eight producers,
   and the two adopters were found in the first afternoon. Geography did not
   predict a second wave.
2. **Is `m.{domain}` a real host?** Two DNS lookups — `m.{domain}` and a
   nonsense subdomain as the wildcard control — and **not a single HTTP
   request**. A CNAME to `domains.vincod.com` is the strongest positive signal
   in the French pool: three of the four publishing producers are on Vincod and
   it is the source of the only attached French declaration. Do this first,
   always — but **a negative does not close the question.** Bargemone is on
   Vincod with no `m.` host at all (2026-08-08), and Brumont's `m.` host is
   wildcard DNS pretending to be one. The probe is cheap and one-directional.
3. **Does any product page contain the string `vincod` or an
   `alliance-alsace.com` GS1 URL?** One grep of one product page settles the
   rest, and this is what the DNS probe cannot do. In France the anchor is
   usually *"Consulter la fiche technique"*, not anything about ingredients —
   grep for the platform name, not for the word.
4. **Does the range page state a vintage?** If not, stop — an undated cuvée
   page cannot be matched to a bottling however much text it carries. Six
   French producers have now failed on this alone.
5. **Does a sitemap exist, and does it contain a wine?** Cheapest HTTP probe in
   the file. Marc Morey's seventeen URLs closed six wines, Les Quatre Tours'
   twenty-nine closed a producer, Bougrier's five closed three wines.
   **Read the sitemap before the home page.**

**Where the remaining French work is**, by cluster size, all vintage 2024+ and
undeclared, after the 2026-08-08 batch: Domaine Fontaine-Gagnard 5, Clotilde
Davenne 3, Chartron et Trébuchet 3, then pairs — François Chidaine, Domaine de
la Rectorie, Pascal Jolivet, François Mikulski, Domaine Cruchandeau, Georges
Duboeuf, Baron Philippe de Rothschild, Chai Berteaud Manceau, Domaine de Terres
Blanches, Mommessin, Chateau des Annibals, Les Sablonnettes, Henri Boillot,
Jean-Paul & Benoît Droin — and a long tail of ones.
Burgundy is around 60 of the 148 and, on the Marc Morey evidence, is the
weakest region yet — its estates sell through allocation and have no reason to
keep a consumer-facing product page at all. **Of the non-Burgundy pairs,
Pascal Jolivet is the most promising untried profile** — a Sancerre house of
real size with a first-party site, the shape that has not yet been eliminated.

Prefer wines whose Systembolaget vintage is **2025** over 2024, with one
correction: **the French shop is not reliably ahead of the Swedish shelf.**
Rhonéa's had rolled past our 2024; Turckheim's had not yet reached our 2025.
Both directions cost a wine in this pool.

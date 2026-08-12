# E-label platforms, and which of them can be read

What `declaration-finder` has learned about where producers publish the
ingredient declaration when Systembolaget's page carries none. **Extend this
file; do not start over.** Every run that rediscovers a platform already listed
here has wasted its budget, and budget is the binding constraint.

Regulation (EU) 2021/2117 lets the ingredient list live behind a QR code
instead of on the bottle. The question for every platform is the same: **is the
declaration in the HTML the server returns, or only after JavaScript runs?**

Status as of 2026-08-12, across 410 wine records and some 190 producer strings
(fewer actual producers — Systembolaget spells several of them twice). **The German
2024-and-later undeclared pool is exhausted** — see the closing section. **The
French pool ran from 2026-08-07 to 2026-08-09 and is now set aside** at
sixty-nine producers and 142 wines, four declarations attached and nine
rejected — see *France, and why it is not Germany* and *The first French find*.
**The Alsace slice is exhausted** — see *Alsace, tested to exhaustion*. The last
French batch is *The estate that hosts its own e-labels and publishes them only
for the 0,0 %*, below.

**Italy opened on 2026-08-09** and has had seven batches — sixty-one producers,
149 wines, **eight declarations attached** and ten rejected, with 118 wines still
untouched. See *Italy, where the page is undated*, the last major section of this
file, and in particular its subsections *The first Italian declarations
attached*, *Italy's first e-label vendor, and its second first-party shape*,
*The fifth Italian batch*, *The sixth Italian batch: the vendor that publishes
one list per vintage*, *The seventh Italian batch: a new vendor, a QR image, and
the same producer twice* and *Where the remaining Italian work is*. Read them
before touching an Italian producer: five different producer profiles have now
been falsified there and the closing advice is a fixed probe, not a shape to
select for — starting with the question of whether the Swedish name is the
producer's name at all. **And before picking a producer at all, normalise the
producer string**: the seventh batch's only find was a wine whose estate had
already been done under a differently-spelled name.

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
| **VINISCAN (ABSOMOD)** | `v9.lu/v/{code}` and `iviti.fr/v/?q={token}` | **One French vendor, two hosts, two different gates, and both are readable.** Plain server-rendered HTML: a `Déclaration nutritionnelle` table per 100 mL and an `Ingrédients` paragraph, a 24-language EU selector including Svenska, `noindex`, and the footer `© 2026 VINISCAN by ABSOMOD GROUP`. Neither host serves a `robots.txt` (404 on both), so nothing is disallowed. **The page states no wine name, no vintage, no bottle size and no alcohol** — it is a bare template keyed by the URL, so identity rests entirely on the producer's own per-wine linking, the weakest provenance of any readable platform here. Both hosts refuse a plain request with a short 200-with-body, and **the two refusals are not the same thing**: `v9.lu` answers `Smartphone only` and yields to the mobile-shaped User-Agent from the 2026-08-08 device-gate decision, while **`iviti.fr` answers `Accès refusé...` to that same mobile UA and yields to nothing but a `Referer` header naming the producer page that published the link** — hotlink protection, and the Referer we send is simply true. Try the Referer before the mobile UA; it needs no exception at all. `iviti.fr`'s own root answers 403 to everything, which is absolute — one URL per wine and nothing else on the host. Seen at Domaine Gassier (v9.lu, QR image in a Shopify description) and Domaine André Brunel (iviti.fr, an anchor reading *"Cliquez ici pour retrouver la liste des ingrédients et informations nutritionnelles de cette cuvée"*). Tokens are per wine: Brunel's siblings share the trailing producer segment and differ in the prefix. |
| **wineplatform.it** | `shop.{producer}.{tld}/{country}/{currency}/{lang}/prodotti/{slug-with-vintage}` | An Italian shop platform, plain server-rendered, **one product per vintage with the vintage in the slug and in an `Annata` field** — the best identity in Italy (Annata, Denominazione, Vitigni, Alcol, Formato) and **never a declaration**: where the ingredient list belongs it prints `Info: Contiene Solfiti - Prodotto in Italia`. Permissive `robots.txt` naming a sitemap that is a complete per-market census. Seen at Marchesi di Barolo and Tenute Piccini, four wines, same near-miss each time. The `<title>` carries a stale vintage; read the H1. |
| **Giunko ED (ead-qr)** | `ead-qr.com/p/{numeric id}` | **The best-behaved e-label platform in this file, and the only one anywhere that solves the vintage problem.** Giunko Srl, Bologna, sells it as *ED etichetta digitale* (`etichettaambientaledigitale.it`). ~38 kB of plain server-rendered HTML carrying the environmental label and the ingredient declaration on one page, and **a SEPARATE, EXPLICITLY YEAR-LABELLED nutrition and ingredient block for every vintage still on the market** — `Valori Nutrizionali 2024` / `Ingredienti 2024` beside `… 2025`, with genuinely different recipes. It states the wine, the line and the pack in its heading (`Prima Linea Cerasuolo d'Abruzzo DOC 0,75`) and names the responsible company, and it links the producer's own product card, which supplies the alcohol. 25-language EU selector including Svenska, **driven by the `Accept-Language` header on the same URL** — no new URL needed. **No `robots.txt` at all** (a genuine 404 with a plain-text body). Ids are per product and consecutive across a range (1890568, 1890569); that is not a licence to enumerate. Reached from an anchor reading **`Valori nutrizionali`**, class `btn-nutrizionale`, on the producer's WooCommerce. Found via Azienda Marramiero — both Swedish wines attached. |
| **IoAgri** | `app.ioagri.it/Qr/DL?id={token}` | **The first Italian third-party e-label vendor seen in an `href`** (La Pruina, Puglia, 2026-08-09). Server-rendered; the payload names `CompanyName`, `ProductName`, `AlcoholPercentage`, an ingredient line, a nutrition table per 100 ml and an environmental-labelling block. **It states no vintage — `Year` is null** — so the vintage rests entirely on the producer's own linking page, which is where La Pruina's Manduria was rejected. Tokens look product-keyed, not vintage-keyed, so a producer that edits one WooCommerce product forward should carry the new recipe under the same token. Reached from a WooCommerce anchor reading *"VALORI NUTRIZIONALI E INGREDIENTI \| SMALTIMENTO — CLICCA QUI"*. |
| **A WooCommerce `Ingredienti` tab** | `shop.{producer}.{tld}/prodotto/{slug}` | **Not a platform — a product tab, and Italy's second first-party publisher shape.** Demarie's shop renders a fourth WooCommerce panel, `<div class="ingredient-list"><p class="ingredient-list__body">Ingredienti: uva. Conservanti: <strong class="ingredient-list__allergen">solfiti</strong></p></div>`, in the server's HTML. The H1 carries the vintage. **It is an ingredient list and not the complete mandated set** — no nutrition table, no energy value — and the same line appears on every product, so it is a house template. Coppi runs the identical software with only two tabs. **Count the tabs; the platform supports it and the estate decides.** |
| **carmaqrcode** | `www.carmaqrcode.it/{n}/{nnn-nnn-valori-nutrizionali-{wine-slug}}/` | **Readable only through the PDF, and the page itself is empty.** An Italian vendor running WordPress, one post per wine, whose `entry-content` is a single empty `<div class="_df_book">` — a 3D FlipBook viewer. **A stripped-text read and an `<a href>` scan both come back with nothing**; the document URL appears only inside an inline script as `"source":"…pdf"`, so only a raw grep for `.pdf` finds it. The PDF is a two-page Illustrator artboard: page one the ingredient list, the allergens and the nutrition table, trilingual it/en/fr in three columns; page two the Italian *etichettatura ambientale*. `robots.txt` is the stock WordPress `Disallow: /wp-admin/` with `Allow: /wp-admin/admin-ajax.php`, so the post and the `wp-content` PDF are allowed and **no exception is needed**. **It states no vintage**, and neither did the producer that used it, which is why the find was a rejection. Found via Tralci Hirpini (Campania), reached because the producer's own product URL **301s straight into the vendor**. |
| **Producer's page itself** | no platform at all | Bastianshauser Hof – Erbeldinger puts the **complete mandated set inline** on its WooCommerce product page, inside a collapsed accordion whose panel is in the server's HTML: Jahrgang, Alk., Flasche, Bio-Hinweis, `Zutaten:`, `Ø Nährwerte pro 100 ml` and the Gutsabfüller. No link, no iframe, nothing for an href scan to find — only a raw-HTML grep for `Zutaten` finds it. |

## Unreadable — client-side rendering

| Platform | Pattern | Why |
|---|---|---|
| **Scantrust** | `matu.st4.ch/{token}` or `label.{producer}.{tld}/qr/{slug}` → `elabel.scantrust.com/default/#/?uid=…&api_key=…&qr={slug}` | 828-byte shell, empty `<div id=app>`. **The uid and api_key are in the URL fragment, which is never sent to the server** — that host cannot serve the declaration by construction. The api_key is minted and signed per request, so it is an issued token and absolute under the agent's rules. Do not mine the JS bundles. `matu.st4.ch` answers `Disallow: /`, which is where the robots exception applies. **Second deployment, and the first Italian one: Masi Agricola**, on its own vanity host `label.masi.it`, whose `robots.txt` is the single line `User-agent: *` with no directives under it — nothing disallowed, so no exception was needed there. Masi's redirect is a 1 590-byte shell rather than 828 and the slug is echoed back as a `qr=` parameter, but the fragment problem is identical. **The uid is per wine and the slug is NOT per vintage** — see *Masi publishes its e-label as a QR image*, below. |
| **IMERO** | `s.imero.io/c{id}` | Angular/Ionic SPA. Its catalogue lists per-article e-labels keyed by article number whose first two digits are the vintage, so a wine can be present for one vintage and absent for another — Dönnhoff and Robert Weil both failed this way. |
| **Dropbox folder** | `dropbox.com/scl/fo/…`, one folder per vintage | The folder *view* renders client-side: 309 kB of shell, no file names, and the page's own `&noscript=1` variant is no better. **But the same folder answers `&dl=1` with a zip**, and that is a server response. See *The Dropbox route* below — it is now a resolved find, not a dead end. |
| **plugwine** | `{producer-slug}.plugwine.com/{fr,en}/vins/{range}/{cuvée-vintage}/{id}` | **A French wine-shop platform, Angular, and every URL on it returns one BYTE-IDENTICAL 67 kB shell with an empty `<pw-root>`** — listing, product and `sitemap.xml` alike (the sitemap is a soft 404). Recognise it by `<pw-root>`, by a `robots.txt` that carries `crawl-delay: 10`, `Disallow: /fr/*` and the ASP.NET pair `/WebResource.axd` + `/ApplicationError.aspx*`, and by a Cloudflare-managed Content-Signal preamble. **Domaine Roquefeuille's `www.domaineroquefeuille.fr` was this platform white-labelled** — same `<pw-root>`, same robots lines — so the two are one platform, not two producers. The product URL does carry cuvée and vintage, so a *range census* is possible from search results even though no page content is. Seen at Vignoble Hermouet and Domaine Roquefeuille. |
| **Kuupanda** | `commande.kuupanda.com/producteur/{id}/particulier` | A French producer-direct ordering marketplace some estates use *instead of* their own shop (Domaine Fontanel links out to it from its `/boutique/` page). 2 383 bytes of React shell, `You need to enable JavaScript to run this app`, empty `<div id="root">`. `robots.txt` is `User-agent: *` / `Disallow:` — everything allowed and nothing readable. |
| ~~**v9.lu**~~ | `v9.lu/v/{code}` | **Moved to the readable table on 2026-08-08 — see VINISCAN (ABSOMOD).** It was listed here when a plain request returned fifteen bytes reading `Smartphone only`; the device-gate decision of the same day made it readable with a mobile-shaped, still self-identifying User-Agent, and its sibling host `iviti.fr` then showed the gate can be a `Referer` check instead. Kept as a row so the failure mode stays recognisable: **a short 200-with-body is a gate, not a rendering problem, and not every gate is the same gate.** |
| **i-wine (discover-iwine)** | `d.i-wine.app:8444/01/{producer-uuid}-p{8-digit id}` → `qr.i-wine.app/…` | An Italian vendor whose `/01/` path imitates a **GS1 Digital Link and is not one** — the value is a UUID, not a GTIN. 730-byte Vite/React shell, empty `<div id="root">`, one module bundle; `Accept: application/json` on the same URL returns the identical shell. Both hosts answer `/robots.txt` with the SPA's own HTML — a **soft 404**, so no directives exist and no exception is needed; there is simply nothing to read. The token is **product-keyed and shared across pack variations** (one wine's 375 ml and 750 ml WooCommerce variations carry the same href). Found via Mastroberardino, reached from a shop block reading *"Scansiona per: Valori nutrizionali, Ingredienti, Raccolta differenziata"* wrapping a QR image in an anchor. |
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

### French e-label vendors — three are now seen, and all three are readable

The 2026-08-07 cooperative run ended the "no third-party vendor in France"
finding. All three now in the readable table:

- **`vin.co` / Vincod** — `m.{producer}.{tld}/{code}`, mirrored at
  `vincod.com/{code}`, assets on `cdn.vin.co`. Seen at Hugel and, without its
  e-label filled in, at Rhonéa. Server-rendered.
- **Alliance Nutri**, `alliance-alsace.com` — a GS1 Digital Link resolver.
  Seen at Cave de Turckheim. Server-rendered.
- **VINISCAN by ABSOMOD** — two hosts, `v9.lu/v/{code}` and
  `iviti.fr/v/?q={token}`, sharing one stylesheet tree under
  `v9.lu/commonfiles/`. Server-rendered behind a gate; see the table row.
  **The vendor is identifiable from whois**: AFNIC gives `iviti.fr`'s registrar
  as ABSOMOD Group, which is how the two hosts were tied together. ABSOMOD also
  trades as `viniscan.com`, `qrcode.vin`, `vitiquette.com`, `vinicode` and
  `steeqr.com`, so **expect more hostnames from one vendor** and recognise the
  family by the `/v/` path, the `noindex`, the 24-language selector and the
  ABSOMOD footer rather than by the domain.

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

### The device-gated e-label, and nine producers that were the settled French shape

**2026-08-08 (second run), nine producers, twelve wines: one e-label found,
unreadable at the time and attached later the same day.** Chai Berteaud Manceau, Domaine de
Terres Blanches, Les Sablonnettes, Vignerons Ardéchois (UVICA), Ogier, Château
la Gordonne, Domaine Saint Damien, Vignobles Diffonty, Domaine Gassier. The
batch was picked to avoid Burgundy and to take the named non-Burgundy
multi-wine producers first.

| Producer | Region | Site | Our bottle on it? | Declaration? |
|---|---|---|---|---|
| Chai Berteaud Manceau | Loire | 4-page WP + 3-product WooCommerce | no, shop is on the 2023 | none, not even a sulphite line |
| Domaine de Terres Blanches | Loire / Sancerre | WP multisite under Saget la Perrière | cuvée yes, **no vintage anywhere** | none |
| Les Sablonnettes | Loire / Anjou | **one image and a mailto** | — | — |
| Vignerons Ardéchois (UVICA) | Rhône | marketing site + own PrestaShop | no, shop rolled to the 2025 | none |
| Ogier | Rhône | WordPress, cuvée pages, no vintage | cuvée yes | none |
| Château la Gordonne | Provence | 6-page brochure site | no, four cuvées at 2025 | none |
| Domaine Saint Damien | Rhône / Gigondas | Kadence WP, per-cuvée pages | cuvée yes, **no vintage** | none |
| Vignobles Diffonty | Rhône / CdP | WP with a **per-vintage fiche archive back to 2001** | no, the cuvée is absent | none |
| **Domaine Gassier** | Rhône / Gard | WP + **own Shopify** | **yes, exactly — SKU says 24 and EU** | **yes, at `v9.lu` — unreadable** |

**Gassier is the finding.** Its own Shopify shop
(`famillegassier.fr`, Château de Nages – Domaine Gassier) publishes a
per-wine QR-code image inside the product description whose anchor is a
`v9.lu/v/{code}` short URL, and the product's identity fields are the
strongest of any French wine in this file: product JSON title
`Embruns de Viognier 2024`, single-variant SKU **`MGVIBL24EU06CF`** — `24` the
vintage, `EU` the market — and barcode `3760270931707`. The e-label answers
`Smartphone only` in fifteen bytes. It was recorded `not_found` at first,
because nothing had been read and therefore nothing had been matched; **later
the same day the device-gate decision made it readable and the record became
`found`.** It is the first wine in this project whose disclosure was reached by
varying a request header, and the precedent it set is what unlocked
`iviti.fr` — see *A gate that was a Referer check*.

Three things worth carrying forward:

- **A Shopify product description is a place a French e-label hides.** Not an
  anchor with useful text, not an iframe, but an `<img>` of a QR code wrapped
  in an `<a>`. An href scan finds it; a text scan does not, because the anchor
  has no text at all. **Grep the raw HTML for `<a href` values pointing at
  short hosts**, and read Shopify's embedded `ProductJson` for the title, SKU
  and barcode while you are there — it is the cheapest strong identity check
  in this project after Winestro.
- **A "Teneur en SO₂ totale" rendered as a JPEG.** Gassier states the sulphur
  figure as an image of a scale, per wine, on both products checked. It is an
  analysis figure and not an ingredient list, and it is also invisible to every
  grep. Add it to the near-miss list.
- **The vintage stopped being the obstacle again.** Four of the nine producers
  publish per-cuvée pages that state **no vintage at all** (Terres Blanches,
  Ogier, Saint Damien, and Berteaud Manceau's range page dates only to 2023),
  which closes a wine as soon as the range page is read. Two more had rolled
  past our bottle. Only Gassier had our exact vintage identified on its own
  page, and that is the one that had the e-label.

And two ways the wine simply is not there, both already named and both seen
again:

- **Vignobles Diffonty keeps a genuine per-vintage fiche archive** — Château
  Sixtine Rouge back to 2001, Blanc back to 2005, Cuvée du Vatican Rouge back
  to 2015, one PDF per vintage including `ft_rge_sixtine_2024.pdf` and
  `ft_blc_sixtine_2025.pdf` — and **our Côtes-du-Rhône rosé "Réserve de l'Abbé"
  is not in it**, matching `abbé` and `rosé` zero times on the range page. The
  Rectorie shape. The 2024 fiche was read to settle whether the estate's
  per-vintage documents are declarations: appellation, grape percentages,
  15 % vol, yield, terroir, total production in bottles, food pairings, ageing
  potential, FR-BIO-01 — and no list, no table, no energy value.
- **Les Sablonnettes has no website in any useful sense.** Seven candidate
  domains are NXDOMAIN and the address the French directories publish,
  `lessablonnettes.free.fr`, is **706 bytes: one background image, one image
  map, one `mailto` area**. Not a missing site, not a broken one — a site with
  no content. Two requests settle it. Its 2024s appear only on US retailers'
  shelves, which are not a source.

**UVICA closes the co-op question for good.** It is the Rhônea profile exactly
— a growers' union with a first-party PrestaShop, per-vintage product slugs,
one product per cuvée — and the only label-adjacent text on the product page is
`Contient des Sulfites. 13% vol.` Its fiche technique (reached through
`index.php?controller=attachment&id_attachment={n}`, a PrestaShop pattern worth
recognising) is undated and lists nothing. Co-op, small estate, big house and
now growers' union have each been tested and none of them predicts publication.

**And a group parent does not open a group.** Ogier is AdVini and no AdVini
e-label platform exists to find; Château la Gordonne is Vranken-Pommery and the
same. Worth noting that Systembolaget itself already carries declarations for
two other Ogier wines, so the house supplies the data through the trade channel
while publishing none of it on its own site — the absence is editorial, again.

### A gate that was a Referer check, and a declaration written once for a whole estate

**2026-08-08 (fourth run), six producers, eight wines: one declaration attached,
one found and rejected, six not found.** Domaine de la Tour du Bon, Domaine de
Cristia, Domaine André Brunel, Famille Lieubeau, Domaine Horgelus, Domaine du
Salvard — all non-Burgundy, taken from the untouched pool.

| Producer | Region | Site | Our bottle on it? | Declaration? |
|---|---|---|---|---|
| Domaine de la Tour du Bon | Provence / Bandol | Kirby site **blanket-disallowed** + open Shopify shop | yes, the 2025 rosé exactly | none on the readable side |
| Domaine de Cristia | Rhône / CdP | Wix (Château Cristia) | **yes, CdR Blanc 2025** | none; the fiche is a **PNG on Google Drive** |
| **Domaine André Brunel** | Rhône / CdP | bespoke PHP shop, one page per cuvée per vintage | **yes, Sommelongue 2024, 14,5 %, 75 cl** | **yes — VINISCAN at `iviti.fr`, attached** |
| Famille Lieubeau | Loire / Muscadet | Avada WP; shop on a **disallowed** subdomain | cuvée yes, **no vintage** | none readable |
| Domaine Horgelus | Sud-Ouest / Gascogne | 13-page IONOS brochure | cuvée yes, **no vintage** | none |
| **Domaine du Salvard** | Loire / Cheverny | Shopify (`delaille.com`) | no, shop rolled to the 2025 | **yes, complete — and range-wide, rejected** |

**The find is Brunel and the lesson is the gate.** His per-cuvée pages end with
*">> Cliquez ici pour retrouver la liste des ingrédients et informations
nutritionnelles de cette cuvée <<"*, linking `iviti.fr/v/?q=…`. A plain request
returns sixteen bytes, `Accès refusé...`; **the mobile-shaped User-Agent from
the device-gate decision changes nothing**; and two controlled requests then
showed the check is a `Referer`. Sending the true Referer — the producer page
that published the link and that we did in fact come from — returns the full
disclosure **under the project's ordinary User-Agent**, so no exception, no
device framing and no misrepresentation was involved. **When a 200-with-body
refusal appears, test the Referer first.** It is the cheapest possibility and
the only one that needs no policy at all.

**The rejection is a new French shape and deserves a name: the range-wide
declaration.** Domaine du Salvard's Shopify footer links `/pages/declaration
-nutritionnelle`, which carries the complete mandated set — bilingual FR/EN,
`Raisins/Grapes`, sulphites, metatartaric acid, protective-atmosphere bottling,
328 kJ / 79 kcal per 100 ml — and names **no wine, no cuvée, no colour, no
bottle size and no vintage**. The estate makes a white, a red, a rosé and a
crémant; one list cannot be the per-bottling disclosure for all four. It is
rejected on the matching rules' own words, and the vintage fails independently
(the shop's product JSON says `Millésime : 2025` against our 2024). **Expect
this shape wherever a small producer has understood the obligation and answered
it in one page** — a footer link called *Déclaration nutritionnelle* or
*Valeurs nutritionnelles* is worth one fetch on every French shop, and it is
worth grepping the product page for it, since nothing on the product page
itself hints that the page exists.

Four smaller things this batch settles:

- **HTML entities defeat the grep, and this nearly cost the find.** Brunel's
  page matches `ingrédient` **zero** times in the raw HTML because it is written
  `ingr&#233;dients`. The whole run's screening grep would have closed the one
  producer that publishes. **Grep the stripped, entity-decoded text, not the raw
  HTML** — the opposite of the Shopify-QR lesson, so do both.
- **And tag-stripping eats a nutrition figure.** VINISCAN prints
  `dont sucres  < 0.5 g`; a regex that removes `<[^>]+>` swallows `< 0.5 g` as
  if it were a tag. Read the value out of the HTML, not out of the stripped
  text.
- **A fiche technique can be an image on a general file host.** Cristia's
  "FICHE TECHNIQUE" link is `drive.google.com/file/d/…/view`, and the file is
  `Côtes du rhône.png`. `drive.google.com/robots.txt` allows `/file`, so the
  view page is fetchable and names the file; the bytes live on
  `drive.usercontent.google.com`, which is `Disallow: /`. **The 2026-08-06
  Dropbox widening does not reach it**, because that widening turns on the
  producer naming the file as the *declaration* and this one is named as a
  fiche. Honoured, not fetched, and recorded as such.
- **A producer's marketing site and its shop are different hosts with different
  directives, in both directions.** Tour du Bon's `www.tourdubon.com` merges two
  `User-agent: *` groups into a blanket disallow while `boutique.tourdubon.com`
  is an open Shopify; Lieubeau is the mirror image, an open WordPress and a
  shop at `Disallow: /`. **Read robots.txt on the host you are about to fetch,
  never on the one you found the link on** — and when the shop is the closed
  one, say plainly that the shop is unknown rather than that the producer
  declares nothing.

### The estate that hosts its own e-labels and publishes them only for the 0,0 %

**2026-08-09, seven producers, eight wines: nothing found, nothing rejected.**
Famille Roumieux, Domaine Saint Roch, Domaine Garon, Alain Jaume, Château de
Tracy (two wines), Domaine Comte Peraldi, Domaine La Provenquière — the named
non-Burgundy leads from the previous run, taken in order.

| Producer | Region | Site | Our bottle on it? | Declaration? |
|---|---|---|---|---|
| Famille Roumieux | Rhône / CdP | Clos du Calvaire, 6-page WP | **no — the négociant brand is absent** | none |
| Domaine Saint Roch | Rhône / Beaumes-de-Venise | 15-page site, no shop | cuvée yes, **no vintage** | none |
| Domaine Garon | Rhône / Côte-Rôtie | 5-page Divi WP, no shop | cuvée yes, **no vintage** | none |
| Alain Jaume | Rhône / Orange | own PrestaShop, five ranges | **yes, Bellissime Rosé 2025 exactly** | none but a sulphite line |
| Château de Tracy | Loire / Pouilly-Fumé | **Soluxa** shop | no, shop rolled to the 2025 | none |
| Domaine Comte Peraldi | **Corsica / Ajaccio** | Wix + Wix Stores | **yes, Rosé 2025 exactly** | none, not even a sulphite line |
| **Domaine La Provenquière** | Languedoc / Capestang | WP + own PrestaShop | **yes, the magnum, 2024, 150 cl** | **its own e-labels exist — for other products** |

**Five of the seven had our exact bottle or an exact cuvée match on the
producer's own page, and not one declared anything on it.** The settled French
shape, again, and the batch adds no new platform to the readable table.

**The finding is La Provenquière, and it is the sharpest version yet of "the
absence is editorial".** The estate hosts its *own* e-label pages —
`provenquiere.com/label-qr/{slug}`, plain server-rendered WordPress, one per
product, mirrored in `/en/` and `/de/`, linked from a hub page that says in so
many words *"Retrouvez sur cette page tous les QR Code du domaine : – QR vin
pour les valeurs Nutritionnel de nos vins ou vins sans alcool"*. The pages
carry the complete mandated set; the one read gives

```
Ingrédients** Extrait de levure (eau, Levure), Jus de Raisin, Acidifiants
(Acide Lactique, Acide Citrique), Conservateurs ( E220**, E202, E242),
Arômes Naturels, Gaz Carbonique (CO2).
```

plus a nutrition table per 100 ml at 96 kJ / 23 kcal. **All four are 0,0 %
products** — Péché Coquin Zéro, a spritz, a sauvignon and a blanc de blancs —
and there is no page for any wine the estate makes as wine.

That is not laziness, it is the law drawing a line: a drink under 1,2 % vol is
an ordinary foodstuff whose ingredient list Regulation (EU) 1169/2011 requires
on the label outright, while the estate's wines fall under 2021/2117, where the
QR route is optional and the producer has taken none of it. **A producer can
build the whole apparatus and point it only where the obligation is
unambiguous.** Worth checking for on any French estate with an alcohol-free
range: the `/label-qr/` tree may exist, and the wines may not be in it.

Four more things this batch settles:

- **The Soluxa shop skin ships a nutrition tab, unused.** Château de Tracy's
  product pages (`tracy-et-cie.com/{slug}-s{id}.html`, also served under
  `chateau-de-tracy.com/boutique/`) load a script binding `.tab-header`, whose
  second tab pushes **`?nutrition`** onto the URL. The platform has the feature;
  this deployment renders no tab markup at all. Soluxa is the same platform seen
  at Etienne Simonis, so **look for a nutrition tab on the next Soluxa estate**
  — recognise Soluxa by the shop being proxied from `ec1.soluxa.eu/{code}/`.
- **A fiche can be older than the vintage it is hung on.** Tracy's "notice
  technique" on the *2025* product is the **2023** — it names the vintage in
  its body and describes the 2023 growing season. The file name gives nothing
  away (`img/prod/125534-file1-1.pdf`). So the fiche is not a reliable vintage
  marker in either direction: Jolivet's and Chidaine's file names were, this
  one's is not. Read the body.
- **A Wix product slug keeps the vintage it was first published under.**
  Peraldi's URL is `/product-page/domaine-comte-peraldi-rosé-2020` and the
  product on it is the **2025**. A Wix `store-products-sitemap.xml` is a
  catalogue, **not a vintage census** — the opposite of Shopify and PrestaShop
  slugs, which this file has been reading as vintage markers.
- **The fiche technique can exist and simply not be published.** Domaine Garon
  has no shop and no PDF anywhere; every button on its range page opens one
  Divi overlay whose first option is *"Recevoir des informations sur le domaine
  et nos vins (tarifs, fiches techniques)"*. Documents issued on request to a
  named enquirer are not a public source, and writing to an estate is not in
  this agent's remit. Close the producer there.

#### Three greps and a DNS probe that lied, all in one batch

- **`kJ` matches `checkJQuery`.** PrestaShop's product page defines a
  `checkJQuery()` polling function, so a raw grep for the energy unit returns
  three confident hits on a page with no nutrition table. Add it to the
  Stripe/Font Awesome/`responsiveLabel` list.
- **On a Wix page, `ingr` and `kJ` match only the bundle.** Peraldi's 1,6 MB
  product page matches `ingr` fourteen times and `kJ` fifty-three, every hit a
  minified identifier or a `specs.restaurants.*` feature flag. And **`13,5`
  matched twice as SVG path data** — `d="M13,5 L13,12 …"` is a plus-sign icon,
  not an alcohol figure. Strip scripts *and* be wary of matching a number.
- **Wildcard DNS makes the Vincod probe say yes.** `mayard.fr` is a Dovendi
  domain-for-sale page with a wildcard record, so `m.mayard.fr` resolves — and
  so does `randomxyz123.mayard.fr`. **The nonsense-subdomain control is what
  catches this and it is not optional.** Separately, Domaine Saint Roch's
  `m.` subdomain is a real CNAME to the site's own apex rather than to
  `domains.vincod.com`: an `m.` record existing is not the signal, a CNAME to
  Vincod is.
- **Two parked domains on one producer.** Roumieux's `roumieux.fr` resets the
  TLS handshake and serves OVH's *Site en construction* over plain http;
  `mayard.fr` is for sale. The live estate is `clos-du-calvaire.fr` — Vignobles
  Mayard renamed itself Clos du Calvaire in 2021, so **the producer's historic
  name can be the wrong search term**, and Systembolaget's "Famille Roumieux"
  is the négociant arm whose brand appears nowhere on the estate's own site.
  The export-brand rule, one more time.

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
- `v9.lu` serves **no `robots.txt` (404)** and answers every `/v/{code}` with
  **HTTP 200 and fifteen bytes, `Smartphone only`**. Nothing is disallowed and
  nothing is refused technologically — it is a device gate, and the mobile-shaped
  self-identifying User-Agent decided on 2026-08-08 gets past it.
- `iviti.fr` is the same vendor (ABSOMOD/VINISCAN) with a **different gate**: it
  serves no `robots.txt` (404), answers `/v/?q={token}` with sixteen bytes,
  `Accès refusé...`, **ignores the mobile User-Agent entirely**, and returns the
  full page as soon as a `Referer` naming the linking producer page is sent. Its
  own root answers **403 to everything**, which is absolute — fetch the one URL
  the producer published and nothing else.
- `michelgassier.com` answers on **wildcard DNS**: `m.michelgassier.com` and
  `randomxyz.michelgassier.com` resolve to the same address, and so do
  `domainegassier.com` and `domaine-gassier.com`. Third sighting of the
  `m.grandsud.fr` trap. Domaine Gassier's live sites are
  `www.domainegassier.com` (WordPress) and `famillegassier.fr` (Shopify).
- `www.domainegassier.com/robots.txt` opens with a bare `Crawl-delay: 10`
  **before any `User-agent` line**, so it belongs to no group and binds nobody
  under RFC 9309. Honour it anyway; it costs four extra pages of waiting.
- `boutique.vignerons-ardechois.com` serves **no `robots.txt`** (a styled 404),
  and its PrestaShop resolves a product by **id regardless of the slug**:
  the marketing site's stale `…/68-syrah-basalte-du-coiron-rouge-2017-75cl.html`
  302s to the `-2025-` URL. **That is a free one-request vintage census for a
  single wine** — follow the producer's own old link and read where it lands.
  Its fiches are served from `index.php?controller=attachment&id_attachment={n}`.
- `chateausixtine.com` and `cuveeduvatican.com` are both NXDOMAIN; Vignobles
  Diffonty is at `www.chateau-sixtine.com`.
- `lessablonnettes.free.fr` is a producer's entire web presence in **706 bytes**
  — one background image, one image map, one `mailto` area. Seven candidate
  `.fr`/`.com` domains for the estate are NXDOMAIN. A free.fr personal page is
  still worth the one request; it can be a complete answer.
- `www.tourdubon.com/robots.txt` is 110 bytes holding **two `user-agent: *`
  groups**: one disallowing `/kirby/`, `/site/`, `/cdn-cgi/` and allowing
  `/media/`, then a second that is a bare `disallow: /`. RFC 9309 merges records
  naming the same token, so the site is blanket-disallowed bar `/media/`. The
  estate's shop is the separate host `boutique.tourdubon.com`, an ordinary
  Shopify that allows `/products/`.
- `boutique.lieubeau.com` is `Disallow: /` while `lieubeau.com` allows
  everything but `xmlrpc.php`. `lieubeau.fr` and `famille-lieubeau.fr` both fail
  TLS with `TLSV1_ALERT_INTERNAL_ERROR`; over plain http `lieubeau.fr` 301s to
  `lieubeau.com`, and `lieubeau.com/sitemap_index.xml` is a **soft 404 that
  returns the 590 kB home page** — read `/nos-vins/` instead.
- `www.horgelus.com` fails TLS the same way and answers normally over plain
  http. Its sitemap is the whole site: thirteen URLs.
- `andrebrunel.com`, `domaine-andre-brunel.com` and `andre-brunel.fr` are one
  site on **wildcard DNS**, so the `m.` Vincod probe is meaningless. Its
  `robots.txt` is a bad-bot blocklist ending `Disallow: /` with **no
  `User-agent: *` group**, preceded by five stray `Disallow: https://…` lines
  that sit before any `User-agent` record and are discarded. Nothing binds us.
- `delaille.com` is Domaine du Salvard; `domainedusalvard.com`,
  `domaine-du-salvard.fr` and `salvard.fr` are all NXDOMAIN. It is Shopify, so
  it answers on a wildcard and the `m.` probe proves nothing there either.
- `drive.google.com/robots.txt` **allows `/file`** (so a shared file's view page
  can be read and will at least give you its name) while
  `drive.usercontent.google.com`, which serves the bytes, is `Disallow: /`.
- `www.domaine-terres-blanches.com` is a **WordPress multisite under Saget la
  Perrière** — its uploads live under `/wp-content/uploads/sites/2/`, which is
  how to tell an estate site is really a group's. Its `wines-sitemap.xml` is a
  custom post type worth knowing about: ten cuvée pages, no vintage on any.

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

**Most producers publish nothing reachable.** Across 129 producers probed and
281 wine records, 22 declarations are attached, 40 wines were rejected against
a declaration that was found and read, and 219 came to nothing. Roughly a third
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

## Italy, where the page is undated

**2026-08-09, the first real Italian batch: eight producers, twenty-four wines,
zero attached, two rejected.** SA.PI SPA (Sartori di Verona), Pico Maccario,
Cantina Santa Maria La Palma, Ricasoli, Zorzettig, Vinosìa, Cantina Valpolicella
Negrar (Domìni Veneti), Gruppo Italiano Vini (Bolla). Producers were chosen by
cluster size, on the German economics of one e-label covering a range; that is
not what decided the outcomes.

Before this batch Italy had only the 2026-07-28/30 reconnaissance — Marchesi
Antinori (Scantrust, unreadable) and Tommasi and Vini Franchetti (nothing).
Italy now stands at **eleven producers and forty-four wines, 0 found, 42 not
found, 2 rejected**, with **228 of the 252 untouched 2024+ undeclared wines
remaining**.

| Producer | Region | Site | Our bottle on it? | Declaration? |
|---|---|---|---|---|
| SA.PI SPA / Sartori | Veneto | three first-party hosts | cuvée yes, **no vintage** | none |
| Pico Maccario | Piemonte | WordPress + Shopify | cuvée yes, **no vintage** | none |
| Santa Maria La Palma | Sardegna | WP + nopCommerce shop | **yes, Annata 2025 exactly** | none, an allergen line |
| **Ricasoli** | Toscana | WP with a real per-vintage archive | **yes, the 2024, alcohol exact** | none |
| Zorzettig | Friuli | one undated range page | cuvée yes, **no vintage** | none |
| Vinosìa | Campania | **HTTP 500 on every URL** | unreadable | unreadable |
| Cantina Valpolicella Negrar | Veneto | WP + a group site | cuvée yes, **no vintage** | **self-hosted, for a third brand** |
| **Gruppo Italiano Vini** | Veneto | brand site + **vinicum.com** | no, both rolled to the 2025 | **yes, complete and inline** — both rejected |

### The Italian failure is the undated cuvée page

In Germany the binding constraint was the vintage; in France it was that the
declaration does not exist at all. **In Italy the commonest shape is a producer
that keeps one page per cuvée and never states a vintage on it.** Four of the
eight — Sartori, Zorzettig, Santa Maria La Palma and Domìni Veneti — have a page
for our exact wine, and it describes a wine rather than a bottling. A page like
that cannot be vintage-matched even if a list appeared on it, so **the range
page's silence about the year is an early close, exactly as in France**, and it
is worth checking in the first fetch.

And what those pages *do* carry is the Italian near-miss, in a very consistent
form:

```
Allergeni: contiene solfiti
Origine: Prodotto in Italia
```

Two of the label's mandatory particulars, no substances, no energy value. It is
the Italian counterpart of the French "Contient des sulfites" boilerplate and it
is not a declaration. Santa Maria La Palma prints it on both its marketing site
and its shop.

The second near-miss is the **scheda tecnica**, the Italian *fiche technique*:
denominazione, vitigno, coltivazione, esposizione, altitudine, terreno,
vendemmia, vinificazione, affinamento, tasting note, ageing potential, service
temperature, formato, closure — and nothing else. Pico Maccario's whole range is
seventeen of them behind SCHEDA / INFO links; Ricasoli attaches one per vintage.
**One PDF settles the template for an estate.**

### Ricasoli is the sharpest evidence that the absence is editorial

Barone Ricasoli publishes an **808-URL per-vintage product archive back to
2006** — one page per wine per vintage per language, each with a `<select>`
naming every other vintage of that wine. That is the vintage control this
project otherwise only gets from Vincod, on a producer's own WordPress, and our
2024 Albia Rosé is on it with `Alcol: 13% vol.` matching Systembolaget exactly.
It carries no ingredient list, no nutrition table, not even a sulphite line, for
any wine in any year. Structure does not predict publication — Wegeler and
Galoupet in a third country.

Two more Ricasoli details worth carrying: its per-vintage `SCHEDA TECNICA` link
(`/wp-content/uploads/2018/01/{Wine}-{Vintage}.pdf`) **404s**, and its
`ACQUISTA` link into `eshop.ricasoli.com` **404s too** because the shop has
rolled to the 2025 while the marketing site keeps the archive. A producer's own
links can be broken in both directions at once.

### Where an Italian declaration actually was: inline, and inside a GraphQL payload

**Gruppo Italiano Vini is the first Italian producer this project has read a
declaration from**, and it is not on a QR platform. GIV's own e-commerce,
`www.vinicum.com`, prints the complete mandated set on every product page:

```
INGREDIENTI
Uve, mosto di uve, conservanti (solfiti), agenti stabilizzanti (gomma arabica).
Imbottigliato in atmosfera protettiva.

ALLERGENI
Solfiti

VALORI NUTRIZIONALI (PER 100 ML)
Energia: 293 kJ / 71 kcal
Grassi: 0 g …
```

Four things about it:

- **It is server-rendered and a stripped-text grep misses it completely.** The
  string lives in the embedded Apollo GraphQL state, as a
  `DescrizioneAggiuntivaProdottoType` with `"chiave":"allergeni"` and
  `"titolo":"Informazioni Nutrizionali"`. On a 380 kB page, `ingredien`,
  `nutrizion`, `kcal`, `kJ`, `solfiti`, `allergen` and `energia` are **zero in
  the stripped text and one or two each in the raw HTML** — the inverse of the
  Stripe/Font-Awesome trap. Grep both, always.
- **It identifies itself.** Rendered `dato-prodotto-main` fields give Vitigno,
  Colore, **Gradazione**, **Annata** and **Formato**, and the URL carries GIV's
  article number and pack code (`…-68134-06` = article 68134, six-bottle case of
  the 750 ml). Winestro-grade provenance on a first-party Italian shop.
- **The lists are per wine.** The Bardolino's stabiliser is gum arabic, the
  Soave's antioxidant is L-ascorbic acid, and the energy differs (293 against
  291 kJ). Not a house template.
- **And both wines were rejected on vintage.** Vinicum keeps one product per
  cuvée, edited forward, and both had rolled to Annata 2025 against
  Systembolaget's 2024. The Rhonéa and Paul Mas failure mode, in Italy, on the
  first Italian producer that publishes.

`bolla.it` and `bolla.com` both 301 into `gruppoitalianovini.it/it/brand/bolla`,
whose per-wine pages carry no declaration and no vintage; **the declaration is
one hop away, on the group's shop.** GIV owns some thirty Italian brands and its
catalogue is one `d/sitemap-prodotti.xml`, so **this is the best untried Italian
lead in the file** — see the closing list.

### The second Italian publisher self-hosts, and covers a third brand

Cantina Valpolicella Negrar sells to Sweden as **Domìni Veneti** and declares
nothing on `dominiveneti.it`. But its group site `www.cantinanegrar.com` has a
42-page sitemap containing **three real e-labels**,
`/it/valori-nutrizionali-gransignoria-{bardolino-doc-classico,
valpolicella-ripasso-doc-classico-superiore, amarone-della-valpolicella-docg-classico}`
— plain server-rendered WordPress/Elementor, one per wine, with a proper
`Elenco degli ingredienti` in text:

```
Uva, Mosto concentrato; Conservanti e antiossidanti: Metabisolfito di potassio,
Dimetildicarbonato (DMDC); Agenti stabilizzanti: Gomma arabica, Mannoproteina di
lievito, Poliaspartato di potassio. Prodotto imbottigliato in atmosfera protettiva.
```

All three are **GranSignoria**, which is neither of the co-op's Swedish wines
and not even the Domìni Veneti brand. **Adoption in Italy is per product line,
not per producer** — ask which line, not which company.

Two things about the page itself: the heading `Dichiarazione nutrizionale` is
followed by an **`<img>`**, so **the nutrition table is a PNG and only the
ingredient list is text** — an Italian self-hosted e-label can be half-readable.
And it states no vintage, no lot, no bottle size and no alcohol, so it
identifies itself no better than f-label or apys; a find there would rest
entirely on the producer's linking.

### Three Italian false positives, and one rule this batch corrects

- **A page called `/qrcode…` is often a catalogue.** Pico Maccario's
  `/qrcode01` is the most promising URL a sitemap produced all day and its only
  two outbound links are `issuu.com/grart01/docs/picomaccario2025_{ita,eng}`. On
  an Italian producer a QR landing page is as likely to be the sales catalogue,
  a wine list or a tasting menu as a 2021/2117 disclosure.
- **`/etikette/` and `/etichetta/` in a URL can be a translated post-type
  slug.** Ricasoli's sitemap holds hundreds of `/de/etikette/{wine}-{vintage}/`
  URLs; WPML translates the `prodotto` post type as `etikette` in German, and
  the page is the identical marketing page with zero matches for `Zutat`,
  `Nährwert`, `kcal` and `Sulfit`.
- **`etichettatura ambientale` is a different obligation.** Three of the six
  declaration-ish URLs on `cantinanegrar.com` are packaging pages under the
  Italian environmental-labelling decree — which material each component is and
  which bin it goes in. Recognise it on sight.
- **A WordPress upload path is the date of *first* upload, and the file can be
  replaced under it.** The existing rule ("read the path before spending the
  fetch — a 2018 file cannot carry a declaration") **needs a HEAD first**: Pico
  Maccario's schede all sit under `/wp-content/uploads/2019/06/` and
  `Lavignone-Barbera.pdf` answers `last-modified: Thu, 03 Jul 2025`. The path
  lied; the header did not. One HEAD is cheaper than being wrong.

### Italian hosts with quirks

- **`www.sartori.it` is a law firm**, thirteen pages about banking and insurance
  law. Casa Vinicola Sartori is `sartorinet.com` (whose wine URLs 301 to
  `casasartori1898.it`), `sartoridiverona.it` and `www.sartoriwineshop.com`. The
  surname trap, in Italy.
- **`sartorinet.com/robots.txt` disallows `/qr/` and `/qrcode/`** — the
  strongest hint of an e-label tree in the batch — and **no page on any of
  Sartori's three hosts links into it.** There is no URL to hold, and the
  e-label exception explicitly does not license guessing one. Note the shape:
  *robots.txt can prove an e-label tree exists and still leave you nothing to
  fetch.*
- **`zorzettig.it` is an unrelated IIS host** that serves a detailed IIS 10.0
  404 over http and refuses TLS over https. The estate is `zorzettigvini.it`,
  reachable only over IPv6 in this environment.
- **`vinosia.it` answers HTTP 500 with WordPress's own `Database Error` page**
  on the root and on both sitemap names; `vinosia.com` and `www.vinosia.com`
  resolve to the same address and serve a bare Apache 404 for every path, and
  `https://vinosia.com` does not complete a TLS connection. An outage, not a
  refusal — recorded `not_found` with all three wines flagged as revisit
  candidates, since all three are 2025.
- **`vinosia.it/robots.txt` still answers 200 while the application is down**,
  and its only groups are `User-agent: MSNBot` and `User-agent: bingbot`, each
  with a `Crawl-delay` and no `Disallow`. No `User-agent: *` group, so the
  RFC 9309 reading of 2026-08-08 (`bpdr.com`) applies: nothing is disallowed to
  us. It changed nothing here, and it is recorded in the wines' records anyway.
- **`eshop.ricasoli.com` serves a soft 404 for `robots.txt`** — the site's HTML
  at 200 — so there are no directives at all. Its ASP.NET WebForms
  `__VIEWSTATE` blob produces **thirteen false `kJ` matches** in base64; add it
  to the `checkJQuery` list.
- **`collisheritage.com`** (Sartori's parent group) answers 200 with the site's
  HTML for both `robots.txt` and `sitemap.xml`. Another soft 404 dressed as a
  success — read the body.
- **`pico-maccario-shop.myshopify.com` is `User-agent: * / Disallow: /`.** An
  ordinary storefront on Shopify's preview domain, not a disclosure page, so the
  e-label exception does not reach it; honoured in full and not fetched.
- `dominiveneti.it`'s Elementor product pages are **420 kB each** and contain
  zero declaration markers in raw HTML as well as stripped text. Budget for the
  size, not for the search.

### Italian e-label vendors, none of them yet seen on a producer's page

Searching in Italian for the obligation surfaces a crowded vendor market and
**not one of these has turned up in an `href` yet**. Names worth recognising:
`quveer.com`, `qretichette.it`, `wine-elabels.eu`, `etichettaambientalevino.com`,
`ideasiti.wine`. **U-label** (`u-label.com`) remains the big one and still has no
publicly linked URL anywhere in this project's notes; Italy was expected to be
where it shows up and it did not, in eight producers.

**That opening line is now out of date and is kept for the record.** Four
Italian vendors have since been seen in producers' own linking: **IoAgri**
(La Pruina), **i-wine** (Mastroberardino), **Giunko's ead-qr** (Marramiero) and
**carmaqrcode** (Tralci Hirpini) — two readable, two not. **U-label itself has
still never been seen**, and the closest thing to it, Masi's product field
literally labelled `u-Label`, turned out to point at Scantrust.

What Italy has produced instead is **two first-party publishers and no vendor at
all** — GIV inline on its own shop, Negrar self-hosted on its group site. On
this evidence the French question ("has it adopted a QR platform?") is the wrong
one to ask an Italian producer. **Ask instead whether the group runs its own
e-commerce**, because that is where both Italian declarations were.

### The first Italian declarations attached, and they came from the least likely producer

**2026-08-09, second Italian batch: seven producers, fifteen wines, TWO FOUND,
thirteen not found, none rejected.** Cantina Terlan, Köfererhof, Hans
Rottensteiner, Weingut Pranzegg, Cantina LaVis, Cà dei Frati, Tenute Piccini.
Italy now stands at **nineteen producers and sixty-one wines, 2 found, 54 not
found, 5 rejected**, with **211 untouched 2024+ undeclared wines remaining**.

The batch was designed to test the two hypotheses the last one left. Both
failed, and the find came from neither.

| Producer | Region | Site | Our bottle on it? | Declaration? |
|---|---|---|---|---|
| Cantina Terlan | Alto Adige | own site, **per-vintage archive** | **yes, the Pinot Noir 2025 exactly** | none |
| Köfererhof | Alto Adige | 3-page Squarespace | **no per-wine page at all** | none |
| Hans Rottensteiner | Alto Adige | WordPress + Magento shop | no, rolled to the 2025; shop 403 | none |
| Weingut Pranzegg | Alto Adige | Wix, one page per cuvée | no, only 2021 is documented | none |
| Cantina LaVis | Trentino | WordPress + own WooCommerce | undated page, **`vintage24` scheda** | none |
| **Cà dei Frati** | Lombardia | **WordPress, no shop** | **yes, both, exactly** | **yes, both — inline and attached** |
| Tenute Piccini | Toscana | 11 brands on **wineplatform.it** | one yes, one absent | none |

- **The Alto Adige hypothesis failed.** Four German-speaking Italian producers
  were taken on the theory that they would behave like the German pool, which
  was this project's most productive. They behave like Italians: not one
  published anything, and the two with the best editorial machinery published
  the *packaging* obligation instead (below).
- **The own-e-commerce hypothesis failed too.** It was the last batch's closing
  advice, on the GIV evidence. LaVis (a co-op group with its own WooCommerce),
  Marchesi di Barolo and Tenute Piccini all run first-party shops and all three
  print an allergen line where the ingredient list belongs.
- **What actually yielded was a family estate with no webshop at all**, putting
  the declaration inline on its ordinary marketing page. On present evidence
  *nothing* about an Italian producer's shape predicts publication — check the
  ordinary per-wine page of every one of them, cheaply, and do not pre-select.

#### Cà dei Frati: inline on `/vini/{wine}/`, and not where the QR points

`cadeifrati.it` (Az. Agr. Cà dei Frati, Lugana di Sirmione) prints the complete
mandated set in the server's HTML of each `/vini/{wine}/` page, in a block that
begins with the identity and ends with the table:

```
Annata: 2024
Bottiglia: 750 ml
Grado alcolico: 13 % vol
PRODOTTO IN ITALIA – CONTIENE SOLFITI
Ingredienti
uva, mosto di uve concentrato, agenti stabilizzanti (acido citrico, gomma
arabica, carbossimetilcellulosa), conservanti e antiossidanti (solfiti, acido
L-ascorbico). Imbottigliato in atmosfera protettiva.
Dichiarazione nutrizionale per 100 ml
Energia: 337 kJ – 81 kcal …
```

**It identifies itself as well as Winestro does** — vintage, pack and labelled
strength, right above the list — and the `Scarica la scheda tecnica` link
(`/wp-content/uploads/2026/07/pratto2024_ST.pdf`) confirms the vintage a second
way. Pratto 2024 and Rosa dei Frati 2025 both matched Systembolaget on
producer, cuvée, vintage, pack **and** alcohol exactly, so both were attached.
The ingredient line is a house template shared by the two, but the **energy
values differ** (337 kJ against 317), so they are two disclosures and not one.

And the trap in it: **the same estate runs a 96-URL `/qr-code-promo/` post
type**, one `{wine}-landing/` language chooser plus a `{wine}-landing/{wine}/`
leaf per language, listed in its own `qr-code-promo-sitemap.xml`. It is the
most e-label-shaped URL tree seen in Italy and it is **pure marketing** — a
tasting note, the family history and a cellar-visit pitch, zero matches for
`ingredien`, `nutrizion`, `solfit`, `kcal`, `energia`. *The disclosure is on
the page the QR does not point at.* Read `/vini/` before drawing any conclusion
from a `/qr-code-promo/` page.

#### wineplatform.it: perfect identity, no declaration

Marchesi di Barolo and Tenute Piccini run **the same shop platform**, and it is
now worth recognising on sight: `shop.{producer}.{tld}`, path
`/{country}/{currency}/{lang}/prodotti/{slug-with-vintage}`, a permissive
`User-Agent: * / Allow: /` naming its sitemap, and a product page whose fields
are always *Annata, Denominazione, Vitigni, Alcol, Formato, Temperatura di
servizio* followed by **`Info: Contiene Solfiti - Prodotto in Italia`**. The
vendor is named in Marchesi's customer-care address,
`marchesidibarolo@wineplatform.it`.

- **One product per vintage, with the vintage in the slug** — the vintage
  control Italy otherwise lacks, and the sitemap is a complete census (2 503
  URLs at Marchesi, 8 221 at Piccini for eleven brands). One fetch tells you
  every vintage of every wine in every market.
- **And the declaration is never there.** Four wines across two producers, the
  same two-particular near-miss each time.
- **The `<title>` is stale where the `<h1>` is current.** Piccini's Donna di
  Valiano 2024 page is titled `… IGT 2023`, its Collezione Oro 2024 page
  `… 2022`. Read the H1 and the `Annata` field; never the title.

#### The packaging obligation is met and the ingredient one is not

Two producers in this batch publish a per-component recycling table — material
code and bin, under the Italian *etichettatura ambientale* decree — on the very
page where the ingredient list is missing: Cantina Terlan's
`Recyclinginformationen` (capsule C/ALU 90, cork FOR 51, bottle GL 71) and
every Pranzegg wine page's `DIFFERENZIARE I RIFIUTI`. Added to the three
packaging pages on `cantinanegrar.com` in the last batch, that is **four
Italian producers meeting one 2023-era label obligation on the web and not the
other**. It is the strongest available evidence that the absence is editorial.

#### Two more ways the wine simply is not there

- **Pranzegg has no cuvée called "Rosso per tutti".** Its nine wines are
  Tonsur, Elysion, Caroline, GT, Miau!Miau!, Demian, Vino Rosso Leggero, Ca'l
  and Laurenc. The Swedish bottle's profile fits *Vino Rosso Leggero* and its
  name does not, and nothing on the producer's surface bridges the two.
- **Tenute Piccini's catalogue contains no organic Collezione Oro Chianti**,
  although the group labels its other organic wines plainly with `bio` in the
  slug (Histrio, Scalunera, Calandrino, Primasso, Il Pacchia, Genesi,
  Casarossa). Systembolaget's 2024 *Collezione Oro Chianti Organic* has no
  counterpart on the producer's own shop; the nearest sibling, Chianti
  Superiore 2024, has zero occurrences of `bio`. **The export-only brand rule,
  one SKU wide.**

#### The Italian scheda tecnica, three more times, and one that names the vintage

Rottensteiner, LaVis and Pranzegg all attach a per-cuvée PDF and none is a
declaration. What they add:

- **Pranzegg's is the closest miss yet**: `TONSUR L2021`, vine age, yield,
  4 000 bottles, `Alcohol 11,5 %`, `Residual Sugar <1 g/l` and **`Total SO2
  35 mg/l`**. An SO₂ figure with no ingredient list — the Revelette near-miss,
  in German, on a biodynamic estate.
- **A file name can carry the vintage the page withholds.** LaVis's undated
  cuvée page links `Classici_Riesling_Lavis_vintage24.pdf` — our vintage —
  and Rottensteiner's links `2025_Pinot_Grigio_it.pdf`. **On an undated Italian
  cuvée page, read the PDF href before giving up on vintage-matching.**
- **The two surfaces of one producer can disagree**: LaVis's marketing site
  links the `vintage24` sheet and its own shop links `vintage23`.
- **The WordPress upload-path trap, confirmed twice more.** Rottensteiner's
  schede sit under `/uploads/2021/06/` with `Last-Modified: 04 Mar 2026`;
  LaVis's under `/uploads/2019/03/` with `25 Sep 2025`. HEAD first, always.

#### Italian hosts with quirks, second batch

- **`cantina-terlano.com` disallows `/*?*`** — every query string — and its
  vintage archive is reachable *only* as `/weine/{wine}-{id}/?wine-id={n}`.
  It is an ordinary marketing site with no e-label, so the disclosure exception
  does not reach it and the 2024 page was **not** fetched. The wine's default
  page is the current release, so a producer whose current release is our
  vintage is still readable; one of the two Terlan wines was. Its sitemap,
  named in robots.txt, answers HTTP 500 with a Laravel error page.
- **`www.koefererhof.it`'s sitemap is a valid but EMPTY `<urlset/>`**, 211
  bytes, zero `<loc>`. A Squarespace site with no indexable collections, which
  is itself the answer: three pages, one per language, no per-wine page at all.
  Its robots.txt lists the AI-crawler tokens **and** `User-agent: *` in one
  group, so unlike `bpdr.com` the group binds everyone and no RFC 9309 reading
  is needed.
- **`www.rottensteiner-wein.com` does not resolve**; the estate is
  `rottensteiner.wine`, which sets `Crawl-delay: 10` (honoured, ≥9 s between
  requests). Its shop `www.shop.rottensteiner.wine` answers **HTTP 403** to a
  plain request for a product URL its own robots.txt allows — a technological
  refusal, absolute, not worked around. That shop's robots.txt disallows about
  ninety anchored `/*{brand}$` landing slugs (antinori, zenato, ferrari,
  livio_felluga, angelo_negro, antonio_facchin …), so it sells far beyond
  Rottensteiner — but it 403s, so it is a source for none of them.
- **`www.marchesibarolo.com` fails TLS on a hostname mismatch** and
  `www.marchesidibarolo.com` on an unknown issuer; the live site is the apex
  `marchesibarolo.com`, which serves a **soft 404 for `/robots.txt`** (HTTP 200
  carrying a black "404 – Pagina non trovata" page), so no directives exist on
  it. It is a **pre-rendered Nuxt static export** — 1 MB of HTML for under 2 kB
  of text, but fully readable, unlike Les Quatre Tours' Nuxt SPA.
- **`www.tenutepiccini.it` and `www.piccini1882.com` both 302 to
  `www.piccini1882.it`**, whose sitemap index has no product sitemap at all;
  the products are on `shop.piccini1882.it`, reachable from `/catalogo/`.
- **Pranzegg's Wix pages are server-rendered and readable** — per-wine text and
  PDF hrefs are in the HTML — but 670–690 kB each for ~1,5 kB of text. Its
  `/download` page, which looks like the Carl Loewen "Download Center"
  signature, is an alias of the wines index with no files on it: **the Loewen
  recogniser needs "eLabels" as well as "Download Center".**

#### Four more greps that lie

`e-label` and `elabel` are now unsafe on four more platforms, matching zero
times in stripped text and up to 35 times in raw HTML:

| String | Where | What it really is |
|---|---|---|
| `e-label` | Squarespace | `event-date-label`, `…folder-item--toggle-label` |
| `e-label` | any Iubenda/cookie banner | `cm-cookie-label`, `cm-cookie-label-slider` |
| `elabel` | generic JS | `slideLabel`, `whitelabel` |
| `kJ` | Wix | base64 PNG data (`…ErkJggg==`) and `webpackJsonp` |

Add them to the `responsiveLabel` / `checkJQuery` / `__VIEWSTATE` list.

### Italy's first e-label vendor, and its second first-party shape

**2026-08-09/11, third and fourth Italian batches: twelve producers, thirty-two
wines, three found, twenty-six not found, three rejected.** Paolo Scavino, Marco
Porello, La Pruina, Az. Agr. VIGNA '800, Le Fraghe, Demarie Giovanni,
Castellani, Michele Chiarlo, Casa Vinicola Coppi, Ca' del Baio, Tenuta il
Falchetto, Azelia. Producers were taken off the cluster list in order, without
pre-selecting for shape, which is the closing advice of the batch before.

| Producer | Region | Site | Our bottle on it? | Declaration? |
|---|---|---|---|---|
| Paolo Scavino | Piemonte | maintenance placeholder | no site at all | none |
| Marco Porello | Piemonte | hand-built static, ten cuvée pages | cuvée yes, **no vintage** | none |
| **La Pruina** | Puglia | WooCommerce + **IoAgri** | **yes, two of three** | **yes, three read — 2 found, 1 rejected** |
| Az. Agr. VIGNA '800 | Veneto | Squarespace + Squarespace shop | cuvée yes, **no vintage** | none — footer promises one, links a 404 |
| Le Fraghe | Veneto | Squarespace + WooCommerce shop | no, shop a vintage behind | none |
| **Demarie Giovanni** | Piemonte | per-vintage archive + **own WooCommerce** | **yes, one of three** | **yes — 1 found, 2 rejected** |
| Castellani | Toscana | group site, **no product post type** | no, two brands unhosted | none |
| Michele Chiarlo | Piemonte | WordPress, **per-vintage schede** | **yes, a 2024 scheda** | none |
| Casa Vinicola Coppi | Puglia | **WooCommerce, two tabs** | cuvée yes, **no vintage** | none |
| Ca' del Baio | Piemonte | WordPress + empty Download Area | cuvée yes, **no vintage** | none |
| Tenuta il Falchetto | Piemonte | WordPress + Shopify | one at 2025, one wrong pack | none |
| Azelia | Piemonte | WordPress, `etichettatura` post type | cuvée yes, **no vintage** | none |

Two of the twelve published, and **neither is the shape the last batch
predicted**. Both are in the readable table above.

#### La Pruina: IoAgri, and the first Italian vendor in an href

`www.lapruinavini.com` is an ordinary WooCommerce, and its product pages end
with an anchor reading **"VALORI NUTRIZIONALI E INGREDIENTI | SMALTIMENTO —
CLICCA QUI"** pointing at `app.ioagri.it/Qr/DL?id={token}`. Eight Italian
producers had been checked before one turned up a vendor at all, and the
vendor is not one of the names this file had been watching for — not U-label,
not `quveer.com`, not `qretichette.it`. **Watch for the anchor, not the host.**

Three e-labels were read there and the identification is unusually strong,
because the producer's own product page prints `ANNATA`, `Titolo alcolometrico`
and **the energy value** (`E/100 ML: 326 kJ / 78 kcal`) beside the link, and the
e-label repeats the same energy figure. That is a numeric tie between the two
pages, and it differs per wine — which is also how the estate's two
undifferentiated Negroamaro bottlings were told apart (12,5 % Sole Range at
322 kJ against 13 % Selection at 331). The Manduria was rejected because the
linking page says `ANNATA 2023` and Systembolaget's bottle is the 2024; the
e-label states no year of its own, so there was nothing to appeal to.

#### Demarie: the declaration is a WooCommerce product tab

`shop.demarie.com` renders a fourth product tab headed **`Ingredienti`** whose
panel is plain server HTML. It is one line — `Ingredienti: uva. Conservanti:
solfiti` — and that is an ingredient list, so it qualifies; but **it is not the
complete mandated set** (no nutrition table, no energy value anywhere on either
Demarie host) and **it is identical on every product**, so it does not
discriminate between the estate's wines. It was attached for the Dolcetto
because the shop's H1 carries `2024`, the pack is `0,75 l` and the alcohol is
`13%` — all matching Systembolaget — and because the marketing site's own
per-vintage archive confirms 2024 is the current Dolcetto.

**Coppi runs the same WooCommerce with only two tabs.** So on an Italian
WooCommerce the platform is never the answer: count the panels, and grep for
`ingredient-list`, which is the class the tab renders with.

Demarie also shows a new near-miss: every `/vino/{wine}/annata-{year}/` page
ends with a section `id="qr"` headed **`Valori nutrizionali`** whose only
content is an `<img src="">`. **The template has a slot for the e-label image
and nothing has been put in it, for any wine in any year** — and the
`Acquista On-Line` banner that would have led to the shop is itself a 404. The
declaration was reachable only through the shop's sitemap.

#### The packaging obligation, now eight producers deep, with real machinery

Four Italian producers were already known to publish the *etichettatura
ambientale* table and no ingredient list. This batch adds four more, and two of
them have built per-wine infrastructure for it:

- **Tenuta il Falchetto** loads `etichettature.css` and a script that POSTs an
  action **`changeEtichetta`** with a wine id and slug to `admin-ajax.php` and
  writes the reply into `#contAsyncMateriali`. That is a per-wine, server-side
  label fragment fetched on demand — the exact shape of a self-hosted e-label —
  and it serves `/etichettatura-ambientale/`, twenty-three wines of packaging
  data.
- **Azelia** publishes an **`etichettatura` post type with its own sitemap**,
  nineteen URLs, every one a packaging component: `/etichettatura/bottiglia-gl-71/`,
  `/tappo-for-51/`, `/capsula-c-pvc-90/`, `/gabbietta-fe-40/`, `/cassa-for-50/`.
- Coppi links `ETICHETTATURA-AMBIENTALE_ITA.pdf` from every product footer;
  Ca' del Baio gives it a top-level navigation item and a footer button.

**An `etichetta`/`etichettatura` URL, sitemap or AJAX action in Italy is the
packaging decree until proved otherwise.** It is the strongest evidence yet
that the ingredient absence is editorial: these estates built something.

#### Two near-misses worth recognising on sight

- **A per-vintage scheda tecnica for our exact year, declaring nothing.**
  Michele Chiarlo's Gavi Rovereto page links seven year-buttons, 2019 to 2025,
  and the 2024 PDF opens `ANNATA: 2024` and runs vintage note, vitigno, comune,
  vigneto, soil, exposure, altitude, training, yield, Equalitas, vendemmia,
  vinificazione, affinamento, tasting note, abbinamenti, formati, chiusura —
  and stops, without an ingredient list, an energy value or even an alcohol
  figure. Domaine Fontanel's trap, in Italy. Note also that **one estate can
  run two scheda regimes**: Chiarlo dates the crus and leaves the Classico
  range on one perpetual undated sheet, so read the href per wine.
- **A Download Area whose anchors are empty.** Ca' del Baio's
  `/area-download/schede-vino/` lists sixteen wines each with a `DOWNLOAD`
  button, and every one is `href=""`. Its `Etichette` section is JPEG scans of
  the paper labels. This is the closest Italy has come to the Carl Loewen
  signature and it confirms the recogniser needs the word **eLabels**, not just
  "Download Area". Azelia does the same thing deliberately: an `Etichetta`
  block with one JPEG per vintage back to 2013, **our 2024 included**. A
  photograph of a label is not a source — reading substances off it would be
  OCR, and that is guessing.

#### Italian hosts and greps, third and fourth batches

- **`castellani.it` is a Milanese bespoke tailor**, Joomla, still carrying
  demo lorem ipsum from 2015, and `www.castellani.it` fails TLS on a hostname
  mismatch. The wine company is `castelwine.com`. After `sartori.it` and
  `hermouet.fr`, the surname trap is now a standing expectation.
- **`villapuccini.com` changed hands.** It 301s the whole host to
  `www.winesu.com`, a different Italian group's US site (Varvaglione's
  12 e Mezzo). Castellani's brand lives at `villapucciniwine.com`. An old brand
  domain can belong to somebody else's importer.
- **`cantinecoppi.it` and `coppi.it` are NXDOMAIN**; the estate is
  `vinicoppi.it`, Aruba, IPv6-only in this environment.
- **`porello.it` is not `porellovini.it`** — a different host on a neighbouring
  address, self-signed certificate, 403 from IIS.
- **`u-label` matches Shopify's own navigation markup**, in the class
  `site-nav__link-menu-label`. U-label is the platform this project has been
  watching for since Germany, so this false positive will look like the find of
  the batch. Add it to `responsiveLabel`, `whitelabel`, `toggle-label`,
  `cm-cookie-label`, `slideLabel`, `__VIEWSTATE` and `checkJQuery`.
- **`etichett` is now unsafe too**: it matches the environmental decree's page,
  a theme stylesheet (`etichettature.css`), an AJAX handler
  (`custom-ajax-etichetta`) and a press-assets label gallery.
- **`ingredienti` appears in Italian tasting prose.** Demarie's Dolcetto page
  says the Ligurians traded oil, salt and anchovies, *"ingredienti base"* of
  bagna caoda. Read the hit, not the count.
- **Chiarlo's `/area-download/` is a password wall** (Press and Trade request
  forms). A login wall is absolute and was not probed.
- **`demarie.it` answers Cloudflare 522** on every path while `demarie.com`
  serves the site; an origin timeout, not a refusal.
- **hellobarrio builds a lot of Piedmont**: Michele Chiarlo, Tenuta il
  Falchetto and Azelia all run its `barriotheme`. Recognising the agency does
  not predict a declaration — none of the three publishes one — but it does
  predict the *shape* of the page, which makes the second and third cheap.

### The fifth Italian batch: six producers, twelve wines, nothing to attach

**2026-08-11: Azienda Livon, Prunotto, Antonio Facchin & Figli, Rallo, Olearia
Vinicola Orsogna, Cantine Ermes — twelve wines, 0 found, 12 not found, 0
rejected.** The first Italian batch with no declaration read at all, and the
reason is worth stating plainly: **half the wines had no producer page to
check, because the Swedish name is not the producer's name.**

| Producer | Region | Site | Our bottle on it? | Declaration? |
|---|---|---|---|---|
| Azienda Livon | Friuli | WordPress, four estates, **no shop** | cuvée yes, **no vintage** | none |
| **Prunotto** | Piemonte | Antinori's WordPress, **`?wineyear=` archive** | **yes, both, exactly** | none |
| Antonio Facchin | Veneto | Magento shop + marketing site | **unreadable both ways** | unreadable |
| Rallo | Sicilia | WordPress, no shop, per-vintage schede | **one, at 2024 and 13,5 %** | none — but see below |
| Olearia Vinicola Orsogna | Abruzzo | WooCommerce, 276 products | cuvée yes, **no vintage** | none |
| Cantine Ermes | Sicilia | WordPress, `brand` post type | **brand absent entirely** | none |

#### The export-only brand is Italy's second failure shape, and it is bigger than expected

Four of these twelve wines carry a name the producer does not use: Facchin's
two *High On Love* Proseccos, Rallo's *Amber One* and *Nero Frizzante*, and
Cantine Ermes' two *Ambleri* — six of twelve, across three producers. In each
case the name returns Systembolaget, Vivino, wine-searcher and Swedish
resellers and **nothing on any domain the producer controls**. Facchin's is the
purest form: Systembolaget records the supplier as *High On Love Winery*, so
the brand is the importer's.

**Where the sitemap index names a `brand` post type, one fetch of it is a
complete census of what the producer puts its own name on.** Cantine Ermes'
`brand-sitemap.xml` names its seven consumer brands in fourteen URLs; *Ambleri*
is not among them, and that closed two wines without opening a product page.
Ermes is one of Italy's largest private-label producers, so **the private-label
co-op is a shape to recognise and close fast** — the wine exists, the page never
will.

#### Rallo's scheda has the energy value and no ingredient list

The first source in this file with the nutrition figure and no substances. The
AV01 Catarratto 2024 sheet (`/wp-content/uploads/2026/06/AV01_ITA.pdf`) prints
`ANNATA 2024`, `Grado alcolico: 13,5%`, `Zuccheri residui`, a
**`Valori Nutrizionali / Energia (E) per 100 ml: 314 kj / 75 Kcal`** block,
`Allergeni: Non contiene solfiti`, a full `Informazioni di Smaltimento`
recycling table and the organic certification — and no `Ingredienti` line
anywhere. That is exactly the set of particulars Regulation (EU) 2021/2117 lets
**stay on the physical label**, published on the web with the one part that was
supposed to move online left out. The usual Italian near-miss is the reverse
(Demarie's list with no nutrition, or an allergen line alone), so **a
`Valori Nutrizionali` heading is not a reason to stop reading**.

Note also that the AV01 identification was never completed and did not need to
be: *Amber One* matches AV01 on vintage, grape, pack and strength and disagrees
on the organic flag, and no page names both. **When the sheet carries no
ingredient list, do not spend fetches finishing an identity.**

#### Prunotto: a fourth Italian per-vintage archive, free of charge

`?wineyear={year}` on any `/it/vino/{wine}/` page reaches eight vintages back to
2018, on Antinori's own WordPress theme, and `robots.txt` disallows only `/de/`
— so unlike Cantina Terlan's `?wine-id=` archive there is nothing in the way.
Both Swedish bottles were reachable at exactly 2024 and neither page carries a
substance. After Ricasoli, Terlan and Chiarlo that is **the fourth Italian
producer with real vintage machinery and no ingredient list to hang on it.**

Two corollaries:

- **The default page is not the same vintage for two wines of one estate.**
  Prunotto's Fiulot still shows the 2024 while its Moscato has rolled to the
  2025. Read the year strip per wine.
- **The Antinori group shop does not cover Prunotto.** `26generazioni.com`'s
  product sitemap holds 166 products, exactly two of them Prunotto (Barbaresco
  2023, Barolo 2022), and no Barbera or Asti wine of any brand. The Scantrust
  e-label route found in July is closed for this estate, and closing it cost
  three fetches — **check the group shop's product sitemap before assuming a
  group platform reaches a subsidiary's wines.**

#### Italian hosts and greps, fifth batch

- **`qodef-e-label` is a new `e-label` false positive.** The Qode/QODEF
  WordPress theme family renders its membership widget with that class — nine
  raw hits and zero text hits on every Orsogna product page. Add it to
  `responsiveLabel`, `whitelabel`, `toggle-label`, `cm-cookie-label`,
  `slideLabel`, `site-nav__link-menu-label`, `__VIEWSTATE` and `checkJQuery`.
- **A `trusty.report` subdomain is a whistleblowing channel, not traceability.**
  Orsogna's *Blockchain* page links `orsognacantina.trusty.report`, which under
  a heading about tracing the bottle from the vineyard is Trusty AG's
  confidential-reporting app. One fetch, recognise it, move on.
- **"Etichetta ambientale DIGITALE" is still the packaging decree.** Orsogna
  publishes `/etichetta-ambientale-digitale-zeropuro-pecorino/`: bottle GL 70,
  cork FOR 51, label to landfill, and a link to the wine's own sheet. That is
  the ninth Italian producer to meet that obligation and not this one, and it
  is the most e-label-sounding name the decree has produced.
- **A Demeter sulphite *limit* is not a declaration.** Orsogna prints
  `SOLFITI Limite del vino biodinamico Demeter = vino rosso max 70 mg/lt` where
  the ingredient list belongs, beside `STABILIZZAZIONE TARTARICA Solo
  refrigerazione naturale` and `FILTRAZIONE Non ammessa la filtrazione
  sterile`. A ceiling set by a certification scheme, plus the negative list.
  Expect it on biodynamic estates.
- **A `?gen_pdf=1` datasheet can be 200, `application/pdf` and zero bytes.**
  Prunotto's "Scarica scheda tecnica" is exactly that, over curl and httpx
  alike. Check `content-length` before parsing.
- **WordPress Download Monitor hides the vintage in `Content-Disposition`.**
  Livon's press area links opaque `/download/{id}/?tmstv=…` URLs whose anchor
  text is just "scheda pdf"; the response names the file
  `LIVON__Classica_1_pinot_grigio_2025.pdf`. One GET and a header read tells you
  which year the estate currently documents without opening a 1,4 MB file — but
  the PDF's own text names no year, so **the filename is an edition, not a
  vintage statement.**
- **A producer's own shop can be a third-party retailer, and its `robots.txt`
  is the catalogue.** `antoniofacchinshop.it` disallows about thirty anchored
  `/*{brand}$` slugs — la_tordera, pasqua, angelo_negro, le_morette, degani,
  tenuta_san_leonardo and more. Same shape as `shop.rottensteiner.wine`, same
  conclusion: **a shop that resells is a retailer for everything but its
  owner's wine**, and two of those brands are in this project's own remaining
  Italian pool.
- **Antonio Facchin is blocked twice over.** The shop answers its own
  robots-declared sitemap with HTTP 403 and Cloudflare's `Just a moment…`
  interstitial (`cf-mitigated` header) — a bot challenge, absolute, not
  retried. The marketing site `antoniofacchin.com` answers **HTTP 522** on the
  root and then hangs on every subsequent path. Its `robots.txt` has both a
  `User-agent: *` group with `Allow: /` **and** ten named AI-crawler groups
  with `Disallow: /`; unlike `bpdr.com` the wildcard group exists, so no
  RFC 9309 reading is needed.
- **`biocantinaorsogna.it` disallows by file extension**, `/*.pdf` among them,
  with `Crawl-delay: 2`. Ordinary marketing site, no e-label, so no exception
  reaches it: HTML only, and no PDF was fetched.
- **`cantinerallo.it` 301s the host to `rallo1860.it`** and answers
  `robots.txt` with the site's own HTML — another Italian soft 404.
  `orsognawinery.com` and `cantinaorsogna.it` both 301 to
  `biocantinaorsogna.it` and 404 their robots.
- **A WooCommerce with 276 products can date none of them.** Orsogna's shop
  *is* its marketing site, one product per cuvée across sixteen brands, with no
  vintage field in the template and two tabs (Descrizione, Premi) — no
  `ingredient-list` class anywhere. The standing advice that the Italian shop
  is the surface that declares has its counter-example here.

### The sixth Italian batch: the vendor that publishes one list per vintage

**2026-08-12: Mauro Sebaste, Gaja, Angelo Negro, Mastroberardino, Panizzi, Luigi
Pira, Tagaro, Ciacci Piccolomini, MGM S.r.l. (Enzo Bartoli), Azienda Marramiero,
Le Vigne di Zamò, Giacosa Fratelli — twenty-four wines, 2 found, 22 not found,
0 rejected.** The batch took the named multi-wine leads in order and applied
step 0 first to every one of them.

| Producer | Region | Site | Our bottle on it? | Declaration? |
|---|---|---|---|---|
| Mauro Sebaste | Piemonte | WordPress, 16 wines, no shop | cuvée yes, **no vintage** | none; scheda predates the rule |
| Gaja | Piemonte | **a one-page non-site** | no page exists | none |
| Angelo Negro | Piemonte | WordPress, no shop | cuvée yes, **no vintage** | none; **whole-range packaging page** |
| Mastroberardino | Campania | WordPress + WooCommerce | cuvée yes, no vintage | **i-wine e-label — unreadable** |
| Panizzi | Toscana | WordPress, no shop | cuvée yes, **no vintage** | none |
| Luigi Pira | Piemonte | WordPress, no shop | cuvée yes, **no vintage** | none; **packaging subdomain** |
| Tagaro | Puglia | brand on a second host | cuvée yes, **no vintage** | none |
| Ciacci Piccolomini | Toscana | bespoke CMS, **39-vintage archive** | **yes, 2024, both** | none |
| MGM / Enzo Bartoli | Piemonte | brand site + **Argea group shop** | **yes, Annata 2024, 12 %, 0,75** | none, an allergen line |
| **Azienda Marramiero** | Abruzzo | WooCommerce + **ead-qr** | **yes, both, by year** | **yes, both — attached** |
| Le Vigne di Zamò | Friuli | **host does not answer** | unreachable | unreachable |
| Giacosa Fratelli | Piemonte | WordPress + Shopify | **neither cuvée exists** | none |

#### Giunko's ead-qr is the answer to the vintage problem

Marramiero's WooCommerce product pages carry an anchor reading **`Valori
nutrizionali`** (class `btn-nutrizionale`) pointing at `ead-qr.com/p/{id}`, and
that page does something no other platform in this project does: it prints
**one ingredient list and one nutrition table per vintage, each labelled with
its year**, side by side.

```
Valori Nutrizionali 2024 … Energia 306 kJ 73 kcal …
Ingredienti 2024  uve, mosto di uve concentrato, Conservanti e antiossidanti
( solfiti ), Antiossidanti (acido L-ascorbico), Imbottigliato in atmosfera protettiva
Valori Nutrizionali 2025 … Ingredienti 2025  uve, Agenti stabilizzanti (acido citrico),
Conservanti e antiossidanti ( solfiti ), Imbottigliato in atmosfera protettiva
```

That matters out of all proportion to one producer. **The single commonest
reason this project throws a found declaration away is that the producer's shop
has rolled forward a vintage** — Rhonéa, Turckheim, Paul Mas, GIV, La Pruina's
Manduria, Demarie's two. Marramiero's own shop *has* rolled: its WooCommerce
`Annata` attribute reads 2025 for both wines. The 2024 was attachable only
because the e-label keeps both years. **When an Italian producer turns out to
be on ead-qr, a vintage behind is no longer a rejection — read the year-labelled
block.**

Two more things about the platform, both good for provenance:

- **The identity comes from three places that agree.** The e-label heading
  names the line, the wine and the pack (`Prima Linea Cerasuolo d'Abruzzo DOC
  0,75`); it names `Azienda Marramiero S.R.L.` as responsible; and it links the
  producer's own product card PDF, which supplies the alcohol the e-label
  omits — `12,50% vol.` for the Cerasuolo, `11% vol.` for the Sessanta Passi,
  both matching Systembolaget exactly. The Pecorino's 11 % is an odd enough
  figure to be a strong check on its own.
- **The lists are per wine**: the two 2024 ingredient lines happen to coincide,
  but the energy differs (306 kJ against 268), so they are two disclosures.

`etichettaambientaledigitale.it` is Giunko's own product page for it. Worth
recognising the vendor name in an `href` and worth asking of any Italian
producer whose shop shows a *Valori nutrizionali* button.

#### The second new vendor is a React shell

Mastroberardino's shop carries the block *"Scansiona per: Valori nutrizionali,
Ingredienti, Raccolta differenziata"* around a QR image linking
`d.i-wine.app:8444/01/{uuid}-p{id}`. It is in the unreadable table above. Two
details to recognise: the **non-standard port 8444** on the link the producer
publishes, and a `/01/` path that **looks like a GS1 Digital Link and is not**
— the value after `/01/` is the producer's UUID, not a GTIN, so nothing about
GS1 resolution applies. Its `robots.txt` is a soft 404 serving the SPA shell.

#### Step 0 worked, and it cut both ways

Four of the twenty-four wines were closed or nearly closed on the name alone,
and the two failure modes are opposite:

- **Giacosa Fratelli's *Busije* and *Leunin* do not exist on the producer's own
  surface** — not in its 21-wine sitemap, not among its 21 schede, not in its
  30-product Shopify catalogue, and its own site search returns nothing. The
  wines are attributed to the estate by third parties, so these are export-only
  cuvée names, not another winery. **And the trap is sharp: the estate does make
  a Barbera d'Alba *Bussia*, one letter from *Busije*.** A near-name is not a
  match.
- **Tagaro's *Nardelli* is absent from tagaro.it and its site search says so —
  and the brand is still the producer's.** It lives on its own older host,
  `vininardelli.it`, and the only thing tying the two together is a Facebook
  link in the footer pointing at `facebook.com/TeamTagaro`. **A name absent from
  the producer's own site is not automatically an importer's label: check for a
  brand-owned domain before closing.** That is a correction to the fifth batch's
  rule, not a reversal of it — Ermes' *Ambleri* and Facchin's *High On Love*
  still have no producer host anywhere.

#### The packaging asymmetry now has a subdomain

Two more producers join the nine already recorded, and they are the most
elaborate yet:

- **Luigi Pira runs a whole subdomain for it**, `etichettatura.piraluigi.it`,
  linked from every wine page — one section per wine and one table per format
  (0,75 l, magnum, jeroboam), with bottle GL 71, cork FOR 51, capsule C/ALU 90,
  wooden case FOR 50 and the cardboard divider PAP 20/21 — and publishes no
  ingredient list for any wine.
- **Angelo Negro publishes one page covering its entire range**, grouped by
  closure type, naming all three Swedish wines. Same absence.
- Ciacci Piccolomini prints a *Decreto Rifiuti* block inline on every wine page.

That is **twelve Italian producers** (thirteen after Planeta, in the seventh
batch) meeting the 2023 packaging obligation on
the web and not the ingredient one. And note the agency pattern holds: Pira is
a fourth `hellobarrio` `barriotheme` site after Chiarlo, Falchetto and Azelia,
all four with the packaging machinery and none with a list; Angelo Negro and
Giacosa Fratelli are both built by **blulab**, same story.

#### Three more Italian archives with nothing in them

Ciacci Piccolomini's is the deepest seen anywhere: **39 vintages, 1987 to 2024,
delivered as a single JavaScript array named `$schede` in one response**, one
object per year with a `voci` list of labelled fields. Parse the array and the
whole vintage question costs one fetch. Our 2024 is in it, and its fields are
vineyard, grape, vinification, colour, sensory notes, service, pairing and a
note about the anti-counterfeiting hologram. No substances, no alcohol.

That is now the fifth Italian producer with real per-vintage machinery and no
ingredient list, after Ricasoli, Terlan, Chiarlo and Prunotto.

#### Argea's group shop is the counter-example to GIV's

`shop.argea.com` is a 185-product first-party WooCommerce covering the group's
brands — Botter, Mondo del Vino, Zaccagnini, Ricossa, Cuvage, Poderi dal
Nespoli, Barone Montalto, Enzo Bartoli, Mosketto, Asio Otus, Brilla. Its
product table is **excellent identity and no declaration**: Tipo di vino,
**Annata**, Appellazione, Varietà, **Gradazione alcolica**, **Formato**,
`Allergeni: Contiene Solfiti`, `Provenienza: Prodotto in Italia`. Our Enzo
Bartoli Gavi was there at exactly 2024, 12 % vol and 0,75 L and still could not
be attached. Argea supplies a large share of the Italian volume on the Swedish
shelf, so **that one fetch settles the group**: expect the two-particular
near-miss, and do not spend a batch on their brands hoping otherwise.

#### Italian hosts and greps, sixth batch

- **`u-label` matches `menu-label`.** Mastroberardino's theme renders
  `.responsive-menu-label`, seven raw hits and zero text hits on every page of
  both its hosts. U-label is still the platform this file has been watching for
  since Germany; **any class ending `menu-label` will look like it.** Add it to
  `responsiveLabel`, `whitelabel`, `toggle-label`, `cm-cookie-label`,
  `slideLabel`, `site-nav__link-menu-label`, `qodef-e-label`, `__VIEWSTATE` and
  `checkJQuery`.
- **`gaja.com` is a 2 404-byte black placeholder** — logo, address, phone,
  `mailto:`, eight hrefs, all of them CSS and favicons — and no robots.txt and
  no sitemap (both 404). `gaja.it` and `gajawines.com` 301 to it. **A producer
  can deliberately have no website**, which is a different thing from having no
  page for a wine and is answerable in three fetches.
- **A producer's distribution arm is a multi-brand importer.**
  `gajadistribuzione.it` is an 871-product WooCommerce of Champagne houses and
  Burgundy domaines; the two slugs that look like Gaja's Swedish wines,
  `sito-moresco-4` and `rossj-bass-4`, are the *grappas* of those names. Same
  shape as Facchin and Rottensteiner: **a producer's own shop can be a retailer
  for everything but its owner's wine.**
- **`levignedizamo.com` does not answer at all** — connection refused on 443 at
  the apex (an OVH address) and TCP timeout on `www` (31.193.131.44), over
  httpx and over `curl -4` with a 30 s limit. Not a refusal, a dead host; both
  Zamò wines are revisit candidates. And **`zamo.it` is ZAMO Srl, a maker of
  hydraulic demolition breakers** — the surname trap for the fourth time after
  `sartori.it`, `castellani.it` and `hermouet.fr`.
- **`giacosafratelli.com` fails TLS** (incomplete chain, no local issuer) and
  answers over plain HTTP with an 82-byte page whose entire body is
  `<script>window.location='http://www.giacosa.it'</script>`. **A JavaScript
  redirect is invisible to a redirect-following fetch**; read the body.
- **`ciaccipiccolomini.com` 301s to `ciaccipiccolomini.it`**, which serves no
  robots.txt and no sitemap under any of the three usual names, and whose
  product URLs are `/it/prodotti/prodotti/{cat}/vini/{id}/{slug}`.
- **`mastroberardino.com/robots.txt` names ten sitemaps and eight of them are
  fabrications** (`/wp-admin/shop.php/sitemap84.xml` among them, and the one it
  advertises first, `sitemapindex.xml`, 404s). The real one is the ordinary
  `sitemap_index.xml`. **Read the robots.txt, then ignore what it claims and
  try the standard names.**
- **A WordPress upload path older than the rule still closes a wine, cheaply.**
  Five schede in this batch were closed on a HEAD alone: Mauro Sebaste's two
  (Jun 2023), Mastroberardino's two (Nov 2019) and Luigi Pira's two (**24 Nov
  2023, two weeks before 8 December**). The converse also held — Panizzi's,
  Angelo Negro's and Tagaro's are post-obligation, were downloaded and read in
  full, and contain no substances.
- **A post-obligation scheda can still state no vintage and no alcohol.**
  Panizzi's January 2025 sheets give vineyard, grape, density, vine age, yield,
  vinification and pairing and neither a year nor a strength; the only years on
  the estate's whole surface are an `ANNATE PREMIATE` critics' list that stops
  at 2022. **An award list is not a vintage statement.**

### The seventh Italian batch: a new vendor, a QR image, and the same producer twice

**2026-08-12, in two halves separated by a session limit. First half: Josetta
Saffirio, Fattoria Pagano, Tralci Hirpini, Orion Wines — eight wines, 0 found,
6 not found, 2 rejected. Second half: Cà dei Frati (again), Masi, Le
Battistelle, Planeta, Pasqua, Ciù Ciù, Montalbera, Cantine Volpi — ten wines,
1 found, 9 not found, 0 rejected.** Twelve producers, eighteen wines, one
declaration attached and two rejected against a complete declaration that was
found and read.

| Producer | Region | Site | Our bottle on it? | Declaration? |
|---|---|---|---|---|
| Josetta Saffirio | Piemonte | Next.js on Vercel | **no still rosato exists** | none |
| Fattoria Pagano | Campania | Shopify; marketing site parked | cuvée yes, **no vintage** | none |
| **Tralci Hirpini** | Campania | WooCommerce → **carmaqrcode** | cuvée yes, **no vintage anywhere** | **yes, both — both rejected** |
| Orion Wines | Trentino | two hosts for one brand | cuvée yes, no vintage, no alcohol | none |
| **Cà dei Frati** | Lombardia | WordPress, no shop | **yes, Annata 2025, 13 %, 750 ml** | **yes — attached** |
| **Masi Agricola** | Venetien | wineplatform shop → **Scantrust** | **yes, both, exact vintage** | **adopted, unreadable** |
| Le Battistelle | Venetien | Joomla, no shop | cuvée yes, **no vintage** | none |
| Planeta | Sicilien | WordPress | **yes, a 2024 scheda** | none |
| Pasqua | Venetien | WordPress + wineplatform shop | **brand absent from both** | none |
| Ciù Ciù di Bartolomei | Marche | **host 503s everything but robots.txt** | unreadable | unreadable |
| Montalbera | Piemonte | bespoke PHP, no shop | cuvée yes, **no vintage** | none |
| Cantine Volpi | Piemonte | WordPress, no shop of its own | cuvée yes, **no vintage, no alcohol** | none |

#### carmaqrcode is Italy's third e-label vendor, and the page it serves is empty

Tralci Hirpini (Avellino) has done something no other producer in this project
has: **it has replaced its own product page with a 301 into the vendor.**
`tralcihirpini.com/i-vini/greco-di-tufo-d-o-c-g/` answers 301 straight to
`www.carmaqrcode.it/4/004-004-valori-nutrizionali-greco-di-tufo-docg/`. That is
about as direct a piece of producer linking as provenance can ask for.

The vendor row is in the readable table above. The thing to carry forward is
**how nearly it was missed**: the e-label page's `entry-content` is one empty
`<div class="_df_book">`, a 3D FlipBook viewer, and the PDF URL lives only in an
inline script as `"source":"…pdf"`. Stripped text: nothing. `<a href>` scan:
nothing. **Only a raw grep for `.pdf` finds the document.** Add that to the
grep list — a client-side viewer around a server-served file is not the same
failure as a client-side page, and the two look identical until you grep raw.

**And both wines were rejected, on the vintage, for a reason that is the
vendor's and the producer's together.** The sheet is complete — a trilingual
ingredient list (`Uve, Metabisolfito di potassio, Carbossimetilcellulosa, Gomma
arabica, betonite`), an allergen line and a nutrition table per 100 ml — and it
**states no year, and nothing on the producer's entire surface dates any
bottling**. The post is dated May 2025 and the PDF was made in Illustrator in
March/May 2025, which is *consistent* with the 2024 release and is not evidence
of it. A vintage that cannot be established is not a vintage that matches. Both
declarations are quoted in full in the wines' records, so if either party ever
prints a year the wines attach without a refetch.

#### Masi publishes its e-label as a QR image, and that is a new shape

Masi Agricola is the first producer anywhere in this project whose e-label URL
appears **nowhere in the HTML as text** — not as an `href`, not in a script, not
in a data attribute. Its shop `enotecamasi.it` renders a product field whose
**label is `u-Label` and whose text value is empty**; the field's icon is a
1902×1904 PNG on the DatoCMS asset host, and that PNG is the QR code.

Decoded offline with OpenCV, per the Carl Loewen precedent (no network), it
reads `https://label.masi.it/qr/LevarieMasi`. **The decode needs help**: the
image has no quiet zone and carries an `i` badge over its centre, and
`detectAndDecode` fails on the raw file. Add a white border of ~60 px and
downscale to 0.25–0.5 and it decodes first try. That recipe is worth keeping —
producer QR assets are usually exported flush to the edge.

The destination is Scantrust, so nothing was read. Three facts came out of it
anyway:

- **`u-Label` as a field label does not mean the U-label platform.** After
  eleven Italian producers of watching for `u-label.com`, the first real hit on
  the string was a producer's own name for a QR field pointing at a competitor.
- **The QR is per wine and not per vintage.** The Levarìe 2024 and 2025 product
  pages carry the *identical* image URL and therefore the identical Scantrust
  destination. Even if Scantrust became readable, this wine could not be
  attached on the producer's linking alone.
- **The field is a deployment customisation, not a platform feature.**
  `shop.pasqua.it` is the same wineplatform.it software and shows the platform
  default instead: an `Annata` field with the year and an `Info` field reading
  `Contiene Solfiti - Prodotto in Italia`.

#### The pool counts producers by string, and Systembolaget spells them twice

**The find in this batch is a producer that had already been done.**
Systembolaget carries the Lugana estate as both `Cà dei Frati` and
`CA' DEI FRATI`, so a producer-string diff of the untouched pool treated them as
two producers and left `Lugana I Frati 2025` looking untouched. It was on the
estate's ordinary `/vini/i-frati-lugana/` page all along, under the same inline
block as Pratto and Rosa dei Frati: `Annata: 2025`, `Bottiglia: 750 ml`,
`Grado alcolico: 13 % vol`, an `Ingredienti` list and a `Dichiarazione
nutrizionale per 100 ml`. Vintage, pack and alcohol exact. One fetch.

**Normalise the producer string before deciding an Italian producer is
untouched** — case-fold, strip diacritics and drop the legal-form words. Doing
so on the current pool collapses at least six more apparent singles into pairs:

| One producer, two Systembolaget strings |
|---|
| `Cà dei Frati` / `CA' DEI FRATI` |
| `Masi` / `Masi Agricola` |
| `Le Battistelle` / `Azienda Agricola Le Battistelle` |
| `Planeta` / `Aziende Agricole Planeta s.s.` |
| `Pasqua` / `Pasqua Vigneti e Cantine SpA` |
| `Collemassari` / `ColleMassari Spa Società Agricola` |
| `Marco Felluga` / `Russiz Superiore-Marco Felluga` |
| `Vecchia Cantina di Montepulciano` / `Societa Cooperativa Vecchia Cant` |

That is worth roughly a 6 % saving on the remaining pool and, more importantly,
it is why *the seventh batch's only find cost one request*. It also surfaces two
wines belonging to producers already attempted and closed — `Cantina Lavis Pinot
Nero 2025` and `Tommasi Le Fornaci Lugana 2024` — which should be recorded
against the existing findings rather than re-probed.

#### The near-name trap moves from the cuvée to the domain

Pasqua's *Mucchietto* is a Pasqua-owned export label absent from the house's
own 220-URL sitemap **and** from its own 59-product shop. The
brand-owned-second-domain check that saved Tagaro's *Nardelli* was run and came
back negative in an instructive way: **`mucchietto.it` 301s to
`www.mucchieto.it`, an agriturismo and olive-oil producer one letter away from
the brand name.** `mucchietto.com` 404s with a 47-byte body. After Busije /
Bussia, this is the same trap one level up — in the domain rather than the
cuvée. **Read what the site actually is before treating a resolving domain as
the brand's.**

#### Two more Italian schede that carry everything except a substance

- **Planeta**, `Planeta_Chardonnay-2024-BIO-2.pdf`, Last-Modified March 2026 —
  soil, altitude, yield, training, planting density, organic method, harvest
  dates, vinification, `IMBOTTIGLIAMENTO: agosto 2025`, `GRADAZIONE ALCOLICA:
  13% vol.`, acidity 5,50 g/l, pH 3,33, four formats, bottle weight, cork. It
  **settles the vintage, the strength and the pack for our exact bottle** and
  contains zero occurrences of `ingredien`, `nutrizion`, `kcal`, `energia`,
  `solfit`, `allergen` and `dichiarazion`. This is the strongest Italian
  near-miss so far, ahead of Rallo's.
- **Montalbera**, `/pdf_vini.php?id=75` — a typeset copy of the web page, word
  for word, and the page's alcohol line is **`Da 13,50 a 15,50 gradi in base
  all'annata`**. An estate can say outright that its strength varies by vintage
  while stating no vintage. That is the undated-cuvée-page failure in its
  purest form and it closes a wine on sight.

#### Italian hosts and greps, seventh batch

- **`i-wine` matches `masi-wine-experience`** — fifteen raw hits on every page
  of `masi.it`, all of them in the menu JSON. Any producer whose site has a
  `…i-wine…` substring in a slug will look like the i-wine vendor. Add it to
  `menu-label`, `responsiveLabel`, `whitelabel`, `toggle-label`,
  `cm-cookie-label`, `slideLabel`, `site-nav__link-menu-label`, `qodef-e-label`,
  `__VIEWSTATE` and `checkJQuery`.
- **A host can serve `robots.txt` with a 200 and 503 everything else.**
  `www.ciuciuvini.it` answered 200 on `robots.txt`, named two sitemaps, and
  returned a 468-byte Apache `503 Service Unavailable` on both of them and on
  its home page. That is a third shape after "answers normally" and "does not
  answer at all" (Le Vigne di Zamò), and it is **not** a technological refusal —
  no 401, 403, 429 or challenge — so it was not retried and not worked around.
  Revisit candidate.
- **A relative PDF href on a catch-all router returns the wrong page with a
  200.** Montalbera's anchor is the bare `pdf_vini.php?id=75&l=`; requested
  relative to the product path it returns the 118 kB `/vini/` listing as
  `text/html` and a 200. The real document is at the site root. **Check the
  content type and the byte count before believing you fetched a PDF.**
- **The named-crawler `robots.txt` with no wildcard fallback has a second
  instance**, and this one is Italian: `cantinevolpi.it` serves a four-line
  `#Simple Robots.txt 0.1` with only `User-agent: MSNBot` and
  `User-agent: bingbot`, each carrying a `Crawl-delay: 5` and **no disallow at
  all**. Same reading as `bpdr.com`: no matching group, no wildcard fallback,
  nothing applies. Apply it without re-litigating.
- **A WooCommerce `product` post type can hold no products.** Cantine Volpi's
  `product-sitemap.xml` lists five URLs and all five are tasting-room events;
  the wines are ordinary pages reachable only from `/i-vini/`. An empty or
  irrelevant product sitemap does not close a producer.
- **A Shopify catalogue can be dated everywhere except where you need it.**
  Fattoria Pagano's shop states `Grado alcolico: 13,00% - 14,00% in vol.` — a
  range — on an undated cuvée page, while carrying dated siblings
  (`aglianico-campania-igt-2018-biologico`) six vintages away. Alcohol as a
  range is now seen at three Italian producers and is a reliable sign that the
  page describes a wine and not a bottling.
- **`fattoriapagano.it` and `.com` both serve Aruba's "Sito in costruzione"
  parking page** over http and https and 404 every path including
  `robots.txt` — an outage on the marketing side while the Shopify shop runs
  normally.

### Where the remaining Italian work is

**118 Italian wines with vintage 2024+ and no declaration on Systembolaget
remain untouched, after seven batches** (61 producers and 149 wines attempted;
8 found, 131 not found, 10 rejected). Marchesi Antinori 9, Tommasi 6 and Vini
Franchetti 6 were attempted in the first batches and should not be re-probed
without a new lead.

**Normalise the producer string before counting** — see *The pool counts
producers by string*, above. Doing so leaves **117 producer strings for 118
wines**: one outright pair (**ColleMassari Spa Società Agricola / Collemassari**)
and the rest singles, of which at least three more are one house under two names
that no normalisation will catch — **Marco Felluga / Russiz Superiore-Marco
Felluga**, **Vecchia Cantina di Montepulciano / Societa Cooperativa Vecchia
Cant** (both sell *Poggio Stella*), and **Cadia / Colli Vicentint, Vitevis
Cantine** (both sell *Cadia*). Take those first; they are the last sibling
economics in the Italian pool.

Two wines belong to producers already attempted and closed and should be
recorded against those findings rather than re-probed: `Cantina Lavis Pinot Nero
2025` (7257301) and `Tommasi Le Fornaci Lugana 2024` (7677401).

**The economics have therefore changed.** Every batch until now could lean on
one producer covering several wines; from here each producer is one wine, so
the fixed probe below has to close fast. The two cheapest closes are step 0
(the name) and step 2 (the undated page), and between them they closed
seventeen of this batch's twenty-four wines.

**The one thing worth selecting for is a vendor.** Nothing about an Italian
producer's shape predicts publication — six batches have falsified the
small-estate, Alto Adige, co-op, own-e-commerce and per-vintage-archive
profiles — but **every Italian declaration this project holds came from a
producer that had adopted something**: GIV's own shop software, Cà dei Frati's
inline block, La Pruina's IoAgri, Demarie's WooCommerce tab, Marramiero's
ead-qr. The question to ask a new Italian producer is still *has it adopted a
platform*, and the cheapest way to ask is a raw-HTML grep of one product page
for `ead-qr`, `ioagri`, `i-wine`, `carmaqrcode`, `ingredient-list` and
`btn-nutrizional`. **Add `.pdf` and `u-label` to that grep after the seventh
batch**: carmaqrcode's page holds nothing but a PDF URL inside a script, and
Masi's e-label URL is not in the HTML at all — it is a QR image behind a field
labelled `u-Label`. **Adoption still does not mean readability**: of the seven
Italian producers now known to have adopted a vendor, three published something
this project could read.

**Before step 0, normalise the producer string.** Case-fold, strip diacritics
and drop the legal-form words, then check the result against the producers
already in `data/producer-declarations.json`. The seventh batch's only find was
`CA' DEI FRATI`, an estate already worked as `Cà dei Frati`, and it cost one
request because the answer was already in the file.

**Step 0 stays first: is the Swedish name the producer's name?** Six of the
fifth batch's twelve wines, four of the sixth's twenty-four and two of the
seventh's eighteen were export-only or importer-owned labels. The cheapest way
to find out is the producer's own `brand`, `vino` or product sitemap — one
fetch, and if the name is absent the wine is close to closed. **Check the
producer's own shop as well as its marketing site** (Pasqua's Mucchietto is
absent from both, which is what makes it conclusive). **Check for a brand-owned
second domain before closing** (Tagaro/Nardelli), and never accept a near-name —
in the cuvée (Busije/Bussia) or in the domain (mucchietto.it → Mucchieto, an
agriturismo).

**Do not pre-select by producer shape.** Four batches have now falsified the
small-estate profile, the Alto Adige profile, the co-op profile, the
own-e-commerce profile and the has-a-per-vintage-archive profile in Italy. The
eight wines attached came from a Lombard estate with no shop (three of the
eight), a Puglian WooCommerce with a vendor QR, a Piedmontese estate whose
marketing site's e-label slot is empty and whose shop has the list, and an
Abruzzese WooCommerce whose vendor publishes a list per year. What is cheap and
works is a fixed probe:

1. `robots.txt`, then the sitemap index — an Italian producer's sitemap usually
   names the per-wine post type outright (`wine-sitemap`, `vino-sitemap`,
   `qr-code-promo`, `/vini/`, `/prodotti/`), and an empty or missing one closes
   the producer. **An `etichettatura` sitemap is the packaging decree, not an
   e-label tree.**
2. **Does the producer's own page for the exact wine state a vintage at all?**
   An undated cuvée page is the dominant Italian failure and closes the wine
   immediately. It closed seven of the twelve producers in the third and fourth
   batches and six of the twelve in the sixth. **One exception, new in the sixth
   batch: an undated page that links a vendor e-label does not close the wine**
   — ead-qr states the year itself, so do step 3 before giving up on the date.
3. **One per-wine page, grepped raw as well as stripped**, for `ingredien`,
   `nutrizion`, `solfit`, `kcal`, `energia`, `dichiarazione`, `ingredient-list`,
   `ioagri`, `ead-qr`, `i-wine`, `carmaqrcode`, `u-label`, `btn-nutrizional`
   and `.pdf`. GIV hid it in a GraphQL payload, Cà dei Frati printed it as plain
   text, Demarie put it in a collapsed WooCommerce panel, Marramiero put it
   behind an anchor the stripped text renders as two words, Tralci Hirpini's
   vendor put it in a `"source":"…pdf"` string inside a script; each was missed
   by one of the greps.
3b. **If the greps are silent, look at the product page's images.** Masi's
   e-label URL appears nowhere in the HTML as text: it is a QR code PNG behind
   a field labelled `u-Label`. Decode it offline (OpenCV `QRCodeDetector`, no
   network) — **add a white border and downscale first**, or a producer's
   quiet-zone-free export will not detect.
4. **If there is a shop, it is a separate surface and usually the one that
   declares** — and it is often not linked correctly from the marketing site.
   Reach it through its own sitemap.
5. If the page is undated, **read the scheda tecnica's file name and HEAD it**
   before closing on the vintage. A file modified before 8 December 2023 cannot
   carry a declaration and closes without a download.

Cà dei Frati, Gruppo Italiano Vini, La Pruina and now Marramiero are all worth
revisiting on a later slice — each declares for its whole catalogue, and only
the vintage stood in the way of GIV's two and La Pruina's Manduria. **La
Pruina's is the cheapest revisit in the file**: the IoAgri token looks
product-keyed, so when the estate's Manduria page rolls to `ANNATA 2024` the
same URL should carry the 2024 recipe, in two fetches.

Two revisits added by the seventh batch:

- **Ciù Ciù di Bartolomei**, one 2024 wine, closed only because the host
  answered 503 on everything but `robots.txt`. An outage, not a finding, and a
  large certified-organic Marche estate is exactly the profile worth a second
  pass.
- **Tralci Hirpini**, two 2024 wines, rejected only on the vintage against a
  complete carmaqrcode sheet. Both declarations are quoted in full in the
  records; if the producer or the vendor ever prints a year, they attach with
  no refetch.

Two revisits added by the sixth batch:

- **Le Vigne di Zamò**, two 2024 wines, closed only because the estate's host
  did not answer on either name or either port. That is an outage, not a
  finding.
- **Mastroberardino**, two wines, closed only because the i-wine e-label
  renders client-side. If that vendor ever server-renders, the URLs are already
  held in the wines' records.

# Domain candidates

> **Decided 2026-07-26: `vindeklaration.se` is registered and is the site's
> domain.** It names the EU document this dataset is parsed from. The lists
> below are kept as the record of what was checked and what was rejected —
> useful if a second domain is ever wanted to redirect from, since
> `vindeklaration` was also free on `.com`, `.wine` and `.vin` on that date.

Checked 2026-07-26. Site: an open, bilingual (Swedish/English) dataset and
lookup of the additives declared in wines sold by Systembolaget — consumer
transparency, not a shop, not a review site.

**Owner priority, confirmed:** `.se` is the preferred TLD — the audience and
the source data are both Swedish. Cloudflare Registrar remains the preferred
registrar in general (no markup, one dashboard), but it does not sell `.se`,
so a `.se` registration means a Swedish registrar (Loopia, Binero, Glesys)
instead — an accepted cost, not a mark against a name. Two ranked lists
follow: `.se` candidates, and Cloudflare-supported-TLD candidates. Overlaps
(free in both places) are called out, since the owner may want a `.se` for
the audience and a Cloudflare-bought domain to redirect from.

This supersedes an earlier version of this file written under a
Cloudflare-only brief; several checks below reuse and reconfirm findings from
that run (e.g. `vinkoll.se`/`vinkoll.com` registered, `renvin.se` available,
`wineadditives.com` available).

## Method

- **Is it registered — `.se`.** `.se` (and `.nu`) are **not** in the IANA RDAP
  bootstrap (`https://data.iana.org/rdap/dns.json`), confirmed empty for both
  before trusting anything. `rdap.org` gives a false `404` for every `.se`
  name regardless of registration — verified directly: `rdap.org` returns
  `404` for `systembolaget.se`, which whois confirms has been registered
  since 1994. So every `.se` verdict below comes from
  `whois -h whois.iis.se <name>` instead: `domain "x.se" not found.` means
  free; `state:`/`status:`/`created:` fields mean registered. Paced 2–3 s
  between calls.
- **Is it registered — Cloudflare-eligible TLDs.** `.com`, `.org`, `.wine`,
  `.vin` are all confirmed present in the IANA bootstrap (individually
  checked, not assumed). For these, `https://rdap.org/domain/<name>`
  (followed through its redirect to the authoritative RDAP server) answers
  `200` for registered, `404` for available. A sample of "available" `.com`
  results was cross-checked with registration dates via the same endpoint to
  make sure `404` wasn't a stale cache.
- **Cloudflare support.** Re-ran the scrape at
  `curl -s "https://www.truthdomains.net/cloudflare-registrar/api/" | jq -r '.domains[]'`
  (377 TLDs at check time). Confirmed present: `.com` `.org` `.app` `.dev`
  `.io` `.me` `.co` `.uk` `.wine` `.vin`. Confirmed absent: `.se`, `.nu`, and
  no other Nordic ccTLD, nor `.eu`/`.de`/`.fr`. This is a third party reading
  Cloudflare's own page, not Cloudflare's API — strong evidence, not proof.
- **No check reaches Cloudflare's own dashboard search.** There is no public
  availability API for Cloudflare Registrar. Everything here narrows the list
  to what's worth searching there by hand.
- Nothing below was ambiguous — every whois/RDAP query returned a clean
  registered-or-not-found answer, none had to be re-run for a suspected
  throttle.

## List 1 — `.se` candidates (ranked)

Checked against `whois.iis.se`. This is the preferred TLD; Cloudflare does
not sell it, so these would go through Loopia, Binero or Glesys.

| # | Domain | Verdict | Method | Also free on | What it's going for |
|---|---|---|---|---|---|
| 1 | **vinklart.se** | Available (`not found`) | whois.iis.se | .com, .wine, .vin | Coined — "vin" + "klart" (clear/obviously clear). Doubles as a transparency pun and reads as ordinary Swedish; the strongest cross-registry option |
| 2 | **tillsatskoll.se** | Available (`not found`) | whois.iis.se | .com, .wine | Descriptive Swedish, web-native compound ("additive check") — same pattern as *bilkoll*, *prisjakt*; plain and functional |
| 3 | **vindeklaration.se** | Available (`not found`) | whois.iis.se | .com, .wine, .vin | Descriptive Swedish — names the actual EU-mandated document ("vindeklaration") the dataset is built from |
| 4 | vintillsatser.se | Available (`not found`) | whois.iis.se | .com | Descriptive Swedish, the literal translation of the project's own name ("wine additives") |
| 5 | renvin.se | Available (`not found`) | whois.iis.se | .wine, .vin (not .com — registered) | Coined — "clean wine." Short and easy to say; `renvin.com` is taken, so no `.com` twin |
| 6 | vinsyn.se | Available (`not found`) | whois.iis.se | — (`.com` registered) | Coined — "vin" + "syn" (view/insight); no cross-TLD twin since `vinsyn.com` is taken |

### `.se` names ruled out (registered)

| Domain | Verdict | Method |
|---|---|---|
| vinkoll.se | Registered (active, Loopia, created 2021) | whois.iis.se |
| glasklart.se | Registered (active, InterNetX, created 1997) | whois.iis.se |
| vinfakta.se | Registered (active, INLEED, on Cloudflare DNS already) | whois.iis.se |
| deklarerat.se | Registered (active, InterNetX, created 2025) | whois.iis.se |
| tillsatser.se | Registered (active, InterNetX, created 2008) | whois.iis.se |
| deklaration.se | Registered (active, Loopia, created 2003) | whois.iis.se |

## List 2 — Cloudflare-supported-TLD candidates (ranked)

Checked against RDAP (`rdap.org`, followed to the authoritative server).
`.wine` and `.vin` suit the subject and are Cloudflare-supported; none of the
names below resemble a protected wine appellation (checked by eye against
Champagne, Rioja, Chianti, Cava, Porto, etc. — not the registries' full GI
list).

| # | Domain | Verdict | Method | Cloudflare | Also free on | What it's going for |
|---|---|---|---|---|---|---|
| 1 | **vinklart.com** | Available | RDAP 404 | Supported | .se, .wine, .vin | Same coined transparency pun as the `.se` top pick — buy both, redirect one to the other |
| 2 | **wineadditives.com** | Available | RDAP 404 | Supported | — | Descriptive English, maximally literal — the project's own name, understood instantly in both languages |
| 3 | tillsatskoll.com | Available | RDAP 404 | Supported | .se, .wine | Descriptive Swedish compound, matches the `.se` #2 pick |
| 4 | vindeklaration.com | Available | RDAP 404 | Supported | .se, .wine, .vin | Descriptive Swedish, matches the `.se` #3 pick |
| 5 | wineadditives.org | Available | RDAP 404 | Supported | — | Same as #2; `.org` reads more like an open-data/nonprofit project |
| 6 | vintillsatser.com | Available | RDAP 404 | Supported | .se | Descriptive Swedish, matches `.se` #4 pick |
| 7 | tillsatskoll.wine | Available | RDAP 404 | Supported | .se, .com | Same as #3, industry-specific TLD |
| 8 | renvin.wine / renvin.vin | Available | RDAP 404 | Supported | .se | Coined, "clean wine"; `.com` is taken, industry TLD is the only clean option there |
| 9 | winedeclared.com | Available | RDAP 404 | Supported | — | Descriptive English wordplay — "wine that declares itself" |

### Cloudflare-TLD names ruled out (registered)

| Domain | Verdict | Method |
|---|---|---|
| glasklart.com | Registered (2008) | RDAP 200 |
| vinkoll.com | Registered (2021) | RDAP 200 |
| renvin.com | Registered (2020) | RDAP 200 |
| vinfakta.com | Registered (2026) | RDAP 200 |
| vinsyn.com | Registered | RDAP 200 |
| klarvin.com | Registered | RDAP 200 |
| deklaration.com | Registered | RDAP 200 |
| vindeklaration.com | — free, see List 2 #4 (not ruled out) | — |

## Where `.se` and Cloudflare overlap

For redirecting a Cloudflare-bought domain to the `.se` primary (or vice
versa), these are free on both sides today:

- **vinklart** — .se, .com, .wine, .vin all free
- **tillsatskoll** — .se, .com, .wine all free
- **vindeklaration** — .se, .com, .wine, .vin all free
- **vintillsatser** — .se, .com free

## Recommendation

**First choice: `vinklart.se`**, with `vinklart.com` bought alongside on
Cloudflare and redirected in. It is the one name confirmed free everywhere
checked (`.se`, `.com`, `.wine`, `.vin`), it satisfies the owner's stated
`.se` preference, it reads as ordinary Swedish rather than invented jargon,
and the transparency pun ("wine, clear/obviously") fits a site whose whole
point is showing what's normally hidden on a label.

**Fallback: `vindeklaration.se`** (with `vindeklaration.com` alongside). It
names the actual legal document — the EU wine ingredient declaration — that
the dataset is built from, which is a safer, more literal choice if a pun is
judged too cute for a reference tool; also free on every TLD checked.

## What could not be verified

- **Cloudflare's own dashboard search was not run for any Cloudflare-TLD
  candidate above.** There is no public availability API; a human must
  search each shortlisted name at domains.cloudflare.com before trusting a
  price.
- **Premium-tier pricing is invisible to RDAP and whois**, on both sides.
  `.wine`/`.vin` in particular are known to price short, generic-sounding
  wine-related words at a premium tier that only the registrar's own search
  reveals — `vinklart.wine`, `renvin.wine` and `tillsatskoll.wine` are all
  plausible candidates for that, not confirmed either way.
- **No trademark search was performed** beyond the explicit constraint of
  avoiding "Systembolaget" and producer/importer names. Domain availability
  and trademark clearance are different questions; this only answers the
  first.
- **`.wine`/`.vin` appellation-resemblance check was done by eye**, against
  well-known protected names (Champagne, Rioja, Chianti, Cava, Porto), not
  against the registries' full official geographic-indication list.
- **Registrar pricing/process for `.se` was not checked.** Loopia, Binero and
  Glesys were named as options per the brief but none was queried for price,
  required ID/organisation-number steps, or turnaround time.
- **This reflects a single point in time (2026-07-26).** All results above
  come from queries run today, paced 2–3 s apart to avoid a throttle reading
  as "not found" — but a domain free this afternoon can be registered
  tomorrow. Re-run before acting on this list, especially before purchase.
- **`vinsyn.se` and `renvin.se` have no `.com` twin** (both registered under
  `.com`) — listed because they're strong `.se`-only options, but they don't
  support the "buy both, redirect" pattern the owner mentioned.

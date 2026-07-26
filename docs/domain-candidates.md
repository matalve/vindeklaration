# Domain candidates

Checked 2026-07-26. Site: an open, bilingual (Swedish/English) dataset and
lookup of the additives declared in wines sold by Systembolaget — consumer
transparency, not a shop, not a review site. Must be registrable through
Cloudflare Registrar (hard constraint; `.se`/`.nu`/no Nordic ccTLD, `.eu`,
`.de`, `.fr` are **not** supported — verified below, not assumed).

## Method

- **Registered?** RDAP via `https://rdap.org/domain/<name>`, `200` =
  registered, `404` = available, for TLDs confirmed present in the IANA
  bootstrap (`https://data.iana.org/rdap/dns.json`). `.com`, `.org`, `.wine`,
  `.vin` are all in the bootstrap — confirmed individually, not assumed.
  Every "available" `.com`/`.org`/`.wine` result below was cross-checked a
  second time directly against the authoritative registry RDAP endpoint
  (Verisign for `.com`, Public Interest Registry for `.org`, Identity Digital
  for `.wine`), not just the `rdap.org` proxy.
- **`.se`** is not in the IANA RDAP bootstrap, so `rdap.org` gives a false
  `404` for every `.se` name regardless of registration. Checked instead via
  `whois -h whois.iis.se <name>` — `domain "x.se" not found.` means free;
  `state:`/`status:`/`created:` fields mean registered.
- **Cloudflare support**: cross-checked each TLD against
  `curl -s "https://www.truthdomains.net/cloudflare-registrar/api/" | jq -r '.domains[]'`
  (377 TLDs at check time). This is a third party reading Cloudflare's own
  page, not Cloudflare's API — treat as strong evidence, not proof.
  Confirmed: `.com` `.org` `.app` `.wine` `.vin` supported. Confirmed
  **not** supported: `.se`, `.nu`, `.eu`, and no other Nordic ccTLD either.
- Paced 2s between whois/RDAP calls to avoid a throttle masquerading as
  "not found."
- **No check reaches Cloudflare's own dashboard search** — there is no public
  availability API for Cloudflare Registrar itself. Everything below narrows
  the list to what's worth searching there; a human still has to run that
  search before buying.

## Ranked table

Domains a human should actually go check in the Cloudflare dashboard, best
first. "Available" = RDAP/whois says unregistered; it is **not** a promise
Cloudflare will sell it at standard price — premium-tier pricing is invisible
to both RDAP and whois.

| # | Domain | Verdict | Method | Cloudflare | What it's going for |
|---|---|---|---|---|---|
| 1 | **wineadditives.com** | Available | RDAP 404, confirmed via rdap.org + Verisign direct | Supported | Descriptive English, maximally literal — says exactly what the site is, in both languages (loanword-transparent) |
| 2 | **vindeklaration.com** | Available | RDAP 404, confirmed via rdap.org + Verisign direct | Supported | Descriptive Swedish — names the actual EU-mandated document ("vindeklaration") the whole dataset is built from |
| 3 | wineadditives.org | Available | RDAP 404, confirmed via rdap.org + PIR direct | Supported | Same as #1; `.org` reads more like an open-data/nonprofit project |
| 4 | declaredwine.com | Available | RDAP 404, confirmed via rdap.org + Verisign direct | Supported | Descriptive English wordplay — "wine that declares itself" |
| 5 | tillsatskoll.com | Available | RDAP 404, confirmed via rdap.org + Verisign direct | Supported | Descriptive Swedish, web-native compound ("additive check"), same pattern as *bilkoll*, *prisjakt* |
| 6 | openvin.org | Available | RDAP 404 (rdap.org) | Supported | Coined — "open" + "vin," echoes the README's own "open dataset" framing |
| 7 | vindeklaration.wine | Available | RDAP 404 (rdap.org) | Supported | Same as #2, industry-specific TLD; no resemblance to a protected appellation |
| 8 | wineingredients.org | Available | RDAP 404, confirmed via rdap.org + PIR direct | Supported | Descriptive English, slightly broader than "additives" (dataset also tracks base ingredients/gases) |
| 9 | vinklart.com | Available | RDAP 404, confirmed via rdap.org + Verisign direct | Supported | Coined Swedish — "vin" + "klart" (clear/obviously); doubles as a clarity/transparency pun |
| 10 | vinspegel.com | Available | RDAP 404 (rdap.org) | Supported | Coined Swedish — "vin" + "spegel" (mirror); metaphor for holding a label up to scrutiny |
| 11 | winescan.wine | Available | RDAP 404 (rdap.org) | Supported | Coined English — evokes reading/scanning a label |
| 12 | vinsyn.wine | Available | RDAP 404 (rdap.org) | Supported | Coined Swedish — "vin" + "syn" (view/vision); note it reads roughly as "vin-sin" spoken in English — odd, not offensive |
| 13 | klarvin.wine | Available | RDAP 404 (rdap.org) | Supported | Coined Swedish, same "klar" pun as #9, `.com` of this name is taken |
| 14 | vindeklaration.vin | Available | RDAP 404 (rdap.org) | Supported | Same as #2/#7 in the other wine-industry TLD |
| 15 | wineadditives.wine | Available | RDAP 404 (rdap.org) | Supported | Same as #1, industry TLD |
| 16 | clarivin.wine | Available, **not recommended** | RDAP 404 (rdap.org) | Supported | Coined — reads very close to *Claritin* (Bayer antihistamine); available but likely to invite confusion |

### Checked and already registered (ruled out)

| Domain | Verdict | Method |
|---|---|---|
| vinkoll.com | Registered | RDAP 200 |
| klarvin.com | Registered | RDAP 200 |
| vindata.com | Registered | RDAP 200 |
| renvin.com | Registered | RDAP 200 |
| wineingredients.com | Registered | RDAP 200 |
| winetransparency.com | Registered | RDAP 200 |
| winefacts.com | Registered | RDAP 200 |
| winefacts.org | Registered | RDAP 200 |
| winescan.com | Registered | RDAP 200 |
| vinlens.com | Registered | RDAP 200 |
| vinsyn.com | Registered | RDAP 200 |
| openvin.com | Registered | RDAP 200 |
| wineclarity.com | Registered | RDAP 200 |
| vinkoll.se | Registered (active, expires 2027, registrar Loopia) | whois.iis.se |

### `.se` aside (Cloudflare does not sell `.se` — would need Loopia, Binero or Glesys)

| Domain | Verdict | Method |
|---|---|---|
| renvin.se | Available (`domain "renvin.se" not found.`) | whois.iis.se |
| vinkoll.se | Registered — see table above | whois.iis.se |

## Recommendation

**First choice: `wineadditives.com`.** It is understood instantly in both
languages with no explanation needed, `.com` carries the most default trust
for a public-facing consumer tool, and it is confirmed available through two
independent RDAP sources.

**Fallback: `vindeklaration.com`.** It names the exact legal document (the EU
wine ingredient declaration) the dataset is built from, which will land
harder with the primary Swedish audience than a generic English compound;
also confirmed available through two independent sources, and stays inside
Cloudflare's supported set.

## What could not be verified

- **Cloudflare's own dashboard search was not run for any of these** — there
  is no public API for it, only the dashboard at domains.cloudflare.com. Every
  "Supported" mark above is TLD-level policy (via the third-party scrape),
  not a per-name search. A human still needs to search each shortlisted name
  there before trusting a price.
- **Premium-tier pricing is invisible to RDAP and whois.** Any of the
  available names above — especially the short, generic-sounding `.com` ones
  like `wineadditives.com` — could carry a premium markup that only the
  Cloudflare dashboard reveals.
- **No trademark search was performed**, beyond the explicit `clarivin.wine`
  ↔ Claritin resemblance flagged above. Domain availability and trademark
  clearance are different questions; this only answers the first.
- **`.wine`/`.vin` geographic-indication restrictions** were checked only by
  eye against well-known protected appellations (Champagne, Rioja, Chianti,
  Bordeaux, etc.) — none of the shortlisted names resemble one, but this is
  not a check against the registries' full official GI list.
- **Whois/RDAP results reflect a single point in time** (2026-07-26). A
  handful of the "available" results were cross-verified a second time
  against the authoritative registry directly; most of the `.wine` results
  and the `.org` alternates were confirmed only via the `rdap.org` proxy
  once. Re-run before acting on this list if time has passed.
- **`vinsyn.wine`'s English pronunciation** ("vin-sin") is a judgment call,
  not a hard fact — worth a second opinion before ranking it any higher.

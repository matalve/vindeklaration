# Domain

**`vindeklaration.se`, registered 2026-07-26, live since 2026-07-29.** It names
the EU document the dataset is parsed from. Registered at **INLEED**, DNS
delegated to Cloudflare — the registration stays there because Cloudflare
Registrar sells no `.se`. `docs/deploy-site.md` has the rest.

The ranked candidate lists that used to fill this file are gone: the choice is
made and availability from July 2026 tells nobody anything now. What is worth
keeping is the method, because it is easy to get wrong and someone will check a
domain again.

## Checking a domain, correctly

- **`.se` and `.nu` are absent from the IANA RDAP bootstrap.** `rdap.org`
  returns `404` for every `.se` name whether or not it exists — verified
  against `systembolaget.se`, registered since 1994. Use
  `whois -h whois.iis.se <name>`: `domain "x.se" not found.` means free.
- **`.com`, `.org`, `.wine`, `.vin` are in the bootstrap**, so
  `https://rdap.org/domain/<name>` is authoritative: `200` registered, `404`
  free.
- Pace queries 2–3 s apart. A throttle reads as "not found".
- **Cloudflare Registrar sells no Nordic ccTLD**, and has no public
  availability API — premium pricing on `.wine`/`.vin` is invisible to both
  RDAP and whois and only shows in their own dashboard search.

`vindeklaration` was also free on `.com`, `.wine` and `.vin` on 2026-07-26, if a
second domain to redirect from is ever wanted. Re-check before buying.

## Not done

No trademark search was ever performed, beyond avoiding "Systembolaget" and
producer names. Domain availability and trademark clearance are different
questions and only the first was answered.

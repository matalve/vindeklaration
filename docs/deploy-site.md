# Publishing the site

How vindeklaration.se gets from `data/wines.json` to a browser. Rewritten
2026-07-29 for the Git integration; the steps are untested end to end, so where
something is a guess it says so.

Cloudflare builds the site itself from this repository. Nothing needs to run on
the Pi or in GitHub Actions for a deploy to happen — pushing to `main` is the
whole trigger, and **the Pi's nightly dataset commit around 03:20 is a push**,
so the site follows the data without anyone doing anything.

Order matters: **deploy first, move DNS last**, so the site is known to work
before the domain depends on it.

## What is being deployed

```sh
uv run python -m src.site        # ~24 s on the Pi
```

15 055 files, 36 MB, output in `site/`. Nothing in it is committed — `site/`
is gitignored and rebuilt on Cloudflare, so the repository never carries two
copies of the same data.

This is a build and not a crawler. It reads the dataset out of the repository
and makes no request to Systembolaget, so it does not touch the one-crawler
rule in `CLAUDE.md`.

## 1. Connect the repository

1. Create a Cloudflare account if there is none. The free plan is enough:
   unlimited bandwidth and requests, 500 builds a month against roughly 30 used.
2. **Workers & Pages → Create → Pages → Connect to Git.** Authorise the
   Cloudflare GitHub App and give it access to `matalve/vindeklaration`. A
   private repository works; the App is how it reads it.
3. Project name `vindeklaration`, production branch `main`.

## 2. Build settings

| Field | Value |
|---|---|
| Framework preset | None |
| Build command | `pip install uv && uv run python -m src.site && test $(find site -type f \| wc -l) -le 19000` |
| Build output directory | `site` |
| Root directory | *(leave empty)* |

The `test` at the end is not decoration. **Cloudflare Pages rejects a
deployment over 20 000 files**, and the build grows with the assortment — it is
at 15 055 today. Failing the build with the count visible is much easier to
diagnose than a rejected upload with a generic message. When it trips, read
*Bilingual* in `docs/site-plan.md`, where the cap and the ways past it are
written up.

`uv` is not in the build image, hence `pip install uv`. It reads
`pyproject.toml` and `uv.lock` and installs the rest itself.

## 3. Environment variables

**Settings → Environment variables → Production.**

| Name | Value | When |
|---|---|---|
| `PYTHON_VERSION` | `3.11.5` | now — cheap insurance against the build image changing its default under you |
| `CF_ANALYTICS_TOKEN` | the beacon token | after step 6; leave unset until then and no beacon is rendered |

Unset `CF_ANALYTICS_TOKEN` is a supported state, not a broken one —
`src/site.py` renders no script at all without it, which is also what local
builds do.

## 4. First deploy

Saving the build settings starts one. Three or four minutes, most of it
installing dependencies. It lands on `https://vindeklaration.pages.dev`.

Check before going further:

- The front page loads, and the three counts add up to the total in the
  caption above them.
- Typing in the search box returns wines. The index is 2.7 MB uncompressed;
  Cloudflare gzips it in transit, so read the transferred size in the network
  tab rather than the file size.
- A wine page renders, its bottle photograph appears, and the footer carries
  both Systembolaget sentences.
- `/en/` and `/en/method/` load, and a made-up URL under `/vin/` gets the
  project's own 404 page rather than Cloudflare's.

Every branch that is not `main` now gets its own preview URL automatically.
That is the main thing this arrangement buys, and it is what makes running
`site-auditor` against a change worthwhile before the change is live.

## 5. Move DNS to Cloudflare

The domain is registered at **INLEED** and uses their nameservers
(`ns1.inleed.net` … `ns6.inleed.net`, confirmed by whois 2026-07-29).
Cloudflare Registrar sells no `.se`, so the registration **stays at Inleed** —
only the nameservers change. No transfer, no auth code, no fee.

1. In Cloudflare: **Add a domain** → `vindeklaration.se` → Free plan → let it
   scan the existing records. There is nothing to preserve **unless mail is
   configured for the domain**, in which case copy the MX and any SPF, DKIM and
   DMARC `TXT` records across *before* switching. Post stops otherwise, and it
   stops quietly.
2. Cloudflare gives two nameservers, of the form `something.ns.cloudflare.com`.
3. In Inleed's control panel, replace all six `inleed.net` nameservers with
   Cloudflare's two.
4. Wait. `.se` publishes quickly but resolvers cache; an hour is typical, 24 is
   the number to quote if it looks stuck. Cloudflare emails when the zone is
   active.

Verify from a machine that has not looked the domain up recently:

```sh
whois -h whois.iis.se vindeklaration.se | grep nserver
dig NS vindeklaration.se +short
```

## 6. Attach the domain, then turn on Web Analytics

Once the zone is active: **Workers & Pages → vindeklaration → Custom domains →
Set up a domain** → `vindeklaration.se`. Cloudflare creates the records and
issues the certificate itself, usually within minutes. Add `www` the same way
if you want it, then send it to the apex with a **Redirect Rule** — the same
page existing at two addresses helps nobody, and `vindeklaration.se` is the
shorter thing to say out loud.

Then **Analytics & Logs → Web Analytics → Add a site** for the hostname. Put
the beacon token in `CF_ANALYTICS_TOKEN` (step 3) and redeploy.

Two things worth keeping straight. Cloudflare already reports requests and
bandwidth for the site without any beacon — that is server-side, and it is why
the beacon adds no new party. The beacon adds page-level detail from the
browser. It sets no cookie and builds no cross-site profile, so there is still
no cookie banner, but `/metod` names it and says what it sends. **Remove or
replace the beacon and that paragraph is wrong** — it is `third_party` in
`templates/strings.json`, and the template block that renders the beacon says
so next to itself.

## 7. Optional, once it is working

- **Build watch paths.** *Settings → Builds & deployments.* Excluding `docs/`,
  `deploy/`, `.claude/` and `*.md` stops a documentation commit from rebuilding
  15 000 pages. Nothing breaks without it; it just wastes a build.
- **`_headers` with a Content-Security-Policy** naming
  `product-cdn.systembolaget.se` as the only image source and
  `static.cloudflareinsights.com` as the only script source. That would turn
  the `/metod` paragraph from a promise into something the browser enforces.

## 8. After it is live

- **Set `CDN_CHECKED` in `src/site.py` whenever the image premise is
  re-checked.** `/metod` publishes that date, and condition 2 of
  `docs/legal-notes.md` §2j says the images come down the same day a
  technological measure appears on Systembolaget's CDN. The date is what makes
  that promise checkable. **Nothing automated does this yet** — a real gap, not
  an oversight to inherit quietly.
- **Run `site-auditor` after any change to `templates/`**, against the branch's
  preview URL. It reads the built output against the plan's honesty rules, and
  it has already caught a sentence on `/metod` that was simply untrue about the
  site's own privacy.
- **Watch the file count.** It grows with the assortment and the build fails at
  19 000 deliberately — a warning shot rather than a rejected upload.

## `.github/workflows/deploy.yml`

Kept, but **manual only**, on the same principle as `update.yml`: a standby for
when the primary path is unavailable. It needs `CLOUDFLARE_API_TOKEN` and
`CLOUDFLARE_ACCOUNT_ID` as repository secrets, which do not exist unless
someone adds them, so it will fail until they do. That is the intended state.

Do not put it back on `push`. With the Git integration connected, both would
build and upload the same commit.

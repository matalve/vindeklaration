# Publishing the site

How vindeklaration.se gets from `data/wines.json` to a browser. **Live**: the
domain is bought and DNS points at Cloudflare, and the site deploys as a
Cloudflare Worker that builds straight from this GitHub repository — no
Pi or GitHub Actions involvement. Rewritten 2026-07-29 for **Workers**, after
a first deploy proved the Pages flow this guide originally described no
longer exists. What follows is kept as the step-by-step record of how that
came together, for the day it has to be redone — a lost Worker, a new
project, a second domain.

**It is a Worker with static assets, not a Cloudflare Pages project.**
Cloudflare has absorbed Pages into Workers: Pages is not formally deprecated
and existing projects keep working, but the dashboard steers new projects to
Workers, and "Connect to Git" creates a Worker. The practical differences that
matter here are the hostname (step 1a) and 404 handling (step 2a).

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

15 162 files, 36 MB, output in `site/`. Nothing in it is committed — `site/`
is gitignored and rebuilt on Cloudflare, so the repository never carries two
copies of the same data.

This is a build and not a crawler. It reads the dataset out of the repository
and makes no request to Systembolaget, so it does not touch the one-crawler
rule in `CLAUDE.md`.

## 1a. Set the account subdomain first

**Do this before the first deploy.** A Worker is served at
`<worker-name>.<account-subdomain>.workers.dev`, and **Cloudflare derives the
account subdomain from the account name at signup** — which, if the account was
opened in a person's own name, puts that name in the URL. Pages did not behave
this way, which is why it is easy to be caught by it.

**Workers & Pages → Overview → *Change* beside "Your subdomain".** Use
`matalve`, the project's approved public identifier. It is account-wide rather
than per-project, so it should not be a project name: every future Worker
inherits it. Several Cloudflare community threads suggest the change may only
be possible once, so choose the durable answer rather than the convenient one.

Once a custom domain is attached (step 6), the workers.dev route can be
disabled entirely and the hostname stops answering at all.

## 1. Connect the repository

1. Create a Cloudflare account if there is none. The free plan is enough:
   unlimited bandwidth and requests, and static-asset limits well above what
   this site needs.
2. **Workers & Pages → Create → Connect to Git** (Workers, not Pages — see the
   note at the top). Authorise the Cloudflare GitHub App and give it access to
   `matalve/vindeklaration`. A private repository works; the App is how it
   reads it.
3. Worker name `vindeklaration`, production branch `main`. The name becomes the
   first label of the hostname, so it is the half of the URL you control.

## 2. Build settings

| Field | Value |
|---|---|
| Framework preset | None |
| Build command | see below |
| Build output directory | `site` |
| Root directory | *(leave empty)* |

The `test` at the end is not decoration. **A Worker rejects more than 20 000
static assets on the free plan** (100 000 on paid), and the build grows with
the assortment — it is
at 15 162 today. Failing the build with the count visible is much easier to
diagnose than a rejected upload with a generic message. When it trips, read
*Bilingual* in `docs/site-plan.md`, where the cap and the ways past it are
written up.

`uv` is not in the build image, so the command installs it first. This form is
confirmed working on Cloudflare's image as of 2026-07-29:

```sh
pip install uv && uv run python -m src.site && \
  test $(find site -type f | wc -l) -le 19000
```

Paste it as one line into the build command field. `uv` reads `pyproject.toml`
and `uv.lock` and installs the rest itself.

**If a future build image refuses it** with `externally-managed-environment` or
`uv: command not found`, install into the user site instead:

```sh
pip install --user uv && export PATH="$HOME/.local/bin:$PATH" && \
  uv run python -m src.site && \
  test $(find site -type f | wc -l) -le 19000
```

A Python version below 3.11 in the log means `PYTHON_VERSION` is unset; see
step 3.

## 2a. 404 handling

`wrangler.jsonc` in the repository root sets `not_found_handling: "404-page"`,
so a stale `/vin/…` URL gets the project's own 404 rather than an empty body.
Pages did this automatically; a Worker does not.

Nothing to configure — the file is committed. If a build ever fails right after
that file changes, it is the first suspect: the dashboard's build settings and
a wrangler config can disagree about the output directory.

## 3. Environment variables

**Settings → Environment variables → Production.**

| Name | Value | When |
|---|---|---|
| `PYTHON_VERSION` | `3.11.5` | now — cheap insurance against the build image changing its default under you |
There is **no analytics variable**. Cloudflare injects its own beacon with its
own token; nothing in this repository renders one. See step 6.

## 4. First deploy

Saving the build settings starts one. *Confirmed 2026-07-29: it takes several
minutes, most of it installing dependencies, and the dashboard is quiet for
long enough to look stuck.* It lands on
`https://vindeklaration.<your-subdomain>.workers.dev`, and the exact URL is at
the top of the deployment page.

Check before going further — all of these were confirmed passing on the first
deploy:

- The front page loads, and the three counts add up to the total in the
  caption above them.
- Typing in the search box returns wines. The index is 2.7 MB uncompressed;
  Cloudflare gzips it in transit, so read the transferred size in the network
  tab rather than the file size.
- A wine page renders, its bottle photograph appears, and the footer carries
  both Systembolaget sentences.
- `/en/` and `/en/method/` load, and a made-up URL under `/vin/` gets the
  project's own 404 page rather than an empty body. *This one failed on the
  first deploy and is what `wrangler.jsonc` fixes.*

Every branch that is not `main` now gets its own preview URL automatically.
That is the main thing this arrangement buys, and it is what makes running
`site-auditor` against a change worthwhile before the change is live.

## 5. Move DNS to Cloudflare

**Done** — the domain now resolves through Cloudflare.

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

**Done** — `vindeklaration.se` is the live custom domain and the workers.dev
route is disabled.

Once the zone is active: **Workers & Pages → vindeklaration → Settings →
Domains & Routes → Add → Custom domain** → `vindeklaration.se`. Cloudflare creates the records and
issues the certificate itself, usually within minutes. Add `www` the same way
if you want it, then send it to the apex with a **Redirect Rule** — the same
page existing at two addresses helps nobody, and `vindeklaration.se` is the
shorter thing to say out loud.

**Then disable the workers.dev route**, in the same Domains & Routes panel. The
custom domain is the address; leaving the workers.dev one answering means the
site exists at two addresses, one of which contains whatever the account
subdomain happens to be.

Then **Analytics & Logs → Web Analytics → Add a site** for the hostname and
enable **automatic injection**. *Confirmed 2026-07-29.* There is no token to
copy and nothing to redeploy — for a proxied domain Cloudflare generates the
token and injects the snippet at the edge. The manual snippet with a token
exists only for sites that are not behind Cloudflare, which is why hunting for
one here finds nothing.

Two things worth knowing, both confirmed by reading a served page rather than
from documentation:

- **The beacon is only injected for browser-like requests.** `curl` gets a page
  with no beacon in it, which looks exactly like injection being switched off.
  Send a normal browser `User-Agent` before concluding anything.
- **The script comes from `static.cloudflareinsights.com`**, a third-party host.
  Automatic injection does not make the measurement first-party. `/metod` names
  it as one of two third-party requests, and that is accurate.

Two things worth keeping straight. Cloudflare already reports requests and
bandwidth for the site without any beacon — that is server-side, and it is why
the beacon adds no new party. The beacon adds page-level detail from the
browser. It sets no cookie and builds no cross-site profile, so there is still
no cookie banner, but `/metod` names it and says what it sends. **Remove or
replace the beacon and that paragraph is wrong** — it is `third_party` in
`templates/strings.json`, and the template block that renders the beacon says
so next to itself.

## 6b. www, and HTTPS

**`www` needs a DNS record before any redirect rule can fire.** A rule cannot
act on a request that never reaches Cloudflare. *DNS → Records → Add record*:
`CNAME`, name `www`, target `vindeklaration.se`, **Proxied** — the orange cloud
is the part that matters.

Then *Rules → Redirect Rules → Create*. The editor defaults to **wildcard
pattern** matching, where `${1}` in the target is whatever `*` captured — there
is no "Dynamic" toggle to look for unless you switch to the expression editor.

| Field | Value |
|---|---|
| Request URL | `https://www.vindeklaration.se/*` |
| Target URL | `https://vindeklaration.se/${1}` |
| Status code | `301` |
| Preserve query string | on |

The `${1}` is the point. A target of plain `https://vindeklaration.se` sends
every visitor to the front page, including whoever followed a link to a wine.

Also **SSL/TLS → Edge Certificates → Always Use HTTPS**. *Confirmed working
2026-07-29* — without it `http://vindeklaration.se/` is served in the clear
rather than redirected.

### Free plan settings worth a decision

Not an inventory of the dashboard; the four that matter for a public,
cookie-free, static site that wants to be indexed.

- **Bot Fight Mode: off.** It puts a JS challenge in front of suspect traffic
  and turns away legitimate crawlers, search engines included. Journey 3 —
  arriving from a search engine on a substance name — depends on being indexed.
  There is also something off about a project that is itself a polite crawler
  of someone else's site shutting the door on everyone else's.
- **Rocket Loader: off.** It rearranges when scripts run. `sok.js` is 3 kB and
  already deferred, so there is nothing to win and a known way to lose.
- **Crawler Hints: on.** The site rebuilds nightly; this tells search engines
  when it actually changed instead of having them guess.
- **HSTS: considered, not automatic.** Right in principle since the site should
  never answer over HTTP. Start at six months and **leave preload alone** — a
  preloaded domain is painful to walk back, and that is not something to
  discover afterwards.

Leave caching alone. The response carries `max-age=0, must-revalidate`, which
is the Workers default for HTML and is what lets the nightly rebuild reach
people the same morning. A longer Browser Cache TTL delays the data for no
real gain.

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

# Publishing the site

**vindeklaration.se is live**, as a Cloudflare **Worker with static assets**
that builds from this repository on every push to `main`. The dataset is not
in git: each build downloads `wines.json` from the R2 bucket behind `/data/`,
and the Pi's nightly `update.sh` publishes to that bucket *before* pushing the
small commit (`data/quality-history.json`, which changes on every recorded
run) that triggers the rebuild. Nothing runs on the Pi or in GitHub Actions
for a deploy to happen.

It is **not a Pages project**. Cloudflare absorbed Pages into Workers; existing
Pages projects keep working, but "Connect to Git" now creates a Worker, and the
two differ in the hostname and in 404 handling.

## The dataset lives in R2, not git

`data/wines.json` and `data/catalog.json` are gitignored — a nightly 16 MB
commit costs its near-full size in history, forever. The crawler publishes
them as build output instead:

- **The R2 bucket `vindeklaration-data`**, served by `worker/index.js` at
  `/data/*` with an hour of edge cache. This is what the site build downloads.
- **A rolling `dataset-latest` GitHub release** (`--clobber`, so the download
  URL is stable) for everyone else, plus a frozen `dataset-YYYY-MM` snapshot
  on the first Sunday of each month — with the dataset out of git, history no
  longer answers "what did the assortment look like in spring".

One-time setup:

```sh
wrangler r2 bucket create vindeklaration-data
# Populate the bucket BEFORE the first build that downloads from it:
gzip -kf data/wines.json data/catalog.json
wrangler r2 object put vindeklaration-data/wines.json.gz --file data/wines.json.gz
wrangler r2 object put vindeklaration-data/catalog.json.gz --file data/catalog.json.gz
```

The Pi's timer needs `CLOUDFLARE_API_TOKEN` and `CLOUDFLARE_ACCOUNT_ID` in its
environment (the systemd unit) for `wrangler r2 object put`, and a logged-in
`gh` for the release upload.

## The build

```sh
uv run python -m src.site        # ~25 s, 15 400 files, output in site/
```

`site/` is gitignored and rebuilt on Cloudflare, so the repository never
carries two copies of the site. This is a build, not a crawler: it reads
`data/wines.json` — downloaded from the R2 bucket by the step below — and
makes no request to Systembolaget.

**Build command**, confirmed working on Cloudflare's image:

```sh
mkdir -p data && \
  curl -fsSL https://vindeklaration.se/data/wines.json.gz | gunzip > data/wines.json && \
  pip install uv && uv run python -m src.site && \
  test $(find site -type f | wc -l) -le 19000
```

If the bucket is ever unreachable the release is the fallback:
`https://github.com/matalve/vindeklaration/releases/download/dataset-latest/wines.json.gz`.

| Setting | Value |
|---|---|
| Build output directory | `site` |
| Framework preset, root directory | none |
| `PYTHON_VERSION` | `3.11.5` — insurance against the image changing its default |

**The file-count test is not decoration.** A Worker rejects more than 20 000
static assets on the free plan, the build grows with the assortment, and
failing with the count visible beats a rejected upload with a generic message.
When it trips, read *Bilingual* in `docs/site-plan.md`.

If a future image refuses `pip install uv` with `externally-managed-environment`,
use `pip install --user uv && export PATH="$HOME/.local/bin:$PATH"` instead.

`wrangler.jsonc` sets `not_found_handling: "404-page"` so a stale `/vin/…` URL
gets the project's own 404. Pages did this automatically; a Worker does not. If
a build fails right after that file changes, it is the first suspect — the
dashboard's build settings and a wrangler config can disagree about the output
directory.

## The account subdomain

**Cloudflare derives it from the account name at signup**, which puts a
person's own name in `*.workers.dev` if the account was opened that way. It is
account-wide, may only be changeable once, and is set to `matalve`. The
workers.dev route is disabled anyway, since the custom domain is the address.

## DNS and the domain

Registered at **INLEED**, nameservers delegated to Cloudflare. Cloudflare
Registrar sells no `.se`, so the registration stays at Inleed — only the
nameservers moved. `www` is a proxied `CNAME` to the apex with a Redirect Rule
sending `https://www.vindeklaration.se/*` to `https://vindeklaration.se/${1}`,
301, query string preserved. **The `${1}` is the point**: a bare target sends
everyone who followed a link to a wine to the front page instead.

**SSL/TLS → Always Use HTTPS** is on; without it `http://` is served in the
clear rather than redirected.

To verify from a machine that has not looked the domain up recently:

```sh
whois -h whois.iis.se vindeklaration.se | grep nserver
dig NS vindeklaration.se +short
```

## Analytics

**Cloudflare Web Analytics with automatic injection.** For a proxied domain
Cloudflare generates the token and injects the snippet at the edge — there is
nothing to copy and nothing to redeploy, which is why hunting for a manual
token finds nothing. Two things confirmed by reading a served page rather than
documentation:

- **The beacon is only injected for browser-like requests.** `curl` gets a page
  with no beacon, which looks exactly like injection being off.
- **The script comes from `static.cloudflareinsights.com`**, a third-party host.
  Automatic injection does not make it first-party, and `/metod` names it as
  one of two third-party requests.

**Remove or replace the beacon and that paragraph on `/metod` is wrong** — it is
`third_party` in `templates/strings.json`.

## Free-plan settings that were decided

- **Bot Fight Mode: off.** Its JS challenge turns away legitimate crawlers,
  search engines included, and being indexed is what journey 3 depends on.
- **Rocket Loader: off.** It rearranges when scripts run; `sok.js` is 3 kB and
  already deferred, so there is nothing to win.
- **Crawler Hints: on.** The site rebuilds nightly and this says when it
  actually changed.
- **HSTS: not enabled.** Right in principle. Start at six months if it is, and
  **leave preload alone** — a preloaded domain is painful to walk back.
- **Caching: left alone.** `max-age=0, must-revalidate` is the Workers default
  for HTML and is what lets the nightly rebuild reach people the same morning.

## Standing gaps

- **`CDN_CHECKED` in `src/site.py` is set by hand.** `/metod` publishes that
  date, and condition 2 of `docs/legal-notes.md` §2j says the images come down
  the day a technological measure appears on Systembolaget's CDN. Nothing
  automates the check. A real gap, not an oversight to inherit quietly.
- **Build watch paths are not configured.** Excluding `docs/`, `deploy/`,
  `.claude/` and `*.md` would stop a documentation commit rebuilding 15 000
  pages. Harmless either way — but the nightly rebuild rides on the Pi's
  post-publish commit (`data/quality-history.json` changes on every recorded
  run), so if watch paths are ever configured, **`data/` must stay on the
  trigger list** or the rebuild stops firing, silently.
- **No Content-Security-Policy.** A `_headers` file naming
  `product-cdn.systembolaget.se` as the only image source and
  `static.cloudflareinsights.com` as the only script source would turn the
  `/metod` paragraph from a promise into something the browser enforces.
- **Run `site-auditor` after any change to `templates/`.** It reads the built
  output against the plan's honesty rules and has caught two live errors.

## `.github/workflows/deploy.yml`

Kept as a **manual-only** standby. It needs `CLOUDFLARE_API_TOKEN` and
`CLOUDFLARE_ACCOUNT_ID` as repository secrets, which do not exist, so it fails
until someone adds them. That is the intended state. Do not put it back on
`push`: with the Git integration connected, both would build the same commit.

**Both standby workflows are stale until PR #1's body is applied.** The change
that moved the dataset out of git could not touch `.github/workflows/` (the
authoring token lacked the `workflow` scope), so `deploy.yml` still builds
without downloading `wines.json` first and `update.yml` still commits the
dataset files. Their updated contents are in PR #1's body; paste them in with
workflow-scoped credentials at the same time as the build-command change
above. Remove this paragraph when that is done.

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

**One-time setup — order matters.** The build downloads from the Worker this
change adds, and that Worker only exists after a deploy, so the route must be
bootstrapped before the build command may point at it:

1. Create and seed the bucket:

   ```sh
   wrangler r2 bucket create vindeklaration-data
   gzip -kf data/wines.json data/catalog.json
   wrangler r2 object put vindeklaration-data/wines.json.gz --remote \
     --file data/wines.json.gz --content-type application/gzip
   wrangler r2 object put vindeklaration-data/catalog.json.gz --remote \
     --file data/catalog.json.gz --content-type application/gzip
   ```

   **`--remote` is not optional.** Without it wrangler writes to the local
   simulator and prints `Resource location: local` — the bucket stays empty
   and the command still exits 0. On the Pi it does not even get that far:
   the local path starts `workerd`, which dies allocating against ARM64's
   address space (`TCMalloc ... 48-bit virtual address space`), surfacing as
   `write EPIPE`. The same flag is needed on `r2 object get`, or a check
   reads back the local copy and confirms nothing.

   **Answer no when `bucket create` offers to add the binding for you.** It
   proposes `vindeklaration_data`, but `worker/index.js` reads `env.DATA`, so
   accepting silently breaks every `/data/` request — and the fix is a
   binding name, which is not where anyone looks first. Saying yes also
   reserialises the whole file: it reindented it from spaces to tabs and
   dropped the trailing newline. The `r2_buckets` block below is already
   correct; wrangler has nothing to add.

2. **Bootstrap-deploy the Worker once by hand**, from a checkout with `site/`
   already built:

   ```sh
   uv run python -m src.site
   wrangler deploy
   ```

   After this, `/data/wines.json.gz` answers 200 and every later build can
   download from it.

3. Update the Workers Builds build command (below) and merge.

Do not point the build command at `/data/` before step 2: the request happens
during the build, *before* the Worker that would serve it has been deployed,
and the 404 fails the very deployment that creates the route. The release URL
*is* a bootstrap alternative now that the repository is public (2026-08-29) and
its assets need no `Authorization` header. It was not one before, which is why
`cf-build.sh` reaches for `/data/` first and the release only as a fallback —
that order is now a preference rather than a necessity.

The Pi's timer needs `CLOUDFLARE_API_TOKEN` and `CLOUDFLARE_ACCOUNT_ID` for
`wrangler r2 object put`, and a logged-in `gh` for the release upload. The unit
reads the two secrets from a file outside git:

```sh
mkdir -p ~/.config/vindeklaration
printf 'CLOUDFLARE_API_TOKEN=%s\nCLOUDFLARE_ACCOUNT_ID=%s\n' TOKEN ACCOUNT \
  > ~/.config/vindeklaration/env
chmod 600 ~/.config/vindeklaration/env
systemctl --user daemon-reload
```

The token needs **Workers R2 Storage: Edit**. `update.sh` checks for both
variables, for `gh`, and for `gh` being logged in *before* it starts crawling —
publishing is the last thing it does, and a missing tool discovered there costs
a three-and-a-half-hour pass that is then thrown away undelivered.

**The unit sets its own `PATH`.** systemd gives a user service a minimal one
that excludes `~/.local/bin`, where both `uv` and `gh` live — which is why `UV`
is substituted as an absolute path at install time, and why the first nightly
run after this change stopped on `gh not found` while `gh` worked perfectly in
a login shell. The `Environment=PATH=` line in `vindeklaration.service` names
that directory. Change where a tool is installed and that line is the first
thing to check. `update.sh` still falls back to `npx wrangler@4` where no
global wrangler exists.

Editing the unit in git does not change the running one: it is a template, and
`bootstrap.sh` substitutes `__REPO__` and `__UV__` into
`~/.config/systemd/user/`. After pulling a change to it, reinstall and reload:

```sh
sed "s|__REPO__|$PWD|g; s|__UV__|$(command -v uv)|g" deploy/vindeklaration.service \
  > ~/.config/systemd/user/vindeklaration.service
systemctl --user daemon-reload
```

## The build

```sh
uv run python -m src.site        # ~25 s, 15 400 files, output in site/
```

`site/` is gitignored and rebuilt on Cloudflare, so the repository never
carries two copies of the site. This is a build, not a crawler: it reads
`data/wines.json` — downloaded from the R2 bucket by the step below — and
makes no request to Systembolaget.

**Build command.** A field in the Cloudflare dashboard — the Worker's Settings,
under Build. It holds one line and nothing else:

```sh
bash cf-build.sh
```

The steps themselves live in `cf-build.sh`, at the repository root, because a
dashboard field is not versioned, does not appear in a diff, and cannot be
tested. On 2026-08-28 that field still held the pre-R2 command after the
dataset left git, and three builds failed against a repository that no longer
carried `data/wines.json`. Anything the build does belongs in the script;
change the field only to point somewhere else.

The script fetches the dataset from the bucket, falls back to the rolling
release, builds, and checks the file count. `DATA_URL`, `RELEASE_URL` and
`ASSET_LIMIT` are overridable, so a fork or a local run can build against its
own copy. It installs `uv` only where none is present — on Cloudflare's image
`pip install uv` works, while on Debian and Raspberry Pi OS the same line stops
at PEP 668's `externally-managed-environment`, which says nothing about the
build.

The script sits at the root, not in `deploy/`, because the build's watch paths
exclude `/deploy`: a fix to it must trigger the build that tests it.

If the bucket is ever unreachable the release is the fallback once the
repository is public:
`https://github.com/matalve/vindeklaration/releases/download/dataset-latest/wines.json.gz`.

| Setting | Value |
|---|---|
| Build output directory | `site` |
| Framework preset, root directory | none |
| `PYTHON_VERSION` | `3.11.5` — insurance against the image changing its default |

**Build watch paths are configured**: include `*`, exclude `/docs`, `/deploy`,
`.claude/` and `*.md`, so a documentation commit does not rebuild 15 000 pages.
Two consequences worth keeping in mind before editing that list:

- **`data/` must stay on the trigger list.** The nightly rebuild rides on the
  Pi's post-publish commit — `data/quality-history.json` changes on every
  recorded run — so excluding `data/` would stop the rebuild firing, silently.
- **`/deploy` is excluded**, which is why `cf-build.sh` lives at the repository
  root. A change to the build script has to trigger the build that tests it.

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

Both standby workflows track the dataset's move out of git: `deploy.yml`
downloads `wines.json` from the bucket before building, and `update.yml`
publishes to the rolling release and commits only `unknown.json`.

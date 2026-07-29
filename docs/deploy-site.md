# Publishing the site

How vindeklaration.se gets from `data/wines.json` to a browser. Written
2026-07-29, before the first deploy, so the steps are untested end to end —
where something is a guess it says so.

The build itself is done: `.github/workflows/deploy.yml` builds and publishes
on every push to `main`. What is missing is a Cloudflare account, two GitHub
secrets, and the domain pointing at it. Those need a human, and the order below
matters — **deploy first, move DNS last**, so the site is known to work before
the domain depends on it.

## What is being deployed

```sh
uv run python -m src.site        # ~24 s on the Pi
```

15 055 files, 36 MB, output in `site/`. Nothing in it is committed —
`site/` is gitignored and rebuilt in CI, so the repository never carries two
copies of the same data.

The workflow runs on push to `main`, which includes **the Pi's nightly dataset
commit around 03:20**. That is intentional: the site should follow the data
without anyone doing anything. Pushes that only touch `docs/`, `deploy/`,
`.claude/` or a Markdown file are skipped.

It is a build and not a crawler. It reads the dataset out of the repository and
makes no request to Systembolaget, so it does not conflict with the one-crawler
rule in `CLAUDE.md`.

## 1. Cloudflare account and Pages project

1. Create a Cloudflare account if there is none. The free plan is enough:
   unlimited bandwidth, unlimited requests, 500 builds a month, and we build
   about 30.
2. **Workers & Pages → Create → Pages → Upload assets**, name the project
   `vindeklaration`, and upload anything at all — a single `index.html` will
   do. This exists only to create the project so the API token can target it;
   the first real deploy replaces it.

   Do **not** use "Connect to Git". That path makes Cloudflare run the build,
   which means giving it repository access and reproducing the uv setup in
   their environment. The workflow already builds; Cloudflare only receives
   files.
3. Note the **Account ID**, on the right-hand side of any Workers & Pages page.

## 2. API token

**My Profile → API Tokens → Create Token → Create Custom Token.**

| Field | Value |
|---|---|
| Permissions | `Account` · `Cloudflare Pages` · `Edit` |
| Account Resources | Include · your account |
| TTL | leave open, or set a reminder to rotate |

That single permission is all `wrangler pages deploy` needs. Do not use the
"Edit Cloudflare Workers" template — it grants far more than this.

Copy the token when it is shown. It is not shown again.

## 3. GitHub secrets

**Settings → Secrets and variables → Actions → New repository secret**, twice:

| Name | Value |
|---|---|
| `CLOUDFLARE_API_TOKEN` | the token from step 2 |
| `CLOUDFLARE_ACCOUNT_ID` | the Account ID from step 1 |

The names are what `deploy.yml` reads; changing one means changing the other.

## 4. First deploy

**Actions → Deploy site → Run workflow.** It should take three or four minutes,
most of it installing dependencies.

It lands on `https://vindeklaration.pages.dev`. Check before going further:

- The front page loads and the counts add up to the total shown in the caption.
- Typing in the search box fetches the index and returns wines. The index is
  2.7 MB uncompressed; Cloudflare gzips it in transit, so watch the transferred
  size in the network tab rather than the file size.
- A wine page renders, its bottle photograph appears, and the footer carries
  both Systembolaget sentences.
- `/en/` and `/en/method/` load, and a made-up URL gets the project's own 404
  rather than Cloudflare's.

If the workflow fails on the file-count check, read *Bilingual* in
`docs/site-plan.md` — the cap and the ways past it are written up there.

## 5. Move DNS to Cloudflare

The domain is registered at **INLEED** and currently uses their nameservers
(`ns1.inleed.net` … `ns6.inleed.net`, confirmed by whois 2026-07-29). Cloudflare
Registrar sells no `.se`, so the registration **stays at Inleed** — only the
nameservers change. There is no transfer, no auth code and no fee.

1. In Cloudflare: **Add a domain** → `vindeklaration.se` → select the Free plan
   → let it scan the existing records. There is nothing to preserve unless mail
   is already configured for the domain, in which case copy the MX and any
   SPF/DKIM/DMARC `TXT` records across **before** switching.
2. Cloudflare gives two nameservers, of the form `something.ns.cloudflare.com`.
3. In Inleed's control panel, replace all six `inleed.net` nameservers with
   Cloudflare's two.
4. Wait. `.se` publishes changes quickly but resolvers cache; an hour is
   typical, 24 is the number to quote if it looks stuck. Cloudflare emails when
   the zone goes active.

Verify from a machine that has not looked the domain up recently:

```sh
whois -h whois.iis.se vindeklaration.se | grep nserver
dig NS vindeklaration.se +short
```

## 6. Attach the domain to the site

Once the zone is active in Cloudflare: **Workers & Pages → vindeklaration →
Custom domains → Set up a domain** → `vindeklaration.se`. Add `www` the same
way if you want it; Cloudflare creates the records and issues the certificate
itself, usually within minutes.

Then decide which one is canonical. `vindeklaration.se` without `www` is the
shorter thing to say out loud, and the site's audience is people reading a
phone in a shop — a **Redirect Rule** from `www` to the apex costs nothing and
avoids the same page existing at two addresses.

## 7. After it is live

- **Set `CDN_CHECKED` in `src/site.py` whenever the image premise is
  re-checked.** `/metod` publishes that date, and condition 2 of
  `docs/legal-notes.md` §2j says the images come down the same day a
  technological measure appears on Systembolaget's CDN. The date is the
  mechanism that makes that promise checkable. **Nothing automated does this
  yet** — it is a real gap, not an oversight to inherit quietly.
- Run `site-auditor` after any change to `templates/`. It reads the built
  output against the plan's honesty rules and it has already caught a false
  statement about the site's own privacy.
- Watch the file count. It grows with the assortment, and the workflow fails at
  19 000 deliberately — a warning shot rather than a rejected upload.

## What is not set up, and is worth knowing

- **No analytics, deliberately.** Cloudflare Web Analytics is cookieless and
  would be tempting; it is still a third-party request and `/metod` now states
  that the product photograph is the only one. Adding it means changing that
  sentence, and the sentence is load-bearing.
- **No preview deployments.** The workflow deploys `--branch=main` only.
  Branch previews would give every pull request a public URL, which is a
  reasonable thing to want later and a needless surface today.
- **No `_headers` file.** Worth adding a `Content-Security-Policy` that permits
  only `product-cdn.systembolaget.se` as an image source — it would turn "no
  third-party requests" from a promise into something the browser enforces.

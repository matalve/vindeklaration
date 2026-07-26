# Working on this repository

An open dataset of the additives declared in wines sold by Systembolaget, and
(next) a bilingual site on top of it at **vindeklaration.se**. `README.md`
explains the method and the caveats — read it before changing how anything is
counted. This file is about how to work here.

## Non-negotiable

- **Everything in the repository is in English.** Code, comments, commits,
  README, docs. The owner writes in Swedish and expects Swedish replies in
  chat — the repo is the exception, not the conversation.
- **No personal data, ever.** The only approved identifier is the GitHub
  username `matalve`. Not the owner's real name, not even the first name, and
  not an email address. The repo is configured to commit as
  `matalve <71018760+matalve@users.noreply.github.com>`; do not override it
  with `git -c user.email=...`. History has been rewritten once already to
  remove a personal address that got in this way.
- **Never guess at a declaration.** Text the parser cannot read makes the wine
  `partial`, which keeps it out of the rankings. That is the correct outcome.
  Inventing an alias to make a number look better corrupts the dataset
  silently.

## What is where

| | |
|---|---|
| `src/` | catalog → details → normalize → build → report |
| `data/additives.yaml` | the substance dictionary — the heart of the project |
| `data/lexicon.yaml` | labels, processing notes, stopwords |
| `data/unknown.json` | what the parser could not read, ranked by wines blocked |
| `deploy/` | running it unattended on the Raspberry Pi |
| `.claude/agents/` | lexicon-curator, declaration-auditor, upstream-scout, domain-scout |

```sh
uv run pytest -q                  # fast, run it after any dictionary change
uv run python -m src.build        # rebuild the dataset from the cache
uv run python -m src.report       # coverage, unknown tokens, quality gate
```

## Traps that cost time to rediscover

- **The search API has no ingredient field.** Declarations come from the
  product page's Next.js data route, `/_next/data/{buildId}/produkt/vin/x-{nr}.json`.
  The buildId changes on every deploy and is discovered at runtime.
- **The search API caps page size at 30 and stops paging near 10 000 results**,
  so an unfiltered query silently returns about 8 900 of 15 500 wines. That is
  why `catalog.py` partitions by country.
- **RDAP returns 404 for `.se` whether or not a domain exists** — `.se` is
  absent from the IANA bootstrap. Use `whois -h whois.iis.se`.
- **Cloudflare Registrar sells no Nordic ccTLD.** `.se` needs a Swedish
  registrar; `.wine` and `.vin` are available at Cloudflare.

## The Pi runs the pipeline, not this laptop

`pi@raspberrypi:~/vindeklaration`, on a systemd user timer at 03:00 nightly.
A full pass is hours long and a laptop sleeps through it.

**The Pi's `data/cache` is authoritative and must never be reconciled
downward.** A single `rsync --delete` of the whole tree once destroyed 11 148
fetched declarations. If the cache is ever lost again,
`deploy/rebuild-cache.py` re-derives it from `wines.json` instead of refetching.

**Everything but the cache travels through GitHub, and each direction has one
owner.** Code and the dictionaries go laptop → GitHub → Pi: `update.sh` pulls
before it crawls, so the Pi never spends a night on a stale `additives.yaml`.
The dataset goes Pi → GitHub → laptop: **only the Pi commits `data/wines.json`,
`data/catalog.json` and `data/unknown.json`.** Rebuild them here to check
something by all means, then throw the result away —
`git checkout -- data/wines.json` — because committing it from two machines is
what turns a fast-forward into a merge conflict in a 16 MB file. `wines.sqlite`
is gitignored; it is regenerated from `wines.json`.

`deploy/push-to-pi.sh` is for the first install only, when there is no clone on
the far end yet. After that, use git.

Requests are sequential, 0.4 s apart, identified by User-Agent, and inside what
`robots.txt` allows. Do not parallelise, and do not speed up to catch up after
an outage.

## Open decisions

- **The quality gate is 2%; the real figure is 9.0%.** The gate was set on a
  guess before anyone had seen the corpus. 360 unknown words remain and 252 of
  them block exactly one wine each, so reaching 2% means grinding through
  source-text typos. Recalibrating the gate is the owner's call — do not change
  `QUALITY_GATE` without being asked.
- Declaration coverage is 19.3% today and rises on its own as stock rotates to
  2024-and-later vintages. Expect the numbers in `README.md` to age.

## Reporting to the owner

State what was verified and how, and say plainly what was not. If a run failed,
show it. Do not promise to check back later on a long job — this session only
executes when something wakes it; give an estimate of when to ask instead.

# Working on this repository

An open dataset of the additives declared in wines sold by Systembolaget, and
(next) a bilingual site on top of it at **vindeklaration.se**. `README.md`
explains the method and the caveats — read it before changing how anything is
counted. This file is about how to work here.

## Non-negotiable

- **Everything in the repository is in English.** Code, comments, commits,
  README, docs. The owner writes in Swedish and expects Swedish replies in
  chat — the repo is the exception, not the conversation.
- **None of the owner's personal data, ever.** The only approved identifier is
  the GitHub username `matalve`. Not the owner's real name, not even the first
  name, and not an email address. The repo is configured to commit as
  `matalve <71018760+matalve@users.noreply.github.com>`; do not override it
  with `git -c user.email=...`. History has been rewritten once already to
  remove a personal address that got in this way.
  **This rule is about the owner, not about third parties** — clarified
  2026-07-28. Systembolaget publishes some suppliers under a sole trader's own
  name, so `data/wines.json` carries about eight values that are personal names
  (`Jessica Mihai`, `Staffan Ottosson`, `Ludvig Sääf` and a handful more, on
  some 24 wines). That is approved: it is public business information, taken
  verbatim from the source, and stripping it would misattribute the wines. It
  does have a separate consequence for the importer table, since förtal reaches
  a natural person where it does not reach a company — see *Naming importers*
  in `docs/site-plan.md`.
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
| `src/site.py`, `templates/` | the static site — `uv run python -m src.site` |
| `docs/deploy-site.md` | Cloudflare and the DNS move, step by step |
| `docs/elabel-platforms.md` | which e-label platforms can be read, and which cannot |
| `.claude/agents/` | lexicon-curator, declaration-auditor, upstream-scout, domain-scout, legal-scout, declaration-finder, site-auditor |

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

**`robots.txt` is not the whole permission set.** Systembolaget's Allmänna
användarvillkor (version 2026-04-21) clause 1.7 prohibits crawlers used to
collect information for services providing *information om alkoholdrycker*,
with no commercial qualifier — which describes this project. Their `robots.txt`
says `Allow: /` and blocks only the cart and account pages, so the two do not
agree. **The owner read the finding on 2026-07-28 and decided to keep
crawling**, on the view that a public product API published for use, alongside
a permissive `robots.txt`, contradicts the clause. That is a documented
decision, not an oversight: do not quietly reverse it, and do not restate the
clause as though it were news. Whether a browsewrap term binds a party that
never opened an account is unresolved and is a lawyer's question —
`docs/legal-notes.md` §2k. The crawling discipline above is what makes the
decision defensible in practice, so it is not negotiable.

**One robots.txt is deliberately set aside, and only one.** Decided
2026-07-30: `declaration-finder` fetches an e-label page even where the host
disallows crawling, because that page *is* the disclosure Regulation (EU)
2021/2117 requires and a blanket `Disallow: /` on it makes mandated consumer
information unreadable to anyone comparing two bottles. The argument rests on
not crawling — only URLs already discovered from the producer's own public
linking, one request per wine, no traversal and no enumeration — and it does
not extend to producers' ordinary marketing sites, which are honoured in full.
A technological measure is a different thing and is absolute: a 401, 403, 429,
login wall or bot challenge stops the fetch and is recorded as such. See
`.claude/agents/declaration-finder.md`.

## Open decisions

- ~~The quality gate is 2%.~~ Settled 2026-07-27: the gate watches drift, not a
  level. `DRIFT_LIMIT` in `src/report.py` fails the run when the `partial`
  share rises more than one percentage point since the previous recorded run.
  The baseline lives in `data/quality-history.json`, which the Pi commits with
  the rest of the dataset — **lose that file and the next run has no baseline
  and silently passes.** Only `update.sh` passes `--record`; a manual
  `src.report` compares but never writes. Do not reintroduce an absolute
  threshold without being asked.
- Declaration coverage is 19.3% today and rises on its own as stock rotates to
  2024-and-later vintages. Expect the numbers in `README.md` to age.

## Reporting to the owner

State what was verified and how, and say plainly what was not. If a run failed,
show it. Do not promise to check back later on a long job — this session only
executes when something wakes it; give an estimate of when to ask instead.

## Communication preferences

- Keep responses focused, brief, and concise.
- Keep disclaimers and caveats short, and spend most of the response on the main answer.
- When asked to explain something, give a high-level summary unless an in-depth explanation is specifically requested.
- Explain tradeoffs clearly when there is non-obvious risk.
- If something cannot be verified locally, say so explicitly.
- Before your first tool call, say in one sentence what you're about to do. While working, give a brief update only when you find something important or change direction. When you finish, lead with the outcome: your first sentence should answer "what happened" or "what did you find," with supporting detail after it for readers who want it.
- Match the length of written documents to what the task needs: cover the substance, but do not pad with filler sections, redundant summaries, or boilerplate.
- Deliver what was asked, at the scope intended. Make routine judgment calls yourself, and check in only when different readings of the request would lead to materially different work. If the request seems mistaken or a better approach exists, say so in a sentence and continue with the task as asked rather than quietly narrowing, widening, or transforming it. Finish the whole task, and stop short of actions that are clearly beyond what was asked.
- Delegate to a subagent only for large tasks that are genuinely independent and parallelizable, such as a wide multi-file investigation. Do not delegate work you can finish yourself in a handful of tool calls, and do not use subagents to verify or double-check your own work. If one subagent can complete the task, use one rather than several, and keep spawn counts low.
- Only correct an earlier statement when the error would change the user's code, conclusions, or decisions. State corrections plainly and briefly, then continue the task. For slips that change nothing for the user, make the fix and move on without noting it.

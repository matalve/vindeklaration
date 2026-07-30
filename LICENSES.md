# What covers what

Three different things live in this repository and they are not all the same
kind of thing, so they are not under one licence.

| | Licence |
|---|---|
| Code — `src/`, `deploy/`, `templates/`, `.github/` | **MIT**, in `LICENSE` |
| The dictionaries — `data/additives.yaml`, `data/lexicon.yaml` | **CC BY-SA 4.0** |
| Documentation — `README.md`, `docs/` | **CC BY-SA 4.0** |
| The dataset — `data/wines.json`, `data/catalog.json`, `data/unknown.json` | **No licence is granted.** See below. |

## Why the dataset is not licensed

**Because it is not clear that this project has the right to license it, and
granting a permission you do not hold is worse than granting none.**

The dataset is a compilation of facts published by Systembolaget: product
numbers, names, prices, and the ingredient declarations their suppliers wrote.
None of that is this project's work. What the project did was fetch it, read
it and structure it.

Under upphovsrättslagen 49 § a compilation is protected where a large number of
items have been collected **or** where it is the result of a substantial
investment — alternatives, not cumulative conditions — and the Court of Justice
has held in *British Horseracing Board* (C-203/02) that public accessibility is
no defence, and that repeated small extractions whose cumulative effect
reconstitutes a database are caught. Whether that reaches this dataset has not
been established and would need a Swedish lawyer. `docs/legal-notes.md` §2i
sets out what was and was not found.

So instead of a licence, a statement of provenance:

> The dataset is derived from data published by Systembolaget and from
> ingredient declarations written by the wines' suppliers. This project asserts
> no rights over those underlying facts and grants no permissions over them.
> It is published so that anyone can check the site's claims against their
> source. If you intend to redistribute it or build on it, the terms are
> Systembolaget's to state, not ours — go and read them.

This is not a discouragement. Use it, quote it, check our arithmetic, tell us
where we are wrong. It is an accurate description of what we are in a position
to promise.

## Why the dictionaries are licensed, and generously

`data/additives.yaml` and `data/lexicon.yaml` are the project's own work and
the part worth having: several hundred substances with their E-numbers, their
Swedish and English names, and the aliases, misspellings and mistranslations
that appear in real declarations — `vinsya`, `konservieringsmedel`,
`kaliummetallbisulfit`, `utkast till vätska`. Each was checked against a source
before it was added, and each is a small piece of evidence about how wine
labelling is actually written.

That is given away under **CC BY-SA 4.0**: use it, change it, sell things built
on it, as long as you say where it came from and pass the same freedom on.
Share-alike rather than CC0 because the value is in the dictionary staying
correctable in public.

## The site

vindeklaration.se renders this repository. Its `/metod` page carries the same
split in plain language, in Swedish and English.

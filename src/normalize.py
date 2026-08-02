"""Step 3: turn a supplier's free-text declaration into structured additives.

The text is entered by hand by each importer, so it is inconsistent in every
way that matters: separators are missing, casing is arbitrary, E-numbers are
written both as "E334" and "E 334", and words are misspelled or mistranslated
("Arabiskt tuggummi" for gum arabic).

So we do not split on delimiters. We scan the whole string for known substances,
longest match first, strike out everything we recognised, and judge what is
left. If anything meaningful remains, the wine is marked `partial` and stays out
of the rankings — better to omit a wine than to claim it has two additives when
there is a third we failed to read.
"""

from __future__ import annotations

import functools
import re
import unicodedata
from dataclasses import dataclass, field
from pathlib import Path

import yaml
from rapidfuzz import fuzz, process

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
ADDITIVES_PATH = DATA_DIR / "additives.yaml"
LEXICON_PATH = DATA_DIR / "lexicon.yaml"

# Length-preserving cleanup so match offsets stay valid against the source text.
PUNCTUATION = ",;:()[]{}/\\*.!?\"'`+|&\n\t\r–—-"
TRANSLATION = {ord(character): " " for character in PUNCTUATION}

# The trailing negative lookahead keeps "Energivärde: E/100 ml" (energy per
# 100 ml, a nutrition-declaration convention, not an additive) from reading as
# E100 once the slash has been blanked out to a space.
E_NUMBER_RE = re.compile(r"\be\s?(\d{2,4})\s?([a-z])?\b(?!\s*ml\b)")
FUZZY_MIN_LENGTH = 5
FUZZY_THRESHOLD = 88
# Regex entries win over literal aliases regardless of length.
REGEX_PRIORITY = 10_000


def normalize_text(text: str) -> str:
    """Lowercase and blank out punctuation without changing string length."""
    return unicodedata.normalize("NFC", text).lower().translate(TRANSLATION)


def alias_pattern(alias: str) -> re.Pattern[str]:
    tokens = [re.escape(token) for token in normalize_text(alias).split()]
    if not tokens:
        return re.compile(r"(?!)")
    return re.compile(r"\b" + r"\s+".join(tokens) + r"\b")


@dataclass
class Substance:
    id: str
    bucket: str
    name: dict
    category: str | None = None
    e_number: str | None = None
    group: str | None = None
    generic: bool = False
    allergen: str | None = None
    note: dict = field(default_factory=dict)

    def as_output(self) -> dict:
        out = {"id": self.id, "name": self.name}
        if self.e_number:
            out["e_number"] = self.e_number
        if self.category:
            out["category"] = self.category
        if self.allergen:
            out["allergen"] = self.allergen
        return out


@dataclass
class Lexicon:
    substances: dict[str, Substance]
    patterns: list[tuple[re.Pattern[str], str, str]]  # pattern, kind, key
    by_e_number: dict[str, Substance]
    processing_names: dict[str, dict]
    stopwords: set[str]
    alias_index: dict[str, tuple[str, str]]  # alias -> (kind, key)
    # Aliases claimed by more than one entry. Any of these makes counting
    # arbitrary — whichever entry loaded last would win — so tests reject them.
    alias_conflicts: list[tuple[str, str, str]]


@functools.lru_cache(maxsize=1)
def load_lexicon() -> Lexicon:
    raw_substances = yaml.safe_load(ADDITIVES_PATH.read_text(encoding="utf-8"))
    lexicon_data = yaml.safe_load(LEXICON_PATH.read_text(encoding="utf-8"))

    substances: dict[str, Substance] = {}
    entries: list[tuple[str, str, str]] = []  # alias, kind, key
    substance_regexes: list[tuple[re.Pattern[str], str, str]] = []
    by_e_number: dict[str, Substance] = {}

    for item in raw_substances:
        substance = Substance(
            id=item["id"],
            bucket=item["bucket"],
            name=item["name"],
            category=item.get("category"),
            e_number=item.get("e_number"),
            group=item.get("group"),
            generic=item.get("generic", False),
            allergen=item.get("allergen"),
            note=item.get("note", {}),
        )
        substances[substance.id] = substance
        for alias in item.get("aliases", []):
            entries.append((alias, "substance", substance.id))
        # Swedish compounds are open-ended — svartvinbärskoncentrat,
        # druvmustkoncentrat, svartvinbärsarom — so some substances are matched
        # by shape rather than by an ever-growing alias list.
        for expression in item.get("regexes", []):
            substance_regexes.append(
                (re.compile(expression), "substance", substance.id)
            )
        number = substance.e_number
        if number and "-" not in number:
            by_e_number[number.lstrip("Ee")] = substance

    processing_names: dict[str, dict] = {}
    regexes: list[tuple[re.Pattern[str], str, str]] = list(substance_regexes)
    for note in lexicon_data.get("processing_notes", []):
        processing_names[note["id"]] = note["name"]
        for alias in note.get("aliases", []):
            entries.append((alias, "processing", note["id"]))
        # Some phrases have too many wordings to enumerate — "tappat i en
        # skyddande atmosfär", "kan buteljeras i skyddad atmosfär", "flaskas
        # under en skyddande atmosfär", "bottled in a protective atmosphere".
        for expression in note.get("regexes", []):
            regexes.append((re.compile(expression), "processing", note["id"]))

    for label in lexicon_data.get("category_labels", []):
        entries.append((label, "label", label))

    # Longest alias first: "metavinsyra" must win over "vinsyra", and
    # "koncentrerad druvmust" over "druvmust".
    entries.sort(key=lambda entry: len(entry[0]), reverse=True)
    patterns = regexes + [
        (alias_pattern(alias), kind, key) for alias, kind, key in entries
    ]

    alias_index: dict[str, tuple[str, str]] = {}
    alias_conflicts: list[tuple[str, str, str]] = []
    for alias, kind, key in entries:
        normalized = normalize_text(alias).strip()
        claimed = alias_index.get(normalized)
        if claimed is not None and claimed[1] != key:
            alias_conflicts.append((normalized, claimed[1], key))
        alias_index[normalized] = (kind, key)

    stopwords = {
        normalize_text(word) for word in lexicon_data.get("stopwords", [])
    }
    return Lexicon(
        substances=substances,
        patterns=patterns,
        by_e_number=by_e_number,
        processing_names=processing_names,
        stopwords=stopwords,
        alias_index=alias_index,
        alias_conflicts=alias_conflicts,
    )


def _claim(spans: list[bool], start: int, end: int) -> bool:
    """Mark a span as consumed; refuse if it overlaps something already taken."""
    if any(spans[start:end]):
        return False
    for index in range(start, end):
        spans[index] = True
    return True


@dataclass
class Parsed:
    additives: list[dict]
    gases: list[dict]
    base_ingredients: list[dict]
    processing_notes: list[dict]
    allergens: list[str]
    unknown_e_numbers: list[str]
    unknown_tokens: list[str]
    fuzzy_matches: list[tuple[str, str]]

    @property
    def additive_count(self) -> int:
        return len(self.additives)

    @property
    def status(self) -> str:
        return "partial" if self.unknown_tokens else "complete"

    def as_output(self) -> dict:
        return {
            "additive_count": self.additive_count,
            "parse_status": self.status,
            "additives": self.additives,
            "gases": self.gases,
            "base_ingredients": self.base_ingredients,
            "processing_notes": self.processing_notes,
            "allergens": self.allergens,
            "unknown_tokens": self.unknown_tokens,
        }


def parse_ingredients(text: str, known_names: list[str] | None = None) -> Parsed:
    """Parse one declaration.

    `known_names` are words already published for this wine — its grape
    varieties and its producer. Declarations sometimes name the variety instead
    of "druvor" ("Muscat (druvor)") or lead with the producer ("Prodi-druvor"),
    and no dictionary can hold every grape or winery name, so these are treated
    as known words for that wine only.
    """
    lexicon = load_lexicon()
    normalized = normalize_text(text)
    spans = [False] * len(normalized)

    # Struck out first: these are already reported in the product data, so
    # they carry no information here.
    for name in sorted(known_names or [], key=len, reverse=True):
        for match in alias_pattern(name).finditer(normalized):
            _claim(spans, match.start(), match.end())

    found_substances: dict[str, Substance] = {}
    found_processing: dict[str, dict] = {}
    unknown_e_numbers: list[str] = []
    fuzzy_matches: list[tuple[str, str]] = []

    def take_substance(substance: Substance) -> None:
        found_substances.setdefault(substance.id, substance)

    # 1. Known aliases, longest first.
    for pattern, kind, key in lexicon.patterns:
        for match in pattern.finditer(normalized):
            if not _claim(spans, match.start(), match.end()):
                continue
            if kind == "substance":
                take_substance(lexicon.substances[key])
            elif kind == "processing":
                found_processing.setdefault(
                    key, {"id": key, "name": lexicon.processing_names[key]}
                )
            # "label" spans are consumed and otherwise ignored.

    # 2. Bare E-numbers. An unrecognised one is still definitely an additive,
    #    so it is counted — it just has no name yet.
    for match in E_NUMBER_RE.finditer(normalized):
        if not _claim(spans, match.start(), match.end()):
            continue
        number = match.group(1) + (match.group(2) or "")
        substance = lexicon.by_e_number.get(number)
        if substance is not None:
            take_substance(substance)
        else:
            label = f"E{number.upper()}"
            unknown_e_numbers.append(label)
            found_substances.setdefault(
                label,
                Substance(
                    id=label.lower(),
                    bucket="additive",
                    name={"sv": label, "en": label},
                    e_number=label,
                    category="unclassified",
                ),
            )

    # 3. Whatever is left over.
    leftover = "".join(
        " " if taken else character for character, taken in zip(normalized, spans)
    )
    unknown_tokens: list[str] = []
    for token in leftover.split():
        if token in lexicon.stopwords or len(token) < 3 or token.isdigit():
            continue
        if not any(character.isalpha() for character in token):
            continue
        # 4. Spelling slips: match the leftover against every known alias.
        if len(token) >= FUZZY_MIN_LENGTH:
            match = process.extractOne(
                token,
                lexicon.alias_index.keys(),
                scorer=fuzz.ratio,
                score_cutoff=FUZZY_THRESHOLD,
            )
            if match is not None:
                kind, key = lexicon.alias_index[match[0]]
                fuzzy_matches.append((token, match[0]))
                if kind == "substance":
                    take_substance(lexicon.substances[key])
                elif kind == "processing":
                    found_processing.setdefault(
                        key, {"id": key, "name": lexicon.processing_names[key]}
                    )
                continue
        unknown_tokens.append(token)

    # 5. A specific sulfite species makes the generic "sulfiter" redundant.
    groups = {
        substance.group
        for substance in found_substances.values()
        if substance.group and not substance.generic
    }
    for key, substance in list(found_substances.items()):
        if substance.generic and substance.group in groups:
            del found_substances[key]

    additives, gases, base = [], [], []
    allergens: set[str] = set()
    for substance in found_substances.values():
        if substance.allergen:
            allergens.add(substance.allergen)
        target = {"additive": additives, "gas": gases, "base": base}[substance.bucket]
        target.append(substance.as_output())

    order = {"preservative": 0, "antioxidant": 1, "acidity_regulator": 2, "stabiliser": 3}
    additives.sort(key=lambda item: (order.get(item.get("category"), 9), item["id"]))

    return Parsed(
        additives=additives,
        gases=gases,
        base_ingredients=base,
        processing_notes=list(found_processing.values()),
        allergens=sorted(allergens),
        unknown_e_numbers=unknown_e_numbers,
        unknown_tokens=unknown_tokens,
        fuzzy_matches=fuzzy_matches,
    )

"""Fetch a page for declaration-finder and report only what matters.

The binding constraint on declaration-finder is context, not time. A producer's
page is 100-400 KB of markup, and reading it whole to decide one question --
does this page carry an ingredient list? -- spends the run's budget on
navigation chrome and base64 images.

So the page never enters the agent's context. It is fetched here, written to a
cache directory, and reduced to a report: the status, the robots.txt verdict,
the declaration terms that appear with a line of context each, and the links
that are shaped like a declaration pointer. The agent reads the report and
fetches the saved file only if the report says there is something in it.

    uv run python -m src.probe https://example.com/vino/rosso-2024

Politeness is enforced here rather than remembered: the delay is held in the
cache directory, so it applies across separate invocations, and 401, 403, 429
and the other refusals are reported once and never retried.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import time
import unicodedata
from pathlib import Path
from urllib.parse import urljoin, urlsplit

import httpx

from .http import USER_AGENT

CACHE = Path("/tmp/vindeklaration-probe")
DELAY = 0.6

# The device gate decided 2026-08-08: mobile tokens in front, our own
# identification still in the string. Only for an e-label page that answers a
# plain request with a device check. See .claude/agents/declaration-finder.md.
MOBILE_USER_AGENT = (
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) "
    "AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile " + USER_AGENT
)

# Refusals. Reported and never worked around.
HARD_REFUSALS = {401, 403, 407, 429, 451}

# What a declaration is called, in the languages the shelf is written in.
# Matched against accent-stripped text, so "alergenos" catches "alérgenos" and
# "al·lergens" catches Catalan's "al·lèrgens".
TERMS = [
    "ingredients", "ingredienti", "ingredientes", "ingredienser",
    "ingredienzen", "zutaten", "zutatenliste", "ingredience",
    "allergen", "allergene", "allergeni", "allergenes", "alergenos",
    "allergener", "allergeni",
    "sulfit", "sulphit", "solfiti", "sulfitos", "sulfits", "sulfiti",
    "nutrition", "nutrizional", "nutricional", "nahrwert", "naehrwert",
    "nutritionnel", "narings", "naringsvarde",
    "energiewert", "brennwert", "valore energetico", "valor energetico",
    "valeur energetique", "kcal", "kj/",
    "conservante", "conservant", "antioxidant", "antiossidant",
    "stabilizzante", "estabilizante", "clarifiant", "chiarificante",
    "correttore di acidita", "corrector de acidez", "regolatore di acidita",
]

# Words that make a link look like a pointer to the declaration. Matched
# against path segments and anchor text as whole words, because a substring
# match on "label" finds every "menu-label" and one on "qr" finds PHP's upload
# names. That trap has cost two runs.
LINK_WORDS = {
    "elabel", "e-label", "ulabel", "u-label", "etichetta", "etichette",
    "etiqueta", "etiquetas", "etiquette", "etikett", "etiketten",
    "ingredienti", "ingredientes", "ingredients", "ingredienser", "zutaten",
    "allergeni", "alergenos", "allergene", "allergener", "allergens",
    "alergenos", "nutrizionali", "nutricional", "nutrition", "naehrwerte",
    "nahrwerte", "declaration", "dichiarazione", "declaracion",
    "scheda", "schedatecnica", "fichatecnica", "fichetechnique",
    "downloadcenter", "elabels",
}

# Footer boilerplate that is shaped exactly like a declaration pointer and is
# never one. `Declaración de accesibilidad` sits on most Spanish WordPress
# sites; the cookie and privacy variants are the same shape in every language.
NOT_A_DECLARATION = {
    "accesibilidad", "accessibility", "accessibilita", "accessibilite",
    "barrierefreiheit", "tillganglighet", "toegankelijkheid",
    "cookie", "cookies", "privacidad", "privacy", "privatlivspolitik",
    "datenschutz", "confidentialite", "riservatezza", "integritetspolicy",
}

# `etiqueta` is the worst word in this list: it means the declaration, and it
# also means a shop's tag archive, a gift-label customiser, a commissioned
# artwork and -- at Juan Gil -- the wine's own name. Four false positives on one
# page. These disambiguate it.
NOISE_PATHS = ("etiqueta-producto", "etiquetas-producto", "product-tag",
               "product_tag", "producttag", "/tag/", "/tags/")
NOISE_NEIGHBOURS = {
    # Etiqueta Amarilla, Azul, Plata: a range name, not a declaration.
    "amarilla", "amarillo", "azul", "plata", "negra", "negro", "roja", "rojo",
    "blanca", "blanco", "verde", "dorada", "oro", "gris",
    # a label you design and send with a present
    "regalo", "regalos", "personaliza", "personalizada", "personalizar",
    "disena", "gift",
}

# A host that names itself after the disclosure. `e-label.pernod-ricard.com`
# was missed by everything else: its path is a bare code and its anchor said
# "Click here for product information".
HOST_WORDS = {"elabel", "label", "labels", "etiqueta", "etichetta", "etikett",
              "qr", "ulabel", "declaration", "declaracion"}

# What that anchor says when it says nothing else.
POINTER_PHRASES = (
    "product information", "informacion del producto", "informacion de producto",
    "informazioni sul prodotto", "produktinformation", "informations produit",
    "produktinformationen", "product info", "mas informacion del producto",
)

# Extensions that are never a declaration page.
ASSETS = (
    ".jpg", ".jpeg", ".png", ".gif", ".webp", ".svg", ".ico", ".css", ".js",
    ".woff", ".woff2", ".ttf", ".eot", ".mp4", ".webm", ".zip", ".xml",
)

# E-label vendors seen so far. A hit tells the agent which platform it is on
# before it opens anything, and docs/elabel-platforms.md says which of them
# render server-side.
VENDORS = [
    "u-label.com", "scantrust.com", "wineplatform.it", "i-wine",
    "carmaqrcode", "ioagri", "vinoqr", "winelabel", "labelwine",
    "eulabel", "qr.wine", "v9.lu", "digitallink", "gs1",
]


def _fold(text: str) -> str:
    """Lowercase, strip accents, drop Catalan's interpunct."""
    text = unicodedata.normalize("NFKD", text.lower()).replace("·", "")
    return "".join(c for c in text if not unicodedata.combining(c))


def _visible(html: str) -> str:
    """The text a reader sees, with the noise that produces false hits gone."""
    html = re.sub(r"(?is)<(script|style|noscript|svg)\b.*?</\1>", " ", html)
    html = re.sub(r"(?is)<!--.*?-->", " ", html)
    # base64 payloads and long tokenless runs match anything; drop them.
    html = re.sub(r"data:[^\"')\s]{40,}", " ", html)
    html = re.sub(r"(?i)<br\s*/?>|</(p|div|li|tr|h[1-6]|td)>", "\n", html)
    text = re.sub(r"(?s)<[^>]+>", " ", html)
    text = (
        text.replace("&nbsp;", " ").replace("&amp;", "&")
        .replace("&#39;", "'").replace("&quot;", '"')
    )
    lines = (re.sub(r"[ \t ]+", " ", line).strip() for line in text.split("\n"))
    return "\n".join(line for line in lines if line)


def _term_hits(text: str, context: int) -> list[tuple[str, int, str]]:
    folded_lines = [_fold(line) for line in text.split("\n")]
    raw_lines = text.split("\n")
    hits: list[tuple[str, int, str]] = []
    seen: set[tuple[str, int]] = set()
    for number, folded in enumerate(folded_lines):
        for term in TERMS:
            if term not in folded or (term, number) in seen:
                continue
            seen.add((term, number))
            window = raw_lines[max(0, number - context): number + context + 1]
            hits.append((term, number + 1, " / ".join(window)[:400]))
            break
    return hits


def _anchors(html: str, base: str) -> list[tuple[str, str, set[str]]]:
    seen: dict[str, tuple[str, set[str]]] = {}
    for match in re.finditer(
        r"(?is)<a\b[^>]*href=[\"']([^\"'#]+)[\"'][^>]*>(.*?)</a>", html
    ):
        href, label = match.group(1).strip(), _visible(match.group(2))[:80]
        words = set(re.split(r"[^a-z0-9]+", _fold(urlsplit(href).path)))
        words |= set(re.split(r"[^a-z0-9]+", _fold(label)))
        seen.setdefault(urljoin(base, href), (label, words))
    return sorted((url, label, words) for url, (label, words) in seen.items())


def _links(html: str, base: str) -> list[tuple[str, str]]:
    found = []
    for url, label, words in _anchors(html, base):
        folded_url, folded_label = _fold(url), _fold(label)
        if words & NOT_A_DECLARATION:
            continue
        if any(noise in folded_url for noise in NOISE_PATHS):
            continue
        if "etiqueta" in words and words & NOISE_NEIGHBOURS:
            continue
        host_words = set(re.split(r"[^a-z0-9]+", _fold(urlsplit(url).netloc)))
        if (
            words & LINK_WORDS
            or host_words & HOST_WORDS
            or any(v in folded_url for v in VENDORS)
            or any(phrase in folded_label for phrase in POINTER_PHRASES)
        ):
            found.append((url, label))
    return found


def _same_host_links(html: str, base: str) -> list[tuple[str, str]]:
    """Every same-host page link, so a product URL needs no grep over the file."""
    host = urlsplit(base).netloc
    found = []
    for url, label, _ in _anchors(html, base):
        split = urlsplit(url)
        if split.netloc != host or split.scheme not in {"http", "https"}:
            continue
        if split.path.lower().endswith(ASSETS):
            continue
        found.append((url, label))
    return found


def _robots_groups(body: str) -> dict[str, list[str]]:
    groups: dict[str, list[str]] = {}
    agents: list[str] = []
    fresh = True
    for line in body.splitlines():
        line = line.split("#", 1)[0].strip()
        if not line or ":" not in line:
            continue
        field, _, value = line.partition(":")
        field, value = field.strip().lower(), value.strip()
        if field == "user-agent":
            if not fresh:
                agents = []
                fresh = True
            agents.append(value.lower())
            groups.setdefault(value.lower(), [])
        elif field in {"disallow", "allow"}:
            fresh = False
            for agent in agents:
                groups.setdefault(agent, []).append(f"{field}:{value}")
    return groups


def robots_verdict(client: httpx.Client, url: str, cache: dict) -> tuple[str, bool]:
    """RFC 9309 for our own token. Returns (explanation, allowed)."""
    root = f"{urlsplit(url).scheme}://{urlsplit(url).netloc}"
    if root in cache:
        return cache[root]
    prefix = ""
    try:
        response = client.get(f"{root}/robots.txt")
    except httpx.HTTPError as first_error:
        # An expired certificate must not make the host's robots.txt unreadable
        # too, or the fetch below proceeds without ever having read it.
        if not _is_expired_certificate(first_error):
            error = first_error
            response = None
        else:
            prefix = "(read over an expired certificate) "
            try:
                with httpx.Client(
                    headers={"User-Agent": USER_AGENT}, timeout=30.0,
                    follow_redirects=True, verify=False,
                ) as insecure:
                    response = insecure.get(f"{root}/robots.txt")
                error = None
            except httpx.HTTPError as second_error:
                error = second_error
                response = None
    else:
        error = None
    if response is None:
        # Owner's decision 2026-08-30: an unreachable robots.txt is a
        # misconfiguration or an outage, and neither is a publisher's refusal.
        # RFC 9309 would read it as a complete disallow; that reading closed
        # Damilano for two weeks over a 500 nobody meant.
        verdict = (
            f"unreachable ({type(error).__name__}) - a misconfiguration, "
            "not a refusal; proceeding",
            True,
        )
        cache[root] = verdict
        return verdict
    if response.status_code >= 500:
        verdict = (
            f"{response.status_code} - a misconfiguration, not a refusal; proceeding",
            True,
        )
    elif response.status_code >= 400:
        verdict = (f"{response.status_code} - absent, nothing disallowed", True)
    else:
        groups = _robots_groups(response.text)
        ours = [name for name in groups if name and name in _fold(USER_AGENT)]
        if ours:
            rules = groups[ours[0]]
            blocked = any(
                rule.startswith("disallow:")
                and urlsplit(url).path.startswith(rule.split(":", 1)[1] or "/")
                and rule.split(":", 1)[1] != ""
                for rule in rules
            )
            verdict = (f"group '{ours[0]}' matches us: {rules or ['(empty)']}", not blocked)
        elif "*" in groups:
            rules = groups["*"]
            path = urlsplit(url).path or "/"
            blocked = any(
                rule.startswith("disallow:")
                and rule.split(":", 1)[1]
                and path.startswith(rule.split(":", 1)[1])
                for rule in rules
            )
            verdict = (
                f"wildcard group: {rules or ['(empty)']}",
                not blocked,
            )
        else:
            # Decided 2026-08-08: named groups only, none matching our token,
            # so under RFC 9309 no rule applies to us.
            verdict = (
                f"named groups only ({', '.join(sorted(groups)) or 'none'}), "
                "none matches our token - nothing disallowed",
                True,
            )
    verdict = (prefix + verdict[0], verdict[1])
    cache[root] = verdict
    return verdict


def _is_expired_certificate(error: Exception) -> bool:
    """True only for expiry, which the owner ruled is not a refusal.

    Decided 2026-08-30, on Bodegas Frutos Villar: a certificate that ran out
    yesterday says nothing about whether the site wants to be read. Every other
    TLS failure is a claim about *who* answered, and those still stop the fetch.
    """
    text = " ".join(str(part) for part in (error, error.__cause__, error.__context__))
    return "certificate has expired" in text.lower() or "certificate_expired" in text.lower()


def _wait() -> None:
    CACHE.mkdir(parents=True, exist_ok=True)
    stamp = CACHE / ".last-request"
    if stamp.exists():
        elapsed = time.time() - stamp.stat().st_mtime
        if elapsed < DELAY:
            time.sleep(DELAY - elapsed)
    stamp.touch()


def probe(url: str, options: argparse.Namespace, robots_cache: dict) -> dict:
    agent = MOBILE_USER_AGENT if options.mobile else USER_AGENT
    client = httpx.Client(
        headers={"User-Agent": agent},
        timeout=30.0,
        follow_redirects=True,
    )
    report: dict = {"url": url}
    with client:
        if not options.no_robots_check:
            _wait()
            explanation, allowed = robots_verdict(client, url, robots_cache)
            report["robots"] = explanation
            if not allowed and not options.elabel_exception:
                # Say which kind of stop this is, so a run never refetches to
                # find out what the message meant.
                report["stopped"] = (
                    f"not fetched: robots.txt {explanation}, and no "
                    "--elabel-exception was given"
                )
                return report
            if not allowed:
                report["exception_used"] = options.elabel_exception
        _wait()
        try:
            response = client.get(url)
        except httpx.HTTPError as error:
            if not _is_expired_certificate(error):
                report["stopped"] = f"{type(error).__name__}: {error}"
                return report
            report["tls"] = (
                "certificate expired; fetched without verification "
                "(owner's decision 2026-08-30). Record this in the wine's record."
            )

    if "tls" in report:
        # Only expiry, and only after the verified attempt failed on it. A
        # hostname mismatch or an untrusted issuer is a different claim about
        # who answered, and it still stops the fetch.
        _wait()
        with httpx.Client(
            headers={"User-Agent": agent}, timeout=30.0,
            follow_redirects=True, verify=False,
        ) as insecure:
            try:
                response = insecure.get(url)
            except httpx.HTTPError as error:
                report["stopped"] = f"{type(error).__name__}: {error}"
                return report

    report["status"] = response.status_code
    report["final_url"] = str(response.url)
    report["content_type"] = response.headers.get("content-type", "")
    body = response.content
    report["bytes"] = len(body)
    if options.mobile:
        report["user_agent"] = "mobile-shaped, self-identifying"

    if response.status_code in HARD_REFUSALS:
        report["stopped"] = (
            f"{response.status_code} is a refusal - not retried, not worked around"
        )
        return report

    digest = hashlib.sha1(url.encode()).hexdigest()[:12]
    suffix = ".pdf" if "pdf" in report["content_type"] else ".html"
    saved = CACHE / f"{digest}{suffix}"
    saved.write_bytes(body)
    report["saved"] = str(saved)

    if suffix == ".pdf":
        report["note"] = "PDF saved; no text extractor available in this environment"
        return report

    html = body.decode(response.encoding or "utf-8", errors="replace")
    text = _visible(html)
    report["visible_chars"] = len(text)
    report["terms"] = [
        {"term": term, "line": line, "context": context}
        for term, line, context in _term_hits(text, options.context)
    ]
    report["links"] = [{"url": href, "text": label} for href, label in _links(html, str(response.url))]
    if options.links:
        report["same_host_links"] = [
            {"url": href, "text": label}
            for href, label in _same_host_links(html, str(response.url))
        ]
    vendors = sorted({v for v in VENDORS if v in _fold(html)})
    if vendors:
        report["vendors_mentioned"] = vendors
    return report


def render(report: dict) -> str:
    lines = [f"== {report['url']}"]
    for key in ("robots", "exception_used", "tls", "status", "final_url",
                "content_type", "bytes", "user_agent", "saved", "visible_chars",
                "note", "stopped"):
        if key in report and report[key] != report.get("url"):
            lines.append(f"{key}: {report[key]}")
    if report.get("stopped"):
        return "\n".join(lines)
    if report.get("vendors_mentioned"):
        lines.append(f"vendors_mentioned: {', '.join(report['vendors_mentioned'])}")
    terms = report.get("terms", [])
    lines.append(f"terms: {len(terms)} hit(s)")
    for hit in terms[:40]:
        lines.append(f"  L{hit['line']} {hit['term']}: {hit['context']}")
    if len(terms) > 40:
        lines.append(f"  ... {len(terms) - 40} more, read the saved file")
    links = report.get("links", [])
    lines.append(f"declaration-shaped links: {len(links)}")
    for link in links[:25]:
        lines.append(f"  {link['url']}  [{link['text']}]")
    same_host = report.get("same_host_links")
    if same_host is not None:
        lines.append(f"same-host page links: {len(same_host)}")
        for link in same_host[:120]:
            lines.append(f"  {link['url']}  [{link['text']}]")
        if len(same_host) > 120:
            lines.append(f"  ... {len(same_host) - 120} more, read the saved file")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("urls", nargs="+")
    parser.add_argument("--context", type=int, default=1,
                        help="lines of context around each term hit")
    parser.add_argument("--links", action="store_true",
                        help="also list every same-host page link, for finding "
                             "product URLs without grepping the saved file")
    parser.add_argument("--mobile", action="store_true",
                        help="device-gated e-label page only; see the agent file")
    parser.add_argument("--elabel-exception", metavar="REASON",
                        help="fetch despite a disallow, because the page is the "
                             "regulated disclosure; the reason is echoed for the record")
    parser.add_argument("--no-robots-check", action="store_true",
                        help="robots already read for this host in this run")
    parser.add_argument("--json", action="store_true")
    options = parser.parse_args(argv)

    robots_cache: dict = {}
    reports = [probe(url, options, robots_cache) for url in options.urls]
    if options.json:
        print(json.dumps(reports, ensure_ascii=False, indent=2))
    else:
        print("\n\n".join(render(report) for report in reports))
    return 0


if __name__ == "__main__":
    sys.exit(main())

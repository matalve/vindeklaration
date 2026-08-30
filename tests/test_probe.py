"""The parts of src.probe that decide something, tested without a network."""

from src.probe import _fold, _links, _robots_groups, _term_hits, _visible

PAGE = """
<html><head><style>.menu-label{color:red}</style></head><body>
<nav><a href="/menu-label/x">Menu</a>
<a href="/es/etiqueta-electronica">Etiqueta electr&oacute;nica</a></nav>
<h2>Al&middot;l&egrave;rgens</h2><p>Cont&eacute; sulfits</p>
<div>Ingredientes: uva, sulfitos</div>
<a href="/uploads/phpvWdQrT.jpg">foto</a>
<script>var qrLabel = "ingredients";</script>
</body></html>
"""


def test_fold_strips_accents_and_the_catalan_interpunct():
    assert _fold("Al·lèrgens") == "allergens"
    assert _fold("Información") == "informacion"


def test_visible_drops_script_and_style():
    text = _visible(PAGE)
    assert "qrLabel" not in text
    assert "color:red" not in text
    assert "Ingredientes: uva, sulfitos" in text


def test_visible_drops_base64_payloads():
    html = '<img src="data:image/png;base64,' + "iVBORw0KGgo" * 20 + '"><p>Zutaten</p>'
    text = _visible(html)
    assert "iVBORw0KGgo" not in text
    assert "Zutaten" in text


def test_term_hits_find_the_declaration_words():
    found = {term for term, _, _ in _term_hits(_visible(PAGE), 1)}
    assert "ingredientes" in found
    assert "sulfit" in found


def test_links_ignore_menu_label_and_php_upload_names():
    found = dict(_links(PAGE, "https://example.test/"))
    assert "https://example.test/es/etiqueta-electronica" in found
    assert not any("menu-label" in url for url in found)
    assert not any("phpvWdQrT" in url for url in found)


def test_robots_groups_keep_named_groups_apart():
    groups = _robots_groups(
        "User-agent: ClaudeBot\nDisallow: /\n\nUser-agent: GPTBot\nDisallow: /\n"
    )
    assert set(groups) == {"claudebot", "gptbot"}
    assert "*" not in groups


def test_robots_groups_merge_stacked_user_agents():
    groups = _robots_groups("User-agent: a\nUser-agent: b\nDisallow: /x\n")
    assert groups["a"] == groups["b"] == ["disallow:/x"]

"""The parts of src.probe that decide something, tested without a network."""

from src.probe import (
    _fold,
    _is_expired_certificate,
    _links,
    _robots_groups,
    _same_host_links,
    _term_hits,
    _visible,
)

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


FOOTER = """
<a href="/es/declaracion-de-accesibilidad">Declaración de accesibilidad</a>
<a href="/politica-de-cookies">Cookies</a>
<a href="/es/vinos/el-fanio-2024">El Fanio 2024</a>
<a href="/wp-content/uploads/logo.png">logo</a>
<a href="https://otro.test/vinos/x">otro</a>
"""


def test_links_skip_accessibility_and_cookie_footers():
    found = dict(_links(FOOTER, "https://bodega.test/"))
    assert found == {}


def test_same_host_links_skip_assets_and_other_hosts():
    found = dict(_same_host_links(FOOTER, "https://bodega.test/"))
    assert "https://bodega.test/es/vinos/el-fanio-2024" in found
    assert not any(url.endswith(".png") for url in found)
    assert not any("otro.test" in url for url in found)


def test_only_an_expired_certificate_counts_as_expired():
    expired = Exception(
        "[SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: "
        "certificate has expired (_ssl.c:992)"
    )
    assert _is_expired_certificate(expired)
    for other in (
        "certificate verify failed: self-signed certificate",
        "Hostname mismatch, certificate is not valid for 'x.test'",
        "unable to get local issuer certificate",
    ):
        assert not _is_expired_certificate(Exception(other))


def test_expiry_is_recognised_through_the_exception_chain():
    inner = Exception("certificate has expired")
    outer = Exception("connect error")
    outer.__cause__ = inner
    assert _is_expired_certificate(outer)


CAMPO = """
<a href="https://e-label.pernod-ricard.com/L004YJ">Click here for product information</a>
<a href="/es/etiqueta-producto/tinto/">Etiqueta producto</a>
<a href="/vinos/etiqueta-amarilla">Juan Gil Etiqueta Amarilla</a>
<a href="/tienda/etiqueta-regalo">Etiqueta de regalo personalizada</a>
<a href="/es/etiqueta-electronica/x">Etiqueta electrónica</a>
"""


def test_links_find_a_host_that_names_itself_after_the_disclosure():
    found = dict(_links(CAMPO, "https://www.campoviejo.test/vino/"))
    assert "https://e-label.pernod-ricard.com/L004YJ" in found


def test_links_reject_the_four_other_meanings_of_etiqueta():
    found = dict(_links(CAMPO, "https://www.campoviejo.test/vino/"))
    assert not any("etiqueta-producto" in url for url in found)
    assert not any("etiqueta-amarilla" in url for url in found)
    assert not any("etiqueta-regalo" in url for url in found)
    # the real one still survives
    assert "https://www.campoviejo.test/es/etiqueta-electronica/x" in found

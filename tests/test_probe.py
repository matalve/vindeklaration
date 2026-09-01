"""The parts of src.probe that decide something, tested without a network."""

import pathlib
import shutil

import pytest

from src import probe as probe_module
from src.probe import (
    _fold,
    decode_codes,
    _is_expired_certificate,
    _links,
    _robots_groups,
    _same_host_links,
    _term_hits,
    _visible,
    ocr,
    pdf_text,
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


FIXTURES = pathlib.Path(__file__).parent / "fixtures" / "probe"


@pytest.mark.skipif(not shutil.which("zbarimg"), reason="zbar-tools not installed")
def test_a_qr_code_decodes_to_its_url():
    codes, _ = decode_codes(FIXTURES / "qr.png")
    assert codes == ["https://u-label.com/qr/ABC123"]


@pytest.mark.skipif(not shutil.which("pdftotext"), reason="poppler-utils not installed")
def test_a_pdf_text_layer_is_read_without_ocr():
    text = pdf_text(FIXTURES / "ficha.pdf")
    assert "INGREDIENTES" in text
    assert "sulfitos" in text


@pytest.mark.skipif(not shutil.which("tesseract"), reason="tesseract not installed")
def test_ocr_reads_a_rendered_page():
    text = ocr(FIXTURES / "ficha.pdf", "spa+eng")
    assert "INGREDIENTES" in text.upper()


def test_a_missing_decoder_reports_nothing_rather_than_a_code(monkeypatch):
    """The bug this guards: _run used to return the failure as text, so a
    missing zbarimg became one decoded line and the report printed a `code:`
    for a QR nobody had read. An exact result invented by an absent tool is
    the one thing this fetcher must never produce."""
    monkeypatch.setattr(probe_module.shutil, "which", lambda _: None)
    codes, _ = decode_codes(FIXTURES / "qr.png")
    assert codes == []
    assert pdf_text(FIXTURES / "ficha.pdf") == ""
    assert ocr(FIXTURES / "ficha.pdf", "spa+eng") == ""


def test_an_age_gate_class_is_not_a_declaration_pointer():
    html = '<a href="/js/age-gate-label.js">Age gate</a>'
    assert _links(html, "https://bodega.test/") == []

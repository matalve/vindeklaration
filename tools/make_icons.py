"""Draw the site icon: one geometry, an SVG and the PNG fallbacks.

Run when the mark changes, not on every build — the results are committed:

    python3 tools/make_icons.py

The mark is a wine glass whose bowl is three rules, so it says *declaration*
and *wine* in one shape. Everything is an axis-aligned rectangle on a 16-unit
grid, which is the whole trick: at 16 px, the size a browser tab actually
shows, every edge lands on a pixel boundary and nothing blurs. Earlier drafts
used seven rules and turned into a grey smear with moiré below 32 px.

No dependency is used to rasterise. The shape is rectangles, so the PNG encoder
below is a few lines of zlib, and adding Pillow or cairosvg to the project — and
therefore to Cloudflare's build — to draw five flat squares would be the wrong
trade.
"""

from __future__ import annotations

import struct
import zlib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "templates" / "icons"

# Wine, and the lightened wine the dark theme uses. Same two values as
# --accent in templates/site.css; if those change, these do.
INK_LIGHT = (0x6B, 0x27, 0x37)
INK_DARK = (0xE8, 0xA0, 0xAD)

# x, y, width, height on a 16×16 grid. Read top to bottom: three rules
# narrowing into the bowl, then the stem, then the foot. One unit of gap
# between the rules — less and they merge at 16 px, more and the glass falls
# apart into stripes.
SHAPES = [
    (2, 1, 12, 2),   # rule 1, widest
    (3, 4, 10, 2),   # rule 2
    (4, 7, 8, 2),    # rule 3, the base of the bowl
    (7, 9, 2, 4),    # stem
    (3, 13, 10, 2),  # foot
]
GRID = 16


def svg() -> str:
    """One file for both themes: an SVG icon may carry its own media query."""
    rects = "\n".join(
        f'  <rect x="{x}" y="{y}" width="{w}" height="{h}" rx="0.4"/>'
        for x, y, w, h in SHAPES
    )
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {GRID} {GRID}">
  <title>vindeklaration</title>
  <style>
    /* Wine on a light tab strip, lightened wine on a dark one. Firefox and
       Chrome honour this in an SVG favicon; Safari falls back to the PNG. */
    :root {{ fill: rgb{INK_LIGHT}; }}
    @media (prefers-color-scheme: dark) {{ :root {{ fill: rgb{INK_DARK}; }} }}
  </style>
{rects}
</svg>
"""


def coverage(px: int, py: int, size: int, samples: int = 4) -> float:
    """How much of one output pixel the mark covers, by supersampling.

    Only needed where the output size is not a multiple of 16 — 180 is not, so
    its edges would otherwise stair-step. At 32 every sample agrees and this
    returns 0.0 or 1.0, which is why that file has no soft edge at all.
    """
    scale = GRID / size
    hits = 0
    for sy in range(samples):
        for sx in range(samples):
            gx = (px + (sx + 0.5) / samples) * scale
            gy = (py + (sy + 0.5) / samples) * scale
            for x, y, w, h in SHAPES:
                if x <= gx < x + w and y <= gy < y + h:
                    hits += 1
                    break
    return hits / (samples * samples)


def png(size: int, ink: tuple[int, int, int]) -> bytes:
    """A transparent RGBA PNG of the mark, written without an image library."""
    rows = bytearray()
    for py in range(size):
        rows.append(0)  # filter type 0 for the scanline
        for px in range(size):
            alpha = coverage(px, py, size)
            rows += bytes((*ink, round(alpha * 255)))

    def chunk(tag: bytes, payload: bytes) -> bytes:
        return (
            struct.pack(">I", len(payload))
            + tag
            + payload
            + struct.pack(">I", zlib.crc32(tag + payload) & 0xFFFFFFFF)
        )

    header = struct.pack(">IIBBBBB", size, size, 8, 6, 0, 0, 0)  # 8-bit RGBA
    return (
        b"\x89PNG\r\n\x1a\n"
        + chunk(b"IHDR", header)
        + chunk(b"IDAT", zlib.compress(bytes(rows), 9))
        + chunk(b"IEND", b"")
    )


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "favicon.svg").write_text(svg(), encoding="utf-8")
    # 32 for the tab where SVG favicons are unsupported, 180 for an iOS home
    # screen. Both are drawn in the light ink: neither surface tells us its
    # background, and wine on a pale tab strip is the safer of the two guesses.
    # No 512 and no web manifest — the site is not an installable app, and an
    # asset nothing references is an asset nobody maintains.
    for size, ink, name in [
        (32, INK_LIGHT, "favicon-32.png"),
        (180, INK_LIGHT, "apple-touch-icon.png"),
    ]:
        (OUT / name).write_bytes(png(size, ink))
    for path in sorted(OUT.iterdir()):
        print(f"{path.name:24} {path.stat().st_size:>7} bytes")


if __name__ == "__main__":
    main()

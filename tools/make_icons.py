"""Draw the site icons and the sharing card from the header glass.

Run when the mark changes, not on every build — the results are committed:

    python3 tools/make_icons.py

The mark is the wine glass the site header draws, and the four path strings
below are that glass verbatim. The favicon is not a second drawing of it: it
is one window onto the same geometry, `viewBox="0.5 3.4 27 27"` turned -18
degrees, so the tab and the header can never drift apart. Chosen 2026-08-24
after the alternatives were rasterised and compared at true 16 px.

The paths are parsed rather than duplicated as coordinate tables. One source
of truth: change a curve here and the SVG, the PNGs, the ICO and the sharing
card all move together.

No dependency is used to rasterise. Earlier the mark was five rectangles and
the encoder was a few lines of zlib; now it is four curves, so the sampling
predicate is "within half a stroke of a flattened polyline" instead of "inside
a rectangle". That is thirty lines more. Adding Pillow or cairosvg to the
project — and therefore to Cloudflare's build — is still the wrong trade.

**The one thing that is not scaled exactly is stroke weight.** The header
strokes 2.2 units in a 28x54 space; carried through the crop factor that lands
near 1.3 px in a 16 px icon and washes out to grey. The icons are therefore
drawn at a constant 2.0 units on a 16-unit grid — the shape is exact, the
weight is optically compensated, the way any icon set does it.

The rectangles are gone and with them the promise that every edge landed on a
whole pixel at 16 px. A curve at that size is antialiased; there is no version
of this mark that is both the header's glass and pixel-crisp in a tab strip.
"""

from __future__ import annotations

import math
import re
import struct
import zlib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "templates" / "icons"

# Wine, and the lightened wine the dark theme uses. Same two values as
# --accent in templates/site.css; if those change, these do. PAPER is
# --paper, and is needed wherever an icon may not be transparent.
INK_LIGHT = (0x6B, 0x27, 0x37)
INK_DARK = (0xE8, 0xA0, 0xAD)
PAPER_LIGHT = (0xFA, 0xF8, 0xF5)

# The header glass. Four paths in a 28x54 space: the bowl as one unbroken
# curve so its sides meet without a seam, the rim seen a little from above,
# the stem, and the foot.
GLASS = (
    "M4 5C4 17 7 24 14 26C21 24 24 17 24 5",
    "M4 5Q14 9 24 5",
    "M14 26V45",
    "M6.5 48Q14 43.5 21.5 48",
)
GLASS_BOX = (28.0, 54.0)
HEADER_STROKE = 2.2  # what the header itself strokes, for the sharing card

# The favicon window: origin, side, and the turn. -18 degrees rather than the
# header's own 7: at icon size seven degrees reads as hung crooked, eighteen
# reads as meant.
CROP_X, CROP_Y, CROP_SIDE = 0.5, 3.4, 27.0
CROP_TURN = -18.0
# Icon units on a 16-unit grid. See the note on weight in the docstring.
ICON_STROKE = 2.0


# --- geometry ---------------------------------------------------------------


def parse(d: str) -> list[list[tuple[float, float]]]:
    """Flatten one path string to polylines. Handles the commands we use."""
    tokens = re.findall(r"[MCQVLZ]|-?\d*\.?\d+", d.upper())
    polys: list[list[tuple[float, float]]] = []
    cur: list[tuple[float, float]] = []
    i = 0
    x = y = 0.0
    while i < len(tokens):
        cmd = tokens[i]
        i += 1

        def num() -> float:
            nonlocal i
            v = float(tokens[i])
            i += 1
            return v

        if cmd == "M":
            if cur:
                polys.append(cur)
            x, y = num(), num()
            cur = [(x, y)]
        elif cmd == "L":
            x, y = num(), num()
            cur.append((x, y))
        elif cmd == "V":
            y = num()
            cur.append((x, y))
        elif cmd == "C":
            x1, y1, x2, y2, x3, y3 = (num() for _ in range(6))
            cur += bezier((x, y), (x1, y1), (x2, y2), (x3, y3))
            x, y = x3, y3
        elif cmd == "Q":
            x1, y1, x2, y2 = (num() for _ in range(4))
            cur += quad((x, y), (x1, y1), (x2, y2))
            x, y = x2, y2
        elif cmd == "Z":
            cur.append(cur[0])
    if cur:
        polys.append(cur)
    return polys


def bezier(p0, p1, p2, p3, n: int = 28):
    out = []
    for k in range(1, n + 1):
        t = k / n
        u = 1 - t
        out.append((
            u * u * u * p0[0] + 3 * u * u * t * p1[0] + 3 * u * t * t * p2[0] + t ** 3 * p3[0],
            u * u * u * p0[1] + 3 * u * u * t * p1[1] + 3 * u * t * t * p2[1] + t ** 3 * p3[1],
        ))
    return out


def quad(p0, p1, p2, n: int = 20):
    out = []
    for k in range(1, n + 1):
        t = k / n
        u = 1 - t
        out.append((
            u * u * p0[0] + 2 * u * t * p1[0] + t * t * p2[0],
            u * u * p0[1] + 2 * u * t * p1[1] + t * t * p2[1],
        ))
    return out


def glass_polys() -> list[list[tuple[float, float]]]:
    return [poly for d in GLASS for poly in parse(d)]


def place(polys, scale: float, dx: float, dy: float, turn: float = 0.0, about=(0.0, 0.0)):
    """Turn about a point, then scale and offset. Straight affine, no reshaping."""
    a = math.radians(turn)
    ca, sa = math.cos(a), math.sin(a)
    out = []
    for poly in polys:
        pts = []
        for x, y in poly:
            ox, oy = x - about[0], y - about[1]
            rx, ry = ox * ca - oy * sa, ox * sa + oy * ca
            pts.append(((rx + about[0]) * scale + dx, (ry + about[1]) * scale + dy))
        out.append(pts)
    return out


def icon_polys(size: int) -> tuple[list, float]:
    """The favicon crop, in pixels, plus the stroke radius to match."""
    polys = glass_polys()
    k = size / CROP_SIDE
    centre = (CROP_X + CROP_SIDE / 2, CROP_Y + CROP_SIDE / 2)
    placed = place(polys, k, -CROP_X * k, -CROP_Y * k, CROP_TURN, centre)
    return placed, ICON_STROKE * size / 16.0 / 2.0


# --- rasterising ------------------------------------------------------------


def rows_index(polys, height: int, pad: float):
    """Which segments can touch which output row.

    Without this the sharing card is a minute of arithmetic: 750 000 pixels
    times every segment of every curve. With it each pixel sees a handful.
    """
    index: list[list] = [[] for _ in range(height)]
    for poly in polys:
        for i in range(len(poly) - 1):
            seg = (poly[i], poly[i + 1])
            lo = max(0, int(min(seg[0][1], seg[1][1]) - pad))
            hi = min(height - 1, int(max(seg[0][1], seg[1][1]) + pad) + 1)
            for r in range(lo, hi + 1):
                index[r].append(seg)
    return index


def coverage(polys, width: int, height: int, half: float, samples: int = 4):
    """How much of each pixel the stroked mark covers, by supersampling.

    Same shape as the rectangle version this replaced: sample a grid inside the
    pixel and ask a predicate. The predicate is now distance to a segment.
    """
    index = rows_index(polys, height, half + 2)
    out = bytearray(width * height)
    for py in range(height):
        segs = index[py]
        if not segs:
            continue
        for px in range(width):
            hits = 0
            for sy in range(samples):
                gy = py + (sy + 0.5) / samples
                for sx in range(samples):
                    gx = px + (sx + 0.5) / samples
                    for (ax, ay), (bx, by) in segs:
                        dx, dy = bx - ax, by - ay
                        length = dx * dx + dy * dy
                        t = 0.0 if length == 0 else (gx - ax) * dx + (gy - ay) * dy
                        if length:
                            t = 0.0 if t < 0 else (1.0 if t > length else t / length)
                        qx, qy = ax + t * dx, ay + t * dy
                        if (gx - qx) ** 2 + (gy - qy) ** 2 <= half * half:
                            hits += 1
                            break
            if hits:
                out[py * width + px] = round(hits / (samples * samples) * 255)
    return out


def png(width: int, height: int, alpha: bytearray, ink, ground=None) -> bytes:
    """RGBA if ground is None, otherwise the mark composited onto an opaque one."""
    rows = bytearray()
    for y in range(height):
        rows.append(0)  # filter type 0 for the scanline
        base = y * width
        for x in range(width):
            a = alpha[base + x]
            if ground is None:
                rows += bytes((*ink, a))
            else:
                f = a / 255
                rows += bytes((
                    round(ground[0] * (1 - f) + ink[0] * f),
                    round(ground[1] * (1 - f) + ink[1] * f),
                    round(ground[2] * (1 - f) + ink[2] * f),
                    255,
                ))
    def chunk(tag: bytes, payload: bytes) -> bytes:
        return (
            struct.pack(">I", len(payload))
            + tag
            + payload
            + struct.pack(">I", zlib.crc32(tag + payload) & 0xFFFFFFFF)
        )

    header = struct.pack(">IIBBBBB", width, height, 8, 6, 0, 0, 0)  # 8-bit RGBA
    return (
        b"\x89PNG\r\n\x1a\n"
        + chunk(b"IHDR", header)
        + chunk(b"IDAT", zlib.compress(bytes(rows), 9))
        + chunk(b"IEND", b"")
    )


def ico(images: list[tuple[int, bytes]]) -> bytes:
    """An ICO wrapping PNGs — a header, one entry each, then the files."""
    offset = 6 + 16 * len(images)
    head = struct.pack("<HHH", 0, 1, len(images))
    entries, blobs = b"", b""
    for size, blob in images:
        entries += struct.pack(
            "<BBBBHHII", size, size, 0, 0, 1, 32, len(blob), offset
        )
        blobs += blob
        offset += len(blob)
    return head + entries + blobs


# --- the vector files -------------------------------------------------------


def svg(themed: bool) -> str:
    """The crop as SVG. The same four paths, inside a turned group.

    The stroke is 3.375 rather than 2.0: the viewBox is 27 units across and
    the icon renders at 16, so this is 2.0 icon units expressed in glass units.
    """
    paths = "\n".join(f'    <path d="{d}"/>' for d in GLASS)
    if themed:
        style = f"""  <style>
    /* Wine on a light tab strip, lightened wine on a dark one. Firefox and
       Chrome honour this in an SVG favicon; Safari falls back to the PNG. */
    :root {{ stroke: rgb{INK_LIGHT}; }}
    @media (prefers-color-scheme: dark) {{ :root {{ stroke: rgb{INK_DARK}; }} }}
  </style>
"""
        stroke = ""
    else:
        # Safari's pinned tab takes the shape and applies its own tint, so the
        # file is a plain silhouette with no media query to confuse it.
        style = ""
        stroke = ' stroke="#000"'
    half = CROP_SIDE / 2
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {CROP_SIDE:g} {CROP_SIDE:g}">
  <title>vindeklaration</title>
{style}  <g fill="none"{stroke} stroke-width="{ICON_STROKE * CROP_SIDE / 16:g}"
     stroke-linecap="round" stroke-linejoin="round"
     transform="rotate({CROP_TURN:g} {half:g} {half:g}) translate({-CROP_X:g} {-CROP_Y:g})">
{paths}
  </g>
</svg>
"""


# --- the sharing card -------------------------------------------------------

CARD_W, CARD_H = 1200, 627
CARD_GLASS_H = 430


def card() -> bytes:
    """og:image — the whole glass on paper, no crop and no words.

    1200x627 rather than 630, matching the sibling site. The glass is not
    cropped here: the reason the favicon is a window is that 16 px cannot hold
    a shape twice as tall as it is wide, and a sharing card has no such
    problem. Nothing is written on it — text would need a font rasteriser, and
    the title and description travel in the meta tags anyway.
    """
    scale = CARD_GLASS_H / GLASS_BOX[1]
    polys = place(
        glass_polys(),
        scale,
        (CARD_W - GLASS_BOX[0] * scale) / 2,
        (CARD_H - CARD_GLASS_H) / 2,
    )
    half = HEADER_STROKE * scale / 2
    alpha = coverage(polys, CARD_W, CARD_H, half, samples=2)
    return png(CARD_W, CARD_H, alpha, INK_LIGHT, PAPER_LIGHT)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "favicon.svg").write_text(svg(themed=True), encoding="utf-8")
    (OUT / "safari-pinned-tab.svg").write_text(svg(themed=False), encoding="utf-8")

    # 16 and 32 for the tab and the ICO, 180 for an iOS home screen. The two
    # tab sizes stay transparent; the Apple icon must not. iOS composites a
    # transparent home-screen icon against black, and the mark is dark wine —
    # so it gets the paper painted under it. See issue #8.
    blobs = {}
    for size, ground in ((16, None), (32, None), (180, PAPER_LIGHT)):
        polys, half = icon_polys(size)
        alpha = coverage(polys, size, size, half)
        blobs[size] = png(size, size, alpha, INK_LIGHT, ground)

    (OUT / "favicon-32.png").write_bytes(blobs[32])
    (OUT / "apple-touch-icon.png").write_bytes(blobs[180])
    # A real file even though nothing links to it: browsers that ignore the
    # <link> tags request /favicon.ico anyway, and with Cloudflare's
    # not_found_handling that request is answered with the whole 404 page.
    (OUT / "favicon.ico").write_bytes(ico([(16, blobs[16]), (32, blobs[32])]))
    (OUT / "opengraph.png").write_bytes(card())

    for path in sorted(OUT.iterdir()):
        print(f"{path.name:24} {path.stat().st_size:>7} bytes")


if __name__ == "__main__":
    main()

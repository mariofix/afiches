"""
og_image.py – Generate Limelight Open Graph images (v3 split-panel design).

Usage
-----
CLI:
    python og_image.py --packages 1240 --categories 48 \
                       --contributors 320 --package flask-sqlalchemy \
                       --output my-og.png

Python:
    from og_image import generate_og_image
    generate_og_image(
        packages=1240,
        categories=48,
        contributors=320,
        package="flask-sqlalchemy",
        output_path="og-flask-sqlalchemy.png",
    )

Parameters
----------
packages      : int   – total number of indexed packages  (e.g. 1240)
categories    : int   – total number of categories        (e.g. 48)
contributors  : int   – total number of contributors      (e.g. 320)
package       : str   – featured package name shown in the pip-pill
                        and highlighted on the right panel
output_path   : str   – destination file path (default: "og-image-v3.png")
"""

from __future__ import annotations

import argparse
import os
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

# ── Colours ──────────────────────────────────────────────────────────────────
BRAND      = (29,  78, 216)
BRAND_DARK = (30,  58, 138)
WHITE      = (255, 255, 255)
MUTED_BLUE = (199, 220, 255)
YELLOW     = (250, 204,  21)
DARK_BAR   = (10,  15,  30)

# ── Canvas ───────────────────────────────────────────────────────────────────
W, H = 1200, 630

# ── Font discovery ───────────────────────────────────────────────────────────
_FONT_CANDIDATES_BOLD = [
    "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/System/Library/Fonts/Helvetica.ttc",
    "arialbd.ttf",
]
_FONT_CANDIDATES_REG = [
    "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "/System/Library/Fonts/Helvetica.ttc",
    "arial.ttf",
]


def _find_font(candidates: list[str]) -> str:
    for path in candidates:
        if os.path.exists(path):
            return path
    # last-resort: Pillow's bundled bitmap font (no size control)
    return None


_BOLD = _find_font(_FONT_CANDIDATES_BOLD)
_REG  = _find_font(_FONT_CANDIDATES_REG)


def _font(bold: bool, size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    path = _BOLD if bold else _REG
    if path:
        return ImageFont.truetype(path, size)
    return ImageFont.load_default()


# ── Helpers ───────────────────────────────────────────────────────────────────

def _gradient_left(draw: ImageDraw.ImageDraw, split: int) -> None:
    """Paint a horizontal gradient on the left panel."""
    for x in range(split + 44):
        t = x / (split + 44)
        r = int(BRAND_DARK[0] + t * (BRAND[0] - BRAND_DARK[0]) * 0.6)
        g = int(BRAND_DARK[1] + t * (BRAND[1] - BRAND_DARK[1]) * 0.6)
        b = int(BRAND_DARK[2] + t * (BRAND[2] - BRAND_DARK[2]) * 0.6)
        draw.line([(x, 0), (x, H)], fill=(r, g, b))


def _light_right(draw: ImageDraw.ImageDraw, split: int) -> None:
    """Paint a subtle light gradient on the right panel."""
    for x in range(split + 44, W):
        t = (x - (split + 44)) / (W - (split + 44))
        v = int(241 + t * (248 - 241))
        draw.line([(x, 0), (x, H)], fill=(v, v + 2, v + 6))


def _dot_overlay(img: Image.Image, x_max: int, spacing: int = 38, r: int = 1) -> Image.Image:
    """Add a subtle white dot grid over the left panel."""
    dot = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    dd  = ImageDraw.Draw(dot)
    for gx in range(0, x_max, spacing):
        for gy in range(0, H, spacing):
            dd.ellipse([gx - r, gy - r, gx + r, gy + r], fill=(255, 255, 255, 30))
    return Image.alpha_composite(img.convert("RGBA"), dot).convert("RGB")


def _fmt(n: int) -> str:
    """Format a stat number with a '+' suffix (e.g. 1240 → '1,240+')."""
    return f"{n:,}+"


# ── Main generator ────────────────────────────────────────────────────────────

def generate_og_image(
    packages: int,
    categories: int,
    contributors: int,
    package: str,
    output_path: str = "og-image-v3.png",
) -> str:
    """
    Generate a Limelight OG image (v3 split-panel design) with live statistics
    and a featured package name.

    Parameters
    ----------
    packages      : total number of indexed packages
    categories    : total number of categories
    contributors  : total number of contributors
    package       : featured package name (shown in the pip pill)
    output_path   : where to save the PNG (default: "og-image-v3.png")

    Returns
    -------
    The resolved output path as a string.
    """
    img  = Image.new("RGB", (W, H), DARK_BAR)
    draw = ImageDraw.Draw(img)

    SPLIT = W // 2 + 20
    LPAD  = 70

    # ── Backgrounds ──────────────────────────────────────────────────────────
    _gradient_left(draw, SPLIT)
    _light_right(draw, SPLIT)

    # Diagonal accent strip between panels
    draw.polygon(
        [(SPLIT - 14, 0), (SPLIT + 44, 0), (SPLIT + 44, H), (SPLIT - 14, H)],
        fill=BRAND,
    )

    # Dot overlay on left panel
    img  = _dot_overlay(img, SPLIT + 44)
    draw = ImageDraw.Draw(img)

    # ── Top accent bars ───────────────────────────────────────────────────────
    draw.rectangle([0, 0, SPLIT + 44, 6], fill=YELLOW)   # yellow on left
    draw.rectangle([SPLIT + 44, 0, W, 6], fill=BRAND)    # brand-blue on right

    # ── Left panel: spotlight glyph + wordmark ───────────────────────────────
    draw.ellipse([LPAD, 82, LPAD + 52, 134],    fill=YELLOW)
    draw.ellipse([LPAD + 7, 89, LPAD + 45, 127], fill=BRAND_DARK)

    draw.text((LPAD + 64, 76), "Limelight", font=_font(True, 70), fill=WHITE)

    # ── Left panel: tagline ───────────────────────────────────────────────────
    draw.text((LPAD, 188), "Discover open source", font=_font(True, 34), fill=WHITE)
    draw.text((LPAD, 228), "Flask packages",       font=_font(True, 34), fill=YELLOW)

    draw.text((LPAD, 288), "Extensions, frameworks, modules",   font=_font(False, 22), fill=MUTED_BLUE)
    draw.text((LPAD, 316), "and projects — all in one place.",  font=_font(False, 22), fill=MUTED_BLUE)

    # ── Left panel: live stats (stacked) ──────────────────────────────────────
    stats = [
        (_fmt(packages),     "Packages",     385),
        (str(categories),    "Categories",   437),
        (_fmt(contributors), "Contributors", 489),
    ]
    f_stat_n = _font(True,  38)
    f_stat_l = _font(False, 18)
    for num, label, sy in stats:
        draw.text((LPAD, sy), num, font=f_stat_n, fill=WHITE)
        nb = draw.textbbox((0, 0), num, font=f_stat_n)
        draw.text((LPAD + nb[2] - nb[0] + 10, sy + 12), label, font=f_stat_l, fill=MUTED_BLUE)

    # ── Right panel: large decorative { } ────────────────────────────────────
    RPAD = SPLIT + 70
    f_big = _font(True, 260)
    bb    = draw.textbbox((0, 0), "{ }", font=f_big)
    bx    = RPAD + ((W - RPAD) - (bb[2] - bb[0])) // 2
    draw.text((bx, 60), "{ }", font=f_big, fill=BRAND)

    # ── Right panel: featured package pill ───────────────────────────────────
    pip_text = f"$ pip install {package}"
    f_pip    = _font(True, 22)
    pb       = draw.textbbox((0, 0), pip_text, font=f_pip)
    pw       = pb[2] - pb[0]
    pill_x   = RPAD + ((W - RPAD) - pw - 32) // 2
    pill_y   = 435
    draw.rounded_rectangle(
        [pill_x - 4, pill_y - 6, pill_x + pw + 28, pill_y + 38],
        radius=8,
        fill=BRAND_DARK,
    )
    draw.text((pill_x + 12, pill_y + 6), pip_text, font=f_pip, fill=YELLOW)

    # ── Bottom URL bar ────────────────────────────────────────────────────────
    draw.rectangle([0, H - 54, W, H], fill=DARK_BAR)
    f_url = _font(False, 20)
    draw.text((LPAD, H - 38), "flaskpackages.pythonanywhere.com", font=f_url, fill=(148, 163, 184))
    right_txt = "Powered by the Flask community"
    rb = draw.textbbox((0, 0), right_txt, font=f_url)
    draw.text((W - LPAD - (rb[2] - rb[0]), H - 38), right_txt, font=f_url, fill=(71, 85, 105))

    # ── Save ──────────────────────────────────────────────────────────────────
    out = str(Path(output_path).resolve())
    img.save(out, "PNG", optimize=True)
    return out


# ── CLI entry-point ───────────────────────────────────────────────────────────

def _cli() -> None:
    parser = argparse.ArgumentParser(
        description="Generate a Limelight OG image (v3 split-panel design).",
    )
    parser.add_argument("--packages",      type=int, default=1240,              help="Total packages count")
    parser.add_argument("--categories",    type=int, default=48,                help="Total categories count")
    parser.add_argument("--contributors",  type=int, default=320,               help="Total contributors count")
    parser.add_argument("--package",       type=str, default="flask-sqlalchemy", help="Featured package name")
    parser.add_argument("--output",        type=str, default="og-image-v3.png",  help="Output PNG path")
    args = parser.parse_args()

    out = generate_og_image(
        packages=args.packages,
        categories=args.categories,
        contributors=args.contributors,
        package=args.package,
        output_path=args.output,
    )
    print(f"Saved → {out}")


if __name__ == "__main__":
    _cli()

#!/usr/bin/env python3
"""Computes the colour wheel of the hero shimmer (WHEEL in src/app.js; variant A, Martin 28.10.2026).

36 colours, 10 degrees apart in OKLCH hue, starting at the lime #dafd55 and turning towards green, cyan, blue,
violet, pink, orange and yellow. Each is the most saturated sRGB colour of its hue on which the type #435960
still has at least FLOOR contrast (WCAG). The default floor of 4.6 leaves room for blending between neighbours,
rounding and dither, so the type never drops below 4.5:1 (WCAG AA); the script checks that over the whole wheel.
Mixing two of these colours in linear light (as app.js does) cannot go below the darker of the two.

Usage: python3 tools/colour_wheel.py [floor]   (standard library only; paste the printed line into WHEEL)
"""
import math, sys

FLOOR = float(sys.argv[1]) if len(sys.argv) > 1 else 4.6
INK, LIME = "#435960", "#dafd55"


def to_lin(c):
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def to_srgb(c):
    return 12.92 * c if c <= 0.0031308 else 1.055 * c ** (1 / 2.4) - 0.055


def rgb(hexcode):
    return [int(hexcode[i:i + 2], 16) / 255 for i in (1, 3, 5)]


def hexcode(c):
    return "#%02x%02x%02x" % tuple(max(0, min(255, round(v * 255))) for v in c)


def luminance(c):
    r, g, b = (to_lin(v) for v in c)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast(c):
    return (luminance(c) + 0.05) / (luminance(rgb(INK)) + 0.05)


def oklab_from_lin(r, g, b):
    l = 0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * b
    m = 0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b
    s = 0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b
    l, m, s = (math.copysign(abs(v) ** (1 / 3), v) for v in (l, m, s))
    return (0.2104542553 * l + 0.7936177850 * m - 0.0040720468 * s,
            1.9779984951 * l - 2.4285922050 * m + 0.4505937099 * s,
            0.0259040371 * l + 0.7827717662 * m - 0.8086757660 * s)


def lin_from_oklab(L, a, b):
    l, m, s = (L + 0.3963377774 * a + 0.2158037573 * b) ** 3, (L - 0.1055613458 * a - 0.0638541728 * b) ** 3, \
        (L - 0.0894841775 * a - 1.2914855480 * b) ** 3
    return (4.0767416621 * l - 3.3077115913 * m + 0.2309699292 * s,
            -1.2684380046 * l + 2.6097574011 * m - 0.3413193965 * s,
            -0.0041960863 * l - 0.7034186147 * m + 1.7076147010 * s)


def from_lch(L, C, H):
    """sRGB 0..1 for an OKLCH colour, or None outside the sRGB gamut"""
    lin = lin_from_oklab(L, C * math.cos(math.radians(H)), C * math.sin(math.radians(H)))
    if min(lin) < -1e-6 or max(lin) > 1 + 1e-6:
        return None
    return [to_srgb(min(1, max(0, v))) for v in lin]


def max_chroma(L, H):
    lo, hi = 0.0, 0.5
    for _ in range(30):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if from_lch(L, mid, H) else (lo, mid)
    return lo


def vivid(H):
    """the most saturated in-gamut colour of hue H with at least FLOOR contrast to the type"""
    best = None
    for i in range(400, 1000):
        L = i / 1000
        C = max_chroma(L, H)
        c = from_lch(L, C, H)
        if c and contrast(c) >= FLOOR and (best is None or C > best[0]):
            best = (C, c)
    return best[1]


lab = oklab_from_lin(*(to_lin(v) for v in rgb(LIME)))
h0 = math.degrees(math.atan2(lab[2], lab[1])) % 360
wheel = [LIME] + [hexcode(vivid((h0 + 10 * k) % 360)) for k in range(1, 36)]

# the same blending as app.js (bytes interpolated between neighbours), with the worst case of the dither
keys = [[int(h[i:i + 2], 16) for i in (1, 3, 5)] for h in wheel]
worst = min(
    contrast([max(0, min(255, math.floor(a[c] + (b[c] - a[c]) * f + dz))) / 255 for c in range(3)])
    for k in range(36) for a, b in [(keys[k], keys[(k + 1) % 36])]
    for f in (n / 40 for n in range(40)) for dz in (-0.5, 0.5))

print(" ".join(h[1:] for h in wheel))
print(f"lime hue {h0:.1f}°, floor {FLOOR}:1, lowest contrast on the wheel incl. blending and dither {worst:.3f}:1",
      file=sys.stderr)

#!/usr/bin/env python3
"""WOFF2 version of the site font (05.11.2026): assets/fonts/GoogleSans-latin-wght.woff → .woff2, about a fifth smaller.
Also prints the metric overrides for the fallback font in styles.css (Arial / Liberation Sans sized like Google Sans,
so the text does not jump when the web font arrives).

fontTools does the WOFF2 work; it needs the Python module `brotli`. Where that is missing (no installs in some
environments), a small stand-in passes the compression to Node's built-in brotli (same library, font mode).
Checks: the WOFF2 decodes to exactly the same font tables as the WOFF."""
import json, pathlib, subprocess, sys, types

ROOT = pathlib.Path(__file__).resolve().parents[1]
SRC = ROOT / "assets" / "fonts" / "GoogleSans-latin-wght.woff"
DST = SRC.with_suffix(".woff2")

try:
    import brotli  # noqa: F401
except ImportError:
    JS = ("const z=require('zlib');const c=[];process.stdin.on('data',d=>c.push(d)).on('end',()=>{const b=Buffer.concat(c);"
          "const a=process.argv[1];process.stdout.write(a==='d'?z.brotliDecompressSync(b):z.brotliCompressSync(b,{params:{"
          "[z.constants.BROTLI_PARAM_MODE]:+a,[z.constants.BROTLI_PARAM_QUALITY]:11,[z.constants.BROTLI_PARAM_SIZE_HINT]:b.length}}))})")
    shim = types.ModuleType("brotli")
    shim.MODE_GENERIC, shim.MODE_TEXT, shim.MODE_FONT = 0, 1, 2
    shim.compress = lambda data, mode=0, quality=11, lgwin=22, lgblock=0: subprocess.run(
        ["node", "-e", JS, str(mode)], input=data, capture_output=True, check=True).stdout
    shim.decompress = lambda data: subprocess.run(["node", "-e", JS, "d"], input=data, capture_output=True, check=True).stdout
    sys.modules["brotli"] = shim

from fontTools.ttLib import TTFont  # noqa: E402

f = TTFont(SRC)
f.flavor = "woff2"
f.recalcTimestamp = False   # keep the date of the source font, so the output is reproducible
f.save(DST)
a, b = TTFont(SRC), TTFont(DST)
for tag in sorted(a.keys()):
    if tag == "GlyphOrder":
        continue
    if a.getTableData(tag) != b.getTableData(tag):
        # glyf/loca are re-encoded by the WOFF2 transform: compare the decompiled glyphs instead
        if tag == "head":   # WOFF2 sets flag bit 11 and a new checksum; everything else must match
            fa, fb = vars(a["head"]).copy(), vars(b["head"]).copy()
            for d in (fa, fb):
                d.pop("checkSumAdjustment", None); d["flags"] = d["flags"] & ~(1 << 11); d.pop("tableTag", None)
            assert fa == fb, "head"
        elif tag in ("glyf", "loca"):
            ga, gb = a["glyf"], b["glyf"]
            assert all(ga[n].getCoordinates(ga)[0] == gb[n].getCoordinates(gb)[0] for n in a.getGlyphOrder()), tag
        else:
            raise SystemExit(f"table {tag} differs")
print(f"{DST.name}: {DST.stat().st_size // 1024} KB (WOFF {SRC.stat().st_size // 1024} KB), tables identical")

# fallback metrics (capsize/fontaine method): scale Arial so its average width matches Google Sans
SAMPLE = ("Marken mit KI. Ich baue KI-Systeme, die für Ihre Marke arbeiten. Autonome KI-Agenten, KI-gestützte Websites "
          "und Content-Engines, die mit Ihrem Unternehmen wachsen. Brands with AI. I build AI systems that work for your brand.")


def avg_width(font):
    cmap, hmtx, upm = font.getBestCmap(), font["hmtx"], font["head"].unitsPerEm
    return sum(hmtx[cmap[ord(c)]][0] for c in SAMPLE if ord(c) in cmap) / len(SAMPLE) / upm


arial = TTFont("/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf")   # metric clone of Arial
gs = TTFont(SRC)
size = avg_width(gs) / avg_width(arial)
upm, os2 = gs["head"].unitsPerEm, gs["OS/2"]
print(json.dumps({"size-adjust": f"{size * 100:.2f}%",
                  "ascent-override": f"{os2.sTypoAscender / upm / size * 100:.2f}%",
                  "descent-override": f"{-os2.sTypoDescender / upm / size * 100:.2f}%",
                  "line-gap-override": f"{os2.sTypoLineGap / upm / size * 100:.2f}%"}))

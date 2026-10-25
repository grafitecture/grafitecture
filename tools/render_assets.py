#!/usr/bin/env python3
"""Renders the raster brand assets from the logo SVG with headless Chromium (Playwright):
   assets/icons/apple-touch-icon.png (180), assets/icons/favicon-32.png, assets/og/grafitecture-og.png (1200x630).
   Two colours only: #435960 and white. Run once after the logo changes; build.py copies the results."""
import asyncio, base64, pathlib, re
from playwright.async_api import async_playwright

ROOT = pathlib.Path(__file__).resolve().parents[1]
A = ROOT / "assets"
C, W = "#435960", "#FFFFFF"

logo_w = (A / "logo" / "grafitecture-white.svg").read_text()
logo_w = re.sub(r"<title>.*?</title>", "", logo_w, flags=re.S)
g_path = re.search(r'<path d="([^"]+)"', (A / "logo" / "grafitecture.svg").read_text()).group(1)
font = base64.b64encode((A / "fonts" / "GoogleSans-latin-wght.woff").read_bytes()).decode()

# the "g" of the wordmark: bbox x 71..114.44, y 400.23..459.51 -> centred square viewBox
GX, GY, GW, GH = 71, 400.23, 43.44, 59.28
def g_svg(pad=0.70):
    side = GH / pad
    cx, cy = GX + GW / 2, GY + GH / 2
    x, y = cx - side / 2, cy - side / 2
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{x:.2f} {y:.2f} {side:.2f} {side:.2f}">'
            f'<rect x="{x:.2f}" y="{y:.2f}" width="{side:.2f}" height="{side:.2f}" fill="{C}"/>'
            f'<path fill="{W}" d="{g_path}"/></svg>')

OG = f"""<!doctype html><html><head><meta charset="utf-8"><style>
@font-face {{ font-family: GS; src: url(data:font/woff;base64,{font}) format("woff"); font-weight: 400 700; }}
html, body {{ margin: 0; width: 1200px; height: 630px; background: {C}; color: {W}; font-family: GS, sans-serif; }}
.f {{ box-sizing: border-box; width: 1200px; height: 630px; padding: 76px 84px 70px; display: flex; flex-direction: column; justify-content: space-between; }}
.f svg {{ width: 380px; height: auto; display: block; }}
h1 {{ margin: 0; font-weight: 400; font-size: 168px; line-height: .9; letter-spacing: -.045em; }}
p {{ margin: 22px 0 0; font-size: 26px; letter-spacing: .01em; }}
</style></head><body><div class="f">{logo_w}<div><h1>Marken mit KI.</h1><p>Martin Schweppe, Diplom-Designer · Mannheim</p></div></div></body></html>"""

async def main():
    (A / "icons").mkdir(exist_ok=True); (A / "og").mkdir(exist_ok=True)
    (A / "icons" / "favicon.svg").write_text(g_svg(0.70))
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={"width": 1200, "height": 630})
        await pg.set_content(OG); await pg.evaluate("document.fonts.ready")
        await pg.screenshot(path=str(A / "og" / "grafitecture-og.png"))
        for size, name, pad in ((180, "apple-touch-icon.png", 0.62), (32, "favicon-32.png", 0.74)):
            pg2 = await b.new_page(viewport={"width": size, "height": size}, device_scale_factor=1)
            await pg2.set_content(f'<html><body style="margin:0">{g_svg(pad).replace("<svg ", f"<svg width={size} height={size} ", 1)}</body></html>')
            await pg2.screenshot(path=str(A / "icons" / name), omit_background=False)
        await b.close()
    for f in sorted((A / "icons").iterdir()) + [A / "og" / "grafitecture-og.png"]:
        print(f.relative_to(ROOT), f.stat().st_size, "B")

asyncio.run(main())

"""Rendert Reel-Titelbilder, Storys und Highlight-Cover (1080 × 1920)."""
import asyncio, sys
from playwright.async_api import async_playwright
from engine import page, OUT, ROOT
from content3 import COVERS, STORIES

async def main(items):
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={"width": 1080, "height": 1920})
        for name, (html, sub) in items.items():
            d = OUT / sub; d.mkdir(parents=True, exist_ok=True)
            hp = ROOT / "html" / f"{name}.html"; hp.parent.mkdir(exist_ok=True)
            hp.write_text(page(html, 1080, 1920))
            await pg.goto(hp.as_uri()); await pg.wait_for_function("window.READY === true", timeout=30000)
            await pg.wait_for_timeout(80)
            el = await pg.query_selector("section.slide")
            await el.screenshot(path=str(d / f"{name}.png"))
            print(name)
        await b.close()

items = {f"{k}_Titelbild": (v, "covers") for k, v in COVERS.items()}
items.update({k: (v, "stories") for k, v in STORIES.items()})
asyncio.run(main(items))

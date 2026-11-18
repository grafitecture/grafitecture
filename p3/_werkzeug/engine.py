"""Renders Instagram slides (HTML -> PNG) in the Grafitecture CI with headless Chromium."""
import asyncio, pathlib, re, html as H
from playwright.async_api import async_playwright

ROOT = pathlib.Path(__file__).resolve().parent
REPO = pathlib.Path("/home/claude/grafitecture/grafitecture")
HF = pathlib.Path("/home/claude/ig3/photos/hf")
OUT = pathlib.Path("/home/claude/ig3/out")
FONT = REPO / "assets/fonts/GoogleSans-latin-wght.woff"
CSS = (ROOT / "base.css").read_text().replace("FONT_URL", FONT.as_uri())
SHEEN_JS = (ROOT / "sheen.js").read_text()


def _logo():
    s = (REPO / "assets/logo/grafitecture.svg").read_text()
    s = re.sub(r"<\?xml.*?\?>", "", s, flags=re.S)
    s = re.sub(r"<title>.*?</title>", "", s, flags=re.S)
    return s.replace(' role="img" aria-label="Grafitecture"', "")


LOGO = _logo()
LOGO_WHITE = LOGO.replace('fill="#435960"', 'fill="#ffffff"')
ARROW = ('<svg viewBox="0 0 22 10"><path d="M0 5h20.5M16 .8 20.5 5 16 9.2" fill="none" stroke="currentColor" '
         'stroke-width="1.1"/></svg>')


def img(path):
    p = pathlib.Path(path)
    return p.as_uri()


def logo(cls="logo"):
    return f'<div class="{cls}">{LOGO}</div>'


def page(slides_html, w=1080, h=1350):
    return f"""<!doctype html><html lang="de"><head><meta charset="utf-8"><style>{CSS}</style></head>
<body>{slides_html}<script>{SHEEN_JS}
(async () => {{
  await document.fonts.ready;
  document.querySelectorAll('canvas.sheen').forEach((cv) => {{
    const r = window.paintSheen(cv, parseFloat(cv.dataset.clock || '30'), parseFloat(cv.dataset.res || '3'),
                                {{ noFade: true, hueOffset: parseFloat(cv.dataset.hue || '0') }});
    cv.dataset.pair = JSON.stringify(r);
  }});
  window.READY = true;
}})();
</script></body></html>"""


def slide(cls, inner, sheen=None, extra_style=""):
    """sheen: dict(clock=..., hue=...) paints the two-colour field behind the slide."""
    cv = ""
    if sheen is not None:
        cv = (f'<canvas class="sheen" data-clock="{sheen.get("clock", 30)}" data-hue="{sheen.get("hue", 0)}" '
              f'data-res="{sheen.get("res", 3)}"></canvas>')
    st = f' style="{extra_style}"' if extra_style else ""
    return f'<section class="slide {cls}"{st}>{cv}{inner}</section>'


async def render_posts(posts, only=None, scale=1):
    """posts: dict id -> list of slide html strings. Writes OUT/<id>/<id>_<n>.png"""
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={"width": 1080, "height": 1350}, device_scale_factor=scale)
        for pid, slides in posts.items():
            if only and pid not in only:
                continue
            d = OUT / pid
            d.mkdir(parents=True, exist_ok=True)
            for old in d.glob("*.png"):
                old.unlink()
            for i, s in enumerate(slides, 1):
                hp = ROOT / "html" / f"{pid}_{i:02d}.html"
                hp.parent.mkdir(exist_ok=True)
                hp.write_text(page(s))
                await pg.goto(hp.as_uri())
                await pg.wait_for_function("window.READY === true", timeout=30000)
                await pg.wait_for_timeout(80)
                el = await pg.query_selector("section.slide")
                await el.screenshot(path=str(d / f"{pid}_{i:02d}.png"))
            print(pid, len(slides), "slides")
        await b.close()


def run(posts, only=None):
    asyncio.run(render_posts(posts, only))

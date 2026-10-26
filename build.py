#!/usr/bin/env python3
"""Builds the website from src/ and assets/ (V3, 25.10.2026). Standard library only, no installs.
   public/        the live site. Committed to Git; Vercel serves this folder as is (no build step on Vercel).
   vercel.json    Vercel settings (output folder, headers), written to the repository root.
   dist/artifact/ preview page for a claude.ai artifact (font and logos inlined). Not committed.

Run:  python3 build.py        then commit public/ and vercel.json together with the source change.

Placeholders in src/body.html:
   {{LOGO_DARK}} {{LOGO_WHITE}}  inline wordmark (assets/logo/*.svg)
   {{ARROW}}                     arrow icon for buttons
   {{CLIENTS}} {{CLIENT_COUNT}}  reference list, see CLIENTS below. A client shows its logo when
                                 assets/clients/<slug>.svg|png exists (one colour, #435960), otherwise its name.
   {{IMG_PORTRAIT}} {{IMG_DOOR}} photos, see PHOTOS below
"""
import base64, hashlib, html, json, math, pathlib, re, shutil, struct, unicodedata

ROOT = pathlib.Path(__file__).resolve().parent
SRC = ROOT / "src"
ASSETS = ROOT / "assets"
DIST = ROOT / "dist"
SITE_URL = "https://www.grafitecture.de/"

FONTS = [
    # family, file, extra descriptors  (Google Sans, SIL OFL, subset to Latin, variable weight 400–700)
    ("Google Sans", "GoogleSans-latin-wght.woff", "font-weight: 400 700;"),
]

# name, website (None = not linked). Order = order on the page.
CLIENTS = [
    ("L'Année", "https://1898.ma/"),
    ("Dentaid", "https://www.dentaid-direkt.de/"),
    ("Healthklick", None),
    ("fläsh", "https://flaesh.com/"),
    ("Kaufhaus Ganz", "https://www.kaufhaus-ganz.de/"),
    ("Onkel Otto Bar", "https://www.onkelottobar.de/"),
    ("42health", "http://42health.de/"),
    ("tinytecture", "https://www.tinytecture.de/"),
    ("Detmers", "http://detmers.de/"),
    ("1898", "https://1898.ma/"),
    ("CORE", "https://www.core-cc.com/"),
    ("raumrent", "https://www.raumrent.de/"),
    ("Ultracain", "https://www.ultracain.de/"),
    ("Vitaphone", None),
    ("Steinbeis Finance", "https://steinbeis-finance.de/"),
    ("Creating Smiles", "https://www.creatingsmiles.eu/"),
    ("flaeshapp", "https://www.flaeshapp.com/"),
    ("Zahnarztpraxis Theurer", "https://www.zahnarztpraxis-theurer.de/"),
    ("Gemeinschaftspraxis Günther", "https://www.gemeinschaftspraxis-guenther.de/"),
    ("Tanja Weber", None),
    ("Covendos", "https://www.covendos.com/"),
    ("Zweite Liebe", "https://sanremowebseite.vercel.app/"),
    ("WHITEsmile", "https://www.whitesmile.de/"),
    ("ag+", "https://ahrens-gonzalves.de/"),
    ("CCI Transport", "https://www.cci-transport.de/"),
    ("SanRemo", "https://sanremowebseite.vercel.app/"),
    ("starks", None),
]

TITLE_DE = "Grafitecture · KI-Systeme für Marken · Martin Schweppe, Dipl.-Des., Mannheim"
DESC_DE = ("Martin Schweppe, Diplom-Designer, baut KI-Systeme für Marken: KI-Websites, KI-Agenten, "
           "Content-Engines und Workflow-Automation. Grafitecture GmbH, Mannheim, seit 2000.")
OG_IMAGE = "assets/og/grafitecture-og.png"

ARROW = ('<svg viewBox="0 0 22 10" aria-hidden="true" focusable="false">'
         '<path d="M0 5h20.5M16 .8 20.5 5 16 9.2" fill="none" stroke="currentColor" stroke-width="1.5"/></svg>')

CSP = ("default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; "
       "img-src 'self' data:; font-src 'self' data:; connect-src 'self'; form-action mailto:; "
       "frame-ancestors 'none'; base-uri 'self'; object-src 'none'")


def versioned(rel: str) -> str:
    """URL with a content hash, so /assets can be cached as immutable and still update when a file changes."""
    h = hashlib.sha1((ROOT / rel).read_bytes()).hexdigest()[:10]
    return f"{rel}?v={h}"


def font_css(inline: bool) -> str:
    out = []
    for fam, file, extra in FONTS:
        fmt = "woff2" if file.endswith(".woff2") else "woff"
        if inline:
            data = base64.b64encode((ASSETS / "fonts" / file).read_bytes()).decode()
            src = f'url(data:font/{fmt};base64,{data}) format("{fmt}")'
        else:
            src = f'url("{versioned("assets/fonts/" + file)}") format("{fmt}")'
        out.append(f'@font-face {{ font-family: "{fam}"; src: {src}; {extra} font-style: normal; font-display: swap; }}')
    return "\n".join(out)


def inline_logo(name: str) -> str:
    s = (ASSETS / "logo" / name).read_text()
    s = re.sub(r"<\?xml.*?\?>", "", s, flags=re.S).strip()
    s = re.sub(r"<title>.*?</title>", "", s, flags=re.S)
    s = s.replace(' role="img"', "").replace(' aria-label="Grafitecture"', "")
    return s.replace("<svg ", '<svg aria-hidden="true" focusable="false" ', 1)


def slug(name: str) -> str:
    s = unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-") or "client"


def client_logo(sl: str):
    for ext in ("svg", "png"):
        f = ASSETS / "clients" / f"{sl}.{ext}"
        if f.exists():
            return f
    return None


def natural_size(f: pathlib.Path):
    if f.suffix == ".svg":
        m = re.search(r'viewBox="\s*[-\d.]+[\s,]+[-\d.]+[\s,]+([\d.]+)[\s,]+([\d.]+)', f.read_text())
        return float(m.group(1)), float(m.group(2))
    with f.open("rb") as fh:  # PNG: IHDR width/height
        fh.seek(16)
        return struct.unpack(">II", fh.read(8))


def optical_size(f: pathlib.Path):
    """Equal visual weight: every logo gets roughly the same area, capped in width and height."""
    w, h = natural_size(f)
    r = w / h
    area = 132 * 48
    dh = math.sqrt(area / r)
    dw = r * dh
    k = min(1, 210 / dw, 66 / dh)
    return round(dw * k), round(dh * k)


def display_sizes():
    f = ASSETS / "clients" / "sizes.json"
    return json.loads(f.read_text()) if f.exists() else {}


def logo_src(f: pathlib.Path, mode: str) -> str:
    """deploy: separate file with content hash (cacheable); inline: data URI, so the preview never depends on
    supporting files."""
    rel = f"assets/clients/{f.name}"
    if mode == "inline":
        mime = "image/svg+xml" if f.suffix == ".svg" else "image/png"
        return f"data:{mime};base64,{base64.b64encode(f.read_bytes()).decode()}"
    return versioned(rel) if mode == "deploy" else rel


def clients_html(mode: str) -> str:
    sizes = display_sizes()
    rows = []
    for name, url in CLIENTS:
        nm = html.escape(name)
        sl = slug(name)
        f = client_logo(sl)
        if f:
            w, h = sizes.get(sl) or optical_size(f)
            inner = (f'<img src="{logo_src(f, mode)}" alt="{nm}" width="{w}" height="{h}" style="--w:{w}" '
                     f'loading="lazy" decoding="async">')
        else:
            inner = f'<span class="logo-txt">{nm}</span>'
        if url:
            inner = f'<a href="{html.escape(url)}" target="_blank" rel="noopener noreferrer">{inner}</a>'
        rows.append(f"      <li>{inner}</li>")
    return "\n".join(rows)


# photos supplied by Martin (25.10.2026); 640 and 1280 px wide JPEGs in assets/photos
PHOTOS = {
    "IMG_PORTRAIT": ("martin-schweppe", "Martin Schweppe, Diplom-Designer", "Martin Schweppe, graduate designer",
                     "(min-width: 1100px) 30vw, (min-width: 600px) 520px, 92vw"),
    "IMG_DOOR": ("eingang", "Hauseingang mit Holztür und der Jahreszahl 1926", "Entrance with a wooden door marked 1926",
                 "(min-width: 1100px) 30vw, (min-width: 600px) 520px, 92vw"),
}


def photo_html(key: str, mode: str) -> str:
    stem, alt_de, alt_en, sizes = PHOTOS[key]
    small, large = ASSETS / "photos" / f"{stem}-640.jpg", ASSETS / "photos" / f"{stem}-1280.jpg"
    w, h = natural_size_jpeg(large)
    alts = f'alt="{html.escape(alt_de)}" data-alt-de="{html.escape(alt_de)}" data-alt-en="{html.escape(alt_en)}"'
    if mode == "inline":
        src = f'src="data:image/jpeg;base64,{base64.b64encode(small.read_bytes()).decode()}"'
    else:
        a, b = f"assets/photos/{small.name}", f"assets/photos/{large.name}"
        if mode == "deploy":
            a, b = versioned(a), versioned(b)
        src = f'src="{b}" srcset="{a} 640w, {b} 1280w" sizes="{sizes}"'
    return (f'<figure class="photo"><img {src} {alts} width="{w}" height="{h}" loading="lazy" decoding="async"></figure>')


def natural_size_jpeg(f: pathlib.Path):
    data = f.read_bytes(); i = 2
    while i < len(data):
        if data[i] != 0xFF:
            i += 1; continue
        marker = data[i + 1]
        if marker in (0xC0, 0xC1, 0xC2):
            h, w = struct.unpack(">HH", data[i + 5:i + 9])
            return w, h
        i += 2 + struct.unpack(">H", data[i + 2:i + 4])[0]
    raise ValueError(f"no SOF in {f}")


def render_body(mode: str) -> str:
    body = (SRC / "body.html").read_text()
    body = (body.replace("{{LOGO_DARK}}", inline_logo("grafitecture.svg"))
                .replace("{{LOGO_WHITE}}", inline_logo("grafitecture-white.svg"))
                .replace("{{ARROW}}", ARROW)
                .replace("{{CLIENTS}}", clients_html(mode))
                .replace("{{CLIENT_COUNT}}", str(len(CLIENTS))))
    for key in PHOTOS:
        body = body.replace("{{" + key + "}}", photo_html(key, mode))
    left = re.findall(r"\{\{[A-Z_]+\}\}", body)
    assert not left, f"unreplaced placeholders: {left}"
    return body


styles = (SRC / "styles.css").read_text()
app = (SRC / "app.js").read_text()

ld = {
    "@context": "https://schema.org",
    "@type": "ProfessionalService",
    "name": "Grafitecture GmbH",
    "url": SITE_URL,
    "email": "martin.schweppe@grafitecture.de",
    "image": SITE_URL + OG_IMAGE,
    "logo": SITE_URL + "assets/logo/grafitecture.svg",
    "foundingDate": "2000",
    "address": {"@type": "PostalAddress", "streetAddress": "Rebenstr. 9a", "postalCode": "68309",
                "addressLocality": "Mannheim", "addressCountry": "DE"},
    "employee": {"@type": "Person", "name": "Martin Schweppe", "jobTitle": "Geschäftsführer, Diplom-Designer"},
    "knowsLanguage": ["de", "en"],
}


def copy_clients(out: pathlib.Path):
    d = ASSETS / "clients"
    if d.exists() and any(d.iterdir()):
        shutil.copytree(d, out / "assets" / "clients", ignore=shutil.ignore_patterns("*.txt", "*.json", ".*"))


def vercel_config() -> dict:
    return {
        "$schema": "https://openapi.vercel.sh/vercel.json",
        "framework": None,
        "outputDirectory": "public",
        "cleanUrls": True,
        # Vercel Functions would run in Frankfurt (privacy note by S. Enders, 26.10.2026).
        # The site has no functions; the static files are served by the CDN closest to the visitor.
        "regions": ["fra1"],
        "headers": [
            {"source": "/assets/(.*)", "headers": [{"key": "Cache-Control", "value": "public, max-age=31536000, immutable"}]},
            {"source": "/(.*)", "headers": [
                {"key": "Content-Security-Policy", "value": CSP},
                {"key": "X-Content-Type-Options", "value": "nosniff"},
                {"key": "X-Frame-Options", "value": "DENY"},
                {"key": "Referrer-Policy", "value": "strict-origin-when-cross-origin"},
                {"key": "Permissions-Policy", "value": "camera=(), microphone=(), geolocation=(), browsing-topics=()"}
            ]}
        ]
    }


def build_deploy():
    out = ROOT / "public"   # generated only: everything in it is rebuilt from src/ and assets/
    if out.exists():
        shutil.rmtree(out)
    (out / "assets").mkdir(parents=True)
    for sub in ("fonts", "logo", "og", "photos"):
        shutil.copytree(ASSETS / sub, out / "assets" / sub)
    copy_clients(out)
    for icon in ("favicon.svg", "favicon-32.png", "apple-touch-icon.png"):
        shutil.copy(ASSETS / "icons" / icon, out / icon)
    font_url = versioned("assets/fonts/GoogleSans-latin-wght.woff")
    html_doc = f"""<!doctype html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{TITLE_DE}</title>
<meta name="description" content="{DESC_DE}">
<meta name="theme-color" content="#FFFFFF">
<link rel="canonical" href="{SITE_URL}">
<link rel="icon" href="favicon-32.png" sizes="32x32" type="image/png">
<link rel="icon" href="favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="apple-touch-icon.png">
<link rel="preload" href="{font_url}" as="font" type="font/woff" crossorigin>
<meta property="og:type" content="website">
<meta property="og:site_name" content="Grafitecture">
<meta property="og:url" content="{SITE_URL}">
<meta property="og:title" content="Grafitecture · Marken mit KI. Ich baue KI-Systeme, die für Ihre Marke arbeiten.">
<meta property="og:description" content="{DESC_DE}">
<meta property="og:image" content="{SITE_URL}{OG_IMAGE}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Grafitecture: Marken mit KI. Martin Schweppe, Diplom-Designer, Mannheim">
<meta property="og:locale" content="de_DE">
<meta property="og:locale:alternate" content="en_GB">
<meta name="twitter:card" content="summary_large_image">
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
<style>
{font_css(False)}
{styles}
</style>
</head>
<body>
{render_body("deploy")}
<script>
{app}
</script>
</body>
</html>
"""
    (out / "index.html").write_text(html_doc)
    (out / "robots.txt").write_text("User-agent: *\nAllow: /\n")
    (ROOT / "vercel.json").write_text(json.dumps(vercel_config(), indent=2) + "\n")
    return out


def build_artifact():
    out = DIST / "artifact"
    if out.exists():
        shutil.rmtree(out)
    (out / "assets").mkdir(parents=True)
    # the artifact viewer cannot submit forms anywhere: drop the no-JS mailto fallback, the script handles submit
    no_js_fallback = ' action="mailto:martin.schweppe@grafitecture.de" method="post" enctype="text/plain"'
    body = render_body("inline")   # client logos embedded as data URIs
    assert body.count(no_js_fallback) == 1
    body = body.replace(no_js_fallback, "")
    page = f"""<title>Grafitecture</title>
<meta name="claude:viewport-fit-sides" content="cover">
<meta name="description" content="{DESC_DE}">
<style>
{font_css(True)}
{styles}
</style>
{body}
<script>
{app}
</script>
"""
    (out / "index.html").write_text(page)
    return out


if __name__ == "__main__":
    d = build_deploy()
    a = build_artifact()
    for p in (d / "index.html", a / "index.html"):
        print(p, f"{p.stat().st_size/1024:.1f} KB")
    shown = sum(1 for n, _ in CLIENTS if client_logo(slug(n)))
    print(f"clients: {len(CLIENTS)} total, {shown} with logo file, {len(CLIENTS) - shown} as text")

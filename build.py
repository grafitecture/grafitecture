#!/usr/bin/env python3
"""Builds the website from src/ and assets/ (V3, 25.10.2026; technical pass „tech-max“, 05.11.2026).
Standard library only, no installs.
   public/        the live site. Committed to Git; Vercel serves this folder as is (no build step on Vercel).
                  One page per language (Martin, 05.11.2026), built from the bilingual src/body.html by keeping
                  only the elements of that language: index.html = /  (German), en.html = /en  (English).
                  Impressum and Datenschutz also as pages of their own (Martin, 05.11.2026): impressum.html,
                  datenschutz.html, en/legal-notice.html, en/privacy-policy.html. On / and /en they still open
                  as dialogs, as before.
                  404.html from src/404.html (both languages, switched in place; noindex), sitemap.xml,
                  robots.txt, favicon.ico.
   vercel.json    Vercel settings (output folder, redirects, headers), written to the repository root.
                  Redirects come from seo/redirect-map.csv (one row per old address).
   dist/artifact/ preview page for a claude.ai artifact (both languages, font and logos inlined). Not committed.

Run:  python3 build.py        then commit public/ and vercel.json together with the source change.

Placeholders in src/body.html:
   {{LOGO_DARK}} {{LOGO_WHITE}}  inline wordmark (assets/logo/*.svg)
   {{ARROW}}                     arrow icon for buttons
   {{CLIENTS}} {{CLIENT_COUNT}}  reference list, see CLIENTS below. A client shows its logo when
                                 assets/clients/<slug>.svg|png exists (one colour, #435960), otherwise its name.
   {{IMG_PORTRAIT}} {{IMG_DOOR}} photos, see PHOTOS below
"""
import base64, csv, datetime, hashlib, html, json, math, pathlib, re, shutil, struct, unicodedata
from html.parser import HTMLParser

ROOT = pathlib.Path(__file__).resolve().parent
SRC = ROOT / "src"
ASSETS = ROOT / "assets"
DIST = ROOT / "dist"
SITE = "https://www.grafitecture.de"
SITE_URL = SITE + "/"

# One canonical address per page and language (05.11.2026): https, www, no trailing slash (like the old WordPress
# site: /impressum, /author/martinschweppe, /feed were all asked for without one). /en/ etc. redirect to /en.
LANGS = ("de", "en")
PAGES = {
    "home": {"de": "/", "en": "/en"},
    "impressum": {"de": "/impressum", "en": "/en/legal-notice"},
    "datenschutz": {"de": "/datenschutz", "en": "/en/privacy-policy"},
}
# production aliases on vercel.app (behind Vercel Authentication): send them to the real domain
VERCEL_ALIASES = ["grafitecturewebseite-grafitecture.vercel.app", "grafitecturewebseite-git-main-grafitecture.vercel.app"]
# IndexNow (Bing, Yandex, Seznam, Naver …; not Google): the key is public by design, it lives in /<key>.txt.
# .github/workflows/indexnow.yml sends the sitemap addresses after every production deployment.
INDEXNOW_KEY = "af047a6e4bbe9d70d8e2657ed6e5d075"
ROBOTS_INDEX = "index, follow, max-image-preview:large"


def abs_url(path: str) -> str:
    return SITE_URL if path == "/" else SITE + path


def out_file(path: str) -> str:
    """public/ file for a page address (cleanUrls: /en → en.html, /en/legal-notice → en/legal-notice.html)."""
    return "index.html" if path == "/" else path.lstrip("/") + ".html"


FONTS = [
    # family, file, extra descriptors  (Google Sans, SIL OFL, subset to Latin, variable weight 400–700)
    # WOFF2 since 05.11.2026 (tools/make_woff2.py, 47 instead of 61 KB); the WOFF stays in assets/ for the tools
    ("Google Sans", "GoogleSans-latin-wght.woff2", "font-weight: 400 700;"),
]
FONT_FILE = "assets/fonts/" + FONTS[0][1]

# name, website (None = not linked). Order = order on the page.
CLIENTS = [
    ("L'Année", "https://www.lannee.de/"),   # Martin 30.10. (before 1898.ma)
    ("Dentaid", "https://dentaid-direkt.de/"),   # final address (05.11.2026, was www., 301)
    ("Healthklick", None),
    ("fläsh", "https://flaesh.com/"),
    ("Kaufhaus Ganz", "https://www.kaufhaus-ganz.de/"),
    ("Onkel Otto Bar", "https://www.onkelottobar.de/"),
    ("42health", "https://42health.de/"),   # https (05.11.2026, http answered 301)
    ("tinytecture", "https://www.tinytecture.de/"),
    ("Detmers", "https://detmers.de/"),   # https (05.11.2026, http answered 301)
    ("1898", "https://www.lannee.de/"),   # Martin 30.10. (before 1898.ma)
    ("CORE", "https://www.core-cc.com/"),
    ("raumrent", "https://www.raumrent.de/"),
    ("Ultracain", "https://www.ultracain.de/"),
    ("Vitaphone", None),
    ("Steinbeis Finance", "https://steinbeis-finance.de/"),
    ("Creating Smiles", "https://creatingsmiles.eu/"),   # final address (05.11.2026, was www., 301)
    ("flaeshapp", "https://www.flaeshapp.com/"),
    ("Zahnarztpraxis Theurer", "https://www.zahnarztpraxis-theurer.de/"),
    ("Gemeinschaftspraxis Günther", "https://www.gemeinschaftspraxis-guenther.de/"),
    ("Tanja Weber", None),
    ("Covendos", None),   # link removed (Martin 30.10.)
    ("Zweite Liebe", "https://www.sanremo.ma/"),
    ("WHITEsmile", "https://www.whitesmile.de/"),
    ("ag+", "https://ahrens-gonzalves.de/"),
    ("CCI Transport", "https://www.cci-transport.de/"),
    ("SanRemo", "https://www.sanremo.ma/"),
    ("starks", None),
    ("ecowerth", None),
    ("Covendos Healthcare Group", None),   # Martin 30.10., not linked
]

# Title and description: Martin's wording, unchanged on 05.11.2026 at his request (the title is longer than the
# ~60 characters Google shows; seo_check.py reports that as a warning only). English: the title app.js already used;
# the English description was missing: a translation of the German one, shortened to 160 characters (05.11.2026).
TITLE = {"de": "Grafitecture · KI-Systeme für Marken · Martin Schweppe, Dipl.-Des., Mannheim",
         "en": "Grafitecture · AI systems for brands · Martin Schweppe, Dipl.-Des., Mannheim"}
DESC = {"de": ("Martin Schweppe, Diplom-Designer, baut KI-Systeme für Marken: KI-Websites, KI-Agenten, "
               "Content-Engines und Workflow-Automation. Grafitecture GmbH, Mannheim, seit 2000."),
        "en": ("Martin Schweppe, graduate designer, builds AI systems for brands: AI websites, agents, "
               "content engines and automation. Grafitecture GmbH, Mannheim, since 2000.")}
OG_TITLE = {"de": "Grafitecture · Marken mit KI. Ich baue KI-Systeme, die für Ihre Marke arbeiten.",
            "en": "Grafitecture · Brands with AI. I build AI systems that work for your brand."}
OG_ALT = {"de": "Grafitecture: Marken mit KI. Martin Schweppe, Diplom-Designer, Mannheim",
          "en": "Grafitecture: Brands with AI. Martin Schweppe, graduate designer, Mannheim"}
# title and description of the legal pages (new on 05.11.2026)
LEGAL_META = {
    ("impressum", "de"): ("Impressum · Grafitecture GmbH, Mannheim",
                          "Impressum der Grafitecture GmbH, Mannheim: Anschrift, Vertretung durch Martin Schweppe, "
                          "Handelsregister HRB 432625 und Umsatzsteuer-Identifikationsnummer."),
    ("impressum", "en"): ("Legal notice · Grafitecture GmbH, Mannheim",
                          "Legal notice of Grafitecture GmbH, Mannheim, Germany: address, managing director "
                          "Martin Schweppe, commercial register HRB 432625 and VAT identification number."),
    ("datenschutz", "de"): ("Datenschutz · Grafitecture GmbH, Mannheim",
                            "Datenschutzerklärung der Grafitecture GmbH: Hosting bei Vercel, Kontakt per E-Mail, "
                            "keine Cookies und kein Tracking, Ihre Rechte nach der DSGVO."),
    ("datenschutz", "en"): ("Privacy policy · Grafitecture GmbH, Mannheim",
                            "Privacy policy of Grafitecture GmbH, Mannheim: hosting by Vercel, contact by email, "
                            "no cookies and no tracking, and your rights under the GDPR."),
}
# link preview images (1200x630, tools/render_assets.py): „Marken / mit KI.“ and, since 05.11.2026, „Brands / with AI.“
OG_IMAGE = {"de": "assets/og/grafitecture-og.png", "en": "assets/og/grafitecture-og-en.png"}
# Google Search Console, property https://www.grafitecture.de/ (Martin's account, 05.11.2026): ownership check by
# meta tag. Keep it, or the property loses its verification. (A file check would not work: cleanUrls redirects .html.)
GOOGLE_SITE_VERIFICATION = "E5hh_5YzfsqNIsu4hf9doWHHFXT4N5GLNTrq7SMHQeg"

ARROW = ('<svg viewBox="0 0 22 10" aria-hidden="true" focusable="false">'
         '<path d="M0 5h20.5M16 .8 20.5 5 16 9.2" fill="none" stroke="currentColor" stroke-width="1.5"/></svg>')

# Content-Security-Policy: only this domain. Scripts by hash since 05.11.2026 (no 'unsafe-inline'): every inline
# <script> goes through script_tag(), which records its SHA-256; vercel.json lists exactly those. Styles keep
# 'unsafe-inline' (inline <style> and the style="--w:…" of the client logos). JSON-LD is data, not script.
SCRIPT_HASHES = set()
CSP = ("default-src 'self'; script-src 'self' {hashes}; style-src 'self' 'unsafe-inline'; "
       "img-src 'self' data:; font-src 'self' data:; connect-src 'self'; form-action mailto:; "
       "frame-ancestors 'none'; base-uri 'self'; object-src 'none'")
# /.well-known/security.txt (RFC 9116). Renew before it expires: seo_check.py fails 30 days before.
SECURITY_TXT_EXPIRES = "2027-11-01T00:00:00Z"


def script_tag(js: str) -> str:
    """<script> with the code on its own lines; the exact text between the tags is what the browser hashes."""
    text = "\n" + js + "\n"
    SCRIPT_HASHES.add("'sha256-" + base64.b64encode(hashlib.sha256(text.encode()).digest()).decode() + "'")
    return f"<script>{text}</script>"


def versioned(rel: str) -> str:
    """URL with a content hash, so /assets can be cached as immutable and still update when a file changes."""
    h = hashlib.sha1((ROOT / rel).read_bytes()).hexdigest()[:10]
    return f"{rel}?v={h}"


def font_css(inline: bool, prefix: str = "") -> str:
    """prefix "/" makes the font URL absolute (404 page, pages under /en/)."""
    out = []
    for fam, file, extra in FONTS:
        fmt = "woff2" if file.endswith(".woff2") else "woff"
        if inline:
            data = base64.b64encode((ASSETS / "fonts" / file).read_bytes()).decode()
            src = f'url(data:font/{fmt};base64,{data}) format("{fmt}")'
        else:
            src = f'url("{prefix}{versioned("assets/fonts/" + file)}") format("{fmt}")'
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
    """deploy: separate file with content hash (cacheable), absolute (pages under /en/); inline: data URI, so the
    preview never depends on supporting files."""
    rel = f"assets/clients/{f.name}"
    if mode == "inline":
        mime = "image/svg+xml" if f.suffix == ".svg" else "image/png"
        return f"data:{mime};base64,{base64.b64encode(f.read_bytes()).decode()}"
    return "/" + versioned(rel) if mode == "deploy" else rel


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


# photos supplied by Martin (25.10.2026); 640 and 1280 px wide JPEGs in assets/photos.
# Last field: a very small caption under the photo, the same in both languages (None = no caption).
PHOTOS = {
    "IMG_PORTRAIT": ("martin-schweppe", "Martin Schweppe, Diplom-Designer", "Martin Schweppe, graduate designer",
                     "(min-width: 1100px) 30vw, (min-width: 600px) 520px, 92vw", "Martin Schweppe"),  # caption: Martin 29.10.
    "IMG_DOOR": ("eingang", "Hauseingang mit Holztür und der Jahreszahl 1926", "Entrance with a wooden door marked 1926",
                 "(min-width: 1100px) 30vw, (min-width: 600px) 520px, 92vw", None),
}


def photo_html(key: str, mode: str, lang=None) -> str:
    """lang None: both alt texts (the preview switches them in place); 'de'/'en': the alt text of that page."""
    stem, alt_de, alt_en, sizes, caption = PHOTOS[key]
    small, large = ASSETS / "photos" / f"{stem}-640.jpg", ASSETS / "photos" / f"{stem}-1280.jpg"
    w, h = natural_size_jpeg(large)
    if lang:
        alts = f'alt="{html.escape(alt_de if lang == "de" else alt_en)}"'
    else:
        alts = f'alt="{html.escape(alt_de)}" data-alt-de="{html.escape(alt_de)}" data-alt-en="{html.escape(alt_en)}"'
    if mode == "inline":
        src = f'src="data:image/jpeg;base64,{base64.b64encode(small.read_bytes()).decode()}"'
    else:
        a, b = f"assets/photos/{small.name}", f"assets/photos/{large.name}"
        if mode == "deploy":
            a, b = "/" + versioned(a), "/" + versioned(b)
        src = f'src="{b}" srcset="{a} 640w, {b} 1280w" sizes="{sizes}"'
    cap = f'<figcaption class="small">{html.escape(caption)}</figcaption>' if caption else ""
    img = f'<img {src} {alts} width="{w}" height="{h}" loading="lazy" decoding="async">'
    if mode == "deploy" and small.with_suffix(".avif").exists() and large.with_suffix(".avif").exists():
        # AVIF (05.11.2026, tools/encode_photos.py): about a third smaller; browsers without AVIF take the JPEG
        av = ["/" + versioned("assets/photos/" + f.with_suffix(".avif").name) for f in (small, large)]
        img = f'<picture><source type="image/avif" srcset="{av[0]} 640w, {av[1]} 1280w" sizes="{sizes}">{img}</picture>'
    return f'<figure class="photo">{img}{cap}</figure>'


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


def render_body(mode: str, lang=None) -> str:
    body = (SRC / "body.html").read_text()
    body = (body.replace("{{LOGO_DARK}}", inline_logo("grafitecture.svg"))
                .replace("{{LOGO_WHITE}}", inline_logo("grafitecture-white.svg"))
                .replace("{{ARROW}}", ARROW)
                .replace("{{CLIENTS}}", clients_html(mode))
                .replace("{{CLIENT_COUNT}}", str(len(CLIENTS))))
    for key in PHOTOS:
        body = body.replace("{{" + key + "}}", photo_html(key, mode, lang))
    left = re.findall(r"\{\{[A-Z_]+\}\}", body)
    assert not left, f"unreplaced placeholders: {left}"
    return body


# ---------------------------------------------------------------- one language per page (05.11.2026)

class _OneLanguage(HTMLParser):
    """Copies HTML unchanged, except: every element whose lang attribute is `drop` is left out with all it contains,
    and a line break follows each <br> (text extractors without CSS otherwise glue „Marken“ and „mit KI.“ together;
    in the browser a break at the start of a line is collapsed, so nothing moves)."""
    VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "source", "track", "wbr"}

    def __init__(self, drop):
        super().__init__(convert_charrefs=False)
        self.drop, self.out, self.skip = drop, [], 0

    def handle_starttag(self, tag, attrs):
        if self.skip:
            if tag not in self.VOID:
                self.skip += 1
            return
        if self.drop and dict(attrs).get("lang") == self.drop and tag not in self.VOID:
            self.skip = 1
            return
        self.out.append(self.get_starttag_text())
        if tag == "br" and self.drop:
            self.out.append("\n")

    def handle_startendtag(self, tag, attrs):
        if not self.skip:
            self.out.append(self.get_starttag_text())

    def handle_endtag(self, tag):
        if self.skip:
            if tag not in self.VOID:
                self.skip -= 1
            return
        self.out.append(f"</{tag}>")

    def handle_data(self, d):
        if not self.skip:
            self.out.append(d)

    def handle_entityref(self, name):
        if not self.skip:
            self.out.append(f"&{name};")

    def handle_charref(self, name):
        if not self.skip:
            self.out.append(f"&#{name};")

    def handle_comment(self, d):
        if not self.skip:
            self.out.append(f"<!--{d}-->")


def only_lang(markup: str, lang) -> str:
    """Keeps the elements of `lang` and drops those of the other language (lang None: copy unchanged)."""
    drop = None if lang is None else ("en" if lang == "de" else "de")
    p = _OneLanguage(drop)
    p.feed(markup)
    p.close()
    return "".join(p.out)


LANG_BTN = re.compile(r'<button type="button" data-set-lang="(de|en)" aria-pressed="(?:true|false)" title="([^"]+)">(DE|EN)</button>')


def lang_links(markup: str, lang: str, page: str) -> str:
    """The DE/EN buttons become links to the same page in the other language (the active one: aria-current)."""
    def rep(m):
        l, title, label = m.group(1), m.group(2), m.group(3)
        cur = ' aria-current="page"' if l == lang else ""
        # no lang attribute: styles.css hides [lang] of the other language
        return f'<a href="{PAGES[page][l]}" hreflang="{l}" data-set-lang="{l}" title="{title}"{cur}>{label}</a>'
    out, n = LANG_BTN.subn(rep, markup)
    assert n >= 2, "language buttons not found"
    return out


def legal_links(markup: str, lang: str, keep_dialog: bool) -> str:
    """Impressum and Datenschutz links point to their pages; on / and /en a click still opens the dialog
    (app.js reads data-open), on the legal pages and the 404 page they are plain links."""
    for page in ("impressum", "datenschutz"):
        target = PAGES[page][lang]
        old = f'href="#{page}" data-open="{page}"'
        assert old in markup, old
        markup = markup.replace(old, f'href="{target}" data-open="{page}"' if keep_dialog else f'href="{target}"')
    return markup


def page_body(lang: str) -> str:
    """The start page in one language."""
    body = render_body("deploy", lang)
    body = body.replace('<div class="site" id="site" data-lang="de">', f'<div class="site" id="site" data-lang="{lang}">', 1)
    if lang == "en":
        body = body.replace("?subject=Strategiegespr%C3%A4ch", "?subject=Strategy%20call", 1)
    body = legal_links(body, lang, keep_dialog=True)
    return lang_links(only_lang(body, lang), lang, "home")


styles = (SRC / "styles.css").read_text()
app = (SRC / "app.js").read_text()
for l in LANGS:   # app.js sets document.title from its own table: keep both in step
    assert TITLE[l] in app, f"title ({l}) in app.js differs from TITLE in build.py"

# ---------------------------------------------------------------- structured data (JSON-LD, 05.11.2026)
# One linked @graph per page with stable @ids. Only what the page shows: no telephone, opening hours or ratings
# (there are none on the site). Services and texts in the language of the page.
ORG_ID, SITE_ID, PERSON_ID, LOGO_ID = SITE + "/#organization", SITE + "/#website", SITE + "/#martin-schweppe", SITE + "/#logo"
LD_TEXT = {
    "de": {"job": "Geschäftsführer, Diplom-Designer", "degree": "Diplom-Designer", "catalog": "Leistungen",
           "home": "Startseite"},
    "en": {"job": "Managing Director, graduate designer (Dipl.-Des.)", "degree": "Diplom-Designer (graduate designer)",
           "catalog": "Services", "home": "Home"},
}


def services(page_html: str) -> list:
    """The six services („Was ich baue“) as shown on the page: headline and description."""
    out = []
    ul = re.search(r'<ul class="rows svc">(.*?)</ul>', page_html, flags=re.S).group(1)
    for h3, p in re.findall(r'<h3 class="h4">(.*?)</h3>\s*<p>(.*?)</p>', ul, flags=re.S):
        clean = lambda t: re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", "", t))).replace("\u00ad", "").strip()
        out.append((clean(h3), clean(p)))
    assert len(out) == 6, out
    return out


def jsonld(page: str, lang: str, title: str, desc: str, body: str) -> str:
    url = abs_url(PAGES[page][lang])
    t = LD_TEXT[lang]
    org = {
        "@type": "ProfessionalService", "@id": ORG_ID,
        "name": "Grafitecture GmbH", "alternateName": "Grafitecture", "url": SITE_URL,
        "logo": {"@type": "ImageObject", "@id": LOGO_ID, "url": SITE_URL + "assets/logo/grafitecture-logo.png",
                 "contentUrl": SITE_URL + "assets/logo/grafitecture-logo.png", "width": 1200, "height": 400,
                 "caption": "Grafitecture"},
        "image": SITE_URL + OG_IMAGE[lang],
        "description": DESC[lang],
        "email": "martin.schweppe@grafitecture.de",
        "address": {"@type": "PostalAddress", "streetAddress": "Rebenstr. 9a", "postalCode": "68309",
                    "addressLocality": "Mannheim", "addressCountry": "DE"},
        "foundingDate": "2000",
        "employee": {"@id": PERSON_ID},
        "knowsLanguage": ["de", "en"],
        "sameAs": ["https://www.instagram.com/g.r.a.f.i.t.e.c.t.u.r.e/"],   # Martin 01.11.2026
    }
    if page == "home":
        org["hasOfferCatalog"] = {"@type": "OfferCatalog", "name": t["catalog"], "itemListElement": [
            {"@type": "Offer", "itemOffered": {"@type": "Service", "name": n, "description": d, "provider": {"@id": ORG_ID}}}
            for n, d in services(body)]}
    person = {
        "@type": "Person", "@id": PERSON_ID, "name": "Martin Schweppe", "jobTitle": t["job"],
        "worksFor": {"@id": ORG_ID},
        "image": SITE_URL + "assets/photos/martin-schweppe-1280.jpg",
        "hasCredential": {"@type": "EducationalOccupationalCredential", "credentialCategory": "degree", "name": t["degree"]},
    }
    website = {"@type": "WebSite", "@id": SITE_ID, "url": SITE_URL, "name": "Grafitecture",
               "publisher": {"@id": ORG_ID}, "inLanguage": list(LANGS)}
    webpage = {"@type": "WebPage", "@id": url + "#webpage", "url": url, "name": title, "description": desc,
               "inLanguage": lang, "isPartOf": {"@id": SITE_ID}, "about": {"@id": ORG_ID},
               "primaryImageOfPage": {"@type": "ImageObject", "url": SITE_URL + OG_IMAGE[lang]}}
    graph = [org, website, person, webpage]
    if page != "home":
        name = re.search(r'<h1[^>]*>(.*?)</h1>', body, flags=re.S).group(1)
        webpage["breadcrumb"] = {"@id": url + "#breadcrumb"}
        graph.append({"@type": "BreadcrumbList", "@id": url + "#breadcrumb", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": t["home"], "item": abs_url(PAGES["home"][lang])},
            {"@type": "ListItem", "position": 2, "name": name, "item": url}]})
    return json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False).replace("</", "<\\/")


def copy_clients(out: pathlib.Path):
    d = ASSETS / "clients"
    if d.exists() and any(d.iterdir()):
        shutil.copytree(d, out / "assets" / "clients", ignore=shutil.ignore_patterns("*.txt", "*.json", ".*"))


# ---------------------------------------------------------------- redirects (seo/redirect-map.csv)

def redirect_map():
    """seo/redirect-map.csv: alt, neu, status, grund, quelle. One row per old address (Vercel path syntax, e.g.
    /arbeiten/:path*). Addresses without a file extension also match with a trailing slash."""
    with (ROOT / "seo" / "redirect-map.csv").open(encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def redirects() -> list:
    out = []
    # 1. production aliases on vercel.app → www (they are behind Vercel Authentication anyway)
    for host in VERCEL_ALIASES:
        out.append({"source": "/:path*", "has": [{"type": "host", "value": host}],
                    "destination": SITE + "/:path*", "permanent": True})
    # 2. the pages themselves: with a trailing slash → without (one canonical address)
    for paths in PAGES.values():
        for p in paths.values():
            if p != "/":
                out.append({"source": p + "/", "destination": p, "permanent": True})
    # 3. old addresses
    for r in redirect_map():
        src, dest, status = r["alt"], r["neu"], int(r["status"])
        variants = [src] if re.search(r"\.\w+$", src) or src.endswith("*") else [src, src + "/"]
        for v in variants:
            rule = {"source": v, "destination": dest}
            rule.update({"permanent": True} if status == 308 else {"statusCode": status})
            out.append(rule)
    return out


# ---------------------------------------------------------------- 404 page

def footer_html(lang=None, plain=False) -> str:
    """The footer of the start page with absolute links, for the 404 page (lang None: both languages, links of the
    German pages; the script switches them) and the legal pages (one language)."""
    body = (SRC / "body.html").read_text()
    ftr = re.search(r'<footer class="ftr">.*?</footer>', body, flags=re.S).group(0)
    ftr = ftr.replace("{{LOGO_DARK}}", inline_logo("grafitecture.svg"))
    ftr = ftr.replace('href="#top"', f'href="{PAGES["home"][lang or "de"]}"')
    ftr = legal_links(ftr, lang or "de", keep_dialog=False)
    return only_lang(ftr, lang) if lang else ftr


# 404 page: switches in place (both languages); in English its links lead to the English pages.
NF_LINKS_EN = {"/": "/en", "/#kontakt": "/en#kontakt", "/impressum": "/en/legal-notice",
               "/datenschutz": "/en/privacy-policy"}
NF_SCRIPT = """(() => {
  'use strict';
  const site = document.getElementById('site');
  const T = { de: 'Seite nicht gefunden · Grafitecture', en: 'Page not found · Grafitecture' };
  const EN = %s;
  const links = Array.from(document.querySelectorAll('a[href^="/"]'));
  links.forEach((a) => { a.dataset.href = a.getAttribute('href'); });
  function setLang(l) {
    const lang = l === 'en' ? 'en' : 'de';
    site.dataset.lang = lang;
    document.documentElement.lang = lang;
    document.title = T[lang];
    document.querySelectorAll('[data-set-lang]').forEach((b) => b.setAttribute('aria-pressed', String(b.dataset.setLang === lang)));
    links.forEach((a) => { const h = a.dataset.href; a.setAttribute('href', lang === 'en' ? (EN[h] || h) : h); });
  }
  document.querySelectorAll('[data-set-lang]').forEach((b) => b.addEventListener('click', () => setLang(b.dataset.setLang)));
  let initial = 'de';
  try {
    if (/^\\/en(\\/|$)/.test(location.pathname) || new URLSearchParams(location.search).get('lang') === 'en' || location.hash === '#en') initial = 'en';
  } catch (e) { /* ignore */ }
  setLang(initial);
})();""" % json.dumps(NF_LINKS_EN)


def render_404() -> str:
    body = (SRC / "404.html").read_text()
    body = (body.replace("{{FOOTER}}", footer_html())
                .replace("{{LOGO_DARK}}", inline_logo("grafitecture.svg"))
                .replace("{{ARROW}}", ARROW))
    left = re.findall(r"\{\{[A-Z_]+\}\}", body)
    assert not left, f"unreplaced placeholders in 404.html: {left}"
    font_url = "/" + versioned(FONT_FILE)
    return f"""<!doctype html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>Seite nicht gefunden · Grafitecture</title>
<meta name="robots" content="noindex">
<meta name="theme-color" content="#FFFFFF">
<link rel="icon" href="/favicon-32.png" sizes="32x32" type="image/png">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="preload" href="{font_url}" as="font" type="font/woff2" crossorigin>
<style>
{font_css(False, "/")}
{styles}
</style>
</head>
<body>
{body}
{script_tag(NF_SCRIPT)}
</body>
</html>
"""


# ---------------------------------------------------------------- page head

def head(lang: str, page: str, title: str, desc: str, body: str) -> str:
    font_url = "/" + versioned(FONT_FILE)
    alt = "".join(f'<link rel="alternate" hreflang="{l}" href="{abs_url(PAGES[page][l])}">\n' for l in LANGS)
    alt += f'<link rel="alternate" hreflang="x-default" href="{abs_url(PAGES[page]["de"])}">\n'
    verify = (f'<meta name="google-site-verification" content="{GOOGLE_SITE_VERIFICATION}">\n'
              if (page, lang) == ("home", "de") else "")
    og = f"""<meta property="og:type" content="website">
<meta property="og:site_name" content="Grafitecture">
<meta property="og:url" content="{abs_url(PAGES[page][lang])}">
<meta property="og:title" content="{html.escape(OG_TITLE[lang] if page == 'home' else title)}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:image" content="{SITE_URL}{OG_IMAGE[lang]}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{html.escape(OG_ALT[lang])}">
<meta property="og:locale" content="{'de_DE' if lang == 'de' else 'en_GB'}">
<meta property="og:locale:alternate" content="{'en_GB' if lang == 'de' else 'de_DE'}">
<meta name="twitter:card" content="summary_large_image">
"""
    og += f'<script type="application/ld+json">{jsonld(page, lang, title, desc, body)}</script>\n'
    return f"""<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
<meta name="robots" content="{ROBOTS_INDEX}">
<meta name="theme-color" content="#FFFFFF">
<link rel="canonical" href="{abs_url(PAGES[page][lang])}">
{alt}{verify}<link rel="icon" href="/favicon-32.png" sizes="32x32" type="image/png">
<link rel="icon" href="/favicon-48.png" sizes="48x48" type="image/png">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
<link rel="preload" href="{font_url}" as="font" type="font/woff2" crossorigin>
{og}<style>
{font_css(False, "/")}
{styles}
</style>"""


def render_home(lang: str) -> str:
    body = page_body(lang)
    return f"""<!doctype html>
<html lang="{lang}">
<head>
{head(lang, "home", TITLE[lang], DESC[lang], body)}
</head>
<body>
{body}
{script_tag(app)}
</body>
</html>
"""


# ---------------------------------------------------------------- legal pages (05.11.2026)

def nf_header(lang: str) -> str:
    """The header of the 404 page (logo, DE/EN, no menu); render_legal turns the buttons into links."""
    src = (SRC / "404.html").read_text()
    hdr = re.search(r'<header class="hdr" id="hdr">.*?</header>', src, flags=re.S).group(0)
    hdr = hdr.replace("{{LOGO_DARK}}", inline_logo("grafitecture.svg"))
    return hdr.replace('<a class="logo" href="/"', f'<a class="logo" href="{PAGES["home"][lang]}"', 1)


def render_legal(page: str, lang: str) -> str:
    """Impressum / Datenschutz as a page: the text of the dialog in body.html (one source for both)."""
    body = (SRC / "body.html").read_text()
    dlg = re.search(rf'<dialog class="legal" id="{page}".*?</dialog>', body, flags=re.S).group(0)
    h2 = re.search(r"<h2[^>]*>(.*?)</h2>", dlg, flags=re.S).group(1)
    name = re.search(rf'<span lang="{lang}">(.*?)</span>', h2).group(1)
    text = re.search(rf'<div class="legal-body" lang="{lang}">.*?</div>', dlg, flags=re.S).group(0)
    # under the page's h1 the sections are h2 (in the dialog they follow its h2 as h3); same look through .h6
    text = re.sub(r"<h3( class=\"h6\">.*?)</h3>", r"<h2\1</h2>", text, flags=re.S)
    skip = re.search(r'<a class="skip".*?</a>', body).group(0)
    markup = f"""<div class="site nf" id="site" data-lang="{lang}">
{skip}

{nf_header(lang)}

<main id="main">
<section class="sec legal-page" aria-labelledby="t-page">
  <div class="wrap">
    <header class="legal-hd"><h1 class="h3" id="t-page">{name}</h1></header>
    {text}
  </div>
</section>
</main>

{footer_html(lang)}
</div>"""
    title, desc = LEGAL_META[(page, lang)]
    body = lang_links(only_lang(markup, lang), lang, page)
    return f"""<!doctype html>
<html lang="{lang}">
<head>
{head(lang, page, title, desc, body)}
</head>
<body>
{body}
</body>
</html>
"""


# ---------------------------------------------------------------- other files

def favicon_ico(png: pathlib.Path) -> bytes:
    """/favicon.ico (asked for 43 times since the launch): the 32 px PNG wrapped in an ICO container."""
    data = png.read_bytes()
    w, h = struct.unpack(">II", data[16:24])
    header = struct.pack("<HHH", 0, 1, 1)
    entry = struct.pack("<BBBBHHII", w % 256, h % 256, 0, 0, 1, 32, len(data), 6 + 16)
    return header + entry + data


def content_hash(doc: str) -> str:
    """What a reader gets from a page: title, description and the visible text of <main> (no markup, no asset
    versions). lastmod in the sitemap changes only when this changes."""
    title = re.search(r"<title>(.*?)</title>", doc, flags=re.S).group(1)
    desc = re.search(r'<meta name="description" content="([^"]*)"', doc).group(1)
    main = re.search(r"<main.*?</main>", doc, flags=re.S).group(0)
    text = re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", main))).strip()
    return hashlib.sha256(f"{title}\n{desc}\n{text}".encode()).hexdigest()[:16]


def lastmod(docs: dict) -> dict:
    """seo/lastmod.json keeps, per address, the hash of its content and the day it last changed. Dates only move
    when the content changes, so rebuilding never changes the sitemap by itself (commit the file with the change)."""
    f = ROOT / "seo" / "lastmod.json"
    known = json.loads(f.read_text()) if f.exists() else {}
    today = datetime.date.today().isoformat()
    out = {}
    for path, doc in docs.items():
        h = content_hash(doc)
        old = known.get(path, {})
        out[path] = {"hash": h, "date": old["date"] if old.get("hash") == h else today}
    f.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")
    return {p: v["date"] for p, v in out.items()}


def sitemap(dates: dict) -> str:
    """Every indexable address with its last content change, its language versions (hreflang) and, on the start
    pages, the two photos (Google image search)."""
    photos = "".join(f'    <image:image><image:loc>{SITE}/assets/photos/{stem}-1280.jpg</image:loc></image:image>\n'
                     for stem, *_ in PHOTOS.values())
    urls = []
    for page, paths in PAGES.items():
        alts = "".join(f'    <xhtml:link rel="alternate" hreflang="{l}" href="{abs_url(paths[l])}"/>\n' for l in LANGS)
        alts += f'    <xhtml:link rel="alternate" hreflang="x-default" href="{abs_url(paths["de"])}"/>\n'
        for lang in LANGS:
            p = paths[lang]
            urls.append(f"  <url>\n    <loc>{abs_url(p)}</loc>\n    <lastmod>{dates[p]}</lastmod>\n{alts}"
                        f"{photos if page == 'home' else ''}  </url>\n")
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">
{"".join(urls)}</urlset>
"""


# robots.txt (05.11.2026). Search engines and AI answer engines may read and cite everything; AI training is allowed
# too (Martin, 05.11.2026). Explicit groups, so the decision is visible and easy to change: to stop training, set
# AI_TRAINING = False (the training crawlers then get „Disallow: /“; search and citations stay allowed).
# Names checked against the operators' documentation and github.com/ai-robots-txt/ai.robots.txt on 05.11.2026.
AI_TRAINING = True
BOTS_SEARCH = ["Googlebot", "Bingbot", "OAI-SearchBot", "ChatGPT-User", "Claude-SearchBot", "Claude-User", "PerplexityBot",
               "Perplexity-User", "Applebot", "DuckAssistBot", "MistralAI-User", "meta-webindexer", "Meta-ExternalFetcher"]
BOTS_TRAINING = ["GPTBot", "ClaudeBot", "Google-Extended", "Applebot-Extended", "CCBot", "meta-externalagent", "Bytespider"]


def robots() -> str:
    def group(names, rule):
        return "".join(f"User-agent: {n}\n" for n in names) + rule + "\n"
    return ("# grafitecture.de – built by build.py, do not edit by hand\n\n"
            "# Search engines and AI answer engines: read and cite\n" + group(BOTS_SEARCH, "Allow: /") + "\n"
            "# AI training (Google-Extended and Applebot-Extended are opt-out tokens, not crawlers)\n"
            + group(BOTS_TRAINING, "Allow: /" if AI_TRAINING else "Disallow: /") + "\n"
            "# Everyone else\n" + group(["*"], "Allow: /") + f"\nSitemap: {SITE_URL}sitemap.xml\n")


def llms_txt(de_body: str) -> str:
    """/llms.txt (llmstxt.org): a short Markdown summary for AI tools and agents, built from the German page so it
    never drifts from it. Google does not use it; it is served with X-Robots-Tag: noindex."""
    def text(t):
        return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", t))).replace("\u00ad", "").replace(" .", ".").strip()
    lead = text(re.search(r'<div class="hero-side">\s*<p>(.*?)</p>', de_body, flags=re.S).group(1))
    steps = [text(h) for h in re.findall(r'<li class="row"><span class="num"[^>]*>\d+</span><h3 class="h4">(.*?)</h3>', de_body)]
    svc = "".join(f"- **{n}:** {d}\n" for n, d in services(de_body))
    pages = "".join(f"- [{name}]({abs_url(path)}): {what}\n" for name, path, what in (
        ("Startseite", "/", "Leistungen, Über mich, Ablauf, Referenzen (Kundenlogos) und Kontakt, auf Deutsch"),
        ("Home (English)", "/en", "the same page in English"),
        ("Impressum", "/impressum", "Anbieterkennzeichnung, Handelsregister, USt-IdNr."),
        ("Datenschutz", "/datenschutz", "Datenschutzerklärung")))
    return f"""# Grafitecture GmbH

> {DESC["de"]}

{lead}

- Geschäftsführer: Martin Schweppe, Diplom-Designer
- Anschrift: Grafitecture GmbH, Rebenstr. 9a, 68309 Mannheim, Deutschland
- E-Mail: martin.schweppe@grafitecture.de
- Erstes Strategiegespräch: 30 Minuten, kostenlos
- Sprachen: Deutsch, Englisch

## Leistungen

{svc}
## Ablauf

{" → ".join(steps)}

## Referenzen

Ausgewählte Kunden aus 26 Jahren: {", ".join(n for n, _ in CLIENTS)}.

## Seiten

{pages}
## Optional

- [Legal notice (English)]({abs_url("/en/legal-notice")})
- [Privacy policy (English)]({abs_url("/en/privacy-policy")})
"""


def security_txt() -> str:
    return (f"Contact: mailto:martin.schweppe@grafitecture.de\nExpires: {SECURITY_TXT_EXPIRES}\n"
            f"Preferred-Languages: de, en\nCanonical: {SITE}/.well-known/security.txt\n")


def manifest() -> dict:
    """Web app manifest (05.11.2026): name, colours and the „g“ icon for home screens and browser UIs."""
    icons = []
    for size in (192, 512):
        for purpose in ("any", "maskable"):   # the „g“ fills 62 % of the square, inside the maskable safe zone
            icons.append({"src": f"/icon-{size}.png", "sizes": f"{size}x{size}", "type": "image/png", "purpose": purpose})
    return {"name": "Grafitecture", "short_name": "Grafitecture", "description": DESC["de"], "lang": "de",
            "start_url": "/", "scope": "/", "display": "browser", "background_color": "#FFFFFF", "theme_color": "#FFFFFF",
            "icons": icons}


def vercel_config() -> dict:
    return {
        "$schema": "https://openapi.vercel.sh/vercel.json",
        "framework": None,
        "outputDirectory": "public",
        "cleanUrls": True,
        # Vercel Functions would run in Frankfurt (privacy note by S. Enders, 26.10.2026).
        # The site has no functions; the static files are served by the CDN closest to the visitor.
        "regions": ["fra1"],
        "redirects": redirects(),
        "headers": [
            {"source": "/assets/(.*)", "headers": [{"key": "Cache-Control", "value": "public, max-age=31536000, immutable"}]},
            {"source": "/llms.txt", "headers": [{"key": "X-Robots-Tag", "value": "noindex"}]},
            # previews and the vercel.app aliases never get indexed (Vercel sets this too; this keeps it explicit)
            {"source": "/(.*)", "has": [{"type": "host", "value": r".*\.vercel\.app"}],
             "headers": [{"key": "X-Robots-Tag", "value": "noindex"}]},
            {"source": "/(.*)", "headers": [
                {"key": "Content-Security-Policy", "value": CSP.format(hashes=" ".join(sorted(SCRIPT_HASHES)))},
                {"key": "Cross-Origin-Opener-Policy", "value": "same-origin"},
                {"key": "X-Content-Type-Options", "value": "nosniff"},
                {"key": "X-Frame-Options", "value": "DENY"},
                {"key": "Referrer-Policy", "value": "strict-origin-when-cross-origin"},
                {"key": "Permissions-Policy", "value": "camera=(), microphone=(), geolocation=(), browsing-topics=()"}
            ]}
        ]
    }


def write(out: pathlib.Path, rel: str, text: str):
    f = out / rel
    f.parent.mkdir(parents=True, exist_ok=True)
    f.write_text(text)


def build_deploy():
    out = ROOT / "public"   # generated only: everything in it is rebuilt from src/ and assets/
    if out.exists():
        shutil.rmtree(out)
    (out / "assets").mkdir(parents=True)
    for sub in ("fonts", "logo", "og", "photos"):
        # the WOFF is kept in assets/ for tools/render_assets.py only; the site uses the WOFF2
        shutil.copytree(ASSETS / sub, out / "assets" / sub, ignore=shutil.ignore_patterns("*.woff") if sub == "fonts" else None)
    copy_clients(out)
    for icon in ("favicon.svg", "favicon-32.png", "favicon-48.png", "apple-touch-icon.png", "icon-192.png", "icon-512.png"):
        shutil.copy(ASSETS / "icons" / icon, out / icon)
    write(out, "site.webmanifest", json.dumps(manifest(), indent=2, ensure_ascii=False) + "\n")
    docs = {}
    for lang in LANGS:
        docs[PAGES["home"][lang]] = render_home(lang)
        for page in ("impressum", "datenschutz"):
            docs[PAGES[page][lang]] = render_legal(page, lang)
    for path, doc in docs.items():
        write(out, out_file(path), doc)
    write(out, "404.html", render_404())   # Vercel serves it with status 404 for any unknown address
    write(out, "sitemap.xml", sitemap(lastmod(docs)))
    write(out, f"{INDEXNOW_KEY}.txt", INDEXNOW_KEY)
    write(out, ".well-known/security.txt", security_txt())
    (out / "favicon.ico").write_bytes(favicon_ico(ASSETS / "icons" / "favicon-32.png"))
    write(out, "robots.txt", robots())
    write(out, "llms.txt", llms_txt(page_body("de")))
    (ROOT / "vercel.json").write_text(json.dumps(vercel_config(), indent=2) + "\n")
    return out


def build_artifact():
    out = DIST / "artifact"
    if out.exists():
        shutil.rmtree(out)
    (out / "assets").mkdir(parents=True)
    # the artifact viewer cannot submit forms anywhere: drop the no-JS mailto fallback, the script handles submit
    no_js_fallback = ' action="mailto:martin.schweppe@grafitecture.de" method="post" enctype="text/plain"'
    body = render_body("inline")   # client logos embedded as data URIs; both languages, switched in place
    assert body.count(no_js_fallback) == 1
    body = body.replace(no_js_fallback, "")
    page = f"""<title>Grafitecture</title>
<meta name="claude:viewport-fit-sides" content="cover">
<meta name="description" content="{DESC["de"]}">
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
    src_body = (SRC / "body.html").read_text()
    assert only_lang(src_body, None).lower() == src_body.lower(), "HTML copy is not lossless"
    d = build_deploy()
    a = build_artifact()
    for p in sorted(d.rglob("*.html")) + [a / "index.html"]:
        print(p.relative_to(ROOT), f"{p.stat().st_size/1024:.1f} KB")
    shown = sum(1 for n, _ in CLIENTS if client_logo(slug(n)))
    print(f"clients: {len(CLIENTS)} total, {shown} with logo file, {len(CLIENTS) - shown} as text")

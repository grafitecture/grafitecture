#!/usr/bin/env python3
"""Static checks over the built site (public/, vercel.json). Standard library only. Exit code 1 on any error.

  python3 scripts/seo_check.py

Per page: title and description present and unique (length outside the guide values is a warning: Martin keeps the
longer title on purpose), exactly one h1, html lang, canonical absolute and pointing to the page itself, hreflang
both ways with x-default, every img with alt, og:image absolute, JSON-LD parsable, no noindex (except the 404 page),
no resources from other domains (scripts, styles, fonts, images, frames).
Sitemap: every address exists, is canonical and indexable; every indexable page is in it.
robots.txt: no „Disallow: /“ for everyone or for a search crawler, Sitemap line present.
vercel.json: the CSP lists the hash of every inline script. security.txt not about to expire."""
import base64, datetime, hashlib, json, pathlib, re, sys
from html.parser import HTMLParser

ROOT = pathlib.Path(__file__).resolve().parents[1]
PUB = ROOT / "public"
SITE = "https://www.grafitecture.de"
NOINDEX_OK = {"/404"}
SEARCH_BOTS = {"*", "googlebot", "bingbot", "oai-searchbot", "claude-searchbot", "perplexitybot", "applebot", "duckassistbot"}

errors, warnings = [], []


def err(where, msg):
    errors.append(f"{where}: {msg}")


def warn(where, msg):
    warnings.append(f"{where}: {msg}")


class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.title, self.in_title, self.meta, self.links, self.h1 = "", False, {}, [], 0
        self.lang, self.imgs, self.scripts, self.res, self.cur_script = None, [], [], [], None
        self.levels, self.in_dialog = [], 0   # heading levels outside <dialog> (dialogs have their own outline)

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "html":
            self.lang = a.get("lang")
        elif tag == "title":
            self.in_title = True
        elif tag == "meta":
            key = a.get("name") or a.get("property")
            if key:
                self.meta.setdefault(key, []).append(a.get("content", ""))
        elif tag == "link":
            self.links.append(a)
            if (a.get("rel") or "") in ("stylesheet", "preload", "icon", "apple-touch-icon", "manifest"):
                self.res.append(a.get("href", ""))
        elif tag == "dialog":
            self.in_dialog += 1
        if tag == "h1":
            self.h1 += 1
        if re.fullmatch(r"h[1-6]", tag) and not self.in_dialog:
            self.levels.append(int(tag[1]))
        elif tag == "img":
            self.imgs.append(a)
            self.res.append(a.get("src", ""))
        elif tag in ("script", "iframe", "source", "video", "audio", "embed"):
            src = a.get("src") or a.get("srcset", "").split(" ")[0]
            if src:
                self.res.append(src)
            if tag == "script":
                self.cur_script = {"type": a.get("type"), "text": "", "src": a.get("src")}

    def handle_endtag(self, tag):
        if tag == "dialog":
            self.in_dialog -= 1
        if tag == "title":
            self.in_title = False
        if tag == "script" and self.cur_script is not None:
            self.scripts.append(self.cur_script)
            self.cur_script = None

    def handle_data(self, d):
        if self.in_title:
            self.title += d
        if self.cur_script is not None:
            self.cur_script["text"] += d


def address(f: pathlib.Path) -> str:
    rel = "/" + f.relative_to(PUB).as_posix()
    return "/" if rel == "/index.html" else rel[:-5]


def url(path):
    return SITE + "/" if path == "/" else SITE + path


pages = {}
for f in sorted(PUB.rglob("*.html")):
    p = Page()
    p.feed(f.read_text(encoding="utf-8"))
    pages[address(f)] = p

csp = ""
vercel = json.loads((ROOT / "vercel.json").read_text())
for rule in vercel.get("headers", []):
    for h in rule["headers"]:
        if h["key"].lower() == "content-security-policy":
            csp = h["value"]

titles, descs, indexable = {}, {}, set()
for path, p in pages.items():
    w = path
    robots = " ".join(p.meta.get("robots", []))
    if "noindex" in robots:
        if path not in NOINDEX_OK:
            err(w, "noindex on a page that should be indexed")
    else:
        indexable.add(path)
    # inline scripts: their hash must be in the CSP (otherwise the browser blocks them)
    for s in p.scripts:
        if s["src"] or (s["type"] and s["type"] != "text/javascript" and s["type"] != "module"):
            continue
        h = "'sha256-" + base64.b64encode(hashlib.sha256(s["text"].encode()).digest()).decode() + "'"
        if h not in csp:
            err(w, f"inline script {h} is not in the Content-Security-Policy (run build.py)")
    for s in p.scripts:
        if s["type"] == "application/ld+json":
            try:
                json.loads(s["text"])
            except ValueError as e:
                err(w, f"JSON-LD does not parse: {e}")
    for r in p.res:
        if re.match(r"^(https?:)?//", r) and not r.startswith(SITE):
            err(w, f"resource from another domain: {r}")
    if path in NOINDEX_OK:
        continue
    # one page, one topic
    t = p.title.strip()
    d = (p.meta.get("description") or [""])[0].strip()
    if not t:
        err(w, "no <title>")
    if not d:
        err(w, "no meta description")
    titles.setdefault(t, []).append(path)
    descs.setdefault(d, []).append(path)
    if not 30 <= len(t) <= 60:
        warn(w, f"title has {len(t)} characters (guide 50–60)")
    if not 120 <= len(d) <= 160:
        warn(w, f"description has {len(d)} characters (guide 140–160)")
    if p.h1 != 1:
        err(w, f"{p.h1} h1 elements (want exactly 1)")
    for prev, cur in zip(p.levels, p.levels[1:]):
        if cur > prev + 1:
            err(w, f"heading jumps from h{prev} to h{cur}")
            break
    if p.lang not in ("de", "en"):
        err(w, f"html lang is {p.lang!r}")
    canon = [l.get("href") for l in p.links if l.get("rel") == "canonical"]
    if canon != [url(path)]:
        err(w, f"canonical {canon} should be [{url(path)}]")
    alts = {l.get("hreflang"): l.get("href") for l in p.links if l.get("rel") == "alternate" and l.get("hreflang")}
    if not {"de", "en", "x-default"} <= set(alts):
        err(w, f"hreflang incomplete: {sorted(alts)}")
    if alts.get(p.lang) != url(path):
        err(w, f"hreflang {p.lang} does not point to the page itself")
    for img in p.imgs:
        if "alt" not in img:
            err(w, f"img without alt: {img.get('src')}")
    og = p.meta.get("og:image", [""])[0]
    if not og.startswith(SITE + "/"):
        err(w, f"og:image missing or not absolute: {og!r}")
    if not any(s["type"] == "application/ld+json" for s in p.scripts):
        err(w, "no JSON-LD")

for t, ps in titles.items():
    if len(ps) > 1:
        err(", ".join(ps), f"same title: {t}")
for d, ps in descs.items():
    if len(ps) > 1:
        err(", ".join(ps), "same description")

# hreflang must be confirmed by the other side
by_url = {url(p): p for p in pages}
for path, p in pages.items():
    if path in NOINDEX_OK:
        continue
    for lang, href in {l.get("hreflang"): l.get("href") for l in p.links if l.get("rel") == "alternate"}.items():
        other = pages.get(by_url.get(href, ""))
        if other is None:
            err(path, f"hreflang {lang} → {href} is not a page")
        elif url(path) not in [l.get("href") for l in other.links if l.get("rel") == "alternate"]:
            err(path, f"hreflang {lang} → {href} does not link back")

# sitemap
sm = (PUB / "sitemap.xml").read_text()
locs = re.findall(r"<loc>(.*?)</loc>", sm)
for loc in locs:
    path = loc[len(SITE):] or "/"
    if path not in pages:
        err("sitemap.xml", f"{loc} has no page")
    elif path not in indexable:
        err("sitemap.xml", f"{loc} is noindex")
for path in indexable:
    if url(path) not in locs:
        err("sitemap.xml", f"indexable page {url(path)} missing")
if re.search(r"<(priority|changefreq)>", sm):
    warn("sitemap.xml", "priority/changefreq are ignored by Google")

# robots.txt: groups of User-agent lines followed by rules
robots = (PUB / "robots.txt").read_text()
if not re.search(r"^Sitemap: https://www\.grafitecture\.de/sitemap\.xml$", robots, flags=re.M):
    err("robots.txt", "no absolute Sitemap line")
for block in re.split(r"\n\s*\n", robots):
    agents = {m.lower() for m in re.findall(r"^User-agent:\s*(\S+)", block, flags=re.M | re.I)}
    if agents & SEARCH_BOTS and re.search(r"^Disallow:\s*/\s*$", block, flags=re.M | re.I):
        err("robots.txt", f"„Disallow: /“ for {sorted(agents & SEARCH_BOTS)}")

# security.txt
sec = PUB / ".well-known" / "security.txt"
if not sec.exists():
    err("security.txt", "missing")
else:
    m = re.search(r"^Expires:\s*(\S+)", sec.read_text(), flags=re.M)
    exp = datetime.datetime.fromisoformat(m.group(1).replace("Z", "+00:00")) if m else None
    if not exp or exp - datetime.datetime.now(datetime.timezone.utc) < datetime.timedelta(days=30):
        err("security.txt", f"Expires {m.group(1) if m else '?'} is less than 30 days away: renew SECURITY_TXT_EXPIRES in build.py")

for w in warnings:
    print("WARN ", w)
for e in errors:
    print("ERROR", e)
print(f"\n{len(pages)} pages, {len(locs)} sitemap addresses: {len(errors)} errors, {len(warnings)} warnings")
sys.exit(1 if errors else 0)

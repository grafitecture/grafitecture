#!/usr/bin/env python3
"""IndexNow ping after a production deployment (Bing, Yandex, Seznam, Naver …; Google does not take part).
Sends only the addresses whose content changed in the deployed commit (seo/lastmod.json against the commit before);
--all sends every address of the sitemap. Standard library only.

  python3 scripts/indexnow.py [--all] [--dry-run]"""
import json, pathlib, re, subprocess, sys, urllib.request

ROOT = pathlib.Path(__file__).resolve().parents[1]
SITE = "https://www.grafitecture.de"
KEY = re.search(r'INDEXNOW_KEY = "([0-9a-f]+)"', (ROOT / "build.py").read_text()).group(1)


def lastmod(rev):
    r = subprocess.run(["git", "show", f"{rev}:seo/lastmod.json"], cwd=ROOT, capture_output=True, text=True)
    return json.loads(r.stdout) if r.returncode == 0 else {}


if "--all" in sys.argv:
    paths = sorted(lastmod("HEAD"))
else:
    now, before = lastmod("HEAD"), lastmod("HEAD~1")
    paths = sorted(p for p, v in now.items() if before.get(p, {}).get("date") != v["date"])
urls = [SITE + ("/" if p == "/" else p) for p in paths]
if not urls:
    print("IndexNow: no content changes, nothing to send")
    sys.exit(0)
body = {"host": "www.grafitecture.de", "key": KEY, "keyLocation": f"{SITE}/{KEY}.txt", "urlList": urls}
print("IndexNow:", json.dumps(body, indent=1))
if "--dry-run" in sys.argv:
    sys.exit(0)
req = urllib.request.Request("https://api.indexnow.org/indexnow", data=json.dumps(body).encode(),
                             headers={"Content-Type": "application/json; charset=utf-8"}, method="POST")
with urllib.request.urlopen(req, timeout=30) as r:
    print("IndexNow answered", r.status)   # 200 or 202 = accepted

#!/usr/bin/env python3
"""Instagram section of the website (Martin 20.11.2026), step 2 of 2.

Turns a snapshot of the profile grid (tools/instagram_snapshot.js, run in the built-in browser on the profile) into
the images in assets/instagram and assets/instagram/feed.json, which build.py reads. Nothing is loaded from Instagram
on the website: it serves these copies, and every tile is a plain link to its post.

- Order as on the profile, pinned posts first (18 tiles since 25.11.2026: 6 x 3 from 760 px, 3 x 6 on phones).
- Every tile is cut to 4:5 around the centre, the format of the posts (reels arrive as 640 x 1136 covers, older
  square posts as 1080 x 1080) and saved 400 and 800 px wide (reels 400 and 640: their cover is only 640 wide),
  each as JPEG and AVIF (the AVIF is offered first, the JPEG is the fallback, as with the photos).
- Alt texts (DE and EN) live in feed.json, keyed by the post code, and are kept when the feed is refreshed. A new
  post without them stops the run with a list: write alt_de and alt_en into feed.json (describe what the tile
  shows; for a reel start with „Reel:“) and run again.
- Images of posts that dropped out of the 18 are deleted.

Run:  python3 tools/instagram_feed.py /path/to/grafitecture-instagram-feed.json      then python3 build.py
Needs Pillow with AVIF support (as tools/encode_photos.py)."""
import base64, io, json, pathlib, sys
from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "instagram"
FEED = OUT / "feed.json"
RATIO = 4 / 5            # width / height of a tile
WIDTHS = (400, 800)


def main(snapshot: pathlib.Path):
    snap = json.loads(snapshot.read_text())
    old = {p["code"]: p for p in json.loads(FEED.read_text())["posts"]} if FEED.exists() else {}
    OUT.mkdir(parents=True, exist_ok=True)
    posts, missing, keep = [], [], {FEED.name}
    for it in snap["items"]:
        parts = [s for s in it["href"].split("/") if s]
        kind, code = ("reel" if "reel" in parts else "p"), parts[-1]
        im = Image.open(io.BytesIO(base64.b64decode(it["data"])))
        icc = im.info.get("icc_profile")
        im = im.convert("RGB")
        w, h = im.size
        if w / h > RATIO:                       # too wide: trim left and right
            cw = round(h * RATIO); box = ((w - cw) // 2, 0, (w - cw) // 2 + cw, h)
        else:                                   # too tall: trim top and bottom
            ch = round(w / RATIO); box = (0, (h - ch) // 2, w, (h - ch) // 2 + ch)
        im = im.crop(box)
        widths = sorted({min(x, im.width // 8 * 8) for x in WIDTHS})
        extra = {"icc_profile": icc} if icc else {}
        for x in widths:
            r = im.resize((x, round(x / RATIO)), Image.LANCZOS)
            r.save(OUT / f"{code}-{x}.jpg", quality=80, optimize=True, progressive=True, **extra)
            r.save(OUT / f"{code}-{x}.avif", quality=60, speed=4, **extra)
            keep |= {f"{code}-{x}.jpg", f"{code}-{x}.avif"}
        prev = old.get(code, {})
        entry = {"code": code, "kind": kind, "widths": widths, "w": widths[-1], "h": round(widths[-1] / RATIO),
                 "alt_de": prev.get("alt_de", ""), "alt_en": prev.get("alt_en", "")}
        if not (entry["alt_de"] and entry["alt_en"]):
            missing.append(f"{code} ({kind})")
        posts.append(entry)
        print(f"{it['i']:2d} {kind:4s} {code:12s} {w}x{h} -> {widths}")
    for f in OUT.iterdir():
        if f.name not in keep and f.suffix in (".jpg", ".avif"):
            f.unlink()
            print("removed", f.name)
    FEED.write_text(json.dumps({"profile": snap["profile"], "taken": snap["taken"][:10], "posts": posts},
                               indent=1, ensure_ascii=False) + "\n")
    if missing:
        sys.exit("alt texts missing in assets/instagram/feed.json (alt_de, alt_en): " + ", ".join(missing))


if __name__ == "__main__":
    main(pathlib.Path(sys.argv[1]))

#!/usr/bin/env python3
"""AVIF versions of the photos in assets/photos (05.11.2026): about a third smaller than the JPEGs at the same look
(PSNR about 38 dB). build.py offers them in a <picture>, the JPEG stays as fallback. WebP was tried and left out: only
10 % smaller for these photos. Needs Pillow with AVIF support (Pillow 11.3+). Run again after a photo changes."""
import pathlib
from PIL import Image

PHOTOS = pathlib.Path(__file__).resolve().parents[1] / "assets" / "photos"
for jpg in sorted(PHOTOS.glob("*.jpg")):
    im = Image.open(jpg)
    im = im.convert("RGB")
    icc = Image.open(jpg).info.get("icc_profile")
    extra = {"icc_profile": icc} if icc else {}
    im.save(jpg.with_suffix(".avif"), quality=62, speed=4, **extra)
    sizes = {s: jpg.with_suffix(s).stat().st_size // 1024 for s in (".jpg", ".avif")}
    print(jpg.name, " ".join(f"{k[1:]} {v} KB" for k, v in sizes.items()))

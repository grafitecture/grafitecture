"""Raster-Vorschau Paket 3: Profil mit 3:4-Kacheln, Beitrag 20 oben links."""
from PIL import Image, ImageDraw
import pathlib
from captions3 import PLAN
OUT = pathlib.Path("/home/claude/ig3/out")
TW, TH, G = 360, 480, 6
ids = [p[0] for p in PLAN][::-1]
rows = (len(ids) + 2) // 3
sheet = Image.new("RGB", (3 * TW + 2 * G, rows * TH + (rows - 1) * G), "white")
for i, pid in enumerate(ids):
    if pid.startswith("R"):
        im = Image.open(OUT / "covers" / f"{pid}_Titelbild.png").convert("RGB")
        w, h = im.size; ch = int(w * 4 / 3); im = im.crop((0, (h - ch) // 2, w, (h - ch) // 2 + ch))
    else:
        im = Image.open(sorted((OUT / pid).glob("*.png"))[0]).convert("RGB")
        w, h = im.size; cw = int(h * 3 / 4); im = im.crop(((w - cw) // 2, 0, (w - cw) // 2 + cw, h))
    im = im.resize((TW, TH), Image.LANCZOS)
    sheet.paste(im, ((i % 3) * (TW + G), (i // 3) * (TH + G)))
sheet.save(OUT / "Raster-Vorschau_Paket3.png")
print("ok", sheet.size)

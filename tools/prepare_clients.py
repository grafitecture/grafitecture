#!/usr/bin/env python3
"""Turns the client logos from Desktop/CLAUDE_GRAFITECTURE/KUNDENLOGOS (white on transparent, webp; a few in
colour on transparent, see SHADING) into one-colour #435960 PNGs on transparent, cropped to the logo, saved as
assets/clients/<slug>.png. The alpha channel is the logo shape, so only the colour changes; nothing is redrawn."""
import pathlib, sys
from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parents[1]
SRC = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "/mnt/user-data/uploads/Desktop/CLAUDE_GRAFITECTURE/KUNDENLOGOS")
OUT = ROOT / "assets" / "clients"
C = (0x43, 0x59, 0x60)

# source file -> slug used by build.py (slug of the client name)
MAP = {
    "gt_lannee_project.webp": "l-annee",
    "gt_dentaid_project.webp": "dentaid",
    "gt_healthklick_project.webp": "healthklick",
    "gt_flaesh_project.webp": "flash",
    "gt_ganz_project.webp": "kaufhaus-ganz",
    "gt_onkelottobar.webp": "onkel-otto-bar",
    "gt_42health.webp": "42health",
    "gt_tiniytecture.webp": "tinytecture",
    "gt_detmers.webp": "detmers",
    "gt_1898.webp": "1898",
    "core_cc.webp": "core",
    "raumrent.webp": "raumrent",
    "ultzracain.webp": "ultracain",
    "vitaphone.webp": "vitaphone",
    "steinbeis.webp": "steinbeis-finance",
    "gt_cs.webp": "creating-smiles",
    "gt_flaeshapp.webp": "flaeshapp",
    "gt_theurer.webp": "zahnarztpraxis-theurer",
    "gt_gg_1.webp": "gemeinschaftspraxis-gunther",
    "gt_tw.webp": "tanja-weber",
    "gt_covendos.webp": "covendos",
    "gt_zweiteliebe.webp": "zweite-liebe",
    "gt_ws.webp": "whitesmile",
    "gt_ag.webp": "ag",
    "gt_cci.webp": "cci-transport",
    "sanremo.webp": "sanremo",
    "starks.webp": "starks",
    "ecowerth.png": "ecowerth",          # colour logo (29.10.2026), see SHADING
    "covendos-healthcare-group.png": "covendos-healthcare-group",   # colour logo, red on transparent (30.10.2026)
}

# Colour sources: light grey that only shades, and the colours it touches. It is left out, because in one colour it
# would merge with its neighbours. ecowerth: the two light grey folds between the blue, green and red bar of the
# striped "E" would turn it into a zigzag; without them the three bars stay, as in the colour logo.
SHADING = {
    "ecowerth.png": ((217, 217, 217), [(23, 125, 193), (110, 165, 46), (172, 25, 32)]),
}


def drop_shading(im, grey, neighbours):
    """Alpha of a colour logo without its grey shading. Only next to the grey is a pixel split into neighbour
    colour and grey (the source blends them at the edges); every other edge keeps its anti-aliasing as it is."""
    import numpy as np
    from scipy import ndimage
    arr = np.asarray(im).astype(np.float64)
    rgb, a = arr[..., :3], arr[..., 3]
    g = np.array(grey, dtype=np.float64)
    core = (a >= 200) & (np.linalg.norm(rgb - g, axis=-1) < 28)
    near = ndimage.binary_dilation(core, structure=np.ones((3, 3), bool), iterations=2)
    share, err = np.ones(a.shape), np.full(a.shape, np.inf)      # share of grey per pixel, best-fitting neighbour
    for c in neighbours:
        c = np.array(c, dtype=np.float64)
        v = g - c
        t = np.clip(((rgb - c) * v).sum(-1) / (v @ v), 0, 1)
        e = np.linalg.norm(rgb - (c + t[..., None] * v), axis=-1)
        better = e < err
        share[better], err[better] = t[better], e[better]
    keep = np.where(share >= 0.75, 0.0, 1.0 - share)               # mostly grey: soft edge of the shading, drop
    return Image.fromarray(np.where(near, a * keep, a).round().astype(np.uint8), "L")


def full_strength(alpha):
    """Some sources draw parts at reduced opacity (e.g. a grey ".com"). In one colour that would read as a
    second shade, so every connected shape is scaled until its strongest pixel is fully opaque."""
    import numpy as np
    from scipy import ndimage
    arr = np.asarray(alpha).astype(np.float64)
    labels, n = ndimage.label(arr > 8)
    if n:
        peak = ndimage.maximum(arr, labels, index=np.arange(1, n + 1))
        gain = np.ones(n + 1)
        gain[1:] = np.where(peak > 0, 255.0 / peak, 1.0)
        arr = np.clip(arr * gain[labels], 0, 255)
    return Image.fromarray(arr.round().astype(np.uint8), "L")


OUT.mkdir(parents=True, exist_ok=True)
stats = {}
for src_name, slug in MAP.items():
    im = Image.open(SRC / src_name).convert("RGBA")
    a = drop_shading(im, *SHADING[src_name]) if src_name in SHADING else im.getchannel("A")
    a = a.point(lambda v: 0 if v < 6 else v)          # drop near-invisible fringe
    a = full_strength(a)
    box = a.getbbox()
    pad = 2
    box = (max(0, box[0] - pad), max(0, box[1] - pad), min(im.width, box[2] + pad), min(im.height, box[3] + pad))
    a = a.crop(box)
    out = Image.new("RGBA", a.size, C + (0,))
    out.putalpha(a)
    solid = Image.new("RGBA", a.size, C + (255,))
    solid.putalpha(a)
    # palette PNG: one colour, 256 alpha steps -> small files
    q = solid.quantize(colors=256, method=Image.Quantize.FASTOCTREE)
    dest = OUT / f"{slug}.png"
    q.save(dest, optimize=True)
    import numpy as np
    stats[slug] = (a.size[0], a.size[1], float(np.asarray(a, dtype=np.float64).mean()) / 255)
    print(f"{src_name:30s} -> {dest.name:34s} {a.size[0]}x{a.size[1]}  {dest.stat().st_size} B")

# Display sizes with equal visual weight: same area for every logo, nudged up for light, thin marks and down for
# heavy, solid ones (damped), then capped. build.py reads sizes.json for the img width/height.
import json, math, statistics
d_ref = statistics.median(d for _, _, d in stats.values())
sizes = {}
for slug, (w, h, d) in stats.items():
    r = w / h
    f = min(1.3, max(0.8, (d_ref / d) ** 0.35))
    area = 132 * 48 * f
    dh = math.sqrt(area / r)
    dw = r * dh
    k = min(1, 220 / dw, 70 / dh)
    sizes[slug] = [round(dw * k), round(dh * k)]
(OUT / "sizes.json").write_text(json.dumps(sizes, indent=1, sort_keys=True) + "\n")
print("sizes.json:", json.dumps(sizes, sort_keys=True))

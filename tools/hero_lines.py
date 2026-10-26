#!/usr/bin/env python3
"""Hero animation (26.10.2026): turns the line drawings into 1-px centre lines.

Source: one line drawing per stage of the history of technology, made with Nano Banana Pro on Higgsfield AI
(thin black outlines on white), stored as 1-bit PNGs (2400 x 1792) in assets/hero/drawings. This script finds the
centre line of every drawn line (skeleton), joins the pieces into long strokes (straight through crossings),
smooths and simplifies them and writes assets/hero/lines.json: per scene a list of SVG path strings
("M x y l dx dy ..."), fitted into a 1000 x 800 box, longest stroke first.

    python3 tools/hero_lines.py          (needs numpy, scipy, scikit-image, Pillow)
"""
import json
import math
import pathlib

import numpy as np
from PIL import Image
from scipy import ndimage as ndi
from skimage.morphology import remove_small_objects, skeletonize

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "assets" / "hero" / "drawings"
OUT = ROOT / "assets" / "hero" / "lines.json"
W, H, PAD = 1000, 800, 16

# order of the animation: file, mirrored (so that people, vehicles and machines face or move to the right), name
SCENES = [
    ("s01", True, "feuer"), ("s02", False, "rad"), ("s03", False, "buchdruck"),
    ("s04", False, "entdecker"), ("s05", False, "dampfmaschine"), ("s06", True, "eisenbahn"),
    ("s07", False, "gluehbirne"), ("s08", True, "flugzeug"), ("s09", False, "rakete"),
    ("s10", False, "internet"), ("s11", False, "ki"), ("s12", False, "flugauto"),
]

SPUR = 9          # px (source): skeleton twigs at line ends and corners shorter than this are dropped
MIN_LEN = 10      # px (source): strokes shorter than this are dropped (specks)
SIGMA = 1.3       # px (source): smoothing of the pixel staircase along each stroke
EPS = 0.7         # px (source): simplification tolerance (Ramer-Douglas-Peucker)
STRAIGHT = math.cos(math.radians(140))   # two lines meeting at a crossing are joined when they continue

RING = [(-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1)]   # clockwise from NW
EDGE4 = {1, 3, 5, 7}                                                                # N, E, S, W in RING


def simple(sk, y, x):
    """True if (y, x) can be removed without changing the topology and is not an end point."""
    on = [sk[y + dy, x + dx] for dy, dx in RING]
    if sum(on) < 2:
        return False
    # foreground: one 8-connected group among the neighbours?
    idx = [i for i in range(8) if on[i]]
    parent = {i: i for i in idx}

    def find(i):
        while parent[i] != i:
            i = parent[i]
        return i
    for a in idx:
        for b in idx:
            if a < b and max(abs(RING[a][0] - RING[b][0]), abs(RING[a][1] - RING[b][1])) == 1:
                parent[find(a)] = find(b)
    if len({find(i) for i in idx}) != 1:
        return False
    # background: one 4-connected run (in ring order) touching a 4-neighbour of the pixel?
    runs, cur, first = [], [], None
    for i in range(8):
        if not on[i]:
            cur.append(i)
        elif cur:
            runs.append(cur)
            cur = []
    if cur:
        if runs and runs[0][0] == 0 and not on[7] and not on[0]:
            runs[0] = cur + runs[0]
        else:
            runs.append(cur)
    touching = [r for r in runs if any(i in EDGE4 for i in r)]
    return len(touching) == 1


def thin(sk):
    """Make the skeleton minimal in 8-connectivity (no staircase corners that look like crossings)."""
    sk = np.pad(sk, 1)
    changed = True
    while changed:
        changed = False
        for y, x in zip(*np.nonzero(sk)):
            if simple(sk, y, x):
                sk[y, x] = False
                changed = True
    return sk


def graph(sk):
    """Nodes (end points and crossings) and the pixel chains between them."""
    count = ndi.convolve(sk.astype(np.uint8), np.array([[1, 1, 1], [1, 0, 1], [1, 1, 1]]), mode="constant") * sk
    nodepx = sk & (count != 2)
    lab, n = ndi.label(nodepx, structure=np.ones((3, 3)))
    centers = ndi.center_of_mass(nodepx, lab, range(1, n + 1))
    centers = [np.array(c) for c in centers]
    edges = []                       # [points (list of (y, x)), node a or None, node b or None]
    seen = np.zeros_like(sk)
    done = set()
    for y, x in zip(*np.nonzero(nodepx)):
        a = lab[y, x] - 1
        for dy, dx in RING:
            qy, qx = y + dy, x + dx
            if not sk[qy, qx]:
                continue
            if nodepx[qy, qx]:
                b = lab[qy, qx] - 1
                if b != a and (min(a, b), max(a, b)) not in done:
                    done.add((min(a, b), max(a, b)))
                    edges.append([[(y, x), (qy, qx)], a, b])
                continue
            if seen[qy, qx]:
                continue
            pts = [(y, x), (qy, qx)]
            prev, cur = (y, x), (qy, qx)
            seen[qy, qx] = True
            while True:
                nxt = None
                for ey, ex in RING:
                    ry, rx = cur[0] + ey, cur[1] + ex
                    if sk[ry, rx] and (ry, rx) != prev and not (seen[ry, rx] and not nodepx[ry, rx]):
                        nxt = (ry, rx)
                        if nodepx[ry, rx]:
                            break
                if nxt is None:
                    break
                pts.append(nxt)
                if nodepx[nxt]:
                    break
                seen[nxt] = True
                prev, cur = cur, nxt
            b = lab[pts[-1]] - 1 if nodepx[pts[-1]] else None
            edges.append([pts, a, b])
    # closed loops without any node
    for y, x in zip(*np.nonzero(sk & ~nodepx & ~seen)):
        if seen[y, x]:
            continue
        pts, prev, cur = [(y, x)], None, (y, x)
        seen[y, x] = True
        while True:
            nxt = None
            for ey, ex in RING:
                ry, rx = cur[0] + ey, cur[1] + ex
                if sk[ry, rx] and (ry, rx) != prev and not seen[ry, rx]:
                    nxt = (ry, rx)
                    break
            if nxt is None:
                break
            pts.append(nxt)
            seen[nxt] = True
            prev, cur = cur, nxt
        pts.append(pts[0])
        edges.append([pts, None, None])
    return centers, edges


def length(p):
    return float(np.sum(np.hypot(*np.diff(p, axis=0).T))) if len(p) > 1 else 0.0


def strokes_of(sk):
    centers, edges = graph(sk)
    edges = [[np.array(p, dtype=float), a, b] for p, a, b in edges]
    # drop short twigs that end freely (skeleton artefacts at corners and line ends), twice
    for _ in range(2):
        deg = {}
        for p, a, b in edges:
            for v in (a, b):
                if v is not None:
                    deg[v] = deg.get(v, 0) + 1
        keep = []
        for e in edges:
            p, a, b = e
            free = (a is None or deg.get(a, 0) == 1) != (b is None or deg.get(b, 0) == 1)
            crossing = (a is not None and deg.get(a, 0) >= 3) or (b is not None and deg.get(b, 0) >= 3)
            if free and crossing and length(p) < SPUR:
                continue
            keep.append(e)
        edges = keep
    # end points of each chain sit on the centre of their crossing
    for e in edges:
        p, a, b = e
        if a is not None:
            p[0] = centers[a]
        if b is not None:
            p[-1] = centers[b]
    # at every crossing, join the two chains that continue most straight, then the next pair, ...
    ends = {}
    for i, (p, a, b) in enumerate(edges):
        if a is not None:
            ends.setdefault(a, []).append((i, 0))
        if b is not None:
            ends.setdefault(b, []).append((i, 1))
    link = {}
    for v, lst in ends.items():
        dirs = {}
        for i, end in lst:
            p = edges[i][0] if end == 0 else edges[i][0][::-1]
            d = np.cumsum(np.r_[0, np.hypot(*np.diff(p, axis=0).T)])
            k = min(int(np.searchsorted(d, 14)), len(p) - 1)
            vec = p[k] - p[0]
            nrm = np.hypot(*vec)
            dirs[(i, end)] = vec / nrm if nrm > 0 else np.array([0.0, 0.0])
        free = list(lst)
        if len(free) == 2 and free[0][0] != free[1][0]:
            link[free[0]] = free[1]
            link[free[1]] = free[0]
            continue
        pairs = sorted(((float(dirs[s] @ dirs[t]), s, t) for ai, s in enumerate(free) for t in free[ai + 1:]
                        if s[0] != t[0]), key=lambda z: z[0])
        used = set()
        for dot, s, t in pairs:
            if dot > STRAIGHT:
                break
            if s in used or t in used:
                continue
            link[s] = t
            link[t] = s
            used.update((s, t))
    # walk the chains into strokes
    out, used = [], set()

    def walk(i, end):
        pts = []
        while True:
            used.add(i)
            p = edges[i][0] if end == 0 else edges[i][0][::-1]
            pts.append(p if not pts else p[1:])
            nxt = link.get((i, 1 - end))
            if nxt is None or nxt[0] in used:
                break
            i, end = nxt
        return np.concatenate(pts)
    for i in range(len(edges)):
        for end in (0, 1):
            if i not in used and (i, end) not in link:
                out.append(walk(i, end))
    for i in range(len(edges)):
        if i not in used:
            out.append(walk(i, 0))
    return out


def smooth(p):
    closed = len(p) > 3 and np.hypot(*(p[0] - p[-1])) < 1.5
    if len(p) < 5:
        return p
    if closed:
        q = ndi.gaussian_filter1d(p[:-1], SIGMA, axis=0, mode="wrap")
        return np.vstack([q, q[:1]])
    q = ndi.gaussian_filter1d(p, SIGMA, axis=0, mode="nearest")
    q[0], q[-1] = p[0], p[-1]
    return q


def rdp(p, eps):
    if len(p) < 3:
        return p
    keep = np.zeros(len(p), bool)
    keep[0] = keep[-1] = True
    stack = [(0, len(p) - 1)]
    while stack:
        i, j = stack.pop()
        a, b = p[i], p[j]
        ab = b - a
        nab = np.hypot(*ab)
        seg = p[i + 1:j]
        if not len(seg):
            continue
        if nab == 0:
            d = np.hypot(*(seg - a).T)
        else:
            d = np.abs(ab[0] * (seg[:, 1] - a[1]) - ab[1] * (seg[:, 0] - a[0])) / nab
        k = int(np.argmax(d))
        if d[k] > eps:
            keep[i + 1 + k] = True
            stack += [(i, i + 1 + k), (i + 1 + k, j)]
    return p[keep]


def num(v):
    s = f"{v:.1f}".rstrip("0").rstrip(".")
    if s in ("-0", ""):
        s = "0"
    if s.startswith("0."):
        s = s[1:]
    elif s.startswith("-0."):
        s = "-" + s[2:]
    return s


def path(p):
    """'M x y l dx dy dx dy ...' with one decimal, the minus sign doubling as separator"""
    q = np.round(p * 10) / 10
    parts = ["M" + num(q[0][0]) + " " + num(q[0][1]) + "l"]
    prev = q[0]
    body = ""
    for pt in q[1:]:
        d = pt - prev
        prev = pt
        for v in d:
            t = num(v)
            body += t if (not body or t.startswith("-")) else " " + t
    return parts[0] + body


def scene(name, mirror):
    im = np.array(Image.open(SRC / f"{name}.png").convert("L")) < 128
    if mirror:
        im = im[:, ::-1]
    im = remove_small_objects(im, max_size=23)
    sk = thin(skeletonize(im))
    raw = [s[:, ::-1] - 1 for s in strokes_of(sk)]          # (x, y), undo the padding
    raw = [s for s in raw if length(s) >= MIN_LEN]
    pts = np.vstack(raw)
    lo, hi = pts.min(0), pts.max(0)
    k = min((W - 2 * PAD) / (hi[0] - lo[0]), (H - 2 * PAD) / (hi[1] - lo[1]))
    off = np.array([W, H]) / 2 - (lo + hi) / 2 * k
    res = []
    for s in raw:
        q = rdp(smooth(s), EPS) * k + off
        res.append((length(q), path(q)))
    res.sort(key=lambda z: -z[0])
    return [d for _, d in res], sum(z[0] for z in res), k


def main():
    data = {"w": W, "h": H, "scenes": []}
    for name, mirror, label in SCENES:
        strokes, total, k = scene(name, mirror)
        data["scenes"].append({"id": label, "d": strokes})
        print(f"{label:14s} {len(strokes):4d} strokes, length {total:7.0f}, scale {k:.3f}, "
              f"{sum(len(d) for d in strokes) / 1024:6.1f} KB")
    OUT.write_text(json.dumps(data, separators=(",", ":")))
    print(OUT, f"{OUT.stat().st_size / 1024:.1f} KB")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Hero film: turns the generated clip into the very light, seamless loop in assets/hero (25.10.2026).

Source: keyframe made with GPT Image 2.5 (hand resting on white paper, fine grey lines flowing around the fingertip),
animated with MiniMax H3 on Higgsfield AI, start and end frame = the keyframe, 10 s, 2560x1440, 24 fps.

  python3 tools/hero_film.py SOURCE.mp4 assets/hero          (needs ffmpeg, numpy, scipy, Pillow)

Steps
  1. paper level: smooth illumination of the empty paper (hand masked out), so the paper becomes pure white everywhere
  2. grade: darkness relative to the paper; paper grain below FLOOR disappears, deep shadows are compressed (soft
     knee), so everything stays very light grey
  3. loop: the last XF frames are cross-faded into the first XF frames, which are then dropped from the start
     -> the last frame flows straight into the first one
  4. the paper is written as "superwhite" luma (~241 instead of 235), so compression noise still decodes to #FFFFFF
  5. encodes: hero-film.mp4 (1920x1080 H.264, one keyframe, steady quality up to the loop point), hero-film.webm
     (1280x720 VP9 fallback), hero-poster.jpg (first frame, greyscale)
"""
import pathlib, subprocess, sys
import numpy as np
from PIL import Image
from scipy.ndimage import (binary_dilation, binary_fill_holes, binary_opening, gaussian_filter, label,
                           percentile_filter, zoom)

W, H, FPS = 1920, 1080, 24
FLOOR, KNEE, GAIN, DEPTH, XF = 5.5, 2.0, 1.8, 62.0, 36
X264_FINAL = ("keyint={n}:min-keyint={n}:scenecut=0:ipratio=1.1:pbratio=1.1:"
              "zones={a},{b},b=1.15/{c},{d},b=1.35/{e},{f},b=1.6/{g},{h},b=1.9")
TAGS = ["-color_range", "tv", "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709"]


def frames(src, select=None):
    """luminance frames (float32, 0..255) at W x H"""
    vf = f"scale={W}:{H}:flags=lanczos,format=rgb24"
    if select is not None:
        vf = "select='" + "+".join(f"eq(n\\,{i})" for i in select) + "'," + vf
    p = subprocess.Popen(["ffmpeg", "-v", "error", "-i", str(src), "-vf", vf, "-vsync", "0", "-f", "rawvideo", "-"],
                         stdout=subprocess.PIPE)
    size = W * H * 3
    while True:
        b = p.stdout.read(size)
        if len(b) < size:
            break
        yield np.frombuffer(b, np.uint8).reshape(H, W, 3).astype(np.float32) @ np.float32([0.2126, 0.7152, 0.0722])
    p.wait()


def frame_count(src):
    out = subprocess.run(["ffprobe", "-v", "error", "-count_frames", "-select_streams", "v:0", "-show_entries",
                          "stream=nb_read_frames", "-of", "csv=p=0", str(src)], capture_output=True, text=True)
    return int(out.stdout.strip())


def paper_level(src, n):
    """smooth level of the bare paper; inside the hand it follows a polynomial fit, offset to the hand border"""
    med = np.median(np.stack(list(frames(src, select=np.linspace(0, n - 1, 5).astype(int)))), axis=0)
    s = 4
    sm = med.reshape(H // s, s, W // s, s).mean(axis=(1, 3))
    # polynomial (degree 3) through the bright paper, as fallback where no paper is near
    yy, xx = np.mgrid[0:sm.shape[0], 0:sm.shape[1]]
    x, y = xx / sm.shape[1] * 2 - 1, yy / sm.shape[0] * 2 - 1
    terms = [np.ones_like(x), x, y, x * x, x * y, y * y, x ** 3, x * x * y, x * y * y, y ** 3]
    bright = sm > np.percentile(sm, 30)
    coef, *_ = np.linalg.lstsq(np.stack([t[bright] for t in terms], 1), sm[bright], rcond=None)
    poly = sum(c * t for c, t in zip(coef, terms))
    # the hand: the largest dark connected region, filled and widened
    lab, _ = label(binary_opening(sm < 222, iterations=3))
    sizes = np.bincount(lab.ravel()); sizes[0] = 0
    hand = binary_fill_holes(binary_dilation(lab == sizes.argmax(), iterations=10))
    # paper samples: not the hand, not the lines (darker than the local 80th percentile)
    paper = ~hand & (sm > percentile_filter(sm, 80, size=9) - 3)
    num, den = gaussian_filter(np.where(paper, sm, 0), 10), gaussian_filter(paper.astype(float), 10)
    est = np.where(den > .05, num / np.maximum(den, 1e-6), np.nan)
    border = binary_dilation(hand, iterations=3) & ~hand & ~np.isnan(est)
    fill = poly + (np.nanmedian(est[border] - poly[border]) if border.any() else 0)
    w = np.clip((den - .05) / .25, 0, 1)
    level = gaussian_filter(w * np.nan_to_num(est) + (1 - w) * fill, 3)
    return zoom(level, (s, s), order=1)[:H, :W].astype(np.float32)


def grade(g, level):
    d = np.clip(255.0 * (1.0 - g / level), 0, 255)
    x = d - FLOOR
    d = np.where(x > KNEE, x, np.where(x < -KNEE, 0.0, (x + KNEE) ** 2 / (4 * KNEE)))
    return np.clip(255.0 - DEPTH * (1.0 - np.exp(-GAIN * d / DEPTH)), 0, 255)


def smooth(t):
    return t * t * (3 - 2 * t)


def luma(v):
    """full-range grey -> limited-range Y, paper lifted to superwhite"""
    y = 16.0 + 219.0 * v / 255.0 + 6.0 * smooth(np.clip((v - 247.0) / 8.0, 0, 1))
    return np.clip(np.rint(y), 0, 255).astype(np.uint8)


def main(src, out):
    src, out = pathlib.Path(src), pathlib.Path(out)
    out.mkdir(parents=True, exist_ok=True)
    n = frame_count(src)
    level = paper_level(src, n)
    master = out / "_master.mp4"
    enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "yuv420p", "-s", f"{W}x{H}",
                            "-r", str(FPS), "-color_range", "tv", "-i", "-", "-c:v", "libx264", "-preset", "veryfast",
                            "-crf", "4", "-pix_fmt", "yuv420p", *TAGS, str(master)], stdin=subprocess.PIPE)
    uv = np.full((H // 2) * (W // 2) * 2, 128, np.uint8).tobytes()
    head = []
    for i, g in enumerate(frames(src)):
        o = grade(g, level)
        if i < XF:
            head.append(o); continue
        if i >= n - XF:
            j = i - (n - XF)
            a = smooth((j + .5) / XF)
            o = (1 - a) * o + a * head[j]
        enc.stdin.write(luma(o).tobytes() + uv)
    enc.stdin.close(); enc.wait()
    m = n - XF                                    # frames in the loop
    zones = X264_FINAL.format(n=m, a=m - 57, b=m - 38, c=m - 37, d=m - 23, e=m - 22, f=m - 11, g=m - 10, h=m - 1)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(master), "-c:v", "libx264", "-preset", "slow",
                    "-profile:v", "high", "-level", "4.0", "-crf", "27", "-x264-params", zones, "-an",
                    "-pix_fmt", "yuv420p", *TAGS, "-movflags", "+faststart", str(out / "hero-film.mp4")], check=True)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(master), "-vf", "scale=1280:720:flags=lanczos",
                    "-c:v", "libvpx-vp9", "-b:v", "0", "-crf", "35", "-deadline", "good", "-cpu-used", "2",
                    "-row-mt", "1", "-g", str(m), "-keyint_min", str(m), "-an", "-pix_fmt", "yuv420p",
                    "-color_range", "tv", "-colorspace", "bt709", str(out / "hero-film.webm")], check=True)
    poster = out / "_poster.png"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(out / "hero-film.mp4"), "-frames:v", "1",
                    "-vf", "format=rgb24", str(poster)], check=True)
    Image.open(poster).convert("L").save(out / "hero-poster.jpg", quality=80, optimize=True, progressive=True)
    master.unlink(); poster.unlink()
    for f in ("hero-film.mp4", "hero-film.webm", "hero-poster.jpg"):
        print(f, (out / f).stat().st_size, "bytes")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2])

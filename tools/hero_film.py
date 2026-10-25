#!/usr/bin/env python3
"""Hero film: turns the generated clip into the seamless loop in assets/hero (25.10.2026, second version).

Source: keyframe made with GPT Image 2.5 on Higgsfield AI (a free collage on white: thin lines and arrows, binary
digits, numbers, terminal commands, typeface names, AI icons, Pantone colour chips), animated with MiniMax H3,
start and end frame = the keyframe, 10 s, 2560x1440, 24 fps.

  python3 tools/hero_film.py SOURCE.mp4 assets/hero          (needs ffmpeg, numpy, Pillow)

Steps
  1. white: per frame the level of the bare white background is measured and scaled to pure white; tiny
     deviations below FLOOR (compression noise, faint haze) disappear; colours stay as they are
  2. loop: the last XF frames are cross-faded into the first XF frames, which are then dropped from the start
     -> the last frame flows straight into the first one
  3. encode: RGB -> BT.709 YUV; near-white luma is lifted to "superwhite" (~241 instead of 235), so compression
     noise still decodes to #FFFFFF. hero-film.mp4 (1920x1080 H.264, one keyframe, steady quality up to the loop
     point), hero-film.webm (1280x720 VP9 fallback), hero-poster.jpg (first frame)
"""
import pathlib, subprocess, sys
import numpy as np
from PIL import Image

W, H, FPS = 1920, 1080, 24
FLOOR, KNEE, XF = 4.0, 2.0, 36
TAGS = ["-color_range", "tv", "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709"]
TO_YUV = ("scale=out_color_matrix=bt709:out_range=tv,format=yuv420p,"
          "lutyuv=y='val+6*pow(clip((val-228)/7,0,1),2)*(3-2*clip((val-228)/7,0,1))'")
X264_FINAL = ("keyint={n}:min-keyint={n}:scenecut=0:ipratio=1.1:pbratio=1.1:"
              "zones={a},{b},b=1.15/{c},{d},b=1.35/{e},{f},b=1.6/{g},{h},b=1.9")


def frames(src):
    """RGB frames (float32, 0..255) at W x H"""
    p = subprocess.Popen(["ffmpeg", "-v", "error", "-i", str(src), "-vf", f"scale={W}:{H}:flags=lanczos,format=rgb24",
                          "-f", "rawvideo", "-"], stdout=subprocess.PIPE)
    size = W * H * 3
    while True:
        b = p.stdout.read(size)
        if len(b) < size:
            break
        yield np.frombuffer(b, np.uint8).reshape(H, W, 3).astype(np.float32)
    p.wait()


def frame_count(src):
    out = subprocess.run(["ffprobe", "-v", "error", "-count_frames", "-select_streams", "v:0", "-show_entries",
                          "stream=nb_read_frames", "-of", "csv=p=0", str(src)], capture_output=True, text=True)
    return int(out.stdout.strip())


def whiten(f):
    """scale the bare background to 255, then clean everything closer than FLOOR to white (soft knee)"""
    luma = f @ np.float32([0.2126, 0.7152, 0.0722])
    level = np.percentile(luma[::8, ::8], 75)          # most of the frame is bare background
    d = np.clip(255.0 - f * (255.0 / level), 0, 255)   # per channel distance from white
    x = d - FLOOR
    d = np.where(x > KNEE, x, np.where(x < -KNEE, 0.0, (x + KNEE) ** 2 / (4 * KNEE)))
    return 255.0 - d


def smooth(t):
    return t * t * (3 - 2 * t)


def main(src, out):
    src, out = pathlib.Path(src), pathlib.Path(out)
    out.mkdir(parents=True, exist_ok=True)
    n = frame_count(src)
    master = out / "_master.mp4"
    enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                            "-r", str(FPS), "-i", "-", "-vf", TO_YUV, "-c:v", "libx264", "-preset", "veryfast",
                            "-crf", "4", *TAGS, str(master)], stdin=subprocess.PIPE)
    head = []
    for i, f in enumerate(frames(src)):
        o = whiten(f)
        if i < XF:
            head.append(o); continue
        if i >= n - XF:
            j = i - (n - XF)
            a = smooth((j + .5) / XF)
            o = (1 - a) * o + a * head[j]
        enc.stdin.write(np.clip(np.rint(o), 0, 255).astype(np.uint8).tobytes())
    enc.stdin.close(); enc.wait()
    m = n - XF                                         # frames in the loop
    zones = X264_FINAL.format(n=m, a=m - 57, b=m - 38, c=m - 37, d=m - 23, e=m - 22, f=m - 11, g=m - 10, h=m - 1)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(master), "-c:v", "libx264", "-preset", "slow",
                    "-profile:v", "high", "-level", "4.0", "-crf", "26", "-x264-params", zones, "-an",
                    "-pix_fmt", "yuv420p", *TAGS, "-movflags", "+faststart", str(out / "hero-film.mp4")], check=True)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(master), "-vf", "scale=1280:720:flags=lanczos",
                    "-c:v", "libvpx-vp9", "-b:v", "0", "-crf", "34", "-deadline", "good", "-cpu-used", "2",
                    "-row-mt", "1", "-g", str(m), "-keyint_min", str(m), "-an", "-pix_fmt", "yuv420p",
                    *TAGS, str(out / "hero-film.webm")], check=True)
    poster = out / "_poster.png"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(out / "hero-film.mp4"), "-frames:v", "1",
                    "-vf", "format=rgb24", str(poster)], check=True)
    Image.open(poster).convert("RGB").save(out / "hero-poster.jpg", quality=82, optimize=True, progressive=True)
    master.unlink(); poster.unlink()
    for f in ("hero-film.mp4", "hero-film.webm", "hero-poster.jpg"):
        print(f, (out / f).stat().st_size, "bytes")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2])

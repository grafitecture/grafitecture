"""Three Instagram reels (1080x1920, 30 fps) in the Grafitecture CI.
Scenes are HTML pages animated by setT(t); video scenes get a transparent overlay composited onto the clip."""
import asyncio, pathlib, subprocess, sys, shutil, math
import numpy as np
from PIL import Image
from playwright.async_api import async_playwright
from engine import CSS, SHEEN_JS, LOGO, ARROW, REPO, img

FPS = 30
W, H = 1080, 1920
NB = " "
VID = pathlib.Path("/home/claude/ig/vid")
WORK = pathlib.Path("/home/claude/ig/reelwork")
OUT = pathlib.Path("/home/claude/ig/out/reels")

REEL_CSS = """
html, body { background: transparent; }
.stage { width: 1080px; height: 1920px; position: relative; overflow: hidden; }
.stage.clear { background: transparent; }
.a { position: absolute; left: 96px; right: 96px; will-change: opacity, transform; }
.big { font-size: 236px; line-height: .9; letter-spacing: -.048em; }
.mid { font-size: 150px; line-height: .94; letter-spacing: -.04em; }
.med { font-size: 104px; line-height: 1.02; letter-spacing: -.03em; }
.sm { font-size: 58px; line-height: 1.18; letter-spacing: -.014em; }
.kk { font-size: 30px; line-height: 1.4; letter-spacing: .16em; text-transform: uppercase; font-weight: 500; }
.wht { color: #fff; }
.ln { height: 4px; background: var(--line); transform-origin: left center; }
.row { display: grid; grid-template-columns: 210px 1fr; align-items: baseline; padding: 26px 0 30px; }
.row .n { font-size: 62px; letter-spacing: -.02em; }
.row .t { font-size: 56px; line-height: 1.18; letter-spacing: -.012em; }
.lg svg { height: 52px; width: auto; display: block; }
"""

ANIM_JS = """
const clamp = (v) => Math.max(0, Math.min(1, v));
const ease = (p) => 1 - Math.pow(1 - p, 3);
window.setT = (t) => {
  document.querySelectorAll('[data-in]').forEach((el) => {
    const a = parseFloat(el.dataset.in), d = parseFloat(el.dataset.d || '0.45');
    const p = ease(clamp((t - a) / d));
    const o = el.dataset.out ? ease(clamp((t - parseFloat(el.dataset.out)) / 0.3)) : 0;
    el.style.opacity = (p * (1 - o)).toFixed(3);
    const dy = parseFloat(el.dataset.dy || '40');
    el.style.transform = `translateY(${((1 - p) * dy - o * 20).toFixed(2)}px)`;
  });
  document.querySelectorAll('[data-line]').forEach((el) => {
    const p = ease(clamp((t - parseFloat(el.dataset.line)) / 0.7));
    el.style.transform = `scaleX(${p.toFixed(4)})`;
  });
  document.querySelectorAll('[data-draw]').forEach((el) => {
    const len = el.getTotalLength();
    const p = ease(clamp((t - parseFloat(el.dataset.draw)) / parseFloat(el.dataset.dd || '1')));
    el.style.strokeDasharray = len; el.style.strokeDashoffset = (len * (1 - p)).toFixed(2);
  });
  document.querySelectorAll('canvas.sheen').forEach((cv) => {
    window.paintSheen(cv, parseFloat(cv.dataset.clock || '0') + t * parseFloat(cv.dataset.rate || '6'), 4, { noFade: true });
  });
};
"""


def page(inner, clear=False, bg="white"):
    return f"""<!doctype html><html lang="de"><head><meta charset="utf-8"><style>{CSS}{REEL_CSS}</style></head>
<body><section class="stage {'clear' if clear else bg}">{inner}</section>
<script>{SHEEN_JS}{ANIM_JS}document.fonts.ready.then(() => {{ window.setT(0); window.READY = true; }});</script></body></html>"""


def sheen(clock=0, rate=6):
    return f'<canvas class="sheen" data-clock="{clock}" data-rate="{rate}"></canvas>'


def end_card():
    """Shared sign-off for all three reels: the shimmering field, logo, claim, address."""
    return dict(dur=2.6, bg="shim", html=f"""{sheen(20, 10)}
<div class="a lg" style="top:300px" data-in="0.05">{LOGO}</div>
<div class="a big" style="top:720px" data-in="0.2">Marken<br>mit KI.</div>
<div class="a sm" style="top:1270px" data-in="0.55">grafitecture.de</div>
""")


# ------------------------------------------------------------------ scenes
R1 = [
    dict(dur=4.6, video="v21_use.mp4", html=f"""
<div class="a mid" style="top:250px;font-size:132px" data-in="0.5">Erst Papier.</div>
"""),
    dict(dur=3.2, bg="white", html=f"""
<svg style="position:absolute;left:96px;top:300px" width="888" height="760" viewBox="0 0 888 760" fill="none" stroke="#dafd55" stroke-width="5">
  <path data-draw="0.0" data-dd="0.9" d="M2 2H886V758H2Z"/>
  <path data-draw="0.35" data-dd="0.6" d="M2 96H886"/>
  <path data-draw="0.5" data-dd="0.5" d="M44 50H200"/>
  <path data-draw="0.6" data-dd="0.5" d="M560 50H840"/>
  <path data-draw="0.75" data-dd="0.7" d="M44 190H640M44 260H520"/>
  <path data-draw="0.95" data-dd="0.7" d="M44 380H290V700H44ZM320 380H566V700H320ZM596 380H842V700H596Z"/>
</svg>
<div class="a mid" style="top:1160px" data-in="0.55">Dann Web.</div>
"""),
    dict(dur=3.2, bg="shim", html=f"""{sheen(0, 14)}
<div class="a big" style="top:640px" data-in="0.15">Heute<br>KI.</div>
"""),
    dict(dur=2.6, bg="white", html=f"""
<div class="a med" style="top:600px" data-in="0.1">Das Werkzeug<br>wechselt.</div>
<div class="a med" style="top:960px" data-in="0.9">Die Gestaltung<br>bleibt.</div>
"""),
    end_card(),
]

R2 = [
    dict(dur=5.0, video="v22_use.mp4", html=f"""
<div class="a med wht" style="top:270px;font-size:94px" data-in="0.4">KI recherchiert.</div>
<div class="a med wht" style="top:386px;font-size:94px" data-in="1.5">KI entwirft.</div>
<div class="a med wht" style="top:502px;font-size:94px" data-in="2.6">KI automatisiert.</div>
"""),
    dict(dur=2.6, bg="white", html=f"""
<div class="a big" style="top:720px;font-size:172px" data-in="0.1">Ich<br>entscheide.</div>
"""),
    dict(dur=3.2, bg="lime", html=f"""
<div class="a kk" style="top:420px" data-in="0.1">Haltung</div>
<div class="a big" style="top:640px;font-size:158px" data-in="0.2">Human<br>in the loop.</div>
<div class="a sm" style="top:1060px" data-in="0.8">Die KI macht die Routine.<br>Die Entscheidung bleibt beim Menschen.</div>
"""),
    end_card(),
]

R3 = [
    dict(dur=3.4, video="v23_still.mp4", html=f"""
<div class="a big wht" style="top:300px" data-in="0.3">02:14</div>
<div class="a sm wht" style="top:540px" data-in="0.8">Neue Anfrage über die Website.</div>
"""),
    dict(dur=5.0, bg="white", html=f"""
<div class="a kk" style="top:380px" data-in="0.05">Ihr KI-Agent, heute Nacht</div>
<div class="a" style="top:470px">
  <div class="ln" data-line="0.2"></div>
  <div class="row" data-in="0.4"><span class="n">02:14</span><span class="t">prüft die Anfrage</span></div>
  <div class="ln" data-line="0.5"></div>
  <div class="row" data-in="1.3"><span class="n">02:15</span><span class="t">Budget und Zeitrahmen passen</span></div>
  <div class="ln" data-line="1.4"></div>
  <div class="row" data-in="2.2"><span class="n">02:16</span><span class="t">drei Termine vorgeschlagen</span></div>
  <div class="ln" data-line="2.3"></div>
  <div class="row" data-in="3.1"><span class="n">02:17</span><span class="t">Angebot vorbereitet</span></div>
  <div class="ln" data-line="3.2"></div>
</div>
"""),
    dict(dur=3.0, bg="lime", html=f"""
<div class="a big" style="top:560px" data-in="0.1">07:30</div>
<div class="a med" style="top:860px" data-in="0.6">Sie lesen die Zusammen&shy;fassung.</div>
"""),
    dict(dur=2.6, bg="white", html=f"""
<div class="a med" style="top:600px" data-in="0.1">Ein Agent.<br>Ein klarer Job.</div>
<div class="a med" style="top:960px" data-in="0.9">Ein Mensch<br>gibt frei.</div>
"""),
    end_card(),
]

REELS = {"R1": R1, "R2": R2, "R3": R3}


# ------------------------------------------------------------------ the night still for R3 (logo-free, from the Higgsfield image)
def make_night_still(dur=3.4):
    src = Image.open("/home/claude/ig/hf/src/gt_hf_img3.png").convert("RGB")
    a = np.asarray(src).astype(np.float32) / 255
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    lime = np.clip((g - b - 0.08) * 4, 0, 1) * np.clip((g - 0.15) * 3, 0, 1)   # where the screen light falls
    d = WORK / "night"
    d.mkdir(parents=True, exist_ok=True)
    n = int(dur * FPS)
    sw, sh = src.size
    for i in range(n):
        t = i / FPS
        pulse = 1 + 0.11 * max(0, math.sin(2 * math.pi * (t - 0.6) / 1.4)) ** 3   # a few soft pulses: messages arrive
        f = np.clip(a * (1 + (pulse - 1) * lime[..., None]), 0, 1)
        im = Image.fromarray((f * 255).astype(np.uint8))
        z = 1.0 + 0.075 * (t / dur)                                            # slow push-in towards the laptop
        cw, ch = sw / z, sh / z
        cx, cy = sw * 0.47, sh * 0.52
        box = (cx - cw * 0.47 / 1, cy - ch * 0.52, cx - cw * 0.47 + cw, cy - ch * 0.52 + ch)
        im = im.resize((W, H), Image.LANCZOS, box=box)
        im.save(d / f"{i:04d}.png")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-framerate", str(FPS), "-i", str(d / "%04d.png"), "-c:v", "libx264",
                    "-crf", "12", "-preset", "veryfast", "-pix_fmt", "yuv420p", str(VID / "v23_still.mp4")], check=True)


# ------------------------------------------------------------------ rendering
async def render_scene_frames(pg, html, frames_dir, dur, clear, bg="white"):
    hp = WORK / (frames_dir.name + ".html")
    hp.write_text(page(html, clear, bg))
    await pg.goto(hp.as_uri())
    await pg.wait_for_function("window.READY === true", timeout=30000)
    n = int(round(dur * FPS))
    el = await pg.query_selector("section.stage")
    for i in range(n):
        await pg.evaluate(f"window.setT({i / FPS})")
        await el.screenshot(path=str(frames_dir / f"{i:04d}.png"), omit_background=clear)
    return n


def ff(*args):
    subprocess.run(["ffmpeg", "-v", "error", "-y", *map(str, args)], check=True)


async def build(reel_ids):
    async with async_playwright() as p:
        br = await p.chromium.launch()
        pg = await br.new_page(viewport={"width": W, "height": H})
        for rid in reel_ids:
            segs = []
            for k, sc in enumerate(REELS[rid]):
                fd = WORK / f"{rid}_s{k}"
                if fd.exists():
                    shutil.rmtree(fd)
                fd.mkdir(parents=True)
                video = sc.get("video")
                n = await render_scene_frames(pg, sc["html"], fd, sc["dur"], clear=bool(video), bg=sc.get("bg", "white"))
                seg = WORK / f"{rid}_s{k}.mp4"
                if video:
                    ff("-i", VID / video, "-framerate", FPS, "-i", fd / "%04d.png", "-filter_complex",
                       f"[0:v]fps={FPS},scale=-2:{H}:flags=lanczos,crop={W}:{H},trim=0:{sc['dur']},setpts=PTS-STARTPTS[v];"
                       f"[v][1:v]overlay=0:0:shortest=1,format=yuv420p[o]", "-map", "[o]", "-frames:v", n,
                       "-c:v", "libx264", "-crf", "15", "-preset", "medium", "-r", FPS, seg)
                else:
                    ff("-framerate", FPS, "-i", fd / "%04d.png", "-c:v", "libx264", "-crf", "15", "-preset", "medium",
                       "-pix_fmt", "yuv420p", "-r", FPS, seg)
                segs.append(seg)
            lst = WORK / f"{rid}.txt"
            lst.write_text("".join(f"file '{s}'\n" for s in segs))
            silent = WORK / f"{rid}_silent.mp4"
            ff("-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", silent)
            dur = sum(sc["dur"] for sc in REELS[rid])
            cuts = np.cumsum([0] + [sc["dur"] for sc in REELS[rid]])[:-1]
            wav = WORK / f"{rid}.wav"
            make_audio(wav, dur, cuts, seed={"R1": 0, "R2": 1, "R3": 2}[rid])
            OUT.mkdir(parents=True, exist_ok=True)
            ff("-i", silent, "-i", wav, "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest",
               "-movflags", "+faststart", OUT / f"{rid}.mp4")
            print(rid, f"{dur:.1f}s")
        await br.close()


# ------------------------------------------------------------------ an original, quiet sound bed (synthesised here, no licence needed)
def make_audio(path, dur, cuts, seed=0, sr=48000):
    import wave
    t = np.arange(int(dur * sr)) / sr
    chords = [[220.0, 277.18, 329.63, 415.30], [196.0, 246.94, 293.66, 369.99], [174.61, 220.0, 261.63, 329.63]]
    ch = chords[seed % 3]
    pad = np.zeros_like(t)
    for i, f in enumerate(ch):
        det = 1 + 0.0015 * (i - 1.5)
        pad += np.sin(2 * np.pi * f * det * t + i) * (0.9 ** i)
        pad += 0.35 * np.sin(2 * np.pi * f * 2.001 * t + 2 * i) * (0.8 ** i)
    lfo = 0.75 + 0.25 * np.sin(2 * np.pi * 0.18 * t)
    env = np.minimum(1, t / 1.6) * np.minimum(1, (dur - t) / 1.2)
    pad = pad * lfo * env
    # soft tick on each cut: a short filtered noise burst
    rng = np.random.default_rng(seed)
    tick = np.zeros_like(t)
    for c in cuts[1:]:
        s = int(c * sr)
        L = int(0.09 * sr)
        nz = rng.standard_normal(L) * np.exp(-np.arange(L) / (0.012 * sr))
        nz = np.convolve(nz, np.ones(24) / 24, mode="same")
        tick[s:s + L] += nz[: len(tick[s:s + L])] * 0.9
    # simple reverb: feedback delays
    mix = pad * 0.16 + tick * 0.5
    out = mix.copy()
    for dly, g in ((0.031, 0.35), (0.047, 0.3), (0.071, 0.25), (0.113, 0.2)):
        k = int(dly * sr)
        out[k:] += mix[:-k] * g
    out /= max(1e-9, np.abs(out).max()) / 0.32
    st = np.stack([out, np.roll(out, 240)], axis=1)
    pcm = (np.clip(st, -1, 1) * 32767).astype(np.int16)
    with wave.open(str(path), "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(sr); w.writeframes(pcm.tobytes())


if __name__ == "__main__":
    WORK.mkdir(parents=True, exist_ok=True)
    ids = sys.argv[1:] or ["R1", "R2", "R3"]
    if "R3" in ids and not (VID / "v23_still.mp4").exists():
        make_night_still()
    asyncio.run(build(ids))

"""Paket 3: fünf Reels (1080 × 1920, 30 fps) im Grafitecture-CI. Baut auf reel.py (Paket 1) auf:
Szenen sind HTML-Seiten mit setT(t); Video-Szenen bekommen ein transparentes Overlay; R11 ist ein Vorher/Nachher aus Fotos."""
import asyncio, pathlib, shutil, sys, subprocess
import numpy as np
from PIL import Image, ImageOps, ImageDraw
from playwright.async_api import async_playwright
import reel as R
from engine import LOGO, ARROW, img

R.VID = pathlib.Path("/home/claude/ig3/work/vid")
R.WORK = pathlib.Path("/home/claude/ig3/work/reels")
R.OUT = pathlib.Path("/home/claude/ig3/out/reels")
FPS, W, H = R.FPS, R.W, R.H
NB = " "
P = pathlib.Path("/home/claude/ig3/photos")

# Schreibmaschinen-Effekt für die Chat-Zeile in R7
R.ANIM_JS += """
const _setT = window.setT;
window.setT = (t) => {
  _setT(t);
  document.querySelectorAll('[data-type]').forEach((el) => {
    if (!el.dataset.full) el.dataset.full = el.textContent;
    const a = parseFloat(el.dataset.type), d = parseFloat(el.dataset.td || '1.6');
    const n = Math.round(el.dataset.full.length * Math.max(0, Math.min(1, (t - a) / d)));
    el.textContent = el.dataset.full.slice(0, n);
    el.style.opacity = t >= a ? 1 : 0;
  });
  document.querySelectorAll('[data-caret]').forEach((el) => {
    el.style.opacity = (Math.floor(t * 2.4) % 2 === 0) ? 1 : 0;
  });
};
"""

R.REEL_CSS += """
.chat { border: 4px solid var(--line); border-radius: 4px; padding: 44px 48px; font-size: 64px; line-height: 1.2; letter-spacing: -.016em; min-height: 300px; }
.caret { display: inline-block; width: 5px; height: 68px; background: #435960; vertical-align: -10px; margin-left: 6px; }
.ph { position: absolute; left: 96px; right: 96px; overflow: hidden; border-radius: 4px; }
.ph img { display: block; width: 100%; height: 100%; object-fit: cover; }
"""

YEXT = "Quelle: Yext, Consumer Search Behaviors Report 2026, Deutschland; t3n, 4.8.2026"


def end_card(hitl=False):
    line = "Human<br>in the loop." if hitl else "Marken<br>mit KI."
    return dict(dur=2.8, bg="shim", html=f"""{R.sheen(20, 10)}
<div class="a lg" style="top:300px" data-in="0.05">{LOGO}</div>
<div class="a big" style="top:700px;{'font-size:190px' if hitl else ''}" data-in="0.2">{line}</div>
<div class="a sm" style="top:1250px" data-in="0.55">Martin Schweppe<br>grafitecture.de</div>
""")


R7 = [
    dict(dur=4.0, bg="white", html=f"""
<div class="a kk" style="top:420px" data-in="0.05">Gastronomie · Mannheim</div>
<div class="a chat" style="top:520px"><span data-type="0.35" data-td="2.0">Wo esse ich heute Abend gut in Mannheim?</span><span class="caret" data-caret="1"></span></div>
<div class="a sm" style="top:980px" data-in="2.7">Diese Frage stellen Ihre Gäste.<br>Aber nicht mehr nur Google.</div>
"""),
    dict(dur=3.2, bg="lime", html=f"""
<div class="a big" style="top:560px;white-space:nowrap" data-in="0.1">4 von 10</div>
<div class="a sm" style="top:860px" data-in="0.5">suchen lokale Geschäfte<br>inzwischen mit KI.</div>
<div class="a" style="top:1360px;font-size:26px;line-height:1.45" data-in="0.9">{YEXT}</div>
"""),
    dict(dur=4.2, bg="white", html=f"""
<div class="a kk" style="top:420px" data-in="0.05">Die KI antwortet mit dem, was sie findet</div>
<div class="a" style="top:520px">
  <div class="ln" data-line="0.2"></div>
  <div class="row" data-in="0.4"><span class="n">01</span><span class="t">Ihre Website</span></div>
  <div class="ln" data-line="0.6"></div>
  <div class="row" data-in="1.2"><span class="n">02</span><span class="t">Ihre Einträge</span></div>
  <div class="ln" data-line="1.4"></div>
  <div class="row" data-in="2.0"><span class="n">03</span><span class="t">Ihre Bewertungen</span></div>
  <div class="ln" data-line="2.2"></div>
</div>
"""),
    dict(dur=2.4, bg="white", html="""
<div class="a big" style="top:640px;font-size:172px" data-in="0.1">Steht da das Richtige?</div>
"""),
    dict(dur=3.4, bg="lime", html="""
<div class="a kk" style="top:420px" data-in="0.05">Angebot 02</div>
<div class="a mid" style="top:560px" data-in="0.15">KI-Sicht&shy;barkeits-Check.</div>
<div class="a sm" style="top:1000px" data-in="0.7">Ich frage ChatGPT, Gemini und Perplexity nach Ihnen und bringe Ihre Daten in Ordnung.</div>
<div class="a sm" style="top:1300px" data-in="1.3">Schreiben Sie mir »Check«.</div>
"""),
    end_card(),
]

R8 = [
    dict(dur=5.0, video="w_clip.mp4", html="""
<div class="a kk wht" style="top:250px" data-in="0.2">Human in the loop · Mannheim 2017</div>
<div class="a med wht" style="top:330px" data-in="0.5">Mein Foto.</div>
<div class="a med wht" style="top:446px" data-in="2.2">Bewegt von KI.</div>
"""),
    dict(dur=3.2, bg="white", html=f"""
<div class="a kk" style="top:300px" data-in="0.05">Vorher · Handyfoto, November 2017</div>
<div class="ph" style="top:380px;height:888px" data-in="0.1"><img src="{img(P / 'orig/I15_2017.jpg')}"></div>
<div class="a sm" style="top:1340px" data-in="0.8">Die KI: Licht, Format, Bewegung.<br>Ich: Motiv, Ausschnitt, Freigabe.</div>
"""),
    dict(dur=3.0, bg="lime", html="""
<div class="a big" style="top:600px;font-size:172px" data-in="0.1">Ob es bleibt, entscheide ich.</div>
"""),
    end_card(hitl=True),
]

R9 = [
    dict(dur=2.6, bg="shim", html=f"""{R.sheen(4, 12)}
<div class="a big" style="top:660px" data-in="0.1">Vier<br>Angebote.</div>
"""),
] + [
    dict(dur=2.3, bg=bg, html=f"""
<div class="a kk" style="top:560px" data-in="0.05">Angebot {n}</div>
<div class="a mid" style="top:660px" data-in="0.12">{t}</div>
<div class="a sm" style="top:1000px" data-in="0.55">{s}</div>
""") for n, t, s, bg in [
        ("01", "Website.<br>Kostenlos.", "Für Kundinnen und Kunden.", "white"),
        ("02", "KI-Sicht&shy;barkeit.", "Damit die KI Sie richtig nennt.", "lime"),
        ("03", "Bildwelt<br>mit KI.", "Echte Fotos, besser gemacht.", "white"),
        ("04", "KI-Agenten.", "Ein Agent, ein klarer Job.", "lime"),
    ]
] + [
    dict(dur=2.8, bg="white", html="""
<div class="a med" style="top:620px" data-in="0.1">Ein Ansprech&shy;partner.</div>
<div class="a med" style="top:900px" data-in="0.7">Klare Preise.</div>
<div class="a kk" style="top:1240px" data-in="1.2">Human in the loop: Martin Schweppe</div>
"""),
    end_card(),
]

R10 = [
    dict(dur=3.0, bg="white", html="""
<div class="a big" style="top:620px;font-size:172px" data-in="0.1">Wer fragt die KI nach Ihnen?</div>
"""),
    dict(dur=3.4, bg="lime", html=f"""
<div class="a big" style="top:560px;white-space:nowrap" data-in="0.1">48{NB}%</div>
<div class="a sm" style="top:860px" data-in="0.5">prüfen eine KI-Empfehlung danach<br>auf der Website des Anbieters.</div>
<div class="a" style="top:1360px;font-size:26px;line-height:1.45" data-in="0.9">{YEXT}</div>
"""),
    dict(dur=4.4, bg="white", html="""
<div class="a kk" style="top:420px" data-in="0.05">Was eine Website heute braucht</div>
<div class="a" style="top:520px">
  <div class="ln" data-line="0.2"></div>
  <div class="row" data-in="0.4"><span class="n">01</span><span class="t">Klare Fakten</span></div>
  <div class="ln" data-line="0.6"></div>
  <div class="row" data-in="1.0"><span class="n">02</span><span class="t">Daten, die Maschinen lesen</span></div>
  <div class="ln" data-line="1.2"></div>
  <div class="row" data-in="1.6"><span class="n">03</span><span class="t">Schnell auf dem Handy</span></div>
  <div class="ln" data-line="1.8"></div>
  <div class="row" data-in="2.2"><span class="n">04</span><span class="t">Gestaltung, die man wiedererkennt</span></div>
  <div class="ln" data-line="2.4"></div>
</div>
"""),
    dict(dur=3.2, bg="shim", html=f"""{R.sheen(30, 10)}
<div class="a mid" style="top:560px" data-in="0.1">Ihre neue Website. Kostenlos.</div>
<div class="a sm" style="top:1020px" data-in="0.6">Für Kundinnen und Kunden.<br>Schreiben Sie mir »Website«.</div>
"""),
    end_card(),
]

R11_INTRO = dict(dur=2.4, bg="lime", html="""
<div class="a kk" style="top:420px" data-in="0.05">Human in the loop</div>
<div class="a big" style="top:620px" data-in="0.1">Vorher.<br>Nachher.</div>
<div class="a sm" style="top:1120px" data-in="0.6">Sieben eigene Fotos, 2008 bis 2021.</div>
""")
R11_OUTRO = dict(dur=3.0, bg="white", html="""
<div class="a med" style="top:620px" data-in="0.1">Die KI macht das Licht.</div>
<div class="a med" style="top:900px" data-in="0.8">Das Motiv bleibt echt.</div>
<div class="a kk" style="top:1240px" data-in="1.3">Bildwelt mit KI · Angebot 03</div>
""")
PAIRS = [("D18_2011", "H1"), ("E22_2008", "H2"), ("I3_2016", "H3"), ("N1_2021", "H4"),
         ("N2_2017", "H5"), ("N3_2018", "H6"), ("N5_2021", "H7")]

REELS = {"R7": R7, "R8": R8, "R9": R9, "R10": R10}


CENTER = {"H4": (0.1, 0.5), "N1_2021": (0.15, 0.5)}


def fill(im, key=None):
    return ImageOps.fit(im.convert("RGB"), (W, H), Image.LANCZOS, centering=CENTER.get(key, (0.5, 0.5)))


def make_wipes(path, each=1.7):
    """Vorher/Nachher: Original, dann wischt eine Lime-Linie das bearbeitete Bild herein."""
    d = R.WORK / "R11_wipes"
    if d.exists():
        shutil.rmtree(d)
    d.mkdir(parents=True)
    k = 0
    lime = (218, 253, 85)
    for o, h in PAIRS:
        a = fill(Image.open(P / f"orig/{o}.jpg"), o)
        b = fill(Image.open(P / f"hf/{h}.png"), h)
        n = int(each * FPS)
        for i in range(n):
            t = i / FPS
            p = min(1, max(0, (t - 0.45) / 0.7))
            p = 1 - (1 - p) ** 3
            x = int(round(W * p))
            fr = a.copy()
            if x > 0:
                fr.paste(b.crop((0, 0, x, H)), (0, 0))
            if 0 < p < 1:
                ImageDraw.Draw(fr).rectangle((x - 3, 0, x + 3, H), fill=lime)
            fr.save(d / f"{k:05d}.png")
            k += 1
    R.ff("-framerate", FPS, "-i", d / "%05d.png", "-c:v", "libx264", "-crf", "15", "-preset", "veryfast",
         "-pix_fmt", "yuv420p", "-r", FPS, path)
    return k / FPS


async def scene_mp4(pg, rid, k, sc):
    fd = R.WORK / f"{rid}_s{k}"
    if fd.exists():
        shutil.rmtree(fd)
    fd.mkdir(parents=True)
    video = sc.get("video")
    n = await R.render_scene_frames(pg, sc["html"], fd, sc["dur"], clear=bool(video), bg=sc.get("bg", "white"))
    seg = R.WORK / f"{rid}_s{k}.mp4"
    if video:
        R.ff("-i", R.VID / video, "-framerate", FPS, "-i", fd / "%04d.png", "-filter_complex",
             f"[0:v]fps={FPS},scale={W}:{H}:flags=lanczos,trim=0:{sc['dur']},setpts=PTS-STARTPTS[v];"
             f"[v][1:v]overlay=0:0:shortest=1,format=yuv420p[o]", "-map", "[o]", "-frames:v", n,
             "-c:v", "libx264", "-crf", "15", "-preset", "veryfast", "-r", FPS, seg)
    else:
        R.ff("-framerate", FPS, "-i", fd / "%04d.png", "-c:v", "libx264", "-crf", "15", "-preset", "veryfast",
             "-pix_fmt", "yuv420p", "-r", FPS, seg)
    return seg


async def build(ids):
    R.WORK.mkdir(parents=True, exist_ok=True)
    R.OUT.mkdir(parents=True, exist_ok=True)
    async with async_playwright() as p:
        br = await p.chromium.launch()
        pg = await br.new_page(viewport={"width": W, "height": H})
        for rid in ids:
            segs, durs = [], []
            if rid == "R11":
                plan = [R11_INTRO, "WIPES", R11_OUTRO, end_card(hitl=True)]
            else:
                plan = REELS[rid]
            for k, sc in enumerate(plan):
                if sc == "WIPES":
                    seg = R.WORK / "R11_wipes.mp4"
                    durs.append(make_wipes(seg))
                    segs.append(seg)
                    continue
                segs.append(await scene_mp4(pg, rid, k, sc))
                durs.append(sc["dur"])
            lst = R.WORK / f"{rid}.txt"
            lst.write_text("".join(f"file '{s}'\n" for s in segs))
            silent = R.WORK / f"{rid}_silent.mp4"
            R.ff("-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", silent)
            dur = float(sum(durs))
            cuts = np.cumsum([0] + durs)[:-1]
            wav = R.WORK / f"{rid}.wav"
            R.make_audio(wav, dur, cuts, seed={"R7": 0, "R8": 1, "R9": 2, "R10": 0, "R11": 1}[rid])
            R.ff("-i", silent, "-i", wav, "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest",
                 "-movflags", "+faststart", R.OUT / f"{rid}.mp4")
            print(rid, f"{dur:.1f}s")
        await br.close()


def with_cover(rid, cover_png, still=0.4):
    """Version für Canva: Titelbild als erste Bilder, damit Instagram es als Cover nimmt."""
    out = R.OUT / f"{rid}_mit_Titelbild_fuer_Canva.mp4"
    R.ff("-loop", "1", "-t", still, "-framerate", FPS, "-i", cover_png, "-i", R.OUT / f"{rid}.mp4",
         "-filter_complex",
         f"[0:v]scale={W}:{H},format=yuv420p,setsar=1[c];[1:v]setsar=1[v];"
         f"anullsrc=r=48000:cl=stereo,atrim=0:{still}[s];[1:a]aresample=48000[a];"
         "[c][s][v][a]concat=n=2:v=1:a=1[ov][oa]",
         "-map", "[ov]", "-map", "[oa]", "-c:v", "libx264", "-crf", "16", "-preset", "veryfast", "-r", FPS,
         "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", out)


if __name__ == "__main__":
    ids = sys.argv[1:] or ["R7", "R8", "R9", "R10", "R11"]
    asyncio.run(build(ids))

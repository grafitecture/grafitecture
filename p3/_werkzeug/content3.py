"""Paket 3 (Stand 18.11.2026): 20 Beiträge für @g.r.a.f.i.t.e.c.t.u.r.e.
Neue Serie HUMAN IN THE LOOP (eigene Fotos von Martin, ohne Personen, mit Higgsfield bearbeitet),
Angebote, Website, Gastronomie, Design, Werbung. Jede Zahl mit Quelle auf der Folie."""
from engine import *
from PIL import Image, ImageStat

NB = " "          # schmales geschütztes Leerzeichen: 57 %, 4 von 10
P = pathlib.Path("/home/claude/ig3/photos")
HF = P / "hf"
ORIG = P / "orig"

ORIG_OF = {"H1": "D18_2011", "H2": "E22_2008", "H3": "I3_2016", "H4": "B2_2015", "H5": "B15_2015",
           "H6": "I11_2017", "H7": "I6_2016", "W": "I15_2017"}


def K(t):
    return f'<span class="k">{t}</span>'


def top(left="", right=""):
    return f'<div class="top">{left}{right}</div>'


def src(t, style="margin-top:40px"):
    return f'<p class="src" style="{style}">{t}</p>'


SIGN = "Human in the loop: Martin Schweppe"


def end3(cls, line, sub, dm, sheen=None):
    """Abschluss mit Angebot und Direktnachricht. Unterschrift: Human in the loop ist Martin Schweppe."""
    return slide(cls, f"""
{top(logo(), K("grafitecture.de"))}
<div class="grow"></div>
<p class="h5 m0" style="max-width:15ch">{line}</p>
<p class="h6" style="margin-top:44px;max-width:21ch">{sub}</p>
<p class="h6" style="margin-top:44px;max-width:21ch">Schreiben Sie mir »{dm}« als Direktnachricht. Ich antworte persönlich.</p>
<div class="rule" style="margin-top:64px"></div>
<div class="top" style="margin-top:28px"><span class="k">{SIGN}</span><span class="k">Mannheim</span></div>
""", sheen=sheen)


def label_colour(path, box=(0, 0, 1, 0.12)):
    """Weiß oder #435960 für die kleinen Beschriftungen auf dem Foto, je nach Helligkeit oben."""
    im = Image.open(path).convert("L")
    w, h = im.size
    crop = im.crop((int(box[0] * w), int(box[1] * h), int(box[2] * w), int(box[3] * h)))
    return "#ffffff" if ImageStat.Stat(crop).mean[0] < 150 else "#435960"


def photo(key, n, place, arrow=False, pos="50% 50%", label_box=None):
    """Vollbild aus der Serie Human in the loop: nur das Foto, keine Schrift (Serie, Ort und Jahr stehen in der Caption)."""
    f = HF / f"{key}.png"
    return slide("white", f"""
<div class="bleed" style="top:0"><img src="{img(f)}" style="object-position:{pos}"></div>
""")


def before(key, when, ai, me):
    """Folie Vorher: das Original vom Handy, darunter wer was gemacht hat."""
    f = ORIG / f"{ORIG_OF[key]}.jpg"
    return slide("white", f"""
{top(K("Vorher"), K(when))}
<figure class="photo" style="margin-top:40px;height:640px;background:#fff"><img src="{img(f)}" style="object-fit:contain;object-position:0% 50%"></figure>
<div class="grow"></div>
<ul class="rows">
<li style="grid-template-columns:230px 1fr;column-gap:24px;align-items:baseline"><span class="k">Die KI</span><span class="t">{ai}</span></li>
<li style="grid-template-columns:230px 1fr;column-gap:24px;align-items:baseline"><span class="k">Ich</span><span class="t">{me}</span></li>
</ul>
""")


def thought(n, line, body):
    return slide("lime", f"""
{top(K(f"Human in the loop · {n:02d}"), "")}
<div class="grow"></div>
<p class="h4 m0" style="max-width:9ch">{line}</p>
<p class="h6" style="margin-top:60px;max-width:21ch">{body}</p>
<div class="rule" style="margin-top:64px"></div>
<div class="top" style="margin-top:28px"><span class="k">{SIGN}</span><span class="k">grafitecture.de</span></div>
""")


def offer(n, title, lead, get, ai, me):
    return slide("white", f"""
{top(K(f"Angebot {n:02d}"), K("grafitecture"))}
<p class="h4" style="margin-top:110px;max-width:9ch">{title}</p>
<p class="h6" style="margin-top:44px;max-width:21ch">{lead}</p>
<div class="grow"></div>
<ul class="rows">
<li style="grid-template-columns:250px 1fr;column-gap:24px;align-items:baseline"><span class="k">Sie bekommen</span><span class="d">{get}</span></li>
<li style="grid-template-columns:250px 1fr;column-gap:24px;align-items:baseline"><span class="k">Die KI macht</span><span class="d">{ai}</span></li>
<li style="grid-template-columns:250px 1fr;column-gap:24px;align-items:baseline"><span class="k">Ich entscheide</span><span class="d">{me}</span></li>
</ul>
""")


YEXT = f"Quelle: Yext, Consumer Search Behaviors Report 2026, Befragte in Deutschland; t3n, 4.8.2026"
SEO = "Quelle: YouGov im Auftrag von Seokratie, 509 Entscheiderinnen und Entscheider; Retail-News, 2.8.2026"
DIEL = ("Quelle: Diel u. a., Universität Duisburg-Essen / LVR-Universitätsklinik Essen; "
        "dpa via tageskarte.io, 5.11.2026")
SPROUT = "Quelle: Sprout Social, Q1 2026 Pulse Survey, Konsumentinnen und Konsumenten; 8.4.2026"

POSTS = {}

# ============================================================ HUMAN IN THE LOOP (eigene Fotos, keine Personen)
POSTS["H1"] = [
    photo("H1", 1, "Mannheim · 2011", arrow=True),
    before("H1", "Handyfoto · Januar 2011", "Licht, Farbe, Rauschen, Format 4:5",
           "Motiv, Ausschnitt, Prüfung, Freigabe"),
    thought(1, "Ornament ist Hand&shy;schrift.",
            "Jede Kurve in diesem Geländer hat jemand entschieden. Gute Gestaltung erkennt man daran, "
            "dass Entscheidungen sichtbar sind. Mit KI erst recht."),
]
POSTS["H2"] = [photo("H2", 2, "Mannheim · 2008")]
POSTS["H3"] = [photo("H3", 3, "Mannheim · 2016")]
POSTS["H4"] = [
    photo("H4", 4, "Atelier · 2015", arrow=True),
    before("H4", "Handyfoto · November 2015", "Licht, Chrom, gerader Horizont, Format 4:5",
           "Motiv, Ausschnitt, Prüfung, Freigabe"),
    thought(4, "Die Maschine macht den Kaffee.",
            "Den Geschmack macht der Mensch. Mit KI ist es genauso: Sie erledigt die Routine. "
            "Was rausgeht, entscheide ich."),
]
POSTS["H5"] = [photo("H5", 5, "Atelier · 2015")]
POSTS["H6"] = [
    photo("H6", 6, "Mannheim · 2017", arrow=True),
    before("H6", "Handyfoto · Juni 2017", "Licht, Hintergrund, Format 4:5",
           "Das Gericht bleibt, wie es war. Freigabe"),
    thought(6, "Echtes Essen. Echtes Foto.",
            "KI-generierte Essensbilder machen weniger Appetit, das zeigt eine Studie der Universität "
            "Duisburg-Essen. Deshalb bleibt das Gericht echt. Die KI macht nur das Licht."),
]
POSTS["H7"] = [photo("H7", 7, "Café-Stuhl · 2016")]

# ============================================================ K7 · 4 von 10 (Gastronomie, KI-Suche)
POSTS["K7"] = [
    slide("lime", f"""
{top(logo(), K("KI-Suche · Gastronomie"))}
<div class="grow"></div>
<div style="font-size:330px;line-height:.86;letter-spacing:-.05em;margin-left:-10px;white-space:nowrap">4 von<br>10</div>
<p class="h6" style="margin-top:60px;max-width:19ch">suchen lokale Geschäfte inzwischen mit KI. Auch Ihr Restaurant.</p>
<div class="top" style="margin-top:56px;align-items:flex-end"><p class="src m0" style="max-width:36ch">{YEXT}</p><span class="arrow">{ARROW}</span></div>
"""),
    slide("white", f"""
{top(K("Letzte sechs Monate"), "")}
<div class="grow"></div>
<div style="font-size:400px;line-height:.86;letter-spacing:-.05em;margin-left:-14px">27{NB}%</div>
<p class="h6" style="margin-top:56px;max-width:20ch">haben wegen einer KI-Empfehlung ein neues Geschäft besucht oder kontaktiert.</p>
<p class="h5" style="margin-top:72px;max-width:15ch">Fast jeder Zweite davon ging essen.</p>
{src(YEXT + ". 48 % dieser Gruppe besuchten einen Gastronomiebetrieb.", "margin-top:48px")}
"""),
    slide("white", f"""
<h2 class="h5 m0" style="max-width:14ch">Aber: Die Gäste prüfen nach.</h2>
<div class="grow"></div>
<ul class="rows num">
<li><span class="n">50{NB}%</span><span class="t">in der Suchmaschine</span></li>
<li><span class="n">48{NB}%</span><span class="t">auf Ihrer Website</span></li>
<li><span class="n">33{NB}%</span><span class="t">in den Quellen, die die KI nennt</span></li>
</ul>
{src("Nur 4 % übernehmen eine KI-Empfehlung ohne weitere Prüfung. " + YEXT)}
"""),
    slide("lime", f"""
{top(K("Meine Lesart"), "")}
<div class="grow"></div>
<p class="h4 m0">Die KI empfiehlt. Ihre Website überzeugt.</p>
<p class="h6" style="margin-top:64px;max-width:21ch">Was die KI über Sie sagt, holt sie sich von Ihrer Website, aus Einträgen und Bewertungen. Stimmt dieses Bild?</p>
"""),
    end3("white", "KI-Sichtbarkeits-Check für Ihr Lokal.",
         "Ich frage ChatGPT, Gemini und Perplexity nach Ihnen, prüfe die Antworten und bringe Website und Einträge in Ordnung.",
         "Check"),
]

# ============================================================ K8 · GEO (Werbung, Marketing)
POSTS["K8"] = [
    slide("lime", f"""
{top(logo(), K("Marketing 2026"))}
<div class="grow"></div>
<h1 class="h1 m0">GEO.</h1>
<p class="h6" style="margin-top:60px;max-width:18ch">Das neue SEO. 41{NB}% der Entscheider haben den Begriff noch nie gehört.</p>
<div class="top" style="margin-top:56px;align-items:flex-end"><p class="src m0" style="max-width:36ch">{SEO}</p><span class="arrow">{ARROW}</span></div>
"""),
    slide("white", f"""
{top(K("Generative Engine Optimization"), "")}
<div class="grow"></div>
<p class="h4 m0">Nicht mehr nur gefunden werden. Genannt werden.</p>
<p class="h6" style="margin-top:64px;max-width:21ch">Wer ChatGPT oder Gemini fragt, bekommt keine Trefferliste, sondern eine Antwort. GEO sorgt dafür, dass Ihr Name darin vorkommt, und zwar richtig.</p>
"""),
    slide("white", f"""
{top(K("Entscheider in Deutschland"), "")}
<div class="grow"></div>
<div style="font-size:400px;line-height:.86;letter-spacing:-.05em;margin-left:-14px">58{NB}%</div>
<p class="h6" style="margin-top:56px;max-width:20ch">glauben, dass Unternehmen Kunden verlieren, wenn sie in KI-Antworten nicht vorkommen.</p>
<p class="h6" style="margin-top:48px;max-width:20ch">Von den kleinen Firmen fühlt sich nur ein Drittel vorbereitet.</p>
{src(SEO + ". Kleine Firmen: unter 50 Beschäftigte.", "margin-top:48px")}
"""),
    slide("white", f"""
<div class="two"><span class="k">SEO</span><span class="k">GEO</span></div>
<ul class="rows" style="margin-top:20px">
<li style="grid-template-columns:1fr 1fr;column-gap:48px"><span class="t">Platz in der Liste</span><span class="t">Nennung in der Antwort</span></li>
<li style="grid-template-columns:1fr 1fr;column-gap:48px"><span class="t">Keywords</span><span class="t">klare Fakten</span></li>
<li style="grid-template-columns:1fr 1fr;column-gap:48px"><span class="t">Backlinks</span><span class="t">Quellen und Zahlen</span></li>
<li style="grid-template-columns:1fr 1fr;column-gap:48px"><span class="t">Klick auf Ihre Seite</span><span class="t">Ihr Name im Satz der KI</span></li>
</ul>
<div class="grow"></div>
<p class="h5 m0" style="max-width:16ch">SEO bleibt. GEO kommt dazu.</p>
{src("71 % der Befragten halten SEO auch in der KI-Ära für wichtig. " + SEO)}
"""),
    slide("white", f"""
<h2 class="h5 m0" style="max-width:15ch">Was ich dafür baue</h2>
<div class="grow"></div>
<ul class="rows num">
<li><span class="n">01</span><span class="t">Klare Fakten auf der Website: wer, was, wo, seit wann</span></li>
<li><span class="n">02</span><span class="t">Strukturierte Daten, die Maschinen lesen</span></li>
<li><span class="n">03</span><span class="t">Einträge und Profile, die übereinstimmen</span></li>
<li><span class="n">04</span><span class="t">Ein Agent, der jeden Monat nachfragt, was die KI über Sie sagt</span></li>
</ul>
"""),
    end3("lime", "Was sagt ChatGPT über Ihre Marke?", "Ich finde es heraus und sorge dafür, dass es stimmt.", "GEO"),
]

# ============================================================ K9 · KI-Essen macht weniger Appetit (Gastronomie, Design)
POSTS["K9"] = [
    slide("white", f"""
{top(logo(), K("Gastronomie · Studie 2026"))}
<div class="grow"></div>
<h1 class="h3 m0" style="max-width:8ch">KI-Essen macht weniger Appetit.</h1>
<div class="top" style="margin-top:64px;align-items:flex-end"><p class="h6 m0" style="max-width:17ch">Was das für Ihre Speisekarte heißt.</p><span class="arrow">{ARROW}</span></div>
"""),
    slide("white", f"""
{top(K("Der Versuch"), "")}
<div class="grow"></div>
<p class="h3 m0">87 Personen. 60 Bildpaare.</p>
<p class="h6" style="margin-top:64px;max-width:21ch">Jeweils ein echtes Foto und ein KI-Bild desselben Essens, von Vanilleeis bis Weintrauben. Welches welches war, wussten sie nicht.</p>
{src(DIEL, "margin-top:56px")}
"""),
    slide("lime", f"""
<h2 class="h5 m0">Das Ergebnis</h2>
<div class="grow"></div>
<ul class="rows">
<li style="grid-template-columns:1fr 1fr;column-gap:48px"><span class="t">Gesund?</span><span class="t">gleich bewertet</span></li>
<li style="grid-template-columns:1fr 1fr;column-gap:48px"><span class="t">Kalorien?</span><span class="t">gleich bewertet</span></li>
<li style="grid-template-columns:1fr 1fr;column-gap:48px"><span class="t">Echt?</span><span class="t">KI-Bild verliert</span></li>
<li style="grid-template-columns:1fr 1fr;column-gap:48px"><span class="t">Appetit?</span><span class="t">KI-Bild verliert</span></li>
</ul>
{src(DIEL)}
"""),
    slide("white", f"""
{top(K("So arbeite ich"), "")}
<div class="two" style="margin-top:56px;column-gap:24px">
<figure class="photo" style="height:600px"><img src="{img(ORIG / 'I11_2017.jpg')}"></figure>
<figure class="photo" style="height:600px"><img src="{img(HF / 'H6.png')}"></figure>
</div>
<div class="two" style="margin-top:20px;column-gap:24px"><span class="k">Handyfoto</span><span class="k">Mit KI: Licht, Hintergrund</span></div>
<div class="grow"></div>
<p class="h5 m0" style="max-width:16ch">Das Gericht bleibt echt. Die KI macht das Licht.</p>
"""),
    end3("white", "Bildwelt mit KI für Ihr Lokal.",
         "Ihre echten Gerichte, Ihr Raum, einheitlich bearbeitet, in allen Formaten. Gekennzeichnet, wie es sich gehört.",
         "Bilder"),
]

# ============================================================ K10 · KI-Slop (Design, Werbung)
POSTS["K10"] = [
    slide("white", f"""
{top(logo(), K("Design · Social Media"))}
<div class="grow"></div>
<div style="font-size:430px;line-height:.86;letter-spacing:-.05em;margin-left:-14px">56{NB}%</div>
<p class="h6" style="margin-top:60px;max-width:17ch">sehen in Social Media oft oder sehr oft KI-Slop.</p>
<div class="top" style="margin-top:56px;align-items:flex-end"><p class="src m0" style="max-width:36ch">{SPROUT}</p><span class="arrow">{ARROW}</span></div>
"""),
    slide("white", f"""
{top(K("Ihr größter Wunsch an Marken"), "")}
<div class="grow"></div>
<p class="h4 m0">KI-Inhalte nicht ohne Kenn&shy;zeichnung posten.</p>
{src(SPROUT, "margin-top:72px")}
"""),
    slide("white", f"""
<h2 class="h5 m0" style="max-width:15ch">Fünf Regeln gegen KI-Slop</h2>
<div class="grow"></div>
<ul class="rows num">
<li><span class="n">01</span><span class="t">Kennzeichnen. Immer.</span></li>
<li><span class="n">02</span><span class="t">Echtes Material als Basis: Fotos, Fakten, Stimmen</span></li>
<li><span class="n">03</span><span class="t">Eine Bildsprache statt hundert Stile</span></li>
<li><span class="n">04</span><span class="t">Quellen gehören auf die Folie</span></li>
<li><span class="n">05</span><span class="t">Ein Mensch gibt frei</span></li>
</ul>
"""),
    slide("lime", f"""
{top(K("Meine Lesart"), "")}
<div class="grow"></div>
<p class="h4 m0">Slop ist kein KI-Problem.</p>
<p class="h4" style="margin-top:40px">Es ist ein Gestaltungs&shy;problem.</p>
"""),
    end3("white", "Gestaltung für Marken, die KI nutzen.", "Mit Regeln, Bildsprache und einem Menschen, der freigibt.", "Design"),
]

# ============================================================ K11 · Vier Angebote (Highlight ANGEBOTE)
POSTS["K11"] = [
    slide("shim", f"""
{top(logo(), K("Angebote · November 2026"))}
<div class="grow"></div>
<h1 class="h2 m0" style="font-size:190px">Vier Angebote.</h1>
<div class="top" style="margin-top:64px;align-items:flex-end"><p class="h6 m0" style="max-width:17ch">Marken mit KI. Ein Ansprechpartner. Klare Preise.</p><span class="arrow">{ARROW}</span></div>
""", sheen={"clock": 8}),
    offer(1, "Website. Kostenlos.", "Für Kundinnen und Kunden. Gebaut mit KI, gestaltet von mir, lesbar für Menschen und Maschinen.",
          "eine schnelle, gestaltete Website mit klaren Texten und sauberem Code",
          "Entwürfe, Varianten, Übersetzung, Technik-Routine", "Gestaltung, Texte, Freigabe"),
    offer(2, "KI-Sicht&shy;barkeit.", "Damit ChatGPT, Gemini und Perplexity Ihre Marke richtig nennen.",
          "den Check, was die KI über Sie sagt, und die Korrekturen",
          "Fragen stellen, Antworten vergleichen, monatlich nachprüfen", "was stimmt, was fehlt, was wir ändern"),
    offer(3, "Bildwelt<br>mit KI.", "Ihre echten Fotos, einheitlich bearbeitet. Auf Wunsch als kurze Clips für Reels.",
          "Bilder in allen Formaten, vom Post bis zur Speisekarte",
          "Licht, Farbe, Format, Bewegung", "Auswahl, Bildsprache, Kennzeichnung"),
    offer(4, "KI-Agenten.", "Ein Agent, ein klarer Job. Rund um die Uhr, ohne Babysitting.",
          "z. B. Anfragen vorsortieren oder Antworten auf Bewertungen entwerfen",
          "die Routine, Tag und Nacht", "was rausgeht. Sie geben frei"),
    slide("lime", f"""
{top(K("So läuft’s"), "")}
<div class="grow"></div>
<ul class="rows num">
<li><span class="n">01</span><span class="t">Erstgespräch: Wir prüfen, ob es passt</span></li>
<li><span class="n">02</span><span class="t">Angebot mit klaren Preisen</span></li>
<li><span class="n">03</span><span class="t">Sie entscheiden in Ruhe</span></li>
</ul>
"""),
    end3("white", "Welches Angebot passt zu Ihnen?", "Drei Sätze zu Ihrem Vorhaben reichen.", "Angebot"),
]

# ============================================================ K12 · Das Gastro-Paket
POSTS["K12"] = [
    slide("lime", f"""
{top(logo(), K("Für Gastronomie"))}
<div class="grow"></div>
<h1 class="h2 m0" style="max-width:7ch">Das Gastro-Paket.</h1>
<div class="top" style="margin-top:64px;align-items:flex-end"><p class="h6 m0" style="max-width:17ch">Damit die KI Ihr Lokal empfiehlt und die Gäste es wiederfinden.</p><span class="arrow">{ARROW}</span></div>
"""),
    slide("white", f"""
<h2 class="h5 m0" style="max-width:15ch">Was drin ist</h2>
<div class="grow"></div>
<ul class="rows">
<li><span class="t">Website, kostenlos</span><span class="d">Karte, Öffnungszeiten, Reservierung. Klar für Gäste und für die KI.</span></li>
<li><span class="t">Speisekarte in mehreren Sprachen</span><span class="d">übersetzt mit KI, freigegeben von Ihnen</span></li>
<li><span class="t">Echte Fotos, besser gemacht</span><span class="d">Ihre Gerichte, Ihr Raum. KI nur für Licht und Format</span></li>
<li><span class="t">Antworten auf Bewertungen</span><span class="d">Die KI entwirft, Sie geben frei</span></li>
<li><span class="t">KI-Sichtbarkeits-Check</span><span class="d">Was ChatGPT über Ihr Lokal sagt, und was wir korrigieren</span></li>
</ul>
"""),
    slide("white", f"""
{top(K("Warum jetzt"), "")}
<div class="grow"></div>
<p class="h4 m0">Fast jeder Zweite, der einer KI-Empfehlung folgt, geht essen.</p>
{src("Von den 27 %, die in den letzten sechs Monaten wegen einer KI-Empfehlung ein neues Geschäft besucht oder kontaktiert haben, gingen 48 % in die Gastronomie. " + YEXT, "margin-top:72px")}
"""),
    slide("lime", f"""
{top(K("Aus der Praxis"), "")}
<div class="grow"></div>
<p class="h4 m0" style="max-width:10ch">Gastronomie ist seit Jahren mein Feld.</p>
<p class="h6" style="margin-top:64px;max-width:21ch">Zum Beispiel die Onkel Otto Bar im Mannheimer Jungbusch. Ich weiß, wie wenig Zeit zwischen Mise en Place und letzter Runde bleibt.</p>
"""),
    end3("white", "Das Gastro-Paket für Ihr Lokal.", "Ein Gespräch, ein Angebot mit klaren Preisen.", "Gastro"),
]

# ============================================================ K13 · Warum Grafitecture
POSTS["K13"] = [
    slide("white", f"""
{top(logo(), K("Marken mit KI"))}
<div class="grow"></div>
<h1 class="m0" style="font-size:136px;line-height:.98;letter-spacing:-.035em;font-weight:400">Warum<br>Grafitecture?</h1>
<div class="top" style="margin-top:64px;align-items:flex-end"><p class="h6 m0" style="max-width:17ch">Sechs Gründe, KI mit einem Gestalter zu machen.</p><span class="arrow">{ARROW}</span></div>
"""),
    slide("white", f"""
<ul class="rows num">
<li><span class="n">01</span><span class="t">26 Jahre Gestaltung, seit 2000 in Mannheim</span></li>
<li><span class="n">02</span><span class="t">Ein Ansprechpartner statt Ticket-System</span></li>
<li><span class="n">03</span><span class="t">Systeme statt Tool-Listen</span></li>
<li><span class="n">04</span><span class="t">Jedes Ergebnis geht über meinen Tisch</span></li>
<li><span class="n">05</span><span class="t">Der Code gehört Ihnen, in Ihrem eigenen Repository</span></li>
<li><span class="n">06</span><span class="t">Zahlen mit Quelle, KI-Inhalte gekennzeichnet</span></li>
</ul>
<div class="grow"></div>
<p class="h6 m0" style="max-width:21ch">Kunden aus Gesundheit, Gastronomie, Finanzen und Logistik.</p>
"""),
    slide("lime", f"""
<div class="grow"></div>
<p class="h4 m0">Die KI liefert Tempo.</p>
<p class="h4" style="margin-top:40px">Ich liefere Urteil.</p>
"""),
    end3("white", "Human in the loop ist Martin Schweppe.", "Diplom-Designer, Grafitecture GmbH, Mannheim.", "Hallo"),
]

# ============================================================ K14 · Ein Foto. Sieben Formate.
def fmt(label, w, h, pos="50% 50%"):
    return (f'<div style="display:flex;flex-direction:column;gap:12px"><figure class="photo" style="width:{w}px;height:{h}px">'
            f'<img src="{img(HF / "H1.png")}" style="object-position:{pos}"></figure><span class="cap">{label}</span></div>')


POSTS["K14"] = [
    slide("white", f"""
{top(logo(), K("Bildwelt mit KI"))}
<h1 class="h3" style="margin-top:110px;max-width:8ch">Ein Foto. Sieben Formate.</h1>
<div class="bleed" style="top:760px"><img src="{img(HF / 'H1.png')}" style="object-position:50% 45%"></div>
"""),
    slide("white", f"""
{top(K("Aus einem Bild"), K("Beispiel"))}
<div style="margin-top:48px;display:flex;gap:24px;align-items:flex-end">
{fmt("Post 4:5", 288, 360)}{fmt("Story 9:16", 203, 360)}{fmt("Profil 1:1", 300, 300)}
</div>
<div style="margin-top:36px;display:flex;gap:24px;align-items:flex-end">
{fmt("Website 16:9", 520, 292, "50% 35%")}{fmt("Plakat A1", 206, 292)}{fmt("Karte A5", 98, 140)}
</div>
<div class="grow"></div>
<p class="h6 m0" style="max-width:21ch">Siebtes Format: ein kurzer Clip für Reels.</p>
"""),
    slide("lime", f"""
{top(K("Wer macht was"), "")}
<div class="grow"></div>
<p class="h5 m0" style="max-width:17ch">Die KI schneidet zu, erweitert, bewegt, übersetzt.</p>
<p class="h5" style="margin-top:56px;max-width:17ch">Ich wähle das eine Foto, das es wert ist.</p>
"""),
    end3("white", "Bildwelt mit KI.", "Aus Ihren Fotos wird ein System für alle Kanäle.", "Bilder"),
]

# ============================================================ Reel-Titelbilder (1080 × 1920, Raster zeigt die Mitte 3:4)
COVERS = {}


def cover(cls, inner, sheen=None):
    return slide(f"{cls} reel", inner, sheen=sheen, extra_style="padding:330px 96px 330px")


COVERS["R7"] = cover("lime", f"""
{top(logo(), K("Reel · Gastronomie"))}
<div class="grow"></div>
<p class="h3 m0" style="max-width:8ch">Fragen Sie mal ChatGPT.</p>
<p class="h6" style="margin-top:56px;max-width:17ch">Was die KI über Ihr Restaurant erzählt.</p>
<div class="grow"></div>
""")
COVERS["R8"] = cover("white", f"""
{top(K("Human in the loop · Reel"), K("Mannheim"))}
<div class="grow"></div>
<p class="h3 m0" style="max-width:7ch">Mein Foto. Bewegt.</p>
<figure class="photo" style="margin-top:64px;height:600px"><img src="{img(HF / 'W.png')}" style="object-position:50% 30%"></figure>
<div class="grow"></div>
""")
COVERS["R9"] = cover("lime", f"""
{top(logo(), K("Reel · Angebote"))}
<div class="grow"></div>
<p class="h2 m0" style="max-width:7ch">Was ich anbiete.</p>
<p class="h6" style="margin-top:56px;max-width:17ch">Vier Angebote in 17 Sekunden.</p>
<div class="grow"></div>
""")
COVERS["R10"] = cover("white", f"""
{top(logo(), K("Reel · Website"))}
<div class="grow"></div>
<p class="h3 m0" style="max-width:8ch">Lesbar für Menschen und Maschinen.</p>
<p class="h6" style="margin-top:56px;max-width:17ch">Ihre neue Website. Kostenlos.</p>
<div class="grow"></div>
""")
COVERS["R11"] = cover("lime", f"""
{top(K("Human in the loop · Reel"), "")}
<div class="grow"></div>
<p class="h2 m0">Vorher. Nachher.</p>
<p class="h6" style="margin-top:56px;max-width:17ch">Sieben eigene Fotos. Die KI macht das Licht.</p>
<div class="grow"></div>
""")

# ============================================================ Highlight-Cover und Storys (1080 × 1920)
STORIES = {}


def hl(word, cls="lime", sheen=None, size=150):
    return slide(f"{cls} reel", f"""
<div class="grow"></div>
<p class="m0" style="font-size:{size}px;line-height:1;letter-spacing:-.035em;text-align:center">{word}</p>
<div class="grow"></div>
""", sheen=sheen)


STORIES["HL_Angebote"] = hl("Angebote")
STORIES["HL_Website"] = hl("Website")
STORIES["HL_Human_in_the_loop"] = hl("Human<br>in the loop", size=120)


def story(kicker, title, body, cta, cls="white", sheen=None):
    return slide(f"{cls} reel", f"""
{top(logo(), K(kicker))}
<div class="grow"></div>
<p class="h3 m0" style="max-width:8ch">{title}</p>
<p class="h6" style="margin-top:56px;max-width:19ch">{body}</p>
<div class="rule" style="margin-top:72px"></div>
<p class="h6" style="margin-top:36px;max-width:19ch">{cta}</p>
<div style="height:260px"></div>
""", sheen=sheen, extra_style="padding:220px 96px 96px")


STORIES["S_Angebot_01_Website"] = story("Angebot 01", "Website. Kostenlos.", "Für Kundinnen und Kunden. Gebaut mit KI, gestaltet von mir.", "Schreiben Sie mir »Website«.")
STORIES["S_Angebot_02_KI-Sichtbarkeit"] = story("Angebot 02", "KI-Sicht&shy;barkeit.", "Was ChatGPT, Gemini und Perplexity über Sie sagen, und die Korrekturen.", "Schreiben Sie mir »Check«.")
STORIES["S_Angebot_03_Bildwelt"] = story("Angebot 03", "Bildwelt<br>mit KI.", "Ihre echten Fotos, einheitlich bearbeitet, in allen Formaten.", "Schreiben Sie mir »Bilder«.")
STORIES["S_Angebot_04_Agenten"] = story("Angebot 04", "KI-Agenten.", "Ein Agent, ein klarer Job. Sie geben frei.", "Schreiben Sie mir »Agent«.")
STORIES["S_Gastro-Paket"] = story("Für Gastronomie", "Das Gastro-Paket.", "Website, Speisekarte, Fotos, Bewertungen, KI-Sichtbarkeit.", "Schreiben Sie mir »Gastro«.", cls="lime")
STORIES["S_Human_in_the_loop"] = story("Human in the loop", "Martin Schweppe.", "Diplom-Designer. Die KI macht die Routine, ich entscheide, was rausgeht.", "grafitecture.de", cls="lime")


if __name__ == "__main__":
    import sys
    allp = {**POSTS}
    only = sys.argv[1:] or None
    run(allp, only)

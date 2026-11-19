"""Paket 3: Reihenfolge, Captions, Alt-Texte, Highlights. Schreibt 00_PLAN.md und je Beitrag Text.txt."""
import pathlib, shutil, json

OUT = pathlib.Path("/home/claude/ig3/out")
PKG = pathlib.Path("/home/claude/ig3/PAKET_3")

KI_FOTO = "Bild: eigenes Foto, bearbeitet mit KI (Higgsfield)."

# Reihenfolge beim Posten (01 zuerst). Im Profil steht 20 oben links.
PLAN = [
    ("K7", "Karussell", "4 von 10 fragen die KI nach dem Restaurant",
     "Wo esse ich heute Abend gut? 4 von 10 Menschen in Deutschland suchen lokale Geschäfte inzwischen mit KI. "
     "Und fast jeder Zweite, der einer KI-Empfehlung folgt, geht essen.\n\n"
     "Die gute Nachricht: 96 % prüfen nach, fast die Hälfte auf der Website des Anbieters. Die KI empfiehlt, Ihre Website überzeugt.\n\n"
     "Mein Angebot: der KI-Sichtbarkeits-Check für Ihr Lokal. Schreiben Sie mir »Check«.\n\n"
     "Quelle: Yext, Consumer Search Behaviors Report 2026; t3n, 4.8.2026.\n"
     "#MarkenMitKI #Gastronomie #KISuche #GEO #Mannheim",
     "Lime-Fläche mit großer Schrift: 4 von 10 suchen lokale Geschäfte inzwischen mit KI."),
    ("H1", "Karussell", "Human in the loop 01: Treppenhaus, Mannheim 2011",
     "Human in the loop · 01\n\nTreppenhaus in Mannheim, Januar 2011. Ornament ist Handschrift: Jede Kurve in diesem Geländer hat jemand entschieden.\n\n"
     "Neue Serie mit eigenen Fotos aus meinem Archiv. Die KI macht Licht, Farbe und Format. Motiv, Ausschnitt und Freigabe entscheide ich. "
     "Wischen Sie für das Original.\n\n" + KI_FOTO + "\n#MarkenMitKI #HumanInTheLoop #Design #Mannheim #Jugendstil",
     "Jugendstil-Treppenhaus mit grünem, geschwungenem Eisengeländer und brauner Holztür mit Glaseinsatz."),
    ("H2", "Einzelbild", "Human in the loop 02: Leuchtkasten B, Mannheim 2008",
     "Human in the loop · 02\n\nEin Buchstabe, drei Farben, von der Straße aus in einer Sekunde gelesen. Mannheim, März 2008.\n\n"
     "Werbung muss nicht laut sein. Nur klar.\n\n"
     "Bild: eigenes Foto, bearbeitet mit KI (Higgsfield): Licht, Farbe, Format, eine Person am Straßenrand entfernt.\n"
     "#MarkenMitKI #HumanInTheLoop #Werbung #Typografie #Mannheim",
     "Alter Leuchtkasten an einer Mannheimer Fassade: schwarzes B auf Orange in blauem Rahmen, darunter die Straße mit parkenden Autos."),
    ("R8", "Reel", "Reel: Mein Foto. Bewegt. (Wasserturm 2017)",
     "Mannheim, November 2017, der Wasserturm zur blauen Stunde. Mein Handyfoto, von der KI bewegt. Ob es bleibt, entscheide ich.\n\n"
     "Human in the loop: Die KI macht Licht, Format und Bewegung. Motiv, Ausschnitt und Freigabe mache ich.\n\n"
     "Video: eigenes Foto, bearbeitet und animiert mit KI (Higgsfield).\n#MarkenMitKI #HumanInTheLoop #Mannheim #Wasserturm #KIVideo",
     "Der Mannheimer Wasserturm in der Dämmerung, Laternen im Park leuchten, die Kamera fährt langsam heran."),
    ("K8", "Karussell", "GEO: Das neue SEO",
     "41 % der Entscheiderinnen und Entscheider haben den Begriff noch nie gehört: GEO, Generative Engine Optimization. "
     "Dabei glauben 58 %, dass Unternehmen Kunden verlieren, wenn sie in KI-Antworten nicht vorkommen.\n\n"
     "GEO heißt: nicht nur gefunden, sondern genannt werden. Mit klaren Fakten, strukturierten Daten und Einträgen, die übereinstimmen. SEO bleibt, GEO kommt dazu.\n\n"
     "Was sagt ChatGPT über Ihre Marke? Schreiben Sie mir »GEO«.\n\n"
     "Quelle: YouGov im Auftrag von Seokratie, 509 Entscheider; Retail-News, 2.8.2026.\n#MarkenMitKI #GEO #SEO #KISuche #Marketing",
     "Lime-Fläche mit dem Wort GEO in sehr großer Schrift."),
    ("R11", "Reel", "Reel: Vorher. Nachher. (sieben eigene Fotos)",
     "Sieben eigene Fotos von 2008 bis 2021, vorher und nachher. Die KI macht das Licht, das Motiv bleibt echt.\n\n"
     "Genau so arbeite ich mit Ihren Bildern: Bildwelt mit KI. Schreiben Sie mir »Bilder«.\n\n"
     "Bilder: eigene Fotos, bearbeitet mit KI (Higgsfield).\n#MarkenMitKI #HumanInTheLoop #Bildbearbeitung #Fotografie #Design",
     "Sieben Fotos wechseln vom Handy-Original zur bearbeiteten Fassung, eine Lime-Linie wischt von links nach rechts."),
    ("H3", "Einzelbild", "Human in the loop 03: 701, Mannheim 2016",
     "Human in the loop · 03\n\n701. Von Hand auf Glas gemalt, mit Kratzern und Notizen. Mannheim, 2016.\n\n"
     "Kein Template der Welt hätte das so gemacht. Genau deshalb merkt man es sich.\n\n"
     "Bild: eigenes Foto, bearbeitet mit KI (Higgsfield): Licht, Farbe, Format.\n#MarkenMitKI #HumanInTheLoop #Typografie #Werbung #Mannheim",
     "Große gelbe Ziffern 701 auf einer Schaufensterscheibe, mit Kratzern und kleinen Notizen."),
    ("K10", "Karussell", "56 % sehen KI-Slop. Fünf Regeln dagegen",
     "56 % sehen in Social Media oft oder sehr oft KI-Slop. Ihr größter Wunsch an Marken: KI-Inhalte nicht ohne Kennzeichnung posten.\n\n"
     "Meine fünf Regeln: kennzeichnen, echtes Material als Basis, eine Bildsprache, Quellen auf die Folie, ein Mensch gibt frei. "
     "Slop ist kein KI-Problem. Es ist ein Gestaltungsproblem.\n\n"
     "Quelle: Sprout Social, Q1 2026 Pulse Survey; 8.4.2026.\n#MarkenMitKI #Design #SocialMedia #KIContent #Branding",
     "Weiße Fläche mit großer Zahl: 56 % sehen in Social Media oft oder sehr oft KI-Slop."),
    ("K14", "Karussell", "Ein Foto. Sieben Formate.",
     "Aus einem guten Foto werden sieben Formate: Post, Story, Profilbild, Website, Plakat, Karte und ein kurzer Clip für Reels.\n\n"
     "Die KI schneidet zu, erweitert, bewegt und übersetzt. Ich wähle das eine Foto, das es wert ist. Bildwelt mit KI, Angebot 03. Schreiben Sie mir »Bilder«.\n\n"
     + KI_FOTO + "\n#MarkenMitKI #Bildwelt #Design #ContentSystem #Branding",
     "Titel Ein Foto. Sieben Formate., darunter das bearbeitete Foto eines Jugendstil-Treppenhauses."),
    ("R9", "Reel", "Reel: Was ich anbiete (vier Angebote)",
     "Vier Angebote, ein Ansprechpartner, klare Preise: 01 Website, kostenlos für Kundinnen und Kunden. 02 KI-Sichtbarkeit. "
     "03 Bildwelt mit KI. 04 KI-Agenten.\n\nDrei Sätze zu Ihrem Vorhaben reichen. Schreiben Sie mir »Angebot«.\n"
     "#MarkenMitKI #KIAgentur #Website #KIAgenten #Mannheim",
     "Typografisches Reel: die vier Angebote nacheinander auf Weiß und Lime."),
    ("R12", "Reel", "Reel: Drei Buchstaben. (BAR, Mannheim)",
     "Human in the loop · Reel\n\nB. A. R. 2010 hingen die drei Leuchtkästen am Haus in Mannheim. Heute leuchten sie in der Bar.\n\n"
     "Gute Gestaltung wird nicht alt, sie zieht um. Die KI hat das Licht der alten Fotos gemacht und das Format erweitert. Die Geschichte ist echt.\n\n"
     "Bilder: eigene Fotos, bearbeitet mit KI (Higgsfield): Licht, Farbe, Format, Kamerafahrt.\n"
     "#MarkenMitKI #HumanInTheLoop #Werbung #Typografie #Mannheim",
     "Reel: Ein senkrechtes Schild aus drei Leuchtkästen B, A, R an einer Mannheimer Sandsteinfassade, dann von oben gesehen, dann leuchtend an der Wand einer dunklen Bar."),
    ("H5", "Einzelbild", "Human in the loop 05: Spargel, Mannheim 2017",
     "Human in the loop · 05\n\nSpargelzeit in Mannheim, April 2017. Geschält, sortiert, bereit.\n\n"
     "Die beste Werbung für ein Restaurant ist die Saison. Wer sie zeigt, braucht kein Stockfoto. Echtes Produkt, echtes Foto, die KI macht nur das Licht.\n\n"
     "Bild: eigenes Foto (2017), bearbeitet mit KI (Higgsfield): Licht, Farbe, Format.\n"
     "#MarkenMitKI #HumanInTheLoop #Gastronomie #Spargelzeit #Mannheim",
     "Geschälter weißer Spargel mit zartrosa Spitzen, Stange an Stange in einer Kiste mit grünem Papier."),
    ("K9", "Karussell", "KI-Essen macht weniger Appetit (Studie 2026)",
     "87 Personen, 60 Bildpaare: Eine Studie der Universität Duisburg-Essen zeigt, KI-Bilder von Essen wirken weniger echt und machen weniger Appetit. "
     "Gesund und kalorienreich wurden sie gleich eingeschätzt.\n\n"
     "Für Ihre Speisekarte heißt das: Das Gericht bleibt echt, die KI macht das Licht. Bildwelt mit KI, schreiben Sie mir »Bilder«.\n\n"
     "Quelle: Diel u. a., Universität Duisburg-Essen / LVR-Universitätsklinik Essen, berichtet von dpa; tageskarte.io, 5.11.2026.\n"
     "#MarkenMitKI #Gastronomie #Foodfotografie #Speisekarte #Restaurant",
     "Weiße Fläche mit dem Satz KI-Essen macht weniger Appetit."),
    ("R7", "Reel", "Reel: Fragen Sie mal ChatGPT (Gastronomie)",
     "Wo esse ich heute Abend gut in Mannheim? Diese Frage stellen Ihre Gäste. Aber nicht mehr nur Google.\n\n"
     "Die KI antwortet mit dem, was sie über Sie findet: Website, Einträge, Bewertungen. Steht da das Richtige? "
     "Mein KI-Sichtbarkeits-Check findet es heraus. Schreiben Sie mir »Check«.\n\n"
     "Quelle: Yext, Consumer Search Behaviors Report 2026; t3n, 4.8.2026.\n#MarkenMitKI #Gastronomie #KISuche #ChatGPT #Mannheim",
     "Typografisches Reel: Eine Chat-Frage wird getippt, dann Zahlen und das Angebot KI-Sichtbarkeits-Check."),
    ("K12", "Karussell", "Das Gastro-Paket",
     "Das Gastro-Paket: Website kostenlos, Speisekarte in mehreren Sprachen, echte Fotos besser gemacht, Antworten auf Bewertungen "
     "(die KI entwirft, Sie geben frei) und der KI-Sichtbarkeits-Check.\n\n"
     "Warum jetzt: Fast jeder Zweite, der einer KI-Empfehlung folgt, geht essen. Ein Gespräch, ein Angebot mit klaren Preisen. Schreiben Sie mir »Gastro«.\n\n"
     "Quelle: Yext, Consumer Search Behaviors Report 2026; t3n, 4.8.2026.\n#MarkenMitKI #Gastronomie #Restaurant #Website #Mannheim",
     "Lime-Fläche mit dem Titel Das Gastro-Paket."),
    ("H6", "Karussell", "Human in the loop 06: Mise en place, Mannheim 2018",
     "Human in the loop · 06\n\nMise en place. Rote Laguiole-Messer für die Zweite Liebe, Mannheim, Januar 2018.\n\n"
     "In einer guten Küche liegt alles bereit, bevor der erste Gast kommt. So arbeite ich mit KI: "
     "Die Vorbereitung macht die Maschine. Angerichtet wird von Hand. Wischen Sie für das Original.\n\n" + KI_FOTO +
     "\n#MarkenMitKI #HumanInTheLoop #Gastronomie #Design #MiseEnPlace",
     "Viele Laguiole-Messer mit glänzend roten Griffen und Stahlklingen liegen kreuz und quer übereinander."),
    ("K13", "Karussell", "Warum Grafitecture?",
     "Sechs Gründe, KI mit einem Gestalter zu machen: 26 Jahre Gestaltung seit 2000 in Mannheim. Ein Ansprechpartner statt Ticket-System. "
     "Systeme statt Tool-Listen. Jedes Ergebnis geht über meinen Tisch. Der Code gehört Ihnen. Zahlen mit Quelle, KI-Inhalte gekennzeichnet.\n\n"
     "Die KI liefert Tempo. Ich liefere Urteil. Human in the loop ist Martin Schweppe.\n"
     "#MarkenMitKI #HumanInTheLoop #KIAgentur #Design #Mannheim",
     "Weiße Fläche mit dem Titel Warum Grafitecture?"),
    ("R10", "Reel", "Reel: Lesbar für Menschen und Maschinen (Website)",
     "Wer fragt die KI nach Ihnen? 48 % prüfen eine KI-Empfehlung danach auf der Website des Anbieters. "
     "Eine Website braucht heute klare Fakten, Daten, die Maschinen lesen, Tempo auf dem Handy und Gestaltung, die man wiedererkennt.\n\n"
     "Ihre neue Website, kostenlos für Kundinnen und Kunden. Schreiben Sie mir »Website«.\n\n"
     "Quelle: Yext, Consumer Search Behaviors Report 2026; t3n, 4.8.2026.\n#MarkenMitKI #Website #Webdesign #GEO #Mannheim",
     "Typografisches Reel über Websites, die für Menschen und KI lesbar sind."),
    ("K11", "Karussell", "Vier Angebote",
     "Vier Angebote, ein Ansprechpartner, klare Preise.\n\n01 Website, kostenlos für Kundinnen und Kunden. 02 KI-Sichtbarkeit: "
     "was ChatGPT, Gemini und Perplexity über Sie sagen. 03 Bildwelt mit KI: Ihre echten Fotos, besser gemacht. "
     "04 KI-Agenten: ein Agent, ein klarer Job.\n\nBei jedem Angebot steht dabei, was die KI macht und was ich entscheide. "
     "Schreiben Sie mir »Angebot«.\n#MarkenMitKI #KIAgentur #Website #KIAgenten #Mannheim",
     "Farbverlauf in Mint und Hellblau mit dem Titel Vier Angebote."),
    ("H7", "Einzelbild", "Human in the loop 07: Mannheim von oben, 2021",
     "Human in the loop · 07\n\nMannheim vom Fernmeldeturm aus, Oktober 2021. Der Neckar, ein Frachtschiff, die Stadt in Herbstfarben.\n\n"
     "Von hier oben sieht man, wie alles zusammenhängt. So sehe ich auch Marken: erst das Ganze, dann das Detail. "
     "Gestaltung aus Mannheim seit 2000. Human in the loop ist Martin Schweppe.\n\n"
     "Bild: eigenes Foto (2021), bearbeitet mit KI (Higgsfield): Licht, Spiegelung im Fenster entfernt, Format.\n"
     "#MarkenMitKI #HumanInTheLoop #Mannheim #Neckar #Design",
     "Blick vom Mannheimer Fernmeldeturm auf den Neckar mit Frachtschiff, Bahnlinie, Häuser mit roten Dächern und Bäume in Herbstfarben, darüber dunkle Wolken."),
]

HIGHLIGHTS = {
    "ANGEBOTE": ["Highlight-Cover/HL_Angebote.png", "Reel R9 Was ich anbiete", "Reel R7 Fragen Sie mal ChatGPT",
                 "Storys S_Angebot_01 bis 04 und S_Gastro-Paket", "alte Reels R3 (02:14) und R6 (Recherche-Agent)"],
    "WEBSITE": ["Highlight-Cover/HL_Website.png", "Reel R10 Lesbar für Menschen und Maschinen", "altes Reel R5 Website, Tag 1",
                "Story S2 Website kostenlos (Paket 2) oder S_Angebot_01_Website"],
    "HUMAN IN THE LOOP": ["Highlight-Cover/HL_Human_in_the_loop.png", "Reel R8 Mein Foto. Bewegt.", "Reel R11 Vorher. Nachher.", "Reel R12 Drei Buchstaben.",
                          "Story S_Human_in_the_loop", "altes Reel R2 Ich entscheide"],
}

import re as _re
def _safe(t):
    t = t.replace("ä","ae").replace("ö","oe").replace("ü","ue").replace("Ä","Ae").replace("Ö","Oe").replace("Ü","Ue").replace("ß","ss")
    t = t.replace("Reel: ", "").split(":")[0] if not t.startswith("Reel") else t.replace("Reel: ", "")
    t = _re.sub(r"\(.*?\)", "", t)
    t = _re.sub(r"[^A-Za-z0-9]+", "_", t).strip("_")
    return t[:36].strip("_")
FOLDER_NAMES = {p[0]: f"{i:02d}_{p[0]}_{_safe(p[2])}" for i, p in enumerate(PLAN, 1)}


def package():
    if PKG.exists():
        shutil.rmtree(PKG)
    PKG.mkdir(parents=True)
    lines = ["# Instagram Paket 3 · Stand 18.11.2026", "",
             "20 Beiträge: 10 Karussells, 6 Reels, 4 Einzelbilder. Neue Serie HUMAN IN THE LOOP mit eigenen Fotos (ohne Personen), "
             "mit Higgsfield bearbeitet (GPT Image 2.6; Clip R8 mit Kling 3.0).", "",
             "Reihenfolge beim Posten: 01 zuerst, 20 zuletzt. Im Profil steht 20 oben links. Raster: Raster-Vorschau_Paket3.png.", "",
             "| Nr | ID | Format | Beitrag |", "|---|---|---|---|"]
    for i, (pid, fmt, title, cap, alt) in enumerate(PLAN, 1):
        d = PKG / FOLDER_NAMES[pid]
        d.mkdir()
        if pid.startswith("R"):
            shutil.copy(OUT / "reels" / f"{pid}.mp4", d / f"{pid}_Reel.mp4")
            shutil.copy(OUT / "reels" / f"{pid}_mit_Titelbild_fuer_Canva.mp4", d / f"{pid}_Reel_mit_Titelbild_fuer_Canva.mp4")
            shutil.copy(OUT / "covers" / f"{pid}_Titelbild.png", d / f"{pid}_Titelbild.png")
        else:
            for f in sorted((OUT / pid).glob("*.png")):
                shutil.copy(f, d / f.name)
        (d / "Text.txt").write_text(f"{title}\n\nCaption:\n{cap}\n\nAlt-Text:\n{alt}\n")
        lines.append(f"| {i:02d} | {pid} | {fmt} | {title} |")
    lines += ["", "## Highlights (in der Instagram-App anlegen)", ""]
    for h, items in HIGHLIGHTS.items():
        lines.append(f"- **{h}**: " + "; ".join(items))
    lines += ["", "Highlights gehen nur in der App: Story posten (Reel teilen oder MP4/PNG als Story), dann im Profil auf + und Highlight anlegen, "
              "Cover aus Highlight-Cover wählen. Das alte Highlight ANGEBOT kann durch ANGEBOTE ersetzt werden.", "",
              "## Quellen", "",
              "- Yext, Consumer Search Behaviors Report 2026; t3n, 4.8.2026 (K7, K12, R7, R10)",
              "- YouGov im Auftrag von Seokratie, 509 Entscheider; Retail-News, 2.8.2026 (K8)",
              "- Diel u. a., Universität Duisburg-Essen / LVR-Universitätsklinik Essen; dpa via tageskarte.io, 5.11.2026 (K9)",
              "- Sprout Social, Q1 2026 Pulse Survey; 8.4.2026 (K10)", "",
              "## Fotos (Mediathek, ohne Personen)", "",
              "H1 Treppenhaus 18.1.2011 · H2 Leuchtkasten B 6.3.2008 (Person am Straßenrand per KI entfernt) · H3 701, 4.10.2016 · "
              "R12 BAR-Schild am Haus (Kameradatum 6.3.2008, laut Martin 2010) und in der Bar 21.8.2021 · H5 Spargel Mannheim 27.4.2017 · H6 Laguiole-Messer Zweite Liebe, Mannheim 8.1.2018 · H7 Mannheim vom Fernmeldeturm 23.10.2021 · "
              "R8 Wasserturm 15.11.2017. Originale in _arbeit/originale, Higgsfield-Fassungen in _arbeit/hf."]
    (PKG / "00_PLAN.md").write_text("\n".join(lines) + "\n")
    shutil.copy(OUT / "Raster-Vorschau_Paket3.png", PKG / "Raster-Vorschau_Paket3.png")
    (PKG / "Highlight-Cover").mkdir()
    (PKG / "Storys").mkdir()
    for f in (OUT / "stories").glob("*.png"):
        shutil.copy(f, PKG / ("Highlight-Cover" if f.name.startswith("HL_") else "Storys") / f.name)
    json.dump([{"nr": i, "id": p[0], "format": p[1], "title": p[2], "caption": p[3], "alt": p[4]} for i, p in enumerate(PLAN, 1)],
              open(PKG / "plan.json", "w"), ensure_ascii=False, indent=1)
    print("ok", len(PLAN))


if __name__ == "__main__":
    package()

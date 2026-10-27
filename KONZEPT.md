# Grafitecture Website · Konzept & Stand

Repository: https://github.com/grafitecture/grafitecture (Branch `main`, Vercel liefert `public/` aus)
Vercel: Projekt `grafitecture`, mit dem Repository verbunden, jeder Push auf `main` geht live auf https://grafitecture.vercel.app (per Vercel-Login geschützt). Domain grafitecture.de noch nicht verbunden.
Vorschau (privates Artifact): https://claude.ai/artifact/V21UNy1YJ9uLywDrYpKTT5
Quellcode: `src/body.html`, `src/styles.css`, `src/app.js`, `build.py`, `tools/`; Schrift, Logos, Kundenlogos und Icons in `assets/`.

## Version 3 (25.10.2026) · aktueller Stand

Änderungswünsche von Martin, umgesetzt:

- **Hero:** Zeile „Weniger Routine. Mehr Gestaltung.“, H1 „Marken mit KI.“ (bis 17.942rem), immer mit Umbruch nach „Marken“ bzw. „Brands“, auch im Vorschaubild für Links, Lead „Ich baue KI-Systeme, die für Ihre Marke arbeiten.“, kurzer Text, zwei Buttons. Der Hero füllt den ersten Bildschirm, seit 25.10. als Fläche in Lime (siehe Nachträge).
- **Farben:** #435960 und Weiß (Kontrast 7,4 : 1), dazu seit 25.10. ein Akzent in Lime #dafd55 (siehe Nachträge). Keine Tönungen, keine Transparenzen. Hero und Footer sind Lime-Flächen; die Hero-Fläche changiert seit 26.10. zusätzlich durch Neongelb, Mint und Aqua (siehe Nachträge).
- **Logo:** `LOGO_GT_2026.svg` im Kopf und im Footer (der Footer ist seit 25.10. Lime, das weiße Logo wird nicht mehr gebraucht), immer genauso groß wie das Logo im Kopf. Aus dem A4-Artboard auf die Wortmarke zugeschnitten (ohne „tinytecture“), inline eingebunden.
- **Kundenlogos:** aus `Desktop/CLAUDE_GRAFITECTURE/KUNDENLOGOS` (27 Logos, weiß auf transparent). Umgefärbt in #435960, auf das Logo zugeschnitten, halbtransparente Teile (z. B. „.com“ bei flaeshapp) auf volle Deckkraft gebracht. Größen optisch ausgeglichen (gleiche Fläche, leichte Korrektur nach Schwärzung) und auf Martins Wunsch auf die Hälfte verkleinert, Raster 2/3/5 Spalten ohne Zellrahmen. Verlinkt, wo eine Website bekannt ist.
- **Stadtplan-Gedanke verworfen:** keine Blattnummern, kein Grundriss, kein Bauzeitenplan, keine Maßlinien, kein Siegel, kein Nordpfeil.
- **Gestaltung:** ruhig und einfach. Große Weißflächen (Abstand zwischen Abschnitten bis 17.942rem), große Headlines (h2 bis 11.089rem), Listen nur mit feinen Linien. Ablauf als nummerierte Schritte 01–05.
- **Schrift und Skala** unverändert aus V2: Google Sans, Goldener Schnitt mit clamp (h1 17.942rem · h2 11.089rem · h3 6.854rem · h4 4.236rem · h5 2.618rem · h6 1.618rem · p 1rem · small 0.618rem · 0.382rem).

### Nachträge 25.10.2026

- Kundenlogos halb so groß; beim Darüberfahren eine kleinere farbige Fläche hinter dem Logo.
- Leads mit festem Umbruch: „KI-Websites, Agenten und Content-Systeme. / Auf dem Fundament …“ und „Vom ersten Gespräch zum laufenden System, / in fünf klaren Schritten.“ (DE und EN, ab 560 px immer zwei Zeilen).
- Buttons, Fotos und die Hover-Fläche der Kundenlogos mit ganz leichter Rundung an allen vier Ecken (4 px).
- Fotos von Martin (mit Higgsfield bearbeitet): Porträt in „Über mich“ über den Eckdaten, Hauseingang neben „Bereit?“ im Kontakt. In Farbe, ohne Rahmen.
- **Akzentfarbe Lime #dafd55 statt Pink** (vorher #E0187A), immer der volle Ton: keine Abstufung, keine Tönung, keine Transparenz. Nichts wird unterlegt, Schrift und Logo selbst sind Lime. Lime-Schrift auf Weiß hat nur 1,2 : 1 Kontrast; so von Martin gewünscht. Schrift auf einer Lime-Fläche ist immer #435960 (6,4 : 1), nie Weiß.
  - Alle großen Headlines wieder in #435960 wie die übrige Schrift („Marken mit KI.“, „Was ich baue“, „Ich bin Martin.“, „So läuft’s“, „Referenzen“, „Bereit?“, Titel von Impressum und Datenschutz). Pink und Lime waren ausprobiert.
  - Ab und zu zieht eine Farbwelle in Lime durch die Headlines der Abschnitte und von Impressum/Datenschutz (nicht durch das H1 auf der Lime-Fläche): ein Band im vollen #dafd55 mit kurzen weichen Kanten läuft in 2,4 s von links nach rechts durch die Schrift. Erstmals kurz nachdem eine Headline ins Bild kommt, danach alle 8–14 Sekunden, solange sie sichtbar ist. Bei „Bewegung reduzieren“ keine Welle.
  - Alle Mouse-over-Zustände in Lime: Schrift und Logo werden #dafd55 (Links, Navigation, Menü, E-Mail-Adresse, Impressum, Datenschutz, Sprach- und Menü-Schalter, Logo im Kopf). Buttons füllen sich Lime mit Schrift in #435960; Kundenlogos bekommen eine kleinere Lime-Fläche und bleiben #435960. E-Mail-Adresse, Impressum und Datenschutz ohne Unterstreichung.
  - Auf Touch-Geräten (ohne Maus) gibt es keine Hover-Zustände, damit nach einem Tipp nichts Lime hängen bleibt.
- **Hero und Footer in Lime (25.10.):** Beide Bereiche sind jetzt Flächen im vollen #dafd55, Schrift, Linien und Logo in #435960 (6,4 : 1). Kein Bild und keine Animation im Hero; der Hero-Film (erst die Hand auf Papier, dann die Collage mit Pantone-Chips) ist entfernt, er liegt in der Git-Historie. Im Footer jetzt das dunkle Logo. Mouse-over auf den Lime-Flächen: Schrift und Footer-Logo werden weiß, die Hero-Buttons füllen sich weiß mit Schrift in #435960. Der Bildnachweis im Impressum ist mit dem Film entfallen.

- **„So läuft’s“ und „Bereit?“ in Lime (26.10.):** Beide Abschnitte haben jetzt vollflächig den Hintergrund #dafd55 wie Hero und Footer; Schrift und Linien #435960. „Bereit?“ geht nahtlos in den Lime-Footer über. Mouse-over dort wie im Hero: Schrift weiß, Buttons füllen sich weiß. Die Farbwelle läuft nur noch durch die Headlines auf Weiß.

- **Kennzahlen entfernt (26.10.):** Der Block „26 Jahre Gestaltung / 27 Referenzen / 24/7 Autonomer Betrieb“ ist raus. Auf „So läuft’s“ (Lime) folgen direkt die Referenzen auf Weiß.

- **Changierende Hero-Fläche (26.10.):** Nur die Fläche des Hero changiert, ganz langsam und unauffällig, in grellen, frischen Farben: Vier weiche Farbfelder ziehen über das Lime und wandern dabei durch Lime #dafd55, Neongelb #fff200, Mint #4dffb8 und Aqua #57f5ff. Ein Farbwechsel dauert seit 27.10. etwa 24 s (vorher 38 s, auf Martins Wunsch etwas schneller), die Felder brauchen 1 bis 1½ Minuten für eine Bewegung; nach dem Laden blendet das Farbspiel in 4 s aus dem reinen Lime ein. Die Schrift #435960 bleibt auf jeder Farbe mindestens 5,5 : 1 lesbar (gemessen über zwei volle Farbumläufe). Ohne Higgsfield gebaut: Ein Video hätte bei so weichen Verläufen Farbstufen und wäre viel größer; im Code bleibt der Verlauf sauber und kostet nur wenige Millisekunden Rechenzeit. Kleines Pause-Symbol rechts neben „Weniger Routine. Mehr Gestaltung.“ (Pflicht für Barrierefreiheit). Bei „Bewegung reduzieren“ und ohne JavaScript bleibt der Hero reines Lime; „So läuft’s“ und „Bereit?“ bleiben unverändert.
  - **Auch im Footer (26.10., Martin):** Der Footer changiert genauso, zeitlich versetzt zum Hero. Zu seiner Oberkante hin läuft die Farbe über die obere Hälfte ins reine Lime aus, so geht „Bereit?“ weiterhin nahtlos in den Footer über; die Farben steigen von unten auf. Ein zweites Pause-Symbol sitzt rechts neben dem Footer-Logo; beide Symbole halten das Farbspiel an beiden Stellen an. Das Farbspiel im Footer blendet ein, sobald er ins Bild kommt. Kontrast auch hier mindestens 5,5 : 1.

- **Hero auf dem Smartphone (27.10.):** „Weniger Routine. Mehr Gestaltung.“ bricht nie um; auf sehr schmalen Geräten (unter 380 px) mit etwas weniger Laufweite, damit die Zeile bis 320 px neben das Pause-Symbol passt. „Marken mit KI.“ steht auf dem Smartphone etwa 40 px höher, näher an der Kopfzeile (Abstand 4,236rem statt 6,854rem); dadurch sind bei 390 × 844 beide Buttons im ersten Bildschirm. Tablet und Desktop unverändert.

- **Leistungen auf dem Smartphone (27.10.):** Unter 760 px Breite stehen bei „Was ich baue“ nur noch die sechs Überschriften, die Beschreibungen sind ausgeblendet. Auf Tablet und Desktop bleiben Überschrift und Beschreibung wie bisher.

- **Linien-Animation im Hero wieder entfernt (26.10.):** Eine Animation nur aus 1-px-Linien (zwölf Stationen der Technikgeschichte vom Neandertaler am Feuer bis zum fliegenden Roadster, Zeichnungen mit Nano Banana Pro auf Higgsfield AI) war kurz online und ist auf Martins Wunsch wieder raus. Der Hero ist wieder die reine Lime-Fläche ohne Bild und Animation. Zeichnungen, Skript und Animation liegen in der Git-Historie (Commit 1310fc4).

### Rechtstexte (Stand Oktober 2026)

- **Impressum:** § 5 DDG, vertreten durch Martin Schweppe (Geschäftsführer), E-Mail, HRB 432625 Amtsgericht Mannheim, USt-IdNr. DE209730809, verantwortlich nach § 18 Abs. 2 MStV, Hinweis zur Verbraucherstreitbeilegung (VSBG), Markenhinweis zu den Kundenlogos. Entfernt: Haftungs- und Urheberrechtsfloskeln. Kein Link zur OS-Plattform (EU hat sie am 20.07.2025 abgeschaltet).
- **Wirtschafts-Identifikationsnummer:** ab Dezember 2026 Pflichtangabe, aber nur wenn keine USt-IdNr. angegeben ist. Die USt-IdNr. steht drin, damit ist das erfüllt.
- **Datenschutz, gekürzt auf 5 Punkte:** 1. Verantwortlicher. 2. Hosting bei Vercel Inc. (Logdaten, Art. 6 Abs. 1 lit. f, AV-Vertrag Art. 28, USA über EU-US Data Privacy Framework Art. 45 und Standardvertragsklauseln Art. 46). 3. Kontakt per E-Mail (Formular öffnet nur das Mailprogramm). 4. Keine Cookies, kein Tracking, keine Drittanbieter. 5. Rechte und Beschwerde beim LfDI Baden-Württemberg.
- **Cookie-Banner:** nicht nötig (§ 25 TDDDG). Die Seite setzt keine Cookies, speichert nichts im Browser und lädt nur von der eigenen Domain.

### Prüfung Hosting und Datenschutz (26.10.2026, Anmerkung von Sebastian Enders)

- **US-Anbieter in der Datenschutzerklärung:** war schon erledigt. Punkt 2 nennt Vercel Inc. mit US-Anschrift, die Logdaten, die Rechtsgrundlage, den AV-Vertrag und die Übermittlung in die USA (Data Privacy Framework, Art. 45, und Standardvertragsklauseln, Art. 46).
- **AV-Vertrag (DPA):** Vercels DPA gilt für Kunden im Pro- und Enterprise-Tarif und wird mit den Vertragsbedingungen wirksam, ohne Unterschrift (Fassung vom 17.03.2026, gültig ab 31.03.2026, mit den EU-Standardvertragsklauseln). Der kostenlose Hobby-Tarif ist nur für nicht-kommerzielle Nutzung; die Seite braucht Pro. Empfehlung: DPA als PDF zu den Unterlagen legen (vercel.com/legal/dpa).
- **Function Region:** seit 26.10. Frankfurt (`fra1`), festgelegt in `vercel.json` (`regions`). Die Seite hat keine Functions; die statischen Dateien liefert Vercels CDN vom Standort aus, der dem Besucher am nächsten ist.
- **Vercel Web Analytics, Speed Insights:** auf der Seite nicht eingebunden (kein Skript, keine Cookies, kein Speicher im Browser, nur Anfragen an die eigene Domain; geprüft). Die Content-Security-Policy lässt keine fremden Quellen zu.

### Technik

- Favicon, Apple-Touch-Icon und OG-Bild (1200 × 630) aus der Wortmarke, nur zwei Farben (`tools/render_assets.py`).
- `vercel.json`: Content-Security-Policy (nur eigene Domain), X-Frame-Options, nosniff, Referrer-Policy, Permissions-Policy; `/assets` ein Jahr cachebar, URLs mit Inhalts-Hash (`?v=…`), damit Änderungen trotzdem sofort ankommen. Function Region Frankfurt (`regions: ["fra1"]`).
- Kontaktformular: prüft Eingaben, öffnet das Mailprogramm mit vorbereiteter Nachricht und zeigt sie zusätzlich zum Kopieren. Ohne JavaScript öffnet es ebenfalls nur das Mailprogramm; nichts wird an einen Server geschickt.
- Geprüft mit Playwright bei 1920, 1512, 820 und 390 px, DE und EN: keine Konsolen- oder CSP-Fehler, kein horizontales Scrollen, nur #435960, Weiß und Lime im Einsatz, Menü, Overlays, Deep-Links und Formular funktionieren.

## Version 2 (21.10.2026)

Hero-Film „Flug über Mannheim“ (Higgsfield AI: GPT Image 2.5 + Kling 3.0), Google Sans, Goldener-Schnitt-Skala, Farben #5a6f7a und #01a6ff, Planmotive (Blattnummern, Grundriss, Bauzeitenplan, Maßstab, Nordpfeil). Film und Poster archiviert.

## Version 1 (20.10.2026)

Konzept „Planmappe“ mit Papierstadt-Animation, Big Shoulders/Archivo/Martian Mono, Ultramarin. Assets archiviert.

## Inhalte

- Struktur und Inhalte nach vibewith-ai.com, für Martin Schweppe, Diplom-Designer, neu geschrieben (Sie-Form, DE + EN).
- Keine erfundenen Kundenstimmen; stattdessen echte Referenzen (27 Kunden von grafitecture.de).

## Offene Punkte

- Telefonnummer im Impressum ergänzen (empfohlen).
- Übernommene Zusagen bestätigen: kostenloses 30-Minuten-Strategiegespräch, Antwort in der Regel innerhalb von 24 Stunden.
- Kundenlogo Zahnarztpraxis Theurer: In der weißen Vorlage überlagert der Zahn die Schrift. Bei Bedarf eine bessere Vorlage in den Ordner legen.
- Mit dem Livegang wird die alte Datenschutzerklärung auf grafitecture.de ersetzt (sie nennt eine fremde Firma, „Dots United GmbH“).
- Im Vercel-Dashboard bestätigen: Team „grafitecture“ im Pro-Tarif, Web Analytics und Speed Insights im Projekt aus.

## Build und Pflege

- `python3 build.py` erzeugt `public/` (Live-Seite, wird mit committet) und `vercel.json` sowie `dist/artifact/` (Vorschau mit eingebetteter Schrift und Logos, nicht im Repository). Danach committen und nach `main` pushen; Vercel veröffentlicht automatisch.
- Kundenlogos neu einlesen: Logos (weiß auf transparent) in `KUNDENLOGOS` legen, Zuordnung in `tools/prepare_clients.py` ergänzen, Skript ausführen, dann `build.py`. Reihenfolge, Namen und Links stehen in `CLIENTS` in `build.py`.
- Icons und OG-Bild neu erzeugen: `python3 tools/render_assets.py`.

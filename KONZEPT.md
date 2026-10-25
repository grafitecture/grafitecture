# Grafitecture Website · Konzept & Stand

Repository: https://github.com/grafitecture/grafitecture (Branch `main`, Vercel liefert `public/` aus)
Vercel: Projekt `grafitecture`, mit dem Repository verbunden, jeder Push auf `main` geht live auf https://grafitecture.vercel.app (per Vercel-Login geschützt). Domain grafitecture.de noch nicht verbunden.
Vorschau (privates Artifact): https://claude.ai/artifact/V21UNy1YJ9uLywDrYpKTT5
Quellcode: `src/body.html`, `src/styles.css`, `src/app.js`, `build.py`, `tools/`; Schrift, Logos, Kundenlogos und Icons in `assets/`.

## Version 3 (25.10.2026) · aktueller Stand

Änderungswünsche von Martin, umgesetzt:

- **Hero ohne Bild:** nur Typografie. Zeile „Weniger Routine. Mehr Gestaltung.“, H1 „Marken mit KI.“ (bis 17.942rem), immer mit Umbruch nach „Marken“ bzw. „Brands“, auch im Vorschaubild für Links, Lead „Ich baue KI-Systeme, die für Ihre Marke arbeiten.“, kurzer Text, zwei Buttons. Der Hero füllt den ersten Bildschirm, darüber viel Weiß.
- **Farben:** ausschließlich #435960 und Weiß (Kontrast 7,4 : 1). Keine Tönungen, keine Transparenzen. Hover und Fokus kehren um: Fläche #435960, Schrift und Logo weiß. Einzige farbige Fläche ist der Footer.
- **Logo:** `LOGO_GT_2026.svg` im Kopf, `LOGO_GT_weiss_2026.svg` im Footer, immer genauso groß wie das Logo im Kopf. Aus dem A4-Artboard auf die Wortmarke zugeschnitten (ohne „tinytecture“), inline eingebunden.
- **Kundenlogos:** aus `Desktop/CLAUDE_GRAFITECTURE/KUNDENLOGOS` (27 Logos, weiß auf transparent). Umgefärbt in #435960, auf das Logo zugeschnitten, halbtransparente Teile (z. B. „.com“ bei flaeshapp) auf volle Deckkraft gebracht. Größen optisch ausgeglichen (gleiche Fläche, leichte Korrektur nach Schwärzung) und auf Martins Wunsch auf die Hälfte verkleinert, Raster 2/3/5 Spalten ohne Zellrahmen. Verlinkt, wo eine Website bekannt ist.
- **Stadtplan-Gedanke verworfen:** keine Blattnummern, kein Grundriss, kein Bauzeitenplan, keine Maßlinien, kein Siegel, kein Nordpfeil.
- **Gestaltung:** ruhig und einfach. Große Weißflächen (Abstand zwischen Abschnitten bis 17.942rem), große Headlines (h2 bis 11.089rem), Listen nur mit feinen Linien. Ablauf als nummerierte Schritte 01–05, Kennzahlen 26 / 27 / 24/7.
- **Schrift und Skala** unverändert aus V2: Google Sans, Goldener Schnitt mit clamp (h1 17.942rem · h2 11.089rem · h3 6.854rem · h4 4.236rem · h5 2.618rem · h6 1.618rem · p 1rem · small 0.618rem · 0.382rem).

### Nachträge 25.10.2026

- Kundenlogos halb so groß; beim Darüberfahren kleinere Fläche in Pink, Logo weiß.
- H1 „Marken mit KI.“ / „Brands with AI.“ in Pink.
- Alle Mouse-over-Zustände in Pink (#E0187A, Kontrast 4,6 : 1 zu Weiß in beide Richtungen): Links und Navigation pink, Buttons pink mit weißer Schrift, Logo im Kopf pink. E-Mail-Adresse, Impressum und Datenschutz ohne Unterstreichung, beim Darüberfahren wird die Schrift pink (auch im dunklen Footer dasselbe Pink). Pink ist die einzige Farbe neben #435960 und Weiß.
- Leads mit festem Umbruch: „KI-Websites, Agenten und Content-Systeme. / Auf dem Fundament …“ und „Vom ersten Gespräch zum laufenden System, / in fünf klaren Schritten.“ (DE und EN, ab 560 px immer zwei Zeilen).
- Fotos von Martin (mit Higgsfield bearbeitet): Porträt in „Über mich“ über den Eckdaten, Hauseingang neben „Bereit?“ im Kontakt. In Farbe, ohne Rahmen.

### Rechtstexte (Stand Oktober 2026)

- **Impressum:** § 5 DDG, vertreten durch Martin Schweppe (Geschäftsführer), E-Mail, HRB 432625 Amtsgericht Mannheim, USt-IdNr. DE209730809, verantwortlich nach § 18 Abs. 2 MStV, Hinweis zur Verbraucherstreitbeilegung (VSBG), Markenhinweis zu den Kundenlogos. Entfernt: Bildnachweis Higgsfield (kein Film mehr), Haftungs- und Urheberrechtsfloskeln. Kein Link zur OS-Plattform (EU hat sie am 20.07.2025 abgeschaltet).
- **Wirtschafts-Identifikationsnummer:** ab Dezember 2026 Pflichtangabe, aber nur wenn keine USt-IdNr. angegeben ist. Die USt-IdNr. steht drin, damit ist das erfüllt.
- **Datenschutz, gekürzt auf 5 Punkte:** 1. Verantwortlicher. 2. Hosting bei Vercel Inc. (Logdaten, Art. 6 Abs. 1 lit. f, AV-Vertrag Art. 28, USA über EU-US Data Privacy Framework Art. 45 und Standardvertragsklauseln Art. 46). 3. Kontakt per E-Mail (Formular öffnet nur das Mailprogramm). 4. Keine Cookies, kein Tracking, keine Drittanbieter. 5. Rechte und Beschwerde beim LfDI Baden-Württemberg.

### Technik

- Favicon, Apple-Touch-Icon und OG-Bild (1200 × 630) aus der Wortmarke, nur zwei Farben (`tools/render_assets.py`).
- `vercel.json`: Content-Security-Policy (nur eigene Domain), X-Frame-Options, nosniff, Referrer-Policy, Permissions-Policy; `/assets` ein Jahr cachebar, URLs mit Inhalts-Hash (`?v=…`), damit Änderungen trotzdem sofort ankommen.
- Kontaktformular: prüft Eingaben, öffnet das Mailprogramm mit vorbereiteter Nachricht und zeigt sie zusätzlich zum Kopieren. Ohne JavaScript öffnet es ebenfalls nur das Mailprogramm; nichts wird an einen Server geschickt.
- Geprüft mit Playwright bei 1920, 1512, 820 und 390 px, DE und EN: keine Konsolen- oder CSP-Fehler, kein horizontales Scrollen, nur die zwei Farben im Einsatz, Menü, Overlays, Deep-Links und Formular funktionieren.

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

## Build und Pflege

- `python3 build.py` erzeugt `public/` (Live-Seite, wird mit committet) und `vercel.json` sowie `dist/artifact/` (Vorschau mit eingebetteter Schrift und Logos, nicht im Repository). Danach committen und nach `main` pushen; Vercel veröffentlicht automatisch.
- Kundenlogos neu einlesen: Logos (weiß auf transparent) in `KUNDENLOGOS` legen, Zuordnung in `tools/prepare_clients.py` ergänzen, Skript ausführen, dann `build.py`. Reihenfolge, Namen und Links stehen in `CLIENTS` in `build.py`.
- Icons und OG-Bild neu erzeugen: `python3 tools/render_assets.py`.

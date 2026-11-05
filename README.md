# grafitecture.de

Website der Grafitecture GmbH, Mannheim. One-Pager auf Deutsch und Englisch, statisch, ohne Cookies, ohne Tracking, ohne Drittanbieter.

## Aufbau

```
public/        fertige Website, wird von Vercel so ausgeliefert (nicht von Hand bearbeiten):
               / (Deutsch), /en (Englisch), /impressum, /datenschutz, /en/legal-notice, /en/privacy-policy
src/           Inhalt (body.html), Gestaltung (styles.css), Verhalten (app.js)
assets/        Schrift, Logo, Kundenlogos, Fotos, Icons, Vorschaubild für Links
build.py       baut public/ und vercel.json aus src/ und assets/
tools/         Hilfsskripte für Kundenlogos, Icons, Vorschaubilder, AVIF-Fotos, WOFF2-Schrift und den Farbkreis des Hero
scripts/       Prüfungen (npm run seo:check), lokaler Vercel-Nachbau (serve.py), IndexNow
seo/           Weiterleitungen (redirect-map.csv), Audit, Berichte, Inhalts-Empfehlungen
vercel.json    Vercel-Einstellungen: Ausgabeordner public/, Function Region Frankfurt, Sicherheits- und Cache-Header
KONZEPT.md     Gestaltung, Inhalte, Rechtstexte, offene Punkte
```

## Ändern und veröffentlichen

1. Text oder Gestaltung in `src/` ändern.
2. `python3 build.py` ausführen (nur Python-Standardbibliothek, keine Installation nötig).
3. `npm run seo:check` ausführen – muss grün sein.
4. Alles committen, auch `public/`, `vercel.json` und `seo/lastmod.json`, und nach `main` pushen. Vercel veröffentlicht automatisch; GitHub Actions prüft jeden Push (inkl. Lighthouse und axe) und nach dem Deployment die Live-Seite.

Eine Adresse ändern oder entfernen: neue Zeile in `seo/redirect-map.csv`, `python3 build.py`, `npm run seo:check`.

## Vercel einrichten (einmalig)

1. In Vercel „Add New → Project“ wählen und dieses Repository importieren. Die Einstellungen kommen aus `vercel.json`; Framework, Build-Befehl und Ausgabeordner müssen nicht eingetragen werden.
2. Das Projekt im Pro-Team anlegen. Der Hobby-Tarif ist nur für nicht-kommerzielle Nutzung, und Vercels Auftragsverarbeitungsvertrag, auf den die Datenschutzerklärung verweist, gilt für Pro.
3. Unter „Settings → Domains“ `grafitecture.de` und `www.grafitecture.de` hinzufügen und die angezeigten DNS-Einträge beim Domain-Anbieter setzen.
4. Web Analytics und Speed Insights ausgeschaltet lassen. Wer sie einschaltet, muss die Datenschutzerklärung ergänzen.
5. Die Function Region steht in `vercel.json` auf Frankfurt (`fra1`) und muss im Dashboard nicht eingestellt werden. Die Seite hat keine Functions; die statischen Dateien kommen vom nächstgelegenen CDN-Standort.

Die Content-Security-Policy erlaubt nur Inhalte von der eigenen Domain. Auf Vorschau-Deployments kann sie die Vercel-Toolbar blockieren; die Live-Seite ist davon nicht betroffen.

## Gestaltung

- Farben: #435960 und Weiß (Kontrast 7,4 : 1), auch für alle Headlines. Akzent Lime #dafd55 immer im vollen Ton für alle Mouse-over-Zustände: Schrift und Logo werden Lime (auf den Lime-Flächen Weiß), Buttons füllen sich Lime. Nichts wird unterlegt. Schrift auf Lime ist #435960. Alle Linien und Unterstreichungen sind Lime, auf den Lime-Flächen weiß (`--line`); nur der Fokusrahmen für die Tastatur bleibt #435960.
- Schrift: Google Sans, Skala im Goldenen Schnitt mit `clamp()` (Maximum bei 1920 px):
  h1 17.942rem · h2 11.089rem · h3 6.854rem · h4 4.236rem · h5 2.618rem · h6 1.618rem · p 1rem · small 0.618rem · 0.382rem.
- Große Headlines, große Weißflächen. Kundenlogos einfarbig in #435960.
- Hero, „So läuft’s“ und „Bereit?“ als vollflächige Lime-Flächen #dafd55 mit Schrift in #435960; der Hero ohne Bild. Der Footer ist weiß.
- Die Hero-Fläche changiert durch das ganze Farbspektrum, immer zwei Farben zugleich (Canvas hinter dem Inhalt, `sheen()` in `src/app.js`, Farbkreis aus `tools/colour_wheel.py`, Schrift überall mindestens 4,5 : 1); bei „Bewegung reduzieren“ bleibt sie reines Lime. Dasselbe Farbspiel liegt beim Öffnen von Impressum und Datenschutz neben dem weißen Blatt, auf derselben Zeitachse wie der Hero.

## Sprache und Links

Deutsch unter `/`, Englisch unter `/en` (seit 05.11.2026 je eine eigene Seite). Der Schalter DE/EN wechselt die Seite und behält den Abschnitt; alte Links `…/?lang=en` und `…/#en` führen auf `/en`.
Impressum und Datenschutz als Seiten: `/impressum`, `/datenschutz`, `/en/legal-notice`, `/en/privacy-policy`; `…/#impressum` öffnet weiterhin den Dialog auf der Startseite.

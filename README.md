# grafitecture.de

Website der Grafitecture GmbH, Mannheim. One-Pager auf Deutsch und Englisch, statisch, ohne Cookies, ohne Tracking, ohne Drittanbieter.

## Aufbau

```
public/        fertige Website, wird von Vercel so ausgeliefert (nicht von Hand bearbeiten)
src/           Inhalt (body.html), Gestaltung (styles.css), Verhalten (app.js)
assets/        Schrift, Logo, Kundenlogos, Fotos, Icons, Vorschaubild für Links
build.py       baut public/ und vercel.json aus src/ und assets/
tools/         Hilfsskripte für Kundenlogos, Icons und den Farbkreis des Hero (brauchen Pillow bzw. Playwright, colour_wheel.py nur Python)
vercel.json    Vercel-Einstellungen: Ausgabeordner public/, Function Region Frankfurt, Sicherheits- und Cache-Header
KONZEPT.md     Gestaltung, Inhalte, Rechtstexte, offene Punkte
```

## Ändern und veröffentlichen

1. Text oder Gestaltung in `src/` ändern.
2. `python3 build.py` ausführen (nur Python-Standardbibliothek, keine Installation nötig).
3. Alles committen, auch `public/` und `vercel.json`, und nach `main` pushen. Vercel veröffentlicht automatisch.

## Vercel einrichten (einmalig)

1. In Vercel „Add New → Project“ wählen und dieses Repository importieren. Die Einstellungen kommen aus `vercel.json`; Framework, Build-Befehl und Ausgabeordner müssen nicht eingetragen werden.
2. Das Projekt im Pro-Team anlegen. Der Hobby-Tarif ist nur für nicht-kommerzielle Nutzung, und Vercels Auftragsverarbeitungsvertrag, auf den die Datenschutzerklärung verweist, gilt für Pro.
3. Unter „Settings → Domains“ `grafitecture.de` und `www.grafitecture.de` hinzufügen und die angezeigten DNS-Einträge beim Domain-Anbieter setzen.
4. Web Analytics und Speed Insights ausgeschaltet lassen. Wer sie einschaltet, muss die Datenschutzerklärung ergänzen.
5. Die Function Region steht in `vercel.json` auf Frankfurt (`fra1`) und muss im Dashboard nicht eingestellt werden. Die Seite hat keine Functions; die statischen Dateien kommen vom nächstgelegenen CDN-Standort.

Die Content-Security-Policy erlaubt nur Inhalte von der eigenen Domain. Auf Vorschau-Deployments kann sie die Vercel-Toolbar blockieren; die Live-Seite ist davon nicht betroffen.

## Gestaltung

- Farben: #435960 und Weiß (Kontrast 7,4 : 1), auch für alle Headlines. Akzent Lime #dafd55 immer im vollen Ton für alle Mouse-over-Zustände: Schrift und Logo werden Lime (auf den Lime-Flächen Weiß), Buttons füllen sich Lime. Nichts wird unterlegt. Schrift auf Lime ist #435960.
- Schrift: Google Sans, Skala im Goldenen Schnitt mit `clamp()` (Maximum bei 1920 px):
  h1 17.942rem · h2 11.089rem · h3 6.854rem · h4 4.236rem · h5 2.618rem · h6 1.618rem · p 1rem · small 0.618rem · 0.382rem.
- Große Headlines, große Weißflächen. Kundenlogos einfarbig in #435960.
- Hero, „So läuft’s“ und „Bereit?“ als vollflächige Lime-Flächen #dafd55 mit Schrift in #435960; der Hero ohne Bild. Der Footer ist weiß.
- Die Hero-Fläche changiert durch das ganze Farbspektrum, immer zwei Farben zugleich (Canvas hinter dem Inhalt, `sheen()` in `src/app.js`, Farbkreis aus `tools/colour_wheel.py`, Schrift überall mindestens 4,5 : 1); bei „Bewegung reduzieren“ bleibt sie reines Lime.

## Sprache und Links

Standard ist Deutsch. Englisch über den Schalter DE/EN (am Desktop in der Kopfzeile, auf Handy und Tablet im Menü) oder per `…/#en` bzw. `…/?lang=en`.
Impressum und Datenschutz direkt verlinkbar: `…/#impressum`, `…/#datenschutz`.

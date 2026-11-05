# Ist-Audit grafitecture.de (Phase 1, 05.11.2026)

Stand: `main` @ 8229478 (= Produktion seit 05.11.2026, 07:11 UTC). Keine Änderungen am Code in dieser Phase.
Legende: ✅ erfüllt · ⚠️ teilweise / Verbesserung möglich · ❌ fehlt oder falsch

## Projekt-Parameter (ermittelt)

| Parameter | Wert | Quelle |
|---|---|---|
| DOMAIN | `https://www.grafitecture.de` | Vercel-Domains, Canonical |
| HOST | `www` (Apex `grafitecture.de` → 308 auf www, Vercel-Domain-Einstellung) | Vercel API |
| TRAILING_SLASH | entfällt praktisch (eine Seite `/`); alte Pfade mit und ohne `/` werden umgeleitet | vercel.json |
| HOSTING | `vercel` (Projekt `grafitecture_webseite`, Team Grafitecture, Pro) | Vercel API, CLAUDE.md |
| ALTE_DOMAIN | `keine` (alte WordPress-Seite lief auf derselben Domain) | 404-Log |
| ALTES_SYSTEM | `wordpress` (Theme „The7“ wahrscheinlich, `/wp-sitemap.xml`, `/author/…`, `/feed`) | 404-Log |
| ALTE_URL_QUELLEN | Vercel-404-Log 20.10.–05.11.2026; **kein** `seo-input/` (keine GSC-Exporte, keine alte Sitemap, kein Crawl) | – |
| SPRACHEN | `de,en` – beide Sprachen in **einer** HTML-Seite, umgeschaltet per JavaScript (`?lang=en`, `#en`) | src/body.html, app.js |
| TYP | `b2b` / überregional (Agentur), Standort Mannheim | Inhalt |
| KI_TRAINING | offen (Default `erlauben`) | – |
| BFSG_PFLICHTIG | voraussichtlich `nein` (B2B, kein Online-Shop/Buchung für Verbraucher); WCAG 2.2 AA wird trotzdem umgesetzt | Inhalt |

## Stack & Rendering

| Prüfpunkt | Status | Fundstelle / Beleg |
|---|---|---|
| Framework | ✅ kein Framework: statisches HTML, gebaut mit `python3 build.py` (nur Standardbibliothek) | build.py |
| Build / Output | ✅ `public/` wird committet, Vercel liefert ohne Build-Schritt aus (`framework: null`, `outputDirectory: public`) | vercel.json |
| Rendering | ✅ SSG – alles im ausgelieferten HTML, CSS und JS inline (96 KB unkomprimiert) | public/index.html |
| Inhalt ohne JavaScript | ⚠️ alle Texte im HTML, **aber** DE und EN stehen verschachtelt direkt nebeneinander. Ein Crawler ohne CSS liest „LeistungenServices“, „Markenmit KI.Brandswith AI.“ (111 verschmolzene Wörter gezählt). Impressum/Datenschutz sind ohne JS nicht erreichbar (Dialoge öffnen nur per Script) | lxml-Extraktion von public/index.html |
| Build reproduzierbar | ✅ `python3 build.py` erzeugt byte-identisches `public/` | `git status` nach Build leer |

## Phase 2 – URL-Architektur & Weiterleitungen

| Prüfpunkt | Status | Fundstelle / Beleg |
|---|---|---|
| Nur https, eine Host-Variante | ✅ Apex → www 308 (Vercel), http → https (Vercel) | Vercel-Domain-Einstellungen |
| Varianten in **einem** Hop | ⚠️ Apex + alter Pfad (`grafitecture.de/impressum`) = 2 Hops (Domain-Redirect, dann Pfad-Redirect); http + Apex + Pfad = 3 Hops. Live nicht prüfbar (Netzwerk-Allowlist), aus der Konfiguration abgeleitet | Vercel-Domain-Redirect + vercel.json |
| `/index.html` → `/` | ✅ 308 (`cleanUrls`) | lokaler Nachbau |
| Großbuchstaben | ⚠️ nur einzeln abgefangen (`/Impressum`, `/Kontakt` …), `/Blog`, `/BLOG` → 404 | vercel.json |
| Redirect-Map als Datei | ❌ kein `seo/redirect-map.csv`; Regeln stehen als Dict `REDIRECTS` in build.py (79 Einträge inkl. Slash-Varianten) | build.py |
| Alte URLs mit Nachfrage abgedeckt | ⚠️ abgedeckt: Impressum, Datenschutz, Kontakt, Über mich, WP-Sitemaps. **Offen:** `/arbeiten/internet` (alte Arbeiten-Seite), `/files/GT_ANFAHRT.pdf` (Anfahrtsplan), `/blog`, `/agb`, `/feed`, `/comments/feed`, `/category/uncategorised`, `/author-sitemap.xml` → 404 | seo/urls-alt.csv |
| Massen-Redirect auf Startseite | ✅ keiner (Ziele sind Abschnitte `/#…`, deren Inhalt auf der Startseite steht) | vercel.json |
| Ketten / Schleifen | ✅ keine im Pfad-Teil | lokaler Nachbau |
| Bot-Pfade (`/wp-admin/`, `/wp-login.php`, `/xmlrpc.php`) | ✅ 404, nicht umgeleitet | lokaler Nachbau |
| 410 für entfernte Inhalte | ❌ nicht umgesetzt (mit `redirects`/`headers`/`cleanUrls` in vercel.json nicht möglich, nur über `routes`) | – |
| Redirect-Test-Skript | ❌ fehlt | – |

## Phase 3 – Statuscodes & 404

| Prüfpunkt | Status | Fundstelle / Beleg |
|---|---|---|
| Echte 404 mit Status 404 | ✅ live: `GET /gibtsnicht-xyz` → `404 Not Found`, eigene Seite, `noindex` | Vercel-Fetch 05.11.2026 08:52 UTC |
| Inhalt 404-Seite | ✅ Meldung, Startseite, Kontakt, Footer mit Impressum/Datenschutz, gleiches Design | src/404.html |
| Interne Links ohne Redirect/404 | ✅ alle internen Links sind Anker auf der Seite (`#…`), Assets existieren | Build-Output |
| Tote externe Links | ⚠️ nicht prüfbar (kein Netzzugriff); 22 externe Kundenlinks, `http://42health.de/` und `http://detmers.de/` ohne https | build.py `CLIENTS` |

## Phase 4 – Indexierung & Crawling

| Prüfpunkt | Status | Fundstelle / Beleg |
|---|---|---|
| robots.txt | ⚠️ vorhanden, `Allow: /`, absolute Sitemap-Zeile; keine expliziten Gruppen für KI-Crawler | public/robots.txt (live 200) |
| Preview/Staging nicht indexierbar | ✅ `*.vercel.app` hinter Vercel-Login; Vercel setzt dort automatisch `x-robots-tag: noindex` (live geprüft) | Vercel-Fetch robots.txt auf vercel.app |
| Produktion ohne `noindex` | ✅ kein `noindex` auf `/`, kein `Disallow: /`; aber kein automatischer Check | – |
| sitemap.xml | ⚠️ vorhanden mit `/`, ohne `lastmod` | public/sitemap.xml |
| Canonical | ✅ selbstreferenzierend, absolut | public/index.html |
| Meta-Robots | ⚠️ nicht gesetzt (Default index,follow), `max-image-preview:large` fehlt | – |
| hreflang / Sprach-URLs | ❌ Englisch hat keine eigene URL; `<html lang="de">` fest, Englisch nur per JS | build.py |
| IndexNow | ❌ nicht eingerichtet | – |
| Google Search Console | ✅ URL-Präfix-Property bestätigt (Meta-Tag), Sitemap eingereicht (05.11.) | CLAUDE.md |
| Bing Webmaster Tools | ❌ unbekannt / nicht eingerichtet | – |

## Phase 5 – On-Page

| Prüfpunkt | Status | Fundstelle / Beleg |
|---|---|---|
| Title | ⚠️ 76 Zeichen (Ziel 50–60), Marke vorne | build.py `TITLE_DE` |
| Description | ⚠️ 167 Zeichen (Ziel 140–160) | build.py `DESC_DE` |
| Genau eine H1 | ✅ 1 | Browser-Check |
| Überschriften-Hierarchie | ✅ keine Sprünge (h1 → h2 → h3) | Browser-Check |
| Semantisches HTML | ✅ header, nav, ein main, section mit Überschrift, footer, Listen, dl | src/body.html |
| Links | ✅ echte `<a href>`, beschreibende Texte, `target=_blank` mit `rel="noopener noreferrer"` | src/body.html, build.py |
| Bilder: alt, Maße, srcset, lazy | ✅ alle `img` mit `alt`, `width`/`height`, `srcset`/`sizes`, `loading="lazy"` | build.py |
| Bilder: modernes Format | ❌ Fotos nur JPEG (1280 px: 408 KB und 432 KB), Kundenlogos PNG | assets/photos |
| Open Graph / Twitter | ✅ og:title/description/image (1200×630, absolut)/url/type/locale/site_name, `summary_large_image` | public/index.html |
| Icons & Manifest | ⚠️ favicon.ico, SVG, 32 px PNG, apple-touch-icon 180×180 vorhanden; **kein** Web-Manifest (192/512), kein Icon in 48er-Vielfachem | public/ |
| Viewport, Schrift ≥ 16 px | ✅ | styles.css |

## Phase 6 – Strukturierte Daten

| Prüfpunkt | Status | Fundstelle / Beleg |
|---|---|---|
| JSON-LD serverseitig, gültig | ✅ parsebar | public/index.html |
| `@graph` mit `@id` | ❌ ein einzelnes Objekt `ProfessionalService` | build.py `ld` |
| Organization/LocalBusiness vollständig | ⚠️ name, url, email, image, logo (SVG), foundingDate, address, sameAs (Instagram). Fehlt: description, geo, Logo als Rasterbild; telephone/openingHours stehen nicht auf der Seite (nicht erfinden) | build.py |
| WebSite, WebPage | ❌ fehlen | – |
| Person (Martin Schweppe) | ⚠️ nur als `employee` ohne `@id`, ohne `image`, ohne `sameAs` | build.py |
| Service-Markup für die 6 Leistungen | ❌ fehlt (Leistungen stehen sichtbar auf der Seite) | – |
| FAQ/HowTo/Bewertungen | ✅ keine (richtig so) | – |

## Phase 7 – KI-Lesbarkeit & KI-Crawler

| Prüfpunkt | Status | Fundstelle / Beleg |
|---|---|---|
| Explizite Crawler-Gruppen in robots.txt | ❌ nur `User-agent: *` | public/robots.txt |
| Firewall/Bot-Schutz | ✅ keine eigene Vercel-Firewall-Konfiguration (API: „config not found“), also keine Bot- oder KI-Sperren; Live-Test mit Crawler-User-Agents hier nicht möglich (Allowlist) | Vercel API 05.11.2026 |
| Inhalt ohne JS | ⚠️ siehe Stack: Sprachen verschmolzen | – |
| Erster Absatz beantwortet Wer/Was/Wo | ⚠️ Hero nennt Was (KI-Systeme für Marken) und Erfahrung, aber nicht Firmenname und Ort im Fließtext (stehen erst in „Über mich“/Footer) | src/body.html |
| NAP einheitlich | ✅ „Grafitecture GmbH, Rebenstr. 9a, 68309 Mannheim“ überall gleich; keine Telefonnummer | – |
| llms.txt | ❌ fehlt | – |
| `/.well-known/tdmrep.json` | ❌ 18 Anfragen, 404 (TDM-Vorbehalt nach EU-Urheberrecht, hängt an KI_TRAINING) | 404-Log |
| Kein Cloaking | ✅ | – |

## Phase 8 – Performance (Labor, lokal nachgebaut)

Messung: Chrome 153, Viewport 412×823, 4× CPU-Drosselung, 150 ms RTT, 1,44 Mbit/s – ähnlich Lighthouse mobil. Median aus 3 Läufen.

| Prüfpunkt | Status | Wert |
|---|---|---|
| LCP | ✅ | 592 ms (Element: Hero-Absatz, Text) |
| CLS | ✅ | 0 |
| TBT | ✅ | 0 ms |
| Gewicht erster Aufruf | ✅ | 95 KB, 3 Requests (HTML, Schrift, Favicon); Fotos lazy |
| Schrift | ⚠️ lokal, preload, `font-display: swap` ✅; Format WOFF (62 KB) statt WOFF2; kein metrisch angepasster Fallback | assets/fonts |
| CSS/JS | ✅ inline, kein render-blockierendes Laden, keine Drittanbieter | – |
| Caching | ✅ `/assets/*` `max-age=31536000, immutable` (mit Content-Hash `?v=`), HTML `max-age=0, must-revalidate` | vercel.json, live |
| Kompression | ✅ Brotli live (`content-encoding: br`) | Vercel-Fetch |
| Lighthouse | ⚠️ hier nicht ausführbar (npm/PageSpeed gesperrt) → in CI (GitHub Actions) | – |

## Phase 9 – Sicherheit & Header (live)

| Prüfpunkt | Status | Wert |
|---|---|---|
| HSTS | ⚠️ `max-age=63072000` (Vercel-Default), ohne `includeSubDomains` | live |
| CSP | ⚠️ gesetzt, nur `'self'`, aber `script-src 'unsafe-inline'` (ließe sich durch Hashes ersetzen) | live |
| X-Content-Type-Options, Referrer-Policy, Permissions-Policy, X-Frame-Options/frame-ancestors | ✅ | live |
| `/.well-known/security.txt` | ❌ fehlt | – |
| Interna nicht ausgeliefert | ✅ nur `public/` wird ausgeliefert (`/.git/config` → 404) | 404-Log |
| Formular | ✅ kein Server, `mailto:` – kein Spam-Risiko auf Serverseite | src/body.html |
| npm audit | ✅ entfällt (keine npm-Abhängigkeiten) | – |

## Phase 10 – Barrierefreiheit (automatisch, eigener Browser-Check statt axe)

Geprüft bei 390 px (DE) und 1512 px (EN), „Bewegung reduzieren“ an.

| Prüfpunkt | Status | Befund |
|---|---|---|
| Kontrast Text | ✅ 0 Verstöße (Hover-Lime auf Weiß ist Martins bewusste Entscheidung, nicht im Ruhezustand) | – |
| Namen von Links/Buttons/Bildern, Labels | ✅ 0 Verstöße | – |
| Landmarks, lang, eine H1, keine doppelten IDs | ✅ | – |
| Skip-Link | ✅ „Zum Inhalt springen“ | – |
| Sichtbarer Fokus | ❌ Formularfelder (Name, E-Mail, Nachricht): `outline: none`, Fokus nur als 2 px weiße Linie auf Lime (≈ 1,2 : 1) | styles.css `.field input` |
| Pause für Bewegung | ✅ Pause-Symbol (WCAG 2.2.2), reduzierte Bewegung respektiert | – |
| Zielgrößen ≥ 24 px | ✅ | – |
| Overlay-Widgets | ✅ keine | – |

## Phase 11 – Datenschutz-Technik

| Prüfpunkt | Status | Befund |
|---|---|---|
| Keine Drittanbieter beim ersten Aufruf | ✅ einziger Host: eigene Domain | Netzwerk-Mitschnitt |
| Kein Consent-Banner nötig | ✅ keine Cookies, kein Storage, kein Tracking | – |
| Impressum/Datenschutz mit einem Klick | ⚠️ ja (Footer, Menü), aber als Dialoge: ohne JavaScript nicht erreichbar, keine eigenen URLs | src/body.html |
| Vercel als US-Anbieter in der Datenschutzerklärung | ✅ genannt, DPA/DPF | src/body.html |

## Phase 12 – CI

| Prüfpunkt | Status |
|---|---|
| `seo:check`, GitHub Action, Lighthouse CI, axe | ❌ nichts vorhanden |

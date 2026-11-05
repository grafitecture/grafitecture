# Abschlussbericht „tech-max“ – grafitecture.de

Stand 05.11.2026 · Branch `tech-max` (noch **nicht** auf `main`, also noch nicht live) · Ausgangsstand `main` @ 8229478.
Martins Entscheidungen aus Phase 1: zwei Sprachseiten `/` und `/en` · KI-Training erlauben · Impressum/Datenschutz
zusätzlich als eigene Seiten · Title und Description unverändert.

## 1. Zusammenfassung

| | Vorher (main) | Nachher (tech-max) |
|---|---|---|
| Lighthouse mobil (CI, Median aus 3 Läufen) | nicht messbar (PageSpeed/npm hier gesperrt) | **100 / 100 / 100 / 100** auf `/`, `/en`, `/impressum` (Performance / Barrierefreiheit / Best Practices / SEO) |
| Labor mobil (4× CPU, langsames 4G, lokal) | LCP 592 ms · CLS 0 · TBT 0 · 95 KB | LCP 540 ms · CLS 0 · TBT 0 · 79 KB |
| Lighthouse simuliert (CI) | – | LCP 1,2–1,4 s · CLS 0 · TBT 0–43 ms (Budget 200) |
| axe (WCAG 2.2 A/AA), 6 Seiten × 2 Breiten | – | **0 Verstöße** |
| Indexierbare Adressen | 1 (`/`, beide Sprachen gemischt) | 6 (`/`, `/en`, 4 Rechtstext-Seiten), je mit hreflang |
| Wörter, die Crawler ohne CSS verschmolzen lesen | 111 („LeistungenServices“) | 0 inline (Rest nur zwischen Block-Elementen) |
| Weiterleitungen | 60 Regeln, Dict in build.py, ungetestet | 72 Regeln aus `seo/redirect-map.csv` (42 Zeilen), 69 Fälle automatisch geprüft, je **ein Hop** |
| Automatische Checks | keine | `npm run seo:check` + GitHub Actions bei jedem Push, Produktions-Check nach jedem Deployment |
| Design | – | **pixelgleich** (10 Screenshots DE/EN, 390–1920 px, Menü); nur die Fotos sind jetzt AVIF (Abweichung ausschließlich innerhalb der Fotoflächen) |

**Gefunden und behoben:** verschmolzene Sprachen im HTML, kein Englisch-URL/hreflang, Rechtstexte ohne JavaScript nicht
erreichbar, 9 alte Adressen ohne Ziel, kein Manifest/48-px-Icon, kein englisches Vorschaubild, JSON-LD ohne Graph,
keine KI-Crawler-Regeln, kein llms.txt/security.txt/IndexNow, Fotos nur JPEG, Schrift nur WOFF, CSP mit
`'unsafe-inline'` für Scripts, Formularfelder ohne Tastatur-Fokusrahmen, Überschriften-Sprung auf den neuen
Rechtstext-Seiten (von der CI gefunden), 4 Kundenlinks über Weiterleitung bzw. http.

## 2. Prüfpunkte mit Status und Beleg

Belege „lokal“: `python3 scripts/serve.py` (Nachbau von Vercel aus `vercel.json`) + `curl -I`. Belege „Preview“: echtes
Vercel-Deployment `grafitecturewebseite-ghjut12hy-grafitecture.vercel.app` (Commit f34d52c) über die Vercel-API.
Belege „CI“: GitHub Actions Runs 42018362914 (0596fb5) und 42019046176 (f0e2498), grün.

| Bereich | Prüfpunkt | Status | Beleg |
|---|---|---|---|
| 2 URLs | eine kanonische Adresse je Seite (https, www, ohne Schrägstrich) | ✅ | `curl -I /en/` → `308 Location: /en`; `/impressum.html` → `308 /impressum` |
| 2 URLs | Sprachen: `/` Deutsch, `/en` Englisch | ✅ | Preview `/en/` → 200, `<html lang="en">`, Title „Grafitecture · AI systems …“, kein „Was ich baue“ im HTML |
| 2 URLs | alte Adressen mit Nachfrage → passende Seite, ein Hop | ✅ | `seo/redirect-report.md`: 69 Fälle, 0 Fehler; z. B. `/arbeiten/internet` → `308 /#referenzen`, `/imprint` → `308 /en/legal-notice` |
| 2 URLs | keine Massen-Weiterleitung auf die Startseite | ✅ | Ziele sind Seiten bzw. Abschnitte mit passendem Inhalt |
| 2 URLs | Bot-Pfade nicht umgeleitet | ✅ | `curl -I /wp-login.php` → 404, `/.env` → 404 |
| 2 URLs | Apex + alter Pfad in einem Hop | ⚠️ | 2 Hops (Vercel-Domain-Redirect, dann Pfad); siehe Risiken |
| 2 URLs | 410 für entfernte Inhalte | ⚠️ | bewusst 404 (`/feed`, `/blog`, `/tag/…`); siehe Risiken |
| 3 Status | echte 404 mit Status 404 | ✅ | `curl -I /gibtsnicht` → `404`; live (main) 404 belegt am 05.11. 08:52 UTC |
| 3 Status | 404-Seite zweisprachig, unter `/en/…` englisch | ✅ | Browser-Test „404 under /en/ opens in English“ |
| 3 Status | interne Links ohne Weiterleitung/404 | ✅ | `seo/link-report.md`: 44 interne Ziele, alle direkt 200 |
| 3 Status | tote externe Links | ⚠️ | CI-Bericht: kaufhaus-ganz.de antwortet Bots mit 403, Instagram leitet Bots zum Login (beides normal); 4 Kundenlinks auf Endadresse umgestellt |
| 4 Index | robots.txt generiert, Sitemap-Zeile, nichts Nötiges gesperrt | ✅ | `public/robots.txt`; seo_check: 0 Fehler |
| 4 Index | Produktion nie noindex | ✅ | seo_check (Build) + Smoke-Test nach Deployment (`! grep x-robots-tag noindex`) |
| 4 Index | Previews/vercel.app noindex | ✅ | Preview-Header `x-robots-tag: noindex` |
| 4 Index | Sitemap: kanonisch, lastmod aus Inhaltsänderung, hreflang, Bilder | ✅ | `public/sitemap.xml`, `seo/lastmod.json`; Build zweimal → keine Änderung |
| 4 Index | Canonical selbstreferenzierend, hreflang wechselseitig + x-default | ✅ | seo_check prüft beides für alle 6 Seiten |
| 4 Index | Meta-Robots `index, follow, max-image-preview:large` | ✅ | alle indexierbaren Seiten |
| 4 Index | IndexNow | ✅ | Schlüsseldatei 200; `scripts/indexnow.py --all --dry-run`; Ping per Action nach Produktions-Deployment |
| 5 On-Page | Title/Description vorhanden, eindeutig | ✅ | seo_check: 0 Fehler |
| 5 On-Page | Title 50–60 / Description 140–160 Zeichen | ⚠️ | DE/EN-Title 76, DE-Description 167 – Martins Entscheidung (Warnung, kein Fehler) |
| 5 On-Page | genau eine H1, Überschriften ohne Sprünge | ✅ | seo_check + Lighthouse 100 |
| 5 On-Page | Bilder: alt, Maße, srcset, lazy, AVIF | ✅ | `<picture>` mit AVIF, JPEG-Rückfall |
| 5 On-Page | Open Graph auf allen Seiten, EN-Bild | ✅ | `og:image` absolut, `grafitecture-og-en.png` |
| 5 On-Page | Icons, Manifest | ✅ | `/site.webmanifest` 200, `favicon-48.png`, `icon-192/512.png` |
| 6 Daten | JSON-LD-Graph mit stabilen @ids, nur sichtbare Fakten | ✅ | ProfessionalService, WebSite, Person, WebPage, 6 × Service, BreadcrumbList; JSON parst (seo_check) |
| 6 Daten | Rich Results Test / validator.schema.org | ⚠️ | manuell nach dem Merge (To-do) |
| 7 KI | Such- und KI-Crawler explizit erlaubt, Training erlaubt | ✅ | `public/robots.txt`, Namen gegen ai-robots-txt abgeglichen |
| 7 KI | Firewall blockt keine Bots | ✅ | Vercel-API: keine Firewall-Regeln im Projekt |
| 7 KI | Inhalt ohne JavaScript, ohne Sprachgemisch | ✅ | lxml-Extraktion: `/` nur Deutsch, `/en` nur Englisch; Rechtstexte ohne JS erreichbar |
| 7 KI | llms.txt | ✅ | Preview `/llms.txt` 200 mit `x-robots-tag: noindex` |
| 7 KI | Inhalte für Antwortmaschinen | ⚠️ | Empfehlungen in `seo/content-empfehlungen.md` (nichts umgeschrieben) |
| 8 Perf. | Lighthouse ≥ 95, CWV grün, Budgets | ✅ | CI: 100 / 100 / 100 / 100, LCP ≤ 1,4 s, CLS 0, TBT ≤ 43 ms |
| 8 Perf. | Schrift lokal, WOFF2, Fallback mit size-adjust | ✅ | 47 statt 61 KB, Tabellen identisch (`tools/make_woff2.py`) |
| 8 Perf. | Caching | ✅ | `/assets/*` `max-age=31536000, immutable` mit Content-Hash |
| 9 Sicherheit | CSP ohne `'unsafe-inline'` für Scripts, COOP | ✅ | Preview-Header: `script-src 'self' 'sha256-…' 'sha256-…'`, `cross-origin-opener-policy: same-origin` |
| 9 Sicherheit | HSTS mit includeSubDomains | ⚠️ | Vercel-Standard `max-age=63072000` ohne includeSubDomains – wartet auf Martins Bestätigung |
| 9 Sicherheit | security.txt | ✅ | Preview `/.well-known/security.txt` 200, gültig bis 01.11.2027 |
| 9 Sicherheit | npm audit | ✅ | keine Abhängigkeiten (`found 0 vulnerabilities` in der CI) |
| 10 A11y | 0 axe-Fehler, Tastatur vollständig, sichtbarer Fokus | ✅ | CI: axe 0; Formularfelder mit Fokusrahmen per Tastatur |
| 10 A11y | 320 px ohne horizontales Scrollen, 200 % Zoom | ✅ | alle 7 Seiten `scrollWidth` 320 |
| 10 A11y | Sprachauszeichnung fremdsprachiger Passagen | ✅ | „Human in the loop.“ mit `lang="en-GB"` |
| 11 Datenschutz | keine Drittanbieter beim ersten Aufruf | ✅ | CI-Browser-Check: nur eigener Host |
| 11 Datenschutz | Impressum/Datenschutz von jeder Seite, als HTML-Seiten | ✅ | Footer auf allen Seiten, `/impressum`, `/datenschutz` 200 |
| 12 CI | `npm run seo:check`, GitHub Action, Lighthouse CI, axe | ✅ | Runs 42017215675, 42017800271, 42018362914 grün |

## 3. Geänderte Dateien

**Quellen**
- `build.py` – eine Seite je Sprache (`only_lang()`), Rechtstext-Seiten, Redirects aus CSV, hreflang, Meta-Robots, Open Graph auf allen Seiten, JSON-LD-Graph, Sitemap mit lastmod/hreflang/Bildern, robots.txt mit KI-Gruppen, llms.txt, Manifest, security.txt, IndexNow-Schlüssel, CSP mit Script-Hashes, COOP, AVIF-`<picture>`, WOFF2.
- `src/app.js` – Sprachschalter als Links (Abschnitt bzw. Menü bleiben erhalten), alte `?lang=en`/`#en` → `/en`, Tastatur-Erkennung für den Fokusrahmen der Formularfelder.
- `src/styles.css` – Sprachlinks im Look der Buttons, Rechtstext-Seite, `picture`, Schrift-Fallback mit Metriken, Fokusrahmen der Felder, `.legal-body` auch für h2.
- `src/body.html` – nur Markup: Zeilenumbrüche nach den Footer-Beschriftungen und zwischen Impressum/Datenschutz (unsichtbar), `lang="en-GB"` um „Human in the loop.“. Kein sichtbarer Text geändert.
- `src/404.html` – Kommentar (englische Links).
- `tools/render_assets.py` (Icons 48/192/512, EN-Vorschaubild, Logo-PNG), neu `tools/encode_photos.py`, `tools/make_woff2.py`.
- Neue Assets: `assets/icons/favicon-48.png`, `icon-192.png`, `icon-512.png`, `assets/og/grafitecture-og-en.png`, `assets/logo/grafitecture-logo.png`, `assets/photos/*.avif`, `assets/fonts/GoogleSans-latin-wght.woff2`.

**Prüfung und Betrieb:** `package.json` (nur Skripte), `scripts/run-checks.mjs`, `seo_check.py`, `check-links.mjs`, `check-redirects.mjs`, `browser-check.mjs`, `serve.py`, `indexnow.py`, `lighthouse_summary.py`, `lighthouserc.json`, `.github/workflows/seo.yml`, `deployed.yml`, `.gitignore`.

**Dokumentation:** `CLAUDE.md` (Abschnitt „SEO- & Technik-Standards (nicht verhandelbar)“), `README.md`, `KONZEPT.md`, `seo/` (AUDIT, REPORT, redirect-map.csv, lastmod.json, urls-alt/neu, Berichte, content-empfehlungen.md).

**Generiert:** `public/` (neu: `en.html`, `impressum.html`, `datenschutz.html`, `en/legal-notice.html`, `en/privacy-policy.html`, `llms.txt`, `site.webmanifest`, `.well-known/security.txt`, IndexNow-Datei, Icons), `vercel.json`.

**Alle Textänderungen einzeln** (sichtbare Seitentexte: keine)

| Wo | Neu / geändert | Text |
|---|---|---|
| `/en` Meta-Description | neu (fehlte) | „Martin Schweppe, graduate designer, builds AI systems for brands: AI websites, agents, content engines and automation. Grafitecture GmbH, Mannheim, since 2000.“ |
| `/en` og:title, og:image:alt | neu | „Grafitecture · Brands with AI. I build AI systems that work for your brand.“ / „Grafitecture: Brands with AI. Martin Schweppe, graduate designer, Mannheim“ |
| EN-Vorschaubild | neu | „Brands / with AI.“, „Martin Schweppe, graduate designer · Mannheim“ |
| `/impressum` Title + Description | neu | „Impressum · Grafitecture GmbH, Mannheim“ / „Impressum der Grafitecture GmbH, Mannheim: Anschrift, Vertretung durch Martin Schweppe, Handelsregister HRB 432625 und Umsatzsteuer-Identifikationsnummer.“ |
| `/datenschutz` Title + Description | neu | „Datenschutz · Grafitecture GmbH, Mannheim“ / „Datenschutzerklärung der Grafitecture GmbH: Hosting bei Vercel, Kontakt per E-Mail, keine Cookies und kein Tracking, Ihre Rechte nach der DSGVO.“ |
| `/en/legal-notice` Title + Description | neu | „Legal notice · Grafitecture GmbH, Mannheim“ / „Legal notice of Grafitecture GmbH, Mannheim, Germany: address, managing director Martin Schweppe, commercial register HRB 432625 and VAT identification number.“ |
| `/en/privacy-policy` Title + Description | neu | „Privacy policy · Grafitecture GmbH, Mannheim“ / „Privacy policy of Grafitecture GmbH, Mannheim: hosting by Vercel, contact by email, no cookies and no tracking, and your rights under the GDPR.“ |
| JSON-LD | neu | jobTitle EN „Managing Director, graduate designer (Dipl.-Des.)“, Katalog „Leistungen“/„Services“, Brotkrumen „Startseite“/„Home“; Leistungen und Beschreibung von der Seite übernommen |
| `/llms.txt` | neu | aus den Texten der deutschen Seite zusammengesetzt |
| Kundenlinks | geändert | 42health und Detmers `http` → `https`; Dentaid und Creating Smiles ohne `www.` (jeweils die Adresse, auf die die Seite selbst weiterleitet) |

## 4. Meine To-dos (nur Martin kann das)

1. **Freigabe:** Branch `tech-max` ansehen (Vorschau im Vercel-Dashboard, Deployment zum letzten Commit) und den Merge nach `main` freigeben – oder mir sagen, dass ich mergen soll.
2. **Direkt nach dem Merge:** In GitHub unter Actions → „Nach dem Deployment“ einmal manuell mit „IndexNow: alle Adressen“ starten (bei einem Fast-Forward-Merge sieht der automatische Lauf keine Änderung).
3. **Google Search Console:** Sitemap neu einreichen (jetzt 6 Adressen), URL-Prüfung für `/en` und `/impressum` anstoßen. Optional Domain-Property per DNS-TXT bei AutoDNS (deckt Apex, http und alle Subdomains ab).
4. **Bing Webmaster Tools:** Website über „Import aus Google Search Console“ anlegen, Sitemap prüfen.
5. **Google-Unternehmensprofil** mit exakt gleicher Anschrift (Grafitecture GmbH, Rebenstr. 9a, 68309 Mannheim); Links zu Profil und LinkedIn schicken → kommen als `sameAs` ins JSON-LD.
6. **Rich Results Test** und **validator.schema.org** für `/` und `/impressum` nach dem Merge (manuell).
7. **HSTS:** Bestätigen, dass alle Subdomains von grafitecture.de HTTPS können (z. B. Webmail beim Provider). Dann setze ich `includeSubDomains`.
8. **Vercel-Vorschau-Checks (optional):** Vercel → Settings → Deployment Protection → „Protection Bypass for Automation“ erzeugen und als GitHub-Secret `VERCEL_AUTOMATION_BYPASS_SECRET` hinterlegen.
9. **Apex in einem Hop (optional):** Wenn gewünscht, verlege ich die Weiterleitung `grafitecture.de → www` aus den Vercel-Domain-Einstellungen in `vercel.json` – dafür brauche ich deine Freigabe für die Domain-Einstellung.
10. **Inhalte:** `seo/content-empfehlungen.md` durchsehen (Fallbeispiele, FAQ, Preisrahmen, Telefonnummer).
11. **security.txt** läuft am 01.11.2027 ab; die CI meldet sich 30 Tage vorher.

## 5. Go-Live & Monitoring (Phase 13, angepasst: Umschaltung = Merge von `tech-max`)

**Vor dem Merge:** Baseline sichern – GSC „Leistung“ (Klicks, Impressionen, Top-Suchanfragen) als CSV exportieren und in `seo-input/` legen; Lighthouse-Werte stehen oben. DNS bleibt unverändert (keine TTL-Senkung nötig).

**Beim Merge:** Vercel deployt `main`; die Action „Nach dem Deployment“ prüft automatisch alle Seiten (200), eine Fantasie-URL (404), Apex (308), CSP, kein `noindex` und alle Weiterleitungen gegen https://www.grafitecture.de. Danach To-dos 2–4.

**Danach:** 14 Tage täglich GSC „Seiten“ (404, Soft-404, Weiterleitungsfehler, „Gecrawlt – zurzeit nicht indexiert“) – fehlende Adressen als Zeile in `seo/redirect-map.csv`. Vercel → Observability: Anfragen mit Status 404 und Bot-Zugriffe (Googlebot, Bingbot, OAI-SearchBot, Claude-SearchBot, PerplexityBot). Uptime-Monitoring einrichten (z. B. UptimeRobot oder Better Stack, Startseite + `/en`); das SSL-Zertifikat erneuert Vercel automatisch. Nach 4–8 Wochen Vergleich mit der Baseline.

## 6. Offene Risiken und Annahmen

- **Nicht live geprüft:** Diese Umgebung erreicht www.grafitecture.de nicht direkt (Netzwerk-Allowlist). Geprüft wurde lokal (Vercel-Nachbau), auf dem echten Vercel-Preview über die Vercel-API und in GitHub Actions. Die Produktion prüft nach dem Merge automatisch `deployed.yml`.
- **Alte URLs:** Das Inventar stammt aus dem Vercel-404-Log seit dem Launch am 20.10. (kein GSC-Export, keine alte Sitemap, kein Backlink-Export). Ältere Adressen mit Backlinks können fehlen → GSC-„Seiten“-Bericht nach dem Merge beobachten.
- **Apex + alter Pfad = 2 Hops** (`grafitecture.de/impressum.html` → www → `/impressum`). Für einen Hop müsste die Vercel-Domain-Einstellung geändert werden (To-do 9).
- **404 statt 410** für entfernte WordPress-Adressen: Google behandelt beides fast gleich; 410 ginge nur mit einem Umbau der vercel.json auf `routes`.
- **Title/Description** länger als die Richtwerte – Martins Entscheidung, Google kürzt in der Anzeige.
- **Sprachschalter lädt jetzt die andere Seite** (vorher Umschalten ohne Neuladen) – von Martin so entschieden; Abschnitt und offenes Menü bleiben erhalten.
- **HSTS ohne includeSubDomains**, bis Martin die Subdomains bestätigt.
- **Lighthouse/axe** laufen nur in GitHub Actions (hier keine Installation möglich); lokal ersetzt durch eigene Browser-Checks mit gleichen Prüfungen.
- **Annahme BFSG:** nicht pflichtig (B2B, kein Online-Shop oder Buchung für Verbraucher); WCAG 2.2 AA ist trotzdem erfüllt (axe 0, Lighthouse 100). Keine Rechtsberatung.
- **package.json im Repo:** Vercel baut weiterhin nichts (Preview geprüft: READY, ausgeliefert wird `public/`). Bitte kein `build`-Skript ergänzen.

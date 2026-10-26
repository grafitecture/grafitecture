# grafitecture.de – notes for Claude

Static one-pager for Grafitecture GmbH (Martin Schweppe, Diplom-Designer, Mannheim). German and English in one page.

## Build and deploy

- Edit `src/body.html`, `src/styles.css`, `src/app.js`; binary assets live in `assets/`.
- `python3 build.py` (standard library only) regenerates `public/` and `vercel.json`. Vercel serves `public/` as is; there is no build step on Vercel.
- Never edit `public/` by hand. Commit `public/` and `vercel.json` together with every source change.
- `dist/artifact/index.html` is the claude.ai artifact preview (font and client logos inlined, no mailto form action). It is not committed.
- Vercel project `grafitecture` is linked to this repository; pushing to `main` deploys to production (https://grafitecture.vercel.app, behind Vercel Authentication). The domain grafitecture.de is not connected yet; only connect it after Martin confirms.
- Privacy set-up after the note by Sebastian Enders (26.10.2026): `vercel.json` pins the function region to Frankfurt (`"regions": ["fra1"]`, set in `vercel_config()` in build.py; the site has no functions, static files come from the nearest CDN location). The team must stay on Vercel Pro (the DPA covers Pro and Enterprise; Hobby is non-commercial only). Keep Vercel Web Analytics and Speed Insights off; adding them or any other Vercel feature that loads a script needs the privacy policy updated first.

## Design rules (set by Martin, binding)

- Colours: #435960 and #FFFFFF, plus one accent, lime #dafd55 (`--lime`, Martin 25.10., replaced the earlier pink). No tints, no opacity-based colours. Exception: the two colour photos.
- Lime fields (#dafd55, full width) with #435960 type, lines and logo: the hero and the footer (Martin 25.10.), the process section „So läuft’s“ and the contact section „Bereit?“ (Martin 26.10.). They carry the class `is-lime`; the contact field runs straight into the lime footer. No image and no animation in the hero; the header stays white. The figures section (26 / 27 / 24/7) was removed on 26.10.; „Referenzen“ follows „So läuft’s“ with its normal top padding.
- The accent is always the full tone #dafd55: never a darker or lighter variant, no tint, no transparency. Text on a lime field is always #435960 (6.4:1), never white.
- Nothing is put behind type or logos (Martin 25.10.): no marker, no underlay. Martin chose lime type knowing it is only 1.2:1 on white.
- All main headlines are #435960 like the rest of the type (hero H1, the section headlines, the Impressum/Datenschutz titles; Martin 25.10., after trying pink and lime). Now and then a lime wave runs through the headlines on white (sections and Impressum/Datenschutz; not those on lime fields, where it would not show): `app.js` adds `.is-waving` for one 2.4 s pass, first 0.7 s after a headline comes into view, then every 8–14 s while it stays there; never with reduced motion or forced colours. The wave is a gradient clipped to the letters of the inline spans (mostly the full #dafd55, short soft edges); outside a pass the type is plain #435960.
- Every mouse-over on the whole page is lime, and nothing is put behind type or logos (Martin 25.10.): on white the type itself turns #dafd55 (links, nav, menu, e-mail, Impressum/Datenschutz, language and menu buttons) and the header logo turns #dafd55. Martin chose this knowing lime type on white is only 1.2:1 while hovered. Buttons, copy and close buttons fill lime with #435960 type; client logos get a smaller lime field and stay #435960. On the lime fields (`.is-lime`), where lime cannot show, the type and the footer logo turn white and buttons (incl. the copy button) fill white with #435960 type. The e-mail address and the Impressum/Datenschutz links are not underlined. All hover rules sit in one `@media (hover: hover)` block, so taps on touch screens leave nothing behind.
- Font: Google Sans, self-hosted (`assets/fonts`, Latin subset, weight 400–700).
- Type scale, golden ratio with clamp, maximum at 1920 px: h1 17.942rem, h2 11.089rem, h3 6.854rem, h4 4.236rem, h5 2.618rem, h6 1.618rem, p 1rem, small 0.618rem, 0.382rem.
- Calm and simple: large white space, large headlines, no city-map or floor-plan motifs.
- Logo: `assets/logo/grafitecture.svg` in the header and, since the footer is lime, also in the footer (`grafitecture-white.svg` is no longer used). Both always the same size (`--logo-h`).
- The H1 always breaks after the first word: "Marken / mit KI.", "Brands / with AI." (explicit `<br>`), also in the OG image.
- Buttons, photos and the lime hover field have a very slight rounding on all four corners (`--r` 4px); everything else stays square.
- Photos, as supplied by Martin: portrait in "Über mich" (left column above the facts), entrance photo next to "Bereit?" in the contact section. Files in `assets/photos` (640 and 1280 px), alt text in both languages via `data-alt-de`/`data-alt-en`.
- Fixed line breaks: services lead after "Content-Systeme." / "content systems.", process lead after the comma (class `lead-2l`, two lines from 560 px up).
- Client logos: one-colour #435960 PNGs made by `tools/prepare_clients.py` from white-on-transparent sources (Martin's folder `Desktop/CLAUDE_GRAFITECTURE/KUNDENLOGOS`). Display size is half of the balanced size (`--logo-k` in styles.css).

## Content rules

- Every visible text exists twice: `<span lang="de">…</span><span lang="en">…</span>`.
- `body.html` placeholders filled by build.py: `{{LOGO_DARK}}`, `{{LOGO_WHITE}}`, `{{ARROW}}`, `{{CLIENTS}}`, `{{CLIENT_COUNT}}` (currently unused), `{{IMG_PORTRAIT}}`, `{{IMG_DOOR}}`. Client names, order and links: `CLIENTS` in build.py.
- Impressum and Datenschutz are dialogs in body.html (status October 2026: § 5 DDG, § 18 Abs. 2 MStV, hosting Vercel). Keep the privacy policy short, and update it whenever a cookie, analytics, external font or other third-party service is added.
- No cookies, no tracking, no third-party requests; the CSP in vercel.json allows only 'self'.

## Before pushing

Check the page at 1920, 1512, 820 and 390 px in DE and EN: no console or CSP errors, no horizontal scrolling, only #435960, white and the lime accent in use, menu, dialogs and contact form working.

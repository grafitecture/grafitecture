# grafitecture.de – notes for Claude

Static one-pager for Grafitecture GmbH (Martin Schweppe, Diplom-Designer, Mannheim). German and English in one page.

## Build and deploy

- Edit `src/body.html`, `src/styles.css`, `src/app.js`; binary assets live in `assets/`.
- `python3 build.py` (standard library only) regenerates `public/` and `vercel.json`. Vercel serves `public/` as is; there is no build step on Vercel.
- Never edit `public/` by hand. Commit `public/` and `vercel.json` together with every source change.
- `dist/artifact/index.html` is the claude.ai artifact preview (font and client logos inlined, no mailto form action). It is not committed.
- Vercel project `grafitecture` is linked to this repository; pushing to `main` deploys to production (https://grafitecture.vercel.app, behind Vercel Authentication). The domain grafitecture.de is not connected yet; only connect it after Martin confirms.

## Design rules (set by Martin, binding)

- Colours: #435960 and #FFFFFF, plus one accent, lime #dafd55 (`--lime`, Martin 25.10., replaced the earlier pink). No tints, no opacity-based colours. Exceptions: the two colour photos and the grey hero film (below).
- The accent is used exactly as #dafd55, never a darker or lighter variant. Lime type on white would only reach 1.2:1, so on white the lime is a marker band behind the letters (a thick underline, `--mark`/`--mark-o`) and the type stays #435960 (6.4:1 on lime). Text on lime is always #435960, never white.
- All main headlines carry the lime marker (hero H1, the section headlines, the Impressum/Datenschutz titles).
- Every mouse-over on the whole page is lime: text links, nav, language and menu buttons get the marker band; the header logo gets the band behind the wordmark; buttons, copy and close buttons fill lime with #435960 type; client logos get a smaller lime field and stay #435960; on the dark footer the type and the footer logo turn lime. The e-mail address and the Impressum/Datenschutz links are not underlined. All hover rules sit in one `@media (hover: hover)` block, so taps on touch screens leave nothing lime behind.
- Font: Google Sans, self-hosted (`assets/fonts`, Latin subset, weight 400–700).
- Type scale, golden ratio with clamp, maximum at 1920 px: h1 17.942rem, h2 11.089rem, h3 6.854rem, h4 4.236rem, h5 2.618rem, h6 1.618rem, p 1rem, small 0.618rem, 0.382rem.
- Calm and simple: large white space, large headlines, no city-map or floor-plan motifs.
- Hero film (Martin 25.10., "AI with human in the loop"): a hand rests on white paper, fine grey lines flow around the fingertip. Very light greys only, silent, seamless 8.6 s loop behind the hero type, fading into the white page at the top and bottom (CSS mask). Files in `assets/hero` (1920 H.264 MP4, 1280 VP9 WebM fallback, grey poster), made with `tools/hero_film.py` from the Higgsfield clip (keyframe GPT Image 2.5, motion MiniMax H3). `app.js` loads it only after page load, never with reduced motion or save-data (the poster stays), pauses it out of view, and the "Film anhalten / Pause film" button in the hero top row stops it (WCAG 2.2.2; icon only below 560 px). On small screens the film is a band at the top of the hero. The Impressum names it under "Bildnachweis".
- Logo: `assets/logo/grafitecture.svg` in the header, `grafitecture-white.svg` in the footer. Both always the same size (`--logo-h`).
- The H1 always breaks after the first word: "Marken / mit KI.", "Brands / with AI." (explicit `<br>`), also in the OG image.
- Buttons, photos and the lime hover field have a very slight rounding on all four corners (`--r` 4px); everything else stays square.
- Photos, as supplied by Martin: portrait in "Über mich" (left column above the facts), entrance photo next to "Bereit?" in the contact section. Files in `assets/photos` (640 and 1280 px), alt text in both languages via `data-alt-de`/`data-alt-en`.
- Fixed line breaks: services lead after "Content-Systeme." / "content systems.", process lead after the comma (class `lead-2l`, two lines from 560 px up).
- Client logos: one-colour #435960 PNGs made by `tools/prepare_clients.py` from white-on-transparent sources (Martin's folder `Desktop/CLAUDE_GRAFITECTURE/KUNDENLOGOS`). Display size is half of the balanced size (`--logo-k` in styles.css).

## Content rules

- Every visible text exists twice: `<span lang="de">…</span><span lang="en">…</span>`.
- `body.html` placeholders filled by build.py: `{{LOGO_DARK}}`, `{{LOGO_WHITE}}`, `{{ARROW}}`, `{{CLIENTS}}`, `{{CLIENT_COUNT}}`, `{{IMG_PORTRAIT}}`, `{{IMG_DOOR}}`, `{{HERO_FILM}}`. Client names, order and links: `CLIENTS` in build.py.
- The artifact preview embeds the film poster; the two film files are published next to it as supporting files (`dist/artifact/assets/hero/`).
- Impressum and Datenschutz are dialogs in body.html (status October 2026: § 5 DDG, § 18 Abs. 2 MStV, hosting Vercel). Keep the privacy policy short, and update it whenever a cookie, analytics, external font or other third-party service is added.
- No cookies, no tracking, no third-party requests; the CSP in vercel.json allows only 'self'.

## Before pushing

Check the page at 1920, 1512, 820 and 390 px in DE and EN: no console or CSP errors, no horizontal scrolling, only #435960, white and the lime accent in use, menu, dialogs and contact form working, the hero film playing, pausing with its button and staying a still image with reduced motion. Playwright's Chromium has no H.264, so locally it plays the WebM fallback.

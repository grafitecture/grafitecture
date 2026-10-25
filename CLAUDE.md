# grafitecture.de – notes for Claude

Static one-pager for Grafitecture GmbH (Martin Schweppe, Diplom-Designer, Mannheim). German and English in one page.

## Build and deploy

- Edit `src/body.html`, `src/styles.css`, `src/app.js`; binary assets live in `assets/`.
- `python3 build.py` (standard library only) regenerates `public/` and `vercel.json`. Vercel serves `public/` as is; there is no build step on Vercel.
- Never edit `public/` by hand. Commit `public/` and `vercel.json` together with every source change.
- `dist/artifact/index.html` is the claude.ai artifact preview (font and client logos inlined, no mailto form action). It is not committed.
- Pushing to `main` deploys to production.

## Design rules (set by Martin, binding)

- Colours: only #435960 and #FFFFFF. No tints, no opacity-based colours; hover and focus invert the two.
- Font: Google Sans, self-hosted (`assets/fonts`, Latin subset, weight 400–700).
- Type scale, golden ratio with clamp, maximum at 1920 px: h1 17.942rem, h2 11.089rem, h3 6.854rem, h4 4.236rem, h5 2.618rem, h6 1.618rem, p 1rem, small 0.618rem, 0.382rem.
- Calm and simple: large white space, large headlines, no image in the hero, no city-map or floor-plan motifs.
- Logo: `assets/logo/grafitecture.svg` in the header, `grafitecture-white.svg` in the footer.
- Client logos: one-colour #435960 PNGs made by `tools/prepare_clients.py` from white-on-transparent sources (Martin's folder `Desktop/CLAUDE_GRAFITECTURE/KUNDENLOGOS`). Display size is half of the balanced size (`--logo-k` in styles.css).

## Content rules

- Every visible text exists twice: `<span lang="de">…</span><span lang="en">…</span>`.
- `body.html` placeholders filled by build.py: `{{LOGO_DARK}}`, `{{LOGO_WHITE}}`, `{{ARROW}}`, `{{CLIENTS}}`, `{{CLIENT_COUNT}}`. Client names, order and links: `CLIENTS` in build.py.
- Impressum and Datenschutz are dialogs in body.html (status October 2026: § 5 DDG, § 18 Abs. 2 MStV, hosting Vercel). Keep the privacy policy short, and update it whenever a cookie, analytics, external font or other third-party service is added.
- No cookies, no tracking, no third-party requests; the CSP in vercel.json allows only 'self'.

## Before pushing

Check the page at 1920, 1512, 820 and 390 px in DE and EN: no console or CSP errors, no horizontal scrolling, only the two colours in use, menu, dialogs and contact form working.

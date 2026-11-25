(() => {
  'use strict';
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => Array.from(r.querySelectorAll(s));
  const site = $('#site');
  if (!site) return;

  const MAIL = 'martin.schweppe@grafitecture.de';
  const T = {
    de: {
      title: 'Grafitecture · KI-Systeme für Marken · Martin Schweppe, Dipl.-Des., Mannheim',
      err: {
        name: 'Bitte geben Sie Ihren Namen ein.',
        email: 'Bitte geben Sie eine gültige E-Mail-Adresse ein.',
        message: 'Bitte schreiben Sie kurz, worum es geht.'
      },
      subject: 'Anfrage über grafitecture.de',
      call: 'Strategiegespräch',
      to: 'An', subj: 'Betreff'
    },
    en: {
      title: 'Grafitecture · AI systems for brands · Martin Schweppe, Dipl.-Des., Mannheim',
      err: {
        name: 'Please enter your name.',
        email: 'Please enter a valid email address.',
        message: 'Please tell me briefly what it is about.'
      },
      subject: 'Enquiry via grafitecture.de',
      call: 'Strategy call',
      to: 'To', subj: 'Subject'
    }
  };

  /* ---------------- language ----------------
     One page per language since 05.11.2026 (Martin): / carries only the German text, /en only the English one, so
     search engines and AI crawlers read clean text. There the DE/EN switch is a link to the other page: it keeps the
     section in view (/en#leistungen …), and an open menu opens again on the other page (#menu, see the menu below).
     The claude.ai preview still carries both languages and switches in place (buttons instead of links). */
  let lang = site.dataset.lang === 'en' ? 'en' : 'de';
  const inPlace = $$('button[data-set-lang]');
  function setLang(l) {
    lang = l === 'en' ? 'en' : 'de';
    site.dataset.lang = lang;
    document.documentElement.lang = lang;
    document.title = T[lang].title;
    inPlace.forEach((b) => b.setAttribute('aria-pressed', String(b.dataset.setLang === lang)));
    $$('img[data-alt-de]').forEach((img) => { img.alt = lang === 'de' ? img.dataset.altDe : img.dataset.altEn; });
    const call = $('#call-btn');
    if (call) call.href = 'mailto:' + MAIL + '?subject=' + encodeURIComponent(T[lang].call);
    $$('.field.invalid').forEach((field) => {
      const err = $('.f-err', field);
      const key = field.dataset.errKey;
      if (err && key) err.textContent = T[lang].err[key];
    });
  }
  inPlace.forEach((b) => b.addEventListener('click', () => setLang(b.dataset.setLang)));
  $$('a[data-set-lang]').forEach((a) => a.addEventListener('click', (e) => {
    if (a.getAttribute('aria-current') === 'page') { e.preventDefault(); return; }   // already this language
    const menu = $('#menu-panel');
    let hash = '';
    if (menu && !menu.hidden) hash = '#menu';
    else if (window.scrollY > 24) {
      const cur = $('[data-nav][aria-current="true"]');
      if (cur) hash = '#' + cur.dataset.nav;
    }
    if (hash) { e.preventDefault(); location.href = a.href.split('#')[0] + hash; }
  }));
  let initial = lang;
  try {
    // old links: …/?lang=en and …/#en (the claude.ai preview switches in place, the German page goes to /en)
    const q = new URLSearchParams(location.search).get('lang');
    if (location.hash === '#en' || q === 'en') {
      const en = $('a[data-set-lang="en"]');
      if (inPlace.length) initial = 'en';
      else if (en && lang !== 'en') { location.replace(en.href); return; }
    }
  } catch (e) { /* ignore */ }
  setLang(initial);

  /* ---------------- keyboard focus on the form fields (05.11.2026) ----------------
     Text fields count as :focus-visible even after a click, so styles.css shows their #435960 focus ring only while
     the keyboard is in use: Tab switches it on, a pointer press off. */
  const root = document.documentElement;
  document.addEventListener('keydown', (e) => { if (e.key === 'Tab') root.dataset.kbd = ''; }, true);
  document.addEventListener('pointerdown', () => { delete root.dataset.kbd; }, true);

  /* ---------------- header line + current section ---------------- */
  const hdr = $('#hdr');
  let ticking = false;
  function onScroll() {
    if (ticking) return;
    ticking = true;
    requestAnimationFrame(() => {
      ticking = false;
      if (hdr) hdr.classList.toggle('is-scrolled', window.scrollY > 24);
    });
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  const navLinks = $$('[data-nav]');
  if ('IntersectionObserver' in window && navLinks.length) {
    const secObs = new IntersectionObserver((entries) => {
      entries.forEach((en) => {
        if (!en.isIntersecting) return;
        const id = en.target.id;
        navLinks.forEach((a) => {
          if (a.dataset.nav === id) a.setAttribute('aria-current', 'true');
          else a.removeAttribute('aria-current');
        });
      });
    }, { rootMargin: '-42% 0px -52% 0px' });
    $$('[data-sec]').forEach((s) => secObs.observe(s));
  }

  /* ---------------- shimmering fields: the hero (Martin, 26.10.; two colours of the whole spectrum since 28.10.) and,
     since 29.10., the field behind Impressum and Datenschutz ----------------
     The hero field changes colour like shot silk, and at any moment exactly two colours play against each other:
     four soft areas drift over the field, two carry the first colour and two the second, and where they meet the
     two mix in linear light (no grey, no third colour). The pair travels once around the whole colour wheel in
     about 72 s, the second colour running 60–100° ahead of the first, so every hue comes by; it starts with lime
     and neon cyan. The wheel is Martin's variant A (28.10.): yellow, green and cyan as full neon, red, pink,
     violet and blue as light neon tones, all chosen so the #435960 type keeps at least 4.5:1 (WCAG AA) on every
     colour and every mix; fully saturated red, pink, violet or blue would make it unreadable. Painted 12 times a
     second on a canvas at a sixth of the screen resolution, which the browser scales up smoothly behind the
     content; a fine ordered dither keeps the gradients free of bands. The field fades in from plain lime when it
     first comes into view and rests while it is out of view or the tab is hidden. The pause button next to the
     kicker stops it (WCAG 2.2.2). Without JavaScript and with reduced motion it stays plain lime. The footer
     shimmered too from 26.10. and is plain white since 28.10. (Martin; its variant is in the git history).
     Since 29.10. (Martin) the screen behind the Impressum and Datenschutz sheet shimmers the same way, instead of
     the plain #435960 backdrop. Hero and dialogs share one timeline: a dialog opens in the colours the hero shows at
     that moment, and the hero carries on from there when it closes. Only the visible field runs (the hero rests
     while a dialog covers it); each dialog has its own pause icon, and every icon pauses all fields.
     Since 25.11.2026 (Martin) every call-to-action button shimmers too, on the same timeline (see below). */
  const reduceMotion = window.matchMedia ? window.matchMedia('(prefers-reduced-motion: reduce)') : { matches: false };
  const sheenBtns = $$('[data-sheen-btn]');
  const sheens = [];
  let sheenPaused = false;
  let clock = 0, last = 0;   // the shared timeline in seconds, and the time of its last frame
  const legalOpen = () => !!document.querySelector('dialog.legal[open]');
  const syncSheens = () => sheens.forEach((sync) => sync());
  let stopRobot = null;      // ends the robot's scene (below); the pause icons stop it too

  // the colour wheel, variant A (Martin 28.10.): 36 colours 10° apart in OKLCH hue, from the lime towards green,
  // cyan, blue, violet, pink, orange and yellow; each the most saturated colour of its hue on which #435960 keeps
  // at least 4.6:1, so with blending, rounding and dither it never drops below 4.5:1 (tools/colour_wheel.py).
  // Shared since 16.11. with the robot, whose chest window shows the pair the hero shows.
  const WHEEL = 'dafd55 a7ff00 4bff00 00ff7b 00ffab 00ffca 00ffe2 00fff6 00f4ff 00e3ff 60dbff 82d7ff 96d3ff a4d0ff b0cdff bacbff c3c9ff cdc5ff d7c2ff e3beff f3b8ff ffb3f7 ffb6e5 ffb8d8 ffb9cd ffbac3 ffbbb9 ffbcb0 ffbda5 ffbe99 ffbf8a ffc074 ffc24d ffcc00 ffe300 fdff00'
    .split(' ').map((c) => [0, 2, 4].map((i) => parseInt(c.slice(i, i + 2), 16)));
  const SPEED = 4;              // Martin 28.10.: faster again (26.10.: 1, 27.10.: 1.6); the areas drift in 22–37 s
  const TURN = 288;             // s for the pair to go once around the wheel at SPEED 1 (72 s now)
  const GAP = [80, 20, 197];    // the second colour runs 80° ± 20° ahead, period at SPEED 1 (49 s now)
  const FADE = 4, TAU = Math.PI * 2;   // s to fade in
  const lin = (v) => (v <= 10.31475 ? v / 3294.6 : ((v / 255 + 0.055) / 1.055) ** 2.4);         // sRGB 0–255 to linear light
  const enc = (l) => 255 * (l <= 0.0031308 ? 12.92 * l : 1.055 * l ** (1 / 2.4) - 0.055);   // and back
  // the wheel at a hue (degrees from the lime), in linear light
  function wheel(deg) {
    const u = (((deg / 10) % 36) + 36) % 36, k = Math.floor(u), f = u - k, a = WHEEL[k], b = WHEEL[(k + 1) % 36];
    return [0, 1, 2].map((c) => lin(a[c] + (b[c] - a[c]) * f));
  }
  // the pair at time c (s on the shared timeline), in linear light; both start at the lime and part while the
  // field fades in
  function pair(c) {
    const t = c * SPEED, e = Math.min(1, c / FADE), ramp = e * e * (3 - 2 * e);
    const hue = (360 * t) / TURN, gap = GAP[0] + GAP[1] * Math.sin((TAU * t) / GAP[2]);
    return [wheel(ramp * hue), wheel(ramp * (hue + gap))];
  }
  if (!reduceMotion.matches && window.requestAnimationFrame) {
    const add = (field, covered, src) => {
      const cv = document.createElement('canvas');
      const g = cv.getContext('2d');
      if (g) sheens.push(sheen(field, cv, g, covered, src));
    };
    const hero = $('.hero');
    if (hero) add(hero, legalOpen);                            // covered while a legal dialog is open
    // every call-to-action button (Martin 25.11.2026): in the hero the fill shows the field behind the other way
    // round (src = the hero, see sheen()), elsewhere the hero's pair laid out over the button itself; each rests
    // while it is out of view (also inside the closed menu) or a legal dialog is open
    $$('.btn').forEach((b) => add(b, legalOpen, hero && hero.contains(b) ? hero : null));
    $$('dialog.legal').forEach((d) => add(d, () => !d.open));  // runs only while its dialog is open
    if (sheens.length) {
      const setPaused = (p) => {
        sheenPaused = p;
        sheenBtns.forEach((b) => b.classList.toggle('is-paused', p));
        syncSheens();
        if (p && stopRobot) stopRobot();   // the pause icon also ends the robot's scene at once (WCAG 2.2.2)
      };
      sheenBtns.forEach((b) => {
        b.hidden = false;
        b.addEventListener('click', () => setPaused(!sheenPaused));
      });
      if (reduceMotion.addEventListener) reduceMotion.addEventListener('change', () => { if (reduceMotion.matches) setPaused(true); });
    }
  }

  // a shimmering field: a canvas painted behind its content (in a dialog only beside the sheet, see styles.css);
  // covered() says when the field is hidden although on screen. Returns its sync function.
  // With src (the hero's two buttons, Martin 25.11.2026) the canvas shows the counterpart of src's field at
  // the same place: the areas are laid out over src as there, and the two colours are swapped, so wherever the
  // hero shows its first colour the button shows the second and the other way round; still the same two colours.
  function sheen(field, cv, g, covered, src) {
    // areas: centre x, y (share of the field), drift x, y (share), drift periods (s), radius (share of the
    // longer side); the first two (top left, bottom right) carry the first colour, the last two the second
    const AREAS = [
      [0.15, 0.20, 0.14, 0.10, 97, 131, 0.62],
      [0.70, 0.85, 0.16, 0.10, 127, 101, 0.66],
      [0.85, 0.25, 0.12, 0.14, 113, 89, 0.58],
      [0.30, 0.75, 0.10, 0.12, 89, 149, 0.52],
    ];
    const SOFT = 2;               // each area falls off like a bell, weight e^-SOFT at its radius
    const RES = 6;                // CSS px per canvas pixel
    const BAYER = [0, 8, 2, 10, 12, 4, 14, 6, 3, 11, 1, 9, 15, 7, 13, 5].map((v) => (v + 0.5) / 16 - 0.5);
    const mix = new Float32Array(256 * 3);      // this frame's blend from the first colour to the second
    let W = 0, H = 0, w = 1, h = 1, img = null, xs = [], ys = [];
    let painted = -1, raf = 0, inView = true;
    cv.className = 'sheen';
    cv.setAttribute('aria-hidden', 'true');
    field.prepend(cv);

    function paint() {
      // the field the areas are laid out over (fw × fh) and this canvas's place in it (ox, oy)
      let fw = w, fh = h, ox = 0, oy = 0, [ca, cb] = pair(clock);
      if (src) {
        const r = src.getBoundingClientRect(), c = cv.getBoundingClientRect();
        fw = r.width || 1; fh = r.height || 1; ox = c.left - r.left; oy = c.top - r.top;
        [ca, cb] = [cb, ca];
      }
      const t = clock * SPEED, m = Math.max(fw, fh);
      for (let k = 0; k < 256; k++) {
        for (let c = 0; c < 3; c++) mix[k * 3 + c] = enc(ca[c] + ((cb[c] - ca[c]) * k) / 255);
      }
      // per area: its bell along x and along y (the bell is separable)
      AREAS.forEach(([x, y, dx, dy, px, py, r], n) => {
        const cx = (x + dx * Math.sin((TAU * t) / px)) * fw, cy = (y + dy * Math.sin((TAU * t) / py + 1.3)) * fh;
        const k = SOFT / (r * m) ** 2, X = xs[n], Y = ys[n];
        for (let i = 0; i < W; i++) X[i] = Math.exp(-k * (ox + (i + 0.5) * RES - cx) ** 2);
        for (let j = 0; j < H; j++) Y[j] = Math.exp(-k * (oy + (j + 0.5) * RES - cy) ** 2);
      });
      const d = img.data, [X0, X1, X2, X3] = xs;
      let p = 0;
      for (let j = 0; j < H; j++) {
        const y0 = ys[0][j], y1 = ys[1][j], y2 = ys[2][j], y3 = ys[3][j];
        for (let i = 0; i < W; i++) {
          const a = X0[i] * y0 + X1[i] * y1, b = X2[i] * y2 + X3[i] * y3;
          let s = b / (a + b || 1);                // share of the second colour
          s = s * s * (3 - 2 * s);                 // twice: large plain areas of each colour and a soft but
          s = s * s * (3 - 2 * s);                 // narrow zone where they meet, so the pair stays clear
          const q = Math.round(s * 255) * 3, dz = BAYER[((j & 3) << 2) | (i & 3)];
          d[p] = mix[q] + dz; d[p + 1] = mix[q + 1] + dz; d[p + 2] = mix[q + 2] + dz; d[p + 3] = 255;
          p += 4;
        }
      }
      g.putImageData(img, 0, 0);
    }
    function tick(now) {
      raf = 0;
      if (now !== last) {   // the timeline moves once per frame, however many fields run
        clock += last ? Math.min(now - last, 100) / 1000 : 0;
        last = now;
      }
      if (clock - painted >= 1 / 12) { painted = clock; paint(); }
      run();
    }
    function run() {
      if (!raf && !sheenPaused && inView && !document.hidden && !covered()) raf = requestAnimationFrame(tick);
    }
    function rest() {
      if (!raf) return;
      cancelAnimationFrame(raf);
      raf = 0;
      last = 0;   // the next field to run starts without a jump
    }
    function size() {
      const rect = cv.getBoundingClientRect();
      w = rect.width || 1;
      h = rect.height || 1;
      const nw = Math.max(8, Math.ceil(w / RES)), nh = Math.max(8, Math.ceil(h / RES));
      if (nw !== W || nh !== H) {
        W = cv.width = nw;
        H = cv.height = nh;
        img = g.createImageData(W, H);
        xs = AREAS.map(() => new Float32Array(W));
        ys = AREAS.map(() => new Float32Array(H));
      }
      paint();
    }
    function sync() {
      if (sheenPaused || !inView || document.hidden || covered()) rest(); else run();
    }

    size();
    document.addEventListener('visibilitychange', sync);
    // watch the canvas itself: in a dialog it is hidden while the dialog is closed or the sheet fills the screen
    if ('IntersectionObserver' in window) new IntersectionObserver(([en]) => { inView = en.isIntersecting; sync(); }).observe(cv);
    if ('ResizeObserver' in window) new ResizeObserver(size).observe(cv);
    else window.addEventListener('resize', size);
    sync();
    return sync;
  }

  /* ---------------- mobile menu ---------------- */
  const menuBtn = $('#menu-btn');
  const panel = $('#menu-panel');
  function setMenu(open) {
    if (!menuBtn || !panel) return;
    menuBtn.setAttribute('aria-expanded', String(open));
    panel.hidden = !open;
    document.documentElement.style.overflow = open ? 'hidden' : '';
  }
  if (menuBtn && panel) {
    menuBtn.addEventListener('click', () => setMenu(panel.hidden));
    // a link in the menu closes it; the language links keep it open (they reopen it on the other page)
    panel.addEventListener('click', (e) => { if (e.target.closest('a') && !e.target.closest('[data-set-lang]')) setMenu(false); });
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && !panel.hidden) { setMenu(false); menuBtn.focus(); }
    });
    window.addEventListener('resize', () => { if (window.innerWidth >= 1100 && !panel.hidden) setMenu(false); });
    // arriving from the language switch in the menu (/en#menu): the menu opens again, focus on the active language
    if (location.hash === '#menu') {
      try { history.replaceState(null, '', location.pathname + location.search); } catch (e) { /* ignore */ }
      if (window.innerWidth < 1100) {
        setMenu(true);
        const cur = $('a[data-set-lang][aria-current="page"]', panel);
        if (cur) cur.focus({ preventScroll: true });
      }
    }
  }

  /* ---------------- copy buttons ---------------- */
  function flashDone(btn) {
    const idle = $('.cp-idle', btn), done = $('.cp-done', btn);
    if (!idle || !done) return;
    idle.hidden = true; done.hidden = false;
    setTimeout(() => { idle.hidden = false; done.hidden = true; }, 1800);
  }
  function fallbackCopy(text) {
    const ta = document.createElement('textarea');
    ta.value = text; ta.setAttribute('readonly', '');
    ta.style.position = 'fixed'; ta.style.top = '0'; ta.style.left = '0'; ta.style.opacity = '0';
    document.body.appendChild(ta);
    ta.select();
    let ok = false;
    try { ok = document.execCommand('copy'); } catch (e) { ok = false; }
    ta.remove();
    return ok;
  }
  function copyText(text, btn) {
    const done = (ok) => { if (ok && btn) flashDone(btn); };
    try {
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(text).then(() => done(true), () => done(fallbackCopy(text)));
        return;
      }
    } catch (e) { /* fall through */ }
    done(fallbackCopy(text));
  }
  $$('[data-copy]').forEach((b) => b.addEventListener('click', () => copyText(b.dataset.copy, b)));

  /* ---------------- contact form (opens the visitor's mail app, sends nothing itself) ---------------- */
  const form = $('#msg-form');
  if (form) {
    const fName = $('#f-name'), fMail = $('#f-mail'), fMsg = $('#f-msg');
    const note = $('#form-note'), preview = $('#form-preview'), copyMsg = $('#copy-msg');
    let lastText = '';
    const setErr = (input, key) => {
      const field = input.closest('.field');
      const err = $('.f-err', field);
      if (key) {
        field.classList.add('invalid'); field.dataset.errKey = key;
        input.setAttribute('aria-invalid', 'true');
        if (err) { err.textContent = T[lang].err[key]; err.hidden = false; err.id = input.id + '-err'; input.setAttribute('aria-describedby', err.id); }
      } else {
        field.classList.remove('invalid'); delete field.dataset.errKey;
        input.removeAttribute('aria-invalid'); input.removeAttribute('aria-describedby');
        if (err) { err.textContent = ''; err.hidden = true; }
      }
    };
    [fName, fMail, fMsg].forEach((el) => el.addEventListener('input', () => {
      if (el.closest('.field').classList.contains('invalid')) setErr(el, null);
    }));
    form.addEventListener('submit', (e) => {
      e.preventDefault();
      const name = fName.value.trim(), mail = fMail.value.trim(), msg = fMsg.value.trim();
      const bad = [];
      setErr(fName, name ? null : 'name'); if (!name) bad.push(fName);
      const mailOk = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(mail);
      setErr(fMail, mailOk ? null : 'email'); if (!mailOk) bad.push(fMail);
      setErr(fMsg, msg.length >= 3 ? null : 'message'); if (msg.length < 3) bad.push(fMsg);
      if (bad.length) { bad[0].focus(); return; }
      const subject = T[lang].subject + ': ' + name;
      const body = msg + '\n\n' + name + '\n' + mail;
      lastText = T[lang].to + ': ' + MAIL + '\n' + T[lang].subj + ': ' + subject + '\n\n' + body;
      if (preview) preview.textContent = lastText;
      if (note) note.hidden = false;
      const a = document.createElement('a');
      a.href = 'mailto:' + MAIL + '?subject=' + encodeURIComponent(subject) + '&body=' + encodeURIComponent(body);
      a.rel = 'noopener';
      document.body.appendChild(a);
      try { a.click(); } catch (err) { /* the preview above stays as fallback */ }
      a.remove();
    });
    if (copyMsg) copyMsg.addEventListener('click', () => copyText(lastText, copyMsg));
  }

  /* ---------------- legal dialogs ----------------
     Each dialog covers the whole screen: the white sheet (.legal-in, it scrolls) and beside it the shimmering field
     (since 29.10., see above). The hero rests while a dialog is open and takes over the timeline when it closes. */
  const legalIds = ['impressum', 'datenschutz'];
  function openLegal(id) {
    const d = document.getElementById(id);
    if (!d) return;
    $$('dialog.legal[open]').forEach((x) => { if (x !== d) x.close(); });
    setMenu(false);
    if (!d.open) {
      if (typeof d.showModal === 'function') d.showModal(); else d.setAttribute('open', '');
      // focus „Schließen“ as before; the sheet is a scroll area now and would otherwise take the first focus
      const x = $('[data-close]', d);
      if (x) x.focus({ preventScroll: true });
    }
    const sheet = $('.legal-in', d);
    if (sheet) sheet.scrollTop = 0;
    document.documentElement.style.overflow = 'hidden';
    syncSheens();
  }
  $$('[data-open]').forEach((a) => a.addEventListener('click', (e) => { e.preventDefault(); openLegal(a.dataset.open); }));
  $$('dialog.legal').forEach((d) => {
    // a click on the field beside the sheet closes the dialog; only when it was also pressed there, so letting go
    // of a text selection beside the sheet keeps it open
    let pressed = null;
    d.addEventListener('pointerdown', (e) => { pressed = e.target; });
    d.addEventListener('click', (e) => {
      if (e.target === d && pressed === d) d.close();
      pressed = null;
    });
    $$('[data-close]', d).forEach((b) => b.addEventListener('click', () => d.close()));
    d.addEventListener('close', () => {
      if (!legalOpen()) document.documentElement.style.overflow = '';
      syncSheens();
    });
  });
  const h = (location.hash || '').slice(1);
  if (legalIds.includes(h)) openLegal(h);
  window.addEventListener('hashchange', () => {
    const id = (location.hash || '').slice(1);
    if (legalIds.includes(id)) openLegal(id);
  });

  /* ---------------- the robot, scene 1 (Martin 16.11.): he turns the upside-down logo the right way up ----------------
     A tin toy robot after Martin's second flat Higgsfield draft (job d9d6a470): strictly frontal and flat, a square
     head, a line for a mouth, only #435960 and lime in full tones, and in the chest window the two colours the hero
     shows at that moment. On load the logo in the header stands upside down (styles.css: only with JavaScript, without
     reduced motion and only where the header carries data-robo). After 1.5 s the robot trots in from the right in
     small tin-toy steps, stops at the logo, grabs its end, flicks it the right way up with a little spring, nods and
     walks off to the left; 5–6 s in all, once per page view (nothing is stored; /en is a page of its own, so it plays
     there again). It is aria-hidden, takes no clicks and sits absolutely in the header, so nothing moves (CLS 0);
     the pause icons of the shimmer end the scene at once (WCAG 2.2.2). One timeline: pose(t) gives every part for
     any moment, so a dropped frame never puts the robot out of step.
     Drawing in a 88 × 144 grid, x = 0 on the middle axis, feet on y = 143.5. Each part is a group with its pivot in
     data-p: legs at the hips, torso at the middle of its lower edge (it carries head and arms), head at the neck,
     antenna at its foot, arms at the shoulder joints; the pupils move as one. Feet, hands, ears, eyes, mouth, rivets
     and buttons are lime, the rest #435960. */
  const ROBOT_SVG = (id) => '<svg viewBox="-44 0 88 144" aria-hidden="true" focusable="false">'
    + '<defs><linearGradient id="' + id + '">'
    + [0, 25, 50, 75, 100].map((o) => '<stop offset="' + o + '%" stop-color="#dafd55"/>').join('') + '</linearGradient></defs>'
    + '<g data-k="legL" data-p="-14.5 108"><path fill="#435960" d="M-21 100h13v35h-13z"/><path fill="#dafd55" d="M-25.5 134.5h22v9h-22z"/></g>'
    + '<g data-k="legR" data-p="14.5 108"><path fill="#435960" d="M8 100h13v35h-13z"/><path fill="#dafd55" d="M3.5 134.5h22v9h-22z"/></g>'
    + '<g data-k="torso" data-p="0 108">'
    +   '<path fill="#435960" d="M-7.5 46h15v7h-15zM-28.5 52h57v56h-57z"/>'
    +   '<path fill="#dafd55" d="M-23.5 55h3v3h-3zm14.5 0h3v3h-3zm15 0h3v3h-3zm14.5 0h3v3h-3zM-23.5 101.5h3v3h-3zm14.5 0h3v3h-3zm15 0h3v3h-3zm14.5 0h3v3h-3zM-14.5 89h6v6h-6zm11.5 0h6v6h-6zm11.5 0h6v6h-6z"/>'
    +   '<rect x="-21" y="61.5" width="42" height="23" fill="url(#' + id + ')"/>'
    +   '<g data-k="head" data-p="0 47">'
    +     '<g data-k="ant" data-p="0 15"><path fill="#435960" d="M-1.5 5h3v11h-3z"/><path fill="#dafd55" d="M-3.5 0h7v6h-7z"/></g>'
    +     '<path fill="#435960" d="M-20 15h40v32h-40z"/>'
    +     '<path fill="#dafd55" d="M-25.5 25h5.5v14h-5.5zm45.5 0h5.5v14h-5.5zM-14 23h9v9h-9zm19 0h9v9h-9zM-7.5 38.5h15v3h-15z"/>'
    +     '<g data-k="eyes"><path fill="#435960" d="M-11 26h3v3h-3zm19 0h3v3h-3z"/></g>'
    +   '</g>'
    +   '<g data-k="armL" data-p="-29.5 63.5"><path fill="#435960" d="M-31 62h3v3h-3zM-42.5 59h12v38h-12z"/><path fill="#dafd55" d="M-43.5 96.5h14v11h-4.5v-5h-5v5h-4.5z"/></g>'
    +   '<g data-k="armR" data-p="29.5 63.5"><path fill="#435960" d="M28 62h3v3h-3zM30.5 59h12v38h-12z"/><path fill="#dafd55" d="M29.5 96.5h14v11h-4.5v-5h-5v5h-4.5z"/></g>'
    + '</g></svg>';

  // the parts of a robot svg, with a setter: translate(dx dy), then rotate(a) about the part's pivot
  function robotParts(svg) {
    const P = {};
    $$('[data-k]', svg).forEach((g) => { P[g.dataset.k] = g; });
    const r2 = (v) => Math.round(v * 100) / 100;
    P.set = (k, dx, dy, a) => {
      const g = P[k];
      let tr = dx || dy ? 'translate(' + r2(dx) + ' ' + r2(dy) + ')' : '';
      if (a && g.dataset.p) tr += ' rotate(' + r2(a) + ' ' + g.dataset.p + ')';
      g.setAttribute('transform', tr.trim());
    };
    // the chest window: the two colours (linear light) blended across it like the hero blends them
    const stops = $$('stop', svg);
    let was = '';
    P.paint = (ca, cb) => {
      const key = ca.join() + cb.join();
      if (key === was) return;
      was = key;
      stops.forEach((s, i) => {
        let u = i / (stops.length - 1);
        u = u * u * (3 - 2 * u);
        s.setAttribute('stop-color', '#' + [0, 1, 2].map((c) => {
          const v = Math.round(Math.max(0, Math.min(255, enc(ca[c] + (cb[c] - ca[c]) * u))));
          return (v < 16 ? '0' : '') + v.toString(16);
        }).join(''));
      });
    };
    return P;
  }

  // easing helpers: share of a span, smoothstep, ease-out with a little overshoot, a damped wobble,
  // and a spring that settles from 0 to 1 with one small overshoot (about 9 %, peak after 0.4 s)
  const span = (t, a, b) => (t <= a ? 0 : t >= b ? 1 : (t - a) / (b - a));
  const smooth = (u) => u * u * (3 - 2 * u);
  const outBack = (u) => 1 + 2.2 * (u - 1) ** 3 + 1.2 * (u - 1) ** 2;
  const wobble = (s, f) => (s > 0 ? Math.exp(-5 * s) * Math.sin(2 * Math.PI * f * s) : 0);
  function spring(s) {
    if (s <= 0) return 0;
    if (s >= 1.4) return 1;
    const wd = Math.PI / 0.4, k = 0.75 * wd;   // damping ratio 0.6
    return 1 - Math.exp(-k * s) * (Math.cos(wd * s) + (k / wd) * Math.sin(wd * s));
  }

  // one tin-toy step cycle (two steps) at phase ph (cycles) and strength amp (0–1): the lifted leg reaches out
  // to the left (the robot walks leftwards), the body bobs and rocks, head, antenna and arms lag behind
  function gait(ph, amp) {
    const s = Math.sin(2 * Math.PI * ph), up = (v) => (v > 0 ? v ** 0.7 : 0);
    return {
      legL: [0, -4.5 * amp * up(s), 5 * amp * s],
      legR: [0, -4.5 * amp * up(-s), -5 * amp * s],
      torso: [0, -1.6 * amp * Math.abs(s) ** 0.8, 2.5 * amp * s],
      head: [0, 0, -2 * amp * Math.sin(2 * Math.PI * ph - 0.6)],
      ant: 7 * amp * Math.sin(2 * Math.PI * ph - 1.2),
      arm: -6 * amp * s,
    };
  }

  // the whole scene at t s after the robot sets off. m: x0 start, x1 at the logo, x2 gone (px, robot centre),
  // din and dout (s) for walking in and out. Returns the robot centre x (px), the logo angle and each part.
  const ACT = 2.45;   // s at the logo: reach, hold, flick, nod
  function pose(t, m) {
    const p = { x: m.x1, logo: 0, legL: [0, 0, 0], legR: [0, 0, 0], torso: [0, 0, 0], head: [0, 0, 0], ant: 0, eyes: 0, armL: 0, armR: 0 };
    const walk = (g) => {
      p.legL = g.legL; p.legR = g.legR; p.torso = g.torso; p.head = g.head; p.ant = g.ant;
      p.armL = g.arm; p.armR = g.arm;
    };
    if (t < m.din) {                                   // trotting in, quick at first, slowing down to the logo
      const u = t / m.din, e = 1 - (1 - u) ** 2;
      p.x = m.x0 + (m.x1 - m.x0) * e;
      p.logo = 180;
      walk(gait(2.6 * t + e * m.din, Math.min(1, t / 0.12, (m.din - t) / 0.35)));
      return p;
    }
    const r = t - m.din;
    if (r < ACT) {                                     // at the logo
      const look = smooth(span(r, 0.1, 0.35)) - smooth(span(r, 1.1, 1.45));
      p.head = [0, 2.5 * (Math.sin(Math.PI * span(r, 1.55, 1.77)) + Math.sin(Math.PI * span(r, 1.81, 2.03))), -5 * look];
      p.eyes = -1.5 * look;
      p.torso = [0, 1.2 * Math.sin(Math.PI * span(r, 0, 0.25)) + 0.8 * Math.sin(Math.PI * span(r, 0.7, 0.9)), 1.5 * wobble(r - 0.85, 2.5)];
      p.ant = 8 * wobble(r - 0.85, 3) + 9 * wobble(r - 1.55, 3);
      p.armL = r < 0.85 ? 90 * outBack(span(r, 0.25, 0.6))                 // reach and hold the end of the logo
        : r < 1 ? 90 + 45 * (1 - (1 - span(r, 0.85, 0.97)) ** 2)        // flick
        : 135 * (1 - smooth(span(r, 1, 1.4)));                          // and down again
      p.armR = -10 * Math.sin(Math.PI * span(r, 0.77, 1.2));
      p.logo = r < 0.85 ? 180 - 4 * Math.sin(Math.PI * span(r, 0.7, 0.85)) : 180 * (1 - spring(r - 0.85));
      return p;
    }
    const s = r - ACT, u = Math.min(1, s / m.dout);   // and off to the left, speeding up
    p.x = m.x1 + (m.x2 - m.x1) * u * u;
    walk(gait(2.6 * s + u * u * m.dout, Math.min(1, s / 0.2)));
    return p;
  }

  function robot(colours) {   // colours(t): the chest window's two colours, t s after the page started
    const hdr = $('#hdr');
    if (!hdr || !hdr.hasAttribute('data-robo')) return;
    const link = $('.logo', hdr), mark = link && $('svg', link);
    const scripting = window.matchMedia ? window.matchMedia('(scripting: enabled)') : null;
    const DELAY = 1.5;
    let stage = null, svg = null, P = null, raf = 0, t = 0, last = 0, m = null, k0 = 0;

    function finish() {
      if (raf > 0) cancelAnimationFrame(raf);
      raf = -1;
      hdr.removeAttribute('data-robo');
      hdr.classList.remove('rb-on');
      if (mark) mark.style.transform = '';
      if (stage) stage.remove();
      document.removeEventListener('visibilitychange', wake);
      if (reduceMotion.removeEventListener) reduceMotion.removeEventListener('change', finish);
    }
    function wake() {
      if (raf === 0 && !document.hidden) { last = 0; raf = requestAnimationFrame(frame); }
    }
    if (!mark || !scripting || !scripting.matches || reduceMotion.matches || !window.requestAnimationFrame || legalOpen()) {
      finish();
      return null;
    }
    hdr.classList.add('rb-on');   // from here the script holds the logo (styles.css would turn it back after 4 s)

    // where things are, in px from the header's top left; k = px per grid unit, chosen so that the claw of the
    // raised arm meets the middle of the logo while the feet stand on the lower edge of the header
    function measure() {
      const h = hdr.getBoundingClientRect(), l = link.getBoundingClientRect();
      const H = hdr.offsetHeight, ly = (l.top + l.bottom) / 2 - h.top;
      const k = Math.max(0.25, (H - ly) / 87);
      const x1 = l.right - h.left + 68.5 * k;
      return { k, H, x0: h.width + 50 * k, x1, x2: -50 * k };
    }

    stage = document.createElement('div');
    stage.className = 'rb-stage';
    stage.setAttribute('aria-hidden', 'true');
    stage.innerHTML = ROBOT_SVG('rb-win');
    svg = stage.firstChild;
    P = robotParts(svg);
    hdr.appendChild(stage);
    m = measure();
    m.din = Math.min(2.4, Math.max(1.7, (m.x0 - m.x1) / 650));
    m.dout = Math.min(1.4, Math.max(1, (m.x1 - m.x2) / 450));

    function draw(p) {
      if (m.k !== k0) {
        k0 = m.k;
        svg.style.width = 88 * m.k + 'px';
        svg.style.height = 144 * m.k + 'px';
        svg.style.left = -44 * m.k + 'px';
        svg.style.top = m.H - 143.5 * m.k + 'px';
      }
      svg.style.transform = 'translateX(' + Math.round(p.x * 10) / 10 + 'px)';
      mark.style.transform = 'rotate(' + Math.round(p.logo * 100) / 100 + 'deg)';
      ['legL', 'legR', 'torso', 'head'].forEach((n) => P.set(n, p[n][0], p[n][1], p[n][2]));
      P.set('ant', 0, 0, p.ant);
      P.set('eyes', p.eyes, 0, 0);
      P.set('armL', 0, 0, p.armL);
      P.set('armR', 0, 0, p.armR);
      const c = colours(t);
      P.paint(c[0], c[1]);
    }
    function frame(now) {
      raf = 0;
      try {
        if (last) t += Math.min(now - last, 50) / 1000;   // a slow or hidden tab pauses the scene, it never jumps
        last = now;
        const s = t - DELAY;
        Object.assign(m, measure());
        if (s >= m.din + ACT + m.dout) { finish(); return; }
        draw(pose(Math.max(0, s), m));
      } catch (e) {
        finish();
        return;
      }
      if (!document.hidden) raf = requestAnimationFrame(frame);
    }
    draw(pose(0, m));   // sized and in place (off screen to the right) before the page is painted again
    document.addEventListener('visibilitychange', wake);
    if (reduceMotion.addEventListener) reduceMotion.addEventListener('change', finish);
    wake();
    return finish;
  }

  // the chest window shows the hero's pair; while the hero is out of view (the page opened further down) its clock
  // rests, so the robot then runs the colours on with his own time
  stopRobot = robot((t) => pair(Math.max(clock, t)));
})();

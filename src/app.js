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

  /* ---------------- language ---------------- */
  let lang = 'de';
  function setLang(l) {
    lang = l === 'en' ? 'en' : 'de';
    site.dataset.lang = lang;
    document.documentElement.lang = lang;
    document.title = T[lang].title;
    $$('[data-set-lang]').forEach((b) => b.setAttribute('aria-pressed', String(b.dataset.setLang === lang)));
    $$('img[data-alt-de]').forEach((img) => { img.alt = lang === 'de' ? img.dataset.altDe : img.dataset.altEn; });
    const call = $('#call-btn');
    if (call) call.href = 'mailto:' + MAIL + '?subject=' + encodeURIComponent(T[lang].call);
    $$('.field.invalid').forEach((field) => {
      const err = $('.f-err', field);
      const key = field.dataset.errKey;
      if (err && key) err.textContent = T[lang].err[key];
    });
  }
  $$('[data-set-lang]').forEach((b) => b.addEventListener('click', () => setLang(b.dataset.setLang)));
  let initial = 'de';
  try {
    const q = new URLSearchParams(location.search).get('lang');
    if (location.hash === '#en' || q === 'en') initial = 'en';
  } catch (e) { /* ignore */ }
  setLang(initial);

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

  /* ---------------- hero and footer: the surface shimmers (Martin, 26.10.) ----------------
     Only the hero field and the footer change colour, slowly and quietly, like shot silk: four soft areas
     drift over the lime on slow paths, and each passes through fresh, bright colours (lime, neon yellow, mint,
     aqua). Painted 12 times a second on a canvas at a sixth of the screen resolution (a few milliseconds of work),
     which the browser scales up smoothly behind the content; a fine ordered dither keeps the gradients free of
     bands. Each field fades in from plain lime when it first comes into view and rests while it is out of view
     or the tab is hidden. In the footer the colours fade out towards its top edge, so the lime contact section
     still runs straight into it. One pause state for both fields, set by either button (WCAG 2.2.2). Without
     JavaScript and with reduced motion both stay plain lime. */
  const reduceMotion = window.matchMedia ? window.matchMedia('(prefers-reduced-motion: reduce)') : { matches: false };
  const sheenBtns = $$('[data-sheen-btn]');
  const sheens = [];
  let sheenPaused = false;
  if (!reduceMotion.matches && window.requestAnimationFrame) {
    // field, time shift (s) so the two fields differ, share of the height over which the colour fades in from the top
    [[$('.hero'), 0, 0], [$('.ftr'), 57, 0.5]].forEach(([field, shift, fadeTop]) => {
      if (!field) return;
      const cv = document.createElement('canvas');
      const g = cv.getContext('2d');
      if (g) sheens.push(sheen(field, cv, g, shift, fadeTop));
    });
    if (sheens.length) {
      const setPaused = (p) => {
        sheenPaused = p;
        sheenBtns.forEach((b) => b.classList.toggle('is-paused', p));
        sheens.forEach((sync) => sync());
      };
      sheenBtns.forEach((b) => {
        b.hidden = false;
        b.addEventListener('click', () => setPaused(!sheenPaused));
      });
      if (reduceMotion.addEventListener) reduceMotion.addEventListener('change', () => { if (reduceMotion.matches) setPaused(true); });
    }
  }

  // one shimmering field; returns its sync function
  function sheen(field, cv, g, shift, fadeTop) {
    const LIME = [218, 253, 85];
    const PAL = [LIME, [255, 242, 0], [77, 255, 184], [87, 245, 255]];   // lime, neon yellow, mint, aqua
    // areas: centre x, y (share of the field), drift x, y (share), drift periods (s), radius (share of the
    // longer side), where in the colour cycle it starts
    const AREAS = [
      [0.15, 0.20, 0.14, 0.10, 97, 131, 0.62, 0.4],
      [0.85, 0.25, 0.12, 0.14, 113, 89, 0.58, 1.5],
      [0.70, 0.85, 0.16, 0.10, 127, 101, 0.66, 2.5],
      [0.30, 0.75, 0.10, 0.12, 89, 149, 0.52, 3.4],
    ];
    const STEP = 38, FADE = 4, RES = 6, TAU = Math.PI * 2;   // s per colour change, s to fade in, CSS px per pixel
    const SPEED = 1.6;     // Martin 27.10.: a little faster, so a colour change takes about 24 s, a drift 56–93 s
    const BAYER = [0, 8, 2, 10, 12, 4, 14, 6, 3, 11, 1, 9, 15, 7, 13, 5].map((v) => (v + 0.5) / 16 - 0.5);
    let W = 0, H = 0, w = 1, h = 1, img = null, xs = [], ys = [], rows = null;
    let clock = 0, last = 0, painted = -1, raf = 0, inView = true;
    cv.className = 'sheen';
    cv.setAttribute('aria-hidden', 'true');
    field.prepend(cv);

    function colour(off, t) {
      const u = t / STEP + off, k = Math.floor(u), f0 = u - k, f = f0 * f0 * (3 - 2 * f0);
      const a = PAL[k % PAL.length], b = PAL[(k + 1) % PAL.length];
      return [a[0] + (b[0] - a[0]) * f, a[1] + (b[1] - a[1]) * f, a[2] + (b[2] - a[2]) * f];
    }
    function paint() {
      const t = (clock + shift) * SPEED, e = Math.min(1, clock / FADE), ramp = e * e * (3 - 2 * e), m = Math.max(w, h);
      // per area: squared distance along x and y in units of its radius (the bell is separable)
      const areas = AREAS.map(([x, y, dx, dy, px, py, r, off], n) => {
        const cx = (x + dx * Math.sin(TAU * t / px)) * w, cy = (y + dy * Math.sin(TAU * t / py + 1.3)) * h;
        const R2 = (r * m) ** 2, X = xs[n], Y = ys[n];
        for (let i = 0; i < W; i++) X[i] = ((i + 0.5) * RES - cx) ** 2 / R2;
        for (let j = 0; j < H; j++) Y[j] = ((j + 0.5) * RES - cy) ** 2 / R2;
        return { X, Y, c: colour(off, t) };
      }).reverse();                                   // the first area lies on top
      const d = img.data;
      let p = 0;
      for (let j = 0; j < H; j++) {
        const kr = ramp * rows[j];
        for (let i = 0; i < W; i++) {
          let r = LIME[0], gr = LIME[1], b = LIME[2];
          for (let n = 0; n < areas.length; n++) {
            const a = areas[n], q = a.X[i] + a.Y[j];
            if (q < 1) {
              const k = kr * (1 - q) * (1 - q), c = a.c;
              r += (c[0] - r) * k; gr += (c[1] - gr) * k; b += (c[2] - b) * k;
            }
          }
          const dz = BAYER[((j & 3) << 2) | (i & 3)];
          d[p] = r + dz; d[p + 1] = gr + dz; d[p + 2] = b + dz; d[p + 3] = 255;
          p += 4;
        }
      }
      g.putImageData(img, 0, 0);
    }
    function tick(now) {
      raf = 0;
      clock += last ? Math.min(now - last, 100) / 1000 : 0;
      last = now;
      if (clock - painted >= 1 / 12) { painted = clock; paint(); }
      run();
    }
    function run() {
      if (!raf && !sheenPaused && inView && !document.hidden) raf = requestAnimationFrame(tick);
    }
    function rest() {
      if (raf) cancelAnimationFrame(raf);
      raf = 0;
      last = 0;
    }
    function size() {
      const rect = field.getBoundingClientRect();
      w = rect.width || 1;
      h = rect.height || 1;
      const nw = Math.max(8, Math.ceil(w / RES)), nh = Math.max(8, Math.ceil(h / RES));
      if (nw !== W || nh !== H) {
        W = cv.width = nw;
        H = cv.height = nh;
        img = g.createImageData(W, H);
        xs = AREAS.map(() => new Float32Array(W));
        ys = AREAS.map(() => new Float32Array(H));
        rows = new Float32Array(H);
      }
      for (let j = 0; j < H; j++) {               // colour strength by row: fades in from the top edge if asked
        const f = fadeTop ? Math.min(1, ((j + 0.5) * RES) / (fadeTop * h)) : 1;
        rows[j] = f * f * (3 - 2 * f);
      }
      paint();
    }
    function sync() {
      if (sheenPaused || !inView || document.hidden) rest(); else run();
    }

    size();
    document.addEventListener('visibilitychange', sync);
    if ('IntersectionObserver' in window) new IntersectionObserver(([en]) => { inView = en.isIntersecting; sync(); }).observe(field);
    if ('ResizeObserver' in window) new ResizeObserver(size).observe(field);
    else window.addEventListener('resize', size);
    sync();
    return sync;
  }

  /* ---------------- headlines: now and then a lime wave runs through the grey type ----------------
     First pass shortly after a headline comes into view, then every 8–14 s while it stays there.
     No waves with reduced motion or forced colours; the type then simply stays #435960. */
  // not on the lime fields (hero, process, contact), where a lime wave would not show
  const heads = $$('.sec:not(.is-lime) .sec-head h2, .legal-hd h2');
  const calm = window.matchMedia ? window.matchMedia('(prefers-reduced-motion: reduce), (forced-colors: active)') : { matches: false };
  if (heads.length && 'IntersectionObserver' in window && !calm.matches) {
    const timers = new Map();
    const next = (h, ms) => { clearTimeout(timers.get(h)); timers.set(h, setTimeout(() => wave(h), ms)); };
    const wave = (h) => {
      if (!document.hidden && !calm.matches) {
        h.classList.remove('is-waving');
        void h.offsetWidth;            // restart the animation even if a pass is still running
        h.classList.add('is-waving');
      }
      next(h, 8000 + Math.random() * 6000);
    };
    heads.forEach((h) => h.addEventListener('animationend', (e) => {
      if (e.animationName === 'lime-wave') h.classList.remove('is-waving');
    }));
    const headObs = new IntersectionObserver((entries) => entries.forEach((en) => {
      if (en.isIntersecting) next(en.target, 700);
      else { clearTimeout(timers.get(en.target)); en.target.classList.remove('is-waving'); }
    }), { threshold: 0.5 });
    heads.forEach((h) => headObs.observe(h));
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
    panel.addEventListener('click', (e) => { if (e.target.closest('a')) setMenu(false); });
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && !panel.hidden) { setMenu(false); menuBtn.focus(); }
    });
    window.addEventListener('resize', () => { if (window.innerWidth >= 1100 && !panel.hidden) setMenu(false); });
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

  /* ---------------- legal dialogs ---------------- */
  const legalIds = ['impressum', 'datenschutz'];
  function openLegal(id) {
    const d = document.getElementById(id);
    if (!d) return;
    $$('dialog.legal[open]').forEach((x) => { if (x !== d) x.close(); });
    setMenu(false);
    if (!d.open) {
      if (typeof d.showModal === 'function') d.showModal(); else d.setAttribute('open', '');
    }
    d.scrollTop = 0;
    document.documentElement.style.overflow = 'hidden';
  }
  $$('[data-open]').forEach((a) => a.addEventListener('click', (e) => { e.preventDefault(); openLegal(a.dataset.open); }));
  $$('dialog.legal').forEach((d) => {
    d.addEventListener('click', (e) => {
      if (e.target !== d) return;
      const r = d.getBoundingClientRect();
      const inside = e.clientX >= r.left && e.clientX <= r.right && e.clientY >= r.top && e.clientY <= r.bottom;
      if (!inside) d.close();
    });
    $$('[data-close]', d).forEach((b) => b.addEventListener('click', () => d.close()));
    d.addEventListener('close', () => {
      if (!$$('dialog.legal[open]').length) document.documentElement.style.overflow = '';
    });
  });
  const h = (location.hash || '').slice(1);
  if (legalIds.includes(h)) openLegal(h);
  window.addEventListener('hashchange', () => {
    const id = (location.hash || '').slice(1);
    if (legalIds.includes(id)) openLegal(id);
  });
})();

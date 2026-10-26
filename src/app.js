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
    $$('[data-label-de]').forEach((el) => el.setAttribute('aria-label', lang === 'de' ? el.dataset.labelDe : el.dataset.labelEn));
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

  /* ---------------- hero: line animation (Martin, 26.10.) ----------------
     Twelve line drawings from the history of technology, from the Neanderthal at the fire to the flying car
     (drawn with Nano Banana Pro on Higgsfield AI, traced to centre lines by tools/hero_lines.py). Only lines:
     1 px, #435960, transparent on the lime hero. The lines of the next drawing fly in from all directions and take
     the place of the current ones, which fly out. Without JavaScript, with reduced motion or data saver the last
     drawing stays as a still. The button pauses and resumes (WCAG 2.2.2); the animation also rests while the hero
     is out of view or the tab is hidden. */
  const art = $('#hero-art');
  const artBtn = $('#art-btn');
  const still = art && $('.hero-still', art);
  const linesData = $('#hero-lines');           // inlined in the artifact preview; the live site fetches the file
  const reduceMotion = window.matchMedia ? window.matchMedia('(prefers-reduced-motion: reduce)') : { matches: false };
  const saveData = !!(navigator.connection && navigator.connection.saveData);
  if (art && artBtn && still && !reduceMotion.matches && !saveData && window.requestAnimationFrame
      && (linesData || (window.fetch && art.dataset.src))) {
    const go = () => {
      const load = linesData ? Promise.resolve().then(() => JSON.parse(linesData.textContent))
        : fetch(art.dataset.src).then((r) => (r.ok ? r.json() : Promise.reject(new Error(String(r.status)))));
      load.then(heroLines).catch(() => { /* the still stays */ });
    };
    if (document.readyState === 'complete') go();
    else window.addEventListener('load', go, { once: true });
  }

  function heroLines(data) {
    const VW = data.w, VH = data.h, CX = VW / 2, CY = VH / 2;
    const HOLD = 1500, HOLD_END = 2600, HOLD_START = 900;     // ms a finished drawing stands still
    const rnd = (a, b) => a + Math.random() * (b - a);
    const side = () => (Math.random() < 0.5 ? -1 : 1);
    // strokes: absolute points ("M x y l dx dy ..."), centre and radius
    const scenes = data.scenes.map((sc) => sc.d.map((d) => {
      const n = d.match(/-?(?:\d+\.?\d*|\.\d+)/g).map(Number);
      const p = new Float32Array(n.length);
      let x = n[0], y = n[1], cx = 0, cy = 0, r = 0;
      p[0] = x; p[1] = y;
      for (let i = 2; i < n.length; i += 2) { x += n[i]; y += n[i + 1]; p[i] = x; p[i + 1] = y; }
      for (let i = 0; i < p.length; i += 2) { cx += p[i]; cy += p[i + 1]; }
      cx /= p.length / 2; cy /= p.length / 2;
      for (let i = 0; i < p.length; i += 2) r = Math.max(r, Math.hypot(p[i] - cx, p[i + 1] - cy));
      return { p, cx, cy, r };
    }));
    const N = scenes.length;
    const canvas = document.createElement('canvas');
    const ctx = canvas.getContext('2d');
    if (!ctx || !N) return;
    canvas.setAttribute('aria-hidden', 'true');
    art.appendChild(canvas);

    // a way out of the box, roughly away from the centre, on a slight curve, turning
    function flight(s) {
      let ang = Math.atan2(s.cy - CY, s.cx - CX);
      ang = Math.hypot(s.cx - CX, s.cy - CY) < 80 ? rnd(0, 2 * Math.PI) : ang + rnd(-0.45, 0.45);
      const dist = 660 + s.r + rnd(0, 160), bend = rnd(0.08, 0.24) * dist * side();
      return { dx: Math.cos(ang) * dist, dy: Math.sin(ang) * dist,
               bx: -Math.sin(ang) * bend, by: Math.cos(ang) * bend, rot: rnd(0.3, 0.9) * side() };
    }
    // one change: the lines of drawing b fly in, longest first. A line of drawing a leaves as soon as the first
    // new line that will lie near it enters the box, so the new lines take the place of the old ones.
    const CELL = 50, GX = Math.ceil(VW / CELL), GY = Math.ceil(VH / CELL);
    const grid = new Float64Array(GX * GY);
    const cell = (x, y) => Math.min(GY - 1, Math.max(0, Math.floor(y / CELL))) * GX
      + Math.min(GX - 1, Math.max(0, Math.floor(x / CELL)));
    function plan(a, b) {
      const B = scenes[b];
      const inc = B.map((s, j) => {
        const delay = Math.max(0, (j / B.length) * 950 + rnd(-90, 90)), dur = rnd(900, 1150);
        return Object.assign({ s, delay, dur, end: delay + dur }, flight(s));
      });
      const landed = Math.max(...inc.map((c) => c.end));
      grid.fill(Infinity);
      inc.forEach((c) => {
        const hit = c.delay + 0.15 * c.dur, p = c.s.p;
        for (let i = 0; i < p.length; i += 2) {
          const k = cell(p[i], p[i + 1]);
          if (hit < grid[k]) grid[k] = hit;
        }
      });
      const out = scenes[a].map((s) => {
        let hit = Infinity;
        const p = s.p;
        for (let i = 0; i < p.length; i += 2) {
          const gx = Math.floor(p[i] / CELL), gy = Math.floor(p[i + 1] / CELL);
          for (let v = gy - 1; v <= gy + 1; v++) {
            for (let u = gx - 1; u <= gx + 1; u++) {
              if (u >= 0 && v >= 0 && u < GX && v < GY && grid[v * GX + u] < hit) hit = grid[v * GX + u];
            }
          }
        }
        if (hit === Infinity) hit = rnd(0, landed * 0.45);   // nothing new lands here
        const dur = rnd(640, 800);
        return Object.assign({ s, delay: Math.min(hit + rnd(0, 120), landed * 0.55), dur }, flight(s));
      });
      return { inc, out, total: Math.max(landed, ...out.map((o) => o.delay + o.dur)) };
    }

    let dpr = 1, S = 1, ox = 0, oy = 0, color = '#435960';
    let from = N - 1, to = 0, cur = null, t0 = 0, clock = 0, hold = HOLD_START, last = 0, raf = 0;
    let paused = false, inView = true;

    function line(s, tx, ty, rot) {
      const X = s.cx + tx, Y = s.cy + ty;
      if (X + s.r < 0 || X - s.r > VW || Y + s.r < 0 || Y - s.r > VH) return;
      const c = Math.cos(rot), sn = Math.sin(rot), p = s.p;
      for (let i = 0; i < p.length; i += 2) {
        const x = p[i] - s.cx, y = p[i + 1] - s.cy;
        const px = ox + (X + x * c - y * sn) * S, py = oy + (Y + x * sn + y * c) * S;
        if (i) ctx.lineTo(px, py); else ctx.moveTo(px, py);
      }
    }
    function paint() {
      const t = clock - t0;
      ctx.setTransform(1, 0, 0, 1, 0, 0);
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      ctx.beginPath();
      if (!cur) {
        scenes[from].forEach((s) => line(s, 0, 0, 0));
      } else {
        cur.out.forEach((o) => {                 // leaving: accelerates away
          const k = Math.min(Math.max((t - o.delay) / o.dur, 0), 1);
          if (k >= 1) return;
          const e = k * k * k, w = Math.sin(Math.PI * e);
          line(o.s, o.dx * e + o.bx * w, o.dy * e + o.by * w, o.rot * e);
        });
        cur.inc.forEach((c) => {                 // arriving: slows down and lands
          const k = Math.min(Math.max((t - c.delay) / c.dur, 0), 1);
          if (k <= 0) return;
          const u = (1 - k) ** 3, w = Math.sin(Math.PI * u);
          line(c.s, c.dx * u + c.bx * w, c.dy * u + c.by * w, c.rot * u);
        });
      }
      ctx.lineWidth = dpr;                       // 1 CSS pixel
      ctx.lineCap = 'round';
      ctx.lineJoin = 'round';
      ctx.strokeStyle = color;
      ctx.stroke();
    }
    function tick(now) {
      raf = 0;
      clock += last ? Math.min(now - last, 50) : 0;
      last = now;
      if (!cur && clock - t0 >= hold) {
        to = (from + 1) % N;
        cur = plan(from, to);
        t0 = clock;
      }
      if (cur) {
        if (clock - t0 >= cur.total) {
          from = to; cur = null; t0 = clock;
          hold = from === N - 1 ? HOLD_END : HOLD;
        }
        paint();
      }
      run();
    }
    function run() {
      if (!raf && !paused && inView && !document.hidden) raf = requestAnimationFrame(tick);
    }
    function rest() {
      if (raf) cancelAnimationFrame(raf);
      raf = 0;
      last = 0;
    }
    function size() {
      const r = art.getBoundingClientRect();
      dpr = Math.min(window.devicePixelRatio || 1, 3);
      const w = Math.max(1, Math.round(r.width * dpr)), h = Math.max(1, Math.round(r.height * dpr));
      if (canvas.width !== w || canvas.height !== h) { canvas.width = w; canvas.height = h; }
      S = Math.min(w / VW, h / VH);
      ox = (w - VW * S) / 2;
      oy = (h - VH * S) / 2;
      color = getComputedStyle(art).color || color;
      paint();
    }
    function sync() {
      artBtn.classList.toggle('is-paused', paused);
      if (paused || !inView || document.hidden) rest(); else run();
    }

    size();                                      // the still, now drawn on the canvas
    still.style.visibility = 'hidden';
    artBtn.hidden = false;
    artBtn.addEventListener('click', () => { paused = !paused; sync(); });
    document.addEventListener('visibilitychange', sync);
    if (reduceMotion.addEventListener) {
      // motion switched off while running: finish the current drawing at once and stop there
      reduceMotion.addEventListener('change', () => {
        if (!reduceMotion.matches) return;
        if (cur) { from = to; cur = null; t0 = clock; }
        paused = true;
        sync();
        paint();
      });
    }
    if ('IntersectionObserver' in window) new IntersectionObserver(([en]) => { inView = en.isIntersecting; sync(); }).observe(art);
    if ('ResizeObserver' in window) new ResizeObserver(size).observe(art);
    else window.addEventListener('resize', size);
    sync();
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

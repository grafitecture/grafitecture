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

  /* ---------------- hero film ----------------
     A very light, silent loop behind the hero type. It is only loaded when motion is welcome and data is not
     scarce; otherwise the poster stays as a still image. The button pauses and resumes it (WCAG 2.2.2), and the
     film also rests while the hero is out of view or the tab is hidden. */
  const film = $('#hero-video');
  const filmBtn = $('#film-btn');
  if (film && filmBtn) {
    const reduce = window.matchMedia ? window.matchMedia('(prefers-reduced-motion: reduce)') : { matches: false };
    const saveData = !!(navigator.connection && navigator.connection.saveData);
    let userPaused = false, inView = true, started = false;
    const sync = () => {
      filmBtn.classList.toggle('is-paused', userPaused);
      if (!started) return;
      if (!userPaused && inView && !document.hidden) {
        const p = film.play();
        // autoplay refused (e.g. iOS low-power mode): show "play", so a tap can start it
        if (p && p.catch) p.catch(() => { userPaused = true; filmBtn.classList.add('is-paused'); });
      } else {
        film.pause();
      }
    };
    const start = () => {
      // H.264 MP4 (1920 px) where supported, otherwise the small VP9 WebM
      const h264 = film.canPlayType('video/mp4; codecs="avc1.640028"');
      film.src = h264 ? film.dataset.mp4 : film.dataset.webm;
      film.muted = true;
      started = true;
      filmBtn.hidden = false;
      film.addEventListener('error', () => { filmBtn.hidden = true; }, { once: true });
      sync();
    };
    if (!reduce.matches && !saveData) {
      filmBtn.addEventListener('click', () => { userPaused = !userPaused; sync(); });
      if ('IntersectionObserver' in window) {
        new IntersectionObserver(([en]) => { inView = en.isIntersecting; sync(); }).observe(film);
      }
      document.addEventListener('visibilitychange', sync);
      if (reduce.addEventListener) reduce.addEventListener('change', () => { if (reduce.matches) { userPaused = true; sync(); } });
      if (document.readyState === 'complete') start();
      else window.addEventListener('load', start, { once: true });
    }
  }

  /* ---------------- headlines: now and then a lime wave runs through the grey type ----------------
     First pass shortly after a headline comes into view, then every 8–14 s while it stays there.
     No waves with reduced motion or forced colours; the type then simply stays #435960. */
  const heads = $$('.hero h1, .sec-head h2, .legal-hd h2');
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

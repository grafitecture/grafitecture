// Port of sheen() from grafitecture.de (src/app.js, Martin 28.10.2026): two colours of the wheel play on a field.
// Here driven by an explicit clock (seconds) so stills and reel frames are reproducible.
(function () {
  const WHEEL = 'dafd55 a7ff00 4bff00 00ff7b 00ffab 00ffca 00ffe2 00fff6 00f4ff 00e3ff 60dbff 82d7ff 96d3ff a4d0ff b0cdff bacbff c3c9ff cdc5ff d7c2ff e3beff f3b8ff ffb3f7 ffb6e5 ffb8d8 ffb9cd ffbac3 ffbbb9 ffbcb0 ffbda5 ffbe99 ffbf8a ffc074 ffc24d ffcc00 ffe300 fdff00'
    .split(' ').map((c) => [0, 2, 4].map((i) => parseInt(c.slice(i, i + 2), 16)));
  const AREAS = [
    [0.15, 0.20, 0.14, 0.10, 97, 131, 0.62],
    [0.70, 0.85, 0.16, 0.10, 127, 101, 0.66],
    [0.85, 0.25, 0.12, 0.14, 113, 89, 0.58],
    [0.30, 0.75, 0.10, 0.12, 89, 149, 0.52],
  ];
  const SPEED = 4, TURN = 288, GAP = [80, 20, 197], SOFT = 2, FADE = 4, TAU = Math.PI * 2;
  const BAYER = [0, 8, 2, 10, 12, 4, 14, 6, 3, 11, 1, 9, 15, 7, 13, 5].map((v) => (v + 0.5) / 16 - 0.5);
  const lin = (v) => (v <= 10.31475 ? v / 3294.6 : ((v / 255 + 0.055) / 1.055) ** 2.4);
  const enc = (l) => 255 * (l <= 0.0031308 ? 12.92 * l : 1.055 * l ** (1 / 2.4) - 0.055);
  function wheel(deg) {
    const u = (((deg / 10) % 36) + 36) % 36, k = Math.floor(u), f = u - k, a = WHEEL[k], b = WHEEL[(k + 1) % 36];
    return [0, 1, 2].map((c) => lin(a[c] + (b[c] - a[c]) * f));
  }
  // paint the canvas cv (CSS size w x h, RES CSS px per canvas px) at clock seconds; speed scales motion
  window.paintSheen = function (cv, clock, RES, opts) {
    opts = opts || {};
    const rect = cv.getBoundingClientRect();
    const w = rect.width, h = rect.height;
    const W = Math.max(8, Math.ceil(w / RES)), H = Math.max(8, Math.ceil(h / RES));
    if (cv.width !== W) cv.width = W;
    if (cv.height !== H) cv.height = H;
    const g = cv.getContext('2d');
    const img = g.createImageData(W, H);
    const t = clock * SPEED, e = opts.noFade ? 1 : Math.min(1, clock / FADE), ramp = e * e * (3 - 2 * e), m = Math.max(w, h);
    const hue = (360 * t) / TURN + (opts.hueOffset || 0), gap = GAP[0] + GAP[1] * Math.sin((TAU * t) / GAP[2]);
    const ca = wheel(ramp * hue), cb = wheel(ramp * (hue + gap));
    const mix = new Float32Array(256 * 3);
    for (let k = 0; k < 256; k++) for (let c = 0; c < 3; c++) mix[k * 3 + c] = enc(ca[c] + ((cb[c] - ca[c]) * k) / 255);
    const xs = AREAS.map(() => new Float32Array(W)), ys = AREAS.map(() => new Float32Array(H));
    AREAS.forEach(([x, y, dx, dy, px, py, r], n) => {
      const cx = (x + dx * Math.sin((TAU * t) / px)) * w, cy = (y + dy * Math.sin((TAU * t) / py + 1.3)) * h;
      const k = SOFT / (r * m) ** 2;
      for (let i = 0; i < W; i++) xs[n][i] = Math.exp(-k * ((i + 0.5) * RES - cx) ** 2);
      for (let j = 0; j < H; j++) ys[n][j] = Math.exp(-k * ((j + 0.5) * RES - cy) ** 2);
    });
    const d = img.data, [X0, X1, X2, X3] = xs;
    let p = 0;
    for (let j = 0; j < H; j++) {
      const y0 = ys[0][j], y1 = ys[1][j], y2 = ys[2][j], y3 = ys[3][j];
      for (let i = 0; i < W; i++) {
        const a = X0[i] * y0 + X1[i] * y1, b = X2[i] * y2 + X3[i] * y3;
        let s = b / (a + b || 1);
        s = s * s * (3 - 2 * s);
        s = s * s * (3 - 2 * s);
        const q = Math.round(s * 255) * 3, dz = BAYER[((j & 3) << 2) | (i & 3)];
        d[p] = mix[q] + dz; d[p + 1] = mix[q + 1] + dz; d[p + 2] = mix[q + 2] + dz; d[p + 3] = 255;
        p += 4;
      }
    }
    g.putImageData(img, 0, 0);
    return { a: ca.map(enc).map(Math.round), b: cb.map(enc).map(Math.round) };
  };
})();

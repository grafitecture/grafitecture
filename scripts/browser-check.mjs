#!/usr/bin/env node
// Browser checks for CI (needs `npm i --no-save playwright @axe-core/playwright` and a Chromium):
// every page at 390 and 1512 px, both languages, with reduced motion:
//   - axe-core, WCAG 2.0/2.1/2.2 A and AA: 0 violations
//   - first load contacts no other host than the site itself (no third parties before consent, Phase 11)
//   - no console errors (CSP violations show up here)
//   - no horizontal scrolling at 320 px
//   node scripts/browser-check.mjs [BASE_URL]
import { chromium } from 'playwright';
import { AxeBuilder } from '@axe-core/playwright';

const BASE = (process.argv[2] || process.env.BASE_URL || 'http://127.0.0.1:8080').replace(/\/$/, '');
const PAGES = ['/', '/en', '/impressum', '/datenschutz', '/en/legal-notice', '/en/privacy-policy'];
const own = new URL(BASE).host;
let failures = 0;
const fail = (msg) => { failures++; console.log('✖ ' + msg); };

const browser = await chromium.launch();
for (const width of [390, 1512]) {
  for (const path of PAGES) {
    const ctx = await browser.newContext({ viewport: { width, height: 900 }, reducedMotion: 'reduce' });
    const page = await ctx.newPage();
    const hosts = new Set(); const errors = [];
    page.on('request', (r) => { try { hosts.add(new URL(r.url()).host); } catch { /* data: */ } });
    page.on('console', (m) => { if (m.type() === 'error') errors.push(m.text()); });
    page.on('pageerror', (e) => errors.push(String(e)));
    await page.goto(BASE + path, { waitUntil: 'networkidle' });
    const where = `${path} @${width}px`;
    const foreign = [...hosts].filter((h) => h && h !== own);
    if (foreign.length) fail(`${where}: contacts other hosts on first load: ${foreign.join(', ')}`);
    if (errors.length) fail(`${where}: console errors: ${errors.join(' | ')}`);
    const res = await new AxeBuilder({ page }).withTags(['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa', 'wcag22aa']).analyze();
    for (const v of res.violations) {
      fail(`${where}: axe ${v.id} (${v.impact}): ${v.help} – ${v.nodes.slice(0, 3).map((n) => n.target.join(' ')).join(', ')}`);
    }
    await ctx.close();
  }
}
for (const path of PAGES) {
  const page = await browser.newPage({ viewport: { width: 320, height: 700 } });
  await page.goto(BASE + path, { waitUntil: 'networkidle' });
  const sw = await page.evaluate(() => document.documentElement.scrollWidth);
  if (sw > 320) fail(`${path} @320px: horizontal scrolling (${sw}px wide)`);
  await page.close();
}
await browser.close();
console.log(failures ? `\n${failures} problems` : '\nBrowser checks: axe 0 violations, no third parties, no console errors, no horizontal scrolling.');
process.exit(failures ? 1 : 0);

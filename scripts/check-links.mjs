#!/usr/bin/env node
// Link check over the built site (public/*.html): every internal href/src/srcset, canonical, hreflang alternate and
// og:image must answer 200 directly (no redirect, no 404). External links are listed with their status in
// seo/link-report.md; they only fail the run with --strict (other sites change without us).
//
//   node scripts/check-links.mjs [BASE_URL] [--external] [--strict]     default BASE_URL http://127.0.0.1:8080
import { readFileSync, readdirSync, statSync, writeFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, join, relative } from 'node:path';

const ROOT = join(dirname(fileURLToPath(import.meta.url)), '..');
const PUB = join(ROOT, 'public');
const args = process.argv.slice(2);
const BASE = (args.find((a) => !a.startsWith('--')) || process.env.BASE_URL || 'http://127.0.0.1:8080').replace(/\/$/, '');
const EXTERNAL = args.includes('--external');
const STRICT = args.includes('--strict');
const SITE = 'https://www.grafitecture.de';

const files = [];
(function walk(d) { for (const f of readdirSync(d)) { const p = join(d, f); if (statSync(p).isDirectory()) walk(p); else if (p.endsWith('.html')) files.push(p); } })(PUB);

function pagePath(file) {
  const rel = '/' + relative(PUB, file).replace(/\\/g, '/');
  if (rel === '/index.html') return '/';
  return rel.replace(/\.html$/, '');
}

const found = new Map();   // url -> Set of pages
for (const f of files) {
  if (f.endsWith('404.html')) continue;   // the 404 page uses absolute links only and is checked by its own test
  const html = readFileSync(f, 'utf8');
  const from = pagePath(f);
  const urls = [];
  for (const m of html.matchAll(/\s(?:href|src)="([^"]+)"/g)) urls.push(m[1]);
  for (const m of html.matchAll(/\ssrcset="([^"]+)"/g)) for (const part of m[1].split(',')) urls.push(part.trim().split(/\s+/)[0]);
  for (const m of html.matchAll(/<meta property="og:(?:image|url)" content="([^"]+)"/g)) urls.push(m[1]);
  for (const u of urls) {
    if (/^(mailto:|tel:|data:|#|javascript:)/.test(u)) continue;
    const abs = new URL(u, SITE + from).href.split('#')[0];
    if (!found.has(abs)) found.set(abs, new Set());
    found.get(abs).add(from);
  }
}

async function status(url) {
  const internal = url.startsWith(SITE);
  const target = internal ? BASE + url.slice(SITE.length) : url;
  const opts = { redirect: 'manual', headers: { 'user-agent': 'Mozilla/5.0 (grafitecture link check)' }, signal: AbortSignal.timeout(15000) };
  try {
    let r = await fetch(target, { ...opts, method: 'HEAD' });
    if (r.status === 405 || r.status === 403) r = await fetch(target, { ...opts, method: 'GET' });
    return { status: r.status, location: r.headers.get('location') };
  } catch (e) { return { status: 0, location: e.cause?.code || e.name }; }
}

let errors = 0; const intRows = []; const extRows = [];
for (const [url, pages] of [...found].sort()) {
  const internal = url.startsWith(SITE);
  if (!internal && !EXTERNAL) continue;
  const r = await status(url);
  const good = r.status === 200;
  const where = [...pages].join(', ');
  if (internal) {
    if (!good) errors++;
    intRows.push(`| \`${url.slice(SITE.length) || '/'}\` | ${r.status}${r.location ? ' → ' + r.location : ''} | ${good ? '✅' : '❌'} | ${where} |`);
  } else {
    if (!good && STRICT) errors++;
    extRows.push(`| ${url} | ${r.status}${r.location ? ' → ' + r.location : ''} | ${good ? '✅' : '⚠️'} | ${where} |`);
  }
}

const report = `# Link-Report

Geprüft: ${files.length - 1} Seiten aus \`public/\` gegen \`${BASE}\`, ${new Date().toISOString().slice(0, 16).replace('T', ' ')} UTC.
Interne Links müssen direkt 200 liefern (keine Weiterleitung, kein 404). **${errors ? errors + ' Fehler' : 'Alle internen Links in Ordnung'}.**

## Intern (${intRows.length})

| Adresse | Antwort | | Seiten |
|---|---|---|---|
${intRows.join('\n')}
${EXTERNAL ? `
## Extern (${extRows.length}, nur Hinweis${STRICT ? '' : ', bricht den Lauf nicht ab'})

| Adresse | Antwort | | Seiten |
|---|---|---|---|
${extRows.join('\n')}
` : ''}`;
writeFileSync(join(ROOT, 'seo', 'link-report.md'), report);
console.log(report);
process.exit(errors ? 1 : 0);

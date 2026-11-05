#!/usr/bin/env node
// npm run seo:check – everything that must stay green before a push:
//   1. build is in sync      python3 build.py, then public/, vercel.json and seo/lastmod.json must be unchanged
//   2. pages, sitemap, robots, CSP, security.txt     python3 scripts/seo_check.py
//   3. internal links        node scripts/check-links.mjs   (against scripts/serve.py, a local stand-in for Vercel)
//   4. redirects and 404s    node scripts/check-redirects.mjs
//   5. --full (in CI): Lighthouse CI with budgets, axe in a real browser (needs npm access, see .github/workflows)
// Stops at the first failing step with exit code 1.
import { spawn, spawnSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';

const ROOT = join(dirname(fileURLToPath(import.meta.url)), '..');
const FULL = process.argv.includes('--full');
const PORT = process.env.PORT || '8080';
const BASE = `http://127.0.0.1:${PORT}`;

function step(name, cmd, args, env = {}) {
  console.log(`\n▶ ${name}`);
  const r = spawnSync(cmd, args, { cwd: ROOT, stdio: 'inherit', env: { ...process.env, ...env } });
  if (r.status !== 0) { console.error(`✖ ${name} failed`); process.exit(1); }
  console.log(`✔ ${name}`);
}

step('build', 'python3', ['build.py']);
const diff = spawnSync('git', ['status', '--porcelain', '--', 'public', 'vercel.json', 'seo/lastmod.json'], { cwd: ROOT, encoding: 'utf8' });
if (diff.stdout.trim()) {
  console.log(diff.stdout);
  if (process.env.CI) { console.error('✖ public/ is not in sync with src/: run python3 build.py and commit the result'); process.exit(1); }
  console.log('ℹ public/ changed by the build: commit it together with the source change');
}
step('pages, sitemap, robots, CSP', 'python3', ['scripts/seo_check.py']);

const server = spawn('python3', ['scripts/serve.py', PORT], { cwd: ROOT, stdio: 'ignore' });
const stop = () => { try { server.kill(); } catch { /* ignore */ } };
process.on('exit', stop);
for (let i = 0; i < 50; i++) {
  try { await fetch(BASE + '/robots.txt'); break; } catch { await new Promise((r) => setTimeout(r, 100)); }
}
step('internal links', 'node', ['scripts/check-links.mjs', BASE]);
step('redirects and 404', 'node', ['scripts/check-redirects.mjs', BASE]);
if (FULL) {
  step('Lighthouse CI (mobile, budgets)', 'npx', ['--yes', '@lhci/cli@0.15.1', 'autorun', '--config=lighthouserc.json']);   // URLs: port 8080
  step('browser: axe, network, console', 'node', ['scripts/browser-check.mjs', BASE]);
}
stop();
console.log('\nAll checks passed.');

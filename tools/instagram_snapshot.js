// Instagram section of the website (Martin 20.11.2026), step 1 of 2.
// Run in the built-in browser (javascript tool) on https://www.instagram.com/g.r.a.f.i.t.e.c.t.u.r.e/ once the grid
// has loaded. Takes the first 12 tiles of the profile grid, in the order Instagram shows them (pinned posts first),
// fetches their images and downloads ONE file, grafitecture-instagram-feed.json, with the images as base64.
// Step 2: python3 tools/instagram_feed.py grafitecture-instagram-feed.json, then python3 build.py.
// Nothing here runs on the website; the site only serves the copies and links to the posts.
(async () => {
  const N = 12;
  const tiles = [...document.querySelectorAll('main a[href*="/p/"], main a[href*="/reel/"]')].slice(0, N);
  const toB64 = (blob) => new Promise((ok) => { const fr = new FileReader(); fr.onload = () => ok(fr.result.split(',')[1]); fr.readAsDataURL(blob); });
  const items = [];
  for (const [i, a] of tiles.entries()) {
    const img = a.querySelector('img');
    const blob = await (await fetch(img.src)).blob();
    const bmp = await createImageBitmap(blob);
    items.push({ i, href: a.getAttribute('href'), type: blob.type, w: bmp.width, h: bmp.height, data: await toB64(blob) });
  }
  const json = JSON.stringify({ taken: new Date().toISOString(), profile: location.href, items });
  const url = URL.createObjectURL(new Blob([json], { type: 'application/json' }));
  const dl = Object.assign(document.createElement('a'), { href: url, download: 'grafitecture-instagram-feed.json' });
  document.body.appendChild(dl); dl.click(); dl.remove();
  return { posts: items.length, bytes: json.length, codes: items.map((x) => x.href) };
})();

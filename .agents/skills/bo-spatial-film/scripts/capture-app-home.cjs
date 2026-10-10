// Onboard each app, seed a mock library straight into its Dexie IndexedDB, reload, shoot the home screen.
const { chromium } = require(process.env.PLAYWRIGHT_PATH || 'playwright');
const OUT = process.argv[2];

// Runs in the page: draws a cover on a canvas and returns a PNG Blob.
const COVER_FN = `
window.__cover = (w, h, bg, fg, title, sub, motif) => new Promise(res => {
  const c = document.createElement('canvas'); c.width = w; c.height = h; const x = c.getContext('2d');
  const g = x.createLinearGradient(0, 0, w, h); g.addColorStop(0, bg[0]); g.addColorStop(1, bg[1]);
  x.fillStyle = g; x.fillRect(0, 0, w, h);
  x.globalAlpha = .9; x.strokeStyle = fg; x.fillStyle = fg; x.lineWidth = w * .012;
  if (motif === 'disc') { x.beginPath(); x.arc(w * .5, h * .46, w * .26, 0, 7); x.stroke(); x.beginPath(); x.arc(w * .5, h * .46, w * .05, 0, 7); x.fill(); }
  if (motif === 'sun') { x.beginPath(); x.arc(w * .5, h * .5, w * .2, 0, 7); x.fill(); x.fillRect(0, h * .62, w, h * .015); }
  if (motif === 'wave') { for (let i = 0; i < 4; i++) { x.beginPath(); for (let k = 0; k <= w; k += 4) x.lineTo(k, h * (.4 + i * .08) + Math.sin(k / w * 6.28 * 2 + i) * h * .03); x.stroke(); } }
  if (motif === 'rule') { x.fillRect(w * .12, h * .2, w * .76, h * .006); x.fillRect(w * .12, h * .8, w * .76, h * .006); }
  x.globalAlpha = 1; x.textAlign = 'center';
  if (title) { x.font = '600 ' + Math.round(w * .095) + 'px Georgia, serif'; const words = title.split(' '); let line = '', y = h * .38, lines = [];
    for (const wd of words) { if (x.measureText(line + wd).width > w * .74) { lines.push(line.trim()); line = ''; } line += wd + ' '; } lines.push(line.trim());
    lines.forEach((l, i) => x.fillText(l, w / 2, y + i * w * .12)); }
  if (sub) { x.font = '400 ' + Math.round(w * .055) + 'px Georgia, serif'; x.fillText(sub, w / 2, h * .72); }
  c.toBlob(res, 'image/png');
});`;

// Raw IndexedDB put (Dexie DBs open at their current version when no version is passed).
async function seed(p, dbName, rows) {
  await p.evaluate(async ({ dbName, rows }) => {
    const db = await new Promise((res, rej) => { const r = indexedDB.open(dbName); r.onsuccess = () => res(r.result); r.onerror = () => rej(r.error); });
    for (const [store, items] of Object.entries(rows)) {
      for (const it of items) {
        if (it.__cover) { it[it.__cover.field] = await window.__cover(...it.__cover.args); delete it.__cover; }
        for (const k of Object.keys(it)) if (it[k] && it[k].__date) it[k] = new Date(it[k].__date);
        if (it.fileData === '__buf') it.fileData = new ArrayBuffer(16);
        await new Promise((res, rej) => { const t = db.transaction(store, 'readwrite'); t.objectStore(store).put(it); t.oncomplete = res; t.onerror = () => rej(t.error); });
      }
    }
    db.close();
  }, { dbName, rows });
}

// Merge fields into every existing record of a store (the app's settings row after onboarding), plus optional localStorage keys.
async function patchStore(p, dbName, store, fields, ls) {
  await p.evaluate(async ({ dbName, store, fields, ls }) => {
    for (const [k, v] of Object.entries(ls || {})) localStorage.setItem(k, v);
    const db = await new Promise((res, rej) => { const r = indexedDB.open(dbName); r.onsuccess = () => res(r.result); r.onerror = () => rej(r.error); });
    await new Promise((res, rej) => {
      const t = db.transaction(store, 'readwrite'); const os = t.objectStore(store);
      os.openCursor().onsuccess = e => { const c = e.target.result; if (c) { c.update(Object.assign(c.value, fields)); c.continue(); } };
      t.oncomplete = res; t.onerror = () => rej(t.error);
    });
    db.close();
  }, { dbName, store, fields, ls });
}

const d = (minsAgo) => ({ __date: new Date(Date.now() - minsAgo * 60000).toISOString() });

const songs = [
  ['Kape at Midnight', 'Low Tide Club', ['#3B1E54', '#9B7EBD'], '#F5EFFF', 'disc', 214],
  ['Rainy Manila', 'Sari-Sari Radio', ['#1F4E5F', '#79A3B1'], '#FFFFFF', 'wave', 187],
  ['Golden Hour Jeep', 'Paraluman', ['#E8A23A', '#F3D27A'], '#5B2C0A', 'sun', 201],
  ['Slow Sunday', 'Low Tide Club', ['#5E3023', '#C08552'], '#FFF4E6', 'disc', 243],
  ['Night Shift, US Hours', 'Celery & Co.', ['#0B1B33', '#2D78C2'], '#DCEBFA', 'wave', 176],
  ['Tagaytay Fog', 'Paraluman', ['#6A7B76', '#C7D3D4'], '#FFFFFF', 'sun', 229],
].map(([title, artist, bg, fg, motif, dur], i) => ({
  id: 'demo-song-' + i, title, artist, album: artist + ' Sessions', fileData: '__buf', fileSize: 4200000 + i * 310000, fileType: 'mp3',
  duration: dur, addedAt: d(600 + i * 90), lastPlayedAt: d(30 + i * 45), playCount: 12 - i, isFavorite: i % 2 === 0, deletedAt: null, source: 'import',
  __cover: { field: 'coverImage', args: [600, 600, bg, fg, '', '', motif] },
}));

const books = [
  ['The Great Gatsby', 'F. Scott Fitzgerald', ['#0B1B33', '#1F4E79'], '#E8C872', 64],
  ['Pride and Prejudice', 'Jane Austen', ['#7B2D26', '#B5523B'], '#FFF4E6', 38],
  ['Frankenstein', 'Mary Shelley', ['#2F3E46', '#52796F'], '#F1FAEE', 12],
  ['Alice in Wonderland', 'Lewis Carroll', ['#E9C46A', '#F4A261'], '#3D2614', 100],
  ['Dracula', 'Bram Stoker', ['#1B1B1B', '#5C1A1B'], '#F2E8CF', 0],
  ['The Odyssey', 'Homer', ['#264653', '#2A9D8F'], '#FFFFFF', 0],
].map(([title, author, bg, fg, prog], i) => ({
  id: 'demo-book-' + i, title, author, fileData: '__buf', fileSize: 380000 + i * 52000, fileType: 'epub',
  addedAt: d(2000 + i * 300), lastReadAt: d(20 + i * 400), readingProgress: prog, currentCfi: '', isFavorite: i === 0, deletedAt: null,
  __cover: { field: 'coverImage', args: [400, 600, bg, fg, title, author, 'rule'] },
}));

const jobs = [
  // Match the look of the app's own store/landing screenshots: Celery Music light theme + list view, Lettuce Read dark theme.
  { name: 'home-celery', url: 'http://127.0.0.1:5181/', db: 'celery-music', rows: { songs }, taps: ['Skip', "Let's go!", 'Continue', 'Done'],
    patch: { store: 'settings', fields: { theme: 'light', libraryView: 'list' } } },
  { name: 'home-lettuce', url: 'http://127.0.0.1:5182/', db: 'muglit', rows: { books }, taps: ['Skip', 'Continue', "Let's go!", 'Done'],
    patch: { store: 'settings', fields: { theme: 'dark' }, ls: { 'lettuce-read-theme': 'dark' } } },
];

(async () => {
  const b = await chromium.launch();
  for (const j of jobs) {
    const ctx = await b.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 3, isMobile: true, hasTouch: true });
    await ctx.addInitScript(COVER_FN);
    const p = await ctx.newPage();
    try {
      await p.goto(j.url, { waitUntil: 'networkidle', timeout: 60000 });
      await p.waitForTimeout(2000);
      for (let i = 0; i < 8; i++) {
        const inp = p.locator('input[type="text"], input:not([type])').first();
        if (await inp.isVisible().catch(() => false) && !(await inp.inputValue().catch(() => ''))) await inp.fill('Kenneth').catch(() => {});
        let tapped = false;
        for (const t of j.taps) { const el = p.getByText(t, { exact: true }).first(); if (await el.isVisible().catch(() => false)) { await el.click().catch(() => {}); tapped = true; break; } }
        if (!tapped) break;
        await p.waitForTimeout(1200);
      }
      await seed(p, j.db, j.rows);
      if (j.patch) await patchStore(p, j.db, j.patch.store, j.patch.fields, j.patch.ls);
      await p.reload({ waitUntil: 'networkidle' });
      await p.waitForTimeout(3000);
      await p.screenshot({ path: `${OUT}/${j.name}.png` });
      console.log('ok', j.name);
    } catch (e) { console.log('FAIL', j.name, e.message); }
    await ctx.close();
  }
  await b.close();
})();

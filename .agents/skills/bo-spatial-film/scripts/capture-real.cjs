// Capture REAL material for a film: live sites (desktop 2x, hero + scroll strip) and app builds (phone 3x,
// taps past onboarding and fills name prompts so it reaches the real home screen). One PNG per step, so you
// pick the frame that looks finished (an empty state reads unfinished on film; a branded first screen may be better).
//
// usage: node capture-real.cjs <jobs.json> <outDir>
// jobs.json: [{ "name": "site-portfolio", "url": "https://...", "kind": "site" },
//             { "name": "app-celery", "url": "http://127.0.0.1:5181/", "kind": "app",
//               "taps": ["Skip", "Let's go!", "Continue"], "fill": "Kenneth" }]
// Serve an app build first: `python -m http.server 5181 --bind 127.0.0.1` inside its dist/ folder.
// Playwright: PLAYWRIGHT_PATH or a local `npm i -D playwright`.
const fs = require('fs');
const { chromium } = require(process.env.PLAYWRIGHT_PATH || 'playwright');
const [, , jobsPath, OUT] = process.argv;
if (!jobsPath || !OUT) { console.error('usage: node capture-real.cjs <jobs.json> <outDir>'); process.exit(1); }
const jobs = JSON.parse(fs.readFileSync(jobsPath, 'utf8'));
fs.mkdirSync(OUT, { recursive: true });

(async () => {
  const b = await chromium.launch();
  for (const j of jobs) {
    const app = j.kind === 'app';
    const ctx = await b.newContext(app
      ? { viewport: { width: 390, height: 844 }, deviceScaleFactor: 3, isMobile: true, hasTouch: true }
      : { viewport: { width: 1440, height: 900 }, deviceScaleFactor: 2, reducedMotion: 'reduce' });
    const p = await ctx.newPage();
    try {
      await p.goto(j.url, { waitUntil: 'networkidle', timeout: 60000 });
      await p.waitForTimeout(2500);
      if (!app) {
        await p.screenshot({ path: `${OUT}/${j.name}.png` });
        // scroll through so lazy images and reveals fire, then a full-page shot (crop a strip from it later)
        const H = await p.evaluate(() => document.body.scrollHeight);
        for (let y = 0; y < H; y += 600) { await p.evaluate(v => window.scrollTo(0, v), y); await p.waitForTimeout(150); }
        await p.evaluate(() => window.scrollTo(0, 0)); await p.waitForTimeout(800);
        await p.screenshot({ path: `${OUT}/${j.name}-full.png`, fullPage: true });
      } else {
        await p.screenshot({ path: `${OUT}/${j.name}-0.png` });
        for (let i = 1; i <= 8; i++) {
          const inp = p.locator('input[type="text"], input:not([type])').first();
          if (j.fill && await inp.isVisible().catch(() => false) && !(await inp.inputValue().catch(() => ''))) await inp.fill(j.fill).catch(() => {});
          let tapped = false;
          for (const t of (j.taps || ['Skip', 'Continue', 'Next', 'Get started', 'Get Started', 'Done'])) {
            const el = p.getByText(t, { exact: true }).first();
            if (await el.isVisible().catch(() => false)) { await el.click().catch(() => {}); tapped = true; break; }
          }
          if (!tapped) break;
          await p.waitForTimeout(1500);
          await p.screenshot({ path: `${OUT}/${j.name}-${i}.png` });
        }
      }
      console.log('ok', j.name);
    } catch (e) { console.log('FAIL', j.name, e.message); }
    await ctx.close();
  }
  await b.close();
})();

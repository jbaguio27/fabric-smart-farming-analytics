# Phase 2 - Design truth, kit, pre-rendered surfaces

Goal: every worker builds from the same files, so 5 independent scenes look like one film.

## frame.md (fill `template/frame.md`)

Fill every `{{...}}`: tokens from the product's stylesheet (check ink-faint passes AA on the paper - BrewedShot's
had to go #5b6890 -> #505c86), font, kit component list, asset table with native px, BPM/beat/bar, and the seam
table with exact times (`python <skill>/scripts/make-harness.py` prints every scene's duration; seam time =
cumulative). Never loosen the camera rig, flattening traps or smoothness law - they are why it plays at 60fps.

## Kit (`assets/kit.css` + `references/snippets.html`)

- Replace the `:root` token values with the product's. Keep the base components.
- Port the product's own UI 1:1 from its source CSS below the marker line, classes prefixed `kit-` (BrewedShot:
  the whole popup - header, tabs, IN FRAME card, switches, CTA, result block, action row - from popup.css +
  theme.css). Add its markup to snippets.html, including every state a scene needs (idle, busy, result).
- Product mark: a vector SVG rebuilt from the real icon (crisp at any zoom).
- The font: ship the product's real woff2 in `assets/fonts/` (template ships Poppins 500/700 + OFL).

## The product's own screens: capture the real app (best truth)

When the product runs locally, capture it instead of rebuilding it (KAPEVault, 2026-10-04: 17 surfaces, one agent,
~6 min). Electron: Playwright `_electron.launch` with `--force-device-scale-factor=2`, `setContentSize` to the CSS
size you want (Windows adds a 1px frame edge - check the PNG is exactly 2x), a throwaway data dir seeded with mock
data through the app's own bridge, `page.screenshot` / element screenshots. Web/mobile: Playwright Chromium with
`deviceScaleFactor: 2` against the app's mock mode. Traps: OS materials (acrylic, vibrancy) are invisible to page
screenshots - inject an opaque backdrop sampled from a real screenshot; scrub every machine path and real name in
the DOM before each shot (a seeded temp folder printed its full machine path in a list row); stretch auto-hide timers in
the page to catch transient states; write a MAP of 1x element boxes (getBoundingClientRect) in the same run so
workers can lay live overlays exactly on the capture. Keep the capture scripts in `src/captures/app/`.
A website product: build it, serve `dist/` (`python -m http.server`), inject CSS that kills animations,
canvas grounds and reveal states, element-screenshot each component at 2x, and dump a 1x box map + computed
styles in the same run - the kit ports from those resolved values (worked example: a
film project's `src/captures/app/capture-site.cjs`). Scrub prices or anything the film
must not show in the DOM before the shot (e.g. a Package select set to "Still deciding").

**Showreel / personal films: phones show real in-app screens, never a cropped landing page** (Kenneth, 2026-10-07,
rejected desktop marketing pages squeezed into phone frames). `scripts/capture-real.cjs <jobs.json> <out>` shoots each
app's served `dist/` at 390x844 @3x, taps past onboarding and fills name prompts, saving every step; it also shoots live
sites (1440x900 @2x hero + full page for a scroll strip). **Show the home screen, never onboarding** (Kenneth rejected
welcome screens the same day). An empty home ("No music yet") reads unfinished, so seed it:
`scripts/capture-app-home.cjs` is the worked example. It onboards, writes mock rows straight into the app's Dexie
IndexedDB (raw `indexedDB.open(name)` opens the current version; canvas-drawn cover Blobs; public-domain books, invented
track names), reloads and shoots. Read the app's `src/lib/db.ts` + types for the store and field names first. **Match the look the
user already shows publicly** (store listing, landing page, portfolio shot): set the same theme and view through the
settings row (`patch` in the jobs), and build the CURRENT source into scratch (`npx vite build --outDir <scratch>`)
because a repo's `dist/` can be months stale. Kenneth, 2026-10-08: "how come they don't look like this?" - the default
cream theme from a March build did not match his landing pages (Celery Music light + list, Lettuce Read dark). Device screenshots (1080x2400) and `docs/screenshots/` in
the app repo work too; crop the status and gesture bars. Find an app's source by its in-app name, not the folder name
(Lettuce Read lives in `MugLit/`).

## Pre-rendered surfaces (`src/captures/` -> `assets/captures/*.png`)

Anything shown in more than one scene, or heavier than a few DOM nodes (a third-party canvas, a long web page),
is an HTML file rendered ONCE to a 2x PNG:

1. Write `src/captures/<name>.html`, the surface wrapped in `<div id="surface">` at its 1x size; optional shared
   icon symbols in `src/captures/sprite.svg` (inserted at `<!--SPRITE-->`).
2. Third-party builders: copy the ready rebuilds from `<skill>/surfaces/` (GHL, n8n, Zapier, a long Northwind
   marketing page + branded variant) and re-skin the data; specs in `references/platform-canvases.md`. A new
   platform: measure the user's real captures and write its spec the same way.
3. List jobs in `src/captures/jobs.json` (`file, out, w, h, scale, bodyClass?`) and run
   `node <skill>/scripts/capture-surfaces.cjs`.
4. Annotation/crop targets: `node <skill>/scripts/measure-surface.cjs src/captures/<name>.html "<selector>"`,
   paste the 1x boxes into snippets.html "CAPTURE MAP" and cite them in the storyboard blocks.
5. **Look at every PNG** (Read tool) next to the real capture before moving on.

Rules: fictional data only, never real client names, real captures never embedded. Show a capture at or below
native resolution. Tiles of a capture are leaf divs using the PNG as background-image with the exact crop.

## Gate

`frame.md` and `references/worker-brief.md` have no `{{` left (`grep -c "{{" frame.md references/worker-brief.md`), kit tokens are the product's, every PNG has been looked
at, `film.json` scenes match the storyboard durations.

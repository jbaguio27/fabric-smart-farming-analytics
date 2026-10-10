# Microsoft Fabric Cinematic Showcase: Production Plan & Technical Specifications
**Project**: HydroGrow Smart Farming Analytics Platform Showcase Film  
**Target Duration**: Exactly 102.015s (45 Musical Bars @ 106.8 BPM)  
**Render Output**: 1920 × 1080 Landscape @ 60 fps (H.264 CRF 21, AAC Stereo)  
**Production Skill**: `bo-spatial-film` (`.agents/skills/bo-spatial-film/`)  
**Rendering Engine**: HyperFrames CLI (`hyperframes@0.8.117`) with Hardware GPU Acceleration  

---

## 1. Technical Architecture & Tooling Environment

### 1.1 Verified Local Hardware & Runtime Stack
- **Operating System**: Windows 11 64-bit (PowerShell shell environment).
- **GPU Hardware**: AMD Radeon RX 6600 (Hardware GPU acceleration enabled for headless browser rendering).
- **Node.js**: Node v22+ installed and verified.
- **Python Runtime**: Python 3.12 with `numpy` and `Pillow` (verified for audio analysis, beat grid calculation, and seam diffing).
- **Media Engine**: `ffmpeg` and `ffprobe` installed on PATH (verified via audio probing and stream inspection).
- **HyperFrames Engine**: Pinned per project at `0.8.117` in `film/package.json`.

---

## 2. Audio Production & Musical Synchronization

### 2.1 Soundtrack Specification
- **Primary Audio Asset**: `film/assets/audio/Tech Showcase.mp3`.
- **Duration**: Exactly **102.015 seconds** (1 minute 42 seconds).
- **Sample Rate / Encoding**: 44.1 kHz, 2-channel stereo, 134 kbps MP3.
- **Analyzed Tempo**: **106.8 BPM** (1 beat = `0.5618s`, 1 musical bar = `2.2472s`).
- **First Downbeat**: Exactly at `0.27s`.
- **Total Bar Count**: **45 complete musical bars** (Bar 0 to Bar 44).
- **Preservation Decision**:
  - The track fits the user's 60 to 120-second target duration **natively without cutting, looping, or time-stretching**.
  - Bars 0–4 provide a natural ambient build-up.
  - Bar 5 (11.51s) delivers an unmistakable beat drop.
  - Bars 26–37 sustain an intense driving climax.
  - Bars 38–44 resolve gracefully into a low sub-bass chord (79% bass concentration around 295Hz) that naturally decays to silence at 102.0s.
  - **No artificial audio surgery is required.** The soundtrack will be played unabridged from start to finish.

### 2.2 Sound Effects (SFX) Strategy
- **Palette**: 7 tactile UI sound cues curated to match the high-tech SaaS aesthetic:
  1. `whoosh-deep`: Camera accelerations and large 3D scene push-throughs.
  2. `impact-drop`: Heavy beat drop and major architectural arrivals (Bars 5 and 26).
  3. `click-tactile`: Button depressions and query console executions.
  4. `tick-subtle`: Metric counter ticks and rapid sequential checkmarks.
  5. `pop-pill`: Status badges and reflex notification card arrivals.
  6. `stamp-success`: Data quality pass stamps and ACID contract locks.
  7. `ping-chime`: Sub-second latency badges (`42ms`) and resolution confirmations.
- **Cue Sheet Scheduling**: All SFX cues are declared in `film.json` with scene-local timing and explicit durations (`data-duration`), preventing any audio buffer contention or duplicate track warnings. SFX volumes are held strictly between `0.22` and `0.45` beneath the music bed.

---

## 3. Visual & Spatial Technical Standards

### 3.1 Camera & Viewport Geometry
- **Resolution**: 1920 × 1080 (16:9 widescreen landscape).
- **Framing Geometry**: A single virtual camera with a fixed perspective distance of **1866px (35mm equivalent)** across all 10 compositions.
- **Camera Drift**: Underneath active camera motion paths, a subtle perpetual drift layer ($0.5\text{px}$ to $2\text{px}$ displacement) prevents any static hold from looking frozen.
- **Depth Layers**:
  - Background Ground (`$Z = -100\text{px}$` to `$-300\text{px}$`): Obsidian base, soft radial vignette, ambient depth.
  - Main Workspace Surface (`$Z = 0\text{px}$`): IDE windows, Eventstream canvases, report viewports.
  - Elevated Interaction Cards (`$Z = +40\text{px}$` to `$+160\text{px}$`): Floating metrics, reflex alert toasts, active badges.

### 3.2 Typography & CSS Design Kit
- **Core Font Family**: Poppins (`assets/fonts/poppins-500.woff2`, `assets/fonts/poppins-700.woff2`) for structural UI and headlines.
- **Monospace Family**: JetBrains Mono for telemetry JSON, KQL queries, and large metric values.
- **Font Scale Hierarchy**:
  - Headlines: 64px–84px bold.
  - Key Metrics: 48px–72px bold monospace.
  - Subtitles & Callouts: 24px–32px semibold.
  - Badges & Status Chips: 14px–18px bold.
  - Metadata & System Labels: 12px–14px uppercase.
- **Scale Law**: Scale UI elements exclusively via CSS `zoom` (`.kit-zoom`) rather than CSS `transform: scale(>1)` to guarantee sharp subpixel text rendering at 1080p60.

---

## 4. Phase-by-Phase Implementation Strategy

Following the disciplined methodology of `.agents/skills/bo-spatial-film/SKILL.md`:

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                               PRODUCTION WORKFLOW PHASES                               │
├───────────────┬────────────────────────────────────────────────────────┬───────────────┤
│    PHASE      │ KEY DELIVERABLE                                        │ APPROVAL GATE │
├───────────────┼────────────────────────────────────────────────────────┼───────────────┤
│ **Phase 1**   │ Storyboard, Beat Map & Production Plan Lock            │ USER GO-AHEAD │
│ **Phase 2**   │ Contract (`frame.md`), Kit CSS & Pre-Rendered Surfaces │ NO UNRESOLVED │
│ **Phase 3**   │ 10 Scene Compositions & Isolated Test Harnesses        │ LINT 0 ERRORS │
│ **Phase 4**   │ Master Audio Alignment & SFX Cue Assembly              │ CUES IN JSON  │
│ **Phase 5**   │ CLI Assembly, Seam Pixel Proofing & Final GPU Render   │ SEAMS PASS    │
└───────────────┴────────────────────────────────────────────────────────┴───────────────┘
```

### Phase 1: Intake, Storyboard & Production Planning (CURRENT PHASE)
- **Status**: Compiling full audit, data flow map, reference analysis, storyboard, production plan, and asset inventory.
- **Gate**: User reviews planning documents and gives explicit approval before any code or scene implementation begins.

### Phase 2: Frame Contract & Pre-Rendered Surface Generation
- Update `film/film.json` with the locked 10-scene schedule (45 bars / 102.0s).
- Verify `film/frame.md` with exact design tokens, typography rules, and shared seam definitions.
- Pre-render high-resolution 2x surface captures for any complex platform canvases using Playwright / headless captures.

### Phase 3: Scene Construction & Isolated Validation
- Build the 10 HTML scene compositions (`s01` through `s10`) inside `film/compositions/`.
- Ensure each scene adheres to strict modular rules:
  - Paused GSAP timeline registered on `window.__timelines[id]`.
  - Root-relative `assets/...` paths.
  - Unique scene ID prefixes for classes and IDs to prevent collision.
- Run per-scene test harnesses (`scripts/make-harness.py`, `scripts/test-scene.sh`) to verify zero lint errors and inspect contact sheet snapshot PNGs.

### Phase 4: Audio Assembly & SFX Cue Synchronization
- Write the final cue sheet into `film.json`.
- Execute `python scripts/assemble.py` to compile the 10 scenes, background music track, and SFX tracks into the master `film/index.html`.

### Phase 5: Seam Verification, Hardware GPU Render & Web Encoding
- Execute `python scripts/seam-check.py` to mathematically compare shared frames across every scene transition and verify loop closure (0.00% difference outside intentional motion).
- Execute `python scripts/fromto-scan.py` to ensure zero seeking errors.
- Trigger final render using the AMD Radeon RX 6600 hardware GPU:
  ```powershell
  npx hyperframes render . --browser-gpu --workers 6 -o renders/fabric-cinematic-showcase.mp4
  ```
- Encode final web-optimized deliverable using `node scripts/encode-web.mjs` (H.264 CRF 21, faststart).

---

## 5. Technical Risks & Mitigation Plan

| Identified Risk | Impact | Pre-Emptive Mitigation |
| :--- | :--- | :--- |
| **Seam Frame Pops** | Slight visual stutter between scenes | Strictly enforce shared 2D plates held for 0.1s at each seam; verify with `seam-check.py`. |
| **GPU Headless Render Crawl** | Slow software CPU rendering (~1 fps) | Explicitly invoke `--browser-gpu` targeting the machine's AMD Radeon RX 6600 hardware GPU. |
| **3D Flattening Glitch** | CSS 3D perspectives collapsing | Prohibit `opacity`, `overflow: hidden`, `filter`, or `clip-path` on any parent 3D camera container. |
| **Audio Desynchronization** | Beats drifting from visuals | Lock every scene duration strictly to whole or half musical bars of the native 106.8 BPM track. |
| **Long Render Lockups** | Node background process hangs | Monitor render logs directly to a dedicated log file; verify process trees before and after runs. |

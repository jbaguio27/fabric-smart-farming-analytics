---
name: design-taste
description: Anti-slop frontend taste guidelines. Eliminates generic AI UI patterns, elevates visual hierarchy, breaks repetitive bento-grid cliches, introduces intentional typography contrasts, and crafts memorable aesthetics.
---

# Design Taste: Anti-Generic Frontend Aesthetic Principles

## 1. The Core Mandate: Eliminating "AI Slop"
Generic AI-generated interfaces share recognizable flaws:
- Uniform purple-to-cyan neon gradients on pitch-black backgrounds.
- Cookie-cutter 3-column cards or mindless "bento grids" with identical rounded borders.
- Floating cards nested inside floating cards nested inside floating cards.
- Centered headline + centered subtitle + centered pair of generic rounded buttons on every single page.
- Visual noise (random glow blobs, blurred spheres) that add zero informational value.

**The Golden Rule:** Every visual element must either earn its place by communicating information or establish an authentic brand identity. When in doubt, simplify typography, increase whitespace, and calibrate colors.

---

## 2. Layout Diversity: Breaking the Bento Formula
Bento grids have become the default AI cliché. Use layout variety matched to content semantics:

1. **The Editorial Asymmetry:**
   - Giant left-aligned hero narrative occupying 60% of the viewport width.
   - Live interactive widget, dense tabular feed, or architectural snapshot anchored on the remaining 40%.
2. **The Horizontal System Ribbon:**
   - Continuous end-to-end telemetry ticker or pipeline diagram with subtle left/right fade masks.
   - High data density presented horizontally rather than boxed into uniform squares.
3. **The Master-Detail Split:**
   - Persistent contextual category rail on the left, high-fidelity interactive canvas on the right.
   - Ideal for developer tools, dashboards, and complex enterprise flows.
4. **The Staggered Rhythm (Alternating Focal Points):**
   - Full-bleed media visual followed by a narrow, high-contrast typography block, followed by a wide comparative table.
   - Varied vertical pacing keeps the human eye engaged.

---

## 3. Intentional Typography Hierarchy

### Scale & Tracking Rules
Never use the same letter-spacing across different font sizes. Letter-spacing must be optically tuned:
- **Display Headlines (48px–96px):** Always use negative tracking (`letter-spacing: -0.03em` to `-0.04em`). Tightening counter-spaces makes large type feel cohesive and confident.
- **Section Headers (24px–36px):** Subtle negative tracking (`letter-spacing: -0.02em`).
- **Body Copy (15px–17px):** Default or slightly positive tracking (`letter-spacing: -0.005em` to `0em`) with generous line height (`line-height: 1.6` to `1.7`).
- **Eyebrows, Badges & Labels (10px–13px):** Always use positive tracking (`letter-spacing: 0.06em` to `0.1em`), uppercase or monospace, with high contrast.

### Font Pairing with Character
Avoid pairing two generic sans-serif fonts (e.g. Arial with Helvetica, or Inter with Roboto). Instead:
- **Modern Tech / Data:** Geometric Grotesk (`Plus Jakarta Sans` or `Geist`) + Precision Monospace (`JetBrains Mono` or `Geist Mono`).
- **Editorial / High-End SaaS:** High-contrast Display Serif / Grotesk (`Instrument Serif` or `Cabinet Grotesk`) + Clean Neutral Body (`Inter`).
- **Industrial Engineering:** Rigid Swiss Grotesk (`PP Neue Montreal` or `Plus Jakarta Sans`) + High-contrast Technical Mono.

---

## 4. Color & Surface Calibration

### A. Escaping Pure Black and Pure White
Pure `#000000` feels harsh and dead; pure `#FFFFFF` creates unnecessary eye strain in dark interfaces.
- **Deep Slate/Violet Dark:** Use `#080412`, `#0B0F17`, or `#0D1117` as the deep ground.
- **Layer 1 Surface:** `#121824` or `#130E24` (4%–8% lightness).
- **Layer 2 Card/Elevated:** `#1A2234` or `#1E1736` (8%–14% lightness).
- **Primary Text:** `#F4F6FB` or `#F8FAFC` (96% lightness).
- **Secondary Text:** `#94A3B8` or `#A1A1AA` (60%–70% lightness, accessible 4.5:1+ contrast).

### B. Single-Accent Discipline
Do not use 5 competing bright colors across cards. Pick **one signature accent color** and use it deliberately:
- Reserve the signature accent for primary interactive states, key metrics, and focus anchors.
- Use muted neutral tones for secondary badges and category labels.
- Only introduce red/amber for actual error/warning states, never as decorative trim.

---

## 5. Depth Without Heavy Shadows

Generic drop shadows (`box-shadow: 0 10px 30px rgba(0,0,0,0.5)`) look muddy. Modern depth uses **light interaction**:
1. **The Subtle Hairline Inset:**
   ```css
   .card-depth {
     background: rgba(18, 24, 38, 0.7);
     border: 1px solid rgba(255, 255, 255, 0.08);
     box-shadow: inset 0 1px 0 0 rgba(255, 255, 255, 0.06),
                 0 20px 40px -15px rgba(0, 0, 0, 0.4);
   }
   ```
2. **Glassmorphism with Discipline:**
   - Always pair `backdrop-filter: blur(16px)` with at least 65% background opacity so text remains 100% legible over complex underlying graphics.
   - Add a 1px border with a soft gradient or top-light highlight.

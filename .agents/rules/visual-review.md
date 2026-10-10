# Visual Self-Review Protocol: Frontend Engine & Playwright Audit Loop

## 1. Core Mandate
Whenever writing, modifying, or refactoring frontend code (HTML, CSS, JavaScript, Web components, or landing pages), you must never declare a task complete based on code syntax alone. You must visually inspect your work in the browser, self-critique the rendered output, and iteratively patch visual defects.

---

## 2. Mandatory Skill Standards
Every frontend change must strictly adhere to the three foundational design skills:
1. **Emil Animation Principles (`.agents/skills/emil-animation/SKILL.md`)**:
   - Fast micro-interactions (150ms–250ms).
   - Asymmetric exit/entry timing (exits faster than entries).
   - Spring-like deceleration curves (`cubic-bezier(0.16, 1, 0.3, 1)`), anchored transform-origins, and zero composite jank (only animate `transform` and `opacity`).
2. **Design Taste Guidelines (`.agents/skills/design-taste/SKILL.md`)**:
   - Eliminate generic AI templates and repetitive bento-grid clichés.
   - Purposeful color palettes (OLED dark / slate / warm neutrals, single signature accent).
   - Layered surface depth and subtle hairlines instead of harsh 1px borders and muddy drop shadows.
3. **Impeccable Design Precision (`.agents/skills/impeccable-design/SKILL.md`)**:
   - Strict 4pt / 8pt geometric spacing scale (no arbitrary `13px`, `27px`, etc.).
   - Tabular figures (`font-variant-numeric: tabular-nums`) on all data tables, timestamps, and live counters.
   - WCAG AA contrast compliance (minimum 4.5:1 text contrast).

---

## 3. The Playwright Visual Review Execution Loop

Execute the following visual review cycle whenever frontend code is touched:

### Step 1: Start or Verify the Local Preview
Ensure the web app or static site is serving locally:
- If a development server is already running, identify the port (e.g. `http://localhost:3000`, `http://localhost:8080`, or `http://127.0.0.1:8080`).
- If not running, start a lightweight server (e.g. `npx --yes serve site` or `python -m http.server 8080`) as a background task.

### Step 2: Capture Visual Proof via Playwright
Using the Playwright tool / MCP server:
1. **Desktop Viewport**: Navigate to the preview URL with viewport `1440 × 900` (or `1920 × 1080` for wide screens) and take a high-resolution screenshot.
2. **Mobile Viewport**: Resize or configure viewport to `390 × 844` (standard mobile device scale) and take a full-page or key-section screenshot.
3. **Interactive States**: Where relevant, trigger hover/focus/modal states to capture micro-interaction behavior.

### Step 3: Structured Visual Self-Critique
Inspect the captured screenshots against the following scorecard:
- [ ] **Visual Hierarchy:** Is there an immediate, unambiguous focal point? Does the eye naturally flow from headline to supporting narrative to CTA?
- [ ] **Typography Scale & Tracking:** Are large headlines tightened with negative letter-spacing? Are eyebrow labels tracked out? Is line-height comfortable?
- [ ] **4/8pt Spacing Rhythm:** Are margins and paddings consistent and aligned to the geometric grid?
- [ ] **Contrast & Readability:** Does all copy pass WCAG AA standards over background surfaces or blurred backdrops?
- [ ] **Mobile Collapse:** Does the layout stack gracefully below 768px? Is horizontal overflow (`overflow-x: hidden`) strictly contained with no cut-off elements?
- [ ] **Micro-Interaction Polish:** Do buttons have tactile states (`:active scale(0.975)`)? Are transitions smooth and free of layout thrashing?

### Step 4: Iterative Remediation
- If any alignment, contrast, line wrapping, or spacing flaws are identified, apply targeted CSS/HTML fixes immediately.
- Re-run the Playwright screenshot capture to verify the fix.
- Repeat until the rendered interface meets production agency quality before presenting the solution to the user.

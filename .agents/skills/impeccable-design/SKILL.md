---
name: impeccable-design
description: Impeccable design execution rules. Enforces mathematical typography scales, strict 4/8pt spacing systems, slate/neutral contrast hierarchies, tabular figures for all data/metrics, and layered surface elevation.
---

# Impeccable Design: Quantitative Craft & Systems Precision

## 1. The 4pt / 8pt Geometric Spacing Grid
Every margin, padding, gap, and dimension must divide cleanly by 4 (and ideally 8 for layout blocks). Arbitrary values like `13px`, `27px`, or `39px` destroy visual rhythm and make interfaces feel unpolished.

### The Spacing Scale Tokens
| Token | Value | Primary Use Case |
| :--- | :--- | :--- |
| `space-1` | `4px` | Micro-gaps between badge icon & text, caret padding |
| `space-2` | `8px` | Gap between form label & input, compact item padding |
| `space-3` | `12px` | Standard button padding (vertical), list item gap |
| `space-4` | `16px` | Card internal padding (mobile), standard component gap |
| `space-5` | `20px` | Intermediate component spacing |
| `space-6` | `24px` | Standard card internal padding (desktop), grid gap |
| `space-8` | `32px` | Section sub-group gap, modal padding |
| `space-12` | `48px` | Major component separation |
| `space-16` | `64px` | Section vertical padding |
| `space-24` | `96px` | Hero section top/bottom padding |
| `space-32` | `128px` | Major landing page division |

**Layout Container Rule:** Containers must have standardized horizontal padding (`px-4` on mobile, `px-6` on tablet, `px-8` to `px-12` on desktop) with a strict `max-width` limit (`1200px` for editorial, `1440px` for widescreen dashboards).

---

## 2. Mathematical Typography Scale
Typography must adhere to a calibrated typographic scale (Major Second or Minor Third ratio) with consistent line-height and letter-spacing relationships:

```css
:root {
  /* Font Sizes */
  --text-xs: 12px;     /* line-height: 16px (1.33), tracking: +0.06em */
  --text-sm: 14px;     /* line-height: 20px (1.43), tracking: +0.02em */
  --text-base: 16px;   /* line-height: 24px (1.50), tracking: 0em */
  --text-lg: 18px;     /* line-height: 28px (1.55), tracking: -0.01em */
  --text-xl: 20px;     /* line-height: 28px (1.40), tracking: -0.015em */
  --text-2xl: 24px;    /* line-height: 32px (1.33), tracking: -0.02em */
  --text-3xl: 32px;    /* line-height: 40px (1.25), tracking: -0.025em */
  --text-4xl: 40px;    /* line-height: 48px (1.20), tracking: -0.03em */
  --text-5xl: 48px;    /* line-height: 56px (1.16), tracking: -0.035em */
  --text-6xl: 64px;    /* line-height: 72px (1.12), tracking: -0.04em */
}
```

---

## 3. Tabular Figures: The Data & Telemetry Rule
All numerical values, timestamps, monetary figures, metrics, and data tables **MUST** render with tabular numbers. Without this, updating numbers jitter horizontally and tables look sloppy:

```css
/* Universal tabular numbers for metrics and data */
.tabular-nums,
.metric-value,
.timestamp,
.counter,
table td {
  font-variant-numeric: tabular-nums;
  -webkit-font-feature-settings: "tnum" 1;
  font-feature-settings: "tnum" 1;
}
```

---

## 4. Slate & Neutral Contrast Hierarchies

Never use low-contrast text for critical labels. Adhere strictly to **WCAG AA (minimum 4.5:1 for body copy, 3:1 for large display headlines)**.

### Dark Mode Semantic Tokens
- **Canvas Base:** `#090D16` (Deep slate ground)
- **Surface Elevation 1:** `#111827` (Card / Section background)
- **Surface Elevation 2:** `#1F2937` (Interactive item / Table row hover)
- **Surface Elevation 3:** `#374151` (Input surface / Elevated popover)
- **Hairline Border:** `rgba(255, 255, 255, 0.08)` (Crisp 1px boundary)
- **Active Focus Ring:** `rgba(99, 102, 241, 0.5)` with `2px` offset
- **Text Primary:** `#F9FAFB` (Contrast ratio > 14:1)
- **Text Secondary:** `#9CA3AF` (Contrast ratio > 6.2:1)
- **Text Muted / Tertiary:** `#6B7280` (Contrast ratio > 4.6:1)

---

## 5. Layered Elevation Over Harsh Borders

Harsh `1px solid #444` borders look cheap and rigid. Instead, use layered ambient shadows combined with low-opacity hairlines:

```css
/* Level 1: Flat Card (In-flow) */
.elevation-1 {
  background: #111827;
  border: 1px solid rgba(255, 255, 255, 0.06);
  box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.25);
}

/* Level 2: Interactive Card / Floating Panel */
.elevation-2 {
  background: #151E2E;
  border: 1px solid rgba(255, 255, 255, 0.08);
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.3),
              0 2px 4px -2px rgba(0, 0, 0, 0.2),
              inset 0 1px 0 0 rgba(255, 255, 255, 0.05);
}

/* Level 3: Modal / Dropdown / Popover */
.elevation-3 {
  background: #1A2438;
  border: 1px solid rgba(255, 255, 255, 0.12);
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.5),
              0 8px 10px -6px rgba(0, 0, 0, 0.4),
              inset 0 1px 0 0 rgba(255, 255, 255, 0.08);
}
```

---

## 6. Optical Alignment Principles
1. **Button Icon & Text:** Align icon optical mass with font cap-height, not bounding box height. Add `margin-top: -1px` if the icon looks visually low.
2. **Badge Padding:** Badges need slightly more horizontal padding than vertical padding (e.g. `py-1 px-2.5` or `py-0.5 px-2`).
3. **Corner Radii Scaling:** Nested rounded containers must follow concentric curvature:
   $$\text{Outer Radius} = \text{Inner Radius} + \text{Padding}$$
   *(If padding is 8px and outer radius is 12px, inner radius should be 4px to avoid awkward corner gaps).*

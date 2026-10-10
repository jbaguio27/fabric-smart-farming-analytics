---
name: emil-animation
description: Modern web animation principles inspired by Emil Kowalski. Master spring physics vs easing curves, micro-interactions, layout transitions, exit/entry timing, scale anchors, interruptibility, and 60/120fps jank prevention.
---

# Emil Animation: Modern Web Animation & Micro-Interaction Engine

## 1. Philosophy: Purposeful Motion, Not Decoration
Motion on the web exists to communicate spatial continuity, provide immediate tactile feedback, and direct user focus. It should never delay the user or feel self-indulgent.

- **Rule 1: Fast & Responsive.** If an interaction takes longer than 300ms to complete its primary motion, it feels sluggish. Micro-interactions should resolve within 150ms–250ms.
- **Rule 2: Asymmetric Entry & Exit.** Exits must always be faster than entries. Entering elements introduce context (200ms–300ms); exiting elements clear an obstacle (100ms–180ms).
- **Rule 3: Natural Deceleration.** Things in the physical world do not suddenly stop. Most digital UI animations should be front-loaded (fast start, long smooth deceleration).

---

## 2. Springs vs. Bézier Curves

### When to Use Springs
Use spring physics for **user-driven, physical, or interruptible** interactions:
- Dragging, swiping, gesture reveals
- Scale/press feedback on buttons and cards
- Sheet and modal dragging
- Reordering lists and layout shifts

**Recommended Spring Parameters:**
- **Snappy UI (Buttons, Toggles):** `stiffness: 400`, `damping: 30`, `mass: 0.8` (no overshoot, quick settle)
- **Fluid Surface (Modals, Popovers, Drawers):** `stiffness: 300`, `damping: 28`, `mass: 1.0` (subtle bounce, very organic)
- **Playful Feedback (Badges, Reactions):** `stiffness: 500`, `damping: 20`, `mass: 1.0` (deliberate micro-overshoot)

### When to Use Cubic Béziers
Use cubic béziers for **programmatic, predictable, opacity-coupled** UI changes:
- Fade transitions
- Background color morphs
- Pre-baked SVG path animations
- Timed sequence reveals

**The Gold Standard Easings (CSS):**
```css
/* Smooth Natural Deceleration (Emil standard for entries) */
--ease-out-quint: cubic-bezier(0.22, 1, 0.36, 1);
--ease-out-expo: cubic-bezier(0.16, 1, 0.3, 1);

/* Responsive Spring-like Bézier (Snappy, front-loaded) */
--ease-spring: cubic-bezier(0.175, 0.885, 0.32, 1.1);

/* Acceleration for fast dismissals */
--ease-in-quad: cubic-bezier(0.32, 0, 0.67, 0);
```

---

## 3. Micro-Interactions & Tactile Feedback

### A. The Tactile Button Press
Never use opacity drop alone. Pair optical color shift with physical scale:
```css
.btn-tactile {
  transition: transform 120ms cubic-bezier(0.16, 1, 0.3, 1),
              box-shadow 120ms cubic-bezier(0.16, 1, 0.3, 1),
              background-color 150ms ease;
  transform-origin: center center;
}

.btn-tactile:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

.btn-tactile:active {
  transform: translateY(0.5px) scale(0.975);
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.06);
}
```

### B. Scale Anchors & Transform Origin
Always anchor transforms to the source of truth:
- **Dropdown menus:** `transform-origin: top left` (or `top right` depending on alignment).
- **Tooltips:** `transform-origin: bottom center` (emerging from the arrow tip).
- **Dialogs / Modals:** `transform-origin: center center` (scale from `0.95` to `1.0`).
- **Context cards:** Anchor to the trigger element's center point.

### C. Staggering & Cascade Timing
Never stagger elements with delays larger than 30ms–50ms. Heavy staggers (>100ms) force users to wait for page comprehension.
```css
/* Stagger rule: tight intervals */
.list-item:nth-child(1) { animation-delay: 0ms; }
.list-item:nth-child(2) { animation-delay: 25ms; }
.list-item:nth-child(3) { animation-delay: 50ms; }
.list-item:nth-child(4) { animation-delay: 75ms; }
.list-item:nth-child(5) { animation-delay: 100ms; }
```

---

## 4. Layout Transitions (Without Height: Auto Jank)

### The CSS Grid 0fr → 1fr Accordion Trick
Never animate `max-height` (causes timing mismatch and stutter). Animate `grid-template-rows`:
```css
.accordion-content {
  display: grid;
  grid-template-rows: 0fr;
  transition: grid-template-rows 220ms cubic-bezier(0.16, 1, 0.3, 1);
}

.accordion-item[data-open="true"] .accordion-content {
  grid-template-rows: 1fr;
}

.accordion-inner {
  overflow: hidden;
}
```

### FLIP Transitions (First, Last, Invert, Play)
When moving elements between parent containers or changing DOM order:
1. Record initial bounding rect (`First`).
2. Apply DOM mutation and record final bounding rect (`Last`).
3. Compute delta and apply reverse `transform: translate(dx, dy)` (`Invert`).
4. Animate transform to `translate(0, 0)` on the next animation frame (`Play`).

---

## 5. 60fps & 120fps Jank Prevention Checklist

1. **Only Animate Composite Properties:**
   - Allowed: `transform`, `opacity`, and CSS filter in moderation.
   - Strictly banned for animation loops: `width`, `height`, `top`, `left`, `margin`, `padding`, `border-width`.
2. **Promote to GPU Layers Wisely:**
   ```css
   .hardware-accelerated {
     transform: translateZ(0);
     backface-visibility: hidden;
     will-change: transform, opacity;
   }
   ```
   *Note: Remove `will-change` once animations finish to avoid VRAM exhaustion.*
3. **Prevent Subpixel Jitter:** Always round transform values to integer or half-pixel boundaries in JavaScript calculations.
4. **Accessible Reduced Motion:**
   ```css
   @media (prefers-reduced-motion: reduce) {
     *, *::before, *::after {
       animation-duration: 0.01ms !important;
       animation-iteration-count: 1 !important;
       transition-duration: 0.01ms !important;
       scroll-behavior: auto !important;
     }
   }
   ```

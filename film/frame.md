# frame.md - Microsoft Fabric Real-Time Smart Farming Analytics (design truth)

1920x1080, rendered at **60fps**, 46.91s, 7 scenes. Obsidian dark-room data engineering spatial film with floating 3D glass panels, glowing green-cyan telemetry stream vectors, and sub-second Direct Lake analytical precision.
Content per scene lives in each storyboard block; this file is the LOOK and the shared rules. Workers obey it to the letter.

## Tokens (from HydroGrow Microsoft Fabric design system)

| Role | Value |
|---|---|
| canvas / paper (ground) | `#0A0D08` (`.kit-ground` = radial #121A0E -> #0A0D08 -> #060805) |
| paper-hi | `#121A0E` |
| card / surface, well | `#11160C`, `#0D1109` |
| ink / ink-soft / ink-faint | `#F4F6F0` / `#BAC5B0` / `#6D7A64` |
| accent (moss green) | `#687941` |
| accent-lime | `#A3BF65` |
| good / success | `#4ADE80` |
| warn / dlq amber | `#E27324` |
| direct lake cyan | `#38BDF8` |
| spring ease (CSS) | `cubic-bezier(0.34, 1.56, 0.64, 1)` |

Bans: generic emoji, purple-to-blue generic neon gradients, cheap circular spinners (use shimmer sweep), stock people, "John Doe", hard cuts, empty frames. Data is authentic to HydroGrow (8 Benguet facilities, 80 zones, 10,480 events/min, ₱137.83M gross crop revenue, sub-3s SLA).

## Type

Poppins and JetBrains Mono, weights 500 and 700, shipped at `assets/fonts/`. Every scene declares, inside its template:

```css
@font-face { font-family: 'Poppins'; font-weight: 500; src: url('assets/fonts/poppins-500.woff2') format('woff2'); }
@font-face { font-family: 'Poppins'; font-weight: 700; src: url('assets/fonts/poppins-700.woff2') format('woff2'); }
```

Film labels (chips, names, keycaps): 26-34px/700. Lockup wordmark 80-120px/700. Never below 20px for film-level text. Text inside product UI uses the UI's real sizes, scaled with `.kit-zoom`.

## Shared kit - `assets/kit.css` + `references/snippets.html`

Every scene links it inside its template: `<link rel="stylesheet" href="assets/kit.css">`.
Components: `.kit-ground`, `.kit-grain`, `.kit-zoom`, `.kit-chip`, `.kit-cursor`, `.kit-ring`, `.kit-ck` (corner ticks), `.kit-win` (browser window), `.kit-metric`, `.kit-pulse`.

- **Scaling UI:** wrap a component in `<div class="kit-zoom" style="--z:2.2">`. CSS zoom re-lays out at the bigger size, so text stays sharp. **Never** scale UI up with `transform: scale(>1)` or by pushing it toward the camera past its authored size.

## Assets (reference them ROOT-RELATIVE as `assets/...` from a scene)

| File | What | Native px |
|---|---|---|
| `captures/directlake-executive.png` | Power BI Executive Operations (Direct Lake) | 1920x1080 |
| `captures/environmental-microclimates.png` | Benguet Microclimate Telemetry Zones | 1920x1080 |
| `captures/dataops-observability.png` | OpenTelemetry Pipeline Observability | 1920x1080 |
| `captures/fabric-solution-architecture.png` | End-to-End Microsoft Fabric Architecture | 1920x1080 |
| `captures/medallion-architecture.png` | Medallion Lakehouse Lineage Blueprint | 1920x1080 |
| `captures/gold-star-schema-erd.png` | Kimball Star Schema Dimensional Model | 1920x1080 |

## The camera (one rig per scene, same lens everywhere)

```html
<div id="<id>-stage" class="clip" data-start="0" data-duration="<dur>" data-track-index="1"
     style="position:absolute; inset:0; perspective:1866px; perspective-origin:50% 50%;">
  <div id="<id>-drift" class="<id>-layer">          <!-- constant breath only -->
    <div id="<id>-cam" class="<id>-layer">          <!-- authored camera legs -->
      <!-- world objects: position:absolute; left:50%; top:50%; then gsap.set(x,y,z,rotationX/Y) -->
    </div>
  </div>
</div>
```

- 1866px perspective = 35mm lens on a 1920 frame.
- Move camera by tweening `#<id>-cam` (inverse transform: to dolly in, tween `z` positive; to orbit, tween `rotationY`).
- Flattening traps: no `opacity < 1`, `filter`, `overflow:hidden`, or `clip-path` on ancestor holding 3D children. Put only on leaf elements.
- Depth of field: far layers get `filter: blur(4-8px)` on the leaf.
- Constant life: `#<id>-drift` carries slow breath for the whole scene (2-3% scale, 1-2deg orbit, `sine.inOut`).
- Layered shadow: `box-shadow: var(--float)`.

## Smoothness law (60fps)

1. Animate only `x, y, z, rotationX/Y/Z, scale, opacity`.
2. Eases: `back.out(1.4-1.8)` for landings; `expo.out` / `power3.out` for arrivals; `power2.inOut` / `expo.inOut` for camera legs. No linear transitions.
3. Camera legs overlap: start the next leg 0.15-0.3s before previous ends.
4. Seekable and deterministic: one paused timeline registered last on `window.__timelines[id]`, `immediateRender: false` on later `fromTo` of same property.
5. Grid: 110 BPM, beat = **0.5455s**, bar = **2.1818s**. Clicks, ticks, stamps and arrivals sit on beats.

## Seams - shared frames

| Seam | Time | Shared frame |
|---|---|---|
| `s07-architecture-lockup` -> `s01-edge-ingress` (loop) | 46.9091 / 0.0000 | `#0A0D08` camera aligned to Benguet edge telemetry gateway |
| `s01-edge-ingress` -> `s02-eventstream-kql` | 6.5455 | `#0D130B` solid push-through into Eventstream ingress port |
| `s02-eventstream-kql` -> `s03-medallion-lakehouse` | 13.0909 | `#0E120A` solid push-through into Lakehouse Delta stream connector |
| `s03-medallion-lakehouse` -> `s04-selfhealing-dlq` | 20.7273 | `#11160C` solid push-through into DLQ Quarantine plate |
| `s04-selfhealing-dlq` -> `s05-directlake-powerbi` | 27.2727 | `#0A0D08` solid push-through into Power BI Direct Lake canvas |
| `s05-directlake-powerbi` -> `s06-activator-reflex` | 34.9091 | `#11160C` solid push-through into Fabric Activator Reflex stage |
| `s06-activator-reflex` -> `s07-architecture-lockup` | 40.3636 | `#0A0D08` solid dolly-out into Master Architecture lockup |

`.kit-grain` sits on top of every scene for its whole duration.

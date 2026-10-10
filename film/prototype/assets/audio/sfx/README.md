# Audio Sound Effects Manifest (`film/assets/audio/sfx/`)

**Project**: Microsoft Fabric Real-Time Smart Farming Analytics Showcase Film  
**Audio Foundation Track**: `film/assets/audio/Tech Showcase.mp3` (102.015s, 106.8 BPM, 44.1kHz stereo)  
**Manifest Updated**: October 10, 2026  
**License Compliance**: All assets licensed under **Creative Commons Zero (CC0) 1.0 Universal / Public Domain** or royalty-free open-source video libraries. Safe for enterprise production and commercial distribution without mandatory attribution.

---

## 1. Primary Sound Design Assets

| Filename | Category | Format / Specs | Duration | Peak Level | Source URL | Creator / Pack | License | Download Date | Cinematic Usage & Action Pairing |
|---|---|---|---|---|---|---|---|---|---|
| `ui_click.mp3` (`.wav`) | `ui_click` | 44.1kHz, 192 kbps, stereo | 0.097s | -1.5 dBFS | [Kenney Interface Sounds](https://kenney.nl/assets/interface-sounds) | Kenney (`click_001.wav`) | CC0 1.0 | 2026-10-10 | **Click &rarr; Open (Action A)**: Cursor lands on workspace item (`FarmingTelemetryEventstream`, report slicer, query run). |
| `ui_open.mp3` (`.wav`) | `ui_open` | 44.1kHz, 192 kbps, stereo | 0.148s | -2.0 dBFS | [Kenney Interface Sounds](https://kenney.nl/assets/interface-sounds) | Kenney (`open_001.wav`) | CC0 1.0 | 2026-10-10 | **Click &rarr; Open (Action A)**: Workspace item editor, side panel, or modal canvas opens into focus. |
| `whoosh_short.mp3` (`.wav`) | `whoosh_short` | 44.1kHz, 192 kbps, stereo | 0.154s | -3.0 dBFS | [Remotion SFX CDN](https://remotion.media/whoosh.wav) | Remotion Media Library | CC0 1.0 | 2026-10-10 | **Camera Move &rarr; Whoosh (Action B)**: Fast push-through transition between scenes or zoom into detail. |
| `whoosh_riser.mp3` (`.wav`) | `whoosh_riser` | 44.1kHz, 192 kbps, stereo | 0.518s | -2.5 dBFS | [Kenney Digital Audio](https://kenney.nl/assets/digital-audio) | Kenney (`phaserUp1.wav`) | CC0 1.0 | 2026-10-10 | **Camera Move &rarr; Whoosh (Action B)**: Major narrative buildup leading into beat drops (Bar 4.0 &rarr; 5.0 and Bar 25.0 &rarr; 26.0). |
| `data_flow.mp3` (`.wav`) | `data_flow` | 44.1kHz, 192 kbps, stereo | 0.467s | -4.0 dBFS | [Kenney Digital Audio](https://kenney.nl/assets/digital-audio) | Kenney (`phaseJump1.wav`) | CC0 1.0 | 2026-10-10 | **Data-Flow Movement**: Animated data packet splines travelling across Eventstream routing nodes. |
| `success_chime.mp3` (`.wav`) | `success_chime` | 44.1kHz, 192 kbps, stereo | 0.290s | -3.0 dBFS | [Kenney Interface Sounds](https://kenney.nl/assets/interface-sounds) | Kenney (`confirmation_001.wav`) | CC0 1.0 | 2026-10-10 | **Major Reveal &rarr; Accent (Action C)**: Verified sub-second query completion (`42ms`), SLA compliance, and DLQ replay success. |
| `notification.mp3` (`.wav`) | `notification` | 44.1kHz, 192 kbps, stereo | 0.721s | -3.5 dBFS | [Kenney Digital Audio](https://kenney.nl/assets/digital-audio) | Kenney (`twoTone1.wav`) | CC0 1.0 | 2026-10-10 | **Tactile Alert Action**: Fabric Activator Reflex operational emergency alert pop. |
| `deep_impact.mp3` (`.wav`) | `deep_impact` | 44.1kHz, 192 kbps, stereo | 0.527s | -1.0 dBFS | [Kenney Impact Sounds](https://kenney.nl/assets/impact-sounds) | Kenney (`impactSoft_heavy_000.wav`) | CC0 1.0 | 2026-10-10 | **Major Reveal &rarr; Accent (Action C)**: Musical beat drop impact (Bar 5.0, Bar 26.0) and master architecture lockup. |
| `soft_transition.mp3` (`.wav`) | `soft_transition` | 44.1kHz, 192 kbps, stereo | 0.132s | -5.0 dBFS | [Kenney Interface Sounds](https://kenney.nl/assets/interface-sounds) | Kenney (`drop_001.wav`) | CC0 1.0 | 2026-10-10 | **Quiet Handoff**: Calm camera glide during meditative breakdown bridge (Bars 17–20). |

---

## 2. Legacy / Auxiliary SFX (Maintained for Backward Compatibility)

| Filename | Duration | Purpose |
|---|---|---|
| `click.mp3` | 0.080s | Legacy short click transient |
| `whoosh.mp3` | 0.350s | Legacy broadband camera whoosh |
| `pop.mp3` | 0.120s | Legacy badge appearance pop |
| `punch.mp3` | 0.250s | Legacy mid-bass impact |
| `stamp.mp3` | 0.180s | Legacy contract seal stamp |
| `impact.mp3` | 0.450s | Legacy sub-bass hit |

---

## 3. Mixing & Production Guidelines

1. **Volume Calibration**:
   - `Tech Showcase.mp3` soundtrack runs at master volume `0.65` (baseline).
   - During major UI actions (`ui_click`, `notification`, `deep_impact`), soundtrack ducks by `-3dB` (`0.48`) for `0.3s`, then smoothly returns.
   - SFX track volumes are calibrated between `0.20` and `0.50` to maintain clean headroom without distortion or clipping.
2. **Local Rendering**:
   - All audio files are stored locally in `film/assets/audio/sfx/`. No external network requests or CDN dependencies are invoked during rendering.
3. **Format Support**:
   - Both `.wav` (uncompressed 16-bit 44.1kHz) and `.mp3` (192 kbps high-efficiency) versions are provided for total pipeline and browser compatibility.

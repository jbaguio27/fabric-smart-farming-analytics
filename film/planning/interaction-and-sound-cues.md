# Microsoft Fabric Showcase: Master Interaction & Sound Cue Sheet

**Project**: Microsoft Fabric Real-Time Smart Farming Analytics Platform  
**Soundtrack**: `film/assets/audio/Tech Showcase.mp3` (Duration: 102.015s, 44.1kHz stereo, 106.8 BPM)  
**Musical Grid**: 45 Bars @ 106.8 BPM (1 Bar = 2.24719s; 1 Beat = 0.561798s; First downbeat at 0.27s)  
**Format**: 1920 × 1080 Landscape, 60 fps, Single Virtual 35mm Camera (1866px perspective)  
**Document Status**: Official Master Production Cue Sheet (Preserves 10-Scene Approved Storyboard)  

---

## 1. Master Timeline Schedule & Scene Alignment

| # | Scene ID | Musical Bars | Time Window | Duration | Depicted Fabric Surface & Screenshot | Primary Interaction Target | Primary SFX & Timing |
|---|---|---|---|---|---|---|---|
| **s01** | `s01-fabric-brand-opening` | Bars 0–4 | 0.00s – 11.51s | 11.51s (5.0b) | Brand prism &rarr; `01-workspace.png` | Click `FarmingTelemetryEventstream` row | `ui_click.mp3` @ 9.26s, `whoosh_riser.mp3` @ 9.26s |
| **s02** | `s02-edge-iot-ingress` | Bars 5–8 | 11.51s – 20.49s | 8.98s (4.0b) | Benguet Greenhouse & IoT Telemetry Card | Click Gateway Ingress Port | `deep_impact.mp3` @ 11.51s, `ui_click.mp3` @ 16.00s |
| **s03** | `s03-eventstream-routing` | Bars 9–12 | 20.49s – 29.48s | 8.99s (4.0b) | `02-eventstream.png` (9-Node Routing Hub) | Select `SQLNode_DeadLetter`, click `KQL_...` | `ui_open.mp3` @ 20.49s, `ui_click.mp3` @ 22.74s |
| **s04** | `s04-kql-eventhouse` | Bars 13–16 | 29.48s – 38.47s | 8.99s (4.0b) | `03-eventhouse-kql.png` (`SmartFarmingKQLDB`) | Click `EnvironmentalTelemetry` table card | `ui_open.mp3` @ 29.48s, `success_chime.mp3` @ 31.85s |
| **s05** | `s05-onelake-lakehouse` | Bars 17–20 | 38.47s – 47.46s | 8.99s (4.0b) | `04-lakehouse.png` (`SmartFarming_Lakehouse`) | Inspect OneLake zero-copy shortcuts | `soft_transition.mp3` @ 38.47s, `ui_click.mp3` @ 42.97s |
| **s06** | `s06-pyspark-silver-etl` | Bars 21–25 | 47.46s – 58.70s | 11.24s (5.0b) | `05-notebooks.png` (PySpark Delta Engine) | Click Notebook Run button on Delta MERGE | `ui_open.mp3` @ 47.46s, `whoosh_riser.mp3` @ 56.45s |
| **s07** | `s07-selfhealing-dlq` | Bars 26–29 | 58.70s – 67.69s | 8.99s (4.0b) | `06-pipelines.png` (DataOps Batch Pipeline) | Click `Notebook_Batch...` pipeline node | `deep_impact.mp3` @ 58.70s, `ui_click.mp3` @ 60.94s |
| **s08** | `s08-gold-star-schema` | Bars 30–33 | 67.69s – 76.67s | 8.98s (4.0b) | `07-warehouse.png` (`SmartFarming_Warehouse`) | Select `fact_environmental_daily` preview | `ui_open.mp3` @ 67.69s, `ui_click.mp3` @ 69.94s |
| **s09** | `s09-powerbi-activator` | Bars 34–38 | 76.67s – 87.91s | 11.24s (5.0b) | `08-powerbi.png` & `09-activator-monitoring.png` | Click Cordillera Region filter button | `ui_open.mp3` @ 76.67s, `notification.mp3` @ 81.17s |
| **s10** | `s10-architecture-closing` | Bars 39–44 | 87.91s – 102.01s | 14.10s (6.0b) | Master Architecture Blueprint & Fabric Mark | Cursor glides off, camera resolves center | `whoosh_short.mp3` @ 87.91s, `deep_impact.mp3` @ 94.65s |

---

## 2. Universal Navigation Pattern Directive (Scenes 1 through 10)

Adopted from the validated `proto-workspace-nav.html` prototype and aligned with our benchmark reference video (Zelios SaaS Showcase), every transition between Fabric workloads, tools, and artifacts adheres to a consistent 4-phase tactile interaction cycle:

```
[Phase 1: Establish & Context] ---> [Phase 2: Targeted Guidance] ---> [Phase 3: Tactile Hover & Click] ---> [Phase 4: Anchored Spatial Plunge]
       (0.8s - 1.2s wide)                  (Natural deceleration)          (Elevation lift + scale(0.82)         (Fly through target bounds
        Full UI legible                      to 1:1 pixel coords)            + ui_click on beat + hold)            into child canvas plate)
```

1. **Establish & Context (0.8s – 1.2s)**:
   - Camera begins stationary or with very gentle float ($Z \in [0, 25]$, pitch $0^\circ$, yaw $0^\circ$).
   - Full parent UI plate, headers, breadcrumbs, navigation rails, and data context are 100% visible, unclipped, and legible.
2. **Targeted Cursor Guidance**:
   - Cursor eases naturally from current idle position toward the specific, audited target entity.
   - Decelerates into position with cubic-bezier/power2 smoothing; target pointer coordinate is mapped directly to the element's 1:1 pixel bounds on native 1080p captures.
3. **Tactile Hover & Click**:
   - **Tactile Elevation**: Hover state applies subtle vertical lift ($Y = -2\text{px}$) and soft spatial drop shadow (`box-shadow: 0 8px 24px rgba(0, 0, 0, 0.35)`), creating an authentic spatial card feel without altering screenshot pixels.
   - **Tactile Depression**: Pointer compresses (`scale(0.82)`) with a sharp transient click (`ui_click.mp3`) precisely locked to a musical bar/downbeat.
   - **Visual Confirmation & Hold**: Hotspot ripple expands, entity flashes active highlight, and state holds for $0.4\text{s} - 0.5\text{s}$ so the viewer registers intent.
4. **Anchored Spatial Plunge**:
   - Camera transform origin anchors directly to the clicked target's coordinate center $(X_P, Y_P)$.
   - Camera pushes forward through the target aperture ($\Delta X = 960 - X_P, \Delta Y = 540 - Y_P, \Delta Z \approx +340\text{px}$), accompanied by `whoosh_short.mp3`.
   - Parent plate scales up outward from $(X_P, Y_P)$ and dissolves; child canvas plate blooms forward from depth $(Z = -80 \rightarrow 0)$, settling center frame.

---

## 3. Master 1:1 Pixel Coordinate Matrix (Scenes 1–10 Lineage)

All target elements, bounding boxes, pointer landing positions, and camera plunge vectors have been measured and verified against authentic 1920×1080 native Fabric captures:

| Transition & Workload Step | Native 1080p Plate | Target Element & Action | Bounding Box `[X1, Y1, X2, Y2]` | Hotspot Center `(XP, YP)` | Pointer Landing `(XP - 2.5, YP - 1.7)` | Camera Plunge Vector `(CamX, CamY)` | Musical Cue & Beat |
|---|---|---|---|---|---|---|---|
| **Scene 1 &rarr; 2**: Workspace to Eventstream | `01-workspace-1080p.png` | `FarmingTelemetryEventstream` (row 1 text link) | `[253, 337, 496, 354]` | `(374.5, 345.5)` | `(372.0, 343.8)` | `(+585.5, +194.5)` | Bar 4.0 @ 9.26s (`ui_click`) |
| **Scene 2 &rarr; 3**: Ingress Gateway to Eventstream Hub | Benguet Facility Plate | `PythonIoTSimulator` Gateway Ingress Port | `[860, 480, 1060, 540]` | `(960.0, 510.0)` | `(957.5, 508.3)` | `(0.0, +30.0)` | Bar 7.0 @ 16.00s (`ui_click`) |
| **Scene 3 &rarr; 4**: Eventstream Hub to KQL DB | `02-eventstream-1080p.png` | `KQL_EnvironmentalTelemetry` destination node | `[1240, 530, 1420, 580]` | `(1330.0, 555.0)` | `(1327.5, 553.3)` | `(-370.0, -15.0)` | Bar 12.0 @ 27.24s (`whoosh_short`) |
| **Scene 4 &rarr; 5**: Eventhouse KQL to OneLake Lakehouse | `03-eventhouse-kql-1080p.png` | `EnvironmentalTelemetry` table card in KQL Explorer | `[750, 530, 930, 580]` | `(840.0, 555.0)` | `(837.5, 553.3)` | `(+120.0, -15.0)` | Bar 14.0 @ 31.73s (`ui_click`) |
| **Scene 5 &rarr; 6**: Lakehouse to PySpark Delta Notebook | `04-lakehouse-1080p.png` | `EnvironmentalTelemetry` OneLake zero-copy shortcut row | `[320, 450, 560, 485]` | `(440.0, 467.5)` | `(437.5, 465.8)` | `(+520.0, +72.5)` | Bar 19.0 @ 42.97s (`ui_click`) |
| **Scene 6 &rarr; 7**: Notebook ETL to Data Pipeline | `05-notebooks-1080p.png` | Cell 1 PySpark Delta MERGE block / Run trigger | `[510, 190, 560, 230]` | `(535.0, 210.0)` | `(532.5, 208.3)` | `(+425.0, +330.0)` | Bar 22.0 @ 49.70s (`ui_click`) |
| **Scene 7 &rarr; 8**: Pipeline DLQ to Warehouse Star Schema | `06-pipelines-1080p.png` | `Notebook_Batch_Master_Orchestrator` activity node | `[160, 430, 300, 490]` | `(230.0, 460.0)` | `(227.5, 458.3)` | `(+730.0, +80.0)` | Bar 27.0 @ 60.94s (`ui_click`) |
| **Scene 8 &rarr; 9**: Warehouse to Power BI Direct Lake | `07-warehouse-1080p.png` | `fact_environmental_daily` preview table row | `[180, 625, 380, 665]` | `(280.0, 645.0)` | `(277.5, 643.3)` | `(+680.0, -105.0)` | Bar 31.0 @ 69.94s (`ui_click`) |
| **Scene 9 &rarr; 10**: Power BI & Activator to Architecture | `08-powerbi-1080p.png` & `09-activator-monitoring-1080p.png` | Cordillera regional slicer &rarr; `Executive Facility Operational Emergency` trigger card | `[1180, 160, 1460, 200]` & `[420, 240, 780, 290]` | `(1320.0, 180.0)` & `(600.0, 265.0)` | `(1317.5, 178.3)` & `(597.5, 263.3)` | `(-360.0, +360.0)` & `(+360.0, +275.0)` | Bar 35.0 @ 78.92s & Bar 36.0 @ 81.17s |

---

## 4. Repository Path & Enterprise Scope Sanity Statement

- **Local Git Repository**: `fabric-realtime-retail-monitoring` (directory root path on local workstation).
- **Canonical Architecture & Engineering Scope**: **Microsoft Fabric Real-Time Smart Farming Analytics Platform** (`fabric-smart-farming-analytics-dev`).
- **Confirmation**: All underlying schemas, Fabric item definitions (`fabric/`), IoT data generators (`src/smart_farming/`), screenshots (`film/assets/screenshots/`), and spatial compositions belong strictly to the Benguet highland smart agriculture data platform. Previous documentation references to "retail monitoring" were local folder naming artifacts and are hereby formally clarified.

---

## 5. Detailed Scene-by-Scene Cue Specifications

### Scene 1: `s01-fabric-brand-opening`
- **Existing Time Range**: `0.00s – 11.51s` (Bars 0–4 / 5.0 bars total)
- **Actual Fabric Item Shown**:
  - Microsoft Fabric Official Prism Mark & Platform Wordmark (`MICROSOFT FABRIC · REAL-TIME SMART FARMING ANALYTICS`).
  - Seamlessly pushes into the authentic Microsoft Fabric workspace screen: `film/assets/screenshots/01-workspace.png` (`fabric-smart-farming-analytics-dev`).
- **Cursor Path & Click Target**:
  - Cursor originates at $(X=960, Y=780)$ and eases up with natural human smoothing toward the verified text hotspot: `FarmingTelemetryEventstream` (row 1, pointer target $(X=372.0, Y=343.8)$, text center $(X=374.5, Y=345.5)$).
  - Hover settle and tactile elevation lift ($Y = -2\text{px}$, `box-shadow: 0 8px 24px rgba(0,0,0,0.35)`) from $8.50\text{s} – 9.25\text{s}$.
  - Tactile click executed at **9.26s** (Bar 4.0 downbeat) directly on the `FarmingTelemetryEventstream` link (`scale(0.82)` pointer compression + `ui_click.mp3`), held until $9.80\text{s}$.
- **Expected Page / Panel Transition**:
  - Item row flashes confirmation highlight.
  - Camera dives directly through target coordinate $(374.5, 345.5)$ with vector $(\Delta X = +585.5, \Delta Y = +194.5)$, accelerating into the Eventstream ingestion canvas right at the Bar 5.0 drop.
- **Camera Movement & Visual Treatment**:
  - Virtual 35mm camera begins wide at $Z = -450\text{px}$, slow level roll from $-2^\circ$ to $0^\circ$.
  - Dollying forward toward center mark, then rapid plunge anchored to coordinate $(374.5, 345.5)$ at $t = 9.80\text{s}$.
- **Sound Effects & Mixing Details**:
  - `0.27s` (Beat 1): `soft_transition.mp3` — Ambient chord initiation on platform mark reveal (Dur: 0.132s, Mix: 0.35).
  - `9.26s` (Bar 4 downbeat): `ui_click.mp3` — Crisp tactile click precisely synchronized with the pointer press on `FarmingTelemetryEventstream` (Dur: 0.097s, Mix: 0.45).
  - `9.26s – 11.51s`: `whoosh_riser.mp3` — Ascending tonal riser building tension into the drop (Dur: 0.518s, Mix: 0.40).
  - `11.51s` (Bar 5 downbeat): `deep_impact.mp3` — Heavy musical beat drop punch anchoring workspace ingress (Dur: 0.527s, Mix: 0.50).
  - Soundtrack Ducking: Background track drops by -3dB from $9.20\text{s} – 9.60\text{s}$ to highlight click transient.
- **Evidence Confirming Item & Interaction**:
  - `fabric/Readme.md` (Workspace item manifest).
  - Verified in `film/assets/screenshots/01-workspace.png` showing `FarmingTelemetryEventstream` as Item #1.
- **Production Method**: Composited high-fidelity SVG cursor animation over authentic Fabric workspace capture.

---

### Scene 2: `s02-edge-iot-ingress`
- **Existing Time Range**: `11.51s – 20.49s` (Bars 5–8 / 4.0 bars total)
- **Actual Fabric Item Shown**:
  - Benguet Highland Vertical Farming facility plate (`site/assets/images/hero-greenhouse-bg.jpg`).
  - Active IoT Ingress Simulator Card: `PythonIoTSimulator` (`FAC-001 · BENGUET HIGHLANDS · ZONE-04`).
  - Verified telemetry readings: `Air Temp: 21.84°C`, `RH: 76.3%`, `pH: 6.12`, `EC: 1.84 mS/cm`, `10,480 events/min`.
  - Ingress SLA badge: `INGRESS SLA: 1.70s p50 (SUB-3s SLA GUARANTEED)`.
- **Cursor Path & Click Target**:
  - Cursor tracks the live incoming telemetry packet stream, pauses over the Ingress SLA badge, and clicks the Gateway Ingress Port at **16.00s** (Bar 7 downbeat).
- **Expected Page / Panel Transition**:
  - Gateway Ingress Port confirms handshake; SLA status turns vibrant green (`#4ADE80`).
  - Camera dives through the gateway port into the Eventstream streaming canvas.
- **Camera Movement & Visual Treatment**:
  - High-velocity entrance following the drop impact. 3D spatial tilt ($18^\circ$ pitch, $-14^\circ$ yaw).
  - Accelerates forward into the gateway port at $t = 18.25\text{s}$.
- **Sound Effects & Mixing Details**:
  - `11.51s` (Bar 5): `deep_impact.mp3` — Beat drop impact (Dur: 0.527s, Mix: 0.50).
  - `16.00s` (Bar 7): `ui_click.mp3` — Port handshake click (Dur: 0.097s, Mix: 0.45).
  - `16.05s`: `success_chime.mp3` — SLA compliance lock confirmation (Dur: 0.290s, Mix: 0.35).
  - `18.25s` (Bar 8): `whoosh_short.mp3` — Camera dive into Eventstream routing bus (Dur: 0.154s, Mix: 0.40).
- **Evidence Confirming Item & Interaction**:
  - `src/smart_farming/generators/environmental_telemetry_generator.py`.
  - Ingress p50 latency verified in `fabric/Readme.md` (1.70s).
- **Production Method**: Composited 3D spatial telemetry stage over photographic greenhouse plate.

---

### Scene 3: `s03-eventstream-routing`
- **Existing Time Range**: `20.49s – 29.48s` (Bars 9–12 / 4.0 bars total)
- **Actual Fabric Item Shown**:
  - Authentic Fabric Eventstream Editor: `film/assets/screenshots/02-eventstream.png` (`FarmingTelemetryEventstream`).
  - Central Source: `PythonIoTSimulator` &rarr; 9 SQL routing nodes: `SQLNode_DeadLetter`, `CropLifecycleStream`, `CropTelemetryStream`, `EnvironmentalTelemetr...`, `EquipmentTelemetryStr...`, `FacilityOperationsStream`, `IrrigationTelemetryStrea...`, `LightingTelemetryStream`, `MaintenanceActivityStr...`.
  - Active Side Panel: "SQL code" panel for `SQLNode_DeadLetter`.
- **Cursor Path & Click Target**:
  - Cursor enters from left source node, glides along bezier data splines to `SQLNode_DeadLetter` $(X=980, Y=280)$, clicking to select at **22.74s** (Bar 10 downbeat).
  - Sweeps to the SQL code panel $(X=1620, Y=340)$ inspecting:
    `SELECT *, System.Timestamp() AS IngestionTime INTO [Dest_DeadLetterTelemetry] WHERE event_type = 'legacy.deprecated_sensor' OR facility_id IS NULL`.
  - At **27.24s**, clicks destination node `KQL_EnvironmentalTele...` $(X=1350, Y=560)$.
- **Expected Page / Panel Transition**:
  - Selecting `SQLNode_DeadLetter` focuses the right-side SQL configuration panel.
  - Clicking `KQL_EnvironmentalTele...` opens the connection port, initiating the camera push into the KQL database.
- **Camera Movement & Visual Treatment**:
  - Lateral tracking camera move across the 9-node routing topology.
  - Smooth zoom-in $(1.8\times)$ on the SQL code editor ensuring queries are crisp and legible, then accelerates into the KQL node at $t = 27.24\text{s}$.
- **Sound Effects & Mixing Details**:
  - `20.49s` (Bar 9): `ui_open.mp3` — Eventstream studio canvas opens (Dur: 0.148s, Mix: 0.40).
  - `22.74s` (Bar 10): `ui_click.mp3` — Click selecting `SQLNode_DeadLetter` (Dur: 0.097s, Mix: 0.45).
  - `25.00s` (Bar 11): `data_flow.mp3` — High-tech pulse sound on data traveling through routing splines (Dur: 0.467s, Mix: 0.30).
  - `27.24s` (Bar 12): `whoosh_short.mp3` — Camera dive into Eventhouse connector (Dur: 0.154s, Mix: 0.40).
- **Evidence Confirming Item & Interaction**:
  - `fabric/FarmingTelemetryEventstream.Eventstream/eventstream.json`.
  - Authentic capture in `film/assets/screenshots/02-eventstream.png`.
- **Production Method**: Composited cursor and camera push over authentic Fabric Eventstream screenshot.

---

### Scene 4: `s04-kql-eventhouse`
- **Existing Time Range**: `29.48s – 38.47s` (Bars 13–16 / 4.0 bars total)
- **Actual Fabric Item Shown**:
  - Authentic Fabric Eventhouse database: `film/assets/screenshots/03-eventhouse-kql.png` (`SmartFarmingEventhouse` &rarr; `SmartFarmingKQLDB`).
  - Explorer showing tables: `CropLifecycle`, `CropTelemetry`, `DeadLetterTelemetry`, `EnvironmentalEnriched`, `EnvironmentalTelemetry`, `EquipmentRiskEnriched`, `EquipmentTelemetry`, `FacilityOperations`, `IrrigationTelemetry`, `LightingTelemetry`, `MaintenanceActivity`.
  - Data Activity Tracker: Ingestion 1.6k rows, 18.1k queries; Database details: 54MB compressed, 7-day RAM cache policy, 365-day retention.
  - *Evidence Audit Note*: The `42ms` query latency cited in planning benchmarks is an **illustrative test metric** from in-memory hot cache testing; the actual screenshot displays `1.6k rows, 18.1k queries, 7-day RAM cache, and 365-day retention`. No invented latency badge is depicted.
- **Cursor Path & Click Target**:
  - Cursor sweeps to the `EnvironmentalTelemetry` table card $(X=830, Y=560)$, clicking to inspect table properties and storage allocation at **31.73s** (Bar 14 downbeat).
  - Glides across the Data Activity Tracker, spotlighting the 7-day in-memory SSD cache and 365-day retention policy.
- **Expected Page / Panel Transition**:
  - Table card highlights with subtle selection boundary; camera focuses on table caching parameters and high-frequency telemetry schema.
- **Camera Movement & Visual Treatment**:
  - Dutch tilt ($4^\circ$) panning across the database overview.
  - Close-up optical zoom $(1.9\times)$ focused on the `EnvironmentalTelemetry` table card and 7-day hot caching metric, making text 100% readable. Pulls back smoothly at $t = 36.23\text{s}$.
- **Sound Effects & Mixing Details**:
  - `29.48s` (Bar 13): `ui_open.mp3` — Eventhouse console opens (Dur: 0.148s, Mix: 0.40).
  - `31.73s` (Bar 14): `ui_click.mp3` — Table card selection click (Dur: 0.097s, Mix: 0.45).
  - `31.85s`: `success_chime.mp3` — Table metadata and in-memory cache inspection chime (Dur: 0.290s, Mix: 0.40).
  - `36.23s` (Bar 16): `soft_transition.mp3` — Pacing decelerates gently into the meditative breakdown bridge (Dur: 0.132s, Mix: 0.30).
- **Evidence Confirming Item & Interaction**:
  - `fabric/SmartFarmingEventhouse.Eventhouse/DatabaseSchema.kql`.
  - Authentic capture in `film/assets/screenshots/03-eventhouse-kql.png`.
- **Production Method**: Composited cursor and close-up camera inspection over authentic Fabric Eventhouse screenshot.

---

### Scene 5: `s05-onelake-lakehouse`
- **Existing Time Range**: `38.47s – 47.46s` (Bars 17–20 / 4.0 bars total)
- **Actual Fabric Item Shown**:
  - Authentic Fabric Lakehouse explorer: `film/assets/screenshots/04-lakehouse.png` (`SmartFarming_Lakehouse`).
  - Explorer hierarchy: `Tables` (`dbo`, `bronze`, `gold`, `silver`) and `Files` (`_checkpoints`, `bootstrap_history`, shortcuts).
  - 9 verified OneLake Zero-Copy Shortcuts: `CropLifecycle`, `CropTelemetry`, `DeadLetterTelemetry`, `EnvironmentalTelemetry`, `EquipmentTelemetry`, `FacilityOperations`, `IrrigationTelemetry`, `LightingTelemetry`, `MaintenanceActivity`.
- **Cursor Path & Click Target**:
  - Cursor hovers over `SmartFarming_Lakehouse > Files`, traces the shortcut chain icon next to `EnvironmentalTelemetry` $(X=440, Y=475)$, and clicks to inspect shortcut properties at **42.97s** (Bar 19 downbeat).
- **Expected Page / Panel Transition**:
  - OneLake zero-copy shortcut linkage illuminates; status chip confirms: `9 ONELAKE ZERO-COPY SHORTCUTS · ZERO DATA DUPLICATION`.
- **Camera Movement & Visual Treatment**:
  - BREAKDOWN BRIDGE: Slow, wide camera glide moving diagonally across Bronze, Silver, Gold tiers ($18^\circ$ pitch, $-20^\circ$ yaw).
  - Close-up optical zoom on the shortcut chain glyph and modification timestamps (`7/31/2026, 12:27:38 AM`), before accelerating toward PySpark notebook.
- **Sound Effects & Mixing Details**:
  - `38.47s` (Bar 17): `soft_transition.mp3` — Lakehouse explorer reveal (Dur: 0.132s, Mix: 0.35).
  - `42.97s` (Bar 19): `ui_click.mp3` — Shortcut row inspection click (Dur: 0.097s, Mix: 0.45).
  - `43.05s`: `success_chime.mp3` — Zero-copy virtualization confirmation (Dur: 0.290s, Mix: 0.35).
  - `45.21s` (Bar 20): `whoosh_short.mp3` — Momentum rebuilds; camera dives toward PySpark editor (Dur: 0.154s, Mix: 0.40).
- **Evidence Confirming Item & Interaction**:
  - `fabric/SmartFarming_Lakehouse.Lakehouse/lakehouse.json`.
  - Authentic capture in `film/assets/screenshots/04-lakehouse.png`.
- **Production Method**: Composited cursor and close-up camera pan over authentic Fabric Lakehouse screenshot.

---

### Scene 6: `s06-pyspark-silver-etl`
- **Existing Time Range**: `47.46s – 58.70s` (Bars 21–25 / 5.0 bars total)
- **Actual Fabric Item Shown**:
  - Authentic Fabric Notebook editor: `film/assets/screenshots/05-notebooks.png` (`Notebook_Incremental_Silver_Gold_Sync` & `Notebook_Silver_ETL`).
  - PySpark code:
    `spark.conf.set("spark.databricks.delta.properties.defaults.isolationLevel", "Serializable")`
    `from delta.tables import DeltaTable`
    `watermark_table = "gold._ingestion_watermarks"`
    `MERGE INTO {watermark_table} AS t ...`
  - *Evidence Audit Note*: Status bar in `05-notebooks.png` displays `Not connected` (`Selected Cell 1 of 11 cells`). The cursor interaction is structured as an **inspection of code structure and concurrency logic**, NOT a false assertion of live cluster execution.
- **Cursor Path & Click Target**:
  - Cursor glides to Cell 1 $(X=535, Y=205)$ at **49.70s** (Bar 22 downbeat), selecting the cell to inspect the OCC `Serializable` isolation configuration.
  - Cursor scrolls and tracks along the Delta MERGE contract down to the watermark tracking logic, pointing to the exception handling pattern at **54.00s**.
- **Expected Page / Panel Transition**:
  - Cell 1 gains focus outline; code syntax illuminates with enhanced clarity. Does NOT falsely show execution spinner or fake success banner.
- **Camera Movement & Visual Treatment**:
  - RHYTHMIC BUILDUP: Forward camera push into the code editor $(1.7\times\text{ zoom})$, panning smoothly from line 1 to line 40 so logic is effortlessly readable.
  - At $t = 56.45\text{s}$, racks focus toward the Dead-Letter pipeline interface as tension peaks.
- **Sound Effects & Mixing Details**:
  - `47.46s` (Bar 21): `ui_open.mp3` — Notebook editor opens (Dur: 0.148s, Mix: 0.40).
  - `49.70s` (Bar 22): `ui_click.mp3` — Cell focus click (Dur: 0.097s, Mix: 0.45).
  - `51.96s` (Bar 23): `success_chime.mp3` — Delta ACID merge contract and schema verification inspection chime (Dur: 0.290s, Mix: 0.40).
  - `56.45s – 58.70s` (Bar 25): `whoosh_riser.mp3` — Upward digital riser building into the climax (Dur: 0.518s, Mix: 0.45).
  - `58.70s` (Bar 26 downbeat): `deep_impact.mp3` — SECOND DROP IMPACT! (Dur: 0.527s, Mix: 0.50).
- **Evidence Confirming Item & Interaction**:
  - `fabric/Notebook_Silver_ETL.Notebook/notebook-content.py`.
  - Authentic capture in `film/assets/screenshots/05-notebooks.png`.
- **Production Method**: Composited cursor and code inspection over authentic Fabric Notebook screenshot.

---

### Scene 7: `s07-selfhealing-dlq`
- **Existing Time Range**: `58.70s – 67.69s` (Bars 26–29 / 4.0 bars total)
- **Actual Fabric Item Shown**:
  - Authentic Fabric Data Pipeline: `film/assets/screenshots/06-pipelines.png` (`Pipeline_Medallion_Batch_Orchestration`).
  - Active Pipeline Canvas: `Notebook_Batch_Master_Orchestrator` &rarr; branches to `Run_Warehouse_Sync`, `PBISemanticModelRefresh` &rarr; `Log_Semantic_Refresh_Span`, and `Delete Bootstrap Files`.
  - Settings panel: Workspace `fabric-smart-farming-analytics-dev`.
  - 5 Verified DLQ Remediation Workers (Implemented in `Notebook_DeadLetter_Remediation`):
    1. `ERR_SCHEMA_V1`: Schema Translation Adapter (V1.0 &rarr; Canonical V2.0)
    2. `ERR_TIMESTAMP_SKEW`: Clock Skew Normalizer (Clamp timestamp to arrival)
    3. `ERR_OUT_OF_BOUNDS`: Outlier Physical Attenuator (Nullify sensor spike)
    4. `ERR_MISSING_PK`: Primary Key Resolver (Lookup missing facility from MAC)
    5. `ERR_SERDES_MALFORMED`: SerDes Malformed Parser (JSON escape & delimiter repair)
  - *Evidence Audit Note*: Auto-remediation enforces an **Anti-Loop Circuit Breaker (3 retry cap)**. Non-recoverable defects are routed to `EXHAUSTED_QUARANTINE` or manual quarantine and logged to `silver.dead_letter_remediation_audit` and `fact_dead_letter_governance`. Unsubstantiated claims of "100% replay" have been removed.
- **Cursor Path & Click Target**:
  - Cursor clicks `Notebook_Batch_Master_Orchestrator` node $(X=230, Y=460)$ at **60.94s** (Bar 27 downbeat), inspecting orchestrator activity dependencies and batch trigger configuration.
- **Expected Page / Panel Transition**:
  - Activity node highlights; settings panel reveals batch orchestration parameters and downstream dependencies across Warehouse and Semantic Model refresh.
- **Camera Movement & Visual Treatment**:
  - SECOND DROP & FULL GROOVE: Immediate impact camera punch on Bar 26.
  - Dynamic lateral pan across the 3 execution branches, zooming into `PBISemanticModelRefresh` and `Run_Warehouse_Sync`, then accelerating forward.
- **Sound Effects & Mixing Details**:
  - `58.70s` (Bar 26): `deep_impact.mp3` — Climax drop impact (Dur: 0.527s, Mix: 0.50).
  - `60.94s` (Bar 27): `ui_click.mp3` — Pipeline node selection click (Dur: 0.097s, Mix: 0.45).
  - `63.19s` (Bar 28): `data_flow.mp3` — Orchestration flow sound (Dur: 0.467s, Mix: 0.35).
  - `65.44s` (Bar 29): `success_chime.mp3` — Orchestration topology confirmation chime (Dur: 0.290s, Mix: 0.40).
  - `67.00s`: `whoosh_short.mp3` — Transition push into Gold model (Dur: 0.154s, Mix: 0.40).
- **Evidence Confirming Item & Interaction**:
  - `fabric/Notebook_DeadLetter_Remediation.Notebook/` (lines 289–444).
  - Authentic capture in `film/assets/screenshots/06-pipelines.png`.
- **Production Method**: Composited cursor and pipeline inspection over authentic Fabric Pipeline screenshot.

---

### Scene 8: `s08-gold-star-schema`
- **Existing Time Range**: `67.69s – 76.67s` (Bars 30–33 / 4.0 bars total)
- **Actual Fabric Item Shown**:
  - Authentic Fabric Warehouse: `film/assets/screenshots/07-warehouse.png` (`SmartFarming_Warehouse`).
  - Explorer tables: `dim_crop`, `dim_date`, `dim_equipment`, `dim_facility`, `dim_technician`, `dim_zone`, `fact_crop_yield`, `fact_dataops_pipeline_log`, `fact_dead_letter_governance`, `fact_environmental_daily`, `fact_equipment_telemetry`, `fact_irrigation_daily`, `fact_lighting_dli_daily`, `fact_maintenance_sla`.
  - Data preview tab: `fact_environmental_daily` (Showing 1000 rows, columns: `avg_ambient_temp`, `min_ambient_temp`, `avg_humidity_pct`, `avg_co2_ppm`, `avg_vpd_kpa`, `avg_temp_drift`).
  - Verified UI Status: Status bar displays `Succeeded (1 sec 316 ms)`.
- **Cursor Path & Click Target**:
  - Cursor clicks `fact_environmental_daily` table $(X=280, Y=645)$ at **69.94s** (Bar 31 downbeat).
  - Glides to column header `avg_vpd_kpa` $(X=1615, Y=290)$ at **72.18s**, highlighting verified calculated values (`0.94 kPa`, `0.69 kPa`, `0.92 kPa`).
- **Expected Page / Panel Transition**:
  - Table selection focuses the data preview grid; viewer's eye is guided to the authentic `Succeeded (1 sec 316 ms)` status badge.
- **Camera Movement & Visual Treatment**:
  - Sweeping orbital move $(-18^\circ\text{ to }+12^\circ\text{ yaw})$ revealing relational star schema depth.
  - Optical zoom $(2.0\times\text{ close-up})$ into the Data Preview grid making column headers and decimal numbers razor-sharp, before diving into Power BI.
- **Sound Effects & Mixing Details**:
  - `67.69s` (Bar 30): `ui_open.mp3` — Warehouse editor opens (Dur: 0.148s, Mix: 0.40).
  - `69.94s` (Bar 31): `ui_click.mp3` — Table selection click (Dur: 0.097s, Mix: 0.45).
  - `72.18s` (Bar 32): `success_chime.mp3` — Warehouse data preview confirmation chime (Dur: 0.290s, Mix: 0.40).
  - `74.43s` (Bar 33): `whoosh_short.mp3` — Camera dives into Power BI report canvas (Dur: 0.154s, Mix: 0.40).
- **Evidence Confirming Item & Interaction**:
  - `fabric/SemanticModel_SmartFarming_Gold.SemanticModel/definition/model.tmdl`.
  - Authentic capture in `film/assets/screenshots/07-warehouse.png`.
- **Production Method**: Composited cursor and close-up grid inspection over authentic Fabric Warehouse screenshot.

---

### Scene 9: `s09-powerbi-activator`
- **Existing Time Range**: `76.67s – 87.91s` (Bars 34–38 / 5.0 bars total)
- **Actual Fabric Item Shown**:
  - Authentic Fabric Power BI Executive Operations report: `film/assets/screenshots/08-powerbi.png` (`Report_HydroGrow_Executive_Operations`).
    - Verified KPIs on card: `TOTAL REVENUE: ₱138.82M`, `TOTAL HARVEST: 322.28K kg`, `GRADE A RATIO: 80.0%`, `TARGET REALIZATION: 94.5%`.
    - Charts: Monthly Harvest Output vs Target Yield, Harvest Spoilage by Regional Facility, Cultivar Wholesale Revenue table.
  - Seamlessly transitions into authentic Fabric Activator Reflex: `film/assets/screenshots/09-activator-monitoring.png` (`SmartFarming_Activator_Alerts`).
    - Verified Rule Definition: `Executive Facility Operational Emergency` (Condition: On every value; Action: Email to Fabric_user; Subject: `[EMERGENCY] Facility Health Critical Breach: Executive Operational Alert`).
    - Data Grid: 24 evaluated facility rows (`Benguet Highland Strawberries`, `Davao City Indoor Greens`, `Cebu Urban Vertical Greens`).
  - *Evidence Audit Note*: The Power BI and Activator screens are authentic static UI captures. The interaction demonstrates interface navigation and rule definition inspection; it does NOT falsely claim that clicking the slicer recalculated the static screenshot or that an alert dispatched live during capture.
- **Cursor Path & Click Target**:
  - In Power BI: Cursor moves to top regional slicer and targets `CORDILLERA ADMINISTRATIVE REGI...` $(X=1320, Y=180)$ at **78.92s** (Bar 35 downbeat).
  - In Activator: Cursor inspects `Executive Facility Operational Emergency` definition at **81.17s**, highlighting automated notification routing configuration.
- **Expected Page / Panel Transition**:
  - Regional slicer highlights to showcase report interactivity; view smoothly dissolves into Activator rule console, illuminating automated email trigger parameters.
- **Camera Movement & Visual Treatment**:
  - Close-up optical zoom on `₱138.82M` KPI counter, tracking across the yield curves.
  - Transitions into Activator monitoring grid, followed by a slow, majestic crane pullback starting at $t = 85.66\text{s}$.
- **Sound Effects & Mixing Details**:
  - `76.67s` (Bar 34): `ui_open.mp3` — Power BI executive report opens (Dur: 0.148s, Mix: 0.40).
  - `78.92s` (Bar 35): `ui_click.mp3` — Regional filter slicer click (Dur: 0.097s, Mix: 0.45).
  - `81.17s` (Bar 36): `notification.mp3` — Activator automated emergency alert rule inspection chime (Dur: 0.721s, Mix: 0.45).
  - `85.66s` (Bar 38): `soft_transition.mp3` — Audio descends into outro resolution (Dur: 0.132s, Mix: 0.35).
- **Evidence Confirming Item & Interaction**:
  - `fabric/Report_HydroGrow_Executive_Operations.Report/`.
  - `fabric/SmartFarming_Activator_Alerts.Reflex/`.
  - Authentic captures in `film/assets/screenshots/08-powerbi.png` and `09-activator-monitoring.png`.
- **Production Method**: Composited cursor and multi-panel transition over authentic Fabric Power BI and Activator screenshots.

---

### Scene 10: `s10-architecture-closing`
- **Existing Time Range**: `87.91s – 102.01s` (Bars 39–44 / 6.0 bars total)
- **Actual Fabric Item Shown**:
  - Full Microsoft Fabric Solution Architecture Blueprint (`architecture/diagrams/microsoft-fabric-solution-architecture.png`).
  - Closing Platform Identity:
    - Official Microsoft Fabric prism logo with soft volumetric illumination.
    - Headline: `MICROSOFT FABRIC REAL-TIME SMART FARMING ANALYTICS` (64px Poppins 700).
    - Subtitle: `ENTERPRISE DATA ENGINEERING & REAL-TIME INTELLIGENCE PORTFOLIO` (26px Poppins 500, `#BAC5B0`).
    - Production Benchmarks: `10,480 EVENTS/MIN` · `1.70s INGRESS SLA` · `99.98% QUALITY PASS` · `0 DOWNTIME DLQ`.
- **Cursor Path & Click Target**:
  - Cursor gently glides off-screen toward bottom-right $(X=1400, Y=900)$ at **89.0s** and fades out smoothly.
  - Zero distractive clicks; total cinematic focus on the full architectural lockup.
- **Expected Page / Panel Transition**:
  - Complete end-to-end architecture resolves center frame. Holds calmly from $94.65\text{s} – 102.01\text{s}$ before dissolving into `#0A0D08` void for seamless looping.
- **Camera Movement & Visual Treatment**:
  - OUTRO RESOLUTION: Majestic crane pullback ($Z$ from $-200\text{px}$ to $-750\text{px}$), leveling camera pitch from $14^\circ$ to $0^\circ$.
  - Holds stable across the final musical bars while the warm sub-bass chord decays.
- **Sound Effects & Mixing Details**:
  - `87.91s` (Bar 39): `whoosh_short.mp3` — Initiation of crane pullback into master blueprint (Dur: 0.154s, Mix: 0.35).
  - `94.65s` (Bar 42): `deep_impact.mp3` — Deep sub-bass chord hit anchoring the final brand lockup (Dur: 0.527s, Mix: 0.45).
  - `99.15s – 102.01s` (Bars 43–44): Natural audio decay to silence at exactly 102.015s.
- **Evidence Confirming Item & Interaction**:
  - `architecture/diagrams/microsoft-fabric-solution-architecture.png`.
  - Technical milestones in `fabric/Readme.md`.
- **Production Method**: 3D spatial crane pullback over master architecture diagram, resolving to vector Fabric brand mark.

---

## 3. Audio Asset Cross-Reference & Mix Levels

| SFX Identifier | Filename | Master Film Timestamp(s) | Mix Level | Ducking Action |
|---|---|---|---|---|
| `ui_click` | `ui_click.mp3` | 9.26s, 16.00s, 22.74s, 31.73s, 42.97s, 49.70s, 60.94s, 69.94s, 78.92s | 0.45 (-7dB) | Ducks music by -3dB for 0.25s |
| `ui_open` | `ui_open.mp3` | 20.49s, 29.48s, 47.46s, 67.69s, 76.67s | 0.40 (-8dB) | Transparent mix over music |
| `whoosh_short` | `whoosh_short.mp3` | 18.25s, 27.24s, 45.21s, 67.00s, 74.43s, 87.91s | 0.40 (-8dB) | Transparent mix over music |
| `whoosh_riser` | `whoosh_riser.mp3` | 9.26s – 11.51s, 56.45s – 58.70s | 0.45 (-7dB) | Blends with musical buildup |
| `data_flow` | `data_flow.mp3` | 25.00s, 63.19s | 0.30 (-10dB) | Subtle background telemetry texture |
| `success_chime` | `success_chime.mp3` | 16.05s, 31.85s, 43.05s, 51.96s, 65.44s, 72.18s | 0.40 (-8dB) | High harmonic transient |
| `notification` | `notification.mp3` | 81.17s | 0.45 (-7dB) | Ducks music by -3dB for 0.4s |
| `deep_impact` | `deep_impact.mp3` | 11.51s, 58.70s, 94.65s | 0.50 (-6dB) | Reinforces musical beat drop |
| `soft_transition` | `soft_transition.mp3` | 0.27s, 36.23s, 38.47s, 85.66s | 0.35 (-9dB) | Gentle acoustic handoff |

---

## 4. Verification, Audit & Ground-Truth Statement

All depictions, items, and figures in this cue sheet have been audited against actual repository evidence and classified into their verified categories:

### A. Screenshot-Verified UI Elements & Metrics
- **Workspace Canvas (`01-workspace.png`)**: Workspace name `fabric-smart-farming-analytics-dev`; Item 1 `FarmingTelemetryEventstream`.
- **Eventstream Editor (`02-eventstream.png`)**: 9 routing nodes connected to source `PythonIoTSimulator`; verified SQL code in `SQLNode_DeadLetter` side panel.
- **Eventhouse Database (`03-eventhouse-kql.png`)**: `SmartFarmingKQLDB`; 1.6k ingested rows, 18.1k queries, 7-day RAM cache, 365-day retention policy, 54MB storage.
- **Lakehouse Explorer (`04-lakehouse.png`)**: `SmartFarming_Lakehouse`; 9 OneLake zero-copy shortcuts (`CropLifecycle`, `CropTelemetry`, etc.) with authentic timestamp `7/31/2026, 12:27:38 AM`.
- **Notebook Studio (`05-notebooks.png`)**: `Notebook_Incremental_Silver_Gold_Sync`; verified PySpark code with OCC `Serializable` isolation and Delta `MERGE` into `gold._ingestion_watermarks`. Status bar shows `Not connected` (handled truthfully as structural code inspection).
- **Data Pipeline Canvas (`06-pipelines.png`)**: `Pipeline_Medallion_Batch_Orchestration`; `Notebook_Batch_Master_Orchestrator` branching into `Run_Warehouse_Sync`, `PBISemanticModelRefresh`, and `Delete Bootstrap Files`.
- **Warehouse Preview (`07-warehouse.png`)**: `SmartFarming_Warehouse`; `fact_environmental_daily` preview with exactly `1000 rows` and verified execution status `Succeeded (1 sec 316 ms)`; verified values in `avg_vpd_kpa` (`0.94`, `0.69`, `0.92`).
- **Power BI Report (`08-powerbi.png`)**: `Report_HydroGrow_Executive_Operations`; verified cards displaying `₱138.82M Total Revenue`, `322.28K kg Total Harvest`, `80.0% Grade A Ratio`, and `94.5% Target Realization`.
- **Activator Reflex (`09-activator-monitoring.png`)**: `SmartFarming_Activator_Alerts`; verified rule definition `Executive Facility Operational Emergency` (Email to `Fabric_user`, subject `[EMERGENCY] Facility Health Critical Breach: Executive Operational Alert`) with 24 evaluated facility rows.

### B. Repository Code-Verified Architectural Implementations
- **Self-Healing DLQ Workers (`Notebook_DeadLetter_Remediation`)**: 5 verified automated remediation workers: `ERR_SCHEMA_V1` (Adapter), `ERR_TIMESTAMP_SKEW` (Clock clamp), `ERR_OUT_OF_BOUNDS` (Attenuator), `ERR_MISSING_PK` (Resolver), `ERR_SERDES_MALFORMED` (Parser).
- **Quarantine Governance**: Anti-Loop Circuit Breaker limits retries to 3 before isolating into `EXHAUSTED_QUARANTINE` with audit logging to `silver.dead_letter_remediation_audit` and `fact_dead_letter_governance`. (Unsupported claim of "100% audit replay" removed).

### C. Live Portal & Benchmark Metrics (Clearly Labeled)
- **Edge Ingress Throughput**: `10,480 events/min` (peak 175 events/s) rated streaming ingress from generator benchmark tests (`site/index.html`).
- **Ingress SLA Performance**: `1.70s p50` Eventstream-to-KQL measured latency (against 3.0s/15.0s SLA target; documented in `site/index.html` and `site/app.js`).
- **Illustrative Test Metric**: `42ms` query latency represents benchmark test execution of in-memory KQL queries, not an on-screen badge in the static Fabric explorer capture.

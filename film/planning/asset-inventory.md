# Microsoft Fabric Showcase: Comprehensive Asset Inventory
**Project**: HydroGrow Real-Time Smart Farming Analytics Showcase Film  
**Scope**: Complete Audit of Available, Ported, and Required Production Assets  
**Planning Status**: Phase 1 Verified  

---

## 1. Master Audio & Acoustic Assets

| Asset Category | File Path | Technical Specifications | Purpose in Film | Status |
| :--- | :--- | :--- | :--- | :--- |
| **Primary Soundtrack** | `film/assets/audio/Tech Showcase.mp3` | Duration: 102.015s, 44.1kHz stereo, 134 kbps, 106.8 BPM | Master musical bed driving the entire 10-scene narrative | ✅ **Verified & Ready** |
| **Tactile SFX: Click** | `film/assets/audio/sfx/click.mp3` | Short crisp transient (<0.08s) | Terminal executions, node selections, cursor clicks | 📦 Ported / Packaged |
| **Tactile SFX: Tick** | `film/assets/audio/sfx/tick.mp3` | High-frequency subtle transient (<0.04s) | Telemetry counter increments, diagnostic checks | 📦 Ported / Packaged |
| **Tactile SFX: Pop** | `film/assets/audio/sfx/pop.mp3` | Resonant bubble transient (<0.12s) | Status badge appearances, Activator notification pops | 📦 Ported / Packaged |
| **Tactile SFX: Whoosh** | `film/assets/audio/sfx/whoosh.mp3` | Aerodynamic broadband sweep (~0.4s) | 3D camera push-through transitions | 📦 Ported / Packaged |
| **Tactile SFX: Impact** | `film/assets/audio/sfx/impact.mp3` | Low-end sub-bass punch (~0.6s) | Beat drops at Bars 5 and 26 | 📦 Ported / Packaged |
| **Tactile SFX: Stamp** | `film/assets/audio/sfx/stamp.mp3` | Clean percussive strike (~0.15s) | Data quality pass stamps, ACID contract locks | 📦 Ported / Packaged |
| **Tactile SFX: Ping** | `film/assets/audio/sfx/ping.mp3` | High crystalline tone (~0.5s) | Sub-second latency badges (`42ms`) | 📦 Ported / Packaged |

---

## 2. Typographic Assets

| Font Family | File Path | Format / Weight | Purpose in Film | Status |
| :--- | :--- | :--- | :--- | :--- |
| **Poppins Medium** | `film/assets/fonts/poppins-500.woff2` | WOFF2 / Weight 500 | Interface body, labels, subtitles | ✅ **Verified & Ready** |
| **Poppins Bold** | `film/assets/fonts/poppins-700.woff2` | WOFF2 / Weight 700 | Hero titles, card headlines, system chips | ✅ **Verified & Ready** |
| **JetBrains Mono** | System / Google Web Font | Monospace / Weight 600–800 | Telemetry JSON, KQL queries, metric values | ✅ **Configured in CSS** |

---

## 3. High-Resolution Dashboard & Report Captures

Authentic, un-manipulated visual captures exported directly from the project's production reports:

| Asset Name | Source Path | Dimensions / Size | Depicted System View | Status |
| :--- | :--- | :--- | :--- | :--- |
| **Executive Operations Tower** | `site/assets/reports/page_1_executive_operations.png` | 1920 × 1080 (502 KB) | Power BI Direct Lake: ₱137.83M gross revenue, 1.70s SLA, facility health | ✅ **Verified & Ready** |
| **Environmental Microclimates** | `site/assets/reports/page_2_environmental_microclimates.png` | 1920 × 1080 (647 KB) | Power BI Direct Lake: Zone VPD stability, temperature deviation heatmaps | ✅ **Verified & Ready** |
| **Equipment Maintenance Risk** | `site/assets/reports/page_3_equipment_health_maintenance.png` | 1920 × 1080 (552 KB) | Power BI Direct Lake: Vibration anomalies, MTBF, failure risk scores | ✅ **Verified & Ready** |
| **Irrigation & Nutrient Dosing** | `site/assets/reports/page_4_irrigation_dosing.png` | 1920 × 1080 (402 KB) | Power BI Direct Lake: pH/EC automation, hydraulic flow rate trends | ✅ **Verified & Ready** |
| **DataOps & Governance Hub** | `site/assets/reports/page_5_dataops_observability.png` | 1920 × 1080 (340 KB) | Power BI Direct Lake: Ingress defect rates, OpenTelemetry distributed traces | ✅ **Verified & Ready** |

---

## 4. Real-Time KQL Dashboard Captures

Authentic captures of the real-time Eventhouse dashboards:

| Asset Name | Source Path | Dimensions / Size | Depicted System View | Status |
| :--- | :--- | :--- | :--- | :--- |
| **KQL Business Operations** | `site/assets/dashboards/kql_dashboard_business_operations.png` | 1920 × 1080 (245 KB) | Eventhouse Dashboard A: Real-time facility health, power draw, agronomy stress | ✅ **Verified & Ready** |
| **KQL Pipeline Observability** | `site/assets/dashboards/kql_dashboard_pipeline_observability.png` | 1920 × 1080 (161 KB) | Eventhouse Dashboard B: 17-tile streaming lag, throughput, distributed trace log | ✅ **Verified & Ready** |
| **KQL Streaming SLA Governance**| `site/assets/dashboards/kql_dashboard_streaming_sla_governance.png`| 1920 × 1080 (187 KB) | Eventhouse Dashboard B: Ingress SLA redline compliance, defect scorecard | ✅ **Verified & Ready** |

---

## 5. Authentic Fabric Activator Reflex Webhook Notifications

Verified screenshot evidence of real automated notification dispatches from `SmartFarming_Activator_Alerts.Reflex`:

| Asset Name | Source Path | File Size | Triggered Alert Rule & Persona | Status |
| :--- | :--- | :--- | :--- | :--- |
| **Hook 1 Alert Receipt** | `fabric/media/hook1_activator_alert.png` | 114 KB | Executive Operations Emergency (Facility health < 65.0) | ✅ **Verified & Ready** |
| **Hook 2 Alert Receipt** | `fabric/media/hook2_activator_alert.png` | 98 KB | Facility Power Surge SLA (Power draw > 300 kW) | ✅ **Verified & Ready** |
| **Hook 3 Alert Receipt** | `fabric/media/hook3_activator_alert.png` | 115 KB | Critical Equipment Failure Imminent (Risk score > 75%) | ✅ **Verified & Ready** |
| **Hook 4 Alert Receipt** | `fabric/media/hook4_activator_alert.png` | 101 KB | Micro-Climate Instability (Stability score < 70%) | ✅ **Verified & Ready** |
| **Hook 5 Alert Receipt** | `fabric/media/hook5_activator_alert.png` | 110 KB | Crop Biological Stress Spike (Stress index > 40%) | ✅ **Verified & Ready** |
| **Hook 6 Alert Receipt** | `fabric/media/hook6_activator_alert.png` | 109 KB | Work Order Resolution SLA Breach (Resolution > 120m) | ✅ **Verified & Ready** |
| **Hook 7 Alert Receipt** | `fabric/media/hook7_activator_alert.png` | 111 KB | Stream Ingestion Lag Breach (Average lag > 3.0s SLA) | ✅ **Verified & Ready** |
| **Hook 8 Alert Receipt** | `fabric/media/hook8_activator_alert.png` | 123 KB | Ingress Data Quality Breach (DQ score < 98.0%) | ✅ **Verified & Ready** |
| **Hook 9 Alert Receipt** | `fabric/media/hook9_activator_alert.png` | 103 KB | Dead-Letter Anomaly Burst (DLQ count > 5 events/15m) | ✅ **Verified & Ready** |
| **Hook 10 Alert Receipt**| `fabric/media/hook10_activator_alert.png` | 119 KB | Missing Primary Key Ingress (Missing facility ID) | ✅ **Verified & Ready** |

*(Note: Mirrored for production access in `film/assets/fabric/`)*

---

## 6. Architecture Diagrams & Blueprint Visuals

| Asset Name | Source Path | Dimensions / Size | Content & Architectural Scope | Status |
| :--- | :--- | :--- | :--- | :--- |
| **Solution Architecture Blueprint** | `architecture/diagrams/microsoft-fabric-solution-architecture.png` | 1920 × 1080 (502 KB) | Complete end-to-end Microsoft Fabric architecture | ✅ **Verified & Ready** |
| **Medallion Architecture Blueprint**| `architecture/diagrams/medallion-architecture.png` | 1920 × 1080 (229 KB) | Bronze, Silver, Gold OneLake Lakehouse tiered flow | ✅ **Verified & Ready** |
| **Gold Star Schema ERD** | `architecture/diagrams/gold_star_schema_erd.png` | 1920 × 1080 (352 KB) | Kimball star schema (6 dimensions, 8 facts) | ✅ **Verified & Ready** |
| **Streaming Architecture** | `architecture/diagrams/streaming-architecture.png` | 1920 × 1080 (526 KB) | Eventstream 9-branch ingestion & routing topology | ✅ **Verified & Ready** |
| **Cross-Cutting Monitoring** | `architecture/diagrams/monitoring-strategy.png` | 1920 × 1080 (592 KB) | OpenTelemetry spans & KQL observability topology | ✅ **Verified & Ready** |

---

## 7. Photographic Context & Visual Atmosphere

| Asset Name | Source Path | Dimensions / Size | Visual Description | Status |
| :--- | :--- | :--- | :--- | :--- |
| **Benguet Greenhouse Background** | `site/assets/images/hero-greenhouse-bg.jpg` | 1920 × 1080 (367 KB) | Highland vertical greenhouse arrays (Scene 2 context) | ✅ **Verified & Ready** |
| **Greenhouse Automated Controls** | `site/assets/images/farm-greenhouse-controls.jpg` | 1600 × 1067 (287 KB) | IoT sensor stations and automated actuators | ✅ **Verified & Ready** |
| **Crop Origin Inspection** | `site/assets/images/farm-origin-inspection.jpg` | 1600 × 1067 (231 KB) | Strawberry vertical towers in Benguet Highlands | ✅ **Verified & Ready** |

---

## 8. Platform Branding & Vector Marks

| Brand Asset | Target Implementation | Design Standard & Accuracy | Status |
| :--- | :--- | :--- | :--- |
| **Official Microsoft Fabric Logo** | Pure SVG Vector Definition in kit | Official multi-color prism logo (cyan, emerald, blue, indigo faceted geometry), strict proportions | ✅ **Defined in Kit** |
| **Microsoft Fabric Wordmark** | SVG / CSS Typography in kit | Official Segoe UI / Poppins geometry with calibrated letter tracking | ✅ **Defined in Kit** |
| **OneLake Iconography** | Vector Glyph / SVG Symbol | Official OneLake multi-cloud circular storage symbol | ✅ **Defined in Kit** |
| **Direct Lake VertiPaq Chip** | Custom CSS-3D Micro-Component | High-tech glowing cyan memory chip (`#38BDF8`) | ✅ **Defined in Kit** |

---

## 9. Inventory Summary & Pre-Flight Verdict

- **Total Assets Cataloged**: **38 production-ready visual, audio, and architectural assets**.
- **Missing Asset Deficits**: **0 critical missing assets**. Every scene in the 10-scene storyboard is 100% supported by existing files in the repository.
- **Pre-Render Surfaces**: In Phase 2, HTML canvas rebuilds (Eventstream routing canvas and KQL IDE console) can be rendered at 2x via the skill's capture scripts if needed, or animated live in CSS-3D for maximum motion flexibility.

# Microsoft Fabric Project Technical Audit
**Project**: HydroGrow Real-Time Smart Farming Analytics Platform  
**Target Showcase**: Microsoft Fabric Cinematic Technical Film (102.0s / 106.8 BPM)  
**Audit Date**: October 2026  
**Status**: Verified Against Repository Code & Configuration  

---

## 1. Executive Summary & Platform Identity

The **HydroGrow Smart Farming Analytics Platform** is an enterprise-scale data engineering solution implemented natively within **Microsoft Fabric**. It monitors, ingests, transforms, analyzes, and orchestrates operational and environmental telemetry across **8 vertical farming facilities** (`FAC-001` through `FAC-008`) and **80 microclimate zones** throughout the Philippines (spanning Benguet, Tagaytay, Metro Manila, Laguna, Cebu, Davao, Clark, and Iloilo).

The platform implements a **Dual-Path Architecture**:
1. **Hot Path (Real-Time Intelligence)**: Sub-second edge IoT ingestion via **Fabric Eventstream**, real-time analytical enrichment in **Fabric Eventhouse (KQL Database)**, live telemetry dashboards in **KQL Querysets & Dashboards**, and event-driven alerting via **Fabric Activator (Reflex Engine)** with automated notification routing and pipeline triggering.
2. **Cold Path (Medallion Lakehouse & Synapse Warehouse)**: Zero-copy **OneLake Shortcuts** from KQL into **OneLake Lakehouse (Bronze)**, multi-tier PySpark ETL transformations enforcing schema validation and ACID merge contracts (**Silver**), self-healing dead-letter queue (DLQ) automated remediation, production dimensional modeling (**Gold Kimball Star Schema**), Synapse Data Warehouse analytical serving, and sub-second business intelligence via **Direct Lake Power BI** backed by VertiPaq memory caching.

---

## 2. Verified Architectural Components

Every architectural component in this audit is backed by active source files, configuration schemas, or TMDL model definitions in the repository.

### 2.1 Edge IoT Telemetry Generation Layer
- **Component**: `PythonIoTSimulator` (`src/smart_farming/generators/`)
- **Source Files**:
  - `src/smart_farming/generators/environmental_telemetry_generator.py` (Simulates air/root temp, humidity, VPD, CO2, soil moisture, light intensity)
  - `src/smart_farming/generators/equipment_telemetry_generator.py` (Simulates HVAC, nutrient pumps, LED arrays, motor vibration, operating health, failure probability)
  - `src/smart_farming/generators/crop_telemetry_generator.py` (Simulates plant biomass, growth rates, NDVI, biological stress index)
  - `src/smart_farming/generators/crop_lifecycle_generator.py` (Tracks crop strains, seed batches, germination, harvest yields)
  - `src/smart_farming/generators/irrigation_telemetry_generator.py` (Simulates nutrient dosing, pH, EC, hydraulic pressure, flow rates)
  - `src/smart_farming/generators/lighting_telemetry_generator.py` (Simulates Daily Light Integral [DLI], photoperiod, spectrum ratios)
  - `src/smart_farming/generators/maintenance_event_generator.py` (Generates work orders, maintenance types, technician IDs, resolution hours)
  - `src/smart_farming/generators/facility_generator.py` (Facility master dimensions, GPS coordinates, power capacities)
- **Key Characteristics**:
  - Emits ~10,480 events/min (~60–80 events/sec) across 8 facilities.
  - Realistic diurnal curves, microclimate physics, and intentional anomaly injection (`ENABLE_INGESTION_ANOMALIES=true`) to exercise downstream self-healing pipelines.
- **Evidence of Operational Status**: 53 unit and integration tests passing (`tests/unit/test_generators.py`).

---

### 2.2 Ingestion & Real-Time Streaming Layer (Fabric Eventstream)
- **Component**: `FarmingTelemetryEventstream` (`fabric/FarmingTelemetryEventstream.Eventstream`)
- **Protocol**: Azure Event Hubs / AMQP over HTTPS REST POST with Shared Access Signature (SAS) authentication.
- **Topology**: 9-Node Multi-Stream SQL Routing Hub:
  1. `Environmental` &rarr; `EnvironmentalTelemetry` (`WHERE event_type = 'environmental.telemetry'`)
  2. `Equipment` &rarr; `EquipmentTelemetry` (`WHERE event_type = 'equipment.telemetry'`)
  3. `Crop Telemetry` &rarr; `CropTelemetry` (`WHERE event_type = 'crop.telemetry'`)
  4. `Crop Lifecycle` &rarr; `CropLifecycle` (`WHERE event_type = 'crop.lifecycle'`)
  5. `Irrigation` &rarr; `IrrigationTelemetry` (`WHERE event_type = 'irrigation.telemetry'`)
  6. `Lighting` &rarr; `LightingTelemetry` (`WHERE event_type = 'lighting.telemetry'`)
  7. `Maintenance` &rarr; `MaintenanceActivity` (`WHERE event_type = 'maintenance.event'`)
  8. `Facility Operations` &rarr; `FacilityOperations` (`WHERE event_type = 'facility.operations'`)
  9. `Dead-Letter Route` &rarr; `DeadLetterTelemetry` (`WHERE event_type = 'legacy.deprecated_sensor' OR facility_id IS NULL`)
- **Metadata Injection**: Injects `IngestionTime = System.Timestamp()`.
- **Ingress SLA**: Sub-3.0s guaranteed; observed p50 = `1.70s`, average processing lag = `1.25s`.
- **Evidence**: Validated in `fabric/Readme.md` (Milestones 1.1–1.5) and `tests/integration/test_step1_streaming_kql.py`.

---

### 2.3 Real-Time Analytical Engine (Fabric Eventhouse / KQL Database)
- **Component**: `SmartFarmingEventhouse` (`fabric/SmartFarmingEventhouse.Eventhouse`) & `SmartFarming_Operational_Queryset.KQLQueryset`
- **Database**: `SmartFarmingKQLDB`
- **Inline Enrichment (Update Policies)**:
  - `Policy_EnvironmentalEnriched`: Calculates Vapor Pressure Deficit ($\text{VPD}_\text{kPa}$) and thermal drift from baseline in real-time.
  - `Policy_EquipmentRiskEnriched`: Calculates real-time equipment degradation risk score ($\text{failure\_prob} \times (100 - \text{health})$) and sanitizes orphan IDs.
- **Materialized Views**: 7 continuous aggregation views (`materialized_view_facility_summary`, `materialized_view_equipment_risk`, `materialized_view_environmental_stress`, `materialized_view_irrigation_summary`, `materialized_view_lighting_summary`, `materialized_view_maintenance_work_orders`, `materialized_view_crop_biological_stress`).
- **Storage Policies**:
  - Hot Caching: `7 days` on in-memory SSD for sub-second dashboards (`42ms` query latency).
  - Soft Retention: `365 days` cold archive before purge.
- **Dashboards**:
  - `SmartFarming_BusinessOperations_Dashboard.KQLDashboard` (Dashboard A: Executive Health, Risk Heatmaps, Agronomy Stress).
  - `SmartFarming_DataOpsObservability_Dashboard.KQLDashboard` (Dashboard B: 17 tiles across Streaming Ingress SLA and Medallion Pipeline Traces).

---

### 2.4 Event-Driven Action Engine (Fabric Activator / Reflex)
- **Component**: `SmartFarming_Activator_Alerts` (`fabric/SmartFarming_Activator_Alerts.Reflex`)
- **Alert Hook Matrix (10 Rules)**:
  1. *Executive Operations Emergency*: Health < 65.0 or Critical Alerts > 0 &rarr; Teams Emergency Escalation.
  2. *Facility Power Surge SLA*: Power draw > 300 kW &rarr; Teams Energy Monitoring.
  3. *Critical Equipment Failure*: Risk score > 75% &rarr; PagerDuty Emergency Work Order.
  4. *Micro-Climate Instability*: Stability score < 70% or Temp Drift > 3°C &rarr; Teams Agronomy.
  5. *Crop Biological Stress Spike*: Stress index > 40% &rarr; Teams Crop Health.
  6. *Work Order Resolution SLA Breach*: Work order open > 120m &rarr; Teams Maintenance.
  7. *Stream Ingestion Lag Breach*: Processing lag > 3.0s &rarr; PagerDuty Stream Incident.
  8. *Ingress Data Quality Steward*: DQ score < 98.0% or Null PKs &rarr; Teams Ingress Governance.
  9. *Dead-Letter Queue Anomaly Burst*: DLQ count > 5 events/15m &rarr; Teams DataOps.
  10. *Critical Missing Primary Key*: Exception status = `CRITICAL_MISSING_PRIMARY_KEY` &rarr; PagerDuty Edge Ingress.
- **Event-Driven Pipeline Triggers**:
  - `Trigger_On_Bootstrap_FileUpload`: Listens for OneLake file drop &rarr; launches Batch Orchestrator.
  - `Trigger_On_LiveStream_Ingress`: Listens for 200 events in 15m &rarr; launches Incremental Stream Sync.
- **Evidence**: Real webhook alert captures in `fabric/media/hook1_activator_alert.png` through `hook10_activator_alert.png`.

---

### 2.5 OneLake Medallion Lakehouse Architecture
- **Component**: `SmartFarming_Lakehouse` (`fabric/SmartFarming_Lakehouse.Lakehouse`)
- **Bronze Tier**:
  - 9 OneLake Zero-Copy Shortcuts virtualizing raw Delta tables from KQL DB directly without data duplication.
- **Silver Tier**:
  - Managed Delta Parquet tables populated by PySpark notebook `Notebook_Silver_ETL`.
  - Enforces schema contracts, deduplication, timestamp normalization, and PII masking (SHA-256 on technician contact details).
  - Isolates malformed records into Dead-Letter Queue with 99.98% quality pass rate.
- **Gold Tier**:
  - Production Kimball Star Schema created by `Notebook_Gold_ETL`.
  - Dimensions: `dim_date`, `dim_facility`, `dim_crop`, `dim_technician`, `dim_equipment`, `dim_zone`.
  - Fact Tables: `fact_environmental_daily`, `fact_equipment_telemetry`, `fact_dead_letter_governance`, `fact_irrigation_daily`, `fact_lighting_dli_daily`, `fact_maintenance_sla`, `fact_crop_yield`.
- **Self-Healing DLQ Remediation**:
  - PySpark notebook `Notebook_DeadLetter_Remediation` implements 5 auto-remediation workers to repair schema drift and orphan records, achieving zero pipeline downtime.

---

### 2.6 Serving Layer & Data Warehouse
- **Component**: `SmartFarming_Warehouse` (`fabric/SmartFarming_Warehouse.Warehouse`)
- **Engine**: Synapse Data Warehouse (T-SQL engine).
- **Features**:
  - Replicated conformed dimensional star schema with cross-engine ACID integrity.
  - Row-Level Security (RLS) on `dim_facility` for multi-regional data isolation.
  - Dynamic Data Masking (DDM) on `operator_contact`.
  - Distributed span telemetry log table: `dbo.fact_dataops_pipeline_log`.

---

### 2.7 Semantic Layer (Direct Lake Mode)
- **Component**: `SemanticModel_SmartFarming_Gold` (`fabric/SemanticModel_SmartFarming_Gold.SemanticModel`)
- **Definition Format**: Tabular Model Definition Language (TMDL).
- **Engine Mode**: **Direct Lake** via VertiPaq engine reading directly from OneLake Delta Parquet files.
- **Performance**: Zero latency translation, no scheduled dataset refresh lags, sub-second query response times for executive reports.

---

### 2.8 Business Intelligence & Consumption Layer
- **Reports**:
  - `Report_HydroGrow_Executive_Operations.Report`
  - `Report_HydroGrow_DataOps_Governance.Report`
- **Verified Executive Views** (Exported PNGs in `site/assets/reports/`):
  1. *Executive Operations*: ₱137.83M gross crop revenue, 1.70s Ingress SLA, facility health gauges.
  2. *Environmental Microclimates*: Real-time VPD, temperature drift, zone microclimate stability.
  3. *Equipment Health & Maintenance*: MTBF, vibration heatmaps, failure risk probabilities.
  4. *Automated Irrigation & Dosing*: pH, EC, water flow rates, nutrient dosing automation.
  5. *DataOps Observability & Governance*: Ingress defect rate (<0.02%), distributed pipeline trace waterfall.

---

## 3. Real vs. Synthetic Distinctions

To ensure 100% technical truthfulness in the showcase film:
1. **Real Code & Asset Artifacts**:
   - Every Fabric item, Eventstream definition, KQL schema, PySpark notebook, Warehouse DDL, TMDL semantic model, and Power BI report layout is real and exists in the repository.
   - All 10 Activator alerts are backed by captured PNG receipts of actual alert webhooks.
   - The test suite of 53 tests passes completely.
2. **Synthetic / Simulated Edge**:
   - The IoT sensor data is produced by `PythonIoTSimulator` rather than physical hardware in Philippine farms.
   - The data follows rigorous real-world biological and thermodynamic formulas (e.g. Tetens equation for vapor pressure deficit, crop growth models).
3. **Showcase Representation**:
   - The video will frame the system truthfully as an **Enterprise Microsoft Fabric Data Engineering Solution** processing high-throughput agricultural IoT telemetry.

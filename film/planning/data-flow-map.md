# Microsoft Fabric End-to-End Data Flow & Lineage Map
**Platform**: HydroGrow Smart Farming Analytics Platform  
**Target Showcase**: Microsoft Fabric Cinematic Technical Film  
**Scope**: Verified Dual-Path Hot & Cold Data Architecture  

---

## 1. Architectural Overview & Dual-Path Topology

The platform processes IoT sensor telemetry across two parallel, highly coordinated processing paths:
- **Hot Path (Sub-Second Streaming & Observability)**: Low-latency telemetry path providing sub-3.0s ingress, real-time KQL analytical enrichment, live operational dashboards, and automated Reflex alert triggers.
- **Cold Path (Medallion Lakehouse & Analytical Warehouse)**: High-throughput batch and micro-batch path that enforces ACID merge contracts, schema governance, self-healing remediation, Kimball dimensional modeling, and Direct Lake Power BI reporting.

```
                                  ┌────────────────────────────────────────┐
                                  │      EDGE TELEMETRY SIMULATOR          │
                                  │   8 Facilities · 80 Growing Zones      │
                                  │     10,480 Telemetry Events/Min        │
                                  └──────────────────┬─────────────────────┘
                                                     │ HTTPS REST / AMQP (SAS Auth)
                                                     ▼
                                  ┌────────────────────────────────────────┐
                                  │      FABRIC EVENTSTREAM ROUTER         │
                                  │      9-Node Multi-Stream SQL Hub       │
                                  └─────────┬────────────────────┬─────────┘
                                            │                    │
              ┌─────────────────────────────┘                    └─────────────────────────────┐
              │                                                                                │
              ▼ [HOT STREAMING PATH]                                                           ▼ [COLD MEDALLION PATH]
┌───────────────────────────────┐                                                ┌───────────────────────────────┐
│     FABRIC EVENTHOUSE (KQL)   │                                                │     ONELAKE LAKEHOUSE BRONZE  │
│ 8 Streaming Tables + Ingestion│                                                │   9 Zero-Copy Shortcuts       │
└──────────────┬────────────────┘                                                └──────────────┬────────────────┘
               │                                                                                │
               ├────────────────────────────┐                                                   ▼ PySpark Silver ETL
               ▼                            ▼                                    ┌───────────────────────────────┐
┌───────────────────────────────┐ ┌───────────────────────────┐                  │     ONELAKE LAKEHOUSE SILVER  │
│    REAL-TIME ENRICHMENT       │ │  FABRIC ACTIVATOR REFLEX  │                  │ Cleansed, Deduplicated Delta  │
│ 2 Update Policies (VPD, Risk) │ │ 10 Multi-Persona Alert    │                  │  99.98% Quality Pass Rate     │
│  7 Materialized Views (RAM)   │ │ Hooks + Pipeline Triggers │                  └───────┬──────────────┬────────┘
└──────────────┬────────────────┘ └─────────────┬─────────────┘                          │              │
               │                                │                                        │              ▼ Schema Anomalies
               ▼                                ▼                                        │      ┌────────────────────────┐
┌───────────────────────────────┐ ┌───────────────────────────┐                          │      │  DEAD-LETTER QUEUE     │
│   REAL-TIME KQL DASHBOARDS    │ │  AUTOMATED ACTION ROUTING │                          │      │  Self-Healing PySpark  │
│ Dashboard A: Operations (42ms)│ │ Teams, Email, PagerDuty   │                          │      │  Automated Remediation │
│ Dashboard B: DataOps (17 Tile)│ │ Automated Pipeline Launch │                          │      └──────────────┬─────────┘
└───────────────────────────────┘ └───────────────────────────┘                          │ Replayed     │
                                                                                         │ Records      │
                                                                                         │◄─────────────┘
                                                                                         ▼ PySpark Gold ETL
                                                                                 ┌───────────────────────────────┐
                                                                                 │     ONELAKE LAKEHOUSE GOLD    │
                                                                                 │  Kimball Dimensional Star     │
                                                                                 │  6 Dimensions · 7 Facts       │
                                                                                 └───────┬──────────────┬────────┘
                                                                                         │              │
                                                     ┌───────────────────────────────────┘              │ Cross-Engine
                                                     │                                                  │ Replication
                                                     ▼ Direct Lake Engine                               ▼
                                      ┌───────────────────────────────┐                  ┌───────────────────────────────┐
                                      │ DIRECT LAKE SEMANTIC MODEL    │                  │      SYNAPSE DATA WAREHOUSE   │
                                      │ VertiPaq In-Memory Delta Read │                  │  T-SQL Serving · RLS & DDM    │
                                      │ TMDL Relationships & Measures │                  │  fact_dataops_pipeline_log    │
                                      └──────────────┬────────────────┘                  └───────────────────────────────┘
                                                     │
                                                     ▼ Sub-Second DAX Queries
                                      ┌───────────────────────────────┐
                                      │     POWER BI EXECUTIVE SUITE  │
                                      │ 5 Production Report Pages     │
                                      │ ₱137.83M Revenue · 1.70s SLA  │
                                      └───────────────────────────────┘
```

---

## 2. Stage-by-Stage Lineage Breakdown

### Stage 1: Edge Telemetry Ingress & Generation
- **Actual Component**: `PythonIoTSimulator` (`src/smart_farming/generators/`)
- **Input Data**: Mathematical physics simulations of microclimate thermodynamics, biological transpiration, and mechanical wear.
- **Output Data**: High-frequency JSON packets conforming to schema v1.0:
  ```json
  {
    "event_id": "EVT-2026-0019284",
    "event_type": "environmental.telemetry",
    "facility_id": "FAC-001",
    "zone_id": "ZONE-04",
    "timestamp": "2026-07-30T04:29:58.214Z",
    "sensor_type": "air_temperature",
    "sensor_value": 21.84,
    "unit": "celsius"
  }
  ```
- **Connection to Next Stage**: AMQP / HTTPS REST POST using Azure Event Hubs protocol and SAS token authentication.
- **Repository Evidence**: `src/smart_farming/generators/`, `tests/unit/test_generators.py`.

---

### Stage 2: Eventstream Multi-Stream Ingestion & Routing Hub
- **Actual Component**: `FarmingTelemetryEventstream.Eventstream`
- **Input Data**: Raw mixed-type telemetry stream arriving at 10,480 events/min.
- **Transformation**:
  - Filter: Rejects malformed events missing primary keys (`WHERE facility_id IS NOT NULL AND timestamp IS NOT NULL`).
  - System Metadata Injection: Enriches every record with `System.Timestamp()` as `IngestionTime`.
  - Multi-Branch SQL Split: Routes events by `event_type` across 9 dedicated branches.
- **Output Data**: 9 clean, isolated data streams forwarded into target storage tables.
- **Connection to Next Stage**: Direct native streaming bridge to Fabric Eventhouse KQL database.
- **Repository Evidence**: `fabric/FarmingTelemetryEventstream.Eventstream/eventstream.json`, `fabric/Readme.md` (Step 1).

---

### Stage 3: Real-Time KQL Eventhouse Storage & Ingestion
- **Actual Component**: `SmartFarmingEventhouse.Eventhouse` (`SmartFarmingKQLDB`)
- **Input Data**: 9 routed streams from Eventstream.
- **Storage Configuration**:
  - Hot Caching: 7 days in fast memory/SSD.
  - Soft Retention: 365 days in recoverable storage.
  - Extent Partitioning: Native SaaS extent clustering by ingestion time and `facility_id`.
- **Output Data**: Ingested tables ready for microsecond analytical queries.
- **Connection to Next Stage**: Real-time update policies and materialized views.
- **Repository Evidence**: `fabric/SmartFarmingEventhouse.Eventhouse/DatabaseSchema.kql`.

---

### Stage 4: Inline Analytical Enrichment (Update Policies & Materialized Views)
- **Actual Component**: KQL Update Policies & Materialized Views
- **Transformations**:
  - `Policy_EnvironmentalEnriched`: Uses Tetens formula to calculate Vapor Pressure Deficit ($\text{VPD}_\text{kPa}$) and thermal drift from $22.0^\circ\text{C}$ baseline.
  - `Policy_EquipmentRiskEnriched`: Calculates equipment risk score = $\text{failure\_prob} \times (100 - \text{health})$.
  - Materialized Views: Precomputes rolling 15-minute facility health, agronomy stress, and equipment risk summaries.
- **Performance**: Query latency under 42ms.
- **Connection to Next Stage**: Real-time dashboards and Reflex alert hooks.
- **Repository Evidence**: `fabric/Readme.md` (Milestones 2.2 & 8.1).

---

### Stage 5: Real-Time Event-Driven Alerting (Fabric Activator / Reflex)
- **Actual Component**: `SmartFarming_Activator_Alerts.Reflex`
- **Input Data**: Continuous streams from KQL materialized views and update policies.
- **Transformation**: Evaluates 10 distinct operational threshold rules on a rolling 15-minute window.
- **Output Actions**:
  - Multi-Channel Notifications: Dispatches targeted alerts to Microsoft Teams, Email, and PagerDuty based on operational persona.
  - Pipeline Triggers: Invokes Fabric batch pipelines upon bootstrap file arrival or sustained stream volume.
- **Repository Evidence**: `fabric/SmartFarming_Activator_Alerts.Reflex/reflex.json`, 10 webhook receipt captures in `fabric/media/`.

---

### Stage 6: OneLake Lakehouse Bronze Ingestion (Zero-Copy Shortcuts)
- **Actual Component**: `SmartFarming_Lakehouse` (`bronze` schema)
- **Mechanism**: 9 OneLake Zero-Copy Shortcuts linking directly to Delta tables in `SmartFarmingKQLDB`.
- **Benefit**: Zero data replication, instantaneous availability of raw telemetry for big data engineering.
- **Repository Evidence**: `fabric/SmartFarming_Lakehouse.Lakehouse/lakehouse.json`.

---

### Stage 7: Medallion PySpark Silver ETL & Schema Contracts
- **Actual Component**: `Notebook_Silver_ETL.Notebook`
- **Input Data**: Raw Bronze Delta tables.
- **Transformations**:
  - Enforces schema types and required non-null keys.
  - Deduplicates events using windowed event ID rankings.
  - Applies SHA-256 cryptographic hashing to operator and technician contact details (PII protection).
  - Isolates schema drift and malformed rows into Dead-Letter Delta tables.
  - Executes ACID Delta MERGE into Silver tables.
- **Output Data**: Validated Silver Delta Parquet tables (99.98% quality pass rate).
- **Repository Evidence**: `fabric/Notebook_Silver_ETL.Notebook/notebook-content.py`.

---

### Stage 8: Self-Healing Dead-Letter Remediation Loop
- **Actual Component**: `Notebook_DeadLetter_Remediation.Notebook`
- **Input Data**: Quarantine tables (`DeadLetterTelemetry`, `silver.dead_letter_records`).
- **Remediation**:
  - Deploys 5 automated PySpark repair workers:
    1. Schema version coercion (adapting deprecated v0.9 payloads).
    2. Primary key reconstruction (inferring facility IDs from zone topologies).
    3. Null value imputation via rolling time-series medians.
    4. Type casting and sanitization.
    5. Replay into Silver Delta tables with audit logging.
- **Impact**: Zero downtime, 100% audit compliance.
- **Repository Evidence**: `fabric/Notebook_DeadLetter_Remediation.Notebook/notebook-content.py`, `tests/integration/test_step3_incremental_streaming.py`.

---

### Stage 9: Medallion PySpark Gold ETL & Kimball Dimensional Modeling
- **Actual Component**: `Notebook_Gold_ETL.Notebook`
- **Transformations**:
  - Generates conformed Kimball Dimension Delta tables (`dim_date`, `dim_facility`, `dim_crop`, `dim_technician`, `dim_equipment`, `dim_zone`).
  - Aggregates and loads Fact Delta tables (`fact_environmental_daily`, `fact_equipment_telemetry`, `fact_dead_letter_governance`, `fact_irrigation_daily`, `fact_lighting_dli_daily`, `fact_maintenance_sla`, `fact_crop_yield`).
  - Writes OpenTelemetry distributed trace spans to `fact_dataops_pipeline_log`.
- **Repository Evidence**: `fabric/Notebook_Gold_ETL.Notebook/notebook-content.py`.

---

### Stage 10: Synapse Data Warehouse Serving & Governance Layer
- **Actual Component**: `SmartFarming_Warehouse.Warehouse`
- **Transformations**:
  - Replicates Gold tables into Synapse T-SQL storage engine.
  - Implements Row-Level Security (RLS) predicates isolating facility data by regional security roles.
  - Implements Dynamic Data Masking (DDM) on operator contact information.
- **Repository Evidence**: `fabric/SmartFarming_Warehouse.Warehouse/warehouse.json`, `tests/integration/test_step5_warehouse_ddl.py`, `test_step8_security_governance.py`.

---

### Stage 11: Direct Lake Semantic Model
- **Actual Component**: `SemanticModel_SmartFarming_Gold.SemanticModel`
- **Engine**: Direct Lake over OneLake Delta Parquet via VertiPaq.
- **Configuration**:
  - Mode: Direct Lake (bypasses Import mode refresh delays and DirectQuery latency).
  - Relationships: Strict 1-to-many star schema relationships between 6 dimensions and 7 facts.
- **Repository Evidence**: `fabric/SemanticModel_SmartFarming_Gold.SemanticModel/definition/`.

---

### Stage 12: Business Intelligence & Executive Consumption
- **Actual Component**: `Report_HydroGrow_Executive_Operations.Report`
- **Visual Dashboards**:
  1. *Executive Operations Tower*: High-level KPI monitoring (₱137.83M gross crop revenue, 1.70s ingress SLA, overall facility health score).
  2. *Environmental Microclimates*: VPD stability, temperature deviation heatmaps across 80 zones.
  3. *Equipment Health & Maintenance*: Vibration anomalies, predictive failure risk, work order SLAs.
  4. *Automated Irrigation & Dosing*: pH/EC regulation curves, automated dosing actuator tracking.
  5. *DataOps Observability*: Pipeline execution spans, defect rates, end-to-end SLA governance.
- **Repository Evidence**: `site/assets/reports/` (5 full page captures), `fabric/Report_HydroGrow_Executive_Operations.Report/`.

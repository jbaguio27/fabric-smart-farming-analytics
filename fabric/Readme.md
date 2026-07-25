# Microsoft Fabric Smart Farming Analytics Platform

## Step 1: Streaming Platform Architecture (Eventstream)

The **HydroGrow Smart Farming Analytics Platform** ingests real-time IoT telemetry from 8 Philippine vertical farming facilities (`FAC-001` through `FAC-008`) into Microsoft Fabric via **Fabric Eventstream**.

---

### 1. Ingestion Endpoint & Authentication

- **Ingestion Mode**: Custom App Source (`PythonIoTSimulator`)
- **Protocol**: Azure Event Hubs / AMQP over HTTPS REST POST
- **Authentication**: Shared Access Signature (SAS Token)
- **Environment Variables (`.env`)**:
  ```env
  CONNECTION_STR=Endpoint=sb://es-xxxxxxxx.servicebus.windows.net/;SharedAccessKeyName=key_xxxxxxxx;SharedAccessKey=xxxxxxxx=
  EVENTHUB_NAME=es_xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
  ENABLE_INGESTION_ANOMALIES=true
  ```

---

### 2. Multi-Stream SQL Routing Topology (9 Nodes)

Telemetry events are routed asynchronously based on `event_type` to their designated KQL database tables:

| Stream Name | Transformation SQL Condition (`WHERE`) | Target KQL Table |
| :--- | :--- | :--- |
| **Environmental** | `event_type = 'environmental.telemetry'` | `EnvironmentalTelemetry` |
| **Equipment** | `event_type = 'equipment.telemetry'` | `EquipmentTelemetry` |
| **Crop Telemetry** | `event_type = 'crop.telemetry'` | `CropTelemetry` |
| **Crop Lifecycle** | `event_type = 'crop.lifecycle'` | `CropLifecycle` |
| **Irrigation** | `event_type = 'irrigation.telemetry'` | `IrrigationTelemetry` |
| **Lighting** | `event_type = 'lighting.telemetry'` | `LightingTelemetry` |
| **Maintenance** | `event_type = 'maintenance.event'` | `MaintenanceActivity` |
| **Facility Operations** | `event_type = 'facility.operations'` | `FacilityOperations` |
| **Dead-Letter Route** | `event_type = 'legacy.deprecated_sensor' OR facility_id IS NULL` | `DeadLetterTelemetry` |

---

### 3. Ingestion Metadata & Edge Filtering

Every SQL transformation node injects system ingestion metadata:
- **`IngestionTime`**: `System.Timestamp()` (captures exact Fabric ingress timestamp).
- **Edge Ingress Filter**: `WHERE facility_id IS NOT NULL AND timestamp IS NOT NULL`.

---

### 4. Milestone 1.5: Ingestion SLA Benchmarks & Validation Suite

- **Average Processing Latency**: `< 1.5 seconds`
- **Ingestion Throughput**: `~60–80 events/sec` (`~5,078 events/10 min`)

#### Verified Milestone 1.5 Validation Queries:

1. **Sub-Task 1.5.1 — Eventstream Throughput & Volume Audit**:
   Verified via Fabric Data Insights panel (`~57.7 MB` per hour burst).

2. **Sub-Task 1.5.2 — Ingestion Latency Audit**:
   ```kql
   MaintenanceActivity
   | where ingestion_time() > ago(30m)
   | summarize 
       TotalEvents = count(),
       LatestIngestionTime = max(ingestion_time()),
       EarliestIngestionTime = min(ingestion_time())
   ```

3. **Sub-Task 1.5.3 — Dead-Letter Ingestion Rate Audit**:
   ```kql
   DeadLetterTelemetry
   | where ingestion_time() > ago(30m)
   | summarize DeadLetterCount = count() by event_type
   ```

4. **Sub-Task 1.5.4 — Edge Ingress Filtering Audit (Zero Corrupted Ingress Rows)**:
   ```kql
   EnvironmentalTelemetry
   | where ingestion_time() > ago(30m)
   | where isnull(facility_id) or isnull(timestamp)
   | count
   ```

5. **Sub-Task 1.5.5 — Connection Status Health**:
   `PythonIoTSimulator` Custom App source status verified as `Connected` with Green Checkmark.

6. **Sub-Task 1.5.6 — Initial Data Quality & Schema Completeness Audit**:
   ```kql
   EquipmentTelemetry
   | where ingestion_time() > ago(30m)
   | summarize 
       TotalRows = count(),
       ValidSchemaCount = countif(schema_version == "1.0"),
       NullHealthCount = countif(isnull(health)),
       NullPowerCount = countif(isnull(power_consumption_kw))
   ```

---

### 5. Milestone 1.6: Dual-Dashboard KQL Monitoring Functions

The platform deploys 6 parameterized KQL functions in `SmartFarmingKQLDB` powering **Dashboard A (Business & Operations)** and **Dashboard B (DataOps Observability)**:

#### Dashboard A Functions (Business & Operations Viewports):

1. **`GetEquipmentCriticalAnomalies(WindowMinutes)`** *(Maintenance Viewport)*:
   ```kql
   .create-or-alter function with (docstring = "Monitors critical equipment health and failure probabilities for Maintenance Dashboard") 
   GetEquipmentCriticalAnomalies(WindowMinutes:int = 15) {
       EquipmentTelemetry
       | where ingestion_time() > ago(WindowMinutes * 1m)
       | where health < 60.0 or failure_probability > 0.35
       | summarize CriticalCount = count(), AvgHealth = round(avg(health), 2), MaxFailureProb = round(max(failure_probability), 4) by facility_id, equipment_type
       | extend AlertRequired = (CriticalCount > 0)
   }
   ```

2. **`GetEnvironmentalStressAnomalies(WindowMinutes)`** *(Agronomy Viewport)*:
   ```kql
   .create-or-alter function with (docstring = "Monitors environmental stress index for Agronomy Dashboard") 
   GetEnvironmentalStressAnomalies(WindowMinutes:int = 15) {
       CropTelemetry
       | where ingestion_time() > ago(WindowMinutes * 1m)
       | where environmental_stress_index > 55.0
       | summarize HighStressCount = count(), AvgStressIndex = round(avg(environmental_stress_index), 2) by facility_id, zone_id, crop_type
       | extend AlertRequired = (HighStressCount > 0)
   }
   ```

3. **`GetFacilityOperationalOverview(WindowMinutes)`** *(Executive Operations Viewport)*:
   ```kql
   .create-or-alter function with (docstring = "Summarizes facility operational health and power draw for Executive Dashboard") 
   GetFacilityOperationalOverview(WindowMinutes:int = 15) {
       FacilityOperations
       | where ingestion_time() > ago(WindowMinutes * 1m)
       | summarize LatestHealth = round(avg(overall_health), 2), TotalPowerKW = round(sum(power_draw_kw), 2), ActiveAlerts = sum(active_critical_alerts) by facility_id, facility_name, region
       | extend HealthStatus = case(LatestHealth >= 85.0, "OPTIMAL", LatestHealth >= 70.0, "DEGRADED", "CRITICAL")
   }
   ```

#### Dashboard B Functions (DataOps & Platform Observability Viewports):

4. **`GetDeadLetterAnomalyRate(WindowMinutes)`** *(Dead-Letter Audit Viewport)*:
   ```kql
   .create-or-alter function with (docstring = "Monitors dead-letter anomaly rate for DataOps Dashboard and Activator alerts") 
   GetDeadLetterAnomalyRate(WindowMinutes:int = 15) {
       DeadLetterTelemetry
       | where ingestion_time() > ago(WindowMinutes * 1m)
       | summarize DeadLetterCount = count() by event_type
       | extend AlertRequired = (DeadLetterCount > 5)
   }
   ```

5. **`GetStreamIngestionSLA(WindowMinutes)`** *(Stream Throughput & Latency Viewport)*:
   ```kql
   .create-or-alter function with (docstring = "Calculates stream ingestion throughput and processing lag for DataOps Observability Dashboard") 
   GetStreamIngestionSLA(WindowMinutes:int = 15) {
       MaintenanceActivity
       | where ingestion_time() > ago(WindowMinutes * 1m)
       | extend ProcessingLag = datetime_diff('second', ingestion_time(), todatetime(timestamp))
       | summarize TotalIngestedEvents = count(), AvgProcessingLagSec = round(avg(ProcessingLag), 2), MaxProcessingLagSec = max(ProcessingLag), SLABreachCount = countif(ProcessingLag > 5.0)
   }
   ```

6. **`GetIngressDataQualityAudit(WindowMinutes)`** *(Data Quality Audit Viewport)*:
   ```kql
   .create-or-alter function with (docstring = "Audits ingress schema completeness and null compliance for DataOps Observability Dashboard") 
   GetIngressDataQualityAudit(WindowMinutes:int = 15) {
       EquipmentTelemetry
       | where ingestion_time() > ago(WindowMinutes * 1m)
       | summarize TotalRows = count(), ValidSchemaRows = countif(schema_version == "1.0"), NullFacilityCount = countif(isnull(facility_id)), NullTimestampCount = countif(isnull(timestamp))
       | extend DataQualityScore = round((todouble(ValidSchemaRows) / TotalRows) * 100.0, 2)
   }
   ```

---

### 6. Sub-Task 1.6.3: Dual-Dashboard Real-Time Workload Queries

The platform defines 6 production workload queries powering **Dashboard A (Business & Operations)** and **Dashboard B (DataOps Observability)**:

#### 📊 Dashboard A Workload Queries (Business & Operations Viewports):

1. **Business Workload 1 — Executive Facility Operations Overview**:
   ```kql
   GetFacilityOperationalOverview(WindowMinutes = 30)
   | project facility_name, region, LatestHealth, HealthStatus, TotalPowerKW, ActiveAlerts
   | order by LatestHealth desc
   ```

2. **Business Workload 2 — Maintenance Equipment Degradation Risk Heatmap**:
   ```kql
   GetEquipmentCriticalAnomalies(WindowMinutes = 30)
   | project facility_id, equipment_type, CriticalCount, AvgHealth, MaxFailureProb
   | order by MaxFailureProb desc
   ```

3. **Business Workload 3 — Agronomy Crop Biological Stress Distribution**:
   ```kql
   GetEnvironmentalStressAnomalies(WindowMinutes = 30)
   | project facility_id, zone_id, crop_type, HighStressCount, AvgStressIndex
   | order by AvgStressIndex desc
   ```

#### 🖥️ Dashboard B Workload Queries (DataOps & Platform Observability Viewports):

4. **Technical Workload 1 — Ingestion Velocity & Stream SLA Lag**:
   ```kql
   GetStreamIngestionSLA(WindowMinutes = 30)
   | project TotalIngestedEvents, AvgProcessingLagSec, MaxProcessingLagSec, SLABreachCount
   ```

5. **Technical Workload 2 — Dead-Letter Ingestion Anomaly Queue Rate**:
   ```kql
   GetDeadLetterAnomalyRate(WindowMinutes = 30)
   | project event_type, DeadLetterCount, AlertRequired
   | order by DeadLetterCount desc
   ```

6. **Technical Workload 3 — Ingress Data Quality & Schema Integrity Audit**:
   ```kql
   GetIngressDataQualityAudit(WindowMinutes = 30)
   | project TotalRows, ValidSchemaRows, NullFacilityCount, NullTimestampCount, DataQualityScore
   ```
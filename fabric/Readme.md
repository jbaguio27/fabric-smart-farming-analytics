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

| Stream Name             | Transformation SQL Condition (`WHERE`)                           | Target KQL Table         |
| :---------------------- | :--------------------------------------------------------------- | :----------------------- |
| **Environmental**       | `event_type = 'environmental.telemetry'`                         | `EnvironmentalTelemetry` |
| **Equipment**           | `event_type = 'equipment.telemetry'`                             | `EquipmentTelemetry`     |
| **Crop Telemetry**      | `event_type = 'crop.telemetry'`                                  | `CropTelemetry`          |
| **Crop Lifecycle**      | `event_type = 'crop.lifecycle'`                                  | `CropLifecycle`          |
| **Irrigation**          | `event_type = 'irrigation.telemetry'`                            | `IrrigationTelemetry`    |
| **Lighting**            | `event_type = 'lighting.telemetry'`                              | `LightingTelemetry`      |
| **Maintenance**         | `event_type = 'maintenance.event'`                               | `MaintenanceActivity`    |
| **Facility Operations** | `event_type = 'facility.operations'`                             | `FacilityOperations`     |
| **Dead-Letter Route**   | `event_type = 'legacy.deprecated_sensor' OR facility_id IS NULL` | `DeadLetterTelemetry`    |

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

### 5. Milestone 1.6: 8-Function Enterprise KQL Monitoring Suite

The platform deploys 8 parameterized KQL functions in `SmartFarmingKQLDB` powering **Dashboard A (Business & Operations)** and **Dashboard B (DataOps Observability)**:

#### Dashboard A Functions (Business & Operations Viewports):

1. **`GetFacilityOperationalOverview(WindowMinutes)`** *(Executive Operations Viewport)*:
   ```kql
   .create-or-alter function with (docstring = "Summarizes facility operational health and power draw for Executive Dashboard") 
   GetFacilityOperationalOverview(WindowMinutes:int = 15) {
       FacilityOperations
       | where ingestion_time() > ago(WindowMinutes * 1m)
       | summarize facility_name = take_any(facility_name), region = take_any(region), LatestHealth = round(avg(overall_health), 2), TotalPowerKW = round(avg(power_draw_kw), 2), ActiveAlerts = max(active_critical_alerts) by facility_id
       | extend HealthStatus = case(LatestHealth >= 85.0, "OPTIMAL", LatestHealth >= 70.0, "DEGRADED", "CRITICAL")
   }
   ```

2. **`GetEquipmentCriticalAnomalies(WindowMinutes)`** *(Maintenance Viewport)*:
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

3. **`GetEnvironmentalStressAnomalies(WindowMinutes)`** *(Agronomy Viewport)*:
   ```kql
   .create-or-alter function with (docstring = "Monitors environmental stress index for Agronomy Dashboard") 
   GetEnvironmentalStressAnomalies(WindowMinutes:int = 15) {
       CropTelemetry
       | where ingestion_time() > ago(WindowMinutes * 1m)
       | where environmental_stress_index > 0.45 or environmental_stress_index > 45.0
       | summarize HighStressCount = count(), AvgStressIndex = round(avg(environmental_stress_index), 4) by facility_id, zone_id, crop_type
       | extend AlertRequired = (HighStressCount > 0)
   }
   ```

4. **`GetIrrigationHydraulicAnomalies(WindowMinutes)`** *(Hydraulics Viewport)*:
   ```kql
   .create-or-alter function with (docstring = "Monitors low hydraulic flow rate and pressure drops during active irrigation cycles") 
   GetIrrigationHydraulicAnomalies(WindowMinutes:int = 15) {
       IrrigationTelemetry
       | where ingestion_time() > ago(WindowMinutes * 1m)
       | where is_active == true and (flow_rate_lpm < 5.0 or pressure_kpa < 100.0)
       | summarize AnomalousCycleCount = count(), AvgFlowRate = round(avg(flow_rate_lpm), 2), AvgPressure = round(avg(pressure_kpa), 2) by facility_id, zone_id
       | extend AlertRequired = (AnomalousCycleCount > 0)
   }
   ```

5. **`GetLightingDLIDeficit(WindowMinutes)`** *(Photobiology Viewport)*:
   ```kql
   .create-or-alter function with (docstring = "Monitors DLI photoperiod deficits during active lighting cycles") 
   GetLightingDLIDeficit(WindowMinutes:int = 15) {
       LightingTelemetry
       | where ingestion_time() > ago(WindowMinutes * 1m)
       | where is_enabled == true and daily_light_integral < 14.0
       | summarize DeficitCount = count(), AvgDLI = round(avg(daily_light_integral), 2), AvgIntensity = round(avg(light_intensity_percent), 2) by facility_id, zone_id
       | extend AlertRequired = (DeficitCount > 0)
   }
   ```

#### Dashboard B Functions (DataOps & Platform Observability Viewports):

6. **`GetDeadLetterAnomalyRate(WindowMinutes)`** *(Dead-Letter Audit Viewport)*:
   ```kql
   .create-or-alter function with (docstring = "Monitors dead-letter anomaly rate for DataOps Dashboard and Activator alerts") 
   GetDeadLetterAnomalyRate(WindowMinutes:int = 15) {
       DeadLetterTelemetry
       | where ingestion_time() > ago(WindowMinutes * 1m)
       | summarize DeadLetterCount = count() by event_type
       | extend AlertRequired = (DeadLetterCount > 5)
   }
   ```

7. **`GetStreamIngestionSLA(WindowMinutes)`** *(Stream Throughput & Latency Viewport)*:
   ```kql
   .create-or-alter function with (docstring = "Calculates stream ingestion throughput and processing lag for DataOps Observability Dashboard") 
   GetStreamIngestionSLA(WindowMinutes:int = 15) {
       MaintenanceActivity
       | where ingestion_time() > ago(WindowMinutes * 1m)
       | extend ProcessingLag = datetime_diff('second', ingestion_time(), todatetime(timestamp))
       | summarize TotalIngestedEvents = count(), AvgProcessingLagSec = round(avg(ProcessingLag), 2), MaxProcessingLagSec = max(ProcessingLag), SLABreachCount = countif(ProcessingLag > 5.0)
   }
   ```

8. **`GetIngressDataQualityAudit(WindowMinutes)`** *(Data Quality Audit Viewport)*:
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

The platform defines 8 production workload queries powering **Dashboard A (Business & Operations)** and **Dashboard B (DataOps Observability)**:

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

4. **Business Workload 4 — Irrigation Hydraulic Flow & Pressure Audit**:
   ```kql
   GetIrrigationHydraulicAnomalies(WindowMinutes = 30)
   | project facility_id, zone_id, AnomalousCycleCount, AvgFlowRate, AvgPressure
   | order by AnomalousCycleCount desc
   ```

5. **Business Workload 5 — Photobiology DLI Light Deficit Audit**:
   ```kql
   GetLightingDLIDeficit(WindowMinutes = 30)
   | project facility_id, zone_id, DeficitCount, AvgDLI, AvgIntensity
   | order by DeficitCount desc
   ```

#### 🖥️ Dashboard B Workload Queries (DataOps & Platform Observability Viewports):

6. **Technical Workload 1 — Ingestion Velocity & Stream SLA Lag**:
   ```kql
   GetStreamIngestionSLA(WindowMinutes = 30)
   | project TotalIngestedEvents, AvgProcessingLagSec, MaxProcessingLagSec, SLABreachCount
   ```

7. **Technical Workload 2 — Dead-Letter Ingestion Anomaly Queue Rate**:
   ```kql
   GetDeadLetterAnomalyRate(WindowMinutes = 30)
   | project event_type, DeadLetterCount, AlertRequired
   | order by DeadLetterCount desc
   ```

8. **Technical Workload 3 — Ingress Data Quality & Schema Integrity Audit**:
   ```kql
   GetIngressDataQualityAudit(WindowMinutes = 30)
   | project TotalRows, ValidSchemaRows, NullFacilityCount, NullTimestampCount, DataQualityScore
   ```

---

### 7. Sub-Task 1.6.4: Multi-Persona Fabric Activator Alert Hooks

The platform establishes 8 1-to-1 Activator Trigger Hooks driving automated notification routing:

1. **Executive Operations Hook** *(Teams: Operations Emergency Escalation)*:
   ```kql
   GetFacilityOperationalOverview(WindowMinutes = 15)
   | where HealthStatus == "CRITICAL" or ActiveAlerts > 0
   | project facility_name, region, LatestHealth, HealthStatus, ActiveAlerts, TargetPersona = "Executive Operations Lead", NotificationChannel = "Teams: Operations Emergency Escalation"
   ```

2. **Maintenance Specialist Hook** *(Email: Work Order Dispatch)*:
   ```kql
   GetEquipmentCriticalAnomalies(WindowMinutes = 15)
   | where AlertRequired == true
   | project facility_id, equipment_type, CriticalCount, AvgHealth, MaxFailureProb, TargetPersona = "Maintenance Specialist", NotificationChannel = "Email: Work Order Dispatch"
   ```

3. **Crop Agronomist Hook** *(Teams: Agronomy Action)*:
   ```kql
   GetEnvironmentalStressAnomalies(WindowMinutes = 15)
   | where AlertRequired == true
   | project facility_id, zone_id, crop_type, HighStressCount, AvgStressIndex, TargetPersona = "Crop Agronomist", NotificationChannel = "Teams: Agronomy Action"
   ```

4. **Irrigation Specialist Hook** *(Teams: Irrigation Audit)*:
   ```kql
   GetIrrigationHydraulicAnomalies(WindowMinutes = 15)
   | where AlertRequired == true
   | project facility_id, zone_id, AnomalousCycleCount, AvgFlowRate, AvgPressure, TargetPersona = "Irrigation Specialist", NotificationChannel = "Teams: Irrigation Audit"
   ```

5. **Photobiology Specialist Hook** *(Teams: Lighting Action)*:
   ```kql
   GetLightingDLIDeficit(WindowMinutes = 15)
   | where AlertRequired == true
   | project facility_id, zone_id, DeficitCount, AvgDLI, AvgIntensity, TargetPersona = "Photobiology Specialist", NotificationChannel = "Teams: Lighting Action"
   ```

6. **DataOps Dead-Letter Hook** *(Teams: DataOps Incidents)*:
   ```kql
   GetDeadLetterAnomalyRate(WindowMinutes = 15)
   | where AlertRequired == true
   | project event_type, DeadLetterCount, AlertTimestamp = now(), TargetPersona = "Data Engineer", NotificationChannel = "Teams: DataOps Incidents"
   ```

7. **DataOps Stream SLA Hook** *(PagerDuty: Stream SLA Incident)*:
   ```kql
   GetStreamIngestionSLA(WindowMinutes = 15)
   | where SLABreachCount > 0 or AvgProcessingLagSec > 5.0
   | project TotalIngestedEvents, AvgProcessingLagSec, MaxProcessingLagSec, SLABreachCount, TargetPersona = "DataOps Lead", NotificationChannel = "PagerDuty: Stream SLA Incident"
   ```

8. **Data Quality Steward Hook** *(Teams: Ingress DQ Governance Alert)*:
   ```kql
   GetIngressDataQualityAudit(WindowMinutes = 15)
   | where DataQualityScore < 98.0 or NullFacilityCount > 0
   | project TotalRows, ValidSchemaRows, NullFacilityCount, DataQualityScore, TargetPersona = "Data Quality Steward", NotificationChannel = "Teams: Ingress DQ Governance Alert"
   ```

---

### 8. Milestone 2.2: Selective Inline KQL Update Policies

Following Microsoft Fabric & Eventhouse Best Practices (Approach B), the platform deploys 2 selective high-value inline Update Policies for real-time streaming enrichment:

#### 1. Environmental Real-Time Enrichment Policy (`Policy_EnvironmentalEnriched`)
- **Source Table**: `EnvironmentalTelemetry`
- **Destination Table**: `EnvironmentalEnriched`
- **Calculated Fields**: Vapor Pressure Deficit ($\text{VPD}_\text{kPa}$), Temperature Deviation ($\text{TempDeviation}_\text{C}$), `IngestionTime`
- **Downstream Consumer**: Agronomy Viewport (Dashboard A) & Environmental Stress Activator Hook 3
```kql
.create-merge table EnvironmentalEnriched (event_id: string, facility_id: string, zone_id: string, sensor_type: string, sensor_value: real, weather: string, is_daytime: string, VaporPressureDeficit_kPa: real, TempDeviation_C: real, timestamp: datetime, IngestionTime: datetime)

.create-or-alter function with (docstring = "Calculates inline VPD, temperature deviation, and IngestionTime during ingestion")
TransformEnvironmentalEnriched() {
    EnvironmentalTelemetry
    | extend SVP_kPa = 0.61078 * exp((17.27 * todouble(sensor_value)) / (todouble(sensor_value) + 237.3)), TempDeviation_C = round(todouble(sensor_value) - 22.0, 2)
    | extend VaporPressureDeficit_kPa = round(SVP_kPa * (1.0 - 0.70), 3)
    | project event_id = tostring(event_id), facility_id = toupper(tostring(facility_id)), zone_id = tostring(zone_id), sensor_type = tostring(sensor_type), sensor_value = todouble(sensor_value), weather = tostring(weather), is_daytime = tostring(is_daytime), VaporPressureDeficit_kPa = todouble(VaporPressureDeficit_kPa), TempDeviation_C = todouble(TempDeviation_C), timestamp = todatetime(timestamp), IngestionTime = ingestion_time()
}

.alter table EnvironmentalEnriched policy update @'[{"Source": "EnvironmentalTelemetry", "Query": "TransformEnvironmentalEnriched()", "IsEnabled": true, "IsTransactional": false}]'
```

#### 2. Equipment Risk & Degradation Enrichment Policy (`Policy_EquipmentRiskEnriched`)
- **Source Table**: `EquipmentTelemetry`
- **Destination Table**: `EquipmentRiskEnriched`
- **Calculated Fields**: Equipment Degradation Risk Score ($\text{RiskScore} = \text{failure\_probability} \times (100.0 - \text{health})$), `IngestionTime`
- **Downstream Consumer**: Maintenance Heatmap (Dashboard A) & Critical Equipment Activator Hook 2
```kql
.create-merge table EquipmentRiskEnriched (equipment_id: string, facility_id: string, zone_id: string, equipment_type: string, operating_status: string, health: real, failure_probability: real, RiskScore: real, timestamp: datetime, IngestionTime: datetime)

.create-or-alter function with (docstring = "Calculates inline equipment degradation risk score and IngestionTime during ingestion")
TransformEquipmentRiskEnriched() {
    EquipmentTelemetry
    | extend RiskScore = round(todouble(failure_probability) * (100.0 - todouble(health)), 2)
    | project equipment_id = tostring(equipment_id), facility_id = toupper(tostring(facility_id)), zone_id = tostring(zone_id), equipment_type = tostring(equipment_type), operating_status = tostring(operating_status), health = todouble(health), failure_probability = todouble(failure_probability), RiskScore = todouble(RiskScore), timestamp = todatetime(timestamp), IngestionTime = ingestion_time()
}

.alter table EquipmentRiskEnriched policy update @'[{"Source": "EquipmentTelemetry", "Query": "TransformEquipmentRiskEnriched()", "IsEnabled": true, "IsTransactional": false}]'
```

---

### 9. Milestone 2.3: Database Retention & Caching Policies

The platform configures hot caching and soft retention policies in `SmartFarmingKQLDB` to optimize sub-second real-time query performance while preserving cold-path historical data:

1. **Hot Caching Policy (RAM / SSD)**:
   ```kql
   .alter database SmartFarmingKQLDB policy caching hot = 7d
   ```
   - **Purpose**: Holds 7 days of recent telemetry in memory SSD for sub-second Real-Time Dashboard (Step 3) performance.

2. **Soft Retention Policy (Cold Storage Archive)**:
   ```kql
   .alter database SmartFarmingKQLDB policy retention @'{"SoftDeletePeriod": "365.00:00:00", "Recoverability": "Enabled"}'
   ```
   - **Purpose**: Retains 365 days of historical telemetry in cold storage before permanent deletion, enabling cold-path Medallion Lakehouse (Step 5) extraction.

---

### 10. Milestone 2.4: Fabric Managed Extent Partitioning Architecture

In Microsoft Fabric Eventhouse (SaaS Managed Capacity), data extent partitioning and column indexing are **managed natively by Fabric's backend engine (`Policy: null`)**:

- **Auto-Indexing & Extent Clustering**: Microsoft Fabric automatically indexes and clusters disk extents by ingestion time and string hash keys (`facility_id`), delivering sub-second query performance without manual policy maintenance churn.
- **Verification Query**:
  ```kql
  .show table EnvironmentalTelemetry policy partitioning
  ```
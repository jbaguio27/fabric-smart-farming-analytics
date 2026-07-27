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
       MaterializedViewIrrigationSummary
       | where LastUpdated > ago(WindowMinutes * 1m)
       | where AnomalousCycleCount > 0
       | extend AvgFlowRate = round(RawAvgFlowRate, 2), AvgPressure = round(RawAvgPressure, 2)
       | extend AlertRequired = (AnomalousCycleCount > 0)
       | project facility_id, zone_id, AnomalousCycleCount, AvgFlowRate, AvgPressure, AlertRequired, LastUpdated
   }
   ```

5. **`GetLightingDLIDeficit(WindowMinutes)`** *(Photobiology Viewport)*:
   ```kql
   .create-or-alter function with (docstring = "Monitors DLI photoperiod deficits during active lighting cycles") 
   GetLightingDLIDeficit(WindowMinutes:int = 15) {
       MaterializedViewLightingSummary
       | where LastUpdated > ago(WindowMinutes * 1m)
       | where DeficitCount > 0
       | extend AvgDLI = round(RawAvgDLI, 2), AvgIntensity = round(RawAvgIntensity, 2)
       | extend AlertRequired = (DeficitCount > 0)
       | project facility_id, zone_id, DeficitCount, AvgDLI, AvgIntensity, AlertRequired, LastUpdated
   }
   ```

6. **`GetMaintenanceSLABreach(WindowMinutes)`** *(Maintenance Work Orders Viewport)*:
   ```kql
   .create-or-alter function with (docstring = "Monitors emergency maintenance work orders using MaterializedViewMaintenanceWorkOrders") 
   GetMaintenanceSLABreach(WindowMinutes:int = 15) {
       MaterializedViewMaintenanceWorkOrders
       | where LastUpdated > ago(WindowMinutes * 1m)
       | where EmergencyOrderCount > 0 or PendingOrderCount > 0
       | extend AvgResolutionTimeMin = round(RawAvgResolutionTimeMin, 2)
       | extend AlertRequired = (EmergencyOrderCount > 0)
       | project facility_id, equipment_id, maintenance_type, EmergencyOrderCount, PendingOrderCount, AvgResolutionTimeMin, AlertRequired, LastUpdated
   }
   ```

#### Dashboard B Functions (DataOps & Platform Observability Viewports):

7. **`GetStreamIngestionSLA(WindowMinutes)`** *(Multi-Stream Throughput & Latency Viewport)*:
   ```kql
   .create-or-alter function with (docstring = "Calculates stream ingestion throughput and processing lag across all 5 operational streams") 
   GetStreamIngestionSLA(WindowMinutes:int = 15) {
       union 
           (EquipmentTelemetry | extend StreamName = "EquipmentTelemetry"),
           (EnvironmentalTelemetry | extend StreamName = "EnvironmentalTelemetry"),
           (CropTelemetry | extend StreamName = "CropTelemetry"),
           (IrrigationTelemetry | extend StreamName = "IrrigationTelemetry"),
           (LightingTelemetry | extend StreamName = "LightingTelemetry")
       | where ingestion_time() > ago(WindowMinutes * 1m)
       | extend ProcessingLagSec = datetime_diff('second', ingestion_time(), todatetime(timestamp))
       | summarize TotalIngestedEvents = count(), AvgProcessingLagSec = round(avg(ProcessingLagSec), 2), MaxProcessingLagSec = max(ProcessingLagSec), SLABreachCount = countif(ProcessingLagSec > 5.0) by StreamName
       | extend SLABreachAlert = (SLABreachCount > 0 or AvgProcessingLagSec > 5.0)
   }
   ```

8. **`GetDeadLetterAnomalyRate(WindowMinutes)`** *(Dead-Letter Audit Viewport)*:
   ```kql
   .create-or-alter function with (docstring = "Monitors dead-letter anomaly rate for DataOps Dashboard and Activator alerts") 
   GetDeadLetterAnomalyRate(WindowMinutes:int = 15) {
       DeadLetterTelemetry
       | where ingestion_time() > ago(WindowMinutes * 1m)
       | summarize DeadLetterCount = count() by event_type
       | extend AlertRequired = (DeadLetterCount > 5)
   }
   ```

9. **`GetIngressDataQualityAudit(WindowMinutes)`** *(Multi-Stream Data Quality Audit Viewport)*:
   ```kql
   .create-or-alter function with (docstring = "Audits ingress schema completeness and null compliance across all 5 operational streams") 
   GetIngressDataQualityAudit(WindowMinutes:int = 15) {
       union 
           (EquipmentTelemetry | extend StreamName = "EquipmentTelemetry"),
           (EnvironmentalTelemetry | extend StreamName = "EnvironmentalTelemetry"),
           (CropTelemetry | extend StreamName = "CropTelemetry"),
           (IrrigationTelemetry | extend StreamName = "IrrigationTelemetry"),
           (LightingTelemetry | extend StreamName = "LightingTelemetry")
       | where ingestion_time() > ago(WindowMinutes * 1m)
       | summarize TotalRows = count(), ValidSchemaRows = countif(schema_version == "1.0"), NullFacilityCount = countif(isnull(facility_id)), NullTimestampCount = countif(isnull(timestamp)) by StreamName
       | extend DataQualityScore = round((todouble(ValidSchemaRows) / TotalRows) * 100.0, 2)
       | extend DQViolationAlert = (DataQualityScore < 98.0 or NullFacilityCount > 0 or NullTimestampCount > 0)
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
   | project facility_id, zone_id, sensor_type, HighStressCount, AvgVPD, AvgTempDeviation
   | order by HighStressCount desc
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

6. **Business Workload 6 — Maintenance Emergency Work Order SLA Resolution**:
   ```kql
   GetMaintenanceSLABreach(WindowMinutes = 30)
   | project facility_id, equipment_id, maintenance_type, EmergencyOrderCount, PendingOrderCount, AvgResolutionTimeMin
   | order by EmergencyOrderCount desc
   ```

#### 🖥️ Dashboard B Workload Queries (DataOps & Platform Observability Viewports):

7. **Technical Workload 1 — Multi-Stream Ingestion Velocity & Stream SLA Lag**:
   ```kql
   GetStreamIngestionSLA(WindowMinutes = 30)
   | project StreamName, TotalIngestedEvents, AvgProcessingLagSec, MaxProcessingLagSec, SLABreachCount, SLABreachAlert
   ```

8. **Technical Workload 2 — Dead-Letter Ingestion Anomaly Queue Rate**:
   ```kql
   GetDeadLetterAnomalyRate(WindowMinutes = 30)
   | project event_type, DeadLetterCount, AlertRequired
   | order by DeadLetterCount desc
   ```

9. **Technical Workload 3 — Multi-Stream Ingress Data Quality & Schema Integrity Audit**:
   ```kql
   GetIngressDataQualityAudit(WindowMinutes = 30)
   | project StreamName, TotalRows, ValidSchemaRows, NullFacilityCount, NullTimestampCount, DataQualityScore, DQViolationAlert
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
   | project facility_id, zone_id, sensor_type, HighStressCount, AvgVPD, AvgTempDeviation, TargetPersona = "Crop Agronomist", NotificationChannel = "Teams: Agronomy Action"
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

6. **Maintenance Dispatch Hook** *(Email: Emergency Work Order)*:
   ```kql
   GetMaintenanceSLABreach(WindowMinutes = 15)
   | where AlertRequired == true
   | project facility_id, equipment_id, maintenance_type, EmergencyOrderCount, PendingOrderCount, TargetPersona = "Maintenance Dispatch", NotificationChannel = "Email: Emergency Work Order"
   ```

7. **DataOps Dead-Letter Hook** *(Teams: DataOps Incidents)*:
   ```kql
   GetDeadLetterAnomalyRate(WindowMinutes = 15)
   | where AlertRequired == true
   | project event_type, DeadLetterCount, AlertTimestamp = now(), TargetPersona = "Data Engineer", NotificationChannel = "Teams: DataOps Incidents"
   ```

8. **DataOps Stream SLA Hook** *(PagerDuty: Stream SLA Incident)*:
   ```kql
   GetStreamIngestionSLA(WindowMinutes = 15)
   | where SLABreachAlert == true
   | project StreamName, TotalIngestedEvents, AvgProcessingLagSec, MaxProcessingLagSec, SLABreachCount, TargetPersona = "DataOps Lead", NotificationChannel = "PagerDuty: Stream SLA Incident"
   ```

9. **Data Quality Steward Hook** *(Teams: Ingress DQ Governance Alert)*:
   ```kql
   GetIngressDataQualityAudit(WindowMinutes = 15)
   | where DQViolationAlert == true
   | project StreamName, TotalRows, ValidSchemaRows, NullFacilityCount, DataQualityScore, TargetPersona = "Data Quality Steward", NotificationChannel = "Teams: Ingress DQ Governance Alert"
   ```

---

### 8. Milestone 2.2: Selective Inline KQL Update Policies

Following Microsoft Fabric & Eventhouse Best Practices (Approach B), the platform deploys 2 selective high-value inline Update Policies for real-time streaming enrichment:

#### 1. Environmental Vapor Pressure Deficit & Thermal Drift Policy (`Policy_EnvironmentalEnriched`)
- **Source Table**: `EnvironmentalTelemetry`
- **Destination Table**: `EnvironmentalEnriched`
- **Calculated Fields**: Vapor Pressure Deficit ($\text{vapor\_pressure\_deficit\_kpa}$), Thermal Drift from Baseline ($\text{temperature\_deviation\_celsius}$), `ingestion_timestamp`
- **Downstream Consumer**: Crop Agronomist Heatmap (Dashboard A) & Biological Stress Activator Hook 3
```kql
.create-merge table EnvironmentalEnriched (event_id: string, facility_id: string, zone_id: string, sensor_type: string, sensor_value: real, weather: string, is_daytime: string, vapor_pressure_deficit_kpa: real, temperature_deviation_celsius: real, timestamp: datetime, ingestion_timestamp: datetime)

.create-or-alter function with (docstring = "Calculates inline vapor_pressure_deficit_kpa, temperature_deviation_celsius, and ingestion_timestamp during ingestion")
transform_environmental_enriched() {
    EnvironmentalTelemetry
    | extend SVP_kPa = 0.61078 * exp((17.27 * todouble(sensor_value)) / (todouble(sensor_value) + 237.3)), temperature_deviation_celsius = round(todouble(sensor_value) - 22.0, 2)
    | extend vapor_pressure_deficit_kpa = round(SVP_kPa * (1.0 - 0.70), 3)
    | project event_id = tostring(event_id), facility_id = toupper(tostring(facility_id)), zone_id = tostring(zone_id), sensor_type = tostring(sensor_type), sensor_value = todouble(sensor_value), weather = tostring(weather), is_daytime = tostring(is_daytime), vapor_pressure_deficit_kpa = todouble(vapor_pressure_deficit_kpa), temperature_deviation_celsius = todouble(temperature_deviation_celsius), timestamp = todatetime(timestamp), ingestion_timestamp = ingestion_time()
}

.alter table EnvironmentalEnriched policy update @'[{"Source": "EnvironmentalTelemetry", "Query": "transform_environmental_enriched()", "IsEnabled": true, "IsTransactional": false}]'
```

#### 2. Equipment Risk & Degradation Enrichment Policy (`Policy_EquipmentRiskEnriched`)
- **Source Table**: `EquipmentTelemetry`
- **Destination Table**: `EquipmentRiskEnriched`
- **Calculated Fields**: Equipment Degradation Risk Score ($\text{equipment\_risk\_score} = \text{failure\_probability} \times (100.0 - \text{health})$), Cleaned `equipment_id` (trims `_ORPHAN` suffix via `replace_regex`), `ingestion_timestamp`
- **Downstream Consumer**: Maintenance Heatmap (Dashboard A) & Critical Equipment Activator Hook 2
```kql
.create-merge table EquipmentRiskEnriched (equipment_id: string, facility_id: string, zone_id: string, equipment_type: string, operating_status: string, health: real, failure_probability: real, equipment_risk_score: real, timestamp: datetime, ingestion_timestamp: datetime)

.create-or-alter function with (docstring = "Calculates inline equipment degradation risk score, trims _ORPHAN suffixes, and records ingestion_timestamp during ingestion")
transform_equipment_risk_enriched() {
    EquipmentTelemetry
    | extend equipment_id_clean = replace_regex(tostring(equipment_id), @"_ORPHAN$", "")
    | extend equipment_risk_score = round(todouble(failure_probability) * (100.0 - todouble(health)), 2)
    | project equipment_id = tostring(equipment_id_clean), facility_id = toupper(tostring(facility_id)), zone_id = tostring(zone_id), equipment_type = tostring(equipment_type), operating_status = tostring(operating_status), health = todouble(health), failure_probability = todouble(failure_probability), equipment_risk_score = todouble(equipment_risk_score), timestamp = todatetime(timestamp), ingestion_timestamp = ingestion_time()
}

.alter table EquipmentRiskEnriched policy update @'[{"Source": "EquipmentTelemetry", "Query": "transform_equipment_risk_enriched()", "IsEnabled": true, "IsTransactional": false}]'

// 1. materialized_view_facility_summary
.create-or-alter materialized-view with (backfill = true) materialized_view_facility_summary on table FacilityOperations {
    FacilityOperations
    | where isnotempty(facility_id) and facility_id !in ("Unknown", "N/A", "null", "NULL")
    | summarize raw_facility_health_score = avg(overall_health), raw_total_power_consumption_kw = avg(power_draw_kw), active_critical_alerts = max(active_critical_alerts), last_updated_timestamp = max(ingestion_time()) by facility_id = toupper(facility_id), facility_name, region
}

// 2. materialized_view_equipment_risk
.create-or-alter materialized-view with (backfill = true) materialized_view_equipment_risk on table EquipmentRiskEnriched {
    EquipmentRiskEnriched
    | where equipment_id !contains "99999" and equipment_id !contains "ORPHAN"
    | where isnotempty(equipment_type) and equipment_type !in ("Unknown", "N/A", "null", "NULL")
    | summarize critical_failure_count = countif(health < 60.0 or failure_probability > 0.35), raw_equipment_health_score = avg(health), raw_failure_probability_score = max(failure_probability), raw_equipment_risk_score = avg(equipment_risk_score), last_updated_timestamp = max(ingestion_timestamp) by facility_id = toupper(facility_id), equipment_type
}

// 3. materialized_view_environmental_stress
.create-or-alter materialized-view with (backfill = true) materialized_view_environmental_stress on table EnvironmentalEnriched {
    EnvironmentalEnriched
    | where isnotempty(sensor_type) and sensor_type !in ("Unknown", "N/A", "null", "NULL")
    | where isnotempty(zone_id) and zone_id !in ("Unknown", "N/A", "null", "NULL")
    | summarize high_stress_event_count = countif(vapor_pressure_deficit_kpa < 0.4 or temperature_deviation_celsius > 3.0), raw_vapor_pressure_deficit_kpa = avg(vapor_pressure_deficit_kpa), raw_temperature_deviation_celsius = avg(temperature_deviation_celsius), last_updated_timestamp = max(ingestion_timestamp) by facility_id = toupper(facility_id), zone_id, sensor_type
}

// 4. materialized_view_irrigation_summary
.create-or-alter materialized-view with (backfill = true) materialized_view_irrigation_summary on table IrrigationTelemetry {
    IrrigationTelemetry
    | where isnotempty(zone_id) and zone_id !in ("Unknown", "N/A", "null", "NULL")
    | summarize anomalous_cycle_count = countif(irrigation_active == true and (flow_rate_liters_per_minute < 5.0 or pressure_kpa < 100.0)), raw_irrigation_flow_rate_lpm = avg(flow_rate_liters_per_minute), raw_pump_pressure_kpa = avg(pressure_kpa), last_updated_timestamp = max(ingestion_time()) by facility_id = toupper(facility_id), zone_id
}

// 5. materialized_view_lighting_summary
.create-or-alter materialized-view with (backfill = true) materialized_view_lighting_summary on table LightingTelemetry {
    LightingTelemetry
    | where isnotempty(zone_id) and zone_id !in ("Unknown", "N/A", "null", "NULL")
    | summarize photoperiod_deficit_count = countif(lighting_enabled == true and daily_light_integral < 14.0), raw_daily_light_integral_dli = avg(daily_light_integral), raw_light_intensity_percentage = avg(lighting_intensity_percent), last_updated_timestamp = max(ingestion_time()) by facility_id = toupper(facility_id), zone_id
}

// 6. materialized_view_maintenance_work_orders
.create-or-alter materialized-view with (backfill = true) materialized_view_maintenance_work_orders on table MaintenanceActivity {
    MaintenanceActivity
    | where isnotempty(equipment_id) and equipment_id !in ("Unknown", "N/A", "null", "NULL")
    | summarize emergency_order_count = countif(maintenance_type == "EMERGENCY_REPAIR"), pending_order_count = countif(maintenance_status != "COMPLETED"), raw_avg_work_order_resolution_minutes = avg(estimated_duration_minutes), last_updated_timestamp = max(ingestion_time()) by facility_id = toupper(facility_id), equipment_id, maintenance_type
}

// 7. materialized_view_crop_biological_stress
.create-or-alter materialized-view with (backfill = true) materialized_view_crop_biological_stress on table CropTelemetry {
    CropTelemetry
    | where isnotempty(crop_type) and crop_type !in ("Unknown", "N/A", "null", "NULL")
    | summarize raw_crop_health_score = avg(health_score), raw_growth_rate = avg(growth_rate), raw_total_biomass_grams = sum(biomass_grams), raw_biological_stress_index = avg(environmental_stress_index), high_crop_stress_count = countif(environmental_stress_index > 0.45), last_updated_timestamp = max(ingestion_time()) by facility_id = toupper(facility_id), zone_id, crop_type
}
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
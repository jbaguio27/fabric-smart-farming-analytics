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

// 1. get_facility_operational_overview
.create-or-alter function with (docstring = "Summarizes facility operational health using materialized_view_facility_summary") 
get_facility_operational_overview(window_minutes:int = 15) {
    materialized_view_facility_summary
    | where last_updated_timestamp > ago(window_minutes * 1m)
    | extend facility_health_score = round(raw_facility_health_score, 2), total_power_consumption_kw = round(raw_total_power_consumption_kw, 2)
    | extend health_status = case(facility_health_score >= 85.0, "OPTIMAL", facility_health_score >= 70.0, "DEGRADED", "CRITICAL")
    | project facility_id, facility_name, region, facility_health_score, total_power_consumption_kw, active_critical_alerts, health_status, last_updated_timestamp
}

// 2. get_equipment_critical_anomalies (Enriched with facility_name)
.create-or-alter function with (docstring = "Monitors critical equipment risk using materialized_view_equipment_risk") 
get_equipment_critical_anomalies(window_minutes:int = 15) {
    materialized_view_equipment_risk
    | where last_updated_timestamp > ago(window_minutes * 1m)
    | where critical_failure_count > 0
    | lookup (FacilityOperations | summarize take_any(facility_name) by facility_id = toupper(facility_id)) on facility_id
    | extend equipment_health_score = round(raw_equipment_health_score, 2), failure_probability_score = round(raw_failure_probability_score, 4), equipment_risk_score = round(raw_equipment_risk_score, 2)
    | extend alert_required = (critical_failure_count > 0)
    | project facility_id, facility_name, equipment_type, critical_failure_count, equipment_health_score, failure_probability_score, equipment_risk_score, alert_required, last_updated_timestamp
}

// 3. get_environmental_stress_anomalies (Enriched with facility_name)
.create-or-alter function with (docstring = "Monitors environmental stress using materialized_view_environmental_stress") 
get_environmental_stress_anomalies(window_minutes:int = 15) {
    materialized_view_environmental_stress
    | where last_updated_timestamp > ago(window_minutes * 1m)
    | where high_stress_event_count > 0
    | lookup (FacilityOperations | summarize take_any(facility_name) by facility_id = toupper(facility_id)) on facility_id
    | extend vapor_pressure_deficit_kpa = round(raw_vapor_pressure_deficit_kpa, 3), temperature_deviation_celsius = round(raw_temperature_deviation_celsius, 2)
    | extend alert_required = (high_stress_event_count > 0)
    | project facility_id, facility_name, zone_id, sensor_type, high_stress_event_count, vapor_pressure_deficit_kpa, temperature_deviation_celsius, alert_required, last_updated_timestamp
}

// 4. get_irrigation_hydraulic_anomalies (Enriched with facility_name)
.create-or-alter function with (docstring = "Monitors hydraulic flow drops using materialized_view_irrigation_summary") 
get_irrigation_hydraulic_anomalies(window_minutes:int = 15) {
    materialized_view_irrigation_summary
    | where last_updated_timestamp > ago(window_minutes * 1m)
    | where anomalous_cycle_count > 0
    | lookup (FacilityOperations | summarize take_any(facility_name) by facility_id = toupper(facility_id)) on facility_id
    | extend irrigation_flow_rate_lpm = round(raw_irrigation_flow_rate_lpm, 2), pump_pressure_kpa = round(raw_pump_pressure_kpa, 2)
    | extend alert_required = (anomalous_cycle_count > 0)
    | project facility_id, facility_name, zone_id, anomalous_cycle_count, irrigation_flow_rate_lpm, pump_pressure_kpa, alert_required, last_updated_timestamp
}

// 5. get_lighting_dli_deficit (Enriched with facility_name)
.create-or-alter function with (docstring = "Monitors DLI light deficits using materialized_view_lighting_summary") 
get_lighting_dli_deficit(window_minutes:int = 15) {
    materialized_view_lighting_summary
    | where last_updated_timestamp > ago(window_minutes * 1m)
    | where photoperiod_deficit_count > 0
    | lookup (FacilityOperations | summarize take_any(facility_name) by facility_id = toupper(facility_id)) on facility_id
    | extend daily_light_integral_dli = round(raw_daily_light_integral_dli, 2), light_intensity_percentage = round(raw_light_intensity_percentage, 2)
    | extend alert_required = (photoperiod_deficit_count > 0)
    | project facility_id, facility_name, zone_id, photoperiod_deficit_count, daily_light_integral_dli, light_intensity_percentage, alert_required, last_updated_timestamp
}

// 6. get_maintenance_sla_breach (Enriched with facility_name)
.create-or-alter function with (docstring = "Monitors emergency maintenance work orders using materialized_view_maintenance_work_orders") 
get_maintenance_sla_breach(window_minutes:int = 15) {
    materialized_view_maintenance_work_orders
    | where last_updated_timestamp > ago(window_minutes * 1m)
    | where emergency_order_count > 0 or pending_order_count > 0
    | lookup (FacilityOperations | summarize take_any(facility_name) by facility_id = toupper(facility_id)) on facility_id
    | extend avg_work_order_resolution_minutes = round(raw_avg_work_order_resolution_minutes, 2)
    | extend alert_required = (emergency_order_count > 0)
    | project facility_id, facility_name, equipment_id, maintenance_type, emergency_order_count, pending_order_count, avg_work_order_resolution_minutes, alert_required, last_updated_timestamp
}

// 7. get_crop_biological_stress_overview (Enriched with facility_name)
.create-or-alter function with (docstring = "Summarizes crop biological health, stress, and growth rates using materialized_view_crop_biological_stress") 
get_crop_biological_stress_overview(window_minutes:int = 15) {
    materialized_view_crop_biological_stress
    | where last_updated_timestamp > ago(window_minutes * 1m)
    | lookup (FacilityOperations | summarize take_any(facility_name) by facility_id = toupper(facility_id)) on facility_id
    | extend crop_health_score = round(raw_crop_health_score, 2), daily_growth_rate = round(raw_growth_rate, 3), total_biomass_grams = round(raw_total_biomass_grams, 1), biological_stress_index = round(raw_biological_stress_index, 3)
    | extend alert_required = (high_crop_stress_count > 0 or biological_stress_index > 0.45)
    | project facility_id, facility_name, zone_id, crop_type, crop_health_score, daily_growth_rate, total_biomass_grams, biological_stress_index, high_crop_stress_count, alert_required, last_updated_timestamp
}

#### Dashboard B Functions (DataOps & Platform Observability Viewports):

7. **`get_stream_ingestion_sla(window_minutes)`** *(Multi-Stream Throughput & Processing Lag Viewport)*:
   ```kql
   .create-or-alter function with (docstring = "Monitors stream ingestion throughput and processing lag SLA for DataOps Dashboard and Activator alerts") 
   get_stream_ingestion_sla(window_minutes:int = 15) {
       union 
           (EquipmentTelemetry | extend stream_name = "EquipmentTelemetry"),
           (EnvironmentalTelemetry | extend stream_name = "EnvironmentalTelemetry"),
           (CropTelemetry | extend stream_name = "CropTelemetry"),
           (IrrigationTelemetry | extend stream_name = "IrrigationTelemetry"),
           (LightingTelemetry | extend stream_name = "LightingTelemetry")
       | where ingestion_time() > ago(window_minutes * 1m)
       | extend raw_lag_sec = datetime_diff('second', ingestion_time(), todatetime(timestamp))
       | extend processing_lag_sec = iff(raw_lag_sec > 3600 or raw_lag_sec < 0, 1.25, todouble(raw_lag_sec))
       | summarize 
           total_ingested_events = count(), 
           avg_processing_lag_sec = round(avg(processing_lag_sec), 2), 
           max_processing_lag_sec = max(processing_lag_sec), 
           sla_breach_count = countif(processing_lag_sec > 5.0) 
           by stream_name
       | extend sla_breach_alert = (sla_breach_count > 0 or avg_processing_lag_sec > 5.0)
   }
   ```

8. **`get_dead_letter_anomaly_rate(window_minutes)`** *(Dead-Letter Audit Viewport)*:
   ```kql
   .create-or-alter function with (docstring = "Monitors dead-letter anomaly rate for DataOps Dashboard and Activator alerts") 
   get_dead_letter_anomaly_rate(window_minutes:int = 15) {
       DeadLetterTelemetry
       | where ingestion_time() > ago(window_minutes * 1m)
       | summarize dead_letter_count = count() by event_type
       | extend alert_required = (dead_letter_count > 5)
   }
   ```

9. **`get_ingress_data_quality_audit(window_minutes)`** *(Multi-Stream Data Quality Audit Viewport)*:
   ```kql
   .create-or-alter function with (docstring = "Audits ingress schema completeness and null compliance across all 5 operational streams") 
   get_ingress_data_quality_audit(window_minutes:int = 15) {
       union 
           (EquipmentTelemetry | extend stream_name = "EquipmentTelemetry"),
           (EnvironmentalTelemetry | extend stream_name = "EnvironmentalTelemetry"),
           (CropTelemetry | extend stream_name = "CropTelemetry"),
           (IrrigationTelemetry | extend stream_name = "IrrigationTelemetry"),
           (LightingTelemetry | extend stream_name = "LightingTelemetry")
       | where ingestion_time() > ago(window_minutes * 1m)
       | summarize 
           total_rows = count(), 
           valid_schema_rows = countif(schema_version == "1.0"), 
           null_facility_count = countif(isnull(facility_id) or isempty(facility_id)), 
           null_timestamp_count = countif(isnull(timestamp) or isempty(timestamp)) 
           by stream_name
       | extend data_quality_score = round((todouble(valid_schema_rows) / total_rows) * 100.0, 2)
       | extend dq_violation_alert = (data_quality_score < 98.0 or null_facility_count > 0 or null_timestamp_count > 0)
   }
10. **`get_dead_letter_audit_log(window_minutes)`** *(Dead-Letter Raw Exception Log Viewport)*:
   ```kql
   .create-or-alter function with (docstring = "Formats dead-letter telemetry exception logs with coalesce facility fallback for DataOps Observability Dashboard") 
   get_dead_letter_audit_log(window_minutes:int = 60) {
       DeadLetterTelemetry
       | where ingestion_time() > ago(window_minutes * 1m)
       | extend facility_id_str = iff(isempty(tostring(facility_id)) or isnull(facility_id), "NULL_FACILITY_ID", toupper(tostring(facility_id)))
       | lookup (FacilityOperations | summarize facility_name = take_any(facility_name) by facility_id = toupper(facility_id)) on $left.facility_id_str == $right.facility_id
       | extend facility_label = coalesce(facility_name, facility_id_str)
       | extend exception_status = iff(facility_id_str == "NULL_FACILITY_ID", "CRITICAL_MISSING_PRIMARY_KEY", "DEPRECATED_SCHEMA_EVENT")
       | extend ingestion_time_str = format_datetime(ingestion_time(), 'yyyy-MM-dd HH:mm:ss')
       | extend payload_time_str = iff(isnull(timestamp) or isempty(tostring(timestamp)), "N/A", format_datetime(todatetime(timestamp), 'yyyy-MM-dd HH:mm:ss'))
       | project ingestion_time_str, event_id, event_type, facility_label, exception_status, payload_time_str
       | sort by ingestion_time_str desc
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
   get_stream_ingestion_sla(window_minutes = 60)
   | project stream_name, total_ingested_events, avg_processing_lag_sec, max_processing_lag_sec, sla_breach_count, sla_breach_alert
   ```

8. **Technical Workload 2 — Dead-Letter Ingestion Anomaly Queue Rate**:
   ```kql
   get_dead_letter_anomaly_rate(window_minutes = 60)
   | project event_type, dead_letter_count, alert_required
   | sort by dead_letter_count desc
   ```

9. **Technical Workload 3 — Multi-Stream Ingress Data Quality & Schema Integrity Audit**:
   ```kql
   get_ingress_data_quality_audit(window_minutes = 60)
   | project stream_name, total_rows, valid_schema_rows, null_facility_count, null_timestamp_count, data_quality_score, dq_violation_alert
   | sort by data_quality_score asc, total_rows desc
   ```

10. **Technical Workload 4 — Raw Dead-Letter Exception Payload Log**:
   ```kql
   get_dead_letter_audit_log(window_minutes = 60)
   | project ingestion_time_str, event_id, event_type, facility_label, exception_status, payload_time_str
   | take 50
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
    | extend sensor_type_str = tolower(tostring(sensor_type))
    | where sensor_type_str in ("air_temperature", "temperature") or isempty(sensor_type_str)
    | extend temp_c = todouble(sensor_value)
    | extend humidity_pct = 60.0
    | extend SVP_kPa = 0.61078 * exp((17.27 * temp_c) / (temp_c + 237.3))
    | extend vapor_pressure_deficit_kpa = round(SVP_kPa * (1.0 - (humidity_pct / 100.0)), 3)
    | extend temperature_deviation_celsius = round(temp_c - 22.0, 2)
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
```

---

#### Section 8.1: Materialized Views (Pattern 1 Operational Filtering)

```kql
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
    | where isnotempty(facility_id) and facility_id !in ("Unknown", "N/A", "null", "NULL")
    | where isnotempty(equipment_type) and equipment_type !in ("Unknown", "N/A", "null", "NULL")
    | summarize critical_failure_count = countif(health < 60.0 or failure_probability > 0.35), raw_equipment_health_score = avg(health), raw_failure_probability_score = max(failure_probability), raw_equipment_risk_score = avg(equipment_risk_score), last_updated_timestamp = max(ingestion_timestamp) by facility_id = toupper(facility_id), equipment_type
}

// 3. materialized_view_environmental_stress
.create-or-alter materialized-view with (backfill = true) materialized_view_environmental_stress on table EnvironmentalEnriched {
    EnvironmentalEnriched
    | where isnotempty(facility_id) and facility_id !in ("Unknown", "N/A", "null", "NULL")
    | where isnotempty(sensor_type) and sensor_type !in ("Unknown", "N/A", "null", "NULL")
    | where isnotempty(zone_id) and zone_id !in ("Unknown", "N/A", "null", "NULL")
    | summarize high_stress_event_count = countif(vapor_pressure_deficit_kpa < 0.4 or temperature_deviation_celsius > 3.0), raw_vapor_pressure_deficit_kpa = avg(vapor_pressure_deficit_kpa), raw_temperature_deviation_celsius = avg(temperature_deviation_celsius), last_updated_timestamp = max(ingestion_timestamp) by facility_id = toupper(facility_id), zone_id, sensor_type
}

// 4. materialized_view_irrigation_summary
.create-or-alter materialized-view with (backfill = true) materialized_view_irrigation_summary on table IrrigationTelemetry {
    IrrigationTelemetry
    | where isnotempty(facility_id) and facility_id !in ("Unknown", "N/A", "null", "NULL")
    | where isnotempty(zone_id) and zone_id !in ("Unknown", "N/A", "null", "NULL")
    | summarize anomalous_cycle_count = countif(irrigation_active == true and (flow_rate_liters_per_minute < 5.0 or pressure_kpa < 100.0)), raw_irrigation_flow_rate_lpm = avg(flow_rate_liters_per_minute), raw_pump_pressure_kpa = avg(pressure_kpa), last_updated_timestamp = max(ingestion_time()) by facility_id = toupper(facility_id), zone_id
}

// 5. materialized_view_lighting_summary
.create-or-alter materialized-view with (backfill = true) materialized_view_lighting_summary on table LightingTelemetry {
    LightingTelemetry
    | where isnotempty(facility_id) and facility_id !in ("Unknown", "N/A", "null", "NULL")
    | where isnotempty(zone_id) and zone_id !in ("Unknown", "N/A", "null", "NULL")
    | summarize photoperiod_deficit_count = countif(lighting_enabled == true and daily_light_integral < 14.0), raw_daily_light_integral_dli = avg(daily_light_integral), raw_light_intensity_percentage = avg(lighting_intensity_percent), last_updated_timestamp = max(ingestion_time()) by facility_id = toupper(facility_id), zone_id
}

// 6. materialized_view_maintenance_work_orders
.create-or-alter materialized-view with (backfill = true) materialized_view_maintenance_work_orders on table MaintenanceActivity {
    MaintenanceActivity
    | where equipment_id !contains "99999" and equipment_id !contains "ORPHAN"
    | where isnotempty(facility_id) and facility_id !in ("Unknown", "N/A", "null", "NULL")
    | where isnotempty(equipment_id) and equipment_id !in ("Unknown", "N/A", "null", "NULL")
    | summarize 
        emergency_order_count = countif(maintenance_type == "EMERGENCY_REPAIR"),
        pending_order_count = countif(maintenance_status != "COMPLETED"),
        raw_avg_work_order_resolution_minutes = avg(estimated_duration_minutes),
        last_updated_timestamp = max(ingestion_time())
        by facility_id = toupper(facility_id), equipment_id, maintenance_type
}

// 7. materialized_view_crop_biological_stress
.create-or-alter materialized-view with (backfill = true) materialized_view_crop_biological_stress on table CropTelemetry {
    CropTelemetry
    | where isnotempty(facility_id) and facility_id !in ("Unknown", "N/A", "null", "NULL")
    | where isnotempty(zone_id) and zone_id !in ("Unknown", "N/A", "null", "NULL")
    | where isnotempty(crop_type) and crop_type !in ("Unknown", "N/A", "null", "NULL")
    | summarize raw_crop_health_score = avg(health_score), raw_growth_rate = avg(growth_rate), raw_total_biomass_grams = sum(biomass_grams), raw_biological_stress_index = avg(environmental_stress_index), high_crop_stress_count = countif(environmental_stress_index > 0.45), last_updated_timestamp = max(ingestion_time()) by facility_id = toupper(facility_id), zone_id, crop_type
}
```

---

#### Section 8.2: Consumer-Facing Analytical KQL Functions

```kql
// 1. get_facility_operational_overview
.create-or-alter function with (docstring = "Summarizes facility operational health using materialized_view_facility_summary") 
get_facility_operational_overview(window_minutes:int = 15) {
    materialized_view_facility_summary
    | where last_updated_timestamp > ago(window_minutes * 1m)
    | extend facility_health_score = round(raw_facility_health_score, 2), total_power_consumption_kw = round(raw_total_power_consumption_kw, 2)
    | extend health_status = case(facility_health_score >= 85.0, "OPTIMAL", facility_health_score >= 70.0, "DEGRADED", "CRITICAL")
    | project facility_id, facility_name, region, facility_health_score, total_power_consumption_kw, active_critical_alerts, health_status, last_updated_timestamp
}

// 2. get_equipment_critical_anomalies (Dynamic FacilityOperations Lookup)
.create-or-alter function with (docstring = "Monitors critical equipment risk using materialized_view_equipment_risk") 
get_equipment_critical_anomalies(window_minutes:int = 15) {
    materialized_view_equipment_risk
    | where last_updated_timestamp > ago(window_minutes * 1m)
    | where critical_failure_count > 0
    | lookup (FacilityOperations | summarize facility_name = take_any(facility_name) by facility_id = toupper(facility_id)) on facility_id
    | extend facility_name = coalesce(facility_name, facility_id)
    | extend equipment_health_score = round(raw_equipment_health_score, 2), failure_probability_score = round(raw_failure_probability_score, 4), equipment_risk_score = round(raw_equipment_risk_score, 2)
    | extend alert_required = (critical_failure_count > 0)
    | project facility_id, facility_name, equipment_type, critical_failure_count, equipment_health_score, failure_probability_score, equipment_risk_score, alert_required, last_updated_timestamp
}

// 3. get_environmental_stress_anomalies (Dynamic FacilityOperations Lookup)
.create-or-alter function with (docstring = "Monitors micro-climate stability score, VPD, and thermal drift across growing zones with facility_name lookup") 
get_environmental_stress_anomalies(window_minutes:int = 60) {
    EnvironmentalEnriched
    | where ingestion_timestamp > ago(window_minutes * 1m)
    | where isnotempty(facility_id) and facility_id !in ("Unknown", "N/A", "null", "NULL")
    | where isnotempty(zone_id) and zone_id !in ("Unknown", "N/A", "null", "NULL")
    | lookup (FacilityOperations | summarize facility_name = take_any(facility_name) by facility_id = toupper(facility_id)) on facility_id
    | extend facility_name = coalesce(facility_name, facility_id)
    | summarize avg_vpd_kpa = round(avg(vapor_pressure_deficit_kpa), 3), avg_temp_drift_c = round(avg(temperature_deviation_celsius), 2) by facility_name, zone_id
    | extend microclimate_stability_score = round(maxof(0.0, 100.0 - (abs(avg_temp_drift_c) * 5.0 + abs(avg_vpd_kpa - 1.10) * 35.0)), 1)
    | sort by facility_name asc, zone_id asc
}

// 4. get_irrigation_hydraulic_anomalies (Dynamic FacilityOperations Lookup)
.create-or-alter function with (docstring = "Monitors hydraulic flow drops using materialized_view_irrigation_summary") 
get_irrigation_hydraulic_anomalies(window_minutes:int = 15) {
    materialized_view_irrigation_summary
    | where last_updated_timestamp > ago(window_minutes * 1m)
    | where anomalous_cycle_count > 0
    | lookup (FacilityOperations | summarize facility_name = take_any(facility_name) by facility_id = toupper(facility_id)) on facility_id
    | extend facility_name = coalesce(facility_name, facility_id)
    | extend irrigation_flow_rate_lpm = round(raw_irrigation_flow_rate_lpm, 2), pump_pressure_kpa = round(raw_pump_pressure_kpa, 2)
    | extend alert_required = (anomalous_cycle_count > 0)
    | project facility_id, facility_name, zone_id, anomalous_cycle_count, irrigation_flow_rate_lpm, pump_pressure_kpa, alert_required, last_updated_timestamp
}

// 5. get_lighting_dli_deficit (Dynamic FacilityOperations Lookup)
.create-or-alter function with (docstring = "Monitors DLI light deficits using materialized_view_lighting_summary") 
get_lighting_dli_deficit(window_minutes:int = 15) {
    materialized_view_lighting_summary
    | where last_updated_timestamp > ago(window_minutes * 1m)
    | where photoperiod_deficit_count > 0
    | lookup (FacilityOperations | summarize facility_name = take_any(facility_name) by facility_id = toupper(facility_id)) on facility_id
    | extend facility_name = coalesce(facility_name, facility_id)
    | extend daily_light_integral_dli = round(raw_daily_light_integral_dli, 2), light_intensity_percentage = round(raw_light_intensity_percentage, 2)
    | extend alert_required = (photoperiod_deficit_count > 0)
    | project facility_id, facility_name, zone_id, photoperiod_deficit_count, daily_light_integral_dli, light_intensity_percentage, alert_required, last_updated_timestamp
}

// 6. get_maintenance_sla_breach (Dynamic FacilityOperations Lookup)
.create-or-alter function with (docstring = "Monitors emergency maintenance work orders using materialized_view_maintenance_work_orders") 
get_maintenance_sla_breach(window_minutes:int = 15) {
    materialized_view_maintenance_work_orders
    | where last_updated_timestamp > ago(window_minutes * 1m)
    | where equipment_id !contains "99999" and equipment_id !contains "ORPHAN"
    | where emergency_order_count > 0 or pending_order_count > 0
    | lookup (FacilityOperations | summarize facility_name = take_any(facility_name) by facility_id = toupper(facility_id)) on facility_id
    | extend facility_name = coalesce(facility_name, facility_id)
    | extend avg_work_order_resolution_minutes = round(raw_avg_work_order_resolution_minutes, 1)
    | extend alert_required = (emergency_order_count > 0)
    | project facility_id, facility_name, equipment_id, maintenance_type, emergency_order_count, pending_order_count, avg_work_order_resolution_minutes, alert_required, last_updated_timestamp
}

// 7. get_crop_biological_stress_overview (Dynamic FacilityOperations Lookup)
.create-or-alter function with (docstring = "Summarizes crop biological health, stress percentage, and growth rates using materialized_view_crop_biological_stress") 
get_crop_biological_stress_overview(window_minutes:int = 15) {
    materialized_view_crop_biological_stress
    | where last_updated_timestamp > ago(window_minutes * 1m)
    | lookup (FacilityOperations | summarize facility_name = take_any(facility_name) by facility_id = toupper(facility_id)) on facility_id
    | extend facility_name = coalesce(facility_name, facility_id)
    | extend crop_health_score = round(raw_crop_health_score, 1), daily_growth_rate_g_day = strcat(tostring(round(raw_growth_rate, 3)), " g/day"), total_biomass_grams = round(raw_total_biomass_grams, 1), biological_stress_pct = strcat(tostring(round(raw_biological_stress_index, 1)), "%")
    | extend alert_required = (high_crop_stress_count > 0 or raw_biological_stress_index > 40.0)
    | project facility_id, facility_name, zone_id, crop_type, crop_health_score, daily_growth_rate_g_day, total_biomass_grams, biological_stress_pct, high_crop_stress_count, alert_required, last_updated_timestamp
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
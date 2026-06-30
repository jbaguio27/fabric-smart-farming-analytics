# KPI Mapping Matrix

## Purpose

This document maps business KPIs to their underlying data sources, calculation logic, and reporting dashboards.

The KPI Mapping Matrix provides end-to-end traceability between business objectives and the Microsoft Fabric data platform. It ensures KPI definitions remain consistent across Eventhouse, Lakehouse, Warehouse, and Power BI.

---

# KPI Mapping Matrix

| KPI | Source Fact Table(s) | Source Dimension(s) | Calculation Logic | Dashboard(s) |
|-----|----------------------|---------------------|-------------------|--------------|
| Crop Health Score | fact_sensor_telemetry | dim_crop_batch, dim_facility_structure | Composite score derived from environmental measurements within acceptable thresholds | Executive Dashboard, Crop Analytics Dashboard |
| Crop Mortality Rate | fact_sensor_telemetry | dim_crop_batch | (Failed Crop Batches ÷ Total Crop Batches) × 100 | Executive Dashboard, Crop Analytics Dashboard |
| Growth Cycle Completion Rate | fact_sensor_telemetry | dim_crop_batch | (Harvested Crop Batches ÷ Total Crop Batches) × 100 | Crop Analytics Dashboard |
| Active Critical Alerts | fact_sensor_telemetry, fact_hardware_metrics | dim_facility_structure | Count of unresolved critical alerts | Operations Dashboard, Regional Operations Dashboard |
| Average Alert Response Time | fact_sensor_telemetry | dim_facility_structure | Average time between alert generation and acknowledgment | Regional Operations Dashboard |
| Facility Health Score | fact_sensor_telemetry, fact_hardware_metrics | dim_facility_structure | Composite operational health score | Executive Dashboard, Regional Operations Dashboard |
| Equipment Availability | fact_hardware_metrics | dim_sensor, dim_facility_structure | (Equipment Uptime ÷ Total Operating Time) × 100 | Executive Dashboard, Regional Operations Dashboard |
| Pump Failure Rate | fact_hardware_metrics | dim_sensor | (Pump Failures ÷ Total Pump Events) × 100 | Regional Operations Dashboard |
| Sensor Availability | fact_sensor_telemetry | dim_sensor | (Healthy Sensor Readings ÷ Total Expected Readings) × 100 | Platform Monitoring Dashboard |
| Environmental Stability Score | fact_sensor_telemetry | dim_crop_batch, dim_facility_structure | Percentage of environmental readings within acceptable operating ranges | Crop Analytics Dashboard |
| Out-of-Range Sensor Events | fact_sensor_telemetry | dim_sensor, dim_facility_structure | Count of telemetry events flagged as OUT_OF_BOUNDS | Operations Dashboard |
| End-to-End Processing Latency | fact_sensor_telemetry | None | ingestion_timestamp − event_timestamp | Platform Monitoring Dashboard |
| Data Quality Score | fact_sensor_telemetry | None | (GOOD Records ÷ Total Records) × 100 | Platform Monitoring Dashboard |
| Pipeline Success Rate | Pipeline Monitoring Logs | None | (Successful Pipeline Runs ÷ Total Pipeline Runs) × 100 | Platform Monitoring Dashboard |
| Multi-Facility Operational Score | fact_sensor_telemetry, fact_hardware_metrics | dim_crop_batch, dim_facility_structure | Weighted aggregation of operational KPIs across all facilities | Executive Dashboard |

---

# KPI Ownership

| KPI Category | Business Owner |
|--------------|----------------|
| Crop Health | Agricultural Director |
| Operations | Operations Manager |
| Equipment | Operations Manager |
| Environmental | Agricultural Director |
| Data Platform | Data Engineering Team |
| Executive | Executive Leadership |

---

# Data Refresh Strategy

| KPI Category | Refresh Frequency |
|--------------|-------------------|
| Crop Health | Hourly |
| Operations | Near Real-Time |
| Equipment | Near Real-Time |
| Environmental | Near Real-Time |
| Data Platform | Near Real-Time |
| Executive | Near Real-Time |

---

# Implementation Notes

The calculation logic defined in this document represents the business definition of each KPI.

Implementation details, including SQL queries, KQL queries, Spark transformations, or Power BI DAX measures, will be documented during the implementation phases of the project.

The Event Catalog and Event Schema documents will define the raw telemetry events that populate the fact and dimension tables referenced in this matrix.
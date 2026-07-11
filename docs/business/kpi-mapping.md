# KPI Mapping Matrix

## Purpose

This document maps business KPIs to their underlying data sources, calculation logic, and reporting dashboards.

The KPI Mapping Matrix provides end-to-end traceability between business objectives and the Microsoft Fabric Smart Farming Analytics Platform. It ensures KPI definitions remain consistent across Eventhouse, OneLake Lakehouse, Fabric Warehouse, and Power BI.

The platform separates operational analytics from historical business analytics. Operational KPIs are calculated from streaming telemetry stored in Eventhouse, while historical KPIs are derived from curated analytical datasets stored in the Fabric Warehouse.

---

# KPI Mapping Matrix

| KPI | Source Fact Table(s) | Supporting Dimension(s) | Calculation Logic | Dashboard(s) |
|-----|----------------------|---------------------|-------------------|--------------|
| Crop Health Score | fact_sensor_telemetry | dim_crop_batch, dim_facility, dim_date | Composite score derived from environmental measurements within acceptable thresholds | Executive Dashboard, Farm Performance Dashboard |
| Crop Mortality Rate | fact_sensor_telemetry | dim_crop_batch, dim_date | (Failed Crop Batches ÷ Total Crop Batches) × 100 | Executive Dashboard, Farm Performance Dashboard |
| Growth Cycle Completion Rate | fact_sensor_telemetry | dim_crop_batch, dim_date | (Harvested Crop Batches ÷ Total Crop Batches) × 100 | Farm Performance Dashboard |
| Facility Health Score | fact_sensor_telemetry, fact_hardware_metrics | dim_facility, dim_date | Composite operational health score | Executive Dashboard, Real-Time Operations Dashboard |
| Equipment Availability | fact_hardware_metrics | dim_sensor, dim_facility, dim_date | (Equipment Uptime ÷ Total Operating Time) × 100 | Executive Dashboard, Farm Performance Dashboard |
| Pump Failure Rate | fact_hardware_metrics | dim_sensor, dim_date | (Pump Failures ÷ Total Pump Events) × 100 | Farm Performance Dashboard |
| Environmental Stability Score | fact_sensor_telemetry | dim_crop_batch, dim_facility, dim_date | Percentage of environmental readings within acceptable operating ranges | Farm Performance Dashboard |
| Multi-Facility Operational Score | fact_sensor_telemetry, fact_hardware_metrics | dim_crop_batch, dim_facility, dim_date | Weighted aggregation of operational KPIs across all facilities | Executive Dashboard |
| Active Critical Alerts | Eventhouse (KQL) | Facility Metadata | Count of unresolved critical alerts | Real-Time Operations Dashboard |
| Average Alert Response Time | Eventhouse (KQL) | Facility Metadata | Average time between alert generation and acknowledgment | Real-Time Operations Dashboard |
| Sensor Availability | Eventhouse (KQL) | Facility Metadata | (Active Sensors Reporting ÷ Total Registered Sensors) × 100 | Real-Time Operations Dashboard, Platform Monitoring Dashboard |
| Current Environmental Status | Eventhouse (KQL) | Facility Metadata | Latest temperature, humidity, pH, EC, and dissolved oxygen readings | Real-Time Operations Dashboard |
| Out-of-Range Sensor Events | Eventhouse (KQL) | Facility Metadata | Count of telemetry events exceeding configured operational thresholds | Real-Time Operations Dashboard |
| End-to-End Processing Latency | Eventhouse (KQL) | None | dashboard_available_timestamp − event_timestamp | Platform Monitoring Dashboard |
| Data Quality Score | fact_sensor_telemetry | None | (Valid Records ÷ Total Records) × 100 | Platform Monitoring Dashboard |
| Pipeline Success Rate | Fabric Data Factory Pipeline Logs (Pipeline 1 & Pipeline 2) | None | (Successful Pipeline Runs ÷ Total Pipeline Runs) × 100 | Platform Monitoring Dashboard |
| Warehouse Load Success Rate | Fabric Data Factory Pipeline Logs (Pipeline 2) | None | (Successful Warehouse MERGE Executions ÷ Total MERGE Executions) × 100 | Platform Monitoring Dashboard |
| Quarantine Rate | quarantine_invalid_events | None | (Quarantined Records ÷ Total Incoming Records) × 100 | Platform Monitoring Dashboard |
| Platform Availability | Fabric Monitoring Hub | None | (Available Service Time ÷ Total Service Time) × 100 | Platform Monitoring Dashboard |

---

# Dashboard Data Sources

| Dashboard | Primary Data Source | Primary Audience |
|------------|--------------------|------------------|
| Real-Time Operations Dashboard | Eventhouse (KQL) | Operations Team, Farm Managers |
| Farm Performance Dashboard | Fabric Warehouse | Operations Managers, Business Analysts |
| Executive Dashboard | Fabric Warehouse | Executive Leadership |
| Platform Monitoring Dashboard | Fabric Monitoring Hub, Eventhouse, Monitoring Lakehouse, Fabric Data Factory Pipeline Logs | Data Engineering Team |

---

# KPI Ownership

| KPI Category | Business Owner |
|--------------|----------------|
| Crop Health | Agricultural Director |
| Operations | Operations Manager |
| Equipment | Operations Manager |
| Environmental | Agricultural Director |
| Data Platform | Data Engineering Team |
| Platform Operations | Data Engineering Team |
| Executive | Executive Leadership |

---

# Data Refresh Strategy

| KPI Category | Refresh Frequency |
|--------------|-------------------|
| Real-Time Operations | Less than 15 seconds |
| Equipment Monitoring | Less than 15 seconds |
| Environmental Monitoring | Less than 15 seconds |
| Historical Analytics | Scheduled (Hourly) |
| Executive Reporting | Scheduled (Hourly) |
| Platform Monitoring | Near Real-Time (1 to 5 minutes depending on metric source) |

---

# Implementation Notes

The calculation logic defined in this document represents the business definition of each KPI.

Implementation details, including KQL queries, SQL queries, Spark Notebook transformations, Fabric Data Factory pipelines, and Power BI semantic models, will be documented during the implementation phases of the project.

Operational dashboards consume streaming telemetry directly from Eventhouse using KQL queries to provide low-latency operational visibility.

Historical dashboards consume curated analytical datasets from the Fabric Warehouse after processing through the OneLake Medallion Architecture.

The Platform Monitoring Dashboard consolidates telemetry from Microsoft Fabric Monitoring Hub, Eventhouse, Fabric Data Factory pipeline logs, Spark Notebook execution logs, Warehouse load metrics, and Monitoring Lakehouse tables to provide a unified operational view of platform health.

The Event Catalog and Event Schema documents define the telemetry events that populate the streaming platform and downstream analytical models.
# Dashboard Requirements

## Purpose

This document defines the reporting and dashboard requirements for the Microsoft Fabric Smart Farming Analytics Platform.

The platform provides two analytical experiences:

- Near real-time operational monitoring powered by Microsoft Fabric Real-Time Intelligence.
- Historical analytics and executive reporting powered by the Fabric Warehouse.

Each dashboard is designed to support a specific user persona while maintaining a consistent reporting experience across the organization.

---

# Dashboard Overview

| Dashboard | Primary Persona | Data Source | Refresh Type |
|------------|-----------------|-------------|--------------|
| Real-Time Operations Dashboard | Farm Operator | Eventhouse | Near Real-Time |
| Farm Performance Dashboard | Agricultural Director | Fabric Warehouse | Scheduled |
| Executive Dashboard | Executive Leadership | Fabric Warehouse | Scheduled |
| Platform Monitoring Dashboard | Data Engineer | Fabric Monitoring Hub, Eventhouse | Near Real-Time |

---

# Dashboard Requirements

## Dashboard 1: Real-Time Operations Dashboard

### Primary Users

- Farm Operator
- Operations Manager

### Business Purpose

Provide live operational visibility into environmental conditions, equipment status, and active alerts across one or more farming facilities.

### Data Source

- Eventhouse
- KQL Database

### Key Metrics

- Current Water pH
- Current Dissolved Oxygen
- Current Electrical Conductivity
- Current Air Temperature
- Current Humidity
- Pump Status
- Active Critical Alerts
- Sensor Availability

### Visualizations

- Live KPI Cards
- Live Sensor Trend Charts
- Current Equipment Status Grid
- Active Alert Feed
- Facility Status Overview

---

## Dashboard 2: Farm Performance Dashboard

### Primary Users

- Agricultural Director
- Operations Manager
- Data Analyst

### Business Purpose

Provide historical operational analysis to improve crop performance, environmental stability, and equipment reliability across multiple facilities.

### Data Source

- Fabric Warehouse
- Gold Star Schema

### Key Metrics

- Crop Health Score
- Crop Mortality Rate
- Growth Cycle Completion Rate
- Environmental Stability Score
- Equipment Availability
- Pump Failure Rate
- Historical Crop Batch Trends

### Visualizations

- KPI Cards
- Historical Trend Charts
- Facility Comparison Matrix
- Heat Maps
- Seasonal Trend Analysis

---

## Dashboard 3: Executive Dashboard

### Primary Users

- Executive Leadership

### Business Purpose

Provide executives with historical business performance, enterprise KPIs, and strategic trends across all farming facilities.

### Data Source

- Fabric Warehouse
- Gold Star Schema

### Key Metrics

- Total Active Facilities
- Overall Crop Health Score
- Facility Health Score
- Equipment Availability
- Monthly Energy Consumption
- Multi-Facility Operational Score
- Monthly Operational Trends
- Average Daily Critical Alerts

### Visualizations

- KPI Cards
- Facility Performance Ranking
- Monthly Trend Lines
- Production Summary
- Operational Scorecards

---

## Dashboard 4: Platform Monitoring Dashboard

### Primary Users

- Data Engineer

### Business Purpose

Monitor the health, reliability, and performance of the Microsoft Fabric data platform.

### Data Source

- Microsoft Fabric Monitoring Hub
- Eventhouse (Streaming Metrics)
- Fabric Data Factory Pipeline History
- Spark Notebook Execution History
- Validation Logs
- Quarantine Tables

### Key Metrics

Platform Health

- Workspace Availability
- Capacity Utilization
- OneLake Storage Consumption

Streaming

- Eventstream Throughput
- Eventstream Latency
- Eventhouse Ingestion Rate
- Eventhouse Query Latency

Batch Processing

- Pipeline 1 Success Rate
- Pipeline 2 Success Rate
- Spark Notebook Duration
- Warehouse Publishing Duration
- Rows Inserted
- Rows Updated
- Retry Count

Data Quality

- Invalid Records
- Schema Violations
- Quarantine Growth
- Data Quality Score

Warehouse

- Incremental Load Status
- Table Growth
- Refresh Duration

Overall

- End-to-End Processing Latency

### Visualizations

- Platform Health Overview
- Capacity Utilization Gauge
- Streaming Throughput Chart
- Eventhouse Ingestion Timeline
- Pipeline Execution Timeline
- Spark Notebook Performance
- Warehouse MERGE Statistics
- Quarantine Growth Trend
- Data Quality Scorecard
- Alert Severity Breakdown

---

# Dashboard to Persona Mapping

| Dashboard | Primary Persona | Secondary Persona |
|------------|-----------------|-------------------|
| Real-Time Operations Dashboard | Farm Operator | Operations Manager |
| Farm Performance Dashboard | Agricultural Director | Data Analyst |
| Executive Dashboard | Executive Leadership | Operations Manager |
| Platform Monitoring Dashboard | Data Engineer | Operations Manager |

---

# Dashboard Data Sources

| Dashboard | Primary Data Source | Microsoft Fabric Component |
|------------|---------------------|----------------------------|
| Real-Time Operations Dashboard | Streaming Telemetry | Eventhouse |
| Farm Performance Dashboard | Historical Analytical Model | Fabric Warehouse |
| Executive Dashboard | Historical Analytical Model | Fabric Warehouse |
| Platform Monitoring Dashboard | Platform Metrics | Fabric Monitoring Hub, Eventhouse |

---

# Dashboard Refresh Strategy

| Dashboard | Refresh Frequency |
|------------|-------------------|
| Real-Time Operations Dashboard | Near Real-Time (1 to 5 minute refresh depending on data source) |
| Farm Performance Dashboard | After successful Pipeline 2 execution |
| Executive Dashboard | After successful Pipeline 2 execution |
| Platform Monitoring Dashboard | Near Real-Time |

---

# Dashboard Access Matrix

| Dashboard | Farm Operator | Operations Manager | Agricultural Director | Data Analyst | Data Engineer | Executive Leadership |
|------------|--------------|--------------------|-----------------------|--------------|---------------|----------------------|
| Real-Time Operations Dashboard | Full Access | Full Access | View | View | View | View |
| Farm Performance Dashboard | View | Full Access | Full Access | Full Access | View | View |
| Executive Dashboard | View | View | View | View | View | Full Access |
| Platform Monitoring Dashboard | No Access | View | No Access | No Access | Full Access | No Access |

---

# Design Principles

All dashboards shall:

- Present only role-appropriate information.
- Clearly separate real-time operational monitoring from historical business reporting.
- Support interactive filtering where applicable.
- Provide consistent navigation and visual design.
- Highlight critical operational conditions using standardized indicators.
- Minimize unnecessary visual clutter.
- Display KPIs using business-approved definitions from the KPI Mapping Matrix.
- Consume governed datasets from their designated Microsoft Fabric components.

---

# Architecture Alignment

The dashboard strategy follows the Microsoft Fabric solution architecture.

- Real-Time Operations Dashboard consumes streaming telemetry directly from Eventhouse using KQL.
- Farm Performance Dashboard consumes curated historical datasets from the Fabric Warehouse.
- Executive Dashboard provides enterprise KPI reporting using the Fabric Warehouse.
- Platform Monitoring Dashboard combines telemetry from Microsoft Fabric Monitoring Hub, Eventhouse, Fabric Data Factory pipeline history, Spark notebook execution history, validation logs, and quarantine datasets.

The dashboard provides unified operational visibility across:

- Microsoft Fabric infrastructure
- Streaming ingestion
- Batch processing
- Data quality
- Warehouse loading
- Power BI refresh operations

This separation ensures operational monitoring remains low latency while historical reporting uses governed analytical datasets.

---

# Monitoring Dashboard Dependencies

The Platform Monitoring Dashboard consumes operational telemetry from multiple platform components.

| Component | Metrics |
|-----------|---------|
| Fabric Monitoring Hub | Workspace availability, Capacity utilization |
| Eventhouse | Streaming throughput, Ingestion latency |
| Fabric Data Factory | Pipeline execution status, Warehouse publishing |
| Spark Notebooks | Notebook execution duration, Processing metrics |
| Validation Logs | Validation failures, Data quality metrics |
| Quarantine Tables | Invalid records, Schema violations |
| Warehouse | Table growth, Incremental loads |
| Power BI | Dataset refresh status, Refresh duration |

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
- Historical Yield Trends

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
- Monthly Production Trends
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

- Fabric Monitoring Hub
- Eventhouse

### Key Metrics

- Eventstream Throughput
- Eventhouse Ingestion Rate
- Eventhouse Query Latency
- Data Factory Pipeline Success Rate
- Spark Notebook Execution Status
- Processing Latency
- Failed Events
- Data Quality Score

### Visualizations

- Fabric Service Health Cards
- Event Throughput Charts
- Pipeline Execution Timeline
- Latency Trends
- Failure Summary
- Data Quality Overview

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
| Farm Performance Dashboard | Gold Star Schema | Fabric Warehouse |
| Executive Dashboard | Enterprise KPIs | Fabric Warehouse |
| Platform Monitoring Dashboard | Platform Metrics | Fabric Monitoring Hub, Eventhouse |

---

# Dashboard Refresh Strategy

| Dashboard | Refresh Frequency |
|------------|-------------------|
| Real-Time Operations Dashboard | Near Real-Time (<15 seconds) |
| Farm Performance Dashboard | Scheduled Batch |
| Executive Dashboard | Scheduled Batch |
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
- Platform Monitoring Dashboard combines Microsoft Fabric Monitoring Hub metrics with Eventhouse operational metrics.

This separation ensures operational monitoring remains low latency while historical reporting uses governed analytical datasets.
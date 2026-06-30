# Dashboard Requirements

## Purpose

This document defines the reporting and dashboard requirements for the Microsoft Fabric Smart Farming Analytics Platform.

The dashboards are designed to support the operational, analytical, and strategic needs of HydroGrow Solutions. Each dashboard is aligned with one or more user personas and provides role-specific insights to support timely and informed decision-making.

---

# Dashboard Overview

| Dashboard | Primary Persona | Refresh Type |
|------------|-----------------|--------------|
| Executive Dashboard | Executive Leadership | Near Real-Time |
| Operations Dashboard | Farm Operator | Near Real-Time |
| Regional Operations Dashboard | Operations Manager | Near Real-Time |
| Crop Analytics Dashboard | Agricultural Director | Scheduled |
| Business Intelligence Dashboard | Data Analyst | Scheduled |
| Platform Monitoring Dashboard | Data Engineer | Near Real-Time |

---

# Dashboard Requirements

## Dashboard 1: Executive Dashboard

### Primary Users

- Executive Leadership

### Business Purpose

Provide executives with a high-level view of operational performance across all farming facilities.

### Key Metrics

- Total Active Facilities
- Overall Crop Health Score
- Active Critical Alerts
- Crop Yield Performance
- Equipment Availability
- Daily Energy Consumption
- Monthly Production Trends

### Visualizations

- KPI Cards
- Geographic Facility Map
- Trend Lines
- Alert Summary
- Facility Comparison Charts

---

## Dashboard 2: Operations Dashboard

### Primary Users

- Farm Operator

### Business Purpose

Provide real-time monitoring of environmental conditions and equipment status within an assigned facility.

### Key Metrics

- Water pH
- Dissolved Oxygen
- Electrical Conductivity
- Air Temperature
- Humidity
- Pump Status
- Active Alerts

### Visualizations

- Live KPI Cards
- Time-Series Charts
- Equipment Status Indicators
- Environmental Trend Graphs
- Alert Feed

---

## Dashboard 3: Regional Operations Dashboard

### Primary Users

- Operations Manager

### Business Purpose

Monitor operational performance across multiple facilities and identify emerging operational issues.

### Key Metrics

- Facility Health Score
- Equipment Downtime
- Active Alerts by Facility
- Energy Consumption
- Sensor Availability

### Visualizations

- Facility Comparison Matrix
- Heat Maps
- Trend Charts
- Alert Distribution
- Performance Rankings

---

## Dashboard 4: Crop Analytics Dashboard

### Primary Users

- Agricultural Director

### Business Purpose

Analyze historical crop performance and environmental trends to improve farming strategies.

### Key Metrics

- Crop Yield
- Growth Stage Distribution
- Historical pH Trends
- Environmental Stability
- Crop Mortality Rate

### Visualizations

- Historical Trend Charts
- Growth Stage Breakdown
- Correlation Charts
- Seasonal Comparisons

---

## Dashboard 5: Business Intelligence Dashboard

### Primary Users

- Data Analyst

### Business Purpose

Support analytical reporting and ad hoc business analysis using curated Gold-layer datasets.

### Key Metrics

- Historical Sensor Readings
- Equipment Performance
- Data Quality Metrics
- Production KPIs
- Environmental Trends

### Visualizations

- Interactive Reports
- Drill-Through Pages
- Trend Analysis
- Distribution Charts
- Custom Filters

---

## Dashboard 6: Platform Monitoring Dashboard

### Primary Users

- Data Engineer

### Business Purpose

Monitor the health and performance of the Microsoft Fabric data platform.

### Key Metrics

- Eventstream Throughput
- Eventhouse Ingestion Rate
- Pipeline Success Rate
- Processing Latency
- Failed Events
- Data Quality Score

### Visualizations

- Pipeline Health Cards
- Latency Trends
- Event Volume Charts
- Failure Summary
- Processing Timeline

---

# Dashboard to Persona Mapping

| Dashboard | Primary Persona | Secondary Persona |
|------------|-----------------|-------------------|
| Executive Dashboard | Executive Leadership | Operations Manager |
| Operations Dashboard | Farm Operator | Operations Manager |
| Regional Operations Dashboard | Operations Manager | Executive Leadership |
| Crop Analytics Dashboard | Agricultural Director | Data Analyst |
| Business Intelligence Dashboard | Data Analyst | Agricultural Director |
| Platform Monitoring Dashboard | Data Engineer | Platform Administrator |

---

# Dashboard Refresh Strategy

| Dashboard | Refresh Frequency |
|------------|-------------------|
| Executive Dashboard | Near Real-Time |
| Operations Dashboard | Near Real-Time |
| Regional Operations Dashboard | Near Real-Time |
| Crop Analytics Dashboard | Hourly |
| Business Intelligence Dashboard | Scheduled Batch |
| Platform Monitoring Dashboard | Near Real-Time |

---

# Design Principles

All dashboards shall:

- Follow a consistent visual design.
- Display only role-relevant information.
- Support interactive filtering and drill-through.
- Clearly distinguish operational and historical metrics.
- Highlight critical alerts using consistent visual indicators.
- Minimize unnecessary visual clutter.
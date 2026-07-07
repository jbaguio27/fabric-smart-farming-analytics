# Business KPIs

## Purpose

This document defines the Key Performance Indicators (KPIs) used to measure the operational performance, crop health, equipment reliability, and data platform effectiveness of the Microsoft Fabric Smart Farming Analytics Platform.

These KPIs drive the Real-Time Operations Dashboard, Farm Performance Dashboard, Executive Dashboard, and Platform Monitoring Dashboard. They provide a consistent business definition for operational monitoring, historical analytics, and strategic decision-making across the Microsoft Fabric platform.

---

# KPI Categories

The KPIs are organized into the following categories:

- Crop Health
- Operations
- Equipment Performance
- Environmental Stability
- Data Platform
- Enterprise Performance

---

# Crop Health KPIs

## KPI-001: Crop Health Score

### Business Objective

Measure the overall health of active crop batches.

### Description

A composite score calculated using environmental stability, sensor readings, and crop-specific thresholds.

### Target

≥ 95%

### Primary Users

- Agricultural Director
- Executive Leadership

---

## KPI-002: Crop Mortality Rate

### Business Objective

Measure the percentage of crops lost before harvest.

### Formula

Crop Losses / Total Crop Batches × 100

### Target

< 5%

### Primary Users

- Agricultural Director
- Executive Leadership

---

## KPI-003: Growth Cycle Completion Rate

### Business Objective

Measure the percentage of crop batches reaching harvest successfully.

### Target

≥ 98%

### Primary Users

- Agricultural Director

---

# Operations KPIs

## KPI-004: Active Critical Alerts

### Business Objective

Track unresolved operational incidents.

### Target

0 Active Critical Alerts

### Primary Users

- Farm Operator
- Operations Manager

### Dashboard

- Real-Time Operations Dashboard

---

## KPI-005: Average Alert Response Time

### Business Objective

Measure how quickly operational teams respond to alerts.

### Target

< 5 minutes

### Primary Users

- Operations Manager

### Dashboard

- Farm Performance Dashboard

---

## KPI-006: Facility Health Score

### Business Objective

Provide an overall operational health score for each facility.

### Components

- Environmental Stability
- Equipment Availability
- Active Alerts
- Sensor Availability

### Target

≥ 95%

### Primary Users

- Operations Manager
- Executive Leadership

### Dashboard

- Real-Time Operations Dashboard
- Executive Dashboard

---

# Equipment KPIs

## KPI-007: Equipment Availability

### Business Objective

Measure equipment uptime across all facilities.

### Formula

Operating Time / Total Available Time × 100

### Target

≥ 99%

### Primary Users

- Operations Manager

### Dashboard

- Farm Performance Dashboard
- Executive Dashboard

---

## KPI-008: Pump Failure Rate

### Business Objective

Track pump failures requiring maintenance.

### Target

< 1%

### Primary Users

- Operations Manager

---

## KPI-009: Sensor Availability

### Business Objective

Measure the percentage of operational IoT sensors.

### Target

≥ 99%

### Primary Users

- Data Engineer
- Operations Manager

### Dashboard

- Real-Time Operations Dashboard
- Platform Monitoring Dashboard

---

# Environmental KPIs

## KPI-010: Environmental Stability Score

### Business Objective

Measure how consistently environmental conditions remain within acceptable operating ranges.

### Components

- Water pH
- Temperature
- Humidity
- Dissolved Oxygen
- Electrical Conductivity
- Light Intensity

### Target

≥ 98%

### Primary Users

- Agricultural Director

### Dashboard

- Farm Performance Dashboard

---

## KPI-011: Out-of-Range Sensor Events

### Business Objective

Monitor abnormal environmental readings.

### Target

Decreasing trend month over month

### Primary Users

- Farm Operator
- Agricultural Director

### Dashboard

- Real-Time Operations Dashboard

---

# Data Platform KPIs

## KPI-012: End-to-End Processing Latency

### Business Objective

### Description

Measure the elapsed time between event generation and availability in the Real-Time Operations Dashboard.

### Target

< 15 seconds

### Primary Users

- Data Engineer

### Dashboard

- Platform Monitoring Dashboard

---

## KPI-013: Data Quality Score

### Business Objective

Measure the percentage of valid telemetry records successfully processed.

### Formula

Valid Records / Total Records × 100

### Target

≥ 99.5%

### Primary Users

- Data Engineer

### Dashboard

- Platform Monitoring Dashboard

---

## KPI-014: Pipeline Success Rate

### Business Objective

Measure successful execution of Spark Notebook transformations and Fabric Data Factory pipelines.

### Target

≥ 99.9%

### Primary Users

- Data Engineer

### Dashboard

- Platform Monitoring Dashboard

---

# Executive KPIs

## KPI-015: Multi-Facility Operational Score

### Business Objective

Provide a consolidated operational score across all facilities.

### Components

- Crop Health
- Facility Health
- Equipment Availability
- Active Alerts
- Data Quality

### Target

≥ 95%

### Primary Users

- Executive Leadership

### Dashboard

- Executive Dashboard

---

## KPI Summary

| KPI | Category | Target | Primary Dashboard | Primary Persona |
|-----|----------|--------|-------------------|-----------------|
| Crop Health Score | Crop Health | ≥95% | Farm Performance Dashboard | Agricultural Director |
| Crop Mortality Rate | Crop Health | <5% | Farm Performance Dashboard | Agricultural Director |
| Growth Cycle Completion Rate | Crop Health | ≥98% | Farm Performance Dashboard | Agricultural Director |
| Active Critical Alerts | Operations | 0 | Real-Time Operations Dashboard | Farm Operator |
| Average Alert Response Time | Operations | <5 min | Farm Performance Dashboard | Operations Manager |
| Facility Health Score | Operations | ≥95% | Real-Time Operations Dashboard | Operations Manager |
| Equipment Availability | Equipment | ≥99% | Farm Performance Dashboard | Operations Manager |
| Pump Failure Rate | Equipment | <1% | Farm Performance Dashboard | Operations Manager |
| Sensor Availability | Equipment | ≥99% | Platform Monitoring Dashboard | Data Engineer |
| Environmental Stability Score | Environment | ≥98% | Farm Performance Dashboard | Agricultural Director |
| Out-of-Range Sensor Events | Environment | Downward Trend | Real-Time Operations Dashboard | Farm Operator |
| End-to-End Processing Latency | Platform | <15 sec | Platform Monitoring Dashboard | Data Engineer |
| Data Quality Score | Platform | ≥99.5% | Platform Monitoring Dashboard | Data Engineer |
| Pipeline Success Rate | Platform | ≥99.9% | Platform Monitoring Dashboard | Data Engineer |
| Multi-Facility Operational Score | Executive | ≥95% | Executive Dashboard | Executive Leadership |

---

# KPI Governance

Business KPIs shall be reviewed periodically to ensure they remain aligned with operational goals, reporting requirements, and business priorities.

KPI definitions shall remain consistent across Eventhouse, the Fabric Warehouse, and Power BI semantic models. Any changes to KPI definitions, calculation methods, or target values shall be documented, reviewed, and approved before implementation.
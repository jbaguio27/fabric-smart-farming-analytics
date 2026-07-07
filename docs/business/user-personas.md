# User Personas

## Purpose

This document defines the primary users of the Microsoft Fabric Smart Farming Analytics Platform.

Understanding the responsibilities, goals, and data needs of each user group ensures that dashboards, alerts, security, and reporting are designed to support day-to-day operations and strategic decision-making.

---

# Persona 1: Farm Operator

## Overview

Farm Operators are responsible for monitoring the environmental conditions within a single smart farming facility. They respond to equipment failures, environmental anomalies, and operational alerts to ensure healthy crop growth.

## Responsibilities

- Monitor crop-growing conditions
- Respond to environmental alerts
- Investigate equipment failures
- Escalate critical operational issues
- Perform routine operational checks

## Data Needs

- Live environmental telemetry
- Current equipment status
- Active operational alerts
- Sensor health
- Real-Time Operations Dashboard

## Success Criteria

- Detect operational issues immediately
- Minimize crop loss
- Maintain healthy growing conditions

---

# Persona 2: Operations Manager

## Overview

Operations Managers oversee multiple farming facilities and ensure consistent operational performance across the organization.

## Responsibilities

- Monitor facility performance
- Coordinate operational teams
- Review equipment reliability
- Investigate recurring operational issues
- Manage operational efficiency

## Data Needs

- Real-Time Operations Dashboard
- Active operational incidents
- Multi-facility equipment status
- Facility performance metrics
- Historical performance comparisons

## Success Criteria

- Reduce operational downtime
- Improve equipment reliability
- Maintain production targets

---

# Persona 3: Agricultural Director

## Overview

The Agricultural Director focuses on crop health, production efficiency, and long-term farming performance.

## Responsibilities

- Monitor crop performance
- Analyze historical growing conditions
- Review environmental trends
- Improve crop yield strategies
- Evaluate biological risks

## Data Needs

- Farm Performance Dashboard
- Historical crop telemetry
- Growth stage analysis
- Environmental trend reports
- Crop batch performance
- Historical anomaly reports

## Success Criteria

- Improve crop yield
- Reduce crop mortality
- Optimize growing conditions

---

# Persona 4: Data Engineer

## Overview

The Data Engineer is responsible for building, monitoring, and maintaining the Smart Farming Analytics Platform.

## Responsibilities

- Monitor Eventstream ingestion
- Monitor Eventhouse streaming health
- Maintain Spark Notebook transformations
- Maintain Fabric Data Factory pipelines
- Resolve data quality issues
- Maintain OneLake Lakehouse assets
- Maintain Fabric Warehouse assets

## Data Needs

- Eventstream health metrics
- Eventhouse ingestion metrics
- Spark Notebook execution status
- Fabric Data Factory pipeline status
- Data quality reports
- Processing latency
- Failed event logs
- Platform Monitoring Dashboard

## Success Criteria

- Maintain reliable pipelines
- Ensure high data quality
- Meet performance targets
- Minimize processing failures

---

# Persona 5: Data Analyst

## Overview

Data Analysts transform historical telemetry into business insights that support operational improvements and strategic planning.

## Responsibilities

- Build analytical reports
- Analyze historical trends
- Investigate operational patterns
- Support business stakeholders
- Develop Power BI reports

## Data Needs

- Fabric Warehouse
- Gold-layer datasets
- Historical telemetry
- Business KPIs
- Farm Performance Dashboard
- Executive Dashboard

## Success Criteria

- Deliver accurate reporting
- Identify operational trends
- Support data-driven decisions

---

# Persona 6: Executive Leadership

## Overview

Executives require a high-level operational view of the business to monitor organizational performance and support strategic decision-making.

## Responsibilities

- Review company performance
- Monitor production efficiency
- Evaluate operational risks
- Track strategic KPIs
- Support investment decisions

## Data Needs

- Executive Dashboard
- Enterprise KPIs
- Multi-facility performance
- Crop yield metrics
- Operational summaries
- Historical business trends

## Success Criteria

- Improve business performance
- Reduce operational costs
- Increase production efficiency
- Support company growth

---

# Persona Summary

| Persona | Primary Focus | Primary Dashboard | Primary Data Source |
|----------|---------------|-------------------|---------------------|
| Farm Operator | Real-time facility monitoring | Real-Time Operations Dashboard | Eventhouse |
| Operations Manager | Multi-facility operations | Real-Time Operations Dashboard | Eventhouse + Fabric Warehouse |
| Agricultural Director | Crop health and yield | Farm Performance Dashboard | Fabric Warehouse |
| Data Engineer | Platform operations | Platform Monitoring Dashboard | Fabric Monitoring Hub |
| Data Analyst | Historical analytics | Farm Performance Dashboard | Fabric Warehouse |
| Executive Leadership | Business performance | Executive Dashboard | Fabric Warehouse |

---

# Role-Based Access Mapping

| Persona | Access Level |
|----------|--------------|
| Farm Operator | Read access to assigned facility |
| Operations Manager | Read access to Real-Time Operations Dashboard and Farm Performance Dashboard |
| Agricultural Director | Read access to historical analytics |
| Data Engineer | Administrative access to Fabric engineering resources |
| Data Analyst | Read access to Fabric Warehouse, curated analytical datasets, and historical dashboards |
| Executive Leadership | Read access to Executive Dashboard and enterprise KPI reports |

---

# Design Considerations

The user personas influence the design of several project components:

- Real-Time Operations Dashboard
- Farm Performance Dashboard
- Executive Dashboard
- Platform Monitoring Dashboard
- Microsoft Fabric workspace security
- Role-Based Access Control (RBAC)
- Data Activator alert routing
- Reporting and semantic models

These personas will be referenced throughout the remaining project epics to ensure the platform is designed around user needs rather than technology alone.
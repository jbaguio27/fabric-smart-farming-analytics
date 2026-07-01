# Microsoft Fabric Solution Architecture

## Document Information

| Field | Value |
|--------|--------|
| Project | Microsoft Fabric Smart Farming Analytics Platform |
| Business | HydroGrow Solutions |
| Repository | fabric-smart-farming-analytics |
| Document Version | 1.0 |
| Status | Approved |
| Owner | Data Engineering |
| Last Updated | July 2026 |

---

# Purpose

This document describes the end-to-end Microsoft Fabric solution architecture for the Smart Farming Analytics Platform.

The architecture enables HydroGrow Solutions to collect, process, store, analyze, and visualize IoT telemetry generated from multiple smart farming facilities.

The solution combines Microsoft Fabric Real-Time Intelligence with OneLake-based analytics to support both operational monitoring and historical business reporting.

---

# Solution Architecture Diagram
![Microsoft Fabric Solution Architecture](../../architecture/diagrams/microsoft-fabric-solution-architecture.png)

**Figure 1.** End-to-end Microsoft Fabric solution architecture showing the flow of IoT telemetry from event generation through real-time analytics, historical processing, and business intelligence.

---

# Business Objectives

The architecture is designed to achieve the following objectives:

- Detect environmental issues within 15 seconds
- Monitor thousands of IoT devices simultaneously
- Support real-time operational dashboards
- Build a historical analytics platform
- Provide executive reporting through Power BI
- Maintain a single governed data platform
- Minimize operational complexity

---

# High-Level Architecture

The platform follows a layered architecture consisting of five logical layers.

```text
┌────────────────────────────────────────────┐
│ IoT Devices                               │
│ Sensors, Pumps, HVAC, LED Controllers     │
└────────────────────────────────────────────┘
                    │
                    ▼
┌────────────────────────────────────────────┐
│ Python Event Generator                    │
│ Faker-based IoT Simulator                 │
└────────────────────────────────────────────┘
                    │
                    ▼
┌────────────────────────────────────────────┐
│ Eventstream                               │
│ Real-Time Ingestion                       │
└────────────────────────────────────────────┘
                    │
                    ▼
┌────────────────────────────────────────────┐
│ Eventhouse                                │
│ KQL Database                              │
│ Streaming Analytics                       │
└────────────────────────────────────────────┘
          │                     │
          │                     │
          ▼                     ▼
Data Activator         OneLake Lakehouse
Real-Time Alerts       Bronze Layer
                                │
                                ▼
                       Silver Layer
                                │
                                ▼
                        Gold Layer
                                │
                                ▼
                           Warehouse
                                │
                                ▼
                           Power BI
```

---

# Logical Architecture

The platform consists of the following components.

## Data Producers

Enterprise IoT telemetry is generated using a configurable Python simulator.

The simulator publishes multiple event types including:

- sensor.telemetry
- hardware.metrics
- crop.batch.lifecycle
- maintenance.activity
- platform.system
- alert.critical

Each event follows the canonical event envelope defined in the Event Schema document.

---

## Eventstream

Eventstream serves as the ingestion gateway for streaming telemetry.

Responsibilities include:

- Receiving events
- Initial routing
- Event buffering
- Streaming delivery
- Integration with Eventhouse

Eventstream is selected because it provides native integration with Microsoft Fabric Real-Time Intelligence.

---

## Eventhouse

Eventhouse is the operational data store for streaming analytics.

Responsibilities include:

- High-speed event ingestion
- Time-series storage
- KQL analytics
- Operational dashboards
- Real-time investigation
- Data Activator integration

Eventhouse is not considered the enterprise system of record.

Instead, it supports operational analytics requiring low latency.

---

## Data Activator

Data Activator continuously monitors streaming telemetry stored within Eventhouse.

Responsibilities include:

- Threshold monitoring
- Rule evaluation
- Critical event detection
- Operational notifications

Example alerts include:

- High temperature
- Low humidity
- Water pump failure
- LED malfunction
- Sensor offline
- Abnormal pH values

---

## OneLake Lakehouse

OneLake stores historical analytical datasets following the Medallion Architecture.

### Bronze

Stores immutable raw telemetry.

Characteristics:

- Append-only
- Minimal transformations
- Historical replay
- Full audit trail

---

### Silver

Stores validated and standardized datasets.

Processing includes:

- Data cleansing
- Schema validation
- Deduplication
- Data enrichment
- Standardized units

---

### Gold

Stores business-ready datasets optimized for analytics.

Contains:

- Fact tables
- Dimension tables
- Aggregated metrics

The Gold layer follows Kimball dimensional modeling.

---

## Warehouse

The Warehouse provides SQL-based analytical access.

Primary responsibilities:

- Business reporting
- Executive analytics
- Dimensional querying
- Power BI semantic models

Warehouse consumers include:

- Operations Managers
- Farm Managers
- Executives
- Business Analysts

---

## Power BI

Power BI provides executive dashboards.

Example dashboards include:

- Facility Health
- Equipment Monitoring
- Environmental Conditions
- Crop Performance
- Maintenance Performance
- Executive KPI Dashboard

---

# End-to-End Data Flow

The complete data flow consists of the following steps.

1. Python simulator generates IoT telemetry.
2. Events are published into Eventstream.
3. Eventstream delivers telemetry into Eventhouse.
4. Eventhouse enables real-time querying using KQL.
5. Data Activator monitors Eventhouse for alert conditions.
6. Streaming data is persisted into OneLake Bronze.
7. Spark transformations create Silver datasets.
8. Business transformations produce Gold datasets.
9. Gold datasets populate the Warehouse.
10. Power BI dashboards consume Warehouse models.

---

# Microsoft Fabric Services

| Service | Purpose |
|----------|---------|
| Eventstream | Streaming ingestion |
| Eventhouse | Operational streaming analytics |
| KQL Database | Real-time querying |
| Data Activator | Event-driven alerts |
| OneLake | Unified enterprise storage |
| Lakehouse | Historical analytics |
| Spark | Data transformations |
| Warehouse | SQL analytics |
| Power BI | Dashboards and reporting |
| Deployment Pipelines | Environment promotion |
| Git Integration | Source control |

---

# Design Principles

The architecture follows these principles.

## Separation of Concerns

Streaming analytics and historical analytics are isolated into separate components.

---

## Modular Processing

Each Fabric service performs a dedicated responsibility.

---

## Event-Driven Processing

Telemetry is processed immediately after generation.

---

## Governed Analytics

Historical datasets follow Medallion Architecture and Kimball dimensional modeling.

---

## Cloud-Native Design

The platform uses managed Microsoft Fabric services instead of self-managed infrastructure.

---

# Security Overview

The solution follows the principle of least privilege.

Key security practices include:

- Microsoft Entra ID authentication
- Workspace role-based access control
- OneLake permissions
- Warehouse SQL permissions
- Secure GitHub repository
- Managed identities where applicable

Detailed security design is documented in the Security Model.

---

# Monitoring Overview

Platform health is monitored using:

- Fabric Monitoring Hub
- Pipeline monitoring
- Eventstream metrics
- Eventhouse metrics
- Data Activator execution logs

Detailed operational monitoring is documented in the Monitoring Strategy.

---

# Scalability Considerations

The architecture supports future growth through:

- Additional farming facilities
- Increased IoT device counts
- Additional event types
- New analytical workloads
- Expanded Power BI reporting

No architectural redesign is required when onboarding additional facilities.

---

# Cost Considerations

The architecture minimizes operational overhead by using managed Microsoft Fabric services.

Primary cost drivers include:

- Real-Time Intelligence capacity
- OneLake storage
- Spark workloads
- Warehouse compute
- Power BI capacity

Detailed financial analysis is documented in the Cost Considerations document.

---

# Architecture Summary

The Microsoft Fabric Smart Farming Analytics Platform combines Real-Time Intelligence and OneLake analytics into a unified enterprise solution.

Operational telemetry is processed through Eventstream and Eventhouse for low-latency monitoring and alerting.

Historical datasets are curated through the Medallion Architecture before being modeled into a Kimball star schema for business intelligence.

This architecture provides a scalable, governed, and maintainable foundation for real-time monitoring and historical analytics while remaining aligned with Microsoft Fabric best practices.
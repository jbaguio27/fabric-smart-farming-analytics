# Architecture Decisions

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

This document captures the major architectural decisions made during the design of the Microsoft Fabric Smart Farming Analytics Platform.

Each Architecture Decision (AD) records:

- The business requirement
- The selected solution
- Alternative approaches
- Tradeoffs
- Enterprise rationale

Maintaining architectural decisions improves project traceability, supports future enhancements, and provides a clear understanding of why specific technologies and design patterns were selected.

---

# AD-001: Microsoft Fabric as the Unified Analytics Platform

## Decision

Use Microsoft Fabric as the primary analytics platform for both real-time and historical analytics.

## Business Driver

HydroGrow Solutions requires a unified platform capable of supporting:

- Real-time telemetry ingestion
- Historical analytics
- Centralized storage
- SQL analytics
- Business intelligence
- Real-time alerting
- Minimal operational overhead

## Alternatives Considered

| Alternative | Reason Not Selected |
|-------------|---------------------|
| Azure Synapse + Azure Data Explorer | Requires managing multiple Azure services |
| Databricks + Delta Lake | Excellent engineering platform but requires additional services for real-time intelligence |
| AWS Analytics Stack | Does not align with the organization's Microsoft ecosystem |
| Snowflake | Strong warehousing capabilities but limited native real-time event analytics |

## Rationale

Microsoft Fabric provides a unified Software-as-a-Service platform that integrates:

- Eventstream
- Eventhouse
- KQL Database
- OneLake
- Lakehouse
- Warehouse
- Power BI
- Data Activator

This reduces integration complexity while simplifying governance and administration.

## Tradeoffs

### Advantages

- Unified governance
- Native service integration
- Reduced infrastructure management
- Faster development

### Disadvantages

- Vendor lock-in
- Some Fabric capabilities continue to evolve
- Less flexibility than assembling best-of-breed services

---

# AD-002: Event-Driven Architecture

## Decision

Adopt an event-driven architecture for telemetry processing.

## Business Driver

IoT devices continuously generate telemetry that must be processed immediately to detect operational issues.

## Alternatives Considered

| Alternative | Reason Not Selected |
|-------------|---------------------|
| Scheduled batch processing | High detection latency |
| Micro-batch processing | Still introduces processing delay |
| Event-driven streaming | Selected |

## Rationale

An event-driven architecture processes telemetry immediately after generation, allowing the platform to detect failures within seconds rather than hours.

## Tradeoffs

### Advantages

- Near real-time processing
- High scalability
- Loose coupling
- Supports event replay

### Disadvantages

- More complex architecture
- Duplicate event handling required
- Event ordering considerations

---

# AD-003: Canonical Event Envelope

## Decision

All event types will follow a common canonical event envelope.

## Business Driver

The platform receives telemetry from multiple sensor types, equipment types, and operational systems.

A standardized event structure simplifies ingestion, validation, routing, monitoring, and future expansion.

## Standard Metadata

Every event contains:

- event_id
- correlation_id
- schema_version
- event_timestamp
- ingestion_timestamp
- producer_id
- facility_id
- zone_id
- payload

## Alternatives Considered

### Device-specific event schemas

Each device publishes completely independent schemas.

### Reason Not Selected

Creates inconsistent ingestion logic and increases downstream complexity.

## Rationale

A canonical event model improves:

- Schema evolution
- Event routing
- Monitoring
- Data lineage
- Troubleshooting
- Data validation

## Tradeoffs

### Advantages

- Consistent architecture
- Easier downstream processing
- Simplified governance

### Disadvantages

- Slight increase in event size

---

# AD-004: Eventhouse as the Operational Streaming Platform

## Decision

All streaming telemetry lands in Eventhouse before being persisted into OneLake.

## Business Driver

The platform requires immediate querying and real-time alert generation.

## Alternatives Considered

| Alternative | Reason Not Selected |
|-------------|---------------------|
| Direct Lakehouse ingestion | Limited streaming query capabilities |
| Azure Event Hub + Azure Data Explorer | Outside the Fabric ecosystem |
| Eventhouse | Selected |

## Rationale

Eventhouse is designed for high-volume streaming workloads and provides:

- Low-latency ingestion
- Native KQL support
- Time-series analytics
- Integration with Eventstream
- Integration with Data Activator

## Tradeoffs

### Advantages

- Fast ingestion
- Native streaming analytics
- Excellent time-series performance

### Disadvantages

- Requires downstream persistence into OneLake

---

# AD-005: Medallion Architecture

## Decision

Historical analytics will follow the Bronze, Silver, and Gold Medallion Architecture.

## Business Driver

Separate raw telemetry from validated datasets and business-ready reporting models.

## Alternatives Considered

### Flat Data Lake

All datasets stored together.

### Reason Not Selected

Difficult to maintain data quality and lineage.

## Rationale

The Medallion Architecture supports:

- Incremental processing
- Data quality improvements
- Historical replay
- Governance
- Auditability

## Tradeoffs

### Advantages

- Clear processing stages
- Better governance
- Easier troubleshooting
- Supports reprocessing

### Disadvantages

- Additional storage
- More transformation pipelines

---

# AD-006: Kimball Dimensional Modeling

## Decision

Use a Kimball Star Schema in the Gold layer.

## Business Driver

Business users consume data primarily through SQL and Power BI dashboards.

## Alternatives Considered

| Alternative | Reason Not Selected |
|-------------|---------------------|
| Third Normal Form | Poor analytical query performance |
| Data Vault | Greater complexity than required |
| Kimball Star Schema | Selected |

## Rationale

Kimball provides:

- High query performance
- Simple business reporting
- Intuitive relationships
- Excellent Power BI compatibility

## Tradeoffs

### Advantages

- Easy for analysts
- Fast aggregations
- Mature methodology

### Disadvantages

- Additional ETL effort
- Slowly Changing Dimension management

---

# AD-007: Python-Based IoT Event Simulator

## Decision

Simulate enterprise IoT telemetry using Python and Faker.

## Business Driver

No production IoT devices are available during development.

## Alternatives Considered

- Static CSV files
- Public IoT datasets
- Manual event generation

## Rationale

Python allows configurable event generation with realistic timestamps, sensor values, equipment failures, and maintenance events.

## Tradeoffs

### Advantages

- Repeatable testing
- Easy expansion
- Supports multiple event types

### Disadvantages

- Cannot perfectly emulate real hardware behavior

---

# AD-008: Documentation-First Development

## Decision

Complete architecture and business documentation before implementation.

## Business Driver

Enterprise projects require stakeholder alignment before development begins.

## Rationale

Documentation-first development reduces implementation risk and creates a shared understanding of project objectives.

## Tradeoffs

### Advantages

- Clear project direction
- Easier onboarding
- Better maintainability
- Supports architecture reviews

### Disadvantages

- Longer planning phase

---

# AD-009: Separation of Streaming and Historical Storage

## Decision

Separate operational streaming storage from long-term analytical storage.

Real-time telemetry will first be stored in Eventhouse before curated data is persisted into OneLake Lakehouse.

## Business Driver

The platform has two distinct analytical workloads:

1. Operational monitoring requiring sub-minute latency.
2. Historical analytics requiring governed, curated datasets.

A single storage system cannot efficiently satisfy both workloads.

## Alternatives Considered

### Eventhouse as the only storage layer

#### Reason Not Selected

Although Eventhouse provides excellent streaming analytics, it is not intended to serve as the enterprise system of record for long-term analytical datasets.

### Lakehouse only

#### Reason Not Selected

Lakehouse provides excellent historical analytics but lacks the specialized streaming capabilities required for low-latency operational monitoring.

## Rationale

Separating streaming and analytical storage allows each platform component to specialize in its intended purpose.

### Eventhouse

Responsible for:

- High-speed event ingestion
- Streaming analytics
- Time-series queries
- Data Activator integration
- Operational monitoring

### Lakehouse

Responsible for:

- Long-term storage
- Medallion Architecture
- Historical analytics
- Spark transformations
- Data engineering workloads

### Warehouse

Responsible for:

- Dimensional models
- Business reporting
- SQL analytics
- Executive dashboards

This separation follows Microsoft's recommended architecture for combining Real-Time Intelligence with OneLake-based analytics.

## Tradeoffs

### Advantages

- Better workload isolation
- Faster operational queries
- Improved analytical performance
- Clear separation of responsibilities
- Easier long-term governance

### Disadvantages

- Additional data movement
- More orchestration between services
- Slight increase in storage costs

---

---

# AD-010: Dual Analytics Architecture

## Decision

Separate operational analytics from historical analytics by implementing two independent reporting paths.

Operational analytics will query streaming telemetry directly from Eventhouse using KQL, while historical reporting will consume curated datasets from the Microsoft Fabric Warehouse.

## Business Driver

HydroGrow Solutions requires two distinct analytical capabilities:

1. Real-time operational visibility for monitoring live environmental conditions and equipment health.
2. Historical business intelligence for long-term trend analysis, executive reporting, and strategic decision-making.

These workloads have different latency, storage, and query requirements.

## Alternatives Considered

### Single Power BI Dataset

Use one reporting model for both operational and historical analytics.

#### Reason Not Selected

A single reporting model would combine streaming and historical workloads, increasing complexity and potentially impacting performance for low-latency operational monitoring.

### Warehouse Only

Serve all dashboards from the Fabric Warehouse.

#### Reason Not Selected

Warehouse refresh cycles introduce unnecessary latency for operational monitoring and are not designed for second-level streaming analytics.

## Rationale

Separating operational and historical analytics allows each platform component to specialize in its intended purpose.

### Operational Analytics

Powered by:

- Eventhouse
- KQL Queries
- Power BI Real-Time Operations Dashboard
- Data Activator

Primary users:

- Operations Team
- Farm Managers

Primary objectives:

- Monitor live telemetry
- Detect equipment failures
- Visualize current environmental conditions
- Respond to critical alerts

### Historical Analytics

Powered by:

- OneLake Lakehouse
- Spark Notebooks
- Fabric Data Factory
- Fabric Warehouse
- Power BI Historical Dashboards

Primary users:

- Executives
- Business Analysts
- Operations Managers

Primary objectives:

- Historical trend analysis
- KPI reporting
- Facility performance comparison
- Executive decision support

This separation aligns with Microsoft Fabric best practices by isolating low-latency operational workloads from curated analytical reporting.

## Tradeoffs

### Advantages

- Clear separation of responsibilities
- Lower latency for operational monitoring
- Improved reporting performance
- Independent scaling of operational and analytical workloads
- Simpler dashboard design for different user groups

### Disadvantages

- Two Power BI semantic models
- Additional report maintenance
- Separate data sources for operational and historical reporting

---
# Summary of Architecture Decisions

| ID | Decision |
|----|----------|
| AD-001 | Microsoft Fabric as the Unified Analytics Platform |
| AD-002 | Event-Driven Architecture |
| AD-003 | Canonical Event Envelope |
| AD-004 | Eventhouse as the Operational Streaming Platform |
| AD-005 | Medallion Architecture |
| AD-006 | Kimball Dimensional Modeling |
| AD-007 | Python-Based IoT Event Simulator |
| AD-008 | Documentation-First Development |
| AD-009 | Separation of Streaming and Historical Storage |
| AD-010 | Dual Analytics Architecture |

---

# Architecture Review

The selected architecture aligns with enterprise data engineering best practices and Microsoft Fabric design recommendations.

The architecture prioritizes:

- Low-latency streaming analytics
- Reliable historical analytics
- Modular data processing
- Clear separation of concerns
- Governed data management
- Future scalability
- Operational maintainability

These decisions establish a strong architectural foundation for the remaining solution design documents and implementation phases.
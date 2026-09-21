# HydroGrow Platform Documentation

This directory contains the comprehensive technical, functional, architectural, and operational documentation for the **Microsoft Fabric Smart Farming Analytics Platform**.

---

## Documentation Catalog

### 1. Executive & Production Certifications
| Document | Description | Status |
| :--- | :--- | :--- |
| **[`PRODUCTION_SIGNOFF.md`](file:///c:/Users/iosep/Github%20Repositories/fabric-realtime-retail-monitoring/docs/PRODUCTION_SIGNOFF.md)** | Formal executive production sign-off, SLA certifications, and benchmark audit. | ✅ Certified |
| **[`reports/e2e_validation_report.md`](file:///c:/Users/iosep/Github%20Repositories/fabric-realtime-retail-monitoring/docs/reports/e2e_validation_report.md)** | Automated End-to-End multi-stream schema, quality, and latency SLA audit report. | ✅ Complete |
| **[`reports/finops_cost_optimization.md`](file:///c:/Users/iosep/Github%20Repositories/fabric-realtime-retail-monitoring/docs/reports/finops_cost_optimization.md)** | Microsoft Fabric Capacity Sizing (FT64 to F2048) and storage tiering savings model. | ✅ Complete |

---

### 2. Technical Architecture Blueprints
| Document | Description | Status |
| :--- | :--- | :--- |
| **[`architecture/microsoft-fabric-architecture.md`](file:///c:/Users/iosep/Github%20Repositories/fabric-realtime-retail-monitoring/docs/architecture/microsoft-fabric-architecture.md)** | End-to-end Microsoft Fabric SaaS Lakehouse and Real-Time Intelligence architecture. | ✅ Approved |
| **[`architecture/streaming-architecture.md`](file:///c:/Users/iosep/Github%20Repositories/fabric-realtime-retail-monitoring/docs/architecture/streaming-architecture.md)** | Real-time streaming pipeline (Eventstream ➔ Eventhouse KQL Database ➔ Reflex). | ✅ Approved |
| **[`architecture/medallion-architecture.md`](file:///c:/Users/iosep/Github%20Repositories/fabric-realtime-retail-monitoring/docs/architecture/medallion-architecture.md)** | OneLake Medallion Architecture (Bronze shortcuts, Silver PII masking, Gold Star Schema). | ✅ Approved |
| **[`architecture/batch-architecture.md`](file:///c:/Users/iosep/Github%20Repositories/fabric-realtime-retail-monitoring/docs/architecture/batch-architecture.md)** | Master batch orchestration pipelines, incremental micro-batch sync, and CDC merges. | ✅ Approved |
| **[`architecture/security-model.md`](file:///c:/Users/iosep/Github%20Repositories/fabric-realtime-retail-monitoring/docs/architecture/security-model.md)** | Regional Row-Level Security (RLS), Dynamic Data Masking (DDM), and RBAC governance. | ✅ Approved |
| **[`architecture/monitoring-strategy.md`](file:///c:/Users/iosep/Github%20Repositories/fabric-realtime-retail-monitoring/docs/architecture/monitoring-strategy.md)** | OpenTelemetry distributed tracing, `fact_dataops_pipeline_log`, and KQL dashboards. | ✅ Approved |
| **[`architecture/dead-letter-remediation-architecture.md`](file:///c:/Users/iosep/Github%20Repositories/fabric-realtime-retail-monitoring/docs/architecture/dead-letter-remediation-architecture.md)** | 5-worker automated DLQ isolation and self-healing remediation engine. | ✅ Approved |
| **[`architecture/cost-considerations.md`](file:///c:/Users/iosep/Github%20Repositories/fabric-realtime-retail-monitoring/docs/architecture/cost-considerations.md)** | FinOps capacity planning, 24-hr CU smoothing, and SKU right-sizing recommendations. | ✅ Approved |
| **[`architecture/data-retention.md`](file:///c:/Users/iosep/Github%20Repositories/fabric-realtime-retail-monitoring/docs/architecture/data-retention.md)** | Hot Cache (7-day NVMe) vs Cold Storage (30-day OneLake) lifecycle policies. | ✅ Approved |
| **[`architecture/telemetry-attribute-dictionary.md`](file:///c:/Users/iosep/Github%20Repositories/fabric-realtime-retail-monitoring/docs/architecture/telemetry-attribute-dictionary.md)** | Complete data dictionary for all 6 telemetry streams and domain entities. | ✅ Approved |
| **[`architecture/architecture-decisions.md`](file:///c:/Users/iosep/Github%20Repositories/fabric-realtime-retail-monitoring/docs/architecture/architecture-decisions.md)** | Architectural Decision Records (ADRs) and engineering trade-off evaluations. | ✅ Approved |

---

### 3. Operational Setup & Deployment Runbooks
| Document | Description | Status |
| :--- | :--- | :--- |
| **[`fabric/setup-guide.md`](file:///c:/Users/iosep/Github%20Repositories/fabric-realtime-retail-monitoring/docs/fabric/setup-guide.md)** | Step-by-step Fabric workspace provisioning, deployment pipelines, and environment setup. | ✅ Complete |
| **[`events/event-catalog.md`](file:///c:/Users/iosep/Github%20Repositories/fabric-realtime-retail-monitoring/docs/events/event-catalog.md)** | Canonical event catalog defining event types, schema versions, and targets. | ✅ Complete |
| **[`business/business-scenario.md`](file:///c:/Users/iosep/Github%20Repositories/fabric-realtime-retail-monitoring/docs/business/business-scenario.md)** | HydroGrow Solutions business scenario, operational challenges, and KPI matrices. | ✅ Complete |
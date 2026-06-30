# Non-Functional Requirements

## Purpose

This document defines the quality attributes, operational expectations, and engineering standards for the Microsoft Fabric Smart Farming Analytics Platform.

These requirements ensure the platform is reliable, secure, scalable, maintainable, and capable of supporting real-time operational monitoring across multiple smart farming facilities.

---

# Non-Functional Requirements

## NFR-001: Performance

### Description

The platform shall process and expose streaming telemetry with minimal latency to support near real-time operational decision making.

### Requirements

- End-to-end data latency shall not exceed **15 seconds**.
- Event ingestion shall support continuous streaming without interruption.
- Operational dashboards shall reflect new telemetry within the target latency.

### Success Metrics

- Average latency < 15 seconds
- Dashboard refresh within acceptable operational limits

---

## NFR-002: Scalability

### Description

The platform shall support business growth without requiring architectural redesign.

### Requirements

- Support expansion from **5** to **15** smart farming facilities.
- Support thousands of concurrent IoT sensors.
- Support increasing event throughput by adding new facilities.

### Success Metrics

- No event loss during peak ingestion
- Stable query performance as facilities increase

---

## NFR-003: Availability

### Description

The platform shall remain available for operational monitoring during business hours.

### Requirements

- Historical analytics services shall target **99.9% availability**.
- Streaming services shall automatically recover from transient failures where supported.
- Critical operational dashboards shall remain accessible.

### Success Metrics

- Platform availability ≥ 99.9%
- Minimal service interruptions

---

## NFR-004: Reliability

### Description

The platform shall reliably process telemetry without data corruption or loss.

### Requirements

- Streaming events shall preserve event timestamps.
- Failed processing attempts shall be logged.
- Retry mechanisms shall be implemented where supported.
- Duplicate processing shall be minimized.

### Success Metrics

- Zero intentional data loss
- Successful recovery from transient failures

---

## NFR-005: Data Quality

### Description

The platform shall validate telemetry before downstream consumption.

### Requirements

Incoming events shall be checked for:

- Missing values
- Invalid schema
- Duplicate records
- Out-of-range sensor values

### Success Metrics

- 100% of incoming events validated
- Invalid records flagged with data quality status

---

## NFR-006: Security

### Description

The platform shall protect organizational data through Microsoft Fabric security controls.

### Requirements

- Role-Based Access Control (RBAC)
- Least privilege access
- Secure configuration management
- Audit logging where supported

### Success Metrics

- Unauthorized access prevented
- Administrative actions traceable

---

## NFR-007: Maintainability

### Description

The solution shall be designed for long-term maintenance and future enhancement.

### Requirements

- Modular Python codebase
- Configuration-driven design
- Consistent documentation
- Version-controlled source code
- Conventional commit history

### Success Metrics

- New features can be added with minimal code changes
- Documentation remains synchronized with implementation

---

## NFR-008: Observability

### Description

The platform shall provide sufficient operational visibility for troubleshooting and monitoring.

### Requirements

The platform shall expose:

- Pipeline health
- Processing latency
- Event throughput
- Failed events
- Data quality metrics
- Processing logs

### Success Metrics

- Operational issues detectable within minutes
- Monitoring dashboards available

---

## NFR-009: Usability

### Description

Operational dashboards shall present information in a clear and actionable format.

### Requirements

Dashboards shall provide:

- Interactive filtering
- Consistent navigation
- Clearly labeled KPIs
- Accessible visualizations

### Success Metrics

- Users can identify critical issues quickly
- Dashboard navigation is intuitive

---

## NFR-010: Data Retention

### Description

Historical telemetry shall be retained to support reporting and trend analysis.

### Requirements

- Streaming data retained according to Eventhouse policies.
- Curated historical datasets retained within OneLake.
- Retention policies documented and consistently applied.

### Success Metrics

- Historical reports generated without data gaps
- Storage policies align with business requirements

---

## NFR-011: Disaster Recovery

### Description

The platform shall support recovery from failures affecting data processing components.

### Requirements

- Source data retained for replay where supported.
- Infrastructure configuration maintained in version control.
- Recovery procedures documented.

### Success Metrics

- Processing can resume after service interruptions
- Configuration can be recreated consistently

---

## NFR-012: Compliance

### Description

The platform shall follow organizational governance and documentation standards.

### Requirements

- Architecture documented.
- Data lineage maintained.
- Configuration version controlled.
- Development follows engineering standards.

### Success Metrics

- Project documentation remains current.
- Engineering practices consistently followed.

---

# Requirement Traceability

| Requirement | Primary Epic |
|-------------|--------------|
| NFR-001 | Streaming Platform |
| NFR-002 | Streaming Platform |
| NFR-003 | Eventhouse & KQL Database |
| NFR-004 | Monitoring & Observability |
| NFR-005 | Spark Engineering |
| NFR-006 | Security & Governance |
| NFR-007 | Repository & Development Environment |
| NFR-008 | Monitoring & Observability |
| NFR-009 | Power BI |
| NFR-010 | Lakehouse |
| NFR-011 | Deployment Pipelines |
| NFR-012 | Documentation |

---

# Assumptions

- Microsoft Fabric services are available in the deployment region.
- Network connectivity between simulated devices and Microsoft Fabric is reliable.
- Business stakeholders define acceptable environmental thresholds.
- Fabric capacities are appropriately sized for expected workloads.

---

# Constraints

- IoT devices are simulated using Python and Faker.
- External hardware integrations are outside Version 1.0 scope.
- Predictive machine learning is excluded from the initial release.
- Multi-region disaster recovery is outside the scope of this project.

---

# Requirement Prioritization (MoSCoW)

| Requirement | Priority |
|-------------|----------|
| NFR-001 Performance | Must Have |
| NFR-002 Scalability | Must Have |
| NFR-003 Availability | Must Have |
| NFR-004 Reliability | Must Have |
| NFR-005 Data Quality | Must Have |
| NFR-006 Security | Must Have |
| NFR-007 Maintainability | Must Have |
| NFR-008 Observability | Must Have |
| NFR-009 Usability | Should Have |
| NFR-010 Data Retention | Must Have |
| NFR-011 Disaster Recovery | Should Have |
| NFR-012 Compliance | Must Have |
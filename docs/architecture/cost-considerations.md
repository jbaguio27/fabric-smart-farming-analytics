# Cost Considerations

## Document Information

| Attribute | Value |
|-----------|--------|
| Project | Microsoft Fabric Smart Farming Analytics Platform |
| Company | HydroGrow Solutions |
| Epic | Epic 1 – Project Planning & Solution Architecture |
| Version | 1.0 |
| Status | Approved |
| Author | Joseph Baguio |
| Last Updated | 2026-07-09 |

---

# Purpose

This document describes the cost management strategy for the Microsoft Fabric Smart Farming Analytics Platform.

The objective is to design a solution that balances operational performance, scalability, and cost efficiency while supporting real-time analytics, historical reporting, and long-term data retention.

Although this project is implemented using the Microsoft Fabric Trial, the architecture is designed according to production deployment best practices.

---

# Scope

This document covers:

- Compute consumption
- Storage utilization
- Data processing frequency
- Warehouse usage
- Power BI refresh strategy
- Monitoring costs
- Data lifecycle management
- Capacity planning

---

# Cost Optimization Principles

The platform follows these principles to reduce operational costs.

- Process only incremental data.
- Separate streaming from batch workloads.
- Retain only necessary historical data.
- Archive inactive datasets.
- Optimize Delta tables regularly.
- Schedule compute only when required.
- Prevent duplicate processing.
- Monitor resource utilization continuously.

---

# Major Cost Drivers

## Streaming Analytics

Components

- Eventstream
- Eventhouse
- Data Activator

Primary Cost Drivers

- Event ingestion rate
- Streaming throughput
- Query frequency
- Alert evaluation

Optimization Strategy

- Filter unnecessary telemetry.
- Publish only business-relevant events.
- Minimize expensive KQL queries.
- Aggregate streaming metrics where possible.

---

## OneLake Storage

Components

- Bronze
- Silver
- Gold
- Quarantine

Primary Cost Drivers

- Data volume
- Historical retention
- Duplicate records
- Small file generation

Optimization Strategy

- Delta OPTIMIZE
- Delta VACUUM
- Partition by date
- Automatic retention policies
- Quarantine cleanup after retention period
- Separate entity and telemetry datasets to reduce duplicated storage.

---

## Spark Processing

Components

- Bronze → Silver Notebook
- Silver → Gold Notebook

Primary Cost Drivers

- Notebook runtime
- Data volume
- Cluster execution
- Transformation complexity

Optimization Strategy

- Incremental processing
- Predicate pushdown
- Partition pruning
- Efficient Spark transformations
- Avoid full table processing

---

## Fabric Data Factory

Components

- Pipeline 1
- Pipeline 2

Primary Cost Drivers

- Pipeline executions
- Activity count
- Retry frequency

Optimization Strategy

- Execute every 15 minutes.
- Retry only transient failures.
- Modular orchestration.
- Trigger Pipeline 2 only after Pipeline 1 succeeds.

---

## Fabric Warehouse

Components

- Star Schema
- Fact Tables
- Dimension Tables

Primary Cost Drivers

- MERGE operations
- SQL queries
- Historical storage
- Concurrent reporting

Optimization Strategy

- Incremental MERGE
- SCD Type 2 only where required
- Separate dimensions from fact tables
- Partition large fact tables
- Optimize warehouse statistics

---

## Power BI

Components

- Historical Dashboards
- Executive Reports
- Semantic Models

Primary Cost Drivers

- Dataset refresh
- Query complexity
- Concurrent users

Optimization Strategy

- Scheduled refresh
- Reuse semantic models
- Optimize report visuals
- Reduce unnecessary calculations

---

# Data Lifecycle Cost Strategy

| Layer | Retention | Cost Strategy |
|--------|-----------|---------------|
| Eventhouse | 7 Days | Operational analytics only |
| Bronze | 12 Months | Immutable historical storage |
| Silver | 12 Months | Curated analytical history |
| Gold | 24 Months | Business-ready reporting datasets |
| Quarantine | 90 Days | Investigation and replay only |
| Warehouse | 5 Years | Long-term enterprise reporting |
| Archive | Beyond 5 Years | Compressed cold storage |

---

# Compute Scheduling Strategy

| Workload | Execution Strategy |
|----------|-------------------|
| Streaming Analytics | Continuous |
| Pipeline 1 | Every 15 minutes |
| Pipeline 2 | Triggered after Pipeline 1 |
| Semantic Model Refresh | After Warehouse publishing |
| Dashboard Refresh | Scheduled |
| Delta OPTIMIZE | Weekly |
| Delta VACUUM | Weekly |
| Archive Pipeline | Monthly |

---

# Cost Monitoring

The platform continuously monitors resource utilization using Microsoft Fabric Monitoring Hub and the Platform Monitoring Dashboard.

Key metrics include:

- Capacity utilization
- Spark notebook duration
- Pipeline execution duration
- Eventstream throughput
- Warehouse MERGE duration
- Storage growth
- Power BI refresh duration
- Data quality trends

Monitoring these metrics helps identify inefficient workloads before they increase operational costs.

---

# Cost Optimization Techniques

## Incremental Processing

Only new or modified records are processed during each execution cycle.

Benefits

- Reduced compute usage
- Faster execution
- Lower operational cost

---

## Medallion Architecture

Each layer has a dedicated responsibility.

Benefits

- Prevents unnecessary recomputation
- Improves data reuse
- Simplifies maintenance

---

## SCD Type 2 Dimensions

Historical tracking is applied only to dimensions requiring change history.

Benefits

- Reduces storage growth
- Preserves business history
- Improves reporting accuracy

---

## Persistent Business Entities

Static business metadata is stored once within dimension tables while telemetry facts reference those entities using surrogate keys.

Benefits

- Reduced telemetry payload size
- Lower storage consumption
- Improved compression
- Simplified schema evolution
- Reduced data duplication

---

## Delta Lake Maintenance

Scheduled maintenance includes:

- Delta OPTIMIZE
- Delta VACUUM
- File compaction
- Statistics updates

Benefits

- Faster queries
- Reduced storage fragmentation
- Lower processing costs

---

## Automated Data Retention

Retention policies automatically archive or remove obsolete data.

Benefits

- Controls storage growth
- Improves query performance
- Reduces long-term storage costs

---

# Trial Environment

This project is implemented using the Microsoft Fabric Trial.

The trial supports implementation of:

- Eventstream
- Eventhouse
- OneLake Lakehouse
- Spark Notebooks
- Fabric Data Factory
- Fabric Warehouse
- Power BI
- Semantic Models
- Monitoring Hub

Production deployments may require additional Fabric Capacity based on:

- Number of users
- Telemetry volume
- Refresh frequency
- Storage growth
- Concurrent workloads

---

# Best Practices

The solution follows these cost management best practices.

- Process data incrementally.
- Avoid unnecessary full refreshes.
- Archive historical data.
- Partition large datasets.
- Optimize Delta tables regularly.
- Monitor storage growth.
- Schedule workloads appropriately.
- Reuse semantic models.
- Continuously monitor platform utilization.

---

# Relationship to Other Documents

| Document | Responsibility |
|----------|----------------|
| Microsoft Fabric Architecture | Overall solution architecture |
| Batch Architecture | Scheduled processing |
| Monitoring Strategy | Platform monitoring |
| Data Retention Strategy | Data lifecycle management |
| Dashboard Requirements | Reporting workloads |

---

# Summary

The Microsoft Fabric Smart Farming Analytics Platform is designed to provide enterprise-scale analytics while maintaining efficient resource utilization.

By combining incremental processing, the Medallion Architecture, scheduled orchestration, automated retention policies, Delta Lake maintenance, and continuous monitoring, the platform minimizes compute and storage costs without compromising performance, scalability, or governance.

The architecture is suitable for implementation in both Microsoft Fabric Trial environments and production Fabric capacities with minimal design changes.
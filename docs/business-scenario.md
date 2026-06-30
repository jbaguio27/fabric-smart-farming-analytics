# Business Scenario

## Project Overview

HydroGrow Solutions is a rapidly growing indoor vertical farming company operating multiple automated facilities across major urban centers. Each facility uses thousands of IoT sensors to continuously monitor environmental conditions, crop health, and equipment performance across vertically stacked growing systems.

To support sustainable operations and maximize crop yield, HydroGrow requires a centralized analytics platform capable of processing high-volume telemetry in near real time while maintaining a historical analytics platform for reporting, trend analysis, and future forecasting.

This project demonstrates how Microsoft Fabric can be used to build a production-style Industrial IoT analytics platform that combines streaming data, operational intelligence, and historical analytics within a unified architecture.

---

## Company Background

HydroGrow Solutions currently operates five automated indoor farming facilities with plans to expand to fifteen facilities over the coming years.

Each facility continuously produces telemetry from environmental sensors and mechanical equipment, including:

- Water pH
- Electrical conductivity (EC)
- Dissolved oxygen
- Water temperature
- Ambient temperature
- Humidity
- Light intensity
- Pump performance
- Energy consumption

These measurements are essential for maintaining optimal growing conditions, reducing equipment downtime, and maximizing crop yield.

---

## Business Problem

HydroGrow currently relies on isolated monitoring systems and batch data processing that refreshes operational data only once every 24 hours.

Operations teams manually review facility dashboards during scheduled shifts, creating long delays between an environmental incident and corrective action.

Critical failures such as pump malfunctions, abnormal pH levels, HVAC failures, lighting outages, or faulty sensors may remain undetected for several hours, resulting in crop damage, increased operating costs, and reduced production efficiency.

Additionally, telemetry data is fragmented across multiple local systems, limiting enterprise-wide visibility and making historical reporting difficult.

---

## Business Goals

The Smart Farming Analytics Platform aims to:

- Centralize telemetry from all farming facilities into a single analytics platform.
- Reduce operational visibility latency from hours to seconds.
- Detect environmental anomalies before crops are affected.
- Improve equipment monitoring and preventive maintenance.
- Provide enterprise-wide operational dashboards.
- Build a trusted historical analytics platform for reporting and forecasting.
- Support future expansion without redesigning the analytics platform.

---

## Proposed Solution

The proposed solution leverages Microsoft Fabric to build an end-to-end Industrial IoT analytics platform.

The platform will:

- Ingest streaming telemetry using Microsoft Fabric Eventstream.
- Process and analyze streaming events within Eventhouse and KQL Database.
- Validate incoming telemetry to identify missing, duplicated, or invalid sensor readings.
- Generate real-time operational alerts using Data Activator.
- Store historical telemetry in OneLake using a Medallion Architecture.
- Transform curated datasets into a Kimball star schema for analytical reporting.
- Deliver executive and operational dashboards through Power BI.

---

## Expected Business Outcomes

The completed platform is expected to:

- Reduce end-to-end telemetry visibility to less than 15 seconds.
- Detect environmental anomalies before crop damage occurs.
- Improve operational response through automated alerting.
- Increase confidence in historical reporting through automated data quality validation.
- Provide a unified operational view across all farming facilities.
- Support future machine learning and predictive analytics initiatives using trusted historical data.

---

## Success Metrics

| Metric | Target |
|----------|---------|
| End-to-End Data Latency | < 15 seconds |
| Crop Loss Reduction | 95% |
| Alert True Positive Rate | ≥ 99.5% |
| Data Quality Validation | 100% of incoming events validated |
| Facility Scalability | 5 to 15 facilities |
| Historical Data Availability | ≥ 99.9% |
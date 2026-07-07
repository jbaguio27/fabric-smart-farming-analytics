# Business Scenario

## Project Overview

HydroGrow Solutions is a rapidly growing indoor vertical farming company operating multiple automated facilities across major urban centers. Each facility uses thousands of IoT sensors to continuously monitor environmental conditions, crop health, and equipment performance across vertically stacked growing systems.

To support sustainable operations and maximize crop yield, HydroGrow requires a centralized analytics platform capable of processing high-volume telemetry in near real time while maintaining a trusted historical analytics platform for reporting, trend analysis, executive decision-making, and future forecasting.

The solution combines Microsoft Fabric Real-Time Intelligence for operational monitoring with OneLake and Fabric Warehouse for governed historical analytics within a unified cloud-native platform.

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
- Provide real-time operational dashboards for farm monitoring and historical executive dashboards for business reporting.
- Build a trusted historical analytics platform for reporting and forecasting.
- Support future expansion without redesigning the analytics platform.

---

## Proposed Solution

The proposed solution leverages Microsoft Fabric to build an end-to-end Industrial IoT analytics platform.

The platform will:

- Ingest streaming telemetry using Microsoft Fabric Eventstream.
- Process streaming telemetry within Eventhouse using KQL for operational analytics.
- Power a real-time operations dashboard directly from Eventhouse for live facility monitoring.
- Generate real-time operational alerts using Data Activator.
- Continuously persist streaming telemetry into the OneLake Lakehouse Bronze layer.
- Transform historical data through the Medallion Architecture using Spark Notebooks.
- Load curated Gold datasets into the Fabric Warehouse using Fabric Data Factory pipelines.
- Deliver historical business intelligence and executive reporting through Power BI.

---

## Expected Business Outcomes

The completed platform is expected to:

- Reduce end-to-end telemetry visibility to less than 15 seconds.
- Detect environmental anomalies before crop damage occurs.
- Improve operational response through automated alerting.
- Increase confidence in historical reporting through automated data quality validation.
- Provide real-time operational visibility across all farming facilities.
- Deliver trusted historical analytics for executive reporting and long-term trend analysis.
- Support future machine learning and predictive analytics initiatives using trusted historical data.

---

## Success Metrics

| Metric | Target |
|----------|---------|
| End-to-End Data Latency | < 15 seconds |
| Real-Time Dashboard Refresh | < 15 seconds |
| Crop Loss Reduction | 95% |
| Alert True Positive Rate | ≥ 99.5% |
| Data Quality Validation | 100% of incoming events validated |
| Facility Scalability | 5 to 15 facilities |
| Historical Data Availability | ≥ 99.9% |
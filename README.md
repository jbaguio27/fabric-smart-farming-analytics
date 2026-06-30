# Microsoft Fabric: Smart Farming Analytics Platform

> A production-style Industrial IoT analytics platform built with Microsoft Fabric for real-time environmental monitoring, equipment health, historical analytics, and operational intelligence in a smart farming environment.

## Project Status

🚧 In Progress

---

# Project Overview

This project demonstrates how to build an enterprise-grade streaming analytics platform using Microsoft Fabric.

The platform simulates a nationwide indoor vertical farming company operating multiple smart farming facilities. Thousands of simulated IoT sensors continuously generate environmental, equipment, and operational telemetry, enabling real-time monitoring and historical analytics.

Streaming telemetry is ingested into Microsoft Fabric using Eventstream and analyzed in near real time through Eventhouse and KQL Database. Historical data is curated through a Medallion Architecture in OneLake and modeled into a Kimball star schema for reporting, trend analysis, and future forecasting.

This project follows production engineering practices, including modular Python development, configuration management, logging, data quality validation, monitoring, CI/CD, GitHub integration, and Dev, Test, and Production deployment workflows.

---

# Business Problem

HydroGrow Solutions operates multiple indoor vertical farming facilities where crop health depends on continuous monitoring of environmental conditions and equipment performance.

Current operations rely on delayed batch processing and manual monitoring, making it difficult to detect critical issues before crop quality is affected.

Examples include:

- Rapid pH fluctuations
- Water pump failures
- HVAC malfunctions
- LED lighting failures
- Abnormal humidity
- Sensor outages
- Equipment degradation

Delayed detection can result in crop loss, increased operating costs, and reduced production efficiency.

The goal of this platform is to provide operational teams with near real-time visibility into facility health while maintaining a historical analytics platform for long-term optimization and forecasting.

---

# Project Objectives

- Build a production-style streaming analytics platform using Microsoft Fabric
- Simulate enterprise-scale IoT telemetry using Python and Faker
- Implement Microsoft Fabric Eventstream for real-time ingestion
- Perform operational analytics using Eventhouse and KQL Database
- Build a Medallion Architecture in OneLake
- Design a Kimball star schema for historical reporting
- Implement Spark-based data transformation and validation
- Deliver operational dashboards with Power BI
- Trigger real-time alerts using Data Activator
- Apply production engineering practices including logging, monitoring, testing, and CI/CD

---

# Planned Architecture

Architecture diagrams and design documentation will be added throughout the project.

The final solution will include:

- Python Smart Farm Simulator
- Microsoft Fabric Eventstream
- Eventhouse
- KQL Database
- Lakehouse (Bronze, Silver, Gold)
- Spark Notebooks
- Warehouse
- Power BI
- Data Activator
- Fabric Data Factory
- Deployment Pipelines

---

# Technology Stack

| Category | Technology |
|-----------|------------|
| Event Simulation | Python, Faker |
| Streaming | Eventstream |
| Real-Time Storage | Eventhouse |
| Real-Time Analytics | KQL Database |
| Historical Storage | Lakehouse (OneLake) |
| Data Processing | Spark Notebooks |
| SQL Analytics | Warehouse |
| Orchestration | Fabric Data Factory |
| Reporting | Power BI |
| Alerts | Data Activator |
| Version Control | Git, GitHub |
| Development | VS Code |

---

# Repository Structure

```text
(To be updated as the project progresses.)
```

---

# Development Roadmap

- Repository & Development Environment
- Project Planning & Solution Architecture
- Smart Farm Event Simulator
- Real-Time Streaming Platform
- Eventhouse & KQL Database
- Operational Intelligence
- Lakehouse (Bronze, Silver, Gold)
- Spark Data Engineering
- Warehouse & Dimensional Modeling
- Power BI Dashboards
- Data Activator
- Monitoring & Observability
- Security & Governance
- Deployment Pipelines
- CI/CD
- Documentation
- Portfolio Completion

---

# Engineering Principles

This project follows production engineering practices rather than a tutorial-based implementation.

Key principles include:

- Event-driven architecture
- Medallion Architecture
- Kimball dimensional modeling
- Modular Python development
- Configuration management
- Logging and monitoring
- Data quality validation
- Infrastructure documentation
- Git feature branch workflow
- Conventional commits
- Dev, Test, and Production environments

---

# License

MIT License

Copyright (c) 2026 Joseph Baguio

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
# Microsoft Fabric Real-Time Retail Order Monitoring Platform

> A production-style real-time analytics platform built with Microsoft Fabric to monitor retail orders, payments, inventory, and shipments using streaming data.

## Project Status

🚧 In Progress

## Project Overview

This project demonstrates how to build an enterprise-grade real-time analytics platform using Microsoft Fabric. It simulates a retail company that needs to monitor orders and operational events as they happen.

The solution combines real-time streaming with historical analytics by using Eventstream, Eventhouse, KQL Database, Lakehouse, Spark, Warehouse, and Power BI.

## Business Problem

Retail businesses need immediate visibility into operational events such as:

- Incoming orders
- Failed payments
- Inventory shortages
- Shipping delays
- Refunds
- Order cancellations

Traditional batch ETL introduces delays. This platform enables operations teams to monitor these events in near real time.

## Project Objectives

- Build a production-style streaming architecture
- Demonstrate Microsoft Fabric Real-Time Intelligence
- Implement Medallion Architecture
- Support both real-time and historical analytics
- Apply engineering best practices
- Implement monitoring, logging, and data validation
- Demonstrate Dev, Test, and Production deployment

## Planned Architecture

Architecture diagram coming soon.

## Technology Stack

| Category | Technology |
|-----------|------------|
| Streaming | Eventstream |
| Real-Time Storage | Eventhouse |
| Analytics | KQL Database |
| Historical Storage | Lakehouse |
| Batch Processing | Spark |
| SQL Analytics | Warehouse |
| Orchestration | Fabric Data Factory |
| Reporting | Power BI |
| Alerts | Data Activator |
| Version Control | Git + GitHub |
| Development | VS Code + Python |

## Repository Structure

```text
(To be updated during development)
```

## Development Roadmap

- Repository Setup
- Project Planning
- Retail Event Simulator
- Eventstream
- Eventhouse
- KQL Analytics
- Lakehouse
- Spark Transformations
- Warehouse
- Power BI
- Monitoring
- Deployment Pipeline

## License

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

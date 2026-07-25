# Microsoft Fabric Smart Farming Analytics Platform

## Step 1: Streaming Platform Architecture (Eventstream)

The **HydroGrow Smart Farming Analytics Platform** ingests real-time IoT telemetry from 8 Philippine vertical farming facilities (`FAC-001` through `FAC-008`) into Microsoft Fabric via **Fabric Eventstream**.

---

### 1. Ingestion Endpoint & Authentication

- **Ingestion Mode**: Custom App Source (`PythonIoTSimulator`)
- **Protocol**: Azure Event Hubs / AMQP over HTTPS REST POST
- **Authentication**: Shared Access Signature (SAS Token)
- **Environment Variables (`.env`)**:
  ```env
  CONNECTION_STR=Endpoint=sb://es-xxxxxxxx.servicebus.windows.net/;SharedAccessKeyName=key_xxxxxxxx;SharedAccessKey=xxxxxxxx=
  EVENTHUB_NAME=es_xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
  ENABLE_INGESTION_ANOMALIES=true
  ```

---

### 2. Multi-Stream SQL Routing Topology (9 Nodes)

Telemetry events are routed asynchronously based on `event_type` to their designated KQL database tables:

| Stream Name | Transformation SQL Condition (`WHERE`) | Target KQL Table |
| :--- | :--- | :--- |
| **Environmental** | `event_type = 'environmental.telemetry'` | `EnvironmentalTelemetry` |
| **Equipment** | `event_type = 'equipment.telemetry'` | `EquipmentTelemetry` |
| **Crop Telemetry** | `event_type = 'crop.telemetry'` | `CropTelemetry` |
| **Crop Lifecycle** | `event_type = 'crop.lifecycle'` | `CropLifecycle` |
| **Irrigation** | `event_type = 'irrigation.telemetry'` | `IrrigationTelemetry` |
| **Lighting** | `event_type = 'lighting.telemetry'` | `LightingTelemetry` |
| **Maintenance** | `event_type = 'maintenance.event'` | `MaintenanceActivity` |
| **Facility Operations** | `event_type = 'facility.operations'` | `FacilityOperations` |
| **Dead-Letter Route** | `event_type = 'legacy.deprecated_sensor' OR facility_id IS NULL` | `DeadLetterTelemetry` |

---

### 3. Ingestion Metadata & Edge Filtering

Every SQL transformation node injects system ingestion metadata:
- **`IngestionTime`**: `System.Timestamp()` (captures exact Fabric ingress timestamp).
- **Edge Ingress Filter**: `WHERE facility_id IS NOT NULL AND timestamp IS NOT NULL`.

---

### 4. Ingestion SLA Benchmarks & Health Metrics

- **Average Processing Latency**: `< 1.5 seconds`
- **Ingestion Throughput**: `~60–80 events/sec` (`~55 MB/hour`)
- **Telemetry Latency Audit Query**:
  ```kql
  MaintenanceActivity
  | take 10
  | project timestamp, IngestionTime, LagSeconds = datetime_diff('second', IngestionTime, todatetime(timestamp)), facility_id
  ```
- **Dead-Letter Monitoring Function**:
  ```kql
  GetDeadLetterAnomalyRate(15)
  ```
"""
Data Anomaly Injector for Hydroponics Vertical Farming Telemetry.
This module provides the DataAnomalyInjector responsible for injecting raw
data quality defects (duplicate payloads, null values, type casting mismatches,
out-of-bounds outliers, PII data, and broken foreign keys) into JSON payloads
prior to Microsoft Fabric streaming ingestion.
"""

import random
import time
from typing import Final

class DataAnomalyInjector:
    """
    Injects realistic production raw data anomalies into telemetry event payloads
    to challenge downstream Microsoft Fabric PySpark data cleaning and validation pipelines.
    """

    def __init__(
        self,
        anomaly_rate: float = 0.15,
        enable_ingestion_anomalies: bool = False,
    ) -> None:
        """
        Initialize the DataAnomalyInjector.

        Args:
            anomaly_rate: Probability (0.0 to 1.0) of applying a random domain anomaly.
            enable_ingestion_anomalies: If True, injects low-rate (2%) structural ingestion defects.
        """

        self.anomaly_rate: Final[float] = anomaly_rate
        self.enable_ingestion_anomalies: Final[bool] = enable_ingestion_anomalies

    def inject_anomalies(
        self,
        payload: dict[str, object],
    ) -> list[dict[str, object]]:
        """
        Inject real-world raw data anomalies into a telemetry payload dictionary.

        Returns a list of payload dictionaries to support duplicate event burst generation.
        """
        if not isinstance(payload, dict):
            return [payload]

        dirty_payload = dict(payload)
        facility_id = str(dirty_payload.get("facility_id", "FAC-001")).lower()
        facility_phones = {
            "fac-001": "+639178452190",
            "fac-002": "+639183920411",
            "fac-003": "+639209518342",
            "fac-004": "+639284031955",
            "fac-005": "+639985721048",
            "fac-006": "+639082496103",
            "fac-007": "+639196308274",
            "fac-008": "+639271845920",
        }
        dirty_payload["operator_contact"] = f"tech.{facility_id}@smartfarm.ph"
        dirty_payload["operator_phone"] = facility_phones.get(facility_id, "+639178452190")

        # Controlled Structural Ingestion Anomaly Injection (Balanced Multi-Defect Distribution)
        if self.enable_ingestion_anomalies and random.random() <= 0.05:
            defect_type = random.choices(
                population=[
                    "missing_primary_key",
                    "out_of_bounds",
                    "deprecated_schema",
                    "serdes_parse",
                    "clock_skew",
                    "unregistered_mac",
                ],
                weights=[25, 20, 18, 15, 12, 10],
                k=1
            )[0]

            if defect_type == "missing_primary_key":
                dirty_payload["facility_id"] = None
                dirty_payload["exception_reason"] = "MISSING_PRIMARY_KEY: null facility_id"
            elif defect_type == "out_of_bounds":
                dirty_payload["operating_temperature_c"] = 99.5
                dirty_payload["sensor_value"] = 88.5
                dirty_payload["exception_reason"] = "OUT_OF_BOUNDS_SENSOR_VALUE: temperature > 65C"
            elif defect_type == "deprecated_schema":
                dirty_payload["event_type"] = "legacy.deprecated_sensor"
                dirty_payload["schema_version"] = "v1.0"
                dirty_payload["exception_reason"] = "DEPRECATED_SCHEMA_VERSION: v1.0 payload"
            elif defect_type == "serdes_parse":
                dirty_payload["raw_payload"] = "{malformed_json_bytes"
                dirty_payload["exception_reason"] = "SERDES_PARSE_FAILURE: malformed JSON payload"
            elif defect_type == "clock_skew":
                dirty_payload["timestamp"] = "2020-01-01T00:00:00Z"
                dirty_payload["exception_reason"] = "TIMESTAMP_OUT_OF_SYNC: clock skew > 24h"
            elif defect_type == "unregistered_mac":
                dirty_payload["equipment_id"] = "EQ-99999_ORPHAN"
                dirty_payload["mac_address"] = "00:00:00:00:00:00"
                dirty_payload["exception_reason"] = "UNREGISTERED_HARDWARE_MAC_ADDRESS: unregistered device"

            return [dirty_payload]

        # Balanced Regional Health Tier Anomaly Rate Adjuster:
        # - CRITICAL Tier (FAC-003 Manila, FAC-006 Cebu): High edge network defect rate (20.0%)
        # - DEGRADED Tier (FAC-004 Davao, FAC-005 Laguna, FAC-008 Iloilo): Moderate defect rate (10.0%)
        # - OPTIMAL Tier (FAC-001 Benguet, FAC-002 Tagaytay, FAC-007 Clark): Low defect rate (3.0%)
        if facility_id in ("fac-003", "fac-006"):
            effective_anomaly_rate = 0.20
        elif facility_id in ("fac-004", "fac-005", "fac-008"):
            effective_anomaly_rate = 0.10
        else:
            effective_anomaly_rate = 0.03

        # If random roll exceeds effective_anomaly_rate, return single enriched payload
        if random.random() > effective_anomaly_rate:
            return [dirty_payload]

        # Select a random anomaly pattern
        anomaly_type = random.choice([
            "deduplication",
            "missing_values",
            "format_standardization",
            "type_casting",
            "outliers",
            "integrity_constraint",
        ])

        if anomaly_type == "deduplication":
            # Deduplication Task: Return duplicate event bursts with identical IDs
            return [dirty_payload, dirty_payload]

        elif anomaly_type == "missing_values":
            # Handling missing values task: set string fields to None, "N/A", "Unknown", or ""
            target_key = random.choice(["operating_status", "unit", "zone_id", "equipment_type"])
            if target_key in dirty_payload:
                dirty_payload[target_key] = random.choice([None, "N/A", "Unknown", ""])
                dirty_payload["exception_reason"] = "MISSING_PRIMARY_KEY: null facility_id"

        elif anomaly_type == "format_standardization":
            # Format standardization task: lowercase casing & mixed unix epoch timestamps
            if "facility_id" in dirty_payload:
                dirty_payload["facility_id"] = str(dirty_payload["facility_id"]).lower()
            if "operating_status" in dirty_payload:
                dirty_payload["operating_status"] = random.choice(["online", "onlne", "WARNIN"])
            if "timestamp" in dirty_payload:
                dirty_payload["timestamp"] = str(int(time.time()))

        elif anomaly_type == "type_casting":
            # data type casting tasks: convert floats/ints to string and booleans to "Yes"/"Y"
            for temp_key in ["operating_temperature_c", "ambient_temperature_celsius", "sensor_value", "health", "current_load"]:
                if temp_key in dirty_payload and isinstance(dirty_payload[temp_key], (int, float)):
                    dirty_payload[temp_key] = str(dirty_payload[temp_key])
            if "is_active" in dirty_payload and isinstance(dirty_payload["is_active"], bool):
                dirty_payload["is_active"] = "Yes" if dirty_payload["is_active"] else "N"

        elif anomaly_type == "outliers":
            # handling outliers & value bounds tasks: system thermal spikes or negative values
            dirty_payload["exception_reason"] = "OUT_OF_BOUNDS_SENSOR_VALUE: temperature > 65C"
            if "water_ph" in dirty_payload:
                dirty_payload["water_ph"] = -999.0
            elif dirty_payload.get("sensor_type") == "water_ph" and dirty_payload.get("sensor_value") is not None:
                dirty_payload["sensor_value"] = -999.0
            elif "operating_temperature_c" in dirty_payload:
                dirty_payload["operating_temperature_c"] = 9999.99
            elif "ambient_temperature_celsius" in dirty_payload:
                dirty_payload["ambient_temperature_celsius"] = 9999.99
            elif dirty_payload.get("sensor_type") == "air_temperature" and dirty_payload.get("sensor_value") is not None:
                dirty_payload["sensor_value"] = 9999.99
            elif "current_load" in dirty_payload:
                dirty_payload["current_load"] = -50.0

        elif anomaly_type == "integrity_constraint":
            # Integrity constraints tasks: mismatched foreign key referencing non-existent asset
            dirty_payload["exception_reason"] = "UNREGISTERED_HARDWARE_MAC_ADDRESS: unregistered device"
            if "equipment_id" in dirty_payload:
                dirty_payload["equipment_id"] = "EQ-99999_ORPHAN"

        return [dirty_payload]                
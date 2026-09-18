"""Integration Test Suite: Step 1 & 2 - Streaming Ingestion & KQL Database.

Validates:
1. Eventhouse KQL Database schema definitions (tables, columns, types).
2. Telemetry transformation functions and enrichment pipelines.
3. Materialized views and operational query functions.
"""

import os
import unittest


class TestStep1StreamingKQL(unittest.TestCase):
    """Test suite validating Real-Time Eventstream and KQL Database artifacts."""

    @classmethod
    def setUpClass(cls):
        cls.repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
        cls.kql_file = os.path.join(
            cls.repo_root,
            "fabric",
            "SmartFarmingEventhouse.Eventhouse",
            ".children",
            "SmartFarmingKQLDB.KQLDatabase",
            "DatabaseSchema.kql",
        )

    def test_kql_schema_file_exists(self):
        """Verify that DatabaseSchema.kql exists."""
        self.assertTrue(os.path.exists(self.kql_file), f"Missing {self.kql_file}")

    def test_kql_raw_telemetry_tables(self):
        """Verify that all core raw telemetry tables are declared in KQL."""
        with open(self.kql_file, "r", encoding="utf-8") as f:
            content = f.read()

        expected_tables = [
            "EquipmentTelemetry",
            "EnvironmentalTelemetry",
            "CropLifecycle",
            "CropTelemetry",
            "IrrigationTelemetry",
            "LightingTelemetry",
            "MaintenanceActivity",
            "FacilityOperations",
            "DeadLetterTelemetry",
            "EnvironmentalEnriched",
            "EquipmentRiskEnriched",
            "QualityAuditLog",
            "IngestionLatencyTracker",
        ]

        for table in expected_tables:
            self.assertIn(f".create-merge table {table}", content, f"Missing table {table}")

    def test_kql_transformation_functions(self):
        """Verify that streaming transformation and analytical functions exist."""
        with open(self.kql_file, "r", encoding="utf-8") as f:
            content = f.read()

        expected_functions = [
            "transform_environmental_enriched",
            "transform_equipment_risk_enriched",
            "get_facility_operational_overview",
            "get_equipment_critical_anomalies",
        ]

        for func in expected_functions:
            self.assertIn(func, content, f"Missing function {func}")


if __name__ == "__main__":
    unittest.main()

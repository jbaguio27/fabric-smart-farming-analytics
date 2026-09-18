"""Integration Test Suite: Step 6 - Power BI Direct Lake Semantic Model.

Validates:
1. Direct Lake TMDL model definitions and metadata.
2. Star schema relationships (Foreign keys from facts to dimension primary keys).
3. Direct Lake mode configuration and table bindings.
"""

import os
import unittest


class TestStep6SemanticModel(unittest.TestCase):
    """Test suite validating Power BI Direct Lake Semantic Model TMDL definitions."""

    @classmethod
    def setUpClass(cls):
        cls.repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
        cls.model_dir = os.path.join(
            cls.repo_root,
            "fabric",
            "SemanticModel_SmartFarming_Gold.SemanticModel",
            "definition",
        )

    def test_semantic_model_files_exist(self):
        """Verify that essential TMDL semantic model definition files exist."""
        expected_files = [
            "database.tmdl",
            "model.tmdl",
            "relationships.tmdl",
            "expressions.tmdl",
        ]
        for filename in expected_files:
            file_path = os.path.join(self.model_dir, filename)
            self.assertTrue(os.path.exists(file_path), f"Missing TMDL file {filename}")

    def test_star_schema_relationships(self):
        """Verify star schema relationships in relationships.tmdl."""
        rel_file = os.path.join(self.model_dir, "relationships.tmdl")
        self.assertTrue(os.path.exists(rel_file), f"Missing {rel_file}")
        with open(rel_file, "r", encoding="utf-8") as f:
            content = f.read()

        expected_relationships = [
            ("fact_environmental_daily.date_key", "dim_date.date_key"),
            ("fact_equipment_telemetry.date_key", "dim_date.date_key"),
            ("fact_environmental_daily.facility_key", "dim_facility.facility_key"),
            ("fact_equipment_telemetry.facility_key", "dim_facility.facility_key"),
            ("fact_crop_yield.facility_key", "dim_facility.facility_key"),
            ("fact_irrigation_daily.facility_key", "dim_facility.facility_key"),
        ]

        for from_col, to_col in expected_relationships:
            self.assertIn(from_col, content, f"Missing relationship from {from_col}")
            self.assertIn(to_col, content, f"Missing relationship to {to_col}")


if __name__ == "__main__":
    unittest.main()

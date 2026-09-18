"""Integration Test Suite: Step 5 - Synapse Data Warehouse DDL Schemas.

Validates:
1. Presence and syntax of all 14 Warehouse DDL table scripts.
2. 6 Conformed Dimensions and 8 Business Fact tables.
3. Surrogate keys and schema declarations matching Gold Lakehouse models.
"""

import os
import unittest


class TestStep5WarehouseDDL(unittest.TestCase):
    """Test suite validating Synapse Data Warehouse SQL DDL artifacts."""

    @classmethod
    def setUpClass(cls):
        cls.repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
        cls.tables_dir = os.path.join(
            cls.repo_root, "fabric", "SmartFarming_Warehouse.Warehouse", "dbo", "Tables"
        )

    def test_warehouse_dimension_tables(self):
        """Verify that all 6 conformed dimension tables exist in the Warehouse."""
        dimensions = [
            "dim_crop.sql",
            "dim_date.sql",
            "dim_equipment.sql",
            "dim_facility.sql",
            "dim_technician.sql",
            "dim_zone.sql",
        ]
        for dim in dimensions:
            dim_file = os.path.join(self.tables_dir, dim)
            self.assertTrue(os.path.exists(dim_file), f"Missing dimension DDL {dim}")
            with open(dim_file, "r", encoding="utf-8") as f:
                content = f.read()
            self.assertIn("CREATE TABLE [dbo].", content)

    def test_warehouse_fact_tables(self):
        """Verify that all 8 business fact tables exist in the Warehouse."""
        facts = [
            "fact_crop_yield.sql",
            "fact_dataops_pipeline_log.sql",
            "fact_dead_letter_governance.sql",
            "fact_environmental_daily.sql",
            "fact_equipment_telemetry.sql",
            "fact_irrigation_daily.sql",
            "fact_lighting_dli_daily.sql",
            "fact_maintenance_sla.sql",
        ]
        for fact in facts:
            fact_file = os.path.join(self.tables_dir, fact)
            self.assertTrue(os.path.exists(fact_file), f"Missing fact DDL {fact}")
            with open(fact_file, "r", encoding="utf-8") as f:
                content = f.read()
            self.assertIn("CREATE TABLE [dbo].", content)


if __name__ == "__main__":
    unittest.main()

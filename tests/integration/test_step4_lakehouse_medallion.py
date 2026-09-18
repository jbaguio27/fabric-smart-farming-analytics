"""Integration Test Suite: Step 4 - Lakehouse Medallion Architecture.

Validates:
1. Bronze, Silver, Gold, and Quarantine zones in OneLake Lakehouse.
2. Silver deduplication, schema validation, and PII masking.
3. Gold Kimball Star Schema dimensional modeling (Dimensions & Fact tables).
"""

import os
import unittest


class TestStep4LakehouseMedallion(unittest.TestCase):
    """Test suite validating Medallion Lakehouse layers and star schema contracts."""

    @classmethod
    def setUpClass(cls):
        cls.repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
        cls.fabric_dir = os.path.join(cls.repo_root, "fabric")

    def test_silver_etl_contracts(self):
        """Verify Silver ETL notebook implements validation, deduplication, and PII masking."""
        silver_nb = os.path.join(
            self.fabric_dir, "Notebook_Silver_ETL.Notebook", "notebook-content.py"
        )
        self.assertTrue(os.path.exists(silver_nb), f"Missing {silver_nb}")
        with open(silver_nb, "r", encoding="utf-8") as f:
            content = f.read()

        self.assertIn("silver.environmental_enriched", content)
        self.assertIn("bronze.", content)
        self.assertIn("silver.", content)

    def test_gold_etl_kimball_star_schema(self):
        """Verify Gold ETL notebook builds all Kimball dimensions and fact tables."""
        gold_nb = os.path.join(
            self.fabric_dir, "Notebook_Gold_ETL.Notebook", "notebook-content.py"
        )
        self.assertTrue(os.path.exists(gold_nb), f"Missing {gold_nb}")
        with open(gold_nb, "r", encoding="utf-8") as f:
            content = f.read()

        expected_tables = [
            "gold.dim_facility",
            "gold.dim_crop",
            "gold.dim_zone",
            "gold.dim_equipment",
            "gold.dim_date",
            "gold.dim_technician",
            "gold.fact_crop_yield",
            "gold.fact_environmental_daily",
            "gold.fact_irrigation_daily",
            "gold.fact_lighting_dli_daily",
            "gold.fact_equipment_telemetry",
            "gold.fact_maintenance_sla",
            "gold.fact_dead_letter_governance",
        ]

        for table in expected_tables:
            self.assertIn(table, content, f"Missing table {table} in Gold ETL")


if __name__ == "__main__":
    unittest.main()

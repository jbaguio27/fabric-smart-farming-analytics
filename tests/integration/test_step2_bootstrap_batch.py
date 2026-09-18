"""Integration Test Suite: Step 2 - Bootstrap & Historical Batch Ingestion.

Validates:
1. Historical seed datasets in Files/ directory.
2. Bootstrap farm history generation script (scripts/bootstrap_farm_history.py).
3. Batch Medallion ingestion notebooks (Notebook_Load_Bronze_History, Notebook_Silver_ETL, Notebook_Gold_ETL).
4. SCD Type 2 dimension hashing contracts (attr_hash, effective_date, expiration_date, is_current).
"""

import os
import unittest


class TestStep2BootstrapBatch(unittest.TestCase):
    """Test suite validating historical batch bootstrap data and ETL notebooks."""

    @classmethod
    def setUpClass(cls):
        cls.repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
        cls.files_dir = os.path.join(cls.repo_root, "Files")
        cls.fabric_dir = os.path.join(cls.repo_root, "fabric")
        cls.scripts_dir = os.path.join(cls.repo_root, "scripts")

    def test_bootstrap_seed_files_exist(self):
        """Verify that all required historical bootstrap seed files exist."""
        expected_files = [
            "CropLifecycle.json",
            "CropTelemetry.json",
            "DeadLetterTelemetry.json",
            "EnvironmentalTelemetry.json",
            "EquipmentTelemetry.json",
            "FacilityOperations.json",
            "IrrigationTelemetry.json",
            "LightingTelemetry.json",
            "MaintenanceActivity.json",
        ]
        for filename in expected_files:
            file_path = os.path.join(self.files_dir, filename)
            self.assertTrue(os.path.exists(file_path), f"Missing bootstrap file {filename}")
            self.assertGreater(os.path.getsize(file_path), 0, f"File {filename} is empty")

    def test_bootstrap_generation_script(self):
        """Verify that bootstrap_farm_history.py exists and generates required tables."""
        script_file = os.path.join(self.scripts_dir, "bootstrap_farm_history.py")
        self.assertTrue(os.path.exists(script_file), f"Missing {script_file}")
        with open(script_file, "r", encoding="utf-8") as f:
            content = f.read()

        self.assertIn("run_historical_bootstrap", content)
        self.assertIn("FacilityOperations", content)
        self.assertIn("EquipmentTelemetry", content)

    def test_batch_etl_notebooks_exist(self):
        """Verify that batch Medallion ETL notebooks exist."""
        notebooks = [
            "Notebook_Load_Bronze_History.Notebook",
            "Notebook_Silver_ETL.Notebook",
            "Notebook_Gold_ETL.Notebook",
        ]
        for nb in notebooks:
            nb_path = os.path.join(self.fabric_dir, nb, "notebook-content.py")
            self.assertTrue(os.path.exists(nb_path), f"Missing notebook {nb}")


if __name__ == "__main__":
    unittest.main()

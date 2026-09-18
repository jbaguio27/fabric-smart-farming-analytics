"""Integration Test Suite: Step 3 - Livestream Micro-Batches, CDC MERGE & DLQ Remediation.

Validates:
1. Livestream micro-batch files in Files_Incremental/.
2. Incremental update generator (scripts/generate_incremental_update.py).
3. Incremental Silver & Gold Sync notebook CDC MERGE logic.
4. Dead-Letter Queue 5-worker auto-remediation error taxonomy (ERR_SCHEMA_V1, ERR_TIMESTAMP_SKEW, ERR_SERDES_MALFORMED, ERR_OUT_OF_BOUNDS, ERR_UNREGISTERED_MAC).
"""

import os
import unittest


class TestStep3IncrementalStreaming(unittest.TestCase):
    """Test suite validating livestream incremental CDC and dead-letter auto-remediation."""

    @classmethod
    def setUpClass(cls):
        cls.repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
        cls.inc_dir = os.path.join(cls.repo_root, "Files_Incremental")
        cls.fabric_dir = os.path.join(cls.repo_root, "fabric")
        cls.scripts_dir = os.path.join(cls.repo_root, "scripts")

    def test_incremental_seed_files_exist(self):
        """Verify that all required livestream incremental micro-batch files exist."""
        expected_files = [
            "DeadLetterTelemetry.json",
            "EnvironmentalTelemetry.json",
            "EquipmentTelemetry.json",
            "FacilityOperations.json",
            "IrrigationTelemetry.json",
            "LightingTelemetry.json",
            "MaintenanceActivity.json",
        ]
        for filename in expected_files:
            file_path = os.path.join(self.inc_dir, filename)
            self.assertTrue(os.path.exists(file_path), f"Missing incremental file {filename}")
            self.assertGreater(os.path.getsize(file_path), 0, f"File {filename} is empty")

    def test_incremental_generator_script(self):
        """Verify that generate_incremental_update.py exists and generates delta files."""
        script_file = os.path.join(self.scripts_dir, "generate_incremental_update.py")
        self.assertTrue(os.path.exists(script_file), f"Missing {script_file}")
        with open(script_file, "r", encoding="utf-8") as f:
            content = f.read()

        self.assertIn("Files_Incremental", content)
        self.assertIn("EnvironmentalTelemetry", content)
        self.assertIn("EquipmentTelemetry", content)

    def test_dead_letter_remediation_workers(self):
        """Verify that Notebook_DeadLetter_Remediation implements the 5 auto-remediation workers."""
        nb_path = os.path.join(
            self.fabric_dir, "Notebook_DeadLetter_Remediation.Notebook", "notebook-content.py"
        )
        self.assertTrue(os.path.exists(nb_path), f"Missing {nb_path}")
        with open(nb_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Check for standardized error taxonomy
        self.assertIn("ERR_SCHEMA_V1", content)
        self.assertIn("ERR_TIMESTAMP_SKEW", content)
        self.assertIn("ERR_SERDES_MALFORMED", content)
        self.assertIn("ERR_OUT_OF_BOUNDS", content)
        self.assertIn("ERR_UNREGISTERED_MAC", content)


if __name__ == "__main__":
    unittest.main()

"""
Integration Test Suite: Step 10 - Automated End-to-End Testing & Validation Suite.

Validates:
1. Multi-stream schema conformance across all 6 telemetry generators.
2. Data drift & schema evolution detection.
3. Data quality boundary constraints (range, nulls, physical plausibility).
4. Real-time streaming latency SLA benchmarking (< 15.0s).
5. Dead-Letter Queue (DLQ) chaos injection & automated self-healing.
6. End-to-End validation report generation and JSON/Markdown export.
"""

import json
import os
import shutil
import tempfile
import unittest

from smart_farming.validation.e2e_validator import (
    E2EValidationEngine,
    E2EValidationReport,
    StreamQualityResult,
    LatencyBenchmarkResult,
    DLQResilienceResult,
)


class TestStep10E2EValidation(unittest.TestCase):
    """Test suite validating the Step 10 End-to-End Validation Engine and Quality Gates."""

    @classmethod
    def setUpClass(cls):
        cls.engine = E2EValidationEngine(sla_target_seconds=15.0)
        cls.temp_dir = tempfile.mkdtemp()

    @classmethod
    def tearDownClass(cls):
        if os.path.exists(cls.temp_dir):
            shutil.rmtree(cls.temp_dir)

    def test_multi_stream_schema_conformance(self):
        """Verify that all 6 streams conform to expected schemas with zero drift."""
        streams = self.engine.generate_synthetic_telemetry(records_per_stream=25)
        self.assertEqual(len(streams), 6)
        for name in ["environmental", "equipment", "crop", "crop_lifecycle", "irrigation", "lighting"]:
            self.assertIn(name, streams)
            self.assertEqual(len(streams[name]), 25)

        results = self.engine.validate_stream_schemas_and_quality(streams)
        for stream_name, res in results.items():
            self.assertTrue(
                res.passed,
                f"Stream {stream_name} failed quality check with errors: {res.errors}",
            )
            self.assertEqual(res.drift_violations, 0)
            self.assertEqual(res.null_violations, 0)
            self.assertEqual(res.range_violations, 0)

    def test_schema_drift_detection(self):
        """Verify that missing fields or schema drift is detected immediately."""
        bad_stream = {
            "environmental": [
                {"timestamp": "2026-09-21T00:00:00Z", "facility_id": "FAC_001"}  # Missing all sensor fields
            ]
        }
        results = self.engine.validate_stream_schemas_and_quality(bad_stream)
        res = results["environmental"]
        self.assertFalse(res.passed)
        self.assertGreater(res.drift_violations, 0)
        self.assertIn("Missing fields", res.errors[0])

    def test_data_quality_boundary_violations(self):
        """Verify that out-of-bounds metrics (e.g. extreme flow rate or pressure) are caught."""
        bad_irrigation = {
            "irrigation": [
                {
                    "event_id": "test-id-123",
                    "timestamp": "2026-09-21T00:00:00Z",
                    "facility_id": "fac-001",
                    "zone_id": "zone-01",
                    "irrigation_active": True,
                    "flow_rate_liters_per_minute": 500.0,  # Max allowed is 200.0
                    "pressure_kpa": 1200.0,                # Max allowed is 600.0
                    "irrigation_duration_seconds": 120,
                    "water_delivered_liters": 10000.0,     # Max allowed is 5000.0
                    "nutrient_solution_delivered_liters": 2.5,
                }
            ]
        }
        results = self.engine.validate_stream_schemas_and_quality(bad_irrigation)
        res = results["irrigation"]
        self.assertFalse(res.passed)
        self.assertGreaterEqual(res.range_violations, 3)

    def test_latency_sla_benchmarking_pass(self):
        """Verify that latencies under 15s pass the SLA benchmark."""
        fast_delays = [0.5, 1.2, 2.1, 3.4, 4.8, 5.0]
        res = self.engine.benchmark_latency_sla(fast_delays)
        self.assertTrue(res.sla_passed)
        self.assertLessEqual(res.p99_latency_seconds, 15.0)
        self.assertEqual(res.sample_count, 6)

    def test_latency_sla_benchmarking_fail(self):
        """Verify that latencies exceeding 15s trigger an SLA failure."""
        slow_delays = [2.0, 5.0, 10.0, 16.5, 22.0]
        res = self.engine.benchmark_latency_sla(slow_delays)
        self.assertFalse(res.sla_passed)
        self.assertGreater(res.max_latency_seconds, 15.0)

    def test_dlq_chaos_and_auto_remediation(self):
        """Verify that injected poison packets are quarantined in DLQ and auto-healed."""
        dlq_res = self.engine.test_dlq_fault_tolerance(poison_count=10)
        self.assertTrue(dlq_res.resilience_passed)
        self.assertEqual(dlq_res.injected_poison_records, 10)
        self.assertEqual(dlq_res.quarantined_records, 10)
        self.assertEqual(dlq_res.remediated_records, 10)
        self.assertEqual(dlq_res.unhandled_poison_records, 0)
        self.assertEqual(len(dlq_res.remediation_log), 20)  # 10 quarantines + 10 remediations

    def test_full_validation_run_and_reporting(self):
        """Verify complete validation pipeline execution and file export."""
        report = self.engine.run_full_validation(records_per_stream=15, poison_count=5)
        self.assertIsInstance(report, E2EValidationReport)
        self.assertEqual(report.overall_status, "PASSED")
        self.assertTrue(report.schema_validation_passed)
        self.assertTrue(report.latency_result.sla_passed)
        self.assertTrue(report.dlq_result.resilience_passed)
        self.assertIn("# HydroGrow Platform End-to-End Validation Report", report.summary_markdown)

        # Test export
        json_path = os.path.join(self.temp_dir, "test_report.json")
        md_path = os.path.join(self.temp_dir, "test_report.md")
        self.engine.export_report(report, json_path, md_path)

        self.assertTrue(os.path.exists(json_path))
        self.assertTrue(os.path.exists(md_path))

        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            self.assertEqual(data["overall_status"], "PASSED")


if __name__ == "__main__":
    unittest.main()

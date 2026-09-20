"""
Integration Test Suite: Step 11 - Cost Optimization, Capacity Management & SLA Validation.

Validates:
1. Microsoft Fabric Trial (FT64) evaluation pricing ($0/mo) and compute equivalence.
2. Enterprise SKU catalog pricing (F2 to F2048) and Reserved Instance discounts.
3. Workload CU-second allocation and throttling resilience modeling.
4. Storage lifecycle tiering savings (KQL Hot Cache vs OneLake Cold Storage).
5. FinOps capacity report generation and export.
"""

import json
import os
import shutil
import tempfile
import unittest

from smart_farming.capacity.capacity_optimizer import (
    FabricCapacityOptimizer,
    CapacityCostReport,
    SKUProfile,
    WorkloadCUAllocation,
    StorageTieringReport,
)


class TestStep11CostCapacityOptimization(unittest.TestCase):
    """Test suite validating Step 11 FinOps capacity sizing and storage optimization."""

    @classmethod
    def setUpClass(cls):
        cls.optimizer = FabricCapacityOptimizer(default_sku="FT64")
        cls.temp_dir = tempfile.mkdtemp()

    @classmethod
    def tearDownClass(cls):
        if os.path.exists(cls.temp_dir):
            shutil.rmtree(cls.temp_dir)

    def test_trial_ft64_pricing_and_cu_bursting(self):
        """Verify that FT64 Trial provides 64 CUs at $0.00 cost with 3x bursting capacity."""
        cost = self.optimizer.calculate_compute_cost(sku_name="FT64", commitment="payg")
        self.assertEqual(cost["sku_name"], "FT64")
        self.assertEqual(cost["capacity_units"], 64)
        self.assertTrue(cost["is_trial"])
        self.assertEqual(cost["monthly_compute_cost_usd"], 0.00)
        self.assertEqual(cost["effective_hourly_rate_usd"], 0.00)

        profile = self.optimizer.FABRIC_SKU_CATALOG["FT64"]
        self.assertEqual(profile.max_burst_cu, 192)

    def test_payg_sku_pricing_catalog(self):
        """Verify that paid SKUs (F2 to F512) calculate base hourly rates accurately."""
        f64_cost = self.optimizer.calculate_compute_cost(sku_name="F64", commitment="payg")
        self.assertEqual(f64_cost["capacity_units"], 64)
        self.assertAlmostEqual(f64_cost["base_hourly_rate_usd"], 11.52)
        self.assertAlmostEqual(f64_cost["monthly_compute_cost_usd"], 11.52 * 730.0, places=1)

        f128_cost = self.optimizer.calculate_compute_cost(sku_name="F128", commitment="payg")
        self.assertEqual(f128_cost["capacity_units"], 128)
        self.assertAlmostEqual(f128_cost["base_hourly_rate_usd"], 23.04)

    def test_reserved_instance_commitment_discounts(self):
        """Verify that 1-year (40.5%) and 3-year (65%) Reserved Instance discounts apply."""
        payg = self.optimizer.calculate_compute_cost("F64", commitment="payg")
        ri_1yr = self.optimizer.calculate_compute_cost("F64", commitment="1yr")
        ri_3yr = self.optimizer.calculate_compute_cost("F64", commitment="3yr")

        self.assertAlmostEqual(ri_1yr["discount_pct"], 40.5)
        self.assertAlmostEqual(ri_3yr["discount_pct"], 65.0)

        expected_1yr_rate = 11.52 * (1.0 - 0.405)
        expected_3yr_rate = 11.52 * (1.0 - 0.650)
        self.assertAlmostEqual(ri_1yr["effective_hourly_rate_usd"], expected_1yr_rate, places=2)
        self.assertAlmostEqual(ri_3yr["effective_hourly_rate_usd"], expected_3yr_rate, places=2)

    def test_workload_cu_breakdown_and_throttling_risk(self):
        """Verify CU-second allocation across compute engines and safe utilization."""
        workload = self.optimizer.model_workload_cu_breakdown(
            events_per_day=500_000,
            spark_batch_runs_per_day=24,
            spark_avg_run_minutes=4.5,
            pipeline_activities_per_day=120,
            direct_lake_queries_per_day=1500,
            assigned_sku="FT64",
        )

        self.assertGreater(workload.total_cu_seconds_per_day, 0.0)
        self.assertGreater(workload.spark_etl_cu_seconds_per_day, 0.0)
        self.assertGreater(workload.kql_streaming_cu_seconds_per_day, 0.0)
        self.assertGreater(workload.data_pipeline_cu_seconds_per_day, 0.0)
        self.assertGreater(workload.direct_lake_cu_seconds_per_day, 0.0)

        # Average smoothed demand should stay well within 64 CU capacity (< 20% on FT64)
        self.assertLess(workload.throttling_risk_pct, 80.0)
        self.assertLess(workload.avg_cu_demand, 64.0)

    def test_storage_tiering_hot_cold_savings(self):
        """Verify that 7-day Hot / 30-day Cold storage tiering achieves > 60% savings."""
        storage = self.optimizer.calculate_storage_tiering_savings(
            total_raw_data_gb=300.0,
            hot_cache_days=7,
            total_retention_days=30,
        )

        self.assertEqual(storage.total_raw_data_gb, 300.0)
        self.assertEqual(storage.hot_cache_days, 7)
        self.assertEqual(storage.total_retention_days, 30)

        # Unoptimized (all hot @ $0.12/GB): 300 * 0.12 = $36.00
        self.assertAlmostEqual(storage.unoptimized_monthly_storage_usd, 36.00, places=2)

        # Tiered cost is significantly lower
        self.assertLess(storage.tiered_optimized_monthly_storage_usd, storage.unoptimized_monthly_storage_usd)
        self.assertGreater(storage.savings_percentage, 60.0)

    def test_finops_report_generation_and_export(self):
        """Verify full FinOps report generation, upgrade projections, and export."""
        report = self.optimizer.generate_capacity_report(
            sku_name="FT64",
            commitment="payg",
            events_per_day=250_000,
            total_storage_gb=100.0,
        )

        self.assertIsInstance(report, CapacityCostReport)
        self.assertEqual(report.selected_sku, "FT64")
        self.assertTrue(report.is_trial)
        self.assertIn("F64 (Pay-As-You-Go)", report.upgrade_projections)
        self.assertIn("F128 (1-Yr Reserved)", report.upgrade_projections)
        self.assertIn("# HydroGrow Platform - FinOps & Capacity Optimization Report", report.summary_markdown)

        # Export test
        json_path = os.path.join(self.temp_dir, "finops_test.json")
        md_path = os.path.join(self.temp_dir, "finops_test.md")
        self.optimizer.export_report(report, json_path, md_path)

        self.assertTrue(os.path.exists(json_path))
        self.assertTrue(os.path.exists(md_path))

        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            self.assertEqual(data["selected_sku"], "FT64")


if __name__ == "__main__":
    unittest.main()

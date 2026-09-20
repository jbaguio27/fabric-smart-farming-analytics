"""
FinOps & Capacity Optimization Engine for Microsoft Fabric.

Provides parameterized capacity sizing, workload CU-second distribution modeling,
storage lifecycle tiering analysis, and Trial-to-Enterprise upgrade projections.
"""

from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
import json
import logging
import os
import sys
from typing import Any, Dict, List, Optional

logger = logging.getLogger("smart_farming.capacity.capacity_optimizer")


@dataclass
class SKUProfile:
    """Specification and pricing profile for a Microsoft Fabric Capacity SKU."""
    sku_name: str
    capacity_units: int
    hourly_rate_usd: float
    is_trial: bool = False
    max_burst_cu: int = 0

    def __post_init__(self):
        if self.max_burst_cu == 0:
            # Fabric capacity allows bursting up to 3x-4x baseline depending on SKU tier
            self.max_burst_cu = self.capacity_units * 3


@dataclass
class WorkloadCUAllocation:
    """Breakdown of Capacity Unit (CU) consumption across Fabric compute engines."""
    spark_etl_cu_seconds_per_day: float = 0.0
    kql_streaming_cu_seconds_per_day: float = 0.0
    data_pipeline_cu_seconds_per_day: float = 0.0
    direct_lake_cu_seconds_per_day: float = 0.0
    total_cu_seconds_per_day: float = 0.0
    avg_cu_demand: float = 0.0
    peak_cu_demand: float = 0.0
    throttling_risk_pct: float = 0.0


@dataclass
class StorageTieringReport:
    """FinOps evaluation of storage lifecycle tiering and Delta optimizations."""
    total_raw_data_gb: float = 0.0
    hot_cache_days: int = 7
    total_retention_days: int = 30
    unoptimized_monthly_storage_usd: float = 0.0
    tiered_optimized_monthly_storage_usd: float = 0.0
    monthly_storage_savings_usd: float = 0.0
    savings_percentage: float = 0.0


@dataclass
class CapacityCostReport:
    """Comprehensive FinOps capacity management report."""
    evaluation_timestamp: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    selected_sku: str = "FT64"
    capacity_units: int = 64
    is_trial: bool = True
    commitment_tier: str = "payg"
    discount_pct: float = 0.0
    effective_hourly_rate_usd: float = 0.0
    monthly_compute_cost_usd: float = 0.0
    storage_report: StorageTieringReport = field(default_factory=StorageTieringReport)
    workload_cu: WorkloadCUAllocation = field(default_factory=WorkloadCUAllocation)
    total_monthly_run_rate_usd: float = 0.0
    upgrade_projections: Dict[str, float] = field(default_factory=dict)
    summary_markdown: str = ""

    def to_dict(self) -> Dict[str, Any]:
        """Serialize report to dictionary."""
        return asdict(self)


class FabricCapacityOptimizer:
    """
    Enterprise FinOps & Capacity Optimization Engine for Microsoft Fabric.
    
    Supports evaluation trials (FT64), standard pay-as-you-go, and 1-yr/3-yr
    reserved instances across F2 to F2048 SKUs.
    """

    # Hourly rates based on standard East US / Global commercial Fabric capacity pricing
    FABRIC_SKU_CATALOG: Dict[str, SKUProfile] = {
        "FT64": SKUProfile(sku_name="FT64", capacity_units=64, hourly_rate_usd=0.00, is_trial=True),
        "F2": SKUProfile(sku_name="F2", capacity_units=2, hourly_rate_usd=0.36),
        "F4": SKUProfile(sku_name="F4", capacity_units=4, hourly_rate_usd=0.72),
        "F8": SKUProfile(sku_name="F8", capacity_units=8, hourly_rate_usd=1.44),
        "F16": SKUProfile(sku_name="F16", capacity_units=16, hourly_rate_usd=2.88),
        "F32": SKUProfile(sku_name="F32", capacity_units=32, hourly_rate_usd=5.76),
        "F64": SKUProfile(sku_name="F64", capacity_units=64, hourly_rate_usd=11.52),
        "F128": SKUProfile(sku_name="F128", capacity_units=128, hourly_rate_usd=23.04),
        "F256": SKUProfile(sku_name="F256", capacity_units=256, hourly_rate_usd=46.08),
        "F512": SKUProfile(sku_name="F512", capacity_units=512, hourly_rate_usd=92.16),
        "F1024": SKUProfile(sku_name="F1024", capacity_units=1024, hourly_rate_usd=184.32),
        "F2048": SKUProfile(sku_name="F2048", capacity_units=2048, hourly_rate_usd=368.64),
    }

    COMMITMENT_DISCOUNTS: Dict[str, float] = {
        "payg": 0.0,       # Pay-As-You-Go (0% discount)
        "1yr": 0.405,      # 1-Year Reserved Instance (~40.5% discount)
        "3yr": 0.650,      # 3-Year Reserved Instance (~65.0% discount)
    }

    # Storage Unit Rates ($ / GB / Month)
    ONELAKE_STANDARD_STORAGE_PER_GB: float = 0.023
    KQL_HOT_CACHE_STORAGE_PER_GB: float = 0.120

    def __init__(self, default_sku: str = "FT64"):
        self.default_sku = default_sku.upper()
        if self.default_sku not in self.FABRIC_SKU_CATALOG:
            raise ValueError(
                f"Unknown SKU '{self.default_sku}'. Available SKUs: {list(self.FABRIC_SKU_CATALOG.keys())}"
            )

    def calculate_compute_cost(
        self,
        sku_name: str = "FT64",
        hours_per_month: float = 730.0,
        commitment: str = "payg",
    ) -> Dict[str, Any]:
        """Calculates monthly compute cost for a specified SKU and commitment tier."""
        sku_key = sku_name.upper()
        if sku_key not in self.FABRIC_SKU_CATALOG:
            raise ValueError(f"Invalid SKU '{sku_key}'")

        commitment_key = commitment.lower()
        if commitment_key not in self.COMMITMENT_DISCOUNTS:
            raise ValueError(f"Invalid commitment '{commitment_key}'. Use payg, 1yr, or 3yr.")

        sku = self.FABRIC_SKU_CATALOG[sku_key]
        discount = self.COMMITMENT_DISCOUNTS[commitment_key]

        if sku.is_trial:
            effective_rate = 0.00
            monthly_cost = 0.00
            discount = 0.00
        else:
            effective_rate = sku.hourly_rate_usd * (1.0 - discount)
            monthly_cost = effective_rate * hours_per_month

        return {
            "sku_name": sku.sku_name,
            "capacity_units": sku.capacity_units,
            "is_trial": sku.is_trial,
            "commitment_tier": commitment_key,
            "base_hourly_rate_usd": sku.hourly_rate_usd,
            "discount_pct": round(discount * 100.0, 1),
            "effective_hourly_rate_usd": round(effective_rate, 4),
            "monthly_compute_cost_usd": round(monthly_cost, 2),
        }

    def model_workload_cu_breakdown(
        self,
        events_per_day: int = 500_000,
        spark_batch_runs_per_day: int = 24,
        spark_avg_run_minutes: float = 4.5,
        pipeline_activities_per_day: int = 120,
        direct_lake_queries_per_day: int = 1500,
        assigned_sku: str = "FT64",
    ) -> WorkloadCUAllocation:
        """
        Models 24-hour CU-second consumption across Spark, KQL, Pipelines, and Direct Lake.
        Evaluates throttling risk under Fabric 24-hour background smoothing.
        """
        sku_key = assigned_sku.upper()
        sku = self.FABRIC_SKU_CATALOG.get(sku_key, self.FABRIC_SKU_CATALOG["FT64"])

        # 1. KQL Continuous Ingestion & Update Policies (~0.00015 CU-seconds per event)
        kql_cu_seconds = events_per_day * 0.00015

        # 2. Spark Batch Medallion ETL (Bronze -> Silver -> Gold):
        # 1 standard Fabric Spark node = 4 CUs. Run duration in seconds * node CUs.
        spark_node_cu = 4.0
        spark_cu_seconds = spark_batch_runs_per_day * (spark_avg_run_minutes * 60.0) * spark_node_cu

        # 3. Data Pipeline Activity Orchestration (~2.5 CU-seconds per activity)
        pipeline_cu_seconds = pipeline_activities_per_day * 2.5

        # 4. Direct Lake In-Memory Query & Model Eviction (~0.8 CU-seconds per query)
        direct_lake_cu_seconds = direct_lake_queries_per_day * 0.8

        total_cu_seconds = kql_cu_seconds + spark_cu_seconds + pipeline_cu_seconds + direct_lake_cu_seconds
        
        # 24-hour smoothed average CU demand (total CU-seconds / 86,400 seconds)
        avg_cu = total_cu_seconds / 86400.0
        
        # Peak instantaneous burst demand (estimated at 3.5x average)
        peak_cu = avg_cu * 3.5

        # Throttling risk: Percentage of capacity utilized under 24hr smoothed allocation
        throttling_risk = min(100.0, (avg_cu / max(1.0, float(sku.capacity_units))) * 100.0)

        return WorkloadCUAllocation(
            spark_etl_cu_seconds_per_day=round(spark_cu_seconds, 1),
            kql_streaming_cu_seconds_per_day=round(kql_cu_seconds, 1),
            data_pipeline_cu_seconds_per_day=round(pipeline_cu_seconds, 1),
            direct_lake_cu_seconds_per_day=round(direct_lake_cu_seconds, 1),
            total_cu_seconds_per_day=round(total_cu_seconds, 1),
            avg_cu_demand=round(avg_cu, 2),
            peak_cu_demand=round(peak_cu, 2),
            throttling_risk_pct=round(throttling_risk, 1),
        )

    def calculate_storage_tiering_savings(
        self,
        total_raw_data_gb: float = 250.0,
        hot_cache_days: int = 7,
        total_retention_days: int = 30,
    ) -> StorageTieringReport:
        """
        Calculates storage cost savings achieved by tiering KQL Hot Cache (7d)
        and cold OneLake Delta storage (30d) vs keeping all data in hot in-memory cache.
        """
        # Unoptimized scenario: 100% of data retained in hot memory for 30 days
        unoptimized_cost = total_raw_data_gb * self.KQL_HOT_CACHE_STORAGE_PER_GB

        # Tiered optimized scenario:
        # 7/30th of data in Hot Cache, remainder (23/30th) in OneLake cold storage
        hot_fraction = hot_cache_days / float(total_retention_days)
        cold_fraction = (total_retention_days - hot_cache_days) / float(total_retention_days)

        hot_gb = total_raw_data_gb * hot_fraction
        cold_gb = total_raw_data_gb * cold_fraction

        tiered_cost = (hot_gb * self.KQL_HOT_CACHE_STORAGE_PER_GB) + (
            cold_gb * self.ONELAKE_STANDARD_STORAGE_PER_GB
        )
        savings = unoptimized_cost - tiered_cost
        savings_pct = (savings / unoptimized_cost) * 100.0 if unoptimized_cost > 0 else 0.0

        return StorageTieringReport(
            total_raw_data_gb=round(total_raw_data_gb, 2),
            hot_cache_days=hot_cache_days,
            total_retention_days=total_retention_days,
            unoptimized_monthly_storage_usd=round(unoptimized_cost, 2),
            tiered_optimized_monthly_storage_usd=round(tiered_cost, 2),
            monthly_storage_savings_usd=round(savings, 2),
            savings_percentage=round(savings_pct, 1),
        )

    def generate_capacity_report(
        self,
        sku_name: str = "FT64",
        commitment: str = "payg",
        events_per_day: int = 500_000,
        total_storage_gb: float = 250.0,
    ) -> CapacityCostReport:
        """Generates a complete FinOps capacity and workload optimization report."""
        compute = self.calculate_compute_cost(sku_name=sku_name, commitment=commitment)
        workload = self.model_workload_cu_breakdown(events_per_day=events_per_day, assigned_sku=sku_name)
        storage = self.calculate_storage_tiering_savings(total_raw_data_gb=total_storage_gb)

        total_run_rate = compute["monthly_compute_cost_usd"] + storage.tiered_optimized_monthly_storage_usd

        # Upgrade projections for enterprise roadmap
        upgrade_projections = {
            "FT64 (Trial)": 0.00,
            "F64 (Pay-As-You-Go)": self.calculate_compute_cost("F64", commitment="payg")["monthly_compute_cost_usd"] + storage.tiered_optimized_monthly_storage_usd,
            "F64 (1-Yr Reserved)": self.calculate_compute_cost("F64", commitment="1yr")["monthly_compute_cost_usd"] + storage.tiered_optimized_monthly_storage_usd,
            "F128 (Pay-As-You-Go)": self.calculate_compute_cost("F128", commitment="payg")["monthly_compute_cost_usd"] + storage.tiered_optimized_monthly_storage_usd,
            "F128 (1-Yr Reserved)": self.calculate_compute_cost("F128", commitment="1yr")["monthly_compute_cost_usd"] + storage.tiered_optimized_monthly_storage_usd,
        }

        markdown_summary = self._render_finops_markdown(
            compute=compute,
            workload=workload,
            storage=storage,
            total_run_rate=total_run_rate,
            projections=upgrade_projections,
        )

        return CapacityCostReport(
            selected_sku=compute["sku_name"],
            capacity_units=compute["capacity_units"],
            is_trial=compute["is_trial"],
            commitment_tier=compute["commitment_tier"],
            discount_pct=compute["discount_pct"],
            effective_hourly_rate_usd=compute["effective_hourly_rate_usd"],
            monthly_compute_cost_usd=compute["monthly_compute_cost_usd"],
            storage_report=storage,
            workload_cu=workload,
            total_monthly_run_rate_usd=round(total_run_rate, 2),
            upgrade_projections=upgrade_projections,
            summary_markdown=markdown_summary,
        )

    def _render_finops_markdown(
        self,
        compute: Dict[str, Any],
        workload: WorkloadCUAllocation,
        storage: StorageTieringReport,
        total_run_rate: float,
        projections: Dict[str, float],
    ) -> str:
        """Renders an executive FinOps capacity markdown summary."""
        trial_badge = " (Trial Evaluation Tier)" if compute["is_trial"] else ""
        lines = [
            f"# HydroGrow Platform - FinOps & Capacity Optimization Report",
            f"**Assigned SKU**: `{compute['sku_name']}` ({compute['capacity_units']} CUs){trial_badge} | **Commitment**: `{compute['commitment_tier'].upper()}` ({compute['discount_pct']}% discount)",
            f"**Timestamp**: `{datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}`",
            "",
            "## 1. Monthly Financial Run-Rate",
            f"- **Compute Burn**: `${compute['monthly_compute_cost_usd']:,.2f} / month` (${compute['effective_hourly_rate_usd']:.4f}/hr)",
            f"- **Storage (Tiered & Optimized)**: `${storage.tiered_optimized_monthly_storage_usd:,.2f} / month`",
            f"- **Total Monthly Platform Run-Rate**: **`${total_run_rate:,.2f} / month`**",
            "",
            "## 2. Workload CU-Second Breakdown & Throttling Resilience",
            f"- **Spark Batch Medallion ETL**: `{workload.spark_etl_cu_seconds_per_day:,.0f} CU-sec/day`",
            f"- **KQL Streaming Ingestion & Policies**: `{workload.kql_streaming_cu_seconds_per_day:,.0f} CU-sec/day`",
            f"- **Data Factory Pipelines**: `{workload.data_pipeline_cu_seconds_per_day:,.0f} CU-sec/day`",
            f"- **Direct Lake Semantic Queries**: `{workload.direct_lake_cu_seconds_per_day:,.0f} CU-sec/day`",
            f"- **Smoothed Daily Average Demand**: `{workload.avg_cu_demand:.2f} CUs`",
            f"- **Estimated Peak Burst Demand**: `{workload.peak_cu_demand:.2f} CUs`",
            f"- **Capacity Utilization / Throttling Risk**: `{workload.throttling_risk_pct:.1f}%` (Safe Baseline < 80%)",
            "",
            "## 3. Storage Tiering & Delta Optimization Savings",
            f"- **Total Raw Telemetry**: `{storage.total_raw_data_gb:.1f} GB`",
            f"- **Hot In-Memory Cache**: `{storage.hot_cache_days} days` (NVMe SSD for Real-Time Querying)",
            f"- **Cold OneLake Retention**: `{storage.total_retention_days} days` (Delta Parquet with V-Order)",
            f"- **Unoptimized Baseline Cost**: `${storage.unoptimized_monthly_storage_usd:,.2f}/mo`",
            f"- **Optimized Tiered Cost**: `${storage.tiered_optimized_monthly_storage_usd:,.2f}/mo`",
            f"- **Monthly FinOps Savings**: **`${storage.monthly_storage_savings_usd:,.2f}/mo` (`{storage.savings_percentage:.1f}%` Reduction)**",
            "",
            "## 4. Trial-to-Production Enterprise Upgrade Roadmap",
            "| Tier / SKU | Pricing Model | Monthly Cost | Ideal Workload |",
            "| :--- | :--- | :--- | :--- |",
        ]

        for tier, cost in projections.items():
            desc = "PoC & Feature Development" if "Trial" in tier else "Standard Production (1-3 Facilities)" if "F64" in tier else "High-Throughput Enterprise (4-10 Facilities)"
            lines.append(f"| `{tier}` | Fixed / Reserved | `${cost:,.2f}` | {desc} |")

        return "\n".join(lines)

    def export_report(
        self,
        report: CapacityCostReport,
        output_json_path: str,
        output_md_path: Optional[str] = None,
    ) -> None:
        """Exports the FinOps report to JSON and Markdown."""
        os.makedirs(os.path.dirname(os.path.abspath(output_json_path)), exist_ok=True)
        with open(output_json_path, "w", encoding="utf-8") as f:
            json.dump(report.to_dict(), f, indent=2)

        if output_md_path:
            os.makedirs(os.path.dirname(os.path.abspath(output_md_path)), exist_ok=True)
            with open(output_md_path, "w", encoding="utf-8") as f:
                f.write(report.summary_markdown)

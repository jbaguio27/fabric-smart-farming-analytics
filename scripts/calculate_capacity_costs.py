#!/usr/bin/env python3
"""
CLI Tool: Microsoft Fabric Capacity Sizing & FinOps Cost Optimizer.

Calculates:
1. Hourly & monthly compute run-rates across Fabric SKUs (FT64 Trial, F2 - F2048).
2. Reserved Instance (RI) commitment discounts (1-yr @ 40.5%, 3-yr @ 65%).
3. Workload CU-second allocation and throttling risk modeling.
4. Storage tiering savings (KQL Hot Cache vs OneLake Cold Storage).
5. Exports FinOps reports in JSON and Markdown.

Usage:
    python scripts/calculate_capacity_costs.py
    python scripts/calculate_capacity_costs.py --sku FT64
    python scripts/calculate_capacity_costs.py --sku F64 --commitment 1yr --storage-gb 500
"""

import argparse
import os
import sys

# Ensure src/ is on pythonpath
repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
src_path = os.path.join(repo_root, "src")
if src_path not in sys.path:
    sys.path.insert(0, src_path)

from smart_farming.capacity.capacity_optimizer import FabricCapacityOptimizer


def main():
    if sys.stdout.encoding != "utf-8" and hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if sys.stderr.encoding != "utf-8" and hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(
        description="Microsoft Fabric FinOps & Capacity Optimization Calculator"
    )
    parser.add_argument(
        "--sku",
        type=str,
        default="FT64",
        help="Fabric Capacity SKU (FT64, F2, F4, F8, F16, F32, F64, F128, F256, F512)",
    )
    parser.add_argument(
        "--commitment",
        type=str,
        default="payg",
        choices=["payg", "1yr", "3yr"],
        help="Capacity commitment model: payg, 1yr (40.5% off), 3yr (65% off)",
    )
    parser.add_argument(
        "--events-per-day",
        type=int,
        default=500_000,
        help="Daily telemetry events ingested (default: 500,000)",
    )
    parser.add_argument(
        "--storage-gb",
        type=float,
        default=250.0,
        help="Total storage in Gigabytes across OneLake & Eventhouse (default: 250.0 GB)",
    )
    parser.add_argument(
        "--export-json",
        type=str,
        default=os.path.join(repo_root, "docs", "reports", "finops_capacity_report.json"),
        help="Path to export JSON cost report",
    )
    parser.add_argument(
        "--export-md",
        type=str,
        default=os.path.join(repo_root, "docs", "reports", "finops_cost_optimization.md"),
        help="Path to export Markdown FinOps report",
    )

    args = parser.parse_args()

    optimizer = FabricCapacityOptimizer(default_sku=args.sku)
    print("\n" + "=" * 80)
    print("MICROSOFT FABRIC - FINOPS CAPACITY & COST OPTIMIZER")
    print("=" * 80 + "\n")

    report = optimizer.generate_capacity_report(
        sku_name=args.sku,
        commitment=args.commitment,
        events_per_day=args.events_per_day,
        total_storage_gb=args.storage_gb,
    )

    print(report.summary_markdown)
    print("\n" + "=" * 80)

    # Export reports
    optimizer.export_report(
        report=report,
        output_json_path=args.export_json,
        output_md_path=args.export_md,
    )
    print(f"📄 FinOps JSON exported to: {args.export_json}")
    print(f"📄 FinOps Markdown exported to: {args.export_md}")
    print("=" * 80 + "\n")


if __name__ == "__main__":
    main()

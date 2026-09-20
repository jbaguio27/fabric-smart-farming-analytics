#!/usr/bin/env python3
"""
CLI Runner for End-to-End Testing & Validation Suite.

Executes:
1. Multi-stream schema conformance & drift detection.
2. End-to-end streaming latency SLA benchmarking (< 15.0s target).
3. Dead-Letter Queue (DLQ) fault-tolerance and auto-remediation.
4. Generates validation reports in JSON & Markdown.

Usage:
    python scripts/run_e2e_validation.py
    python scripts/run_e2e_validation.py --records-per-stream 100 --sla-target 10.0 --export-md docs/reports/e2e_validation.md
"""

import argparse
import os
import sys

# Ensure src/ is on pythonpath
repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
src_path = os.path.join(repo_root, "src")
if src_path not in sys.path:
    sys.path.insert(0, src_path)

from smart_farming.validation.e2e_validator import E2EValidationEngine


def main():
    if sys.stdout.encoding != "utf-8" and hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if sys.stderr.encoding != "utf-8" and hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(
        description="HydroGrow Platform End-to-End Validation Runner"
    )
    parser.add_argument(
        "--records-per-stream",
        type=int,
        default=50,
        help="Number of synthetic records generated per stream (default: 50)",
    )
    parser.add_argument(
        "--poison-count",
        type=int,
        default=15,
        help="Number of corrupted poison packets for DLQ resilience test (default: 15)",
    )
    parser.add_argument(
        "--sla-target",
        type=float,
        default=15.0,
        help="Target streaming latency SLA in seconds (default: 15.0)",
    )
    parser.add_argument(
        "--export-json",
        type=str,
        default=os.path.join(repo_root, "docs", "reports", "e2e_validation_report.json"),
        help="Path to export validation report as JSON",
    )
    parser.add_argument(
        "--export-md",
        type=str,
        default=os.path.join(repo_root, "docs", "reports", "e2e_validation_report.md"),
        help="Path to export validation report as Markdown",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose output logging",
    )

    args = parser.parse_args()

    engine = E2EValidationEngine(sla_target_seconds=args.sla_target)
    print("\n" + "=" * 80)
    print("HYDROGROW PLATFORM - END-TO-END VALIDATION SUITE")
    print("=" * 80 + "\n")

    report = engine.run_full_validation(
        records_per_stream=args.records_per_stream,
        poison_count=args.poison_count,
    )

    print(report.summary_markdown)
    print("\n" + "=" * 80)

    # Export reports
    engine.export_report(
        report=report,
        output_json_path=args.export_json,
        output_md_path=args.export_md,
    )
    print(f"📄 Report JSON exported to: {args.export_json}")
    print(f"📄 Report Markdown exported to: {args.export_md}")

    if report.overall_status != "PASSED":
        print("\n❌ VALIDATION SUITE FAILED!")
        sys.exit(1)
    else:
        print("\n✅ VALIDATION SUITE PASSED SUCCESSFULLY!")
        sys.exit(0)


if __name__ == "__main__":
    main()

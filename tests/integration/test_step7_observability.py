"""
HydroGrow Smart Farming Analytics Platform
Step 7 Integration Validation Test Suite: Cross-Cutting Monitoring & Observability

Validates:
1. Distributed tracing and pipeline execution span logging schema across Lakehouse, Warehouse, and Notebooks.
2. Data Factory Pipeline CTAS & Incremental CDC orchestration for fact_dataops_pipeline_log.
3. Eventhouse Real-Time KQL DataOps Observability Dashboard (17 tiles, multi-page layout, query integrity).
4. Fabric Activator Reflex Alert rules (10 alert triggers + 2 OneLake/KQL pipeline trigger bindings).
"""

import json
import os
import re
import unittest

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
FABRIC_DIR = os.path.join(PROJECT_ROOT, "fabric")


class TestStep7Observability(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.expected_span_cols = {
            "TraceId",
            "SpanId",
            "PipelineName",
            "StageName",
            "Component",
            "ExecutionStatus",
            "SourceRowCount",
            "TargetRowCount",
            "ExecutionDurationMs",
            "ErrorMessage",
            "Timestamp"
        }

    def test_warehouse_fact_dataops_pipeline_log_schema(self):
        """Verify Warehouse SQL DDL for fact_dataops_pipeline_log contains all required OpenTelemetry columns."""
        sql_path = os.path.join(
            FABRIC_DIR,
            "SmartFarming_Warehouse.Warehouse",
            "dbo",
            "Tables",
            "fact_dataops_pipeline_log.sql"
        )
        self.assertTrue(os.path.exists(sql_path), f"Missing SQL file: {sql_path}")
        with open(sql_path, "r", encoding="utf-8") as f:
            content = f.read()

        for col in self.expected_span_cols:
            self.assertIn(f"[{col}]", content, f"Missing column [{col}] in Warehouse SQL DDL")

    def test_batch_orchestrator_span_logging(self):
        """Verify Notebook_Batch_Master_Orchestrator instruments execution spans and saves to gold.fact_dataops_pipeline_log."""
        nb_path = os.path.join(
            FABRIC_DIR,
            "Notebook_Batch_Master_Orchestrator.Notebook",
            "notebook-content.py"
        )
        self.assertTrue(os.path.exists(nb_path), f"Missing notebook: {nb_path}")
        with open(nb_path, "r", encoding="utf-8") as f:
            content = f.read()

        self.assertIn("gold.fact_dataops_pipeline_log", content)
        self.assertIn("record_span", content)
        self.assertIn("BATCH_RUN_ID", content)
        self.assertIn("whenMatchedUpdateAll", content)

    def test_incremental_sync_span_logging(self):
        """Verify Notebook_Incremental_Silver_Gold_Sync instruments execution spans and flushes to gold.fact_dataops_pipeline_log."""
        nb_path = os.path.join(
            FABRIC_DIR,
            "Notebook_Incremental_Silver_Gold_Sync.Notebook",
            "notebook-content.py"
        )
        self.assertTrue(os.path.exists(nb_path), f"Missing notebook: {nb_path}")
        with open(nb_path, "r", encoding="utf-8") as f:
            content = f.read()

        self.assertIn("gold.fact_dataops_pipeline_log", content)
        self.assertIn("SPN-INCSYNC", content)
        self.assertIn("Pipeline_Medallion_Incremental_Stream_Sync", content)
        self.assertIn("whenMatchedUpdateAll", content)

    def test_batch_pipeline_warehouse_replication(self):
        """Verify Pipeline_Medallion_Batch_Orchestration replicates dbo.fact_dataops_pipeline_log to Warehouse."""
        pipeline_path = os.path.join(
            FABRIC_DIR,
            "Pipeline_Medallion_Batch_Orchestration.DataPipeline",
            "pipeline-content.json"
        )
        self.assertTrue(os.path.exists(pipeline_path), f"Missing pipeline JSON: {pipeline_path}")
        with open(pipeline_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        activities = data["properties"]["activities"]
        sync_act = next((a for a in activities if a.get("name") == "Run_Warehouse_Sync"), None)
        self.assertIsNotNone(sync_act, "Run_Warehouse_Sync activity missing")
        sql_script = sync_act["typeProperties"]["scripts"][0]["text"]["value"]
        self.assertIn("dbo.fact_dataops_pipeline_log", sql_script)

        log_act = next((a for a in activities if a.get("name") == "Log_Semantic_Refresh_Span"), None)
        self.assertIsNotNone(log_act, "Log_Semantic_Refresh_Span activity missing")

    def test_incremental_pipeline_cdc_merge(self):
        """Verify Pipeline_Medallion_Incremental_StreamSync performs CDC MERGE on dbo.fact_dataops_pipeline_log."""
        pipeline_path = os.path.join(
            FABRIC_DIR,
            "Pipeline_Medallion_Incremental_StreamSync.DataPipeline",
            "pipeline-content.json"
        )
        self.assertTrue(os.path.exists(pipeline_path), f"Missing pipeline JSON: {pipeline_path}")
        with open(pipeline_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        activities = data["properties"]["activities"]
        sync_act = next((a for a in activities if a.get("name") == "Run_Incremental_Warehouse_Sync"), None)
        self.assertIsNotNone(sync_act, "Run_Incremental_Warehouse_Sync activity missing")
        sql_script = sync_act["typeProperties"]["scripts"][0]["text"]["value"]
        self.assertIn("MERGE dbo.fact_dataops_pipeline_log AS target", sql_script)

    def test_kql_dataops_observability_dashboard(self):
        """Verify Real-Time KQL DataOps Observability Dashboard configuration and queries."""
        dashboard_path = os.path.join(
            FABRIC_DIR,
            "SmartFarming_DataOpsObservability_Dashboard.KQLDashboard",
            "RealTimeDashboard.json"
        )
        self.assertTrue(os.path.exists(dashboard_path), f"Missing KQL dashboard JSON: {dashboard_path}")
        with open(dashboard_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        # 1. Verify Pages
        pages = data.get("pages", [])
        self.assertEqual(len(pages), 2, "Expected exactly 2 dashboard pages")
        page_names = [p["name"] for p in pages]
        self.assertTrue(any("Real-Time Streaming" in p for p in page_names))
        self.assertTrue(any("Medallion Pipeline" in p for p in page_names))

        # 2. Verify Tiles Count (17 Tiles total)
        tiles = data.get("tiles", [])
        self.assertEqual(len(tiles), 17, f"Expected 17 tiles, found {len(tiles)}")

        # 3. Verify Queries
        queries = data.get("queries", [])
        self.assertGreaterEqual(len(queries), 12, "Expected at least 12 distinct KQL queries")
        query_texts = " ".join([q["text"] for q in queries])
        self.assertIn("get_stream_ingestion_sla", query_texts)
        self.assertIn("get_ingress_data_quality_audit", query_texts)
        self.assertIn("get_dead_letter_anomaly_rate", query_texts)
        self.assertIn("DataOpsPipelineLog", query_texts)

    def test_fabric_activator_reflex_entities(self):
        """Verify Fabric Activator Reflex alert definitions, SLA trigger rules, and item invocations."""
        reflex_path = os.path.join(
            FABRIC_DIR,
            "SmartFarming_Activator_Alerts.Reflex",
            "ReflexEntities.json"
        )
        self.assertTrue(os.path.exists(reflex_path), f"Missing Reflex JSON: {reflex_path}")
        with open(reflex_path, "r", encoding="utf-8") as f:
            entities = json.load(f)

        # Count alert trigger rules
        rules = [e for e in entities if e.get("payload", {}).get("definition", {}).get("type") == "Rule"]
        rule_names = [r["payload"]["name"] for r in rules]

        expected_rules = [
            "Executive Facility Operational Emergency",
            "Facility Power Surge SLA",
            "Critical Equipment Failure Imminent",
            "Micro-Climate Instability & Thermal Drift",
            "Crop Biological Stress Spike",
            "Work Order Resolution SLA Breach",
            "Stream Processing Lag SLA Breach",
            "Ingress Schema Data Quality Breach",
            "Dead-Letter Queue Anomaly Burst Rate",
            "Critical Missing Primary Key Ingress",
            "Trigger_On_Bootstrap_FileUpload",
            "Trigger_On_LiveStream_Ingress"
        ]

        for expected in expected_rules:
            self.assertIn(expected, rule_names, f"Missing Reflex rule: {expected}")


if __name__ == "__main__":
    unittest.main()

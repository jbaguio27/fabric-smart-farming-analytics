# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "synapse_pyspark"
# META   },
# META   "dependencies": {
# META     "lakehouse": {
# META       "default_lakehouse": "54fb63f8-6e3b-4ddc-9303-34774c9b22c3",
# META       "default_lakehouse_name": "SmartFarming_Lakehouse",
# META       "default_lakehouse_workspace_id": "92bc9c4b-1186-473f-8398-f198e8b16b45",
# META       "known_lakehouses": [
# META         {
# META           "id": "54fb63f8-6e3b-4ddc-9303-34774c9b22c3"
# META         }
# META       ]
# META     }
# META   }
# META }

# MARKDOWN ********************

# # 🚀 Master Medallion Batch Orchestrator (Single-Session Free-Trial Execution)

# CELL ********************

# Configure Delta Lake OCC Concurrency & Isolation
spark.conf.set("spark.databricks.delta.properties.defaults.isolationLevel", "Serializable")
spark.conf.set("spark.databricks.delta.write.concurrentAppendMode.enabled", "true")

import time
import uuid
import datetime
from pyspark.sql import functions as F
from delta.tables import DeltaTable

# Initialize Trace Context
BATCH_RUN_ID = f"TRC-{datetime.datetime.utcnow().strftime('%Y%m%d-%H%M%S')}"
batch_spans = []

def record_span(stage_name, component, start_time, src_rows=0, tgt_rows=0, status="SUCCESS", error=""):
    duration_ms = int((time.time() - start_time) * 1000)
    batch_spans.append({
        "TraceId": BATCH_RUN_ID,
        "SpanId": f"SPN-{uuid.uuid4().hex[:6]}",
        "PipelineName": "Pipeline_Medallion_Batch_Orchestration",
        "StageName": stage_name,
        "Component": component,
        "ExecutionStatus": status,
        "SourceRowCount": int(src_rows),
        "TargetRowCount": int(tgt_rows),
        "ExecutionDurationMs": duration_ms,
        "ErrorMessage": str(error),
        "Timestamp": datetime.datetime.utcnow()
    })
    print(f"✅ [{stage_name}] Duration: {duration_ms/1000.0:.2f}s | Rows: {tgt_rows:,} | Status: {status}")

print(f"🚀 Batch Run Initialized: {BATCH_RUN_ID}")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

t_bronze_start = time.time()
print("▶️ Executing Stage 1: Bronze Ingestion...")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

%run Notebook_Load_Bronze_History

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

try:
    bronze_tables = [
        "environmental_telemetry", "equipment_telemetry", "crop_telemetry",
        "irrigation_telemetry", "lighting_telemetry", "dead_letter_telemetry",
        "facility_operations", "crop_lifecycle", "maintenance_activity"
    ]
    bronze_rows = sum([spark.table(f"bronze.{t}").count() for t in bronze_tables if spark.catalog.tableExists(f"bronze.{t}")])
    record_span("Bronze_Ingestion", "Spark_Notebook", t_bronze_start, src_rows=bronze_rows, tgt_rows=bronze_rows)
except Exception as e:
    record_span("Bronze_Ingestion", "Spark_Notebook", t_bronze_start, status="FAILED", error=str(e))
    raise e

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

t_silver_start = time.time()
print("▶️ Executing Stage 2: Silver Cleansing & Quality Gate...")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

%run Notebook_Silver_ETL

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

try:
    silver_tables = [
        "crop_biological_cleaned", "crop_master_enriched", "dead_letter_classified",
        "environmental_cleaned", "environmental_metrics", "equipment_master_enriched",
        "equipment_risk_cleaned", "facility_master_enriched", "irrigation_flow_cleaned",
        "lighting_dli_cleaned", "maintenance_sla_cleaned"
    ]
    silver_rows = sum([spark.table(f"silver.{t}").count() for t in silver_tables if spark.catalog.tableExists(f"silver.{t}")])
    record_span("Silver_Cleansing", "Spark_Notebook", t_silver_start, src_rows=bronze_rows, tgt_rows=silver_rows)
except Exception as e:
    record_span("Silver_Cleansing", "Spark_Notebook", t_silver_start, status="FAILED", error=str(e))
    raise e

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

t_gold_start = time.time()
print("▶️ Executing Stage 3: Gold Star Schema & SCD Type 2...")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

%run Notebook_Gold_ETL

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

try:
    gold_tables = [
        "dim_date", "dim_facility", "dim_zone", "dim_equipment", "dim_crop", "dim_technician",
        "fact_environmental_daily", "fact_equipment_telemetry", "fact_crop_yield",
        "fact_irrigation_daily", "fact_lighting_dli_daily", "fact_maintenance_sla",
        "fact_dead_letter_governance"
    ]
    gold_rows = sum([spark.table(f"gold.{t}").count() for t in gold_tables if spark.catalog.tableExists(f"gold.{t}")])
    record_span("Gold_Star_Schema", "Spark_Notebook", t_gold_start, src_rows=silver_rows, tgt_rows=gold_rows)
except Exception as e:
    record_span("Gold_Star_Schema", "Spark_Notebook", t_gold_start, status="FAILED", error=str(e))
    raise e

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Create Telemetry DataFrame
df_telemetry = spark.createDataFrame(batch_spans)
table_name = "gold.fact_dataops_pipeline_log"

if not spark.catalog.tableExists(table_name):
    df_telemetry.write.format("delta").mode("overwrite").saveAsTable(table_name)
else:
    # Idempotent Delta MERGE on (TraceId, StageName)
    delta_log = DeltaTable.forName(spark, table_name)
    (
        delta_log.alias("target")
        .merge(
            df_telemetry.alias("source"),
            "target.TraceId = source.TraceId AND target.StageName = source.StageName"
        )
        .whenMatchedUpdateAll()
        .whenNotMatchedInsertAll()
        .execute()
    )

total_batch_sec = round(sum([s["ExecutionDurationMs"] for s in batch_spans]) / 1000.0, 2)
print("==============================================================================")
print(f"✨ BATCH RUN {BATCH_RUN_ID} COMPLETED IN {total_batch_sec}s")
print("==============================================================================")
df_telemetry.select("StageName", "ExecutionStatus", F.round(F.col("ExecutionDurationMs")/1000.0, 2).alias("DurationSec"), "TargetRowCount").show(truncate=False)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

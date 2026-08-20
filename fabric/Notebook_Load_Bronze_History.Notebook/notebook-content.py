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

# CELL ********************

# ===================================================================================================================
# MICROSOFT FABRIC PYSPARK INGESTION ENGINE: NOTEBOOK_LOAD_BRONZE_HISTORY
# Platform: HydroGrow Smart Farming Analytics Platform
# Lakehouse: SmartFarming_Lakehouse (Schema: bronze)
# Ingestion Mode: DYNAMICALLY ALIGNED INCREMENTAL DELTA MERGE INTO
# ===================================================================================================================
from pyspark.sql import functions as F
from delta.tables import DeltaTable
import uuid

spark.sql("CREATE SCHEMA IF NOT EXISTS bronze")

run_id = str(uuid.uuid4())
pipeline_ver = "v1.0.0"

# Manifest of 9 Operational Bronze Tables
manifest = [
    {"folder": "EnvironmentalTelemetry", "table": "environmental_telemetry", "pk": "event_id"},
    {"folder": "EquipmentTelemetry",     "table": "equipment_telemetry",     "pk": "event_id"},
    {"folder": "CropTelemetry",          "table": "crop_telemetry",          "pk": "event_id"},
    {"folder": "IrrigationTelemetry",     "table": "irrigation_telemetry",     "pk": "event_id"},
    {"folder": "LightingTelemetry",       "table": "lighting_telemetry",       "pk": "event_id"},
    {"folder": "DeadLetterTelemetry",     "table": "dead_letter_telemetry",     "pk": "event_id"},
    {"folder": "FacilityOperations",     "table": "facility_operations",     "pk": "event_id"},
    {"folder": "CropLifecycle",          "table": "crop_lifecycle",          "pk": "event_id"},
    {"folder": "MaintenanceActivity",     "table": "maintenance_activity",     "pk": "event_id"},
]

print(f"🚀 Starting Dynamic Schema-Aligned Delta Merge Ingestion (Run ID: {run_id[:8]})...")

for entry in manifest:
    source_name = entry["folder"]
    target_table = f"bronze.{entry['table']}"
    pk_col = entry["pk"]
    file_path = f"Files/bootstrap_history/{source_name}.json"
    
    try:
        # 1. Read Bootstrap JSON Data from Files/bootstrap_history/
        df_raw = spark.read.option("multiline", "true").json(file_path)
        
        # 2. Enrich with DataOps Ingestion Metadata & Deduplicate
        df_bronze_source = (
            df_raw
            .drop_duplicates([pk_col])
            .withColumn("ingestion_timestamp", F.current_timestamp())
            .withColumn("ingestion_source", F.lit("BOOTSTRAP"))
            .withColumn("ingestion_run_id", F.lit(run_id))
            .withColumn("source_file", F.lit(file_path))
            .withColumn("pipeline_version", F.lit(pipeline_ver))
        )

        # 3. Dynamic Target Schema Alignment (Aligns IngestionTime, event_type, etc.)
        if spark.catalog.tableExists(target_table):
            target_cols = spark.table(target_table).columns
            for col in target_cols:
                if col not in df_bronze_source.columns:
                    if col.lower() == "ingestiontime":
                        df_bronze_source = df_bronze_source.withColumn(col, F.current_timestamp())
                    elif col.lower() == "event_type":
                        df_bronze_source = df_bronze_source.withColumn(col, F.lit(source_name))
                    else:
                        df_bronze_source = df_bronze_source.withColumn(col, F.lit(None))
            
            # 4. Incremental Delta MERGE INTO
            delta_target = DeltaTable.forName(spark, target_table)
            (
                delta_target.alias("target")
                .merge(
                    df_bronze_source.alias("source"),
                    f"target.{pk_col} = source.{pk_col}"
                )
                .whenNotMatchedInsertAll()
                .execute()
            )
        else:
            df_bronze_source.write.format("delta").saveAsTable(target_table)
            
        row_count = spark.table(target_table).count()
        print(f"✅ Incrementally Merged into {target_table} (Active Total: {row_count} rows)")
    except Exception as e:
        print(f"ℹ️ Notice for {source_name}: {str(e)}")

print("\nSummary of Active Bronze Delta Tables:")
spark.sql("SHOW TABLES IN bronze").show(15, truncate=False)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

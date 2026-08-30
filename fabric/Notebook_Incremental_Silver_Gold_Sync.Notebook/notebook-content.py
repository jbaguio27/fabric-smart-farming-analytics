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

# Configure Delta Lake OCC Concurrency & Auto-Retry
spark.conf.set("spark.databricks.delta.properties.defaults.isolationLevel", "Serializable")
spark.conf.set("spark.databricks.delta.write.concurrentAppendMode.enabled", "true")
spark.conf.set("spark.databricks.delta.commit.retry.limit", "10")

import time
import uuid
import datetime
from pyspark.sql import functions as F
from pyspark.sql.window import Window
from delta.tables import DeltaTable

RUN_ID = f"INC-{datetime.datetime.utcnow().strftime('%Y%m%d-%H%M%S')}"
PIPELINE_RUN_DATE = datetime.date.today()
t0 = time.time()
total_processed_rows = 0

# Watermark Control Table
watermark_table = "gold._ingestion_watermarks"
if not spark.catalog.tableExists(watermark_table):
    spark.sql(f"CREATE TABLE IF NOT EXISTS {watermark_table} (stream_name STRING, last_processed_timestamp TIMESTAMP)")

def get_watermark(stream_name):
    if not spark.catalog.tableExists(watermark_table):
        return None
    try:
        row = spark.table(watermark_table).filter(F.col("stream_name") == stream_name).collect()
        if row and row[0]["last_processed_timestamp"]:
            return row[0]["last_processed_timestamp"]
    except Exception:
        pass
    return None

def set_watermark(stream_name, max_ts):
    if max_ts:
        spark.sql(f"""
            MERGE INTO {watermark_table} AS t 
            USING (SELECT '{stream_name}' AS stream_name, CAST('{max_ts}' AS TIMESTAMP) AS last_processed_timestamp) AS s 
            ON t.stream_name = s.stream_name 
            WHEN MATCHED THEN UPDATE SET t.last_processed_timestamp = s.last_processed_timestamp 
            WHEN NOT MATCHED THEN INSERT *
        """)

# Dynamic Universal Incremental Batch Extractor with Multi-Source Fallback
def extract_incremental_stream(table_candidates, watermark_key):
    if isinstance(table_candidates, str):
        table_candidates = [table_candidates]
    
    wm = get_watermark(watermark_key)
    
    for cand in table_candidates:
        df = None
        if cand.startswith("Files/") or cand.startswith("/"):
            try:
                df = spark.read.format("delta").load(cand)
            except Exception:
                pass
        elif spark.catalog.tableExists(cand):
            try:
                df = spark.table(cand)
            except Exception:
                pass
                
        if df is not None and df.count() > 0:
            cols = df.columns
            col_map = {c.lower(): c for c in cols}
            
            # Resolve timestamp column case-insensitively
            raw_col_name = col_map.get("ingestiontime") or col_map.get("ingestion_timestamp") or col_map.get("timestamp")
            if raw_col_name:
                raw_ts_str = F.regexp_replace(F.trim(F.col(raw_col_name).cast("string")), "[\"']", "")
                ts_expr = F.coalesce(
                    F.to_timestamp(raw_ts_str),
                    F.to_timestamp(raw_ts_str, "yyyy-MM-dd'T'HH:mm:ss.SSSSSS'Z'"),
                    F.to_timestamp(raw_ts_str, "yyyy-MM-dd'T'HH:mm:ss'Z'"),
                    F.to_timestamp(raw_ts_str, "yyyy-MM-dd HH:mm:ss"),
                    F.to_timestamp(F.col(raw_col_name))
                )
            else:
                ts_expr = F.current_timestamp()
                
            df_ts = df.withColumn("_parsed_sync_ts", ts_expr)
            if wm is not None:
                df_filtered = df_ts.filter(F.col("_parsed_sync_ts") > F.lit(wm))
            else:
                df_filtered = df_ts
                
            cnt = df_filtered.count()
            if cnt > 0:
                print(f"[{watermark_key}] Extracted {cnt:,} new events from source '{cand}' (Watermark: {wm})")
                return df_filtered, cnt, "_parsed_sync_ts"
                
    return None, 0, "_parsed_sync_ts"

# Safe Dimension Lookup Helper
def get_safe_dim(table_name, select_cols):
    if spark.catalog.tableExists(table_name) and spark.table(table_name).count() > 0:
        df = spark.table(table_name)
        if "is_current" in df.columns:
            df = df.filter(F.col("is_current") == True)
        return F.broadcast(df.select(*select_cols).cache())
    return None

def resolve_table_df(candidates):
    if isinstance(candidates, str):
        candidates = [candidates]
    for c in candidates:
        if c.startswith("Files/") or c.startswith("/"):
            try:
                df = spark.read.format("delta").load(c)
                if df is not None and df.count() > 0:
                    return df
            except Exception:
                pass
        elif spark.catalog.tableExists(c):
            try:
                df = spark.table(c)
                if df is not None and df.count() > 0:
                    return df
            except Exception:
                pass
    return None

dim_fac_bcast = get_safe_dim("gold.dim_facility", ["facility_key", "facility_id", "effective_date", "expiration_date"])
dim_zone_bcast = get_safe_dim("gold.dim_zone", ["zone_key", "facility_key", "zone_id", "effective_date", "expiration_date"])
dim_eq_bcast = get_safe_dim("gold.dim_equipment", ["equipment_key", "equipment_id", "effective_date", "expiration_date"])
dim_crop_bcast = get_safe_dim("gold.dim_crop", ["crop_key", F.upper(F.col("crop_type")).alias("crop_id")])
dim_tech_bcast = get_safe_dim("gold.dim_technician", ["technician_key", F.trim(F.col("technician_name")).alias("technician_name")])

# Broadcast lookup for facility enrichment
df_fac_lookup = None
if spark.catalog.tableExists("silver.facility_master_enriched"):
    try:
        df_fac_lookup = spark.table("silver.facility_master_enriched").select("facility_id", "facility_name", "region").drop_duplicates(["facility_id"])
    except Exception:
        pass

def enrich_facility_info(df):
    if "facility_name" not in df.columns or "region" not in df.columns:
        if df_fac_lookup is not None:
            df = df.join(df_fac_lookup, "facility_id", "left")
        if "facility_name" not in df.columns:
            df = df.withColumn("facility_name", F.coalesce(F.col("facility_id"), F.lit("FAC-001")))
        else:
            df = df.withColumn("facility_name", F.coalesce(F.col("facility_name"), F.col("facility_id"), F.lit("FAC-001")))
        if "region" not in df.columns:
            df = df.withColumn("region", F.lit("NCR"))
        else:
            df = df.withColumn("region", F.coalesce(F.col("region"), F.lit("NCR")))
    return df

print(f"Initialized Incremental Engine: {RUN_ID} (Multi-Source Extractor & Schema-Aligned Active)")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# 1. Facility Master Enriched (silver.facility_master_enriched)
df_fac_raw = resolve_table_df(["FacilityOperations", "Files/FacilityOperations", "bronze.facility_operations"])
if df_fac_raw is not None:
    df_fac_cleaned = (
        df_fac_raw
        .withColumn("facility_id_clean", F.upper(F.trim(F.col("facility_id"))))
        .withColumn("facility_name_clean", F.trim(F.col("facility_name")))
        .withColumn("region_clean", F.upper(F.trim(F.col("region"))))
        .withColumn("city_clean", F.trim(F.col("city")))
        .withColumn("latitude_clean", F.round(F.col("latitude").cast("double"), 4))
        .withColumn("longitude_clean", F.round(F.col("longitude").cast("double"), 4))
        .withColumn("elevation_m_clean", F.round(F.col("elevation_m").cast("double"), 1))
        .withColumn("climate_zone_clean", F.trim(F.col("climate_zone")))
        .withColumn("water_source_clean", F.trim(F.col("water_source")))
        .withColumn("power_grid_redundancy_clean", F.trim(F.col("power_grid_redundancy")))
        .withColumn("max_zone_capacity_clean", F.col("max_zone_capacity").cast("int"))
        .withColumn("active_zones_clean", F.col("active_zones_count").cast("int"))
        .withColumn("total_equipment_clean", F.col("total_equipment_count").cast("int"))
        .withColumn("overall_health_clean", F.round(F.col("overall_health").cast("double"), 1))
        .withColumn("power_draw_kw_clean", F.round(F.col("power_draw_kw").cast("double"), 2))
        .withColumn("water_circ_lph_clean", F.round(F.col("water_circulation_lph").cast("double"), 1))
        .withColumn("active_alerts_clean", F.col("active_critical_alerts").cast("int"))
        .withColumn("contact_clean", F.coalesce(F.trim(F.col("operator_contact")), F.lit("facility.mgr@smartfarm.ph")))
        .withColumn("phone_clean", F.coalesce(F.trim(F.col("operator_phone")), F.lit("+639178452190")))
        .withColumn("effective_date_clean", F.to_date(F.col("timestamp")))
        .select(
            F.col("facility_id_clean").alias("facility_id"),
            F.col("facility_name_clean").alias("facility_name"),
            F.col("region_clean").alias("region"),
            F.col("city_clean").alias("city"),
            F.col("latitude_clean").alias("latitude"),
            F.col("longitude_clean").alias("longitude"),
            F.col("elevation_m_clean").alias("elevation_m"),
            F.col("climate_zone_clean").alias("climate_zone"),
            F.col("water_source_clean").alias("water_source"),
            F.col("power_grid_redundancy_clean").alias("power_grid_redundancy"),
            F.col("max_zone_capacity_clean").alias("max_zone_capacity"),
            F.col("active_zones_clean").alias("active_zones_count"),
            F.col("total_equipment_clean").alias("total_equipment_count"),
            F.col("overall_health_clean").alias("overall_health"),
            F.col("power_draw_kw_clean").alias("power_draw_kw"),
            F.col("water_circ_lph_clean").alias("water_circulation_lph"),
            F.col("active_alerts_clean").alias("active_critical_alerts"),
            F.col("contact_clean").alias("operator_contact"),
            F.col("phone_clean").alias("operator_phone"),
            F.col("effective_date_clean").alias("effective_date")
        )
        .drop_duplicates(["facility_id", "effective_date"]) # Strict MERGE key deduplication
    )
    DeltaTable.forName(spark, "silver.facility_master_enriched").alias("t").merge(
        df_fac_cleaned.alias("s"), "t.facility_id = s.facility_id AND t.effective_date = s.effective_date"
    ).whenMatchedUpdateAll().whenNotMatchedInsertAll().execute()

# 2. Equipment Master Enriched (silver.equipment_master_enriched)
df_eq_raw = resolve_table_df(["EquipmentTelemetry", "Files/EquipmentTelemetry", "bronze.equipment_telemetry"])
if df_eq_raw is not None:
    window_eq_latest = Window.partitionBy(F.trim(F.col("equipment_id"))).orderBy(F.col("timestamp").desc())
    contact_clean = F.coalesce(F.trim(F.col("operator_contact")), F.lit("tech.support@smartfarm.ph"))
    phone_clean = F.coalesce(F.trim(F.col("operator_phone")), F.lit("+639178452190"))
    
    df_eq_master = (
        df_eq_raw
        .withColumn("eq_id_clean", F.trim(F.col("equipment_id")))
        .withColumn("fac_id_clean", F.upper(F.trim(F.col("facility_id"))))
        .withColumn("zone_id_clean", F.trim(F.col("zone_id")))
        .withColumn("eq_type_clean", F.upper(F.trim(F.col("equipment_type"))))
        .withColumn("mfr_clean", F.coalesce(F.trim(F.col("manufacturer")), F.lit("HydroPump Corp")))
        .withColumn("model_clean", F.coalesce(F.trim(F.col("model_number")), F.lit("HP-3000X")))
        .withColumn("effective_date_clean", F.to_date(F.col("timestamp")))
        .filter(~F.col("eq_id_clean").contains("ORPHAN"))
        .filter(F.col("eq_id_clean").rlike("^EQ-[0-9]{5}$"))
        .withColumn("rank", F.row_number().over(window_eq_latest))
        .filter(F.col("rank") == 1) # Keep exactly 1 latest row per equipment_id
        .select(
            F.col("eq_id_clean").alias("equipment_id"),
            F.col("fac_id_clean").alias("facility_id"),
            F.col("zone_id_clean").alias("zone_id"),
            F.col("eq_type_clean").alias("equipment_type"),
            F.col("mfr_clean").alias("manufacturer"),
            F.col("model_clean").alias("model_number"),
            F.col("effective_date_clean").alias("installation_date"),
            F.round(F.col("runtime_hours").cast("double"), 1).alias("cumulative_runtime_hours"),
            F.round(F.col("health").cast("double"), 1).alias("current_health_score"),
            F.col("operating_status"),
            contact_clean.alias("operator_contact"),
            phone_clean.alias("operator_phone"),
            F.col("effective_date_clean").alias("effective_date")
        )
        .drop_duplicates(["equipment_id"]) # Strict single-key guarantee
    )
    DeltaTable.forName(spark, "silver.equipment_master_enriched").alias("t").merge(
        df_eq_master.alias("s"), "t.equipment_id = s.equipment_id"
    ).whenMatchedUpdateAll().whenNotMatchedInsertAll().execute()

# 3. Crop Master Enriched (silver.crop_master_enriched)
df_crop_raw = resolve_table_df(["CropLifecycle", "Files/CropLifecycle", "bronze.crop_lifecycle"])
if df_crop_raw is not None:
    stage_clean = F.upper(F.trim(F.col("lifecycle_stage")))
    is_active_calc = F.when(stage_clean.isin("HARVESTED", "COMPLETED", "TERMINATED"), F.lit(False)).otherwise(F.lit(True))
    contact_clean = F.coalesce(F.trim(F.col("operator_contact")), F.lit("agronomy.lead@smartfarm.ph"))
    phone_clean = F.coalesce(F.trim(F.col("operator_phone")), F.lit("+639178452190"))
    
    opt_temp_calc = (
        F.when(F.lower(F.col("crop_type")).contains("butterhead"), F.lit(22.0))
         .when(F.lower(F.col("crop_type")).contains("batavia"), F.lit(21.5))
         .when(F.lower(F.col("crop_type")).contains("kale"), F.lit(20.0))
         .when(F.lower(F.col("crop_type")).contains("spinach"), F.lit(19.0))
         .when(F.lower(F.col("crop_type")).contains("arugula"), F.lit(20.0))
         .when(F.lower(F.col("crop_type")).contains("basil"), F.lit(24.0))
         .when(F.lower(F.col("crop_type")).contains("strawberry"), F.lit(19.0))
         .otherwise(F.lit(22.0))
    )
    opt_humid_calc = (
        F.when(F.lower(F.col("crop_type")).contains("strawberry"), F.lit(70.0))
         .when(F.lower(F.col("crop_type")).contains("kale"), F.lit(60.0))
         .otherwise(F.lit(65.0))
    )
    
    window_latest = Window.partitionBy(F.trim(F.col("crop_batch_id"))).orderBy(F.col("timestamp").desc())
    df_crop_master = (
        df_crop_raw
        .withColumn("crop_batch_clean", F.trim(F.col("crop_batch_id")))
        .withColumn("crop_type_clean", F.trim(F.col("crop_type")))
        .withColumn("stage_clean", stage_clean)
        .withColumn("is_active_flag", is_active_calc)
        .withColumn("rank", F.row_number().over(window_latest))
        .filter(F.col("rank") == 1)
        .select(
            F.col("crop_batch_clean").alias("crop_batch_id"),
            F.col("crop_type_clean").alias("crop_type"),
            F.col("stage_clean").alias("lifecycle_stage"),
            F.round(F.col("age_days").cast("double"), 1).alias("stage_age_days_baseline"),
            F.round(F.col("health_score").cast("double"), 1).alias("target_health_score"),
            F.col("harvest_cycle_days").cast("int").alias("harvest_cycle_days"),
            F.round(F.col("target_biomass_g").cast("double"), 1).alias("target_biomass_g"),
            opt_temp_calc.alias("optimal_temperature_celsius"),
            opt_humid_calc.alias("optimal_humidity_percent"),
            F.col("is_active_flag").alias("is_active"),
            contact_clean.alias("operator_contact"),
            phone_clean.alias("operator_phone")
        )
        .drop_duplicates(["crop_batch_id"]) # Strict single-key guarantee
    )
    DeltaTable.forName(spark, "silver.crop_master_enriched").alias("t").merge(
        df_crop_master.alias("s"), "t.crop_batch_id = s.crop_batch_id"
    ).whenMatchedUpdateAll().whenNotMatchedInsertAll().execute()

print("Master Enriched Tables Synced with zero duplicate keys.")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Environmental

df_new_env, cnt_env, time_col = extract_incremental_stream(["EnvironmentalTelemetry", "Files/EnvironmentalTelemetry", "bronze.environmental_telemetry"], "environmental_telemetry")
if df_new_env is not None and cnt_env > 0:
    total_processed_rows += cnt_env
    raw_env_cols = df_new_env.columns
    fac_clean = F.when(F.col("facility_id").isNull() | F.upper(F.trim(F.col("facility_id"))).isin("", "N/A", "UNKNOWN"), F.lit("UNKNOWN_FACILITY")).otherwise(F.upper(F.trim(F.col("facility_id"))))
    zone_clean = F.when(F.col("zone_id").isNull() | F.upper(F.trim(F.col("zone_id"))).isin("", "N/A", "UNKNOWN"), F.lit("ZONE-UNKNOWN")).otherwise(F.upper(F.trim(F.col("zone_id"))))
    stype_raw = F.col("sensor_type") if "sensor_type" in raw_env_cols else F.lit("air_temperature")
    stype_clean = F.lower(F.trim(stype_raw))
    val_raw = (F.col("sensor_value") if "sensor_value" in raw_env_cols else F.lit(22.0)).cast("double")
    unit_col = F.col("unit") if "unit" in raw_env_cols else F.lit("celsius")
    weather_col = F.col("weather") if "weather" in raw_env_cols else F.lit("Clear")
    
    clean_val = (
        F.when((stype_clean == "air_temperature") & ((val_raw < -10.0) | (val_raw > 65.0)), F.lit(None))
        .when((stype_clean == "humidity") & ((val_raw < 0.0) | (val_raw > 100.0)), F.lit(None))
        .when((stype_clean == "co2") & ((val_raw < 0.0) | (val_raw > 5000.0)), F.lit(None))
        .when((stype_clean == "water_ph") & ((val_raw < 0.0) | (val_raw > 14.0)), F.lit(None))
        .when((stype_clean == "electrical_conductivity") & ((val_raw < 0.0) | (val_raw > 15.0)), F.lit(None))
        .otherwise(F.round(val_raw, 2))
    )
    
    raw_ts_str = F.regexp_replace(F.trim(F.col("timestamp").cast("string")), "[\"']", "")
    ts_clean = F.coalesce(F.to_timestamp(raw_ts_str), F.to_timestamp(raw_ts_str, "yyyy-MM-dd'T'HH:mm:ss'Z'"), F.current_timestamp())
    
    # 1. silver.environmental_cleaned
    df_silver_clean = (
        df_new_env
        .withColumn("facility_id", fac_clean)
        .withColumn("zone_id", zone_clean)
        .withColumn("sensor_type", stype_clean)
        .withColumn("sensor_value", clean_val)
        .withColumn("unit", unit_col)
        .withColumn("weather", weather_col)
        .withColumn("timestamp", ts_clean)
        .drop_duplicates(["event_id"])
    )
    df_silver_clean = enrich_facility_info(df_silver_clean).select(
        "event_id", "facility_id", "facility_name", "region", "zone_id",
        "sensor_type", "sensor_value", "unit", "weather", "timestamp"
    )
    DeltaTable.forName(spark, "silver.environmental_cleaned").alias("t").merge(
        df_silver_clean.alias("s"), "t.event_id = s.event_id"
    ).whenMatchedUpdateAll().whenNotMatchedInsertAll().execute()
    
    # 2. silver.environmental_metrics
    df_pivoted = (
        df_silver_clean
        .filter(F.col("zone_id").rlike("^ZONE-[0-9]{3}$"))
        .withColumn("window_time", F.date_trunc("minute", F.col("timestamp")))
        .groupBy("facility_id", "zone_id", "window_time")
        .pivot("sensor_type", ["air_temperature", "humidity", "co2", "light_intensity", "water_ph", "dissolved_oxygen", "electrical_conductivity"])
        .agg(F.avg("sensor_value"))
    )
    
    t_c = F.coalesce(F.col("air_temperature"), F.lit(22.0))
    rh_p = F.coalesce(F.col("humidity"), F.lit(65.0))
    svp = F.lit(0.61078) * F.exp((F.lit(17.27) * t_c) / (t_c + F.lit(237.3)))
    vpd_calc = F.round(svp * (F.lit(1.0) - (rh_p / F.lit(100.0))), 3)
    penalty = F.abs(t_c - F.lit(22.0)) * 2.5 + F.abs(rh_p - F.lit(65.0)) * 0.5
    comp_score = F.round(F.greatest(F.lit(50.0), F.lit(100.0) - penalty), 1)
    
    df_metrics = (
        df_pivoted
        .withColumn("air_temperature_c", F.round(t_c, 2))
        .withColumn("humidity_pct", F.round(rh_p, 1))
        .withColumn("co2_ppm", F.round(F.coalesce(F.col("co2"), F.lit(800.0)), 0))
        .withColumn("light_intensity_lux", F.round(F.coalesce(F.col("light_intensity"), F.lit(30000.0)), 0))
        .withColumn("water_ph", F.round(F.coalesce(F.col("water_ph"), F.lit(6.0)), 2))
        .withColumn("dissolved_oxygen_mg_l", F.round(F.coalesce(F.col("dissolved_oxygen"), F.lit(8.0)), 1))
        .withColumn("electrical_conductivity_ms_cm", F.round(F.coalesce(F.col("electrical_conductivity"), F.lit(2.2)), 2))
        .withColumn("vpd_kpa", vpd_calc)
        .withColumn("temp_drift_c", F.round(t_c - F.lit(22.0), 2))
        .withColumn("composite_stability_score", comp_score)
        .withColumn("environmental_status", F.when(comp_score >= 90.0, "OPTIMAL").when(comp_score >= 75.0, "STABLE").otherwise("WARNING"))
        .withColumn("snapshot_id", F.concat_ws("_", F.col("facility_id"), F.col("zone_id"), F.date_format(F.col("window_time"), "yyyyMMddHHmmss")))
        .drop_duplicates(["snapshot_id"])
    )
    df_metrics = enrich_facility_info(df_metrics).select(
        "snapshot_id", "facility_id", "facility_name", "region", "zone_id",
        "air_temperature_c", "humidity_pct", "co2_ppm", "light_intensity_lux",
        "water_ph", "dissolved_oxygen_mg_l", "electrical_conductivity_ms_cm",
        "vpd_kpa", "temp_drift_c", "composite_stability_score",
        "environmental_status", F.col("window_time").alias("timestamp")
    )
    DeltaTable.forName(spark, "silver.environmental_metrics").alias("t").merge(
        df_metrics.alias("s"), "t.snapshot_id = s.snapshot_id"
    ).whenMatchedUpdateAll().whenNotMatchedInsertAll().execute()
    
    # 3. gold.fact_environmental_daily (Exact Match with Notebook_Gold_ETL)
    df_env_agg = (
        df_metrics
        .withColumn("date_key", F.date_format("timestamp", "yyyyMMdd").cast("int"))
        .withColumn("event_date", F.to_date("timestamp"))
        .groupBy("date_key", "event_date", "facility_id", "zone_id")
        .agg(
            F.round(F.avg("air_temperature_c"), 2).alias("avg_ambient_temp_celsius"),
            F.round(F.min("air_temperature_c"), 2).alias("min_ambient_temp_celsius"),
            F.round(F.max("air_temperature_c"), 2).alias("max_ambient_temp_celsius"),
            F.round(F.avg("humidity_pct"), 2).alias("avg_humidity_pct"),
            F.round(F.avg("co2_ppm"), 2).alias("avg_co2_ppm"),
            F.round(F.avg("vpd_kpa"), 2).alias("avg_vpd_kpa"),
            F.round(F.avg("temp_drift_c"), 2).alias("avg_temp_drift_celsius"),
            F.round(F.avg("composite_stability_score"), 2).alias("avg_stability_score"),
            F.round(F.avg("water_ph"), 2).alias("avg_water_ph"),
            F.round(F.avg("electrical_conductivity_ms_cm"), 2).alias("avg_ec_ms_cm"),
            F.count("snapshot_id").alias("telemetry_sample_count")
        )
    )
    
    df_gold_env = df_env_agg.alias("fact")
    if dim_fac_bcast is not None:
        df_gold_env = df_gold_env.join(dim_fac_bcast.alias("dim_fac"), (F.col("fact.facility_id") == F.col("dim_fac.facility_id")) & (F.col("fact.event_date") >= F.col("dim_fac.effective_date")) & (F.col("fact.event_date") <= F.col("dim_fac.expiration_date")), "left")
    else:
        df_gold_env = df_gold_env.withColumn("dim_fac.facility_key", F.lit(-1))
        
    if dim_zone_bcast is not None:
        df_gold_env = df_gold_env.join(dim_zone_bcast.alias("dim_zn"), (F.col("dim_fac.facility_key") == F.col("dim_zn.facility_key")) & (F.col("fact.zone_id") == F.col("dim_zn.zone_id")) & (F.col("fact.event_date") >= F.col("dim_zn.effective_date")) & (F.col("fact.event_date") <= F.col("dim_zn.expiration_date")), "left")
    else:
        df_gold_env = df_gold_env.withColumn("dim_zn.zone_key", F.lit(-1))

    df_gold_env_final = df_gold_env.select(
        F.col("fact.date_key"),
        F.coalesce(F.col("dim_fac.facility_key"), F.lit(-1)).alias("facility_key"),
        F.coalesce(F.col("dim_zn.zone_key"), F.lit(-1)).alias("zone_key"),
        F.col("fact.avg_ambient_temp_celsius"),
        F.col("fact.min_ambient_temp_celsius"),
        F.col("fact.max_ambient_temp_celsius"),
        F.col("fact.avg_humidity_pct"),
        F.col("fact.avg_co2_ppm"),
        F.col("fact.avg_vpd_kpa"),
        F.col("fact.avg_temp_drift_celsius"),
        F.col("fact.avg_stability_score"),
        F.col("fact.avg_water_ph"),
        F.col("fact.avg_ec_ms_cm"),
        F.col("fact.telemetry_sample_count"),
        F.current_timestamp().alias("created_timestamp"),
        F.lit(PIPELINE_RUN_DATE).alias("pipeline_run_date")
    ).drop_duplicates(["date_key", "facility_key", "zone_key"])
    
    DeltaTable.forName(spark, "gold.fact_environmental_daily").alias("t").merge(
        df_gold_env_final.alias("s"), "t.date_key = s.date_key AND t.facility_key = s.facility_key AND t.zone_key = s.zone_key"
    ).whenMatchedUpdateAll().whenNotMatchedInsertAll().execute()
    
    max_ts_env = df_new_env.select(F.max(time_col)).collect()[0][0]
    set_watermark("environmental_telemetry", max_ts_env)
    print(f"Environmental: Merged {cnt_env:,} rows into environmental_cleaned, metrics & fact_environmental_daily.")


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Equipment

df_new_eq, cnt_eq, time_col_eq = extract_incremental_stream(["EquipmentTelemetry", "Files/EquipmentTelemetry", "bronze.equipment_telemetry"], "equipment_telemetry")
if df_new_eq is not None and cnt_eq > 0:
    total_processed_rows += cnt_eq
    raw_eq_cols = df_new_eq.columns
    eq_id_raw = F.col("equipment_id") if "equipment_id" in raw_eq_cols else F.lit("UNREGISTERED_ASSET")
    raw_eq_id = F.upper(F.trim(eq_id_raw))
    eq_id_clean = F.when(raw_eq_id.isNull() | raw_eq_id.contains("ORPHAN"), F.lit("UNREGISTERED_ASSET")).otherwise(raw_eq_id)
    fac_clean = F.when(F.col("facility_id").isNull() | F.upper(F.trim(F.col("facility_id"))).isin("", "N/A", "UNKNOWN"), F.lit("UNKNOWN_FACILITY")).otherwise(F.upper(F.trim(F.col("facility_id"))))
    zone_clean = F.when(F.col("zone_id").isNull() | F.upper(F.trim(F.col("zone_id"))).isin("", "N/A", "UNKNOWN"), F.lit("ZONE-UNKNOWN")).otherwise(F.upper(F.trim(F.col("zone_id"))))
    
    op_temp = F.col("operating_temperature_c") if "operating_temperature_c" in raw_eq_cols else (F.col("operating_temp_c") if "operating_temp_c" in raw_eq_cols else F.lit(45.0))
    temp_clean = F.coalesce(F.when((op_temp.cast("double") < 0.0) | (op_temp.cast("double") > 150.0), F.lit(None)).otherwise(F.round(op_temp.cast("double"), 2)), F.lit(45.0))
    vib_col = F.round(F.col("vibration_vps").cast("double"), 2) if "vibration_vps" in raw_eq_cols else F.lit(0.05)
    health_col = F.round(F.col("health").cast("double"), 2) if "health" in raw_eq_cols else (F.round(F.col("equipment_health_status").cast("double"), 2) if "equipment_health_status" in raw_eq_cols else F.lit(98.0))
    load_col = F.round(F.col("current_load").cast("double"), 1) if "current_load" in raw_eq_cols else (F.round(F.col("current_load_percent").cast("double"), 1) if "current_load_percent" in raw_eq_cols else F.lit(50.0))
    pwr_col = F.round(F.col("power_consumption_kw").cast("double"), 2) if "power_consumption_kw" in raw_eq_cols else F.lit(5.5)
    fail_col = F.round(F.col("failure_probability").cast("double"), 4) if "failure_probability" in raw_eq_cols else F.lit(0.01)
    runtime_col = F.round(F.col("runtime_hours").cast("double"), 1) if "runtime_hours" in raw_eq_cols else F.lit(120.0)
    eq_type_col = F.col("equipment_type") if "equipment_type" in raw_eq_cols else F.lit("HVAC")
    mfr_col = F.col("manufacturer") if "manufacturer" in raw_eq_cols else F.lit("HydroPump Corp")
    model_col = F.col("model_number") if "model_number" in raw_eq_cols else F.lit("HP-3000X")
    status_col = F.col("operating_status") if "operating_status" in raw_eq_cols else F.lit("RUNNING")
    eq_contact_col = F.coalesce(F.trim(F.col("operator_contact")), F.lit("tech.support@smartfarm.ph")) if "operator_contact" in raw_eq_cols else F.lit("tech.support@smartfarm.ph")
    eq_phone_col = F.coalesce(F.trim(F.col("operator_phone")), F.lit("+639178452190")) if "operator_phone" in raw_eq_cols else F.lit("+639178452190")
    
    df_silver_eq = (
        df_new_eq
        .withColumn("equipment_id", eq_id_clean)
        .withColumn("facility_id", fac_clean)
        .withColumn("zone_id", zone_clean)
        .withColumn("operating_temp_c", temp_clean)
        .withColumn("vibration_vps", vib_col)
        .withColumn("equipment_health_status", health_col)
        .withColumn("current_load_percent", load_col)
        .withColumn("power_consumption_kw", pwr_col)
        .withColumn("failure_probability", fail_col)
        .withColumn("runtime_hours", runtime_col)
        .withColumn("equipment_type", eq_type_col)
        .withColumn("manufacturer", mfr_col)
        .withColumn("model_number", model_col)
        .withColumn("operating_status", status_col)
        .withColumn("operator_contact", eq_contact_col)
        .withColumn("operator_phone", eq_phone_col)
        .drop_duplicates(["event_id"])
    )
    df_silver_eq = enrich_facility_info(df_silver_eq).select(
        "event_id", "facility_id", "facility_name", "region", "zone_id",
        "equipment_id", "equipment_type", "manufacturer", "model_number",
        "operating_status", "operating_temp_c", "vibration_vps",
        "current_load_percent", "power_consumption_kw", "equipment_health_status",
        "failure_probability", "runtime_hours", "operator_contact",
        "operator_phone", "timestamp"
    )
    DeltaTable.forName(spark, "silver.equipment_risk_cleaned").alias("t").merge(
        df_silver_eq.alias("s"), "t.event_id = s.event_id"
    ).whenMatchedUpdateAll().whenNotMatchedInsertAll().execute()
    
    # Gold Aggregation
    df_eq_agg = (
        df_silver_eq
        .withColumn("date_key", F.date_format("timestamp", "yyyyMMdd").cast("int"))
        .withColumn("event_date", F.to_date("timestamp"))
        .groupBy("date_key", "event_date", "facility_id", "equipment_id", "zone_id")
        .agg(
            F.round(F.avg("equipment_health_status"), 1).alias("avg_health_score"),
            F.round(F.max("failure_probability"), 4).alias("max_failure_probability"),
            F.round(F.greatest(F.lit(0.0), F.max("runtime_hours") - F.min("runtime_hours")), 2).alias("daily_runtime_hours"),
            F.round(F.avg("power_consumption_kw"), 2).alias("avg_power_draw_kw"),
            F.round(F.avg("vibration_vps"), 3).alias("avg_vibration_vps"),
            F.round(F.avg("operating_temp_c"), 2).alias("avg_operating_temp_celsius"),
            F.round(F.avg("current_load_percent"), 1).alias("avg_load_percent"),
            F.count("event_id").alias("telemetry_sample_count")
        )
        .withColumn("total_energy_kwh", F.round(F.col("avg_power_draw_kw") * F.col("daily_runtime_hours"), 2))
    )
    
    df_gold_eq = df_eq_agg.alias("fact")
    if dim_fac_bcast is not None:
        df_gold_eq = df_gold_eq.join(dim_fac_bcast.alias("f"), (F.col("fact.facility_id") == F.col("f.facility_id")) & (F.col("fact.event_date") >= F.col("f.effective_date")) & (F.col("fact.event_date") <= F.col("f.expiration_date")), "left")
    else:
        df_gold_eq = df_gold_eq.withColumn("f.facility_key", F.lit(-1))

    if dim_eq_bcast is not None:
        df_gold_eq = df_gold_eq.join(dim_eq_bcast.alias("e"), (F.col("fact.equipment_id") == F.col("e.equipment_id")) & (F.col("fact.event_date") >= F.col("e.effective_date")) & (F.col("fact.event_date") <= F.col("e.expiration_date")), "left")
    else:
        df_gold_eq = df_gold_eq.withColumn("e.equipment_key", F.lit(-1))

    if dim_zone_bcast is not None:
        df_gold_eq = df_gold_eq.join(dim_zone_bcast.alias("z"), (F.col("f.facility_key") == F.col("z.facility_key")) & (F.col("fact.zone_id") == F.col("z.zone_id")) & (F.col("fact.event_date") >= F.col("z.effective_date")) & (F.col("fact.event_date") <= F.col("z.expiration_date")), "left")
    else:
        df_gold_eq = df_gold_eq.withColumn("z.zone_key", F.lit(-1))

    df_gold_eq_final = df_gold_eq.select(
        F.col("fact.date_key"),
        F.coalesce(F.col("f.facility_key"), F.lit(-1)).alias("facility_key"),
        F.coalesce(F.col("e.equipment_key"), F.lit(-1)).alias("equipment_key"),
        F.coalesce(F.col("z.zone_key"), F.lit(-1)).alias("zone_key"),
        F.col("fact.avg_health_score"),
        F.col("fact.max_failure_probability"),
        F.col("fact.daily_runtime_hours"),
        F.col("fact.avg_power_draw_kw"),
        F.col("fact.total_energy_kwh"),
        F.col("fact.avg_vibration_vps"),
        F.col("fact.avg_operating_temp_celsius"),
        F.col("fact.avg_load_percent"),
        F.col("fact.telemetry_sample_count"),
        F.current_timestamp().alias("created_timestamp"),
        F.lit(PIPELINE_RUN_DATE).alias("pipeline_run_date")
    ).drop_duplicates(["date_key", "facility_key", "equipment_key", "zone_key"]) # Strict MERGE key deduplication
    
    DeltaTable.forName(spark, "gold.fact_equipment_telemetry").alias("t").merge(
        df_gold_eq_final.alias("s"), "t.date_key = s.date_key AND t.facility_key = s.facility_key AND t.equipment_key = s.equipment_key AND t.zone_key = s.zone_key"
    ).whenMatchedUpdateAll().whenNotMatchedInsertAll().execute()
    
    max_ts_eq = df_new_eq.select(F.max(time_col_eq)).collect()[0][0]
    set_watermark("equipment_telemetry", max_ts_eq)
    print(f"Equipment: Merged {cnt_eq:,} rows into equipment_risk_cleaned & fact_equipment_telemetry.")


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Crop Biological

df_new_cr, cnt_cr, time_col_cr = extract_incremental_stream(["CropTelemetry", "Files/CropTelemetry", "bronze.crop_telemetry"], "crop_telemetry")
if df_new_cr is not None and cnt_cr > 0:
    total_processed_rows += cnt_cr
    raw_cr_cols = df_new_cr.columns
    fac_clean = F.when(F.col("facility_id").isNull() | F.upper(F.trim(F.col("facility_id"))).isin("", "N/A", "UNKNOWN"), F.lit("UNKNOWN_FACILITY")).otherwise(F.upper(F.trim(F.col("facility_id"))))
    zone_clean = F.when(F.col("zone_id").isNull() | F.upper(F.trim(F.col("zone_id"))).isin("", "N/A", "UNKNOWN"), F.lit("ZONE-UNKNOWN")).otherwise(F.upper(F.trim(F.col("zone_id"))))
    
    crop_batch_col = F.col("crop_batch_id") if "crop_batch_id" in raw_cr_cols else F.lit("BATCH-001")
    crop_type_col = F.col("crop_type") if "crop_type" in raw_cr_cols else F.lit("BUTTERHEAD_LETTUCE")
    stage_col = F.col("lifecycle_stage") if "lifecycle_stage" in raw_cr_cols else F.lit("VEGETATIVE")
    age_col = F.round(F.col("age_days").cast("double"), 1) if "age_days" in raw_cr_cols else F.lit(15.0)
    health_col = F.round(F.col("health_score").cast("double"), 1) if "health_score" in raw_cr_cols else F.lit(95.0)
    growth_col = F.round(F.col("growth_rate").cast("double"), 2) if "growth_rate" in raw_cr_cols else F.lit(2.5)
    biomass_col = F.round(F.col("biomass_grams").cast("double"), 2) if "biomass_grams" in raw_cr_cols else F.lit(150.0)
    
    stress_val = (
        F.round(F.col("environmental_stress_index").cast("double") * F.lit(100.0), 1)
        if "environmental_stress_index" in raw_cr_cols
        else (
            F.round(F.col("biological_stress_percent").cast("double"), 1)
            if "biological_stress_percent" in raw_cr_cols
            else F.lit(5.0)
        )
    )
    
    water_col = F.round(F.col("water_consumption_liters").cast("double"), 2) if "water_consumption_liters" in raw_cr_cols else F.lit(25.0)
    nutr_col = F.round(F.col("nutrient_consumption_grams").cast("double"), 2) if "nutrient_consumption_grams" in raw_cr_cols else F.lit(50.0)
    temp_col = F.round(F.col("ambient_temperature_celsius").cast("double"), 2) if "ambient_temperature_celsius" in raw_cr_cols else F.lit(22.0)
    humid_col = F.round(F.col("ambient_humidity_percent").cast("double"), 1) if "ambient_humidity_percent" in raw_cr_cols else F.lit(65.0)
    contact_col = F.coalesce(F.trim(F.col("operator_contact")), F.lit("agronomy.lead@smartfarm.ph")) if "operator_contact" in raw_cr_cols else F.lit("agronomy.lead@smartfarm.ph")
    phone_col = F.coalesce(F.trim(F.col("operator_phone")), F.lit("+639178452190")) if "operator_phone" in raw_cr_cols else F.lit("+639178452190")
    
    df_silver_cr = (
        df_new_cr
        .withColumn("facility_id", fac_clean)
        .withColumn("zone_id", zone_clean)
        .withColumn("crop_batch_id", crop_batch_col)
        .withColumn("crop_type", crop_type_col)
        .withColumn("lifecycle_stage", stage_col)
        .withColumn("age_days", age_col)
        .withColumn("crop_health_score", health_col)
        .withColumn("growth_rate_g_day", growth_col)
        .withColumn("biomass_g", biomass_col)
        .withColumn("biological_stress_pct", stress_val)
        .withColumn("water_consumption_liters", water_col)
        .withColumn("nutrient_consumption_grams", nutr_col)
        .withColumn("ambient_temperature_celsius", temp_col)
        .withColumn("ambient_humidity_percent", humid_col)
        .withColumn("operator_contact", contact_col)
        .withColumn("operator_phone", phone_col)
        .drop_duplicates(["event_id"])
    )
    df_silver_cr = enrich_facility_info(df_silver_cr).select(
        "event_id", "facility_id", "facility_name", "region", "zone_id",
        "crop_batch_id", "crop_type", "lifecycle_stage", "age_days",
        "crop_health_score", "growth_rate_g_day", "biomass_g",
        "biological_stress_pct", "water_consumption_liters",
        "nutrient_consumption_grams", "ambient_temperature_celsius",
        "ambient_humidity_percent", "operator_contact", "operator_phone", "timestamp"
    )
    DeltaTable.forName(spark, "silver.crop_biological_cleaned").alias("t").merge(
        df_silver_cr.alias("s"), "t.event_id = s.event_id"
    ).whenMatchedUpdateAll().whenNotMatchedInsertAll().execute()
    
    RACK_PLANT_DENSITY = 250.0
    df_yield_agg = (
        df_silver_cr
        .withColumn("event_date", F.to_date("timestamp"))
        .withColumn("date_key", F.date_format("timestamp", "yyyyMMdd").cast("int"))
        .groupBy("date_key", "event_date", "facility_id", "zone_id", F.upper(F.col("crop_type")).alias("crop_id"))
        .agg(
            F.round(F.max("biomass_g") * RACK_PLANT_DENSITY / 1000.0, 2).alias("target_yield_kg"),
            F.round(F.avg("biomass_g") * RACK_PLANT_DENSITY / 1000.0, 2).alias("total_harvest_kg"),
            F.round(F.avg(F.col("biomass_g") * 0.80) * RACK_PLANT_DENSITY / 1000.0, 2).alias("grade_a_harvest_kg"),
            F.round(F.avg(F.col("biomass_g") * 0.15) * RACK_PLANT_DENSITY / 1000.0, 2).alias("grade_b_harvest_kg"),
            F.round(F.avg(F.col("biomass_g") * 0.05) * RACK_PLANT_DENSITY / 1000.0, 2).alias("spoilage_waste_kg"),
            F.round(F.avg("growth_rate_g_day"), 2).alias("avg_growth_rate_g_day"),
            F.count("event_id").alias("harvest_batch_count")
        )
        .withColumn("yield_achievement_pct", F.lit(100.0))
        .withColumn("estimated_revenue_php", F.round(F.col("grade_a_harvest_kg") * 480.0 + F.col("grade_b_harvest_kg") * 312.0, 2))
    )
    
    df_gold_crop = df_yield_agg.alias("fact")
    if dim_fac_bcast is not None:
        df_gold_crop = df_gold_crop.join(dim_fac_bcast.alias("f"), (F.col("fact.facility_id") == F.col("f.facility_id")) & (F.col("fact.event_date") >= F.col("f.effective_date")) & (F.col("fact.event_date") <= F.col("f.expiration_date")), "left")
    else:
        df_gold_crop = df_gold_crop.withColumn("f.facility_key", F.lit(-1))

    if dim_zone_bcast is not None:
        df_gold_crop = df_gold_crop.join(dim_zone_bcast.alias("z"), (F.col("f.facility_key") == F.col("z.facility_key")) & (F.col("fact.zone_id") == F.col("z.zone_id")) & (F.col("fact.event_date") >= F.col("z.effective_date")) & (F.col("fact.event_date") <= F.col("z.expiration_date")), "left")
    else:
        df_gold_crop = df_gold_crop.withColumn("z.zone_key", F.lit(-1))

    if dim_crop_bcast is not None:
        df_gold_crop = df_gold_crop.join(dim_crop_bcast.alias("c"), F.col("fact.crop_id") == F.col("c.crop_id"), "left")
    else:
        df_gold_crop = df_gold_crop.withColumn("c.crop_key", F.lit(-1))

    df_gold_crop_final = df_gold_crop.select(
        F.col("fact.date_key"),
        F.coalesce(F.col("f.facility_key"), F.lit(-1)).alias("facility_key"),
        F.coalesce(F.col("z.zone_key"), F.lit(-1)).alias("zone_key"),
        F.coalesce(F.col("c.crop_key"), F.lit(-1)).alias("crop_key"),
        F.col("fact.target_yield_kg"), F.col("fact.total_harvest_kg"), F.col("fact.grade_a_harvest_kg"),
        F.col("fact.grade_b_harvest_kg"), F.col("fact.spoilage_waste_kg"), F.col("fact.yield_achievement_pct"),
        F.col("fact.estimated_revenue_php"), F.col("fact.avg_growth_rate_g_day"), F.col("fact.harvest_batch_count"),
        F.current_timestamp().alias("created_timestamp"), F.lit(PIPELINE_RUN_DATE).alias("pipeline_run_date")
    ).drop_duplicates(["date_key", "facility_key", "zone_key", "crop_key"]) # 🛡️ Strict MERGE key deduplication
    
    DeltaTable.forName(spark, "gold.fact_crop_yield").alias("t").merge(
        df_gold_crop_final.alias("s"), "t.date_key = s.date_key AND t.facility_key = s.facility_key AND t.zone_key = s.zone_key AND t.crop_key = s.crop_key"
    ).whenMatchedUpdateAll().whenNotMatchedInsertAll().execute()
    
    max_ts_cr = df_new_cr.select(F.max(time_col_cr)).collect()[0][0]
    set_watermark("crop_telemetry", max_ts_cr)
    print(f"Crop: Merged {cnt_cr:,} rows into crop_biological_cleaned & fact_crop_yield.")


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Irrigation, Lighting, and Maintenance

# 1. Irrigation
df_new_irr, cnt_irr, time_col_irr = extract_incremental_stream(["IrrigationTelemetry", "Files/IrrigationTelemetry", "bronze.irrigation_telemetry"], "irrigation_telemetry")
if df_new_irr is not None and cnt_irr > 0:
    total_processed_rows += cnt_irr
    raw_irr_cols = df_new_irr.columns
    fac_clean = F.when(F.col("facility_id").isNull() | F.upper(F.trim(F.col("facility_id"))).isin("", "N/A", "UNKNOWN"), F.lit("UNKNOWN_FACILITY")).otherwise(F.upper(F.trim(F.col("facility_id"))))
    zone_clean = F.when(F.col("zone_id").isNull() | F.upper(F.trim(F.col("zone_id"))).isin("", "N/A", "UNKNOWN"), F.lit("ZONE-UNKNOWN")).otherwise(F.upper(F.trim(F.col("zone_id"))))
    raw_ts_str = F.regexp_replace(F.trim(F.col("timestamp").cast("string")), "[\"']", "")
    ts_clean = F.coalesce(F.to_timestamp(raw_ts_str), F.to_timestamp(raw_ts_str, "yyyy-MM-dd'T'HH:mm:ss'Z'"), F.current_timestamp())
    
    active_col = F.col("irrigation_active").cast("boolean") if "irrigation_active" in raw_irr_cols else F.lit(True)
    flow_col = F.round(F.col("flow_rate_liters_per_minute").cast("double"), 2) if "flow_rate_liters_per_minute" in raw_irr_cols else (F.round(F.col("flow_lpm").cast("double"), 2) if "flow_lpm" in raw_irr_cols else F.lit(12.5))
    press_col = F.round(F.col("pressure_kpa").cast("double"), 1) if "pressure_kpa" in raw_irr_cols else F.lit(210.0)
    dur_col = F.col("irrigation_duration_seconds").cast("int") if "irrigation_duration_seconds" in raw_irr_cols else F.lit(300)
    water_col = F.round(F.col("water_delivered_liters").cast("double"), 2) if "water_delivered_liters" in raw_irr_cols else F.lit(62.5)
    nutr_col = F.round(F.col("nutrient_solution_delivered_liters").cast("double"), 2) if "nutrient_solution_delivered_liters" in raw_irr_cols else F.lit(5.0)
    irr_contact = F.coalesce(F.trim(F.col("operator_contact")), F.lit("hydro.tech@smartfarm.ph")) if "operator_contact" in raw_irr_cols else F.lit("hydro.tech@smartfarm.ph")
    irr_phone = F.coalesce(F.trim(F.col("operator_phone")), F.lit("+639178452190")) if "operator_phone" in raw_irr_cols else F.lit("+639178452190")
    
    df_silver_irr = (
        df_new_irr
        .withColumn("facility_id", fac_clean)
        .withColumn("zone_id", zone_clean)
        .withColumn("timestamp", ts_clean)
        .withColumn("irrigation_active", active_col)
        .withColumn("flow_lpm", flow_col)
        .withColumn("pressure_kpa", press_col)
        .withColumn("irrigation_duration_seconds", dur_col)
        .withColumn("water_delivered_liters", water_col)
        .withColumn("nutrient_solution_delivered_liters", nutr_col)
        .withColumn("operator_contact", irr_contact)
        .withColumn("operator_phone", irr_phone)
        .drop_duplicates(["event_id"])
    )
    df_silver_irr = enrich_facility_info(df_silver_irr).select(
        "event_id", "facility_id", "facility_name", "region", "zone_id",
        "irrigation_active", "flow_lpm", "pressure_kpa",
        "irrigation_duration_seconds", "water_delivered_liters",
        "nutrient_solution_delivered_liters", "operator_contact",
        "operator_phone", "timestamp"
    )
    DeltaTable.forName(spark, "silver.irrigation_flow_cleaned").alias("t").merge(
        df_silver_irr.alias("s"), "t.event_id = s.event_id"
    ).whenMatchedUpdateAll().whenNotMatchedInsertAll().execute()
    
    df_irr_agg = (
        df_silver_irr
        .filter(F.col("facility_id").rlike("^FAC-[0-9]{3}$") & F.col("zone_id").rlike("^ZONE-[0-9]{3}$"))
        .withColumn("event_date", F.to_date(F.col("timestamp")))
        .withColumn("date_key", F.date_format(F.col("timestamp"), "yyyyMMdd").cast("int"))
        .groupBy("date_key", "event_date", "facility_id", "zone_id")
        .agg(
            F.round(F.avg("flow_lpm"), 2).alias("avg_flow_rate_lpm"),
            F.round(F.sum("water_delivered_liters"), 2).alias("total_water_delivered_liters"),
            F.round(F.sum("nutrient_solution_delivered_liters"), 2).alias("total_nutrient_solution_liters"),
            F.round(F.avg("pressure_kpa"), 2).alias("avg_pressure_kpa"),
            F.round(F.sum("irrigation_duration_seconds") / 60.0, 2).alias("total_irrigation_duration_min"),
            F.count("event_id").alias("telemetry_sample_count")
        )
    )
    df_gold_irr = df_irr_agg.alias("fact")
    if dim_fac_bcast is not None:
        df_gold_irr = df_gold_irr.join(dim_fac_bcast.alias("dim_fac"), (F.col("fact.facility_id") == F.col("dim_fac.facility_id")) & (F.col("fact.event_date") >= F.col("dim_fac.effective_date")) & (F.col("fact.event_date") <= F.col("dim_fac.expiration_date")), how="left")
    else:
        df_gold_irr = df_gold_irr.withColumn("dim_fac.facility_key", F.lit(-1))
        
    if dim_zone_bcast is not None:
        df_gold_irr = df_gold_irr.join(dim_zone_bcast.alias("dim_zn"), (F.col("dim_fac.facility_key") == F.col("dim_zn.facility_key")) & (F.col("fact.zone_id") == F.col("dim_zn.zone_id")) & (F.col("fact.event_date") >= F.col("dim_zn.effective_date")) & (F.col("fact.event_date") <= F.col("dim_zn.expiration_date")), how="left")
    else:
        df_gold_irr = df_gold_irr.withColumn("dim_zn.zone_key", F.lit(-1))

    df_gold_irr_final = df_gold_irr.select(
        F.col("fact.date_key"),
        F.coalesce(F.col("dim_fac.facility_key"), F.lit(-1)).alias("facility_key"),
        F.coalesce(F.col("dim_zn.zone_key"), F.lit(-1)).alias("zone_key"),
        F.col("fact.avg_flow_rate_lpm"), F.col("fact.total_water_delivered_liters"), F.col("fact.total_nutrient_solution_liters"),
        F.col("fact.avg_pressure_kpa"), F.col("fact.total_irrigation_duration_min"), F.col("fact.telemetry_sample_count"),
        F.current_timestamp().alias("created_timestamp"), F.lit(PIPELINE_RUN_DATE).alias("pipeline_run_date")
    ).drop_duplicates(["date_key", "facility_key", "zone_key"]) # Strict MERGE key deduplication
    
    DeltaTable.forName(spark, "gold.fact_irrigation_daily").alias("t").merge(
        df_gold_irr_final.alias("s"), "t.date_key = s.date_key AND t.facility_key = s.facility_key AND t.zone_key = s.zone_key"
    ).whenMatchedUpdateAll().whenNotMatchedInsertAll().execute()
    max_ts_irr = df_new_irr.select(F.max(time_col_irr)).collect()[0][0]
    set_watermark("irrigation_telemetry", max_ts_irr)

# 2. Lighting
df_new_lt, cnt_lt, time_col_lt = extract_incremental_stream(["LightingTelemetry", "Files/LightingTelemetry", "bronze.lighting_telemetry"], "lighting_telemetry")
if df_new_lt is not None and cnt_lt > 0:
    total_processed_rows += cnt_lt
    raw_lt_cols = df_new_lt.columns
    fac_clean = F.when(F.col("facility_id").isNull() | F.upper(F.trim(F.col("facility_id"))).isin("", "N/A", "UNKNOWN"), F.lit("UNKNOWN_FACILITY")).otherwise(F.upper(F.trim(F.col("facility_id"))))
    zone_clean = F.when(F.col("zone_id").isNull() | F.upper(F.trim(F.col("zone_id"))).isin("", "N/A", "UNKNOWN"), F.lit("ZONE-UNKNOWN")).otherwise(F.upper(F.trim(F.col("zone_id"))))
    raw_ts_str = F.regexp_replace(F.trim(F.col("timestamp").cast("string")), "[\"']", "")
    ts_clean = F.coalesce(F.to_timestamp(raw_ts_str), F.to_timestamp(raw_ts_str, "yyyy-MM-dd'T'HH:mm:ss'Z'"), F.current_timestamp())
    
    lt_active = F.col("lighting_enabled").cast("boolean") if "lighting_enabled" in raw_lt_cols else F.lit(True)
    lt_intensity = F.round(F.col("lighting_intensity_percent").cast("double"), 1) if "lighting_intensity_percent" in raw_lt_cols else F.lit(85.0)
    lt_period = F.round(F.col("photoperiod_hours").cast("double"), 1) if "photoperiod_hours" in raw_lt_cols else F.lit(16.0)
    lt_dli = F.round(F.col("daily_light_integral").cast("double"), 2) if "daily_light_integral" in raw_lt_cols else (F.round(F.col("dli_mol_m2_day").cast("double"), 2) if "dli_mol_m2_day" in raw_lt_cols else F.lit(18.5))
    lt_contact = F.coalesce(F.trim(F.col("operator_contact")), F.lit("elec.tech@smartfarm.ph")) if "operator_contact" in raw_lt_cols else F.lit("elec.tech@smartfarm.ph")
    lt_phone = F.coalesce(F.trim(F.col("operator_phone")), F.lit("+639178452190")) if "operator_phone" in raw_lt_cols else F.lit("+639178452190")
    
    df_silver_lt = (
        df_new_lt
        .withColumn("facility_id", fac_clean)
        .withColumn("zone_id", zone_clean)
        .withColumn("timestamp", ts_clean)
        .withColumn("lighting_enabled", lt_active)
        .withColumn("lighting_intensity_percent", lt_intensity)
        .withColumn("photoperiod_hours", lt_period)
        .withColumn("dli_mol_m2_day", lt_dli)
        .withColumn("operator_contact", lt_contact)
        .withColumn("operator_phone", lt_phone)
        .drop_duplicates(["event_id"])
    )
    df_silver_lt = enrich_facility_info(df_silver_lt).select(
        "event_id", "facility_id", "facility_name", "region", "zone_id",
        "lighting_enabled", "lighting_intensity_percent",
        "photoperiod_hours", "dli_mol_m2_day", "operator_contact",
        "operator_phone", "timestamp"
    )
    DeltaTable.forName(spark, "silver.lighting_dli_cleaned").alias("t").merge(
        df_silver_lt.alias("s"), "t.event_id = s.event_id"
    ).whenMatchedUpdateAll().whenNotMatchedInsertAll().execute()
    
    df_lt_agg = (
        df_silver_lt
        .filter(F.col("facility_id").rlike("^FAC-[0-9]{3}$") & F.col("zone_id").rlike("^ZONE-[0-9]{3}$"))
        .withColumn("event_date", F.to_date(F.col("timestamp")))
        .withColumn("date_key", F.date_format(F.col("timestamp"), "yyyyMMdd").cast("int"))
        .groupBy("date_key", "event_date", "facility_id", "zone_id")
        .agg(
            F.round(F.avg("dli_mol_m2_day"), 2).alias("avg_daily_light_integral"),
            F.round(F.max("dli_mol_m2_day"), 2).alias("max_daily_light_integral"),
            F.round(F.avg("lighting_intensity_percent"), 1).alias("avg_lighting_intensity_pct"),
            F.round(F.avg("photoperiod_hours"), 1).alias("avg_photoperiod_hours"),
            F.count("event_id").alias("telemetry_sample_count")
        )
    )
    df_gold_lt = df_lt_agg.alias("fact")
    if dim_fac_bcast is not None:
        df_gold_lt = df_gold_lt.join(dim_fac_bcast.alias("dim_fac"), (F.col("fact.facility_id") == F.col("dim_fac.facility_id")) & (F.col("fact.event_date") >= F.col("dim_fac.effective_date")) & (F.col("fact.event_date") <= F.col("dim_fac.expiration_date")), how="left")
    else:
        df_gold_lt = df_gold_lt.withColumn("dim_fac.facility_key", F.lit(-1))
        
    if dim_zone_bcast is not None:
        df_gold_lt = df_gold_lt.join(dim_zone_bcast.alias("dim_zn"), (F.col("dim_fac.facility_key") == F.col("dim_zn.facility_key")) & (F.col("fact.zone_id") == F.col("dim_zn.zone_id")) & (F.col("fact.event_date") >= F.col("dim_zn.effective_date")) & (F.col("fact.event_date") <= F.col("dim_zn.expiration_date")), how="left")
    else:
        df_gold_lt = df_gold_lt.withColumn("dim_zn.zone_key", F.lit(-1))

    df_gold_lt_final = df_gold_lt.select(
        F.col("fact.date_key"),
        F.coalesce(F.col("dim_fac.facility_key"), F.lit(-1)).alias("facility_key"),
        F.coalesce(F.col("dim_zn.zone_key"), F.lit(-1)).alias("zone_key"),
        F.col("fact.avg_daily_light_integral"), F.col("fact.max_daily_light_integral"),
        F.col("fact.avg_lighting_intensity_pct"), F.col("fact.avg_photoperiod_hours"), F.col("fact.telemetry_sample_count"),
        F.current_timestamp().alias("created_timestamp"), F.lit(PIPELINE_RUN_DATE).alias("pipeline_run_date")
    ).drop_duplicates(["date_key", "facility_key", "zone_key"]) # Strict MERGE key deduplication
    
    DeltaTable.forName(spark, "gold.fact_lighting_dli_daily").alias("t").merge(
        df_gold_lt_final.alias("s"), "t.date_key = s.date_key AND t.facility_key = s.facility_key AND t.zone_key = s.zone_key"
    ).whenMatchedUpdateAll().whenNotMatchedInsertAll().execute()
    max_ts_lt = df_new_lt.select(F.max(time_col_lt)).collect()[0][0]
    set_watermark("lighting_telemetry", max_ts_lt)

# 3. Maintenance
df_new_maint, cnt_maint, time_col_maint = extract_incremental_stream(["MaintenanceActivity", "Files/MaintenanceActivity", "bronze.maintenance_activity"], "maintenance_activity")
if df_new_maint is not None and cnt_maint > 0:
    total_processed_rows += cnt_maint
    raw_maint_cols = df_new_maint.columns
    fac_clean = F.when(F.col("facility_id").isNull() | F.upper(F.trim(F.col("facility_id"))).isin("", "N/A", "UNKNOWN"), F.lit("UNKNOWN_FACILITY")).otherwise(F.upper(F.trim(F.col("facility_id"))))
    zone_clean = F.when(F.col("zone_id").isNull() | F.upper(F.trim(F.col("zone_id"))).isin("", "N/A", "UNKNOWN"), F.lit("ZONE-UNKNOWN")).otherwise(F.upper(F.trim(F.col("zone_id"))))
    
    raw_eq_id = F.upper(F.trim(F.col("equipment_id"))) if "equipment_id" in raw_maint_cols else F.lit("UNREGISTERED_ASSET")
    eq_id_clean = F.when(raw_eq_id.isNull() | raw_eq_id.contains("ORPHAN"), F.lit("UNREGISTERED_ASSET")).otherwise(raw_eq_id)
    raw_ts_str = F.regexp_replace(F.trim(F.col("timestamp").cast("string")), "[\"']", "")
    ts_clean = F.coalesce(F.to_timestamp(raw_ts_str), F.to_timestamp(raw_ts_str, "yyyy-MM-dd'T'HH:mm:ss'Z'"), F.current_timestamp())
    
    wo_id = F.trim(F.col("work_order_id")) if "work_order_id" in raw_maint_cols else F.lit("WO-0001")
    m_type = F.trim(F.col("maintenance_type")) if "maintenance_type" in raw_maint_cols else F.lit("PREVENTATIVE")
    prio = F.upper(F.trim(F.col("priority"))) if "priority" in raw_maint_cols else F.lit("MEDIUM")
    tech = F.trim(F.col("assigned_technician")) if "assigned_technician" in raw_maint_cols else F.lit("Juan Dela Cruz")
    maint_status_clean = F.upper(F.trim(F.col("maintenance_status"))) if "maintenance_status" in raw_maint_cols else F.lit("COMPLETED")
    est_dur = F.col("estimated_duration_minutes").cast("int") if "estimated_duration_minutes" in raw_maint_cols else F.lit(60)
    rem_dur = F.col("remaining_duration_minutes").cast("int") if "remaining_duration_minutes" in raw_maint_cols else F.lit(0)
    comp_pct = F.round(F.col("completion_percent").cast("double"), 1) if "completion_percent" in raw_maint_cols else F.lit(100.0)
    is_active_calc = F.when(maint_status_clean == "COMPLETED", F.lit(False)).otherwise(F.lit(True))
    notes = F.trim(F.col("technician_notes")) if "technician_notes" in raw_maint_cols else F.lit("Routine service completed.")
    health_rst = F.round(F.col("health_restored").cast("double"), 1) if "health_restored" in raw_maint_cols else F.lit(15.0)
    lag_calc = est_dur.cast("long") - rem_dur.cast("long")
    maint_contact = F.coalesce(F.trim(F.col("operator_contact")), F.lit("maint.lead@smartfarm.ph")) if "operator_contact" in raw_maint_cols else F.lit("maint.lead@smartfarm.ph")
    maint_phone = F.coalesce(F.trim(F.col("operator_phone")), F.lit("+639178452190")) if "operator_phone" in raw_maint_cols else F.lit("+639178452190")
    
    df_silver_maint = (
        df_new_maint
        .withColumn("facility_id", fac_clean)
        .withColumn("zone_id", zone_clean)
        .withColumn("equipment_id", eq_id_clean)
        .withColumn("timestamp", ts_clean)
        .withColumn("work_order_id", wo_id)
        .withColumn("maintenance_type", m_type)
        .withColumn("priority", prio)
        .withColumn("assigned_technician", tech)
        .withColumn("maintenance_status", maint_status_clean)
        .withColumn("estimated_duration_minutes", est_dur)
        .withColumn("remaining_duration_minutes", rem_dur)
        .withColumn("completion_percent", comp_pct)
        .withColumn("is_active", is_active_calc)
        .withColumn("technician_notes", notes)
        .withColumn("health_restored", health_rst)
        .withColumn("resolution_lag_min", lag_calc)
        .withColumn("operator_contact", maint_contact)
        .withColumn("operator_phone", maint_phone)
        .drop_duplicates(["event_id"])
    )
    df_silver_maint = enrich_facility_info(df_silver_maint).select(
        "event_id", "facility_id", "facility_name", "region", "zone_id",
        "equipment_id", "work_order_id", "maintenance_type", "priority",
        "assigned_technician", "maintenance_status",
        "estimated_duration_minutes", "remaining_duration_minutes",
        "completion_percent", "is_active", "technician_notes",
        "health_restored", "resolution_lag_min", "operator_contact",
        "operator_phone", "timestamp"
    )
    DeltaTable.forName(spark, "silver.maintenance_sla_cleaned").alias("t").merge(
        df_silver_maint.alias("s"), "t.event_id = s.event_id"
    ).whenMatchedUpdateAll().whenNotMatchedInsertAll().execute()
    
    df_maint_agg = (
        df_silver_maint
        .filter(F.col("facility_id").rlike("^FAC-[0-9]{3}$") & F.col("zone_id").rlike("^ZONE-[0-9]{3}$"))
        .filter((F.col("equipment_id").isNotNull()) & (F.col("equipment_id") != "UNREGISTERED_ASSET"))
        .withColumn("technician_name", F.trim(F.col("assigned_technician")))
        .withColumn("event_date", F.to_date(F.col("timestamp")))
        .withColumn("date_key", F.date_format(F.col("timestamp"), "yyyyMMdd").cast("int"))
        .groupBy("date_key", "event_date", "facility_id", "zone_id", "equipment_id", "technician_name")
        .agg(
            F.count("work_order_id").alias("work_order_count"),
            F.round(F.avg("estimated_duration_minutes"), 1).alias("avg_estimated_duration_min"),
            F.round(F.avg(F.col("estimated_duration_minutes") - F.col("remaining_duration_minutes")), 1).alias("avg_actual_duration_min"),
            F.round(F.sum("health_restored"), 1).alias("total_health_restored"),
            F.sum(F.when(F.col("maintenance_status") == "COMPLETED", 1).otherwise(0)).alias("completed_work_orders"),
            F.sum(F.when(F.col("maintenance_status") == "OVERDUE", 1).otherwise(0)).alias("overdue_work_orders")
        )
        .withColumn("sla_compliance_pct", F.when(F.col("work_order_count") > 0, F.round((F.col("completed_work_orders") * 100.0) / F.col("work_order_count"), 2)).otherwise(F.lit(100.0)))
        .withColumn("is_sla_met", F.when(F.col("overdue_work_orders") == 0, True).otherwise(False))
    )
    df_gold_maint = df_maint_agg.alias("fact")
    if dim_fac_bcast is not None:
        df_gold_maint = df_gold_maint.join(dim_fac_bcast.alias("dim_fac"), (F.col("fact.facility_id") == F.col("dim_fac.facility_id")) & (F.col("fact.event_date") >= F.col("dim_fac.effective_date")) & (F.col("fact.event_date") <= F.col("dim_fac.expiration_date")), how="left")
    else:
        df_gold_maint = df_gold_maint.withColumn("dim_fac.facility_key", F.lit(-1))

    if dim_zone_bcast is not None:
        df_gold_maint = df_gold_maint.join(dim_zone_bcast.alias("dim_zn"), (F.col("dim_fac.facility_key") == F.col("dim_zn.facility_key")) & (F.col("fact.zone_id") == F.col("dim_zn.zone_id")) & (F.col("fact.event_date") >= F.col("dim_zn.effective_date")) & (F.col("fact.event_date") <= F.col("dim_zn.expiration_date")), how="left")
    else:
        df_gold_maint = df_gold_maint.withColumn("dim_zn.zone_key", F.lit(-1))

    if dim_eq_bcast is not None:
        df_gold_maint = df_gold_maint.join(dim_eq_bcast.alias("dim_eq"), (F.col("fact.equipment_id") == F.col("dim_eq.equipment_id")) & (F.col("fact.event_date") >= F.col("dim_eq.effective_date")) & (F.col("fact.event_date") <= F.col("dim_eq.expiration_date")), how="left")
    else:
        df_gold_maint = df_gold_maint.withColumn("dim_eq.equipment_key", F.lit(-1))

    if dim_tech_bcast is not None:
        df_gold_maint = df_gold_maint.join(dim_tech_bcast.alias("dim_tech"), F.col("fact.technician_name") == F.col("dim_tech.technician_name"), how="left")
    else:
        df_gold_maint = df_gold_maint.withColumn("dim_tech.technician_key", F.lit(-1))

    df_gold_maint_final = df_gold_maint.select(
        F.col("fact.date_key"),
        F.coalesce(F.col("dim_fac.facility_key"), F.lit(-1)).alias("facility_key"),
        F.coalesce(F.col("dim_zn.zone_key"), F.lit(-1)).alias("zone_key"),
        F.coalesce(F.col("dim_eq.equipment_key"), F.lit(-1)).alias("equipment_key"),
        F.coalesce(F.col("dim_tech.technician_key"), F.lit(-1)).alias("technician_key"),
        F.col("fact.work_order_count"), F.col("fact.completed_work_orders"), F.col("fact.overdue_work_orders"),
        F.col("fact.avg_estimated_duration_min"), F.col("fact.avg_actual_duration_min"), F.col("fact.total_health_restored"),
        F.col("fact.sla_compliance_pct"), F.col("fact.is_sla_met"),
        F.current_timestamp().alias("created_timestamp"), F.lit(PIPELINE_RUN_DATE).alias("pipeline_run_date")
    ).drop_duplicates(["date_key", "facility_key", "zone_key", "equipment_key", "technician_key"]) # Strict MERGE key deduplication
    
    DeltaTable.forName(spark, "gold.fact_maintenance_sla").alias("t").merge(
        df_gold_maint_final.alias("s"), "t.date_key = s.date_key AND t.facility_key = s.facility_key AND t.zone_key = s.zone_key AND t.equipment_key = s.equipment_key AND t.technician_key = s.technician_key"
    ).whenMatchedUpdateAll().whenNotMatchedInsertAll().execute()
    max_ts_maint = df_new_maint.select(F.max(time_col_maint)).collect()[0][0]
    set_watermark("maintenance_activity", max_ts_maint)

print("Incremental Streams Merged: Irrigation, Lighting, Maintenance into Silver & Gold Facts.")


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Dead-Letter Queue Triage

df_new_dl, cnt_dl, time_col_dl = extract_incremental_stream(["DeadLetterTelemetry", "Files/DeadLetterTelemetry", "bronze.dead_letter_telemetry"], "dead_letter_telemetry")
if df_new_dl is not None and cnt_dl > 0:
    total_processed_rows += cnt_dl
    raw_cols = df_new_dl.columns
    fac_id_check = F.col("facility_id").isNull() if "facility_id" in raw_cols else F.lit(False)
    raw_exc_col = F.col("exception_reason") if "exception_reason" in raw_cols else (
        F.col("error_reason") if "error_reason" in raw_cols else F.lit(None).cast("string")
    )
    stream_raw = F.col("target_stream") if "target_stream" in raw_cols else (F.col("event_type") if "event_type" in raw_cols else F.lit("ENVIRONMENTAL_TELEMETRY"))
    raw_payload_val = F.col("raw_payload") if "raw_payload" in raw_cols else F.lit("{}")
    
    # Resolve ingestion timestamp column
    time_raw = F.col("ingestion_timestamp") if "ingestion_timestamp" in raw_cols else (F.col("timestamp") if "timestamp" in raw_cols else F.current_timestamp())
    raw_ts_str = F.regexp_replace(F.trim(time_raw.cast("string")), "[\"']", "")
    ts_clean = F.coalesce(F.to_timestamp(raw_ts_str), F.to_timestamp(raw_ts_str, "yyyy-MM-dd'T'HH:mm:ss'Z'"), F.current_timestamp())
    
    # Safe intelligent resolution of exception_reason
    ev_type_col = F.col("event_type") if "event_type" in raw_cols else F.lit("")
    sch_ver_col = F.col("schema_version") if "schema_version" in raw_cols else F.lit("")
    op_temp_col = F.col("operating_temperature_c") if "operating_temperature_c" in raw_cols else F.lit(0.0)
    sn_val_col = F.col("sensor_value") if "sensor_value" in raw_cols else F.lit(0.0)
    eq_id_col = F.col("equipment_id") if "equipment_id" in raw_cols else F.lit("")
    
    exc_reason_resolved = (
        F.when(raw_exc_col.isNotNull() & (raw_exc_col != "") & (raw_exc_col != "MISSING_PRIMARY_KEY"), raw_exc_col)
         .when((ev_type_col == "legacy.deprecated_sensor") | (sch_ver_col == "v1.0"), F.lit("DEPRECATED_SCHEMA_VERSION: v1.0 payload"))
         .when((op_temp_col > 65.0) | (sn_val_col > 65.0), F.lit("OUT_OF_BOUNDS_SENSOR_VALUE: temperature > 65C"))
         .when(eq_id_col.contains("ORPHAN") | eq_id_col.contains("99999"), F.lit("UNREGISTERED_HARDWARE_MAC_ADDRESS: unregistered device"))
         .when(raw_payload_val.contains("malformed") | raw_payload_val.contains("SERDES"), F.lit("SERDES_PARSE_FAILURE: malformed JSON payload"))
         .when(fac_id_check | (F.col("event_id").isNull()), F.lit("MISSING_PRIMARY_KEY: null facility_id"))
         .otherwise(F.lit("OUT_OF_BOUNDS_SENSOR_VALUE: temperature > 65C"))
    )

    exc_cat_expr = (
        F.when(exc_reason_resolved.contains("MISSING_PRIMARY_KEY") | fac_id_check, F.lit("CRITICAL_MISSING_PRIMARY_KEY"))
         .when(exc_reason_resolved.contains("DEPRECATED") | exc_reason_resolved.contains("SCHEMA"), F.lit("DEPRECATED_SCHEMA_EVENT"))
         .when(exc_reason_resolved.contains("SERDES") | exc_reason_resolved.contains("PARSE") | exc_reason_resolved.contains("JSON"), F.lit("SERDES_PARSE_FAILURE"))
         .when(exc_reason_resolved.contains("TIMESTAMP") | exc_reason_resolved.contains("SYNC") | exc_reason_resolved.contains("CLOCK"), F.lit("TIMESTAMP_OUT_OF_SYNC"))
         .when(exc_reason_resolved.contains("MAC") | exc_reason_resolved.contains("UNREGISTERED"), F.lit("UNREGISTERED_HARDWARE_DEVICE"))
         .otherwise(F.lit("OUT_OF_BOUNDS_ANOMALY"))
    )
    
    # 1. silver.dead_letter_classified
    df_silver_dl = (
        df_new_dl
        .withColumn("event_id", F.trim(F.col("event_id")))
        .withColumn("target_stream", F.upper(F.trim(stream_raw)))
        .withColumn("exception_category", exc_cat_expr)
        .withColumn("exception_reason", F.trim(exc_reason_resolved))
        .withColumn("is_auto_remediable", F.col("exception_category") == F.lit("DEPRECATED_SCHEMA_EVENT"))
        .withColumn("raw_payload", raw_payload_val)
        .withColumn("ingestion_timestamp", ts_clean)
        .drop_duplicates(["event_id"])
        .select("event_id", "target_stream", "exception_category", "exception_reason", "is_auto_remediable", "raw_payload", "ingestion_timestamp")
    )
    DeltaTable.forName(spark, "silver.dead_letter_classified").alias("t").merge(
        df_silver_dl.alias("s"), "t.event_id = s.event_id"
    ).whenMatchedUpdateAll().whenNotMatchedInsertAll().execute()
    
    # 2. gold.fact_dead_letter_governance (Exact Match with Notebook_Gold_ETL)
    df_dl_agg = (
        df_silver_dl
        .withColumn("date_key", F.date_format("ingestion_timestamp", "yyyyMMdd").cast("int"))
        .withColumn("event_date", F.to_date("ingestion_timestamp"))
        .withColumn("target_stream_name", F.upper(F.trim(F.col("target_stream"))))
        .withColumn("governance_exception_reason", F.trim(F.col("exception_reason")))
        .groupBy("date_key", "event_date", "target_stream_name", "governance_exception_reason")
        .agg(
            F.count("event_id").alias("dead_letter_event_count"),
            F.sum(F.when(F.col("exception_reason").contains("MISSING"), 1).otherwise(0)).alias("missing_pk_defect_count"),
            F.sum(F.when(F.col("exception_reason").contains("BOUNDS") | F.col("exception_reason").contains("TEMP"), 1).otherwise(0)).alias("out_of_bounds_defect_count"),
            F.sum(F.when(F.col("exception_reason").contains("DEPRECATED") | F.col("exception_reason").contains("SCHEMA"), 1).otherwise(0)).alias("deprecated_schema_defect_count"),
            F.sum(F.when(F.col("exception_reason").contains("JSON") | F.col("exception_reason").contains("SERDES"), 1).otherwise(0)).alias("serdes_parse_defect_count"),
            F.sum(F.when(F.col("exception_reason").contains("CLOCK") | F.col("exception_reason").contains("SYNC") | F.col("exception_reason").contains("TIMESTAMP"), 1).otherwise(0)).alias("timestamp_sync_defect_count"),
            F.sum(F.when(F.col("exception_reason").contains("MAC") | F.col("exception_reason").contains("UNREGISTERED"), 1).otherwise(0)).alias("unregistered_hardware_defect_count"),
            F.sum(F.when(F.col("exception_reason").contains("SERDES") | F.col("exception_reason").contains("BOUNDS") | F.col("exception_reason").contains("FORMAT"), 1).otherwise(0)).alias("formatting_defect_count")
        )
        .select(
            F.col("date_key"),
            F.col("target_stream_name"),
            F.col("governance_exception_reason"),
            F.col("dead_letter_event_count"),
            F.col("missing_pk_defect_count"),
            F.col("out_of_bounds_defect_count"),
            F.col("deprecated_schema_defect_count"),
            F.col("serdes_parse_defect_count"),
            F.col("timestamp_sync_defect_count"),
            F.col("unregistered_hardware_defect_count"),
            F.col("formatting_defect_count"),
            F.current_timestamp().alias("created_timestamp"),
            F.lit(PIPELINE_RUN_DATE).alias("pipeline_run_date")
        )
        .drop_duplicates(["date_key", "target_stream_name", "governance_exception_reason"])
    )
    
    DeltaTable.forName(spark, "gold.fact_dead_letter_governance").alias("t").merge(
        df_dl_agg.alias("s"), 
        "t.date_key = s.date_key AND t.target_stream_name = s.target_stream_name AND t.governance_exception_reason = s.governance_exception_reason"
    ).whenMatchedUpdateAll().whenNotMatchedInsertAll().execute()
    
    max_ts_dl = df_new_dl.select(F.max(time_col_dl)).collect()[0][0]
    set_watermark("dead_letter_telemetry", max_ts_dl)
    print(f"Dead-Letter: Triaged into silver.dead_letter_classified & gold.fact_dead_letter_governance.")


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Idempotent Observability Trace Span Flush

duration_ms = int((time.time() - t0) * 1000)

span_df = spark.createDataFrame([(
    RUN_ID, "SPN-INCSYNC", "Pipeline_Medallion_Incremental_Stream_Sync", "Incremental_MicroBatch",
    "Spark_Notebook", "SUCCESS", int(total_processed_rows), int(total_processed_rows),
    duration_ms, "", datetime.datetime.utcnow()
)], [
    "TraceId", "SpanId", "PipelineName", "StageName", "Component",
    "ExecutionStatus", "SourceRowCount", "TargetRowCount",
    "ExecutionDurationMs", "ErrorMessage", "Timestamp"
])

# Idempotent MERGE into gold.fact_dataops_pipeline_log
delta_log = DeltaTable.forName(spark, "gold.fact_dataops_pipeline_log")
(
    delta_log.alias("target")
    .merge(
        span_df.alias("source"),
        "target.TraceId = source.TraceId AND target.StageName = source.StageName"
    )
    .whenMatchedUpdateAll()
    .whenNotMatchedInsertAll()
    .execute()
)

print("==============================================================================")
print(f"INCREMENTAL MICRO-BATCH COMPLETE: Processed {total_processed_rows:,} records across all 11 Silver & 13 Gold tables in {duration_ms/1000.0:.2f}s")
print("==============================================================================")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

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

# Bronze Schema & Table Registration From OneLake Shortcuts

from pyspark.sql import functions as F

# Create customer schemas
spark.sql("CREATE SCHEMA IF NOT EXISTS bronze")
spark.sql("CREATE SCHEMA IF NOT EXISTS silver")

shortcut_table_map = {
    "CropLifecycle": "crop_lifecycle",
    "CropTelemetry": "crop_telemetry",
    "DeadLetterTelemetry": "dead_letter_telemetry",
    "EnvironmentalTelemetry": "environmental_telemetry",
    "EquipmentTelemetry": "equipment_telemetry",
    "FacilityOperations": "facility_operations",
    "IrrigationTelemetry": "irrigation_telemetry",
    "LightingTelemetry": "lighting_telemetry",
    "MaintenanceActivity": "maintenance_activity" 
}

print("Starting Incremental Bronze Sync via Native Structured Streaming...")

for k, v in shortcut_table_map.items():
    target_table = f"bronze.{v}"
    file_path = f"Files/{k}"
    checkpoint_path = f"Files/_checkpoints/bronze/{v}"

    initial_count = spark.table(target_table).count() if spark.catalog.tableExists(target_table) else 0

    # Read Stream from Onelake Shortcut Delta source natively
    df_stream = (
        spark.readStream
        .format("delta")
        .option("ignoreChanges", "true")
        .option("startingVersion", "0")
        .load(file_path)
    )

    # Write Stream incrementally using native trigger(availableNow=True)
    query = (
        df_stream.writeStream
        .format("delta")
        .outputMode("append")
        .option("checkpointLocation", checkpoint_path)
        .option("mergeSchema", "true")
        .trigger(availableNow=True)
        .toTable(target_table)
    )

    query.awaitTermination()

    final_count = spark.table(target_table).count()
    appended_rows = final_count - initial_count

    print(f"🔄 Sync Complete: {target_table:<28} | ➕ Appended: {appended_rows:>6,} rows | 📊 Total: {final_count:>10,} rows")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Shared Philippine Facility Master Lookup Dataframe

from pyspark.sql import functions as F

# Load and clean Facility Master for Lookup joins
df_facilities = (
    spark.table("bronze.facility_operations")
    .select(
        F.upper(F.col("facility_id")).alias("fac_id_join"),
        F.col("facility_name"),
        F.col("region"),
        F.col("elevation_m"),
        F.col("power_grid_redundancy")
    )
    .drop_duplicates(["fac_id_join"])
)

print(f"💾 Loaded Facility Master Lookup ({df_facilities.count()} facilities).")
df_facilities.show(5, truncate=False)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Create silver.environmental_enriched

# Anomaly cleansing expressions
facility_id_clean = F.when(
    F.col("facility_id").isNull() | F.upper(F.trim(F.col("facility_id"))).isin("", "N/A", "UNKNOWN", "NULL", "NONE"),
    F.lit("UNKNOWN_FACILITY")
).otherwise(F.upper(F.trim(F.col("facility_id"))))

zone_id_clean = F.when(
    F.col("zone_id").isNull() | F.upper(F.trim(F.col("zone_id"))).isin("", "N/A", "UNKNOWN", "NULL", "NONE"),
    F.lit("ZONE-UNKNOWN")
).otherwise(F.upper(F.trim(F.col("zone_id"))))

sensor_type_clean = F.lower(F.trim(F.col("sensor_type")))

raw_ts_str = F.regexp_replace(F.trim(F.col("timestamp").cast("string")), "[\"']", "")
timestamp_clean = F.coalesce(
    F.to_timestamp(raw_ts_str),
    F.to_timestamp(raw_ts_str, "yyyy-MM-dd HH:mm:ss"),
    F.to_timestamp(raw_ts_str, "yyyy-MM-dd'T'HH:mm:ss'Z'"),
    F.to_timestamp(F.from_unixtime(raw_ts_str.cast("bigint"))),
    F.current_timestamp()
)

# Raw Numeric Cast
val_raw = F.col("sensor_value").cast("double")

# Per-Sensor Type Physical Outlier Filter
clean_sensor_value = (
    F.when((sensor_type_clean == "air_temperature") & ((val_raw < -10.0) | (val_raw > 65.0)), F.lit(None))
    .when((sensor_type_clean == "humidity") & ((val_raw < 0.0) | (val_raw > 100.0)), F.lit(None))
    .when((sensor_type_clean == "co2") & ((val_raw < 0.0) | (val_raw > 5000.0)), F.lit(None))
    .when((sensor_type_clean == "light_intensity") & ((val_raw < 0.0) | (val_raw > 150000.0)), F.lit(None))
    .when((sensor_type_clean == "water_ph") & ((val_raw < 0.0) | (val_raw > 14.0)), F.lit(None))
    .when((sensor_type_clean == "dissolved_oxygen") & ((val_raw < 0.0) | (val_raw > 30.0)), F.lit(None))
    .when((sensor_type_clean == "electrical_conductivity") & ((val_raw < 0.0) | (val_raw > 15.0)), F.lit(None))
    .otherwise(F.round(val_raw, 2))
)

# Unit auto-resolution
unit_clean = F.coalesce(
    F.trim(F.col("unit")),
    F.when(sensor_type_clean == "air_temperature", F.lit("°C"))
    .when(sensor_type_clean == "humidity", F.lit("%"))
    .when(sensor_type_clean == "co2", F.lit("ppm"))
    .when(sensor_type_clean == "light_intensity", F.lit("lux"))
    .when(sensor_type_clean == "water_ph", F.lit("pH"))
    .when(sensor_type_clean == "dissolved_oxygen", F.lit("mg/L"))
    .when(sensor_type_clean == "electrical_conductivity", F.lit("mS/cm"))
    .otherwise(F.lit("UNKNOWN"))
)

df_telemetry_cleaned = (
    spark.table("bronze.environmental_telemetry")
    .withColumn("facility_id_upper", facility_id_clean)
    .withColumn("zone_id_clean", zone_id_clean)
    .withColumn("clean_timestamp", timestamp_clean)
    .drop_duplicates(["event_id"])
)

df_enriched = df_telemetry_cleaned.join(
    df_facilities,
    F.col("facility_id_upper") == F.col("fac_id_join"),
    "left"
)

df_env_cleaned = (
    df_enriched
    .withColumn("facility_name", F.coalesce(F.col("facility_name"), F.col("facility_id_upper")))
    .withColumn("sensor_type_clean", sensor_type_clean)
    .withColumn("sensor_value_clean", clean_sensor_value)
    .withColumn("unit_clean", unit_clean)
    .select(
        F.col("event_id"),
        F.col("facility_id_upper").alias("facility_id"),
        F.col("facility_name"),
        F.col("region"),
        F.col("zone_id_clean").alias("zone_id"),
        F.col("sensor_type_clean").alias("sensor_type"),
        F.col("sensor_value_clean").alias("sensor_value"),
        F.col("unit_clean").alias("unit"),
        F.col("weather"),
        F.col("clean_timestamp").alias("timestamp")
    )
)

df_env_cleaned.write.format("delta")\
                    .mode("overwrite")\
                    .option("overwriteSchema", "true")\
                    .saveAsTable("silver.environmental_cleaned")

print(f"✍ Created silver.environmental_cleaned ({df_env_cleaned.count()} rows).")

df_env_cleaned.show(10, truncate=False)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Create silver.environmental_metrics

df_pivoted = (
    spark.table("silver.environmental_cleaned")
    .filter(F.col("zone_id").rlike("^ZONE-[0-9]{3}$"))  # 🧹 FILTER OUT ZONE-UNKNOWN
    .withColumn("window_time", F.date_trunc("minute", F.col("timestamp")))
    .groupBy("facility_id", "facility_name", "region", "zone_id", "window_time")
    .pivot("sensor_type", ["air_temperature", "humidity", "co2", "light_intensity", "water_ph", "dissolved_oxygen", "electrical_conductivity"])
    .agg(F.avg("sensor_value"))
)

temp_c = F.coalesce(F.col("air_temperature"), F.lit(22.0))
rh_pct = F.coalesce(F.col("humidity"), F.lit(65.0))
co2_val = F.coalesce(F.col("co2"), F.lit(800.0))
light_val = F.coalesce(F.col("light_intensity"), F.lit(30000.0))
ph_val = F.coalesce(F.col("water_ph"), F.lit(6.0))
do_val = F.coalesce(F.col("dissolved_oxygen"), F.lit(8.0))
ec_val = F.coalesce(F.col("electrical_conductivity"), F.lit(2.2))

svp_kpa = F.lit(0.61078) * F.exp((F.lit(17.27) * temp_c) / (temp_c + F.lit(237.3)))
vpd_kpa_calc = F.round(svp_kpa * (F.lit(1.0) - (rh_pct / F.lit(100.0))), 3)

temp_penalty = F.abs(temp_c - F.lit(22.0)) * F.lit(2.5)
rh_penalty = F.abs(rh_pct - F.lit(65.0)) * F.lit(0.5)
vpd_penalty = F.abs(vpd_kpa_calc - F.lit(1.0)) * F.lit(20.0)
ph_penalty = F.abs(F.coalesce(F.col("water_ph"), F.lit(6.0)) - F.lit(6.0)) * F.lit(15.0)

total_penalty = temp_penalty + rh_penalty + vpd_penalty + ph_penalty
raw_composite_score = F.lit(100.0) - total_penalty

composite_stability = F.round(
    F.when(raw_composite_score < 50.0, F.lit(50.0)).otherwise(raw_composite_score), 1
)

env_status = (
    F.when(composite_stability >= 90.0, F.lit("OPTIMAL"))
    .when(composite_stability >= 75.0, F.lit("STABLE"))
    .when(composite_stability >= 60.0, F.lit("WARNING"))
    .otherwise(F.lit("CRITICAL"))
)

df_env_metrics = (
    df_pivoted
    .withColumn("air_temperature_c", F.round(temp_c, 2))
    .withColumn("humidity_pct", F.round(rh_pct, 1))
    .withColumn("co2_ppm", F.round(co2_val, 0))
    .withColumn("light_intensity_lux", F.round(light_val, 0))
    .withColumn("water_ph", F.round(ph_val, 2))
    .withColumn("dissolved_oxygen_mg_l", F.round(do_val, 1))
    .withColumn("electrical_conductivity_ms_cm", F.round(ec_val, 2))
    .withColumn("vpd_kpa", vpd_kpa_calc)
    .withColumn("temp_drift_c", F.round(temp_c - F.lit(22.0), 2))
    .withColumn("composite_stability_score", composite_stability)
    .withColumn("environmental_status", env_status)
    .select(
        F.concat_ws("_", F.col("facility_id"), F.col("zone_id"), F.date_format(F.col("window_time"), "yyyyMMddHHmmss")).alias("snapshot_id"),
        F.col("facility_id"),
        F.col("facility_name"),
        F.col("region"),
        F.col("zone_id"),
        F.col("air_temperature_c"),
        F.col("humidity_pct"),
        F.col("co2_ppm"),
        F.col("light_intensity_lux"),
        F.col("water_ph"),
        F.col("dissolved_oxygen_mg_l"),
        F.col("electrical_conductivity_ms_cm"),
        F.col("vpd_kpa"),
        F.col("temp_drift_c"),
        F.col("composite_stability_score"),
        F.col("environmental_status"),
        F.col("window_time").alias("timestamp")
    )
)

df_env_metrics.write.format("delta") \
                    .mode("overwrite") \
                    .option("overwriteSchema", "true") \
                    .saveAsTable("silver.environmental_metrics")
                    
print(f"✍ Created silver.environmental_metrics ({df_env_metrics.count()} rows.)")

df_env_metrics.show(10, truncate=False)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Create silver.equipment_risk_cleaned 

# Native anomaly cleansing expressions
facility_id_clean = F.when(
    F.col("facility_id").isNull() | F.upper(F.trim(F.col("facility_id"))).isin("", "N/A", "UNKNOWN", "NULL", "NONE"),
    F.lit("UNKNOWN_FACILITY")
).otherwise(F.upper(F.trim(F.col("facility_id"))))

zone_id_clean = F.when(
    F.col("zone_id").isNull() | F.upper(F.trim(F.col("zone_id"))).isin("", "N/A", "UNKNOWN", "NULL", "NONE"),
    F.lit("ZONE-UNKNOWN")
).otherwise(F.upper(F.trim(F.col("zone_id"))))

# Clean equipment_id (handling orphan keys like EQ-99999_ORPHAN)
raw_eq_id = F.upper(F.trim(F.col("equipment_id")))
equipment_id_clean = F.when(
    raw_eq_id.isNull() | raw_eq_id.isin("", "N/A", "UNKNOWN", "NULL", "NONE") | raw_eq_id.contains("ORPHAN"),
    F.lit("UNREGISTERED_ASSET")
).otherwise(raw_eq_id)

manufacturer_clean = F.coalesce(F.trim(F.col("manufacturer")), F.lit("GENERIC_VENDOR"))
model_clean = F.coalesce(F.trim(F.col("model_number")), F.lit("STANDARD_MODEL"))
op_status_clean = F.upper(F.coalesce(F.trim(F.col("operating_status")), F.lit("UNKNOWN_STATUS")))

# Robust Multi-Format Timestamp Cleaning (Strips quotes, spaces, and handles ISO/Epoch)
raw_ts_str = F.regexp_replace(F.trim(F.col("timestamp").cast("string")), "[\"']", "")
timestamp_clean = F.coalesce(
    F.to_timestamp(raw_ts_str),
    F.to_timestamp(raw_ts_str, "yyyy-MM-dd HH:mm:ss"),
    F.to_timestamp(raw_ts_str, "yyyy-MM-dd'T'HH:mm:ss'Z'"),
    F.to_timestamp(F.from_unixtime(raw_ts_str.cast("bigint"))),
    F.current_timestamp()
)

# Outlier filters & numeric casts
temp_clean = F.coalesce(
    F.when(
        (F.col("operating_temperature_c").cast("double") < 0.0) | (F.col("operating_temperature_c").cast("double") > 150.0),
        F.lit(None)
    ).otherwise(F.round(F.col("operating_temperature_c").cast("double"), 2)),
    F.lit(45.0) # Impute 45.0°C baseline for machinery
)

vibration_clean = F.round(F.col("vibration_vps").cast("double"), 2)
health_clean = F.round(F.col("health").cast("double"), 2)
load_clean = F.round(F.col("current_load").cast("double"), 1)
power_clean = F.round(F.col("power_consumption_kw").cast("double"), 2)
failure_prob_clean = F.round(F.col("failure_probability").cast("double"), 4)
runtime_clean = F.round(F.col("runtime_hours").cast("double"), 1)

contact_clean = F.coalesce(F.trim(F.col("operator_contact")), F.lit("tech.support@smartfarm.ph"))
phone_clean = F.coalesce(F.trim(F.col("operator_phone")), F.lit("+639178452190"))

df_telemetry_cleaned = (
    spark.table("bronze.equipment_telemetry")
    .withColumn("facility_id_upper", facility_id_clean)
    .withColumn("zone_id_clean", zone_id_clean)
    .withColumn("clean_equipment_id", equipment_id_clean)
    .withColumn("clean_manufacturer", manufacturer_clean)
    .withColumn("clean_model", model_clean)
    .withColumn("clean_status", op_status_clean)
    .withColumn("clean_timestamp", timestamp_clean)
    .drop_duplicates(["event_id"])
)

df_enriched = df_telemetry_cleaned.join(
    df_facilities,
    F.col("facility_id_upper") == F.col("fac_id_join"),
    "left"
)

df_eq = (
    df_enriched
    .withColumn("facility_name", F.coalesce(F.col("facility_name"), F.col("facility_id_upper")))
    .withColumn("operating_temp_c", temp_clean)
    .withColumn("vibration_vps", vibration_clean)
    .withColumn("equipment_health_status", health_clean)
    .withColumn("current_load_pct", load_clean)
    .withColumn("power_kw", power_clean)
    .withColumn("fail_prob", failure_prob_clean)
    .withColumn("runtime_hrs", runtime_clean)
    .withColumn("operator_contact_clean", contact_clean)
    .withColumn("operator_phone_clean", phone_clean)
    .select(
        F.col("event_id"),
        F.col("facility_id_upper").alias("facility_id"),
        F.col("facility_name"),
        F.col("region"),
        F.col("zone_id_clean").alias("zone_id"),
        F.col("clean_equipment_id").alias("equipment_id"),
        F.trim(F.col("equipment_type")).alias("equipment_type"),
        F.col("clean_manufacturer").alias("manufacturer"),
        F.col("clean_model").alias("model_number"),
        F.col("clean_status").alias("operating_status"),
        F.col("operating_temp_c"),
        F.col("vibration_vps"),
        F.col("current_load_pct").alias("current_load_percent"),
        F.col("power_kw").alias("power_consumption_kw"),
        F.col("equipment_health_status"),
        F.col("fail_prob").alias("failure_probability"),
        F.col("runtime_hrs").alias("runtime_hours"),
        F.col("operator_contact_clean").alias("operator_contact"),
        F.col("operator_phone_clean").alias("operator_phone"),
        F.col("clean_timestamp").alias("timestamp")
    )
)

df_eq.write.format("delta")\
            .mode("overwrite")\
            .option("overwriteSchema", "true")\
            .saveAsTable("silver.equipment_risk_cleaned")

print(f"✍ Created silver.equipment_risk_cleaned ({df_eq.count()} rows).")

df_eq.show(10, truncate=False)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Create silver.crop_biological_cleaned

facility_id_clean = F.when(
    F.col("facility_id").isNull() | F.upper(F.trim(F.col("facility_id"))).isin("", "N/A", "UNKNOWN", "NULL", "NONE"),
    F.lit("UNKNOWN_FACILITY")
).otherwise(F.upper(F.trim(F.col("facility_id"))))

zone_id_clean = F.when(
    F.col("zone_id").isNull() | F.upper(F.trim(F.col("zone_id"))).isin("", "N/A", "UNKNOWN", "NULL", "NONE"),
    F.lit("ZONE-UNKNOWN")
).otherwise(F.upper(F.trim(F.col("zone_id"))))

raw_ts_str = F.regexp_replace(F.trim(F.col("timestamp").cast("string")), "[\"']", "")
timestamp_clean = F.coalesce(
    F.to_timestamp(raw_ts_str),
    F.to_timestamp(raw_ts_str, "yyyy-MM-dd HH:mm:ss"),
    F.to_timestamp(raw_ts_str, "yyyy-MM-dd'T'HH:mm:ss'Z'"),
    F.to_timestamp(F.from_unixtime(raw_ts_str.cast("bigint"))),
    F.current_timestamp()
)

growth_clean = F.round(F.col("growth_rate").cast("double"), 3)
biomass_clean = F.round(F.col("biomass_grams").cast("double"), 1)
stress_clean = F.round(F.col("environmental_stress_index").cast("double") * F.lit(100.0), 1)

contact_clean = F.coalesce(F.trim(F.col("operator_contact")), F.lit("agronomy.lead@smartfarm.ph"))
phone_clean = F.coalesce(F.trim(F.col("operator_phone")), F.lit("+639178452190"))

df_telemetry_cleaned = (
    spark.table("bronze.crop_telemetry")
    .withColumn("facility_id_upper", facility_id_clean)
    .withColumn("zone_id_clean", zone_id_clean)
    .withColumn("clean_timestamp", timestamp_clean)
    .drop_duplicates(["event_id"])
)

df_enriched = df_telemetry_cleaned.join(
    df_facilities,
    F.col("facility_id_upper") == F.col("fac_id_join"),
    "left"
)

df_crop = (
    df_enriched
    .withColumn("facility_name", F.coalesce(F.col("facility_name"), F.col("facility_id_upper")))
    .withColumn("growth_rate_g_day", growth_clean)
    .withColumn("biomass_g", biomass_clean)
    .withColumn("biological_stress_pct", stress_clean)
    .select(
        F.col("event_id"),
        F.col("facility_id_upper").alias("facility_id"),
        F.col("facility_name"),
        F.col("region"),
        F.col("zone_id_clean").alias("zone_id"),
        F.trim(F.col("crop_batch_id")).alias("crop_batch_id"),
        F.trim(F.col("crop_type")).alias("crop_type"),
        F.upper(F.trim(F.col("lifecycle_stage"))).alias("lifecycle_stage"),
        F.round(F.col("age_days").cast("double"), 1).alias("age_days"),
        F.round(F.col("health_score").cast("double"), 1).alias("crop_health_score"),
        F.col("growth_rate_g_day"),
        F.col("biomass_g"),
        F.col("biological_stress_pct"),
        F.round(F.col("water_consumption_liters").cast("double"), 2).alias("water_consumption_liters"),
        F.round(F.col("nutrient_consumption_grams").cast("double"), 2).alias("nutrient_consumption_grams"),
        F.round(F.col("ambient_temperature_celsius").cast("double"), 2).alias("ambient_temperature_celsius"),
        F.round(F.col("ambient_humidity_percent").cast("double"), 1).alias("ambient_humidity_percent"),
        contact_clean.alias("operator_contact"),
        phone_clean.alias("operator_phone"),
        F.col("clean_timestamp").alias("timestamp")
    )
)

df_crop.write.format('delta')\
            .mode("overwrite")\
            .option("overwriteSchema", "true")\
            .saveAsTable("silver.crop_biological_cleaned")

print(f"✍ Created silver.crop_biological_cleaned ({df_crop.count()} rows).")
df_crop.show(10, truncate=False)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Create silver.irrigation_flow_cleaned

facility_id_clean = F.when(
    F.col("facility_id").isNull() | F.upper(F.trim(F.col("facility_id"))).isin("", "N/A", "UNKNOWN", "NULL", "NONE"),
    F.lit("UNKNOWN_FACILITY")
).otherwise(F.upper(F.trim(F.col("facility_id"))))

zone_id_clean = F.when(
    F.col("zone_id").isNull() | F.upper(F.trim(F.col("zone_id"))).isin("", "N/A", "UNKNOWN", "NULL", "NONE"),
    F.lit("ZONE-UNKNOWN")
).otherwise(F.upper(F.trim(F.col("zone_id"))))

raw_ts_str = F.regexp_replace(F.trim(F.col("timestamp").cast("string")), "[\"']", "")
timestamp_clean = F.coalesce(
    F.to_timestamp(raw_ts_str),
    F.to_timestamp(raw_ts_str, "yyyy-MM-dd HH:mm:ss"),
    F.to_timestamp(raw_ts_str, "yyyy-MM-dd'T'HH:mm:ss'Z'"),
    F.to_timestamp(F.from_unixtime(raw_ts_str.cast("bigint"))),
    F.current_timestamp()
)

contact_clean = F.coalesce(F.trim(F.col("operator_contact")), F.lit("hydro.tech@smartfarm.ph"))
phone_clean = F.coalesce(F.trim(F.col("operator_phone")), F.lit("+639178452190"))

df_telemetry_cleaned = (
    spark.table("bronze.irrigation_telemetry")
    .withColumn("facility_id_upper", facility_id_clean)
    .withColumn("zone_id_clean", zone_id_clean)
    .withColumn("clean_timestamp", timestamp_clean)
    .drop_duplicates(["event_id"])
)

df_enriched = df_telemetry_cleaned.join(
    df_facilities,
    F.col("facility_id_upper") == F.col("fac_id_join"),
    "left"
)

df_irr = (
    df_enriched
    .withColumn("facility_name", F.coalesce(F.col("facility_name"), F.col("facility_id_upper")))
    .select(
        F.col("event_id"),
        F.col("facility_id_upper").alias("facility_id"),
        F.col("facility_name"),
        F.col("region"),
        F.col("zone_id_clean").alias("zone_id"),
        F.col("irrigation_active").cast("boolean").alias("irrigation_active"),
        F.round(F.col("flow_rate_liters_per_minute").cast("double"), 2).alias("flow_lpm"),
        F.round(F.col("pressure_kpa").cast("double"), 1).alias("pressure_kpa"),
        F.col("irrigation_duration_seconds").cast("int").alias("irrigation_duration_seconds"),
        F.round(F.col("water_delivered_liters").cast("double"), 2).alias("water_delivered_liters"),
        F.round(F.col("nutrient_solution_delivered_liters").cast("double"), 2).alias("nutrient_solution_delivered_liters"),
        contact_clean.alias("operator_contact"),
        phone_clean.alias("operator_phone"),
        F.col("clean_timestamp").alias("timestamp")
    )
)

df_irr.write.format("delta")\
            .mode("overwrite")\
            .option("overwriteSchema", "true")\
            .saveAsTable("silver.irrigation_flow_cleaned")

print(f"✍ Created silver.irrigation_flow_cleaned ({df_irr.count()} rows).")

df_irr.show(10, truncate=False)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Create silver.lighting_dli_cleaned

facility_id_clean = F.when(
    F.col("facility_id").isNull() | F.upper(F.trim(F.col("facility_id"))).isin("", "N/A", "UNKNOWN", "NULL", "NONE"),
    F.lit("UNKNOWN_FACILITY")
).otherwise(F.upper(F.trim(F.col("facility_id"))))

zone_id_clean = F.when(
    F.col("zone_id").isNull() | F.upper(F.trim(F.col("zone_id"))).isin("", "N/A", "UNKNOWN", "NULL", "NONE"),
    F.lit("ZONE-UNKNOWN")
).otherwise(F.upper(F.trim(F.col("zone_id"))))

raw_ts_str = F.regexp_replace(F.trim(F.col("timestamp").cast("string")), "[\"']", "")
timestamp_clean = F.coalesce(
    F.to_timestamp(raw_ts_str),
    F.to_timestamp(raw_ts_str, "yyyy-MM-dd HH:mm:ss"),
    F.to_timestamp(raw_ts_str, "yyyy-MM-dd'T'HH:mm:ss'Z'"),
    F.to_timestamp(F.from_unixtime(raw_ts_str.cast("bigint"))),
    F.current_timestamp()
)

contact_clean = F.coalesce(F.trim(F.col("operator_contact")), F.lit("elec.tech@smartfarm.ph"))
phone_clean = F.coalesce(F.trim(F.col("operator_phone")), F.lit("+639178452190"))

df_telemetry_cleaned = (
    spark.table("bronze.lighting_telemetry")
    .withColumn("facility_id_upper", facility_id_clean)
    .withColumn("zone_id_clean", zone_id_clean)
    .withColumn("clean_timestamp", timestamp_clean)
    .drop_duplicates(["event_id"])
)

df_enriched = df_telemetry_cleaned.join(
    df_facilities,
    F.col("facility_id_upper") == F.col("fac_id_join"),
    "left"
)

df_light = (
    df_enriched
    .withColumn("facility_name", F.coalesce(F.col("facility_name"), F.col("facility_id_upper")))
    .select(
        F.col("event_id"),
        F.col("facility_id_upper").alias("facility_id"),
        F.col("facility_name"),
        F.col("region"),
        F.col("zone_id_clean").alias("zone_id"),
        F.col("lighting_enabled").cast("boolean").alias("lighting_enabled"),
        F.round(F.col("lighting_intensity_percent").cast("double"), 1).alias("lighting_intensity_percent"),
        F.round(F.col("photoperiod_hours").cast("double"), 1).alias("photoperiod_hours"),
        F.round(F.col("daily_light_integral").cast("double"), 2).alias("dli_mol_m2_day"),
        contact_clean.alias("operator_contact"),
        phone_clean.alias("operator_phone"),
        F.col("clean_timestamp").alias("timestamp")
    )
)

df_light.write.format("delta")\
            .mode("overwrite")\
            .option("overwriteSchema", "true")\
            .saveAsTable("silver.lighting_dli_cleaned")

print(f"✍ Created silver.lighting_dli_cleaned ({df_light.count()} rows).")

df_light.show(10, truncate=False)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Create silver.maintenance_sla_cleaned

facility_id_clean = F.when(
    F.col("facility_id").isNull() | F.upper(F.trim(F.col("facility_id"))).isin("", "N/A", "UNKNOWN", "NULL", "NONE"),
    F.lit("UNKNOWN_FACILITY")
).otherwise(F.upper(F.trim(F.col("facility_id"))))

zone_id_clean = F.when(
    F.col("zone_id").isNull() | F.upper(F.trim(F.col("zone_id"))).isin("", "N/A", "UNKNOWN", "NULL", "NONE"),
    F.lit("ZONE-UNKNOWN")
).otherwise(F.upper(F.trim(F.col("zone_id"))))

# Clean equipment_id (handling orphan keys like EQ-99999_ORPHAN)
raw_eq_id = F.upper(F.trim(F.col("equipment_id")))
equipment_id_clean = F.when(
    raw_eq_id.isNull() | raw_eq_id.isin("", "N/A", "UNKNOWN", "NULL", "NONE") | raw_eq_id.contains("ORPHAN"),
    F.lit("UNREGISTERED_ASSET")
).otherwise(raw_eq_id)

raw_ts_str = F.regexp_replace(F.trim(F.col("timestamp").cast("string")), "[\"']", "")
timestamp_clean = F.coalesce(
    F.to_timestamp(raw_ts_str),
    F.to_timestamp(raw_ts_str, "yyyy-MM-dd HH:mm:ss"),
    F.to_timestamp(raw_ts_str, "yyyy-MM-dd'T'HH:mm:ss'Z'"),
    F.to_timestamp(F.from_unixtime(raw_ts_str.cast("bigint"))),
    F.current_timestamp()
)

lag_calc = F.col("estimated_duration_minutes").cast("long") - F.col("remaining_duration_minutes").cast("long")

maint_status_clean = F.upper(F.trim(F.col("maintenance_status")))
is_active_calc = F.when(maint_status_clean == "COMPLETED", F.lit(False)).otherwise(F.lit(True))

contact_clean = F.coalesce(F.trim(F.col("operator_contact")), F.lit("maint.lead@smartfarm.ph"))
phone_clean = F.coalesce(F.trim(F.col("operator_phone")), F.lit("+639178452190"))

df_telemetry_cleaned = (
    spark.table("bronze.maintenance_activity")
    .withColumn("facility_id_upper", facility_id_clean)
    .withColumn("zone_id_clean", zone_id_clean)
    .withColumn("clean_equipment_id", equipment_id_clean)
    .withColumn("clean_timestamp", timestamp_clean)
    .drop_duplicates(["event_id"])
)

df_enriched = df_telemetry_cleaned.join(
    df_facilities,
    F.col("facility_id_upper") == F.col("fac_id_join"),
    "left"
)

df_maint = (
    df_enriched
    .withColumn('facility_name', F.coalesce(F.col("facility_name"), F.col('facility_id_upper')))
    .withColumn("resolution_lag_min", lag_calc)
    .withColumn("clean_maint_status", maint_status_clean)
    .withColumn("is_active_flag", is_active_calc)
    .select(
        F.col("event_id"),
        F.col("facility_id_upper").alias("facility_id"),
        F.col("facility_name"),
        F.col("region"),
        F.col("zone_id_clean").alias("zone_id"),
        F.col("clean_equipment_id").alias("equipment_id"),
        F.trim(F.col("work_order_id")).alias("work_order_id"),
        F.trim(F.col("maintenance_type")).alias("maintenance_type"),
        F.upper(F.trim(F.col("priority"))).alias("priority"),
        F.trim(F.col("assigned_technician")).alias("assigned_technician"),
        F.upper(F.trim(F.col("maintenance_status"))).alias("maintenance_status"),
        F.col("estimated_duration_minutes").cast("int").alias("estimated_duration_minutes"),
        F.col("remaining_duration_minutes").cast("int").alias("remaining_duration_minutes"),
        F.round(F.col("completion_percent").cast("double"), 1).alias("completion_percent"),
        F.col("is_active_flag").cast("boolean").alias("is_active"),
        F.trim(F.col("technician_notes")).alias("technician_notes"),
        F.round(F.col("health_restored").cast("double"), 1).alias("health_restored"),
        F.col("resolution_lag_min"),
        contact_clean.alias("operator_contact"),
        phone_clean.alias("operator_phone"),
        F.col("clean_timestamp").alias("timestamp")
    )
)

df_maint.write.format("delta")\
            .mode("overwrite")\
            .option("overwriteSchema", "true")\
            .saveAsTable("silver.maintenance_sla_cleaned")

print(f"✍ Created silver.maintenance_sla_cleaned ({df_maint.count()} rows).")

df_maint.show(10, truncate=False)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Create silver.facility_master_enriched (SCD Type 2 Multi-Version Preserving)

df_fac_raw = spark.table("bronze.facility_operations")

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
    # Retain distinct state changes per facility based on tracked attributes
    .drop_duplicates(["facility_id_clean", "facility_name_clean", "max_zone_capacity_clean", "contact_clean"])
)

df_fac_master = df_fac_cleaned.select(
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

df_fac_master.write.format("delta")\
                    .mode("overwrite")\
                    .option("overwriteSchema", "true")\
                    .saveAsTable("silver.facility_master_enriched")

print(f"✍ Created silver.facility_master_enriched ({df_fac_master.count()} rows)")

df_fac_master.show(5, truncate=False)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# CREATE silver.crop_master_enriched (LATEST BATCH STATE TRACKER)

from pyspark.sql.window import Window

df_crop_raw = spark.table("bronze.crop_lifecycle")

stage_clean = F.upper(F.trim(F.col("lifecycle_stage")))
is_active_calc = F.when(stage_clean.isin("HARVESTED", "COMPLETED", "TERMINATED"), F.lit(False)).otherwise(F.lit(True))

contact_clean = F.coalesce(F.trim(F.col("operator_contact")), F.lit("agronomy.lead@smartfarm.ph"))
phone_clean = F.coalesce(F.trim(F.col("operator_phone")), F.lit("+639178452190"))

# Native PySpark mapping for distinct crop biological profiles
opt_temp_calc = (
    F.when(F.lower(F.col("crop_type")).contains("butterhead"), F.lit(22.0))
     .when(F.lower(F.col("crop_type")).contains("batavia"), F.lit(21.5))
     .when(F.lower(F.col("crop_type")).contains("kale"), F.lit(20.0))
     .when(F.lower(F.col("crop_type")).contains("spinach"), F.lit(19.0))
     .when(F.lower(F.col("crop_type")).contains("arugula"), F.lit(20.0))
     .when(F.lower(F.col("crop_type")).contains("basil"), F.lit(24.0))
     .when(F.lower(F.col("crop_type")).contains("cilantro"), F.lit(20.0))
     .when(F.lower(F.col("crop_type")).contains("parsley"), F.lit(20.0))
     .when(F.lower(F.col("crop_type")).contains("microgreens"), F.lit(22.0))
     .when(F.lower(F.col("crop_type")).contains("strawberry"), F.lit(19.0))
     .otherwise(F.lit(22.0))
)

opt_humid_calc = (
    F.when(F.lower(F.col("crop_type")).contains("strawberry"), F.lit(70.0))
     .when(F.lower(F.col("crop_type")).contains("kale"), F.lit(60.0))
     .when(F.lower(F.col("crop_type")).contains("arugula"), F.lit(60.0))
     .when(F.lower(F.col("crop_type")).contains("cilantro"), F.lit(60.0))
     .when(F.lower(F.col("crop_type")).contains("microgreens"), F.lit(60.0))
     .otherwise(F.lit(65.0))
)

# Window to extract the LATEST state per crop batch
window_latest = Window.partitionBy(F.trim(F.col("crop_batch_id"))).orderBy(F.col("timestamp").desc())
df_crop_master = (
    df_crop_raw
    .withColumn("crop_batch_clean", F.trim(F.col("crop_batch_id")))
    .withColumn("crop_type_clean", F.trim(F.col("crop_type")))
    .withColumn("stage_clean", stage_clean)
    .withColumn("is_active_flag", is_active_calc)
    .withColumn("rank", F.row_number().over(window_latest))
    .filter(F.col("rank") == 1)  # Keep LATEST state only
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
)

df_crop_master.write.format("delta") \
                    .mode("overwrite") \
                    .option("overwriteSchema", "true") \
                    .saveAsTable("silver.crop_master_enriched")

print(f"✍ Created silver.crop_master_enriched ({df_crop_master.count()} rows)")

df_crop_master.show(10, truncate=False)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# CREATE silver.equipment_master_enriched (SCD Type 2 Multi-Version Preserving)

df_eq_raw = spark.table("bronze.equipment_telemetry")
contact_clean = F.coalesce(F.trim(F.col("operator_contact")), F.lit("tech.support@smartfarm.ph"))
phone_clean = F.coalesce(F.trim(F.col("operator_phone")), F.lit("+639178452190"))

# Extract all distinct equipment versions based on tracked attributes and their earliest occurrence
df_eq_master = (
    df_eq_raw
    .withColumn("eq_id_clean", F.trim(F.col("equipment_id")))
    .withColumn("fac_id_clean", F.upper(F.trim(F.col("facility_id"))))
    .withColumn("zone_id_clean", F.trim(F.col("zone_id")))
    .withColumn("eq_type_clean", F.upper(F.trim(F.col("equipment_type"))))
    .withColumn("mfr_clean", F.coalesce(F.trim(F.col("manufacturer")), F.lit("HydroPump Corp")))
    .withColumn("model_clean", F.coalesce(F.trim(F.col("model_number")), F.lit("HP-3000X")))
    .withColumn("effective_date_clean", F.to_date(F.col("timestamp")))
    # 🧹 DATA QUALITY FILTER: Remove corrupt & orphan test keys
    .filter(~F.col("eq_id_clean").contains("ORPHAN"))
    .filter(F.col("eq_id_clean").rlike("^EQ-[0-9]{5}$"))
    .drop_duplicates(["eq_id_clean", "mfr_clean", "model_clean"])
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
)

df_eq_master.write.format("delta") \
                  .mode("overwrite") \
                  .option("overwriteSchema", "true") \
                  .saveAsTable("silver.equipment_master_enriched")

print(f"✍ Created silver.equipment_master_enriched ({df_eq_master.count()} rows)")

df_eq_master.show(10, truncate=False)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# CREATE silver.dead_letter_classified (DATAOPS GOVERNANCE EXCEPTION MATRIX)

import time
from pyspark.sql import functions as F

cell_start_time = time.time()
table_name = "silver.dead_letter_classified"

# Read Raw Bronze Table
df_dl_raw = spark.table("bronze.dead_letter_telemetry")
source_row_count = df_dl_raw.count()
raw_cols = df_dl_raw.columns

# Safe Column Resolvers (Schema Agnostic)
target_stream_col = (
    F.col("target_stream") 
    if "target_stream" in raw_cols 
    else F.coalesce(F.col("event_type"), F.lit("ENVIRONMENTAL_TELEMETRY"))
)

exception_reason_col = (
    F.col("exception_reason") 
    if "exception_reason" in raw_cols 
    else F.lit("MISSING_PRIMARY_KEY: null facility_id")
)

raw_payload_col = (
    F.col("raw_payload") 
    if "raw_payload" in raw_cols 
    else F.concat(F.lit('{"event_id":"'), F.col("event_id"), F.lit('"}'))
)

ingestion_ts_col = (
    F.col("ingestion_timestamp") 
    if "ingestion_timestamp" in raw_cols 
    else F.coalesce(F.col("IngestionTime"), F.current_timestamp())
)

# Safe facility_id null check
fac_id_check = F.col("facility_id").isNull() if "facility_id" in raw_cols else F.lit(False)

# Classification Expressions Across All 6 Exception Categories
exception_category_calc = (
    F.when(exception_reason_col.contains("MISSING_PRIMARY_KEY") | fac_id_check, F.lit("CRITICAL_MISSING_PRIMARY_KEY"))
     .when(exception_reason_col.contains("SCHEMA"), F.lit("DEPRECATED_SCHEMA_EVENT"))
     .when(exception_reason_col.contains("JSON") | exception_reason_col.contains("SERDES"), F.lit("SERDES_PARSE_FAILURE"))
     .when(exception_reason_col.contains("CLOCK") | exception_reason_col.contains("SYNC"), F.lit("TIMESTAMP_OUT_OF_SYNC"))
     .when(exception_reason_col.contains("MAC") | exception_reason_col.contains("UNREGISTERED"), F.lit("UNREGISTERED_HARDWARE_DEVICE"))
     .otherwise(F.lit("OUT_OF_BOUNDS_ANOMALY"))
)

is_auto_remediable_calc = (
    F.when(exception_category_calc == F.lit("DEPRECATED_SCHEMA_EVENT"), F.lit(True))
     .otherwise(F.lit(False))
)

# Transformation Pipeline
df_dl_classified = (
    df_dl_raw
    .withColumn("event_id_clean", F.trim(F.col("event_id")))
    .withColumn("target_stream_clean", F.upper(F.trim(target_stream_col)))
    .withColumn("exception_reason_clean", F.upper(F.trim(exception_reason_col)))
    .withColumn("exception_category", exception_category_calc)
    .withColumn("is_auto_remediable", is_auto_remediable_calc)
    .withColumn("raw_payload_clean", raw_payload_col)
    .withColumn("ingestion_ts_clean", ingestion_ts_col)
    .drop_duplicates(["event_id_clean"])
    .select(
        F.col("event_id_clean").alias("event_id"),
        F.col("target_stream_clean").alias("target_stream"),
        F.col("exception_category"),
        F.col("exception_reason_clean").alias("exception_reason"),
        F.col("is_auto_remediable"),
        F.col("raw_payload_clean").alias("raw_payload"),
        F.col("ingestion_ts_clean").alias("ingestion_timestamp")
    )
)

# Save to Silver Delta Table
df_dl_classified.write.format("delta") \
                      .mode("overwrite") \
                      .option("overwriteSchema", "true") \
                      .saveAsTable(table_name)

print(f"✍ Created silver.dead_letter_classified ({df_dl_classified.count()} rows).")


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

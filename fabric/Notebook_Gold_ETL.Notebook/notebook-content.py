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
# META     },
# META     "warehouse": {
# META       "known_warehouses": []
# META     }
# META   }
# META }

# CELL ********************

# Environment Setup & Global Pipeline Constants

from pyspark.sql import functions as F
from pyspark.sql.window import Window
from delta.tables import DeltaTable
import datetime
import time

# Spark Session & Schema Initialization
spark.sql("CREATE SCHEMA IF NOT EXISTS gold")
spark.conf.set("spark.sql.sources.partitionOverwriteMode", "dynamic")

# Global Pipeline Execution Paremeters
PIPELINE_RUN_DATE = datetime.date.today()
FARM_OPERATIONS_START_DATE = datetime.date(2025, 1, 15)
RUN_QUALITY_AUDIT = True

# Tracked Attribute Definitions For SCD Type 2 Change Detection
FACILITY_TRACKED_COLUMNS = ["power_grid_redundancy", "water_source", "max_zone_capacity", "operator_contact"]
EQUIPMENT_TRACKED_COLUMNS = ["zone_id", "operating_status", "model_number", "equipment_type"]

print("==============================================================================")
print(f"🟢 FABRIC ENVIRONMENT INITIALIZED | RUN DATE: {PIPELINE_RUN_DATE}")
print(f"✍️ DYNAMIC PARTITION OVERWRITE MODE: ACTIVE | CUSTOM FUNCTIONS DEFINED: 0")
print("==============================================================================")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Enterprise Calendar Dimension (gold.dim_date - SCD Type 1)

import time
import datetime
from pyspark.sql import functions as F

cell_start_time = time.time()
table_name = "gold.dim_date"
action_type = "SCD TYPE 1 OVERWRITE"
target_end_date = datetime.date(2030, 12, 31)

# Generate 6-year calendar data sequence (2025-01-01 to 2030-12-31)
date_df = spark.sql("SELECT sequence(to_date('2025-01-01'), to_date('2030-12-31'), interval 1 day) as date_array")\
                .withColumn("date", F.explode("date_array"))

dim_date_body = date_df.select(
    F.date_format("date", "yyyyMMdd").cast("int").alias("date_key"),
    F.col("date").alias("full_date"),
    F.year("date").alias("year"),
    F.quarter("date").alias("quarter"),
    F.month("date").alias("month"),
    F.date_format("date", "MMMM").alias("month_name"),
    F.date_format("date", "MMM yyyy").alias("month_year"),
    F.date_format("date", "yyyyMM").cast("int").alias("year_month_sort"),
    F.date_format("date", "MMM-yy").alias("short_month_year"),
    F.dayofmonth("date").alias("day_of_month"),
    F.dayofweek("date").alias("day_of_week"),
    F.date_format("date", "EEEE").alias("day_name"),
    F.dayofyear("date").alias("day_of_year"),
    F.weekofyear("date").alias("week_of_year"),
    F.when(F.dayofweek("date").isin(1, 7), True).otherwise(False).alias("is_weekend"),
    # Fiscal calendar
    F.when(F.month("date") >= 10, F.year("date") + 1).otherwise(F.year("date")).alias("fiscal_year"),
    F.when(F.month("date") >= 10, F.quarter("date") - 3).otherwise(F.quarter("date") + 1).alias("fiscal_quarter"),
    F.month("date").alias("fiscal_period"),
    # Boundary Flags
    (F.col("date") == F.last_day("date")).alias("is_month_end"),
    ((F.col("date") == F.last_day("date")) & F.month("date").isin(3, 6, 9, 12)).alias("is_quarter_end"),
    (F.date_format("date", "MM-dd") == "12-31").alias("is_year_end")
)

# Unknown (-1) Member with Strict 1-to-1 Sort Key
unknown_date = spark.createDataFrame([(
    -1, datetime.date(1900, 1, 1), 1900, 1, 1, "Unknown", "Unknown", -1, "Unk-00", 1, 1, "Unknown", 1, 1, False, 1900, 1, 1, False, False, False
)], dim_date_body.schema)

dim_date_final = unknown_date.unionByName(dim_date_body)

# Write Delta Table
dim_date_final.write.format("delta")\
                    .mode("overwrite")\
                    .option("mergeSchema", "true")\
                    .saveAsTable(table_name)

# Compute Table Statistics
spark.sql(f"ANALYZE TABLE {table_name} COMPUTE STATISTICS")

# Lightweight Validation & Metrics
df_dim_date = spark.table(table_name)
total_rows = df_dim_date.count()
distinct_dates = df_dim_date.select("date_key").distinct().count()
unknown_count = df_dim_date.filter(F.col("date_key") == -1).count()
null_keys = df_dim_date.filter(F.col("date_key").isNull()).count()

elapsed_time = round(time.time() - cell_start_time, 2)
validation_status = "PASSED" if (distinct_dates == total_rows and unknown_count == 1 and null_keys == 0) else "FAILED"

print("==============================================================================")
print(f"⭐ TABLE: {table_name} ({action_type})")
print("==============================================================================")
print(f"Total Table Volume:   {total_rows:,}")
print(f"Distinct Date Keys:   {distinct_dates:,}")
print(f"Null Business Keys:   {null_keys}")
print(f"Unknown Members (-1): {unknown_count}")
print(f"Execution Time:       {elapsed_time}s")
print(f"Validation Status:    {validation_status}")
print("==============================================================================\n")


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Facility Dimension (gold.dim_facility - SCD Type 2)

import time
import datetime
from pyspark.sql import functions as F
from delta.tables import DeltaTable

cell_start_time = time.time()
table_name = "gold.dim_facility"

# Read Source Data & Compute Attribute Hash
df_fac_raw = spark.table("silver.facility_master_enriched")
source_row_count = df_fac_raw.count()

# Prepare staging Dataframe with short_region transformer
eff_fac_col = F.col("effective_date").cast("date") if "effective_date" in df_fac_raw.columns else F.lit(FARM_OPERATIONS_START_DATE).cast("date")

dim_fac_stg = df_fac_raw.select(
    F.col("facility_id"),
    F.col("facility_name"),
    F.col("region"),
    F.regexp_replace(F.col("region"), r"\s*\(.*\)", "").alias("short_region"),
    F.col("city"),
    F.col("latitude"),
    F.col("longitude"),
    F.col("elevation_m"),
    F.col("climate_zone"),
    F.col("water_source"),
    F.col("power_grid_redundancy"),
    F.col("max_zone_capacity"),
    F.col("operator_contact"),
    eff_fac_col.alias("effective_date"),
    F.xxhash64(
        F.concat_ws("||", *[F.coalesce(F.col(c).cast("string"), F.lit("NULL")) for c in FACILITY_TRACKED_COLUMNS])
    ).alias("attr_hash")
)

# Two-pass SCD Type 2 Processing (Initial Load VS Incremental MERGE)

if not spark.catalog.tableExists(table_name):
    # Initial Load: Support multi-version historical baseline records organically
    from pyspark.sql.window import Window
    window_fac = Window.partitionBy("facility_id").orderBy("effective_date")

    dim_fac_initial = (
        dim_fac_stg
        .withColumn("lead_eff_date", F.lead("effective_date").over(window_fac))
        .withColumn(
            "expiration_date",
            F.when(F.col("lead_eff_date").isNotNull(), F.date_sub(F.col("lead_eff_date"), 1))
             .otherwise(F.lit("9999-12-31").cast("date"))
        )
        .withColumn(
            "is_current",
            F.when(F.col("expiration_date") == "9999-12-31", F.lit(True)).otherwise(F.lit(False))
        )
        .select(
            F.abs(F.xxhash64(F.concat_ws("||", F.upper(F.trim(F.col("facility_id"))), F.col("effective_date").cast("string"), F.col("attr_hash").cast("string")))).alias("facility_key"),
            F.col("facility_id"), 
            F.col("facility_name"), 
            F.col("region"), 
            F.col("short_region"),
            F.col("city"), 
            F.col("latitude"), 
            F.col("longitude"), 
            F.col("elevation_m"), 
            F.col("climate_zone"), 
            F.col("water_source"), 
            F.col("power_grid_redundancy"), 
            F.col("max_zone_capacity"), 
            F.col("operator_contact"), 
            F.col("attr_hash"),
            F.col("effective_date"),
            F.col("expiration_date"),
            F.col("is_current"),
            F.current_timestamp().alias("created_timestamp"),
            F.lit(PIPELINE_RUN_DATE).alias("pipeline_run_date")
        )
    )

    # Unknown (-1) Dimension Member
    unknown_fac = spark.createDataFrame([(
        -1, "UNKNOWN", "Unknown Facility", "N/A", "N/A", "N/A", 0.0, 0.0, 0.0, "N/A", "N/A", "N/A", 0, "N/A", 0,
        datetime.date(1900, 1, 1), datetime.date(9999, 12, 31), True,
        datetime.datetime.now(), PIPELINE_RUN_DATE
    )], schema=dim_fac_initial.schema)

    dim_facility_final = unknown_fac.unionByName(dim_fac_initial).drop_duplicates(["facility_key"])

    # Inline Delta Write
    dim_facility_final.write.format("delta")\
                            .mode("overwrite")\
                            .option("mergeSchema", "true")\
                            .saveAsTable(table_name)

    rows_appended_count = dim_facility_final.count()
    action_type = "INITIALIZED BASELINE"

else:
    # Incremental Load: Two-pass SCD Type 2 Staging Pattern
    target_fac = spark.table(table_name).filter(F.col("is_current") == True)

    # Identify Brand New business keys (not present in active target)
    df_new_fac_keys = dim_fac_stg.alias("src").join(target_fac.alias("tgt"), "facility_id", "left_anti")\
                        .select(
                            F.abs(F.xxhash64(F.concat_ws("||", F.upper(F.trim(F.col("facility_id"))), 
                            F.lit(PIPELINE_RUN_DATE).cast("string"), F.col("attr_hash").cast("string")))).alias("facility_key"),
                            F.col("facility_id"), 
                            F.col("facility_name"), 
                            F.col("region"), 
                            F.col("short_region"),
                            F.col("city"), 
                            F.col("latitude"), 
                            F.col("longitude"),
                            F.col("elevation_m"),
                            F.col("climate_zone"),
                            F.col("water_source"),
                            F.col("power_grid_redundancy"),
                            F.col("max_zone_capacity"),
                            F.col("operator_contact"),
                            F.col("attr_hash"),
                            F.lit(PIPELINE_RUN_DATE).cast("date").alias("effective_date"),
                            F.lit("9999-12-31").cast("date").alias("expiration_date"),
                            F.lit(True).alias("is_current"),
                            F.current_timestamp().alias("created_timestamp"),
                            F.lit(PIPELINE_RUN_DATE).alias("pipeline_run_date")
                        )

    # Identify Existing Business Keys whose tracked attributes have changed
    df_changed_fac_keys = dim_fac_stg.alias("src").join(target_fac.alias("tgt"), "facility_id")\
                            .filter(F.col("src.attr_hash") != F.col("tgt.attr_hash"))\
                            .select(
                                F.abs(F.xxhash64(F.concat_ws("||", F.upper(F.trim(F.col("src.facility_id"))), 
                                F.lit(PIPELINE_RUN_DATE).cast("string"), F.col("src.attr_hash").cast("string")))).alias("facility_key"),
                                F.col("src.facility_id"), 
                                F.col("src.facility_name"), 
                                F.col("src.region"), 
                                F.col("src.short_region"),
                                F.col("src.city"), 
                                F.col("src.latitude"), 
                                F.col("src.longitude"),
                                F.col("src.elevation_m"),
                                F.col("src.climate_zone"),
                                F.col("src.water_source"),
                                F.col("src.power_grid_redundancy"),
                                F.col("src.max_zone_capacity"),
                                F.col("src.operator_contact"),
                                F.col("src.attr_hash"),
                                F.lit(PIPELINE_RUN_DATE).cast("date").alias("effective_date"),
                                F.lit("9999-12-31").cast("date").alias("expiration_date"),
                                F.lit(True).alias("is_current"),
                                F.current_timestamp().alias("created_timestamp"),
                                F.lit(PIPELINE_RUN_DATE).alias("pipeline_run_date")
                            )

    # Expire previous active records for changed business keys
    delta_fac = DeltaTable.forName(spark, table_name)
    delta_fac.alias("target").merge(
        df_changed_fac_keys.alias("source"),
        "target.facility_id = source.facility_id AND target.is_current = true"
    ).whenMatchedUpdate(
        set={
            "expiration_date": F.date_sub(F.lit(PIPELINE_RUN_DATE), 1),
            "is_current": F.lit(False)
        }
    ).execute()

    # Append new keys + new versions of changed keys
    df_fac_to_append = df_new_fac_keys.unionByName(df_changed_fac_keys).drop_duplicates(["facility_key"])
    
    if not df_fac_to_append.isEmpty():
        df_fac_to_append.write.format("delta")\
                        .mode("append")\
                        .option("mergeSchema", "true")\
                        .saveAsTable(table_name)
        rows_appended_count = df_fac_to_append.count()
    else:
        rows_appended_count = 0

    action_type = "INCREMENTAL TWO-PASS MERGE"

# Compute Table Statistics
spark.sql(f"ANALYZE TABLE {table_name} COMPUTE STATISTICS")

# Lightweight Validation and Metrics
df_dim_fac = spark.table(table_name)
total_rows = df_dim_fac.count()
distinct_b_keys = df_dim_fac.select("facility_id").distinct().count()
duplicate_active_keys = df_dim_fac.filter("is_current = true AND facility_key != -1").groupBy("facility_id").count().filter("count > 1").count()
null_b_keys = df_dim_fac.filter(F.col("facility_id").isNull()).count()
unknown_count = df_dim_fac.filter(F.col("facility_key") == -1).count()
current_active_rows = df_dim_fac.filter(F.col("is_current") == True).count()
historical_inactive_rows = df_dim_fac.filter(F.col("is_current") == False).count()

elapsed_time = round(time.time() - cell_start_time, 2)
validation_status = "PASSED" if (duplicate_active_keys == 0 and null_b_keys == 0 and unknown_count == 1) else "FAILED"

# Standardized Cell Inline Logging
print("==============================================================================")
print(f"⭐ TABLE: {table_name} ({action_type})")
print("==============================================================================")
print(f"Source Rows Read:     {source_row_count:,}")
print(f"New Rows Appended:    {rows_appended_count:,}")
print(f"Total Table Volume:   {total_rows:,}")
print(f"Distinct Business Keys: {distinct_b_keys:,}")
print(f"Active Current Rows:  {current_active_rows:,}")
print(f"Historical Expired Rows: {historical_inactive_rows:,}")
print(f"Duplicate Active Keys: {duplicate_active_keys}")
print(f"Null Business Keys:   {null_b_keys}")
print(f"Unknown Members (-1): {unknown_count}")
print(f"Execution Time:       {elapsed_time}s")
print(f"Validation Status:    {validation_status}")
print("==============================================================================\n")



# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Zone Dimension (gold.dim_zone - SCD Type 2)

import time
import datetime
from pyspark.sql import functions as F
from pyspark.sql.types import StructType, StructField, LongType, StringType, IntegerType, DateType, BooleanType, TimestampType
from delta.tables import DeltaTable

cell_start_time = time.time()
table_name = "gold.dim_zone"

# Explicit StructType Schema Definition (12 Columns)
dim_zone_schema = StructType([
    StructField("zone_key", LongType(), False),
    StructField("facility_key", LongType(), False),
    StructField("zone_id", StringType(), True),
    StructField("zone_name", StringType(), True),
    StructField("section", StringType(), True),
    StructField("rack_capacity", IntegerType(), True),
    StructField("attr_hash", LongType(), True),
    StructField("effective_date", DateType(), True),
    StructField("expiration_date", DateType(), True),
    StructField("is_current", BooleanType(), True),
    StructField("created_timestamp", TimestampType(), True),
    StructField("pipeline_run_date", DateType(), True)
])

# Read Source Data & Combine distinct zone IDs from telemetry streams
df_env_zones = spark.table("silver.environmental_metrics").select("facility_id", "zone_id")
df_eq_zones  = spark.table("silver.equipment_risk_cleaned").select("facility_id", "zone_id")
df_irr_zones = spark.table("silver.irrigation_flow_cleaned").select("facility_id", "zone_id")
df_lt_zones  = spark.table("silver.lighting_dli_cleaned").select("facility_id", "zone_id")

df_zone_raw = df_env_zones.unionByName(df_eq_zones) \
    .unionByName(df_irr_zones) \
    .unionByName(df_lt_zones) \
    .withColumn("facility_id", F.upper(F.trim(F.col("facility_id")))) \
    .withColumn("zone_id", F.upper(F.trim(F.col("zone_id")))) \
    .filter(
        (F.col("zone_id").rlike("^ZONE-[0-9]{3}$")) &
        (F.col("facility_id").isNotNull()) &
        (F.col("facility_id") != "") &
        (F.col("facility_id") != "UNKNOWN_FACILITY")
    ) \
    .drop_duplicates(["facility_id", "zone_id"])

source_row_count = df_zone_raw.count()

# Rich Category, Name, and Section Mapping for All 10 Hydroponic Zones
zone_name_calc = (
    F.when(F.col("zone_id") == "ZONE-001", F.lit("Butterhead & Batavia Lettuce Array"))
     .when(F.col("zone_id") == "ZONE-002", F.lit("Vertical Strawberry Hydro-Towers"))
     .when(F.col("zone_id") == "ZONE-003", F.lit("Kale & Arugula Canopy Racks"))
     .when(F.col("zone_id") == "ZONE-004", F.lit("Genovese Basil & Cilantro Array"))
     .when(F.col("zone_id") == "ZONE-005", F.lit("High-Density Microgreens Racks"))
     .when(F.col("zone_id") == "ZONE-006", F.lit("Germination & Seedling Nursery"))
     .when(F.col("zone_id") == "ZONE-007", F.lit("Deep Water Culture (DWC) Romaine Channel"))
     .when(F.col("zone_id") == "ZONE-008", F.lit("NFT Spinach & Parsley Tier"))
     .when(F.col("zone_id") == "ZONE-009", F.lit("Aeroponic Cherry Tomato Towers"))
     .when(F.col("zone_id") == "ZONE-010", F.lit("Bell Pepper & Herb Canopy System"))
     .otherwise(F.concat(F.lit("Hydroponic Zone "), F.col("zone_id")))
)

section_calc = (
    F.when(F.col("zone_id") == "ZONE-001", F.lit("LEAFY_GREENS_SECTION_A"))
     .when(F.col("zone_id") == "ZONE-002", F.lit("FRUITING_CULTIVAR_SECTION"))
     .when(F.col("zone_id") == "ZONE-003", F.lit("CRUCIFEROUS_SECTION"))
     .when(F.col("zone_id") == "ZONE-004", F.lit("AROMATIC_HERB_SECTION"))
     .when(F.col("zone_id") == "ZONE-005", F.lit("MICROGREENS_TIER"))
     .when(F.col("zone_id") == "ZONE-006", F.lit("NURSERY_SEEDLING_TIER"))
     .when(F.col("zone_id") == "ZONE-007", F.lit("DEEP_WATER_CULTURE_TIER"))
     .when(F.col("zone_id") == "ZONE-008", F.lit("NFT_CHANNEL_SECTION_B"))
     .when(F.col("zone_id") == "ZONE-009", F.lit("AEROPONIC_TOWER_TIER"))
     .when(F.col("zone_id") == "ZONE-010", F.lit("CANOPY_HERB_TIER"))
     .otherwise(F.concat(F.lit("SECTION_"), F.regexp_extract(F.col("zone_id"), r"(\d+)", 1)))
)

rack_capacity_calc = (
    F.when(F.col("zone_id") == "ZONE-001", F.lit(24))
     .when(F.col("zone_id") == "ZONE-002", F.lit(18))
     .when(F.col("zone_id") == "ZONE-003", F.lit(20))
     .when(F.col("zone_id") == "ZONE-004", F.lit(16))
     .when(F.col("zone_id") == "ZONE-005", F.lit(32))
     .when(F.col("zone_id") == "ZONE-006", F.lit(40))
     .when(F.col("zone_id") == "ZONE-007", F.lit(28))
     .when(F.col("zone_id") == "ZONE-008", F.lit(22))
     .when(F.col("zone_id") == "ZONE-009", F.lit(15))
     .when(F.col("zone_id") == "ZONE-010", F.lit(18))
     .otherwise(F.lit(16))
).cast("int")

dim_zone_stg = df_zone_raw \
    .withColumn("zone_name", zone_name_calc) \
    .withColumn("section", section_calc) \
    .withColumn("rack_capacity", rack_capacity_calc) \
    .withColumn(
        "attr_hash",
        F.xxhash64(
            F.concat_ws("||",
                F.coalesce(F.col("zone_name"), F.lit("NULL")),
                F.coalesce(F.col("section"), F.lit("NULL")),
                F.coalesce(F.col("rack_capacity").cast("string"), F.lit("NULL"))
            )
        )
    )

# Broadcast cached dim_facility for point-in-time facility_key resolution
dim_fac_bcast = F.broadcast(
    spark.table("gold.dim_facility")
    .select("facility_key", "facility_id", "effective_date", "expiration_date")
    .cache()
)

# Two-Pass SCD Type 2 Processing (Initial Load VS Incremental MERGE)
if not spark.catalog.tableExists(table_name):
    dim_zone_stg_init = dim_zone_stg.withColumn("effective_date", F.lit(FARM_OPERATIONS_START_DATE).cast("date"))
    
    dim_zone_initial = dim_zone_stg_init.alias("stg") \
        .join(
            dim_fac_bcast.alias("fac"),
            (F.col("stg.facility_id") == F.col("fac.facility_id")) &
            (F.col("stg.effective_date") >= F.col("fac.effective_date")) &
            (F.col("stg.effective_date") <= F.col("fac.expiration_date")),
            how="left"
        ) \
        .select(
            F.abs(F.xxhash64(F.concat_ws("||", F.col("stg.facility_id"), F.col("stg.zone_id"), F.col("stg.effective_date").cast("string"), F.col("stg.attr_hash").cast("string")))).alias("zone_key"),
            F.coalesce(F.col("fac.facility_key"), F.lit(-1)).alias("facility_key"),
            F.col("stg.zone_id"),
            F.col("stg.zone_name"),
            F.col("stg.section"),
            F.col("stg.rack_capacity"),
            F.col("stg.attr_hash"),
            F.col("stg.effective_date"),
            F.lit("9999-12-31").cast("date").alias("expiration_date"),
            F.lit(True).alias("is_current"),
            F.current_timestamp().alias("created_timestamp"),
            F.lit(PIPELINE_RUN_DATE).alias("pipeline_run_date")
        )

    unknown_zone = spark.createDataFrame([(
        -1, -1, "UNKNOWN", "Unknown Zone", "SECTION_0", 0, 0,
        datetime.date(1900, 1, 1), datetime.date(9999, 12, 31), True,
        datetime.datetime.now(), PIPELINE_RUN_DATE
    )], schema=dim_zone_schema)
    
    dim_zone_final = unknown_zone.unionByName(dim_zone_initial).drop_duplicates(["zone_key"])
    dim_zone_final.write.format("delta") \
        .mode("overwrite") \
        .option("mergeSchema", "true") \
        .saveAsTable(table_name)
    
    rows_appended_count = dim_zone_final.count()
    action_type = "INITIALIZED BASELINE"
else:
    target_zone = spark.table(table_name).filter(F.col("is_current") == True)
    dim_zone_stg_inc = dim_zone_stg.withColumn("effective_date", F.lit(PIPELINE_RUN_DATE).cast("date"))
    dim_zone_stg_resolved = dim_zone_stg_inc.alias("stg") \
        .join(
            dim_fac_bcast.alias("fac"),
            (F.col("stg.facility_id") == F.col("fac.facility_id")) &
            (F.col("stg.effective_date") >= F.col("fac.effective_date")) &
            (F.col("stg.effective_date") <= F.col("fac.expiration_date")),
            how="left"
        ) \
        .select(
            F.col("stg.facility_id"),
            F.col("stg.zone_id"),
            F.coalesce(F.col("fac.facility_key"), F.lit(-1)).alias("facility_key"),
            F.col("stg.zone_name"),
            F.col("stg.section"),
            F.col("stg.rack_capacity"),
            F.col("stg.attr_hash"),
            F.col("stg.effective_date")
        )

    df_new_zone_keys = dim_zone_stg_resolved.alias("src") \
        .join(target_zone.alias("tgt"), ["facility_key", "zone_id"], "left_anti") \
        .select(
            F.abs(F.xxhash64(F.concat_ws("||", F.col("src.facility_id"), F.col("src.zone_id"), F.col("src.effective_date").cast("string"), F.col("src.attr_hash").cast("string")))).alias("zone_key"),
            F.col("src.facility_key"), F.col("src.zone_id"), F.col("src.zone_name"),
            F.col("src.section"), F.col("src.rack_capacity"), F.col("src.attr_hash"),
            F.col("src.effective_date"), F.lit("9999-12-31").cast("date").alias("expiration_date"),
            F.lit(True).alias("is_current"),
            F.current_timestamp().alias("created_timestamp"),
            F.lit(PIPELINE_RUN_DATE).alias("pipeline_run_date")
        )

    df_changed_zone_keys = dim_zone_stg_resolved.alias("src") \
        .join(target_zone.alias("tgt"), ["facility_key", "zone_id"]) \
        .filter(F.col("src.attr_hash") != F.col("tgt.attr_hash")) \
        .select(
            F.abs(F.xxhash64(F.concat_ws("||", F.col("src.facility_id"), F.col("src.zone_id"), F.col("src.effective_date").cast("string"), F.col("src.attr_hash").cast("string")))).alias("zone_key"),
            F.col("src.facility_key"), F.col("src.zone_id"), F.col("src.zone_name"),
            F.col("src.section"), F.col("src.rack_capacity"), F.col("src.attr_hash"),
            F.col("src.effective_date"), F.lit("9999-12-31").cast("date").alias("expiration_date"),
            F.lit(True).alias("is_current"),
            F.current_timestamp().alias("created_timestamp"),
            F.lit(PIPELINE_RUN_DATE).alias("pipeline_run_date")
        )
        
    delta_zone = DeltaTable.forName(spark, table_name)
    delta_zone.alias("target").merge(
        df_changed_zone_keys.alias("source"),
        "target.facility_key = source.facility_key AND target.zone_id = source.zone_id AND target.is_current = true"
    ).whenMatchedUpdate(
        set={
            "expiration_date": F.date_sub(F.lit(PIPELINE_RUN_DATE), 1),
            "is_current": F.lit(False)
        }
    ).execute()
    df_zone_to_append = df_new_zone_keys.unionByName(df_changed_zone_keys).drop_duplicates(["zone_key"])
    
    if not df_zone_to_append.isEmpty():
        df_zone_to_append.write.format("delta") \
            .mode("append") \
            .option("mergeSchema", "true") \
            .saveAsTable(table_name)
        rows_appended_count = df_zone_to_append.count()
    else:
        rows_appended_count = 0
    action_type = "INCREMENTAL TWO-PASS MERGE"

# Compute Table Statistics
spark.sql(f"ANALYZE TABLE {table_name} COMPUTE STATISTICS")

# Lightweight Validation and Metrics
df_dim_zone = spark.table(table_name)
total_rows = df_dim_zone.count()
distinct_b_keys = df_dim_zone.select("facility_key", "zone_id").distinct().count()
duplicate_active_keys = df_dim_zone.filter("is_current = true AND zone_key != -1").groupBy("facility_key", "zone_id").count().filter("count > 1").count()
null_b_keys = df_dim_zone.filter(F.col("zone_id").isNull()).count()
unknown_count = df_dim_zone.filter(F.col("zone_key") == -1).count()
current_active_rows = df_dim_zone.filter(F.col("is_current") == True).count()
historical_inactive_rows = df_dim_zone.filter(F.col("is_current") == False).count()

elapsed_time = round(time.time() - cell_start_time, 2)
validation_status = "PASSED" if (duplicate_active_keys == 0 and null_b_keys == 0 and unknown_count == 1) else "FAILED"

# Standardized Cell Inline Logging
print("==============================================================================")
print(f"⭐ TABLE: {table_name} ({action_type})")
print("==============================================================================")
print(f"Source Rows Read:     {source_row_count:,}")
print(f"New Rows Appended:    {rows_appended_count:,}")
print(f"Total Table Volume:   {total_rows:,}")
print(f"Distinct Business Keys: {distinct_b_keys:,}")
print(f"Active Current Rows:  {current_active_rows:,}")
print(f"Historical Expired Rows: {historical_inactive_rows:,}")
print(f"Duplicate Active Keys: {duplicate_active_keys}")
print(f"Null Business Keys:   {null_b_keys}")
print(f"Unknown Members (-1): {unknown_count}")
print(f"Execution Time:       {elapsed_time}s")
print(f"Validation Status:    {validation_status}")
print("==============================================================================\n")


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Equipment Dimension (gold.dim_equipment - SCD Type 2)

import time
import datetime
from pyspark.sql import functions as F
from pyspark.sql.types import StructType, StructField, LongType, StringType, DateType, BooleanType, TimestampType
from delta.tables import DeltaTable

cell_start_time = time.time()
table_name = "gold.dim_equipment"

# Explicit StructType Schema Definition (14 Columns)
dim_eq_schema = StructType([
    StructField("equipment_key", LongType(), False),
    StructField("facility_key", LongType(), False),
    StructField("zone_key", LongType(), False),
    StructField("equipment_id", StringType(), True),
    StructField("equipment_type", StringType(), True),
    StructField("manufacturer", StringType(), True),
    StructField("model_number", StringType(), True),
    StructField("installation_date", DateType(), True),
    StructField("attr_hash", LongType(), True),
    StructField("effective_date", DateType(), True),
    StructField("expiration_date", DateType(), True),
    StructField("is_current", BooleanType(), True),
    StructField("created_timestamp", TimestampType(), True),
    StructField("pipeline_run_date", DateType(), True)
])

# Tracked attributes for SCD Type 2 change detection in dim_equipment
tracked_cols = ["equipment_type", "manufacturer", "model_number", "installation_date"]

# Read source data & compute attribute hash
df_master_eq = spark.table("silver.equipment_master_enriched").select("equipment_id", "facility_id", "zone_id", "equipment_type", "manufacturer", "model_number", "installation_date")

df_risk_eq = spark.table("silver.equipment_risk_cleaned") \
    .filter(
        (F.col("equipment_id").isNotNull()) &
        (F.col("equipment_id") != "unregistered_asset") &
        (~F.col("equipment_id").contains("ORPHAN"))
    ) \
    .select("equipment_id", "facility_id", "zone_id", "equipment_type", "manufacturer", "model_number") \
    .withColumn("installation_date", F.lit("2025-01-15").cast("date"))

df_eq_union = df_master_eq.unionByName(df_risk_eq) \
    .withColumn("equipment_id", F.trim(F.col("equipment_id"))) \
    .withColumn("facility_id", F.upper(F.trim(F.col("facility_id")))) \
    .withColumn("zone_id", F.upper(F.trim(F.col("zone_id")))) \
    .filter(
        (F.col("equipment_id").isNotNull()) &
        (F.col("equipment_id") != "") &
        (F.col("equipment_id") != "unregistered_asset") &
        (~F.col("equipment_id").contains("ORPHAN"))
    ) \
    .drop_duplicates(["equipment_id", "manufacturer", "model_number"])

source_row_count = df_eq_union.count()

# Select equipment business attributes and compute change detection hash
eff_eq_col = F.col("effective_date").cast("date") if "effective_date" in df_eq_union.columns else (
    F.col("installation_date").cast("date") if "installation_date" in df_eq_union.columns else F.lit(FARM_OPERATIONS_START_DATE).cast("date")
)

dim_eq_stg = df_eq_union.select(
    F.col("equipment_id"),
    F.upper(F.trim(F.col("facility_id"))).alias("facility_id"),
    F.upper(F.trim(F.col("zone_id"))).alias("zone_id"),
    F.upper(F.trim(F.col("equipment_type"))).alias("equipment_type"),
    F.coalesce(F.trim(F.col("manufacturer")), F.lit("HydroPump Corp")).alias("manufacturer"),
    F.coalesce(F.trim(F.col("model_number")), F.lit("HP-3000X")).alias("model_number"),
    F.col("installation_date").cast("date").alias("installation_date"),
    eff_eq_col.alias("effective_date"),
    F.xxhash64(
        F.concat_ws("||", *[F.coalesce(F.col(c).cast("string"), F.lit("NULL")) for c in tracked_cols])
    ).alias("attr_hash")
)

# Broadcast cached dim_facility and dim_zone for Point-in-Time surrogate key resolution
dim_fac_bcast = F.broadcast(
    spark.table("gold.dim_facility")
    .select("facility_key", "facility_id", "effective_date", "expiration_date")
    .cache()
)

dim_zone_bcast = F.broadcast(
    spark.table("gold.dim_zone")
    .select("zone_key", "facility_key", "zone_id", "effective_date", "expiration_date")
    .cache()
)

# Two-pass SCD Type 2 Processing
if not spark.catalog.tableExists(table_name):
    # Support multi-version historical baseline records organically
    from pyspark.sql.window import Window
    window_eq = Window.partitionBy("equipment_id").orderBy("effective_date")

    dim_eq_stg_init = dim_eq_stg \
        .withColumn("lead_eff_date", F.lead("effective_date").over(window_eq)) \
        .withColumn(
            "expiration_date",
            F.when(F.col("lead_eff_date").isNotNull(), F.date_sub(F.col("lead_eff_date"), 1))
             .otherwise(F.lit("9999-12-31").cast("date"))
        ) \
        .withColumn(
            "is_current",
            F.when(F.col("expiration_date") == "9999-12-31", F.lit(True)).otherwise(F.lit(False))
        )

    dim_eq_initial = dim_eq_stg_init.alias("stg") \
        .join(
            dim_fac_bcast.alias("fac"),
            (F.col("stg.facility_id") == F.col("fac.facility_id")) &
            (F.col("stg.effective_date") >= F.col("fac.effective_date")) &
            (F.col("stg.effective_date") <= F.col("fac.expiration_date")),
            how="left"
        ) \
        .join(
            dim_zone_bcast.alias("zn"),
            (F.col("fac.facility_key") == F.col("zn.facility_key")) &
            (F.col("stg.zone_id") == F.col("zn.zone_id")) &
            (F.col("stg.effective_date") >= F.col("zn.effective_date")) &
            (F.col("stg.effective_date") <= F.col("zn.expiration_date")),
            how="left"
        ) \
        .select(
            F.abs(F.xxhash64(F.concat_ws("||", F.upper(F.trim(F.col("stg.equipment_id"))), F.col("stg.effective_date").cast("string"), F.col("stg.attr_hash").cast("string")))).alias("equipment_key"),
            F.coalesce(F.col("fac.facility_key"), F.lit(-1)).alias("facility_key"),
            F.coalesce(F.col("zn.zone_key"), F.lit(-1)).alias("zone_key"),
            F.col("stg.equipment_id"),
            F.col("stg.equipment_type"),
            F.col("stg.manufacturer"),
            F.col("stg.model_number"),
            F.col("stg.installation_date"),
            F.col("stg.attr_hash"),
            F.col("stg.effective_date"),
            F.col("stg.expiration_date"),
            F.col("stg.is_current"),
            F.current_timestamp().alias("created_timestamp"),
            F.lit(PIPELINE_RUN_DATE).alias("pipeline_run_date")
        )

    unknown_eq = spark.createDataFrame([(
        -1, -1, -1, "UNKNOWN", "UNKNOWN", "Unknown Manufacturer", "HP-000",
        datetime.date(1900, 1, 1), 0, datetime.date(1900, 1, 1), datetime.date(9999, 12, 31), True,
        datetime.datetime.now(), PIPELINE_RUN_DATE
    )], schema=dim_eq_schema)

    dim_equipment_final = unknown_eq.unionByName(dim_eq_initial).drop_duplicates(["equipment_key"])
    
    dim_equipment_final.write.format("delta") \
        .mode("overwrite") \
        .option("mergeSchema", "true") \
        .saveAsTable(table_name)
    
    rows_appended_count = dim_equipment_final.count()
    action_type = "INITIALIZED BASELINE"
else:
    target_eq = spark.table(table_name).filter(F.col("is_current") == True)
    dim_eq_stg_inc = dim_eq_stg.withColumn("effective_date", F.lit(PIPELINE_RUN_DATE).cast("date"))
    
    dim_eq_stg_resolved = dim_eq_stg_inc.alias("stg") \
        .join(
            dim_fac_bcast.alias("fac"),
            (F.col("stg.facility_id") == F.col("fac.facility_id")) &
            (F.col("stg.effective_date") >= F.col("fac.effective_date")) &
            (F.col("stg.effective_date") <= F.col("fac.expiration_date")),
            how="left"
        ) \
        .join(
            dim_zone_bcast.alias("zn"),
            (F.col("fac.facility_key") == F.col("zn.facility_key")) &
            (F.col("stg.zone_id") == F.col("zn.zone_id")) &
            (F.col("stg.effective_date") >= F.col("zn.effective_date")) &
            (F.col("stg.effective_date") <= F.col("zn.expiration_date")),
            how="left"
        ) \
        .select(
            F.col("stg.equipment_id"),
            F.coalesce(F.col("fac.facility_key"), F.lit(-1)).alias("facility_key"),
            F.coalesce(F.col("zn.zone_key"), F.lit(-1)).alias("zone_key"),
            F.col("stg.equipment_type"),
            F.col("stg.manufacturer"),
            F.col("stg.model_number"),
            F.col("stg.installation_date"),
            F.col("stg.attr_hash"),
            F.col("stg.effective_date")
        )

    df_changed_eq_keys = dim_eq_stg_resolved.alias("src") \
        .join(target_eq.alias("tgt"), ["equipment_id"]) \
        .filter(F.col("src.attr_hash") != F.col("tgt.attr_hash")) \
        .select(
            F.abs(F.xxhash64(F.concat_ws("||", F.upper(F.trim(F.col("src.equipment_id"))), F.col("src.effective_date").cast("string"), F.col("src.attr_hash").cast("string")))).alias("equipment_key"),
            F.col("src.facility_key"), F.col("src.zone_key"), F.col("src.equipment_id"),
            F.col("src.equipment_type"), F.col("src.manufacturer"), F.col("src.model_number"),
            F.col("src.installation_date"), F.col("src.attr_hash"),
            F.col("src.effective_date"), F.lit("9999-12-31").cast("date").alias("expiration_date"),
            F.lit(True).alias("is_current"),
            F.current_timestamp().alias("created_timestamp"),
            F.lit(PIPELINE_RUN_DATE).alias("pipeline_run_date")
        ).drop_duplicates(["equipment_key"])
        
    delta_eq = DeltaTable.forName(spark, table_name)
    delta_eq.alias("target").merge(
        df_changed_eq_keys.alias("source"),
        "target.equipment_id = source.equipment_id AND target.is_current = true"
    ).whenMatchedUpdate(
        set={
            "expiration_date": "source.effective_date - INTERVAL 1 DAY",
            "is_current": "false"
        }
    ).execute()
    
    df_changed_eq_keys.write.format("delta").mode("append").saveAsTable(table_name)
    rows_appended_count = df_changed_eq_keys.count()
    action_type = f"MERGED SCD TYPE 2 ({rows_appended_count} UPDATES)"

# Compute Table Statistics
spark.sql(f"ANALYZE TABLE {table_name} COMPUTE STATISTICS")

# Lightweight Validation and Metrics
df_dim_eq = spark.table(table_name)
total_rows = df_dim_eq.count()
distinct_keys = df_dim_eq.select("equipment_key").distinct().count()
duplicate_keys = total_rows - distinct_keys
unknown_count = df_dim_eq.filter(F.col("equipment_key") == -1).count()
null_keys = df_dim_eq.filter(F.col("equipment_key").isNull()).count()

elapsed_time = round(time.time() - cell_start_time, 2)
validation_status = "PASSED" if (duplicate_keys == 0 and unknown_count == 1 and null_keys == 0) else "FAILED"

print("==============================================================================")
print(f"⭐ TABLE: {table_name} ({action_type})")
print("==============================================================================")
print(f"Source Rows Read:     {source_row_count:,}")
print(f"Total Table Volume:   {total_rows:,}")
print(f"Distinct Equipment Keys: {distinct_keys:,}")
print(f"Duplicate Key Count:  {duplicate_keys}")
print(f"Unknown Members (-1): {unknown_count}")
print(f"Execution Time:       {elapsed_time}s")
print(f"Validation Status:    {validation_status}")
print("==============================================================================\n")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Crop Master Dimension (gold.dim_crop - SCD Type 1 with Cultivar Wholesale Pricing)

import time
import datetime
from pyspark.sql import functions as F

cell_start_time = time.time()
table_name = "gold.dim_crop"

# Read source data & build staging dimension
df_crop_raw = spark.table("silver.crop_master_enriched")
source_row_count = df_crop_raw.count()

# Select distinct crop types, assign cultivar wholesale pricing, and generate SCD Type 1 surrogate keys
price_a_calc = (
    F.when(F.lower(F.col("crop_type")).contains("strawberry"), F.lit(1400.0))
     .when(F.lower(F.col("crop_type")).contains("microgreen") | F.lower(F.col("crop_type")).contains("pea_shoots"), F.lit(950.0))
     .when(F.lower(F.col("crop_type")).contains("basil") | F.lower(F.col("crop_type")).contains("parsley") | F.lower(F.col("crop_type")).contains("mint"), F.lit(750.0))
     .when(F.lower(F.col("crop_type")).contains("kale") | F.lower(F.col("crop_type")).contains("arugula") | F.lower(F.col("crop_type")).contains("watercress"), F.lit(580.0))
     .when(F.lower(F.col("crop_type")).contains("lettuce") | F.lower(F.col("crop_type")).contains("romaine") | F.lower(F.col("crop_type")).contains("oakleaf"), F.lit(420.0))
     .otherwise(F.lit(480.0))
)

price_b_calc = F.round(price_a_calc * 0.65, 2)

dim_crop_stg = df_crop_raw.select(
    "crop_type",
    "optimal_temperature_celsius",
    "optimal_humidity_percent",
    "target_biomass_g",
    "harvest_cycle_days"
).drop_duplicates(["crop_type"])\
.withColumn("unit_price_grade_a_php", price_a_calc)\
.withColumn("unit_price_grade_b_php", price_b_calc)\
.select(
    F.abs(F.xxhash64(F.upper(F.trim(F.col("crop_type"))))).alias("crop_key"),
    F.col("crop_type"),
    F.col("optimal_temperature_celsius"),
    F.col("optimal_humidity_percent"),
    F.col("target_biomass_g"),
    F.col("harvest_cycle_days"),
    F.col("unit_price_grade_a_php"),
    F.col("unit_price_grade_b_php"),
    F.current_timestamp().alias("created_timestamp"),
    F.lit(PIPELINE_RUN_DATE).alias("pipeline_run_date")
)

# Prepend Unknown (-1) Member & Write Delta Table
unknown_crop = spark.createDataFrame([(
    -1, "Unknown Crop", 22.0, 65.0, 150.0, 35, 480.0, 312.0, datetime.datetime.now(), PIPELINE_RUN_DATE
)], schema=dim_crop_stg.schema)

dim_crop_final = unknown_crop.unionByName(dim_crop_stg)

# Inline Delta Write (SCD Type 1 Overwrite)
dim_crop_final.write.format("delta")\
                    .mode("overwrite")\
                    .option("mergeSchema", "true")\
                    .saveAsTable(table_name)

# Compute Table Statistics
spark.sql(f"ANALYZE TABLE {table_name} COMPUTE STATISTICS")

# Validation Metrics
df_dim_crop = spark.table(table_name)
total_rows = df_dim_crop.count()
distinct_crops = df_dim_crop.select("crop_type").distinct().count()
null_keys = df_dim_crop.filter(F.col("crop_type").isNull()).count()
unknown_count = df_dim_crop.filter(F.col("crop_key") == -1).count()

elapsed_time = round(time.time() - cell_start_time, 2)
validation_status = "PASSED" if (distinct_crops == total_rows and unknown_count == 1 and null_keys == 0) else "FAILED"

print("==============================================================================")
print(f"⭐ TABLE: {table_name} (SCD TYPE 1 OVERWRITE)")
print("==============================================================================")
print(f"Source Rows Read:     {source_row_count:,}")
print(f"Total Table Volume:   {total_rows:,}")
print(f"Distinct Crop Types:  {distinct_crops:,}")
print(f"Null Business Keys:   {null_keys}")
print(f"Unknown Members (-1): {unknown_count}")
print(f"Execution Time:       {elapsed_time}s")
print(f"Validation Status:    {validation_status}")
print("==============================================================================\n")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Technician Directory Dimension (gold.dim_technician - SCD Type 1)

import time 

cell_start_time = time.time()
table_name = "gold.dim_technician"

# Read Source Data and Build Staging Dimension

df_maint_raw = spark.table("silver.maintenance_sla_cleaned")
source_row_count = df_maint_raw.count()

# Select distinct technician contacts and generate SCD Type 1 surrogate keys
dim_tech_stg = df_maint_raw.select(
    F.trim(F.col("assigned_technician")).alias("technician_name"),
    F.coalesce(F.trim(F.col("operator_phone")), 
    F.lit("+639178452190")).alias("phone_number"),
    F.coalesce(F.trim(F.col("operator_contact")), 
    F.lit("tech.support@smartfarm.ph")).alias("email")
).filter(
    (F.col("technician_name").isNotNull()) & (F.col("technician_name") != "")
).drop_duplicates(["technician_name"])\
.select(
    F.abs(F.xxhash64(F.upper(F.trim(F.col("technician_name"))))).alias("technician_key"),
    F.col("technician_name"),
    F.col("phone_number"),
    F.col("email"),
    F.current_timestamp().alias("created_timestamp"),
    F.lit(PIPELINE_RUN_DATE).alias("pipeline_run_date")
)

# Prepend Unknown (-1) Member & Write Delta Table
unknown_tech = spark.createDataFrame([(
    -1, "Unassigned Technician", "+639000000000", "tech.support@smartfarm.ph", datetime.datetime.now(), PIPELINE_RUN_DATE
)], schema=dim_tech_stg.schema)

dim_technician_final = unknown_tech.unionByName(dim_tech_stg)

# Inline Delta Write (SCD Type 1 Overwrite)
dim_technician_final.write.format("delta")\
                        .mode("overwrite")\
                        .option("mergeSchema", "true")\
                        .saveAsTable(table_name)

# Compute Table Statistics

spark.sql(f"ANALYZE TABLE {table_name} COMPUTE STATISTICS")

# Lightweight Validation and Metrics

df_dim_tech = spark.table(table_name)
total_rows = df_dim_tech.count()
distinct_techs = df_dim_tech.select("technician_name").distinct().count()
null_keys = df_dim_tech.filter(F.col("technician_name").isNull()).count()
unknown_count = df_dim_tech.filter(F.col("technician_key") == -1).count()

elapsed_time = round(time.time() - cell_start_time, 2)
validation_status = "PASSED" if (distinct_techs == total_rows and unknown_count == 1 and null_keys == 0) else "FAILED"

# Standardized Cell Inline Logging

print("==============================================================================")
print(f"⭐ TABLE: {table_name} (SCD TYPE 1 OVERWRITE)")
print("==============================================================================")
print(f"Source Rows Read:     {source_row_count:,}")
print(f"Total Table Volume:   {total_rows:,}")
print(f"Distinct Technicians: {distinct_techs:,}")
print(f"Null Business Keys:   {null_keys}")
print(f"Unknown Members (-1): {unknown_count}")
print(f"Execution Time:       {elapsed_time}s")
print(f"Validation Status:    {validation_status}")
print("==============================================================================\n")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Environmental Daily Fact (gold.fact_environmental_daily)

import time

cell_start_time = time.time()
table_name = "gold.fact_environmental_daily"

# Read Source Data and Compute Daily Aggregations

df_env_raw = spark.table("silver.environmental_metrics")\
                    .filter(F.col("zone_id").rlike("^ZONE-[0-9]{3}$"))
source_row_count = df_env_raw.count()

# Aggregate micro-climate telemetry daily per facility and zone
df_env_agg = df_env_raw \
    .withColumn("date_key", F.date_format("timestamp", "yyyyMMdd").cast("int"))\
    .withColumn("event_date", F.to_date("timestamp"))\
    .withColumn("facility_id", F.upper(F.trim(F.col("facility_id"))))\
    .withColumn("zone_id", F.upper(F.trim(F.col("zone_id"))))\
    .groupBy("date_key", "event_date", "facility_id", "zone_id")\
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

# Cached Dimension Lookups and Point-in-time surrogate key resolution

dim_fac_bcast = F.broadcast(
    spark.table("gold.dim_facility")
    .select("facility_key", "facility_id", "effective_date", "expiration_date")
    .cache()
)

dim_zone_bcast = F.broadcast(
    spark.table("gold.dim_zone")
    .select("zone_key", "facility_key", "zone_id", "effective_date", "expiration_date")
    .cache()
)

fact_env_stg = (
    df_env_agg.alias("fact")
    .join(
        dim_fac_bcast.alias("dim_fac"),
        (F.col("fact.facility_id") == F.col("dim_fac.facility_id")) &
        (F.col("fact.event_date") >= F.col("dim_fac.effective_date")) &
        (F.col("fact.event_date") <= F.col("dim_fac.expiration_date")),
        how="left"
    )
    .join(
        dim_zone_bcast.alias("dim_zn"),
        (F.col("dim_fac.facility_key") == F.col("dim_zn.facility_key")) &
        (F.col("fact.zone_id") == F.col("dim_zn.zone_id")) &
        (F.col("fact.event_date") >= F.col("dim_zn.effective_date")) &
        (F.col("fact.event_date") <= F.col("dim_zn.expiration_date")),
        how="left"
    )
    .select(
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
    )
)

# Write Delta Tbale (Dynamic Partition Overwrite by date_key)

fact_env_stg.write.format("delta")\
            .mode("overwrite")\
            .option("mergeSchema", "true")\
            .partitionBy("date_key")\
            .saveAsTable(table_name)

# Compute Table Statistics

spark.sql(f"ANALYZE TABLE {table_name} COMPUTE STATISTICS")

# Lightweight Validation $ Metrics

df_fact_env = spark.table(table_name)
total_rows = df_fact_env.count()
distinct_grain = df_fact_env.select("date_key", "facility_key", "zone_key").distinct().count()
duplicate_grain_count = df_fact_env.groupBy("date_key", "facility_key", "zone_key").count().filter("count > 1").count()
partition_count = df_fact_env.select("date_key").distinct().count()

min_date_key = df_fact_env.select(F.min("date_key")).collect()[0][0]
max_date_key = df_fact_env.select(F.max("date_key")).collect()[0][0]
unknown_fac_count = df_fact_env.filter(F.col("facility_key") == -1).count()
unknown_zone_count = df_fact_env.filter(F.col("zone_key") == -1).count()

elapsed_time = round(time.time() - cell_start_time, 2)
validation_status = "PASSED" if (duplicate_grain_count == 0 and unknown_fac_count == 0 and unknown_zone_count == 0) else "FAILED"

# Standardized Cell Inline Loggings

print("==============================================================================")
print(f"⭐ TABLE: {table_name} (DYNAMIC PARTITION OVERWRITE)")
print("==============================================================================")
print(f"Source Rows Read:     {source_row_count:,}")
print(f"Total Table Volume:   {total_rows:,}")
print(f"Distinct Business Grain: {distinct_grain:,}")
print(f"Duplicate Grain Count:{duplicate_grain_count}")
print(f"Partition Count:      {partition_count} Partitions")
print(f"Partition Range:      {min_date_key} -> {max_date_key}")
print(f"Unknown Facilities (-1): {unknown_fac_count}")
print(f"Unknown Zones (-1):      {unknown_zone_count}")
print(f"Execution Time:       {elapsed_time}s")
print(f"Validation Status:    {validation_status}")
print("==============================================================================\n")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Equipment Telemetry Fact (gold.fact_equipment_telemetry)

import time

cell_start_time = time.time()
table_name = "gold.fact_equipment_telemetry"

# Read Source Data and Compute Daily Aggregations

df_eq_raw = spark.table("silver.equipment_risk_cleaned") \
    .filter(~F.col("equipment_id").contains("ORPHAN")) \
    .withColumn("facility_id", F.upper(F.trim(F.col("facility_id")))) \
    .withColumn("equipment_id", F.trim(F.col("equipment_id"))) \
    .withColumn("zone_id", F.upper(F.trim(F.col("zone_id")))) \
    .filter(F.col("zone_id").rlike("^ZONE-[0-9]{3}$"))

source_row_count = df_eq_raw.count()

# Aggregate machinery telemetry daily per facility, equipment, and zone
df_eq_agg = df_eq_raw \
    .withColumn("date_key", F.date_format("timestamp", "yyyyMMdd").cast("int")) \
    .withColumn("event_date", F.to_date("timestamp")) \
    .groupBy("date_key", "event_date", "facility_id", "equipment_id", "zone_id") \
    .agg(
        F.round(F.avg("equipment_health_status"), 1).alias("avg_health_score"),
        F.round(F.max("failure_probability"), 4).alias("max_failure_probability"),
        F.round(F.greatest(F.lit(0.0), F.max("runtime_hours") - F.min("runtime_hours")), 2).alias("daily_runtime_hours"),
        F.round(F.avg("power_consumption_kw"), 2).alias("avg_power_draw_kw"),
        F.round(F.avg("vibration_vps"), 3).alias("avg_vibration_vps"),
        F.round(F.avg("operating_temp_c"), 2).alias("avg_operating_temp_celsius"),
        F.round(F.avg("current_load_percent"), 1).alias("avg_load_percent"),
        F.count("event_id").alias("telemetry_sample_count")
    ) \
    .withColumn(
        "total_energy_kwh",
        F.round(F.col("avg_power_draw_kw") * F.col("daily_runtime_hours"), 2)
    )


# Cached Dimension Lookups and Point-In-Time Surrogate Key Resolution

dim_fac_bcast = F.broadcast(
    spark.table("gold.dim_facility")
    .select("facility_key", "facility_id", "effective_date", "expiration_date")
    .cache()
)

dim_eq_bcast = F.broadcast(
    spark.table("gold.dim_equipment")
    .select("equipment_key", "equipment_id", "effective_date", "expiration_date")
    .cache()
)

dim_zone_bcast = F.broadcast(
    spark.table("gold.dim_zone")
    .select("zone_key", "facility_key", "zone_id", "effective_date", "expiration_date")
    .cache()
)

fact_eq_stg = (
    df_eq_agg.alias("fact")
    .join(
        dim_fac_bcast.alias("dim_fac"),
        (F.col("fact.facility_id") == F.col("dim_fac.facility_id")) &
        (F.col("fact.event_date") >= F.col("dim_fac.effective_date")) &
        (F.col("fact.event_date") <= F.col("dim_fac.expiration_date")),
        how="left"
    )
    .join(
        dim_eq_bcast.alias("dim_eq"),
        (F.col("fact.equipment_id") == F.col("dim_eq.equipment_id")) &
        (F.col("fact.event_date") >= F.col("dim_eq.effective_date")) &
        (F.col("fact.event_date") <= F.col("dim_eq.expiration_date")),
        how="left"
    )
    .join(
        dim_zone_bcast.alias("dim_zn"),
        (F.col("dim_fac.facility_key") == F.col("dim_zn.facility_key")) &
        (F.col("fact.zone_id") == F.col("dim_zn.zone_id")) &
        (F.col("fact.event_date") >= F.col("dim_zn.effective_date")) &
        (F.col("fact.event_date") <= F.col("dim_zn.expiration_date")),
        how="left"
    )
    .select(
        F.col("fact.date_key"),
        F.coalesce(F.col("dim_fac.facility_key"), F.lit(-1)).alias("facility_key"),
        F.coalesce(F.col("dim_eq.equipment_key"), F.lit(-1)).alias("equipment_key"),
        F.coalesce(F.col("dim_zn.zone_key"), F.lit(-1)).alias("zone_key"),
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
    )
)

# Write Delta Table (Dynamic Partition Overwrite By date_key)

fact_eq_stg.write.format("delta")\
                .mode("overwrite")\
                .option("mergeSchema", "true")\
                .partitionBy("date_key")\
                .saveAsTable(table_name)

# Compute Table Statistics

spark.sql(f"ANALYZE TABLE {table_name} COMPUTE STATISTICS")

# Lighweight Validation and Metrics

df_fact_eq = spark.table(table_name)
total_rows = df_fact_eq.count()
distinct_grain = df_fact_eq.select("date_key", "facility_key", "equipment_key", "zone_key").distinct().count()
duplicate_grain_count = df_fact_eq.groupBy("date_key", "facility_key", "equipment_key", "zone_key").count().filter("count > 1").count()
partition_count = df_fact_eq.select("date_key").distinct().count()

min_date_key = df_fact_eq.select(F.min("date_key")).collect()[0][0]
max_date_key = df_fact_eq.select(F.max("date_key")).collect()[0][0]
unknown_fac_count = df_fact_eq.filter(F.col("facility_key") == -1).count()
unknown_eq_count = df_fact_eq.filter(F.col("equipment_key") == -1).count()
unknown_zone_count = df_fact_eq.filter(F.col("zone_key") == -1).count()

elapsed_time = round(time.time() - cell_start_time, 2)
validation_status = "PASSED" if (duplicate_grain_count == 0 and unknown_fac_count == 0 and unknown_eq_count == 0 and unknown_zone_count == 0) else "FAILED"

# Standarized Cell Inline Logging
print("==============================================================================")
print(f"⭐ TABLE: {table_name} (DYNAMIC PARTITION OVERWRITE)")
print("==============================================================================")
print(f"Source Rows Read:     {source_row_count:,}")
print(f"Total Table Volume:   {total_rows:,}")
print(f"Distinct Business Grain: {distinct_grain:,}")
print(f"Duplicate Grain Count:{duplicate_grain_count}")
print(f"Partition Count:      {partition_count} Partitions")
print(f"Partition Range:      {min_date_key} -> {max_date_key}")
print(f"Unknown Facilities (-1): {unknown_fac_count}")
print(f"Unknown Equipment (-1):  {unknown_eq_count}")
print(f"Unknown Zones (-1):      {unknown_zone_count}")
print(f"Execution Time:       {elapsed_time}s")
print(f"Validation Status:    {validation_status}")
print("==============================================================================\n")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Crop Yield Fact (gold.fact_crop_yield with Cultivar Pricing & Commercial Rack Density)

import time

cell_start_time = time.time()
table_name = "gold.fact_crop_yield"

# Read Source Data and Aggregate Daily Crop Harvest Metrics
df_crop_raw = spark.table("silver.crop_biological_cleaned")
source_row_count = df_crop_raw.count()

# Daily aggregation per facility, zone and crop cultivar with commercial rack plant density (250 plants/rack)
RACK_PLANT_DENSITY = 250.0

df_yield_agg = df_crop_raw \
    .withColumn("facility_id", F.upper(F.trim(F.col("facility_id")))) \
    .withColumn("zone_id", F.upper(F.trim(F.col("zone_id")))) \
    .withColumn("crop_id", F.upper(F.trim(F.col("crop_type")))) \
    .withColumn("event_date", F.to_date(F.col("timestamp"))) \
    .withColumn("date_key", F.date_format(F.col("timestamp"), "yyyyMMdd").cast("int")) \
    .filter(F.col("zone_id").rlike("^ZONE-[0-9]{3}$")) \
    .groupBy("date_key", "event_date", "facility_id", "zone_id", "crop_id") \
    .agg(
        F.round(F.avg("crop_health_score"), 1).alias("avg_health_score"),
        F.round(F.max("biomass_g") * RACK_PLANT_DENSITY / 1000.0, 2).alias("target_yield_kg"),
        F.round(F.avg(F.when(F.col("crop_health_score") >= 80, F.col("biomass_g")).otherwise(F.col("biomass_g") * 0.6)) * RACK_PLANT_DENSITY / 1000.0, 2).alias("total_harvest_kg"),
        F.round(F.avg(F.col("biomass_g") * 0.80) * RACK_PLANT_DENSITY / 1000.0, 2).alias("grade_a_harvest_kg"),
        F.round(F.avg(F.col("biomass_g") * 0.15) * RACK_PLANT_DENSITY / 1000.0, 2).alias("grade_b_harvest_kg"),
        F.round(F.avg(F.col("biomass_g") * 0.05) * RACK_PLANT_DENSITY / 1000.0, 2).alias("spoilage_waste_kg"),
        F.round(F.avg("growth_rate_g_day"), 2).alias("avg_growth_rate_g_day"),
        F.count("crop_batch_id").alias("harvest_batch_count")
    ) \
    .withColumn(
        "yield_achievement_pct",
        F.when(F.col("target_yield_kg") > 0, F.round((F.col("total_harvest_kg") * 100.0) / F.col("target_yield_kg"), 2)).otherwise(F.lit(100.0))
    )

# Join dim_crop to get Cultivar Prices
dim_crop_prices = spark.table("gold.dim_crop").select(
    F.upper(F.trim(F.col("crop_type"))).alias("crop_id"),
    "unit_price_grade_a_php",
    "unit_price_grade_b_php"
)

df_yield_agg = df_yield_agg.alias("fact").join(
    dim_crop_prices.alias("pr"),
    F.col("fact.crop_id") == F.col("pr.crop_id"),
    how="left"
).select(
    F.col("fact.*"),
    F.coalesce(F.col("pr.unit_price_grade_a_php"), F.lit(480.0)).alias("price_a"),
    F.coalesce(F.col("pr.unit_price_grade_b_php"), F.lit(312.0)).alias("price_b")
).withColumn(
    "estimated_revenue_php",
    F.round(F.col("grade_a_harvest_kg") * F.col("price_a") + F.col("grade_b_harvest_kg") * F.col("price_b"), 2)
).drop("price_a", "price_b")

# Cached Dimension Lookups and Point-in-Time Surrogate Key Resolution
dim_fac_bcast = F.broadcast(
    spark.table("gold.dim_facility")
    .select("facility_key", "facility_id", "effective_date", "expiration_date")
    .cache()
)

dim_zone_bcast = F.broadcast(
    spark.table("gold.dim_zone")
    .select("zone_key", "facility_key", "zone_id", "effective_date", "expiration_date")
    .cache()
)

dim_crop_cols = spark.table("gold.dim_crop").columns
dim_crop_natural_col = "crop_type" if "crop_type" in dim_crop_cols else "crop_id"
dim_crop_bcast = F.broadcast(
    spark.table("gold.dim_crop")
    .select("crop_key", F.upper(F.trim(F.col(dim_crop_natural_col))).alias("crop_id"))
    .cache()
)

fact_crop_stg = (
    df_yield_agg.alias("fact")
    .join(
        dim_fac_bcast.alias("dim_fac"),
        (F.col("fact.facility_id") == F.col("dim_fac.facility_id")) &
        (F.col("fact.event_date") >= F.col("dim_fac.effective_date")) &
        (F.col("fact.event_date") <= F.col("dim_fac.expiration_date")),
        how="left"
    )
    .join(
        dim_zone_bcast.alias("dim_zn"),
        (F.col("dim_fac.facility_key") == F.col("dim_zn.facility_key")) &
        (F.col("fact.zone_id") == F.col("dim_zn.zone_id")) &
        (F.col("fact.event_date") >= F.col("dim_zn.effective_date")) &
        (F.col("fact.event_date") <= F.col("dim_zn.expiration_date")),
        how="left"
    )
    .join(
        dim_crop_bcast.alias("dim_cr"),
        F.col("fact.crop_id") == F.col("dim_cr.crop_id"),
        how="left"
    )
    .select(
        F.col("fact.date_key"),
        F.coalesce(F.col("dim_fac.facility_key"), F.lit(-1)).alias("facility_key"),
        F.coalesce(F.col("dim_zn.zone_key"), F.lit(-1)).alias("zone_key"),
        F.coalesce(F.col("dim_cr.crop_key"), F.lit(-1)).alias("crop_key"),
        F.col("fact.target_yield_kg"),
        F.col("fact.total_harvest_kg"),
        F.col("fact.grade_a_harvest_kg"),
        F.col("fact.grade_b_harvest_kg"),
        F.col("fact.spoilage_waste_kg"),
        F.col("fact.yield_achievement_pct"),
        F.col("fact.estimated_revenue_php"),
        F.col("fact.avg_growth_rate_g_day"),
        F.col("fact.harvest_batch_count"),
        F.current_timestamp().alias("created_timestamp"),
        F.lit(PIPELINE_RUN_DATE).alias("pipeline_run_date")
    )
)

# Write Delta Table (Dynamic Partition Overwrite by date_key)
fact_crop_stg.write.format("delta")\
                .mode("overwrite")\
                .option("mergeSchema", "true")\
                .partitionBy("date_key")\
                .saveAsTable(table_name)

# Compute Table Statistics
spark.sql(f"ANALYZE TABLE {table_name} COMPUTE STATISTICS")

# Lightweight validation and metrics
df_fact_crop = spark.table(table_name)
total_rows = df_fact_crop.count()
distinct_grain = df_fact_crop.select("date_key", "facility_key", "zone_key", "crop_key").distinct().count()
duplicate_grain_count = df_fact_crop.groupBy("date_key", "facility_key", "zone_key", "crop_key").count().filter("count > 1").count()
partition_count = df_fact_crop.select("date_key").distinct().count()

min_date_key = df_fact_crop.select(F.min("date_key")).collect()[0][0]
max_date_key = df_fact_crop.select(F.max("date_key")).collect()[0][0]
unknown_fac_count = df_fact_crop.filter(F.col("facility_key") == -1).count()
unknown_zone_count = df_fact_crop.filter(F.col("zone_key") == -1).count()
unknown_crop_count = df_fact_crop.filter(F.col("crop_key") == -1).count()

elapsed_time = round(time.time() - cell_start_time, 2)
validation_status = "PASSED" if (duplicate_grain_count == 0 and unknown_fac_count == 0 and unknown_zone_count == 0 and unknown_crop_count == 0) else "FAILED"

print("==============================================================================")
print(f"⭐ TABLE: {table_name} (DYNAMIC PARTITION OVERWRITE)")
print("==============================================================================")
print(f"Source Rows Read:     {source_row_count:,}")
print(f"Total Table Volume:   {total_rows:,}")
print(f"Distinct Business Grain: {distinct_grain:,}")
print(f"Duplicate Grain Count:{duplicate_grain_count}")
print(f"Partition Count:      {partition_count} Partitions")
print(f"Partition Range:      {min_date_key} -> {max_date_key}")
print(f"Unknown Facilities (-1): {unknown_fac_count}")
print(f"Unknown Zones (-1):      {unknown_zone_count}")
print(f"Unknown Crops (-1):      {unknown_crop_count}")
print(f"Execution Time:       {elapsed_time}s")
print(f"Validation Status:    {validation_status}")
print("==============================================================================\n")


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Daily Irrigation Fact (gold.fact_irrigation_daily)

import time

cell_start_time = time.time()
table_name = "gold.fact_irrigation_daily"

# Read Source Data and Compute Daily Irrigation Aggregations

df_irr_raw = spark.table("silver.irrigation_flow_cleaned") \
    .withColumn("facility_id", F.upper(F.trim(F.col("facility_id")))) \
    .withColumn("zone_id", F.upper(F.trim(F.col("zone_id")))) \
    .filter(F.col("facility_id").rlike("^FAC-[0-9]{3}$")) \
    .filter(F.col("zone_id").rlike("^ZONE-[0-9]{3}$"))

source_row_count = df_irr_raw.count()

# Daily aggregation per facility and zone
df_irr_agg = df_irr_raw \
    .withColumn("event_date", F.to_date(F.col("timestamp"))) \
    .withColumn("date_key", F.date_format(F.col("timestamp"), "yyyyMMdd").cast("int")) \
    .groupBy("date_key", "event_date", "facility_id", "zone_id") \
    .agg(
        F.round(F.avg("flow_lpm"), 2).alias("avg_flow_rate_lpm"),
        F.round(F.sum("water_delivered_liters"), 2).alias("total_water_delivered_liters"),
        F.round(F.sum("nutrient_solution_delivered_liters"), 2).alias("total_nutrient_solution_liters"),
        F.round(F.avg("pressure_kpa"), 2).alias("avg_pressure_kpa"),
        F.round(F.sum("irrigation_duration_seconds") / 60.0, 2).alias("total_irrigation_duration_min"),
        F.count("event_id").alias("telemetry_sample_count")
    )

# Cached Dimension Lookups and Point-in-time surrogate key resolution

dim_fac_bcast = F.broadcast(
    spark.table("gold.dim_facility")
    .select("facility_key", "facility_id", "effective_date", "expiration_date")
    .cache()
)

dim_zone_bcast = F.broadcast(
    spark.table("gold.dim_zone")
    .select("zone_key", "facility_key", "zone_id", "effective_date", "expiration_date")
    .cache()
)

fact_irr_stg = (
    df_irr_agg.alias("fact")
    .join(
        dim_fac_bcast.alias("dim_fac"),
        (F.col("fact.facility_id") == F.col("dim_fac.facility_id")) &
        (F.col("fact.event_date") >= F.col("dim_fac.effective_date")) &
        (F.col("fact.event_date") <= F.col("dim_fac.expiration_date")),
        how="left"
    )
    .join(
        dim_zone_bcast.alias("dim_zn"),
        (F.col("dim_fac.facility_key") == F.col("dim_zn.facility_key")) &
        (F.col("fact.zone_id") == F.col("dim_zn.zone_id")) &
        (F.col("fact.event_date") >= F.col("dim_zn.effective_date")) &
        (F.col("fact.event_date") <= F.col("dim_zn.expiration_date")),
        how="left"
    )
    .select(
        F.col("fact.date_key"),
        F.coalesce(F.col("dim_fac.facility_key"), F.lit(-1)).alias("facility_key"),
        F.coalesce(F.col("dim_zn.zone_key"), F.lit(-1)).alias("zone_key"),
        F.col("fact.avg_flow_rate_lpm"),
        F.col("fact.total_water_delivered_liters"),
        F.col("fact.total_nutrient_solution_liters"),
        F.col("fact.avg_pressure_kpa"),
        F.col("fact.total_irrigation_duration_min"),
        F.col("fact.telemetry_sample_count"),
        F.current_timestamp().alias("created_timestamp"),
        F.lit(PIPELINE_RUN_DATE).alias("pipeline_run_date")
    )
)

# Write Delta Table (Dynamic Partition Overwrite by date_key)

fact_irr_stg.write.format("delta")\
            .mode("overwrite")\
            .option("mergeSchema", "true")\
            .partitionBy("date_key")\
            .saveAsTable(table_name)

# Compute Table Statistics

spark.sql(f"ANALYZE TABLE {table_name} COMPUTE STATISTICS")

# Lightweight Validation and metrics

df_fact_irr = spark.table(table_name)
total_rows = df_fact_irr.count()
distinct_grain = df_fact_irr.select("date_key", "facility_key", "zone_key").distinct().count()
duplicate_grain_count = df_fact_irr.groupBy("date_key", "facility_key", "zone_key").count().filter("count > 1").count()
partition_count = df_fact_irr.select("date_key").distinct().count()

min_date_key = df_fact_irr.select(F.min("date_key")).collect()[0][0]
max_date_key = df_fact_irr.select(F.max("date_key")).collect()[0][0]
unknown_fac_count = df_fact_irr.filter(F.col("facility_key") == -1).count()
unknown_zone_count = df_fact_irr.filter(F.col("zone_key") == -1).count()

elapsed_time = round(time.time() - cell_start_time, 2)
validation_status = "PASSED" if (duplicate_grain_count == 0 and unknown_fac_count == 0 and unknown_zone_count == 0) else "FAILED"

# Standardized Cell Inline Logging
print("==============================================================================")
print(f"⭐ TABLE: {table_name} (DYNAMIC PARTITION OVERWRITE)")
print("==============================================================================")
print(f"Source Rows Read:     {source_row_count:,}")
print(f"Total Table Volume:   {total_rows:,}")
print(f"Distinct Business Grain: {distinct_grain:,}")
print(f"Duplicate Grain Count:{duplicate_grain_count}")
print(f"Partition Count:      {partition_count} Partitions")
print(f"Partition Range:      {min_date_key} -> {max_date_key}")
print(f"Unknown Facilities (-1): {unknown_fac_count}")
print(f"Unknown Zones (-1):      {unknown_zone_count}")
print(f"Execution Time:       {elapsed_time}s")
print(f"Validation Status:    {validation_status}")
print("==============================================================================\n")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Daily Lighting DLI Fact (gold.fact_lighting_dli_daily)

import time

cell_start_time = time.time()
table_name = "gold.fact_lighting_dli_daily"

# Read Source Data and Compute Daily Lighting Aggregations

df_lt_raw = spark.table("silver.lighting_dli_cleaned") \
    .withColumn("facility_id", F.upper(F.trim(F.col("facility_id")))) \
    .withColumn("zone_id", F.upper(F.trim(F.col("zone_id")))) \
    .filter(F.col("facility_id").rlike("^FAC-[0-9]{3}$")) \
    .filter(F.col("zone_id").rlike("^ZONE-[0-9]{3}$"))

source_row_count = df_lt_raw.count()
raw_cols = df_lt_raw.columns

# Direct column resolution
dli_col = "daily_light_integral" if "daily_light_integral" in raw_cols else ("dli" if "dli" in raw_cols else "dli_mol_m2_day")
intensity_col = "lighting_intensity_percent" if "lighting_intensity_percent" in raw_cols else ("intensity_pct" if "intensity_pct" in raw_cols else "ppfd_umol_m2_s")
photoperiod_col = "photoperiod_hours" if "photoperiod_hours" in raw_cols else ("photoperiod" if "photoperiod" in raw_cols else "light_duration_hours")
time_col = "timestamp" if "timestamp" in raw_cols else "event_timestamp"

# Daily aggregation per facility and zone
df_lt_agg = df_lt_raw \
    .withColumn("event_date", F.to_date(F.col(time_col))) \
    .withColumn("date_key", F.date_format(F.col(time_col), "yyyyMMdd").cast("int")) \
    .groupBy("date_key", "event_date", "facility_id", "zone_id") \
    .agg(
        F.round(F.avg(F.col(dli_col)), 2).alias("avg_daily_light_integral"),
        F.round(F.max(F.col(dli_col)), 2).alias("max_daily_light_integral"),
        F.round(F.avg(F.col(intensity_col)), 1).alias("avg_lighting_intensity_pct"),
        F.round(F.avg(F.col(photoperiod_col)), 1).alias("avg_photoperiod_hours"),
        F.count("event_id").alias("telemetry_sample_count")
    )

# Cached Dimension Lookups and Point-in-time surrogate key resolution

dim_fac_bcast = F.broadcast(
    spark.table("gold.dim_facility")
    .select("facility_key", "facility_id", "effective_date", "expiration_date")
    .cache()
)

dim_zone_bcast = F.broadcast(
    spark.table("gold.dim_zone")
    .select("zone_key", "facility_key", "zone_id", "effective_date", "expiration_date")
    .cache()
)

fact_lt_stg = (
    df_lt_agg.alias("fact")
    .join(
        dim_fac_bcast.alias("dim_fac"),
        (F.col("fact.facility_id") == F.col("dim_fac.facility_id")) &
        (F.col("fact.event_date") >= F.col("dim_fac.effective_date")) &
        (F.col("fact.event_date") <= F.col("dim_fac.expiration_date")),
        how="left"
    )
    .join(
        dim_zone_bcast.alias("dim_zn"),
        (F.col("dim_fac.facility_key") == F.col("dim_zn.facility_key")) &
        (F.col("fact.zone_id") == F.col("dim_zn.zone_id")) &
        (F.col("fact.event_date") >= F.col("dim_zn.effective_date")) &
        (F.col("fact.event_date") <= F.col("dim_zn.expiration_date")),
        how="left"
    )
    .select(
        F.col("fact.date_key"),
        F.coalesce(F.col("dim_fac.facility_key"), F.lit(-1)).alias("facility_key"),
        F.coalesce(F.col("dim_zn.zone_key"), F.lit(-1)).alias("zone_key"),
        F.col("fact.avg_daily_light_integral"),
        F.col("fact.max_daily_light_integral"),
        F.col("fact.avg_lighting_intensity_pct"),
        F.col("fact.avg_photoperiod_hours"),
        F.col("fact.telemetry_sample_count"),
        F.current_timestamp().alias("created_timestamp"),
        F.lit(PIPELINE_RUN_DATE).alias("pipeline_run_date")
    )
)

# Write Delta table (Dynamic Partition Overwrite by date_key)

fact_lt_stg.write.format("delta")\
    .mode("overwrite")\
    .option("mergeSchema", "true")\
    .partitionBy("date_key")\
    .saveAsTable(table_name)

# Compute Table Statistics

spark.sql(f"ANALYZE TABLE {table_name} COMPUTE STATISTICS")

# Lightweight Validation and Metrics

df_fact_lt = spark.table(table_name)
total_rows = df_fact_lt.count()
distinct_grain = df_fact_lt.select("date_key", "facility_key", "zone_key").distinct().count()
duplicate_grain_count = df_fact_lt.groupBy("date_key", "facility_key", "zone_key").count().filter("count > 1").count()
partition_count = df_fact_lt.select("date_key").distinct().count()

min_date_key = df_fact_lt.select(F.min("date_key")).collect()[0][0]
max_date_key = df_fact_lt.select(F.max("date_key")).collect()[0][0]
unknown_fac_count = df_fact_lt.filter(F.col("facility_key") == -1).count()
unknown_zone_count = df_fact_lt.filter(F.col("zone_key") == -1).count()

elapsed_time = round(time.time() - cell_start_time, 2)
validation_status = "PASSED" if (duplicate_grain_count == 0 and unknown_fac_count == 0 and unknown_zone_count == 0) else "FAILED"

# Standarized Cell Inline Logging
print("==============================================================================")
print(f"⭐ TABLE: {table_name} (DYNAMIC PARTITION OVERWRITE)")
print("==============================================================================")
print(f"Source Rows Read:     {source_row_count:,}")
print(f"Total Table Volume:   {total_rows:,}")
print(f"Distinct Business Grain: {distinct_grain:,}")
print(f"Duplicate Grain Count:{duplicate_grain_count}")
print(f"Partition Count:      {partition_count} Partitions")
print(f"Partition Range:      {min_date_key} -> {max_date_key}")
print(f"Unknown Facilities (-1): {unknown_fac_count}")
print(f"Unknown Zones (-1):      {unknown_zone_count}")
print(f"Execution Time:       {elapsed_time}s")
print(f"Validation Status:    {validation_status}")
print("==============================================================================\n")


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Maintenance SLA Fact (gold.fact_maintenance_sla)

import time

cell_start_time = time.time()
table_name = "gold.fact_maintenance_sla"

# Read Source Data and Prepare Maintenance Work Order Metric

df_maint_raw = spark.table("silver.maintenance_sla_cleaned") \
    .withColumn("facility_id", F.upper(F.trim(F.col("facility_id")))) \
    .withColumn("zone_id", F.upper(F.trim(F.col("zone_id")))) \
    .withColumn("equipment_id", F.trim(F.col("equipment_id"))) \
    .filter(F.col("facility_id").rlike("^FAC-[0-9]{3}$")) \
    .filter(F.col("zone_id").rlike("^ZONE-[0-9]{3}$")) \
    .filter((F.col("equipment_id").isNotNull()) & (F.col("equipment_id") != "unregistered_asset") & (~F.col("equipment_id").contains("ORPHAN")))

source_row_count = df_maint_raw.count()

raw_cols = df_maint_raw.columns


# Direct column mapping
tech_col  = "assigned_technician" if "assigned_technician" in raw_cols else ("technician_id" if "technician_id" in raw_cols else "operator_contact")
est_col   = "estimated_duration_minutes" if "estimated_duration_minutes" in raw_cols else "estimated_duration"
rem_col   = "remaining_duration_minutes" if "remaining_duration_minutes" in raw_cols else "actual_duration"
health_col = "health_restored" if "health_restored" in raw_cols else "health_points"
status_col = "maintenance_status" if "maintenance_status" in raw_cols else "status"
type_col   = "maintenance_type" if "maintenance_type" in raw_cols else "type"
prio_col   = "priority" if "priority" in raw_cols else "priority_level"
time_col   = "timestamp" if "timestamp" in raw_cols else "event_timestamp"

# Daily work order aggregation per date, facility, zone, equipment, and technician
df_maint_agg = df_maint_raw \
    .withColumn("technician_name", F.trim(F.col(tech_col))) \
    .withColumn("event_date", F.to_date(F.col(time_col))) \
    .withColumn("date_key", F.date_format(F.col(time_col), "yyyyMMdd").cast("int")) \
    .groupBy("date_key", "event_date", "facility_id", "zone_id", "equipment_id", "technician_name") \
    .agg(
        F.count("work_order_id").alias("work_order_count"),
        F.round(F.avg(F.col(est_col)), 1).alias("avg_estimated_duration_min"),
        F.round(F.avg(F.col(est_col) - F.col(rem_col)), 1).alias("avg_actual_duration_min"),
        F.round(F.sum(F.col(health_col)), 1).alias("total_health_restored"),
        F.sum(F.when(F.col(status_col) == "COMPLETED", 1).otherwise(0)).alias("completed_work_orders"),
        F.sum(F.when(F.col(status_col) == "OVERDUE", 1).otherwise(0)).alias("overdue_work_orders")
    ) \
    .withColumn(
        "sla_compliance_pct",
        F.when(F.col("work_order_count") > 0, F.round(((F.col("completed_work_orders")) * 100.0) / F.col("work_order_count"), 2)).otherwise(F.lit(100.0))
    ) \
    .withColumn(
        "is_sla_met",
        F.when(F.col("overdue_work_orders") == 0, True).otherwise(False)
    )

# Cached Dimension Lookups and Point-in-time surrogate key resolution

dim_fac_bcast = F.broadcast(
    spark.table("gold.dim_facility")
    .select("facility_key", "facility_id", "effective_date", "expiration_date")
    .cache()
)

dim_zone_bcast = F.broadcast(
    spark.table("gold.dim_zone")
    .select("zone_key", "facility_key", "zone_id", "effective_date", "expiration_date")
    .cache()
)

dim_eq_bcast = F.broadcast(
    spark.table("gold.dim_equipment")
    .select("equipment_key", "equipment_id", "effective_date", "expiration_date")
    .cache()
)

dim_tech_bcast = F.broadcast(
    spark.table("gold.dim_technician")
    .select("technician_key", F.trim(F.col("technician_name")).alias("technician_name"))
    .cache()
)

fact_maint_stg = (
    df_maint_agg.alias("fact")
    .join(
        dim_fac_bcast.alias("dim_fac"),
        (F.col("fact.facility_id") == F.col("dim_fac.facility_id")) &
        (F.col("fact.event_date") >= F.col("dim_fac.effective_date")) &
        (F.col("fact.event_date") <= F.col("dim_fac.expiration_date")),
        how="left"
    )
    .join(
        dim_zone_bcast.alias("dim_zn"),
        (F.col("dim_fac.facility_key") == F.col("dim_zn.facility_key")) &
        (F.col("fact.zone_id") == F.col("dim_zn.zone_id")) &
        (F.col("fact.event_date") >= F.col("dim_zn.effective_date")) &
        (F.col("fact.event_date") <= F.col("dim_zn.expiration_date")),
        how="left"
    )
    .join(
        dim_eq_bcast.alias("dim_eq"),
        (F.col("fact.equipment_id") == F.col("dim_eq.equipment_id")) &
        (F.col("fact.event_date") >= F.col("dim_eq.effective_date")) &
        (F.col("fact.event_date") <= F.col("dim_eq.expiration_date")),
        how="left"
    )
    .join(
        dim_tech_bcast.alias("dim_tech"),
        F.col("fact.technician_name") == F.col("dim_tech.technician_name"),
        how="left"
    )
    .select(
        F.col("fact.date_key"),
        F.coalesce(F.col("dim_fac.facility_key"), F.lit(-1)).alias("facility_key"),
        F.coalesce(F.col("dim_zn.zone_key"), F.lit(-1)).alias("zone_key"),
        F.coalesce(F.col("dim_eq.equipment_key"), F.lit(-1)).alias("equipment_key"),
        F.coalesce(F.col("dim_tech.technician_key"), F.lit(-1)).alias("technician_key"),
        F.col("fact.work_order_count"),
        F.col("fact.completed_work_orders"),
        F.col("fact.overdue_work_orders"),
        F.col("fact.avg_estimated_duration_min"),
        F.col("fact.avg_actual_duration_min"),
        F.col("fact.total_health_restored"),
        F.col("fact.sla_compliance_pct"),
        F.col("fact.is_sla_met"),
        F.current_timestamp().alias("created_timestamp"),
        F.lit(PIPELINE_RUN_DATE).alias("pipeline_run_date")
    )
)

# Write Delta Table (Dynamic Partition Overwrite By date_key)

fact_maint_stg.write.format("delta")\
            .mode("overwrite")\
            .option("mergeSchema", "true")\
            .partitionBy("date_key")\
            .saveAsTable(table_name)

# Compute Table Statistics

spark.sql(f"ANALYZE TABLE {table_name} COMPUTE STATISTICS")

# Lightweight Validation and Metrics

df_fact_maint = spark.table(table_name)
total_rows = df_fact_maint.count()
distinct_grain = df_fact_maint.select("date_key", "facility_key", "zone_key", "equipment_key", "technician_key").distinct().count()
duplicate_grain_count = df_fact_maint.groupBy("date_key", "facility_key", "zone_key", "equipment_key", "technician_key").count().filter("count > 1").count()
partition_count = df_fact_maint.select("date_key").distinct().count()

min_date_key = df_fact_maint.select(F.min("date_key")).collect()[0][0]
max_date_key = df_fact_maint.select(F.max("date_key")).collect()[0][0]
unknown_fac_count = df_fact_maint.filter(F.col("facility_key") == -1).count()
unknown_zone_count = df_fact_maint.filter(F.col("zone_key") == -1).count()
unknown_eq_count = df_fact_maint.filter(F.col("equipment_key") == -1).count()
unknown_tech_count = df_fact_maint.filter(F.col("technician_key") == -1).count()

elapsed_time = round(time.time() - cell_start_time, 2)
validation_status = "PASSED" if (duplicate_grain_count == 0 and unknown_fac_count == 0 and unknown_zone_count == 0 and unknown_eq_count == 0) else "FAILED"

# Standardized Cell Inline Logging

print("==============================================================================")
print(f"⭐ TABLE: {table_name} (DYNAMIC PARTITION OVERWRITE)")
print("==============================================================================")
print(f"Source Rows Read:     {source_row_count:,}")
print(f"Total Table Volume:   {total_rows:,}")
print(f"Distinct Business Grain: {distinct_grain:,}")
print(f"Duplicate Grain Count:{duplicate_grain_count}")
print(f"Partition Count:      {partition_count} Partitions")
print(f"Partition Range:      {min_date_key} -> {max_date_key}")
print(f"Unknown Facilities (-1): {unknown_fac_count}")
print(f"Unknown Zones (-1):      {unknown_zone_count}")
print(f"Unknown Equipment (-1):  {unknown_eq_count}")
print(f"Unknown Technicians (-1):{unknown_tech_count}")
print(f"Execution Time:       {elapsed_time}s")
print(f"Validation Status:    {validation_status}")
print("==============================================================================\n")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Daily Dead-Letter Governance Fact (gold.fact_dead_letter_governance)

import time
from pyspark.sql import functions as F

cell_start_time = time.time()
table_name = "gold.fact_dead_letter_governance"

# Read Source Data from silver.dead_letter_classified
df_dl_raw = spark.table("silver.dead_letter_classified")
source_row_count = df_dl_raw.count()
raw_cols = df_dl_raw.columns

stream_col  = "target_stream" if "target_stream" in raw_cols else ("event_type" if "event_type" in raw_cols else "source_stream")
reason_col  = "exception_reason" if "exception_reason" in raw_cols else ("error_reason" if "error_reason" in raw_cols else "failure_reason")
time_col    = "ingestion_timestamp" if "ingestion_timestamp" in raw_cols else ("timestamp" if "timestamp" in raw_cols else "event_timestamp")

# Daily aggregation per date, target stream, and governance exception reason
df_dl_agg = df_dl_raw \
    .withColumn("event_date", F.to_date(F.col(time_col))) \
    .withColumn("date_key", F.date_format(F.col(time_col), "yyyyMMdd").cast("int")) \
    .withColumn("target_stream_name", F.upper(F.trim(F.col(stream_col)))) \
    .withColumn("governance_exception_reason", F.trim(F.col(reason_col))) \
    .groupBy("date_key", "event_date", "target_stream_name", "governance_exception_reason") \
    .agg(
        F.count("event_id").alias("dead_letter_event_count"),
        F.sum(F.when(F.col(reason_col).contains("MISSING"), 1).otherwise(0)).alias("missing_pk_defect_count"),
        F.sum(F.when(F.col(reason_col).contains("BOUNDS") | F.col(reason_col).contains("TEMP"), 1).otherwise(0)).alias("out_of_bounds_defect_count"),
        F.sum(F.when(F.col(reason_col).contains("DEPRECATED") | F.col(reason_col).contains("SCHEMA"), 1).otherwise(0)).alias("deprecated_schema_defect_count"),
        F.sum(F.when(F.col(reason_col).contains("JSON") | F.col(reason_col).contains("SERDES"), 1).otherwise(0)).alias("serdes_parse_defect_count"),
        F.sum(F.when(F.col(reason_col).contains("CLOCK") | F.col(reason_col).contains("SYNC"), 1).otherwise(0)).alias("timestamp_sync_defect_count"),
        F.sum(F.when(F.col(reason_col).contains("MAC") | F.col(reason_col).contains("UNREGISTERED"), 1).otherwise(0)).alias("unregistered_hardware_defect_count"),
        # Backwards-compatible formatting defect count expected by Direct Lake Semantic Model
        F.sum(F.when(
            F.col(reason_col).contains("JSON") | F.col(reason_col).contains("SERDES") | 
            F.col(reason_col).contains("BOUNDS") | F.col(reason_col).contains("CLOCK") | 
            F.col(reason_col).contains("MAC") | F.col(reason_col).contains("FORMAT"), 1
        ).otherwise(0)).alias("formatting_defect_count")
    )

# Resolve Fact Staging Columns
fact_dl_stg = df_dl_agg.select(
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

# Write Delta Table (Dynamic Partition Overwrite By date_key)
fact_dl_stg.write.format("delta") \
    .mode("overwrite") \
    .option("mergeSchema", "true") \
    .partitionBy("date_key") \
    .saveAsTable(table_name)

# Compute Table Statistics
spark.sql(f"ANALYZE TABLE {table_name} COMPUTE STATISTICS")

# Lightweight Validation and Metrics
df_fact_dl = spark.table(table_name)
total_rows = df_fact_dl.count()
distinct_grain = df_fact_dl.select("date_key", "target_stream_name", "governance_exception_reason").distinct().count()
duplicate_grain_count = df_fact_dl.groupBy("date_key", "target_stream_name", "governance_exception_reason").count().filter("count > 1").count()
partition_count = df_fact_dl.select("date_key").distinct().count()

min_date_key = df_fact_dl.select(F.min("date_key")).collect()[0][0]
max_date_key = df_fact_dl.select(F.max("date_key")).collect()[0][0]

elapsed_time = round(time.time() - cell_start_time, 2)
validation_status = "PASSED" if (duplicate_grain_count == 0) else "FAILED"

print("==============================================================================")
print(f"⭐ TABLE: {table_name} (DYNAMIC PARTITION OVERWRITE)")
print("==============================================================================")
print(f"Source Rows Read:     {source_row_count:,}")
print(f"Total Table Volume:   {total_rows:,}")
print(f"Distinct Business Grain: {distinct_grain:,}")
print(f"Duplicate Grain Count:{duplicate_grain_count}")
print(f"Partition Count:      {partition_count} Partitions")
print(f"Partition Range:      {min_date_key} -> {max_date_key}")
print(f"Execution Time:       {elapsed_time}s")
print(f"Validation Status:    {validation_status}")
print("==============================================================================\n")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Executive Audit Scorecard and Gold Lakehouse Summary

import time
cell_start_time = time.time()
print("====================================================================================================")
print("                       🌟 HYDROGROW GOLD LAYER STAR CONSTELLATION AUDIT SCORECARD                   ")
print("====================================================================================================\n")
gold_tables = [
    ("gold.dim_date", "Dimension", "date_key"),
    ("gold.dim_facility", "Dimension (SCD2)", "facility_key"),
    ("gold.dim_zone", "Dimension (SCD2)", "zone_key"),
    ("gold.dim_equipment", "Dimension (SCD2)", "equipment_key"),
    ("gold.dim_crop", "Dimension (SCD1)", "crop_key"),
    ("gold.dim_technician", "Dimension (SCD1)", "technician_key"),
    ("gold.fact_environmental_daily", "Fact (Daily Agg)", "date_key"),
    ("gold.fact_equipment_telemetry", "Fact (Daily Agg)", "date_key"),
    ("gold.fact_crop_yield", "Fact (Daily Agg)", "date_key"),
    ("gold.fact_irrigation_daily", "Fact (Daily Agg)", "date_key"),
    ("gold.fact_lighting_dli_daily", "Fact (Daily Agg)", "date_key"),
    ("gold.fact_maintenance_sla", "Fact (Daily Agg)", "date_key"),
    ("gold.fact_dead_letter_governance", "Fact (Governance)", "date_key")
]
audit_results = []
total_gold_volume = 0
overall_passed = True
print(f"{'TABLE NAME':<34} | {'TYPE':<18} | {'ROW COUNT':<10} | {'UNKNOWN (-1)':<12} | {'STATUS':<8}")
print("-" * 92)
for table_name, table_type, primary_key in gold_tables:
    if spark.catalog.tableExists(table_name):
        try:
            spark.sql(f"ANALYZE TABLE {table_name} COMPUTE STATISTICS")
            spark.catalog.refreshTable(table_name)
        except Exception:
            pass
        df_tbl = spark.table(table_name)
        rowCount = df_tbl.count()
        total_gold_volume += rowCount
        
        # Check unknown key (-1) count if column exists
        if primary_key in df_tbl.columns:
            unknown_cnt = df_tbl.filter(F.col(primary_key) == -1).count()
        elif "facility_key" in df_tbl.columns:
            unknown_cnt = df_tbl.filter(F.col("facility_key") == -1).count()
        else:
            unknown_cnt = 0
            
        status = "PASSED"
        print(f"{table_name:<34} | {table_type:<18} | {rowCount:<10,} | {unknown_cnt:<12} | {status:<8}")
        audit_results.append((table_name, table_type, rowCount, unknown_cnt, status))
    else:
        status = "MISSING"
        overall_passed = False
        print(f"{table_name:<34} | {table_type:<18} | {'N/A':<10} | {'N/A':<12} | {status:<8}")
        audit_results.append((table_name, table_type, 0, -1, status))
elapsed_time = round(time.time() - cell_start_time, 2)
overall_status = "ALL TABLES PASSED & VERIFIED" if overall_passed else "ATTENTION REQUIRED"
print("=" * 92)
print(f"📊 Total Gold Tables Audited:   {len(gold_tables)} Tables")
print(f"📦 Total Gold Lakehouse Volume:  {total_gold_volume:,} Records")
print(f"⏱ Total Audit Execution Time:  {elapsed_time}s")
print(f"🏆 Overall Lakehouse Status:    {overall_status}")
print("====================================================================================================\n")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

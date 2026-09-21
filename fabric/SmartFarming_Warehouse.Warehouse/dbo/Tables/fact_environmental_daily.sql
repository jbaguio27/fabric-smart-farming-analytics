CREATE TABLE [dbo].[fact_environmental_daily] (
    [date_key]                 INT           NULL,
    [facility_key]             BIGINT        NULL,
    [zone_key]                 BIGINT        NULL,
    [avg_ambient_temp_celsius] FLOAT (53)    NULL,
    [min_ambient_temp_celsius] FLOAT (53)    NULL,
    [max_ambient_temp_celsius] FLOAT (53)    NULL,
    [avg_humidity_pct]         FLOAT (53)    NULL,
    [avg_co2_ppm]              FLOAT (53)    NULL,
    [avg_vpd_kpa]              FLOAT (53)    NULL,
    [avg_temp_drift_celsius]   FLOAT (53)    NULL,
    [avg_stability_score]      FLOAT (53)    NULL,
    [avg_water_ph]             FLOAT (53)    NULL,
    [avg_ec_ms_cm]             FLOAT (53)    NULL,
    [telemetry_sample_count]   BIGINT        NULL,
    [created_timestamp]        DATETIME2 (6) NULL,
    [pipeline_run_date]        DATE          NULL
);


GO
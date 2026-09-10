CREATE TABLE [dbo].[fact_lighting_dli_daily] (
    [date_key]                   INT           NULL,
    [facility_key]               BIGINT        NULL,
    [zone_key]                   BIGINT        NULL,
    [avg_daily_light_integral]   FLOAT (53)    NULL,
    [max_daily_light_integral]   FLOAT (53)    NULL,
    [avg_lighting_intensity_pct] FLOAT (53)    NULL,
    [avg_photoperiod_hours]      FLOAT (53)    NULL,
    [telemetry_sample_count]     BIGINT        NULL,
    [created_timestamp]          DATETIME2 (6) NULL,
    [pipeline_run_date]          DATE          NULL
);


GO
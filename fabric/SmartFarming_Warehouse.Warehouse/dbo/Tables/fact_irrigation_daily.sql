CREATE TABLE [dbo].[fact_irrigation_daily] (
    [date_key]                       INT           NULL,
    [facility_key]                   BIGINT        NULL,
    [zone_key]                       BIGINT        NULL,
    [avg_flow_rate_lpm]              FLOAT (53)    NULL,
    [total_water_delivered_liters]   FLOAT (53)    NULL,
    [total_nutrient_solution_liters] FLOAT (53)    NULL,
    [avg_pressure_kpa]               FLOAT (53)    NULL,
    [total_irrigation_duration_min]  FLOAT (53)    NULL,
    [telemetry_sample_count]         BIGINT        NULL,
    [created_timestamp]              DATETIME2 (6) NULL,
    [pipeline_run_date]              DATE          NULL
);


GO
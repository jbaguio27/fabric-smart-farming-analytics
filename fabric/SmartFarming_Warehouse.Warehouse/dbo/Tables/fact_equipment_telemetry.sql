CREATE TABLE [dbo].[fact_equipment_telemetry] (
    [date_key]                   INT           NULL,
    [facility_key]               BIGINT        NULL,
    [equipment_key]              BIGINT        NULL,
    [zone_key]                   BIGINT        NULL,
    [avg_health_score]           FLOAT (53)    NULL,
    [max_failure_probability]    FLOAT (53)    NULL,
    [daily_runtime_hours]        FLOAT (53)    NULL,
    [avg_power_draw_kw]          FLOAT (53)    NULL,
    [total_energy_kwh]           FLOAT (53)    NULL,
    [avg_vibration_vps]          FLOAT (53)    NULL,
    [avg_operating_temp_celsius] FLOAT (53)    NULL,
    [avg_load_percent]           FLOAT (53)    NULL,
    [telemetry_sample_count]     BIGINT        NULL,
    [created_timestamp]          DATETIME2 (6) NULL,
    [pipeline_run_date]          DATE          NULL
);


GO
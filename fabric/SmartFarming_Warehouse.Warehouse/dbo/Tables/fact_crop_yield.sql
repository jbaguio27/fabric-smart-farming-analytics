CREATE TABLE [dbo].[fact_crop_yield] (
    [date_key]              INT           NULL,
    [facility_key]          BIGINT        NULL,
    [zone_key]              BIGINT        NULL,
    [crop_key]              BIGINT        NULL,
    [target_yield_kg]       FLOAT (53)    NULL,
    [total_harvest_kg]      FLOAT (53)    NULL,
    [grade_a_harvest_kg]    FLOAT (53)    NULL,
    [grade_b_harvest_kg]    FLOAT (53)    NULL,
    [spoilage_waste_kg]     FLOAT (53)    NULL,
    [yield_achievement_pct] FLOAT (53)    NULL,
    [estimated_revenue_php] FLOAT (53)    NULL,
    [avg_growth_rate_g_day] FLOAT (53)    NULL,
    [harvest_batch_count]   BIGINT        NULL,
    [created_timestamp]     DATETIME2 (6) NULL,
    [pipeline_run_date]     DATE          NULL
);


GO
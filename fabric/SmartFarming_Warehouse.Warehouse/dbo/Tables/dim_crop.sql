CREATE TABLE [dbo].[dim_crop] (
    [crop_key]                    BIGINT         NULL,
    [crop_type]                   VARCHAR (8000) NULL,
    [optimal_temperature_celsius] FLOAT (53)     NULL,
    [optimal_humidity_percent]    FLOAT (53)     NULL,
    [target_biomass_g]            FLOAT (53)     NULL,
    [harvest_cycle_days]          INT            NULL,
    [unit_price_grade_a_php]      FLOAT (53)     NULL,
    [unit_price_grade_b_php]      FLOAT (53)     NULL,
    [created_timestamp]           DATETIME2 (6)  NULL,
    [pipeline_run_date]           DATE           NULL
);


GO
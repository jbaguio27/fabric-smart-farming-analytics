CREATE TABLE [dbo].[fact_lighting_dli_daily] (

	[date_key] int NULL, 
	[facility_key] bigint NULL, 
	[zone_key] bigint NULL, 
	[avg_daily_light_integral] float NULL, 
	[max_daily_light_integral] float NULL, 
	[avg_lighting_intensity_pct] float NULL, 
	[avg_photoperiod_hours] float NULL, 
	[telemetry_sample_count] bigint NULL, 
	[created_timestamp] datetime2(6) NULL, 
	[pipeline_run_date] date NULL
);
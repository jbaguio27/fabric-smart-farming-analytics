CREATE TABLE [dbo].[dim_crop] (

	[crop_key] bigint NULL, 
	[crop_type] varchar(8000) NULL, 
	[optimal_temperature_celsius] float NULL, 
	[optimal_humidity_percent] float NULL, 
	[target_biomass_g] float NULL, 
	[harvest_cycle_days] int NULL, 
	[unit_price_grade_a_php] float NULL, 
	[unit_price_grade_b_php] float NULL, 
	[created_timestamp] datetime2(6) NULL, 
	[pipeline_run_date] date NULL
);
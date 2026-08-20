CREATE TABLE [dbo].[fact_crop_yield] (

	[date_key] int NULL, 
	[facility_key] bigint NULL, 
	[zone_key] bigint NULL, 
	[crop_key] bigint NULL, 
	[target_yield_kg] float NULL, 
	[total_harvest_kg] float NULL, 
	[grade_a_harvest_kg] float NULL, 
	[grade_b_harvest_kg] float NULL, 
	[spoilage_waste_kg] float NULL, 
	[yield_achievement_pct] float NULL, 
	[estimated_revenue_php] float NULL, 
	[avg_growth_rate_g_day] float NULL, 
	[harvest_batch_count] bigint NULL, 
	[created_timestamp] datetime2(6) NULL, 
	[pipeline_run_date] date NULL
);
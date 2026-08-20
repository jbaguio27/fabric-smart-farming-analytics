CREATE TABLE [dbo].[fact_irrigation_daily] (

	[date_key] int NULL, 
	[facility_key] bigint NULL, 
	[zone_key] bigint NULL, 
	[avg_flow_rate_lpm] float NULL, 
	[total_water_delivered_liters] float NULL, 
	[total_nutrient_solution_liters] float NULL, 
	[avg_pressure_kpa] float NULL, 
	[total_irrigation_duration_min] float NULL, 
	[telemetry_sample_count] bigint NULL, 
	[created_timestamp] datetime2(6) NULL, 
	[pipeline_run_date] date NULL
);
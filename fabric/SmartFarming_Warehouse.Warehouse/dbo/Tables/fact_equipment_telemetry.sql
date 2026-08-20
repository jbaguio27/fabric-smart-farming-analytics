CREATE TABLE [dbo].[fact_equipment_telemetry] (

	[date_key] int NULL, 
	[facility_key] bigint NULL, 
	[equipment_key] bigint NULL, 
	[zone_key] bigint NULL, 
	[avg_health_score] float NULL, 
	[max_failure_probability] float NULL, 
	[daily_runtime_hours] float NULL, 
	[avg_power_draw_kw] float NULL, 
	[total_energy_kwh] float NULL, 
	[avg_vibration_vps] float NULL, 
	[avg_operating_temp_celsius] float NULL, 
	[avg_load_percent] float NULL, 
	[telemetry_sample_count] bigint NULL, 
	[created_timestamp] datetime2(6) NULL, 
	[pipeline_run_date] date NULL
);
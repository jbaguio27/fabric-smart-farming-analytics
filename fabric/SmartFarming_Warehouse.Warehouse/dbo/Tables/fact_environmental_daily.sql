CREATE TABLE [dbo].[fact_environmental_daily] (

	[date_key] int NULL, 
	[facility_key] bigint NULL, 
	[zone_key] bigint NULL, 
	[avg_ambient_temp_celsius] float NULL, 
	[min_ambient_temp_celsius] float NULL, 
	[max_ambient_temp_celsius] float NULL, 
	[avg_humidity_pct] float NULL, 
	[avg_co2_ppm] float NULL, 
	[avg_vpd_kpa] float NULL, 
	[avg_temp_drift_celsius] float NULL, 
	[avg_stability_score] float NULL, 
	[avg_water_ph] float NULL, 
	[avg_ec_ms_cm] float NULL, 
	[telemetry_sample_count] bigint NULL, 
	[created_timestamp] datetime2(6) NULL, 
	[pipeline_run_date] date NULL
);
CREATE TABLE [dbo].[dim_facility] (

	[facility_key] bigint NULL, 
	[facility_id] varchar(8000) NULL, 
	[facility_name] varchar(8000) NULL, 
	[region] varchar(8000) NULL, 
	[city] varchar(8000) NULL, 
	[latitude] float NULL, 
	[longitude] float NULL, 
	[elevation_m] float NULL, 
	[climate_zone] varchar(8000) NULL, 
	[water_source] varchar(8000) NULL, 
	[power_grid_redundancy] varchar(8000) NULL, 
	[max_zone_capacity] int NULL, 
	[operator_contact] varchar(8000) NULL, 
	[attr_hash] bigint NULL, 
	[effective_date] date NULL, 
	[expiration_date] date NULL, 
	[is_current] bit NULL, 
	[created_timestamp] datetime2(6) NULL, 
	[pipeline_run_date] date NULL
);
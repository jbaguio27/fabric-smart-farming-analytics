CREATE TABLE [dbo].[dim_zone] (

	[zone_key] bigint NULL, 
	[facility_key] bigint NULL, 
	[zone_id] varchar(8000) NULL, 
	[zone_name] varchar(8000) NULL, 
	[section] varchar(8000) NULL, 
	[rack_capacity] int NULL, 
	[attr_hash] bigint NULL, 
	[effective_date] date NULL, 
	[expiration_date] date NULL, 
	[is_current] bit NULL, 
	[created_timestamp] datetime2(6) NULL, 
	[pipeline_run_date] date NULL
);
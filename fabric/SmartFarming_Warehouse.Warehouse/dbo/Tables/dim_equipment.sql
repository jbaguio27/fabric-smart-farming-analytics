CREATE TABLE [dbo].[dim_equipment] (

	[equipment_key] bigint NULL, 
	[facility_key] bigint NULL, 
	[zone_key] bigint NULL, 
	[equipment_id] varchar(8000) NULL, 
	[equipment_type] varchar(8000) NULL, 
	[manufacturer] varchar(8000) NULL, 
	[model_number] varchar(8000) NULL, 
	[installation_date] date NULL, 
	[attr_hash] bigint NULL, 
	[effective_date] date NULL, 
	[expiration_date] date NULL, 
	[is_current] bit NULL, 
	[created_timestamp] datetime2(6) NULL, 
	[pipeline_run_date] date NULL
);
CREATE TABLE [dbo].[dim_technician] (

	[technician_key] bigint NULL, 
	[technician_name] varchar(8000) NULL, 
	[phone_number] varchar(8000) NULL, 
	[email] varchar(8000) NULL, 
	[created_timestamp] datetime2(6) NULL, 
	[pipeline_run_date] date NULL
);
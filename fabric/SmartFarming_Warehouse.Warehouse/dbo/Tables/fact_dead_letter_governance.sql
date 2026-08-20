CREATE TABLE [dbo].[fact_dead_letter_governance] (

	[date_key] int NULL, 
	[target_stream_name] varchar(8000) NULL, 
	[governance_exception_reason] varchar(8000) NULL, 
	[dead_letter_event_count] bigint NULL, 
	[missing_pk_defect_count] bigint NULL, 
	[deprecated_schema_defect_count] bigint NULL, 
	[formatting_defect_count] bigint NULL, 
	[created_timestamp] datetime2(6) NULL, 
	[pipeline_run_date] date NULL
);
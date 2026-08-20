CREATE TABLE [dbo].[fact_maintenance_sla] (

	[date_key] int NULL, 
	[facility_key] bigint NULL, 
	[zone_key] bigint NULL, 
	[equipment_key] bigint NULL, 
	[technician_key] bigint NULL, 
	[work_order_count] bigint NULL, 
	[completed_work_orders] bigint NULL, 
	[overdue_work_orders] bigint NULL, 
	[avg_estimated_duration_min] float NULL, 
	[avg_actual_duration_min] float NULL, 
	[total_health_restored] float NULL, 
	[sla_compliance_pct] float NULL, 
	[is_sla_met] bit NULL, 
	[created_timestamp] datetime2(6) NULL, 
	[pipeline_run_date] date NULL
);
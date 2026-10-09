CREATE TABLE [dbo].[fact_maintenance_sla] (
    [date_key]                   INT           NULL,
    [facility_key]               BIGINT        NULL,
    [zone_key]                   BIGINT        NULL,
    [equipment_key]              BIGINT        NULL,
    [technician_key]             BIGINT        NULL,
    [work_order_count]           BIGINT        NULL,
    [completed_work_orders]      BIGINT        NULL,
    [overdue_work_orders]        BIGINT        NULL,
    [avg_estimated_duration_min] FLOAT (53)    NULL,
    [avg_actual_duration_min]    FLOAT (53)    NULL,
    [total_health_restored]      FLOAT (53)    NULL,
    [sla_compliance_pct]         FLOAT (53)    NULL,
    [is_sla_met]                 BIT           NULL,
    [created_timestamp]          DATETIME2 (6) NULL,
    [pipeline_run_date]          DATE          NULL
);


GO
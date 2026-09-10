CREATE TABLE [dbo].[fact_dead_letter_governance] (
    [date_key]                           INT            NULL,
    [target_stream_name]                 VARCHAR (8000) NULL,
    [governance_exception_reason]        VARCHAR (8000) NULL,
    [dead_letter_event_count]            BIGINT         NULL,
    [auto_remediated_count]              BIGINT         NULL,
    [quarantined_count]                  BIGINT         NULL,
    [missing_pk_defect_count]            BIGINT         NULL,
    [out_of_bounds_defect_count]         BIGINT         NULL,
    [deprecated_schema_defect_count]     BIGINT         NULL,
    [serdes_parse_defect_count]          BIGINT         NULL,
    [timestamp_sync_defect_count]        BIGINT         NULL,
    [unregistered_hardware_defect_count] BIGINT         NULL,
    [formatting_defect_count]            BIGINT         NULL,
    [remediation_success_rate_pct]       FLOAT (53)     NULL,
    [created_timestamp]                  DATETIME2 (6)  NULL,
    [pipeline_run_date]                  DATE           NULL
);


GO
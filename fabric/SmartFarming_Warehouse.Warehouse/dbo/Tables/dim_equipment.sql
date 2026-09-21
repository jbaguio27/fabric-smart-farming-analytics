CREATE TABLE [dbo].[dim_equipment] (
    [equipment_key]     BIGINT         NULL,
    [facility_key]      BIGINT         NULL,
    [zone_key]          BIGINT         NULL,
    [equipment_id]      VARCHAR (8000) NULL,
    [equipment_type]    VARCHAR (8000) NULL,
    [manufacturer]      VARCHAR (8000) NULL,
    [model_number]      VARCHAR (8000) NULL,
    [installation_date] DATE           NULL,
    [attr_hash]         BIGINT         NULL,
    [effective_date]    DATE           NULL,
    [expiration_date]   DATE           NULL,
    [is_current]        BIT            NULL,
    [created_timestamp] DATETIME2 (6)  NULL,
    [pipeline_run_date] DATE           NULL
);


GO
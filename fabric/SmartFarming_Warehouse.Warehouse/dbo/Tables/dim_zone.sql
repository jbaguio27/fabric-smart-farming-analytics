CREATE TABLE [dbo].[dim_zone] (
    [zone_key]          BIGINT         NULL,
    [facility_key]      BIGINT         NULL,
    [facility_id]       VARCHAR (8000) NULL,
    [zone_id]           VARCHAR (8000) NULL,
    [zone_name]         VARCHAR (8000) NULL,
    [section]           VARCHAR (8000) NULL,
    [rack_capacity]     INT            NULL,
    [attr_hash]         BIGINT         NULL,
    [effective_date]    DATE           NULL,
    [expiration_date]   DATE           NULL,
    [is_current]        BIT            NULL,
    [created_timestamp] DATETIME2 (6)  NULL,
    [pipeline_run_date] DATE           NULL
);


GO
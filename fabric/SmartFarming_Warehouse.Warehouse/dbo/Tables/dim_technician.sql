CREATE TABLE [dbo].[dim_technician] (
    [technician_key]    BIGINT         NULL,
    [technician_name]   VARCHAR (8000) NULL,
    [phone_number]      VARCHAR (8000) NULL,
    [email]             VARCHAR (8000) NULL,
    [created_timestamp] DATETIME2 (6)  NULL,
    [pipeline_run_date] DATE           NULL
);


GO
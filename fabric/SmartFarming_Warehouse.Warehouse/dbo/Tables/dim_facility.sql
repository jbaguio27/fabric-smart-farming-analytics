CREATE TABLE [dbo].[dim_facility] (
    [facility_key]          BIGINT         NULL,
    [facility_id]           VARCHAR (8000) NULL,
    [facility_name]         VARCHAR (8000) NULL,
    [region]                VARCHAR (8000) NULL,
    [short_region]          VARCHAR (8000) NULL,
    [city]                  VARCHAR (8000) NULL,
    [latitude]              FLOAT (53)     NULL,
    [longitude]             FLOAT (53)     NULL,
    [elevation_m]           FLOAT (53)     NULL,
    [climate_zone]          VARCHAR (8000) NULL,
    [water_source]          VARCHAR (8000) NULL,
    [power_grid_redundancy] VARCHAR (8000) NULL,
    [max_zone_capacity]     INT            NULL,
    [operator_contact]      VARCHAR (8000) NULL,
    [attr_hash]             BIGINT         NULL,
    [effective_date]        DATE           NULL,
    [expiration_date]       DATE           NULL,
    [is_current]            BIT            NULL,
    [created_timestamp]     DATETIME2 (6)  NULL,
    [pipeline_run_date]     DATE           NULL
);


GO
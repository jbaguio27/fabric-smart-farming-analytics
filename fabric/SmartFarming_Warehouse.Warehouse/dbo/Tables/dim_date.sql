CREATE TABLE [dbo].[dim_date] (
    [date_key]         INT            NULL,
    [full_date]        DATE           NULL,
    [year]             INT            NULL,
    [quarter]          INT            NULL,
    [month]            INT            NULL,
    [month_name]       VARCHAR (8000) NULL,
    [month_year]       VARCHAR (8000) NULL,
    [year_month_sort]  INT            NULL,
    [short_month_year] VARCHAR (8000) NULL,
    [day_of_month]     INT            NULL,
    [day_of_week]      INT            NULL,
    [day_name]         VARCHAR (8000) NULL,
    [day_of_year]      INT            NULL,
    [week_of_year]     INT            NULL,
    [is_weekend]       BIT            NULL,
    [fiscal_year]      INT            NULL,
    [fiscal_quarter]   INT            NULL,
    [fiscal_period]    INT            NULL,
    [is_month_end]     BIT            NULL,
    [is_quarter_end]   BIT            NULL,
    [is_year_end]      BIT            NULL
);


GO
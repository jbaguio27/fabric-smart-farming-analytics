CREATE TABLE [dbo].[dim_date] (

	[date_key] int NULL, 
	[full_date] date NULL, 
	[year] int NULL, 
	[quarter] int NULL, 
	[month] int NULL, 
	[month_name] varchar(8000) NULL, 
	[day_of_month] int NULL, 
	[day_of_week] int NULL, 
	[day_name] varchar(8000) NULL, 
	[day_of_year] int NULL, 
	[week_of_year] int NULL, 
	[is_weekend] bit NULL, 
	[fiscal_year] int NULL, 
	[fiscal_quarter] int NULL, 
	[fiscal_period] int NULL, 
	[is_month_end] bit NULL, 
	[is_quarter_end] bit NULL, 
	[is_year_end] bit NULL
);
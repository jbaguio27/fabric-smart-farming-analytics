CREATE SECURITY POLICY [Security].[Policy_RowLevelSecurity_RegionalAccess]
    ADD FILTER PREDICATE [Security].[fn_SecurityPredicate_FacilityRegion]([region]) ON [dbo].[dim_facility]
    WITH (STATE = ON);


GO
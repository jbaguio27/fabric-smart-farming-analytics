CREATE FUNCTION Security.fn_SecurityPredicate_FacilityRegion(@region AS VARCHAR(8000))
RETURNS TABLE
WITH SCHEMABINDING
AS
RETURN SELECT 1 AS fn_SecurityPredicate_FacilityRegion_result
WHERE
    IS_MEMBER('HydroGrow_Platform_Admins') = 1
    OR IS_MEMBER('HydroGrow_Executive_Operations') = 1
    OR IS_MEMBER('db_owner') = 1
    OR (IS_MEMBER('HydroGrow_Regional_NCR') = 1 AND @region = 'NCR')
    OR (IS_MEMBER('HydroGrow_Regional_Luzon') = 1 AND @region IN ('CAR', 'Region III', 'Region IV-A'))
    OR (IS_MEMBER('HydroGrow_Regional_Visayas') = 1 AND @region IN ('Region VI', 'Region VII'))
    OR (IS_MEMBER('HydroGrow_Regional_Mindanao') = 1 AND @region = 'Region XI')
    OR CAST(SESSION_CONTEXT(N'FacilityRegion') AS VARCHAR(8000)) = @region;

GO
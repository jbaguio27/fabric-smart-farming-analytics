"""Integration Test Suite: Step 8 - Enterprise Security & Governance.

Validates:
1. Security schema creation.
2. Regional Row-Level Security (RLS) predicate function (fn_SecurityPredicate_FacilityRegion).
3. Warehouse Security Policy binding to dbo.dim_facility.
4. Dynamic Data Masking (DDM) for PII (operator_contact) on dbo.dim_facility.
5. Strict alignment with docs/architecture/security-model.md.
"""

import os
import unittest


class TestStep8SecurityGovernance(unittest.TestCase):
    """Test suite validating Enterprise Security & Governance artifacts in Microsoft Fabric."""

    @classmethod
    def setUpClass(cls):
        cls.repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
        cls.warehouse_dir = os.path.join(
            cls.repo_root, "fabric", "SmartFarming_Warehouse.Warehouse"
        )
        cls.security_dir = os.path.join(cls.warehouse_dir, "Security")

    def test_security_schema_exists(self):
        """Verify that the [Security] schema creation script exists."""
        schema_file = os.path.join(self.security_dir, "Security.sql")
        self.assertTrue(os.path.exists(schema_file), f"Missing {schema_file}")
        with open(schema_file, "r", encoding="utf-8") as f:
            content = f.read()
        self.assertIn("CREATE SCHEMA [Security]", content)

    def test_rls_predicate_function(self):
        """Verify the RLS inline table-valued predicate function definition."""
        func_file = os.path.join(
            self.security_dir, "Functions", "fn_SecurityPredicate_FacilityRegion.sql"
        )
        self.assertTrue(os.path.exists(func_file), f"Missing {func_file}")
        with open(func_file, "r", encoding="utf-8") as f:
            content = f.read()

        # Check function signature & schema binding
        self.assertIn("CREATE FUNCTION Security.fn_SecurityPredicate_FacilityRegion", content)
        self.assertIn("WITH SCHEMABINDING", content)
        self.assertIn("RETURNS TABLE", content)

        # Check role-based regional predicates
        self.assertIn("HydroGrow_Platform_Admins", content)
        self.assertIn("HydroGrow_Executive_Operations", content)
        self.assertIn("db_owner", content)
        self.assertIn("HydroGrow_Regional_NCR", content)
        self.assertIn("HydroGrow_Regional_Luzon", content)
        self.assertIn("HydroGrow_Regional_Visayas", content)
        self.assertIn("HydroGrow_Regional_Mindanao", content)

        # Check session context override for Power BI Direct Lake
        self.assertIn("SESSION_CONTEXT(N'FacilityRegion')", content)

    def test_rls_security_policy(self):
        """Verify the RLS security policy binding to dbo.dim_facility."""
        policy_file = os.path.join(
            self.security_dir, "Security", "Policy_RowLevelSecurity_RegionalAccess.sql"
        )
        self.assertTrue(os.path.exists(policy_file), f"Missing {policy_file}")
        with open(policy_file, "r", encoding="utf-8") as f:
            content = f.read()

        self.assertIn("CREATE SECURITY POLICY [Security].[Policy_RowLevelSecurity_RegionalAccess]", content)
        self.assertIn("ADD FILTER PREDICATE [Security].[fn_SecurityPredicate_FacilityRegion]([region])", content)
        self.assertIn("ON [dbo].[dim_facility]", content)
        self.assertIn("STATE = ON", content)

    def test_dim_facility_ddm_masking(self):
        """Verify that dbo.dim_facility enforces Dynamic Data Masking on operator_contact."""
        table_file = os.path.join(self.warehouse_dir, "dbo", "Tables", "dim_facility.sql")
        self.assertTrue(os.path.exists(table_file), f"Missing {table_file}")
        with open(table_file, "r", encoding="utf-8") as f:
            content = f.read()

        self.assertIn("[operator_contact]", content)
        self.assertIn("MASKED WITH (FUNCTION = 'email()')", content)


if __name__ == "__main__":
    unittest.main()

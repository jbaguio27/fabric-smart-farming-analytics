"""Integration Test Suite: Step 9 - CI/CD Deployment Pipelines & ALM Configuration.

Validates:
1. GitHub Actions CI workflow (.github/workflows/ci.yml).
2. Multi-stage environment configuration schema (config/environments.json).
3. Microsoft Fabric Deployment Pipeline promotion rules (config/deployment_rules.json).
"""

import os
import json
import unittest


class TestStep9CICDDeployment(unittest.TestCase):
    """Test suite validating CI/CD and deployment pipeline configuration artifacts."""

    @classmethod
    def setUpClass(cls):
        cls.repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
        cls.ci_file = os.path.join(cls.repo_root, ".github", "workflows", "ci.yml")
        cls.env_file = os.path.join(cls.repo_root, "config", "environments.json")
        cls.rules_file = os.path.join(cls.repo_root, "config", "deployment_rules.json")

    def test_github_actions_ci_workflow(self):
        """Verify that .github/workflows/ci.yml exists and contains test execution steps."""
        self.assertTrue(os.path.exists(self.ci_file), f"Missing {self.ci_file}")
        with open(self.ci_file, "r", encoding="utf-8") as f:
            content = f.read()

        self.assertIn("actions/checkout@v4", content)
        self.assertIn("actions/setup-python@v5", content)
        self.assertIn("python -m unittest discover -s tests -v", content)

    def test_environments_configuration_schema(self):
        """Verify that config/environments.json defines Dev, Test, and Prod stages."""
        self.assertTrue(os.path.exists(self.env_file), f"Missing {self.env_file}")
        with open(self.env_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        self.assertIn("environments", data)
        envs = data["environments"]
        self.assertIn("development", envs)
        self.assertIn("test", envs)
        self.assertIn("production", envs)

        # Check capacity and Lakehouse definitions
        self.assertEqual(envs["development"]["capacity_sku"], "F64")
        self.assertEqual(envs["production"]["capacity_sku"], "F128")
        self.assertTrue(envs["production"]["lakehouse"]["delta_vorder_enabled"])

    def test_deployment_rules_schema(self):
        """Verify that config/deployment_rules.json defines parameter replacement rules."""
        self.assertTrue(os.path.exists(self.rules_file), f"Missing {self.rules_file}")
        with open(self.rules_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        self.assertIn("deployment_rules", data)
        rules = data["deployment_rules"]
        item_types = [r["item_type"] for r in rules]
        self.assertIn("DataPipeline", item_types)
        self.assertIn("SemanticModel", item_types)
        self.assertIn("Reflex", item_types)


if __name__ == "__main__":
    unittest.main()

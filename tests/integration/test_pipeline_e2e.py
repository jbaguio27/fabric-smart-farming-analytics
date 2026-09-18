"""Integration Test Suite: Simulator End-to-End Pipeline Verification.

Wraps verify_pipeline sanity checks into standard unittest execution.
"""

import os
import io
import sys
import unittest
from tests.integration.verify_pipeline import (
    build_verification_context,
    verify_equipment_telemetry_generator,
    verify_crop_state_manager,
    verify_crop_lifecycle_generator,
    verify_crop_telemetry_generator,
    verify_irrigation_telemetry_generator,
    verify_lighting_telemetry_generator,
    verify_simulator_lifecycle,
)


class TestSimulatorPipelineE2E(unittest.TestCase):
    """End-to-end integration test running simulator lifecycle and generators."""

    @classmethod
    def setUpClass(cls):
        # Build shared verification context once for efficiency
        cls.context = build_verification_context()

    def test_equipment_telemetry(self):
        """Verify equipment state and telemetry generator."""
        # Suppress verbose stdout during test run
        old_stdout = sys.stdout
        sys.stdout = io.StringIO()
        try:
            verify_equipment_telemetry_generator(self.context)
        finally:
            sys.stdout = old_stdout

    def test_crop_state_and_lifecycle(self):
        """Verify crop state manager and lifecycle generator."""
        old_stdout = sys.stdout
        sys.stdout = io.StringIO()
        try:
            verify_crop_state_manager(self.context)
            verify_crop_lifecycle_generator(self.context)
            verify_crop_telemetry_generator(self.context)
        finally:
            sys.stdout = old_stdout

    def test_irrigation_and_lighting(self):
        """Verify irrigation and lighting telemetry generators."""
        old_stdout = sys.stdout
        sys.stdout = io.StringIO()
        try:
            verify_irrigation_telemetry_generator(self.context)
            verify_lighting_telemetry_generator(self.context)
        finally:
            sys.stdout = old_stdout

    def test_simulator_lifecycle_execution(self):
        """Verify complete simulator lifecycle execution."""
        old_stdout = sys.stdout
        sys.stdout = io.StringIO()
        try:
            verify_simulator_lifecycle()
        finally:
            sys.stdout = old_stdout


if __name__ == "__main__":
    unittest.main()

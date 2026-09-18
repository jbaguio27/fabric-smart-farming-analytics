"""Unit Test Suite: IoT Simulator Telemetry Event Models.

Validates that telemetry event models instantiate correctly and inherit BaseEvent metadata.
"""

import unittest
from smart_farming.config import SENSOR_STATUS_HEALTHY
from smart_farming.config.constants import (
    EVENT_TYPE_ENVIRONMENTAL,
    EVENT_TYPE_EQUIPMENT,
)
from smart_farming.models import (
    EnvironmentalTelemetryEvent,
    IrrigationTelemetryEvent,
    LightingTelemetryEvent,
    EquipmentTelemetryEvent,
    EquipmentOperatingStatus,
)


class TestTelemetryGenerators(unittest.TestCase):
    """Unit tests for smart farming telemetry event models."""

    def test_environmental_telemetry_event_creation(self):
        """Verify EnvironmentalTelemetryEvent model fields and BaseEvent inheritance."""
        event = EnvironmentalTelemetryEvent(
            event_type=EVENT_TYPE_ENVIRONMENTAL,
            facility_id="fac-001",
            zone_id="zone-01",
            sensor_type="temperature",
            sensor_value=24.5,
            unit="celsius",
            sensor_status=SENSOR_STATUS_HEALTHY,
            weather="Sunny",
            is_daytime=True,
        )
        self.assertEqual(event.facility_id, "fac-001")
        self.assertEqual(event.sensor_type, "temperature")
        self.assertAlmostEqual(event.sensor_value, 24.5)
        self.assertEqual(len(event.event_id), 36)
        self.assertEqual(event.operator_contact, "tech.fac-001@smartfarm.ph")
        self.assertFalse(event.is_alert())

    def test_irrigation_telemetry_event_creation(self):
        """Verify IrrigationTelemetryEvent model fields and BaseEvent inheritance."""
        event = IrrigationTelemetryEvent(
            event_type="irrigation",
            facility_id="fac-001",
            zone_id="zone-01",
            irrigation_active=True,
            flow_rate_liters_per_minute=12.5,
            pressure_kpa=250.0,
            irrigation_duration_seconds=120,
            water_delivered_liters=25.0,
            nutrient_solution_delivered_liters=2.5,
        )
        self.assertEqual(event.facility_id, "fac-001")
        self.assertTrue(event.irrigation_active)
        self.assertAlmostEqual(event.flow_rate_liters_per_minute, 12.5)
        self.assertEqual(len(event.event_id), 36)

    def test_lighting_telemetry_event_creation(self):
        """Verify LightingTelemetryEvent model fields and BaseEvent inheritance."""
        event = LightingTelemetryEvent(
            event_type="lighting",
            facility_id="fac-001",
            zone_id="zone-01",
            lighting_enabled=True,
            lighting_intensity_percent=85.0,
            photoperiod_hours=16.0,
            daily_light_integral=18.5,
        )
        self.assertEqual(event.facility_id, "fac-001")
        self.assertTrue(event.lighting_enabled)
        self.assertAlmostEqual(event.lighting_intensity_percent, 85.0)
        self.assertEqual(len(event.event_id), 36)

    def test_equipment_telemetry_event_creation(self):
        """Verify EquipmentTelemetryEvent model fields and BaseEvent inheritance."""
        event = EquipmentTelemetryEvent(
            event_type=EVENT_TYPE_EQUIPMENT,
            facility_id="fac-001",
            equipment_id="eq-pump-01",
            zone_id="zone-01",
            equipment_type="PUMP",
            operating_status=EquipmentOperatingStatus.ONLINE,
            health=98.5,
            runtime_hours=145.0,
            current_load=65.0,
            failure_probability=0.002,
            power_consumption_kw=1.5,
            operating_temperature_c=38.0,
            vibration_vps=1.1,
        )
        self.assertEqual(event.equipment_id, "eq-pump-01")
        self.assertEqual(event.operating_status, EquipmentOperatingStatus.ONLINE)
        self.assertAlmostEqual(event.health, 98.5)
        self.assertEqual(len(event.event_id), 36)


if __name__ == "__main__":
    unittest.main()

"""
Equipment sensor profile schema.

This module defines immutable baseline operating characteristics used
when simulating equipment telemetry.

Each equipment category owns one sensor profile describing its expected
power consumption, operating temperature, and vibration envelope.

The profile acts purely as simulator configuration and contains no
runtime behaviour.
"""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class EquipmentSensorProfile:
    """
    Immutable baseline telemetry profile.

    Attributes
    ----------
    idle_power_kw:
        Expected idle electrical consumption.

    max_power_kw:
        Expected power draw under maximum operating load.

    base_temperature_celsius:
        Expected operating temperature at idle.

    max_temperature_celsius:
        Expected operating temperature under maximum load.

    base_vibration_mm_s:
        Expected vibration while lightly loaded.

    max_vibration_mm_s:
        Expected vibration under maximum operating load.
    """

    idle_power_kw: float
    max_power_kw: float

    base_temperature_celsius: float
    max_temperature_celsius: float

    base_vibration_mm_s: float
    max_vibration_mm_s: float
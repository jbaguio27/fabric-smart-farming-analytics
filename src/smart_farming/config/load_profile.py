"""
Equipment load profile configuration.

This module defines immutable operating profiles for each equipment
type used by the HydroGrow Smart Farming Simulator.

Each profile describes the expected operating range and preferred target
load around which equipment utilization naturally fluctuates during
simulation.
"""

from dataclasses import dataclass
from typing import Final

@dataclass(frozen=True, slots=True)
class EquipmentLoadProfile:
    """
    Immutable operating profile for an equipment type.

    Attributes:
        minimum:
            Minimum expected operating load percentage.

        maximum:
            Maximum expected operating load percentage.

        target:
            Preferred steady-state operating load percentage.

        wear_multiplier:
        Relative wear rate compared to a baseline asset.

        normal_threshold:
            Load percentage below which stress has minimal impact.

        warning_threshold:
            Load percentage above which stress begins accelerating.

        moderate_factor_max:
            Maximum stress contribution while operating inside the
            moderate load band.

        critical_factor_max:
            Maximum stress contribution while operating inside the
            critical load band.
    """

    minimum: Final[float]
    maximum: Final[float]
    target: Final[float]

    wear_multiplier: Final[float]
    failure_multiplier: Final[float]
    normal_threshold: Final[float]
    warning_threshold: Final[float]
    moderate_factor_max: Final[float]
    critical_factor_max: Final[float]

@dataclass(frozen=True, slots=True)
class EquipmentSensorProfile:
    """
    Immutable sensor profile for an equipment type.

    This profile defines realistic baseline telemetry ranges for
    equipment-mounted sensors. The simulator uses these ranges to derive
    power consumption, operating temperature, and vibration from runtime
    state without embedding equipment-specific constants in business
    logic.

    Attributes:
        idle_power_kw:
            Expected power draw when equipment is running near minimum
            operating load.

        max_power_kw:
            Expected power draw when equipment is running near maximum
            operating load.

        base_temperature_celsius:
            Expected operating temperature under low stress.

        max_temperature_celsius:
            Maximum expected operating temperature under normal simulated
            operating conditions.

        base_vibration_mm_s:
            Expected vibration velocity under low stress.

        max_vibration_mm_s:
            Maximum expected vibration velocity under normal simulated
            operating conditions.
    """

    idle_power_kw: Final[float]
    max_power_kw: Final[float]
    base_temperature_celsius: Final[float]
    max_temperature_celsius: Final[float]
    base_vibration_mm_s: Final[float]
    max_vibration_mm_s: Final[float]


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
    normal_threshold: Final[float]
    warning_threshold: Final[float]
    moderate_factor_max: Final[float]
    critical_factor_max: Final[float]
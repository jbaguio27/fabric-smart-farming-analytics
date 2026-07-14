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
    """

    minimum: Final[float]
    maximum: Final[float]
    target: Final[float]
"""
Equipment load profile schema.

This module defines the immutable configuration describing the expected
operating load characteristics for a particular equipment category.

Load profiles are consumed by the EquipmentStateManager when calculating
equipment utilization, wear, and failure probability.

These objects contain configuration only and never represent runtime
simulation state.
"""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class EquipmentLoadProfile:
    """
    Immutable operating profile for an equipment category.

    Attributes
    ----------
    minimum:
        Minimum expected operating load percentage.

    target:
        Preferred operating load percentage.

    maximum:
        Maximum normal operating load percentage.

    normal_threshold:
        Load threshold considered normal.

    warning_threshold:
        Load threshold where elevated stress begins.

    wear_multiplier:
        Relative wear multiplier applied to health degradation.

    failure_multiplier:
        Relative failure multiplier applied to failure probability.

    moderate_factor_max:
        Maximum contribution from moderate load stress.

    critical_factor_max:
        Maximum contribution from critical load stress.
    """

    minimum: float
    target: float
    maximum: float

    normal_threshold: float
    warning_threshold: float

    wear_multiplier: float
    failure_multiplier: float

    moderate_factor_max: float
    critical_factor_max: float
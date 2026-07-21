"""
Configuration schema package.

This package contains immutable configuration objects shared throughout
the simulator.

Unlike the models package, these classes do not represent runtime
business entities or telemetry events. Instead, they provide structured
configuration used to define simulation behaviour.

Examples include:
    - Equipment load profiles
    - Equipment sensor profiles
    - Crop growth profiles
    - Facility profiles
    - Lighting profiles
    - Irrigation profiles

Keeping configuration schemas separate from runtime models prevents
architectural coupling between configuration and business domains while
eliminating circular import dependencies.
"""

from .equipment_load_profile import EquipmentLoadProfile
from .equipment_sensor_profile import EquipmentSensorProfile
from .crop_growth_profile import CropGrowthProfile
from .facility_profiles import FacilityProfile

__all__ = [
    "EquipmentLoadProfile",
    "EquipmentSensorProfile",
    "CropGrowthProfile",
    "FacilityProfile"
]
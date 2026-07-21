"""
Nutrient Solution Subsystem Configuration.

This module contains domain constants and operational bounds for hydroponic
nutrient solution dosing, pH balancing, electrical conductivity (EC),
and dissolved oxygen (DO) management in vertical farming facilities.
"""

from typing import Final


# Target Baseline Nutrient Solution Bounds
TARGET_NUTRIENT_PH: Final[float] = 6.0
MIN_SAFE_NUTRIENT_PH: Final[float] = 5.5
MAX_SAFE_NUTRIENT_PH: Final[float] = 6.5

TARGET_NUTRIENT_EC_MS_CM: Final[float] = 1.8
MIN_SAFE_NUTRIENT_EC_MS_CM: Final[float] = 1.2
MAX_SAFE_NUTRIENT_EC_MS_CM: Final[float] = 2.4

TARGET_DISSOLVED_OXYGEN_MG_L: Final[float] = 8.0
MIN_SAFE_DISSOLVED_OXYGEN_MG_L: Final[float] = 6.0
MAX_SAFE_DISSOLVED_OXYGEN_MG_L: Final[float] = 10.0

# Dosing Valve Rates
NUTRIENT_DOSING_RATE_ML_PER_SEC: Final[float] = 15.0
PH_ADJUST_DOSING_RATE_ML_PER_SEC: Final[float] = 5.0

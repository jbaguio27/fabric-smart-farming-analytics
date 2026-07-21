"""
Water Hydraulics & Recirculation Subsystem Configuration.

This module contains domain constants for hydroponic reservoir capacities,
recirculation GPM flow rates, pump pressure bounds, and water chiller temperatures.
"""

from typing import Final


# Reservoir & Hydraulics Parameters
DEFAULT_RESERVOIR_CAPACITY_LITERS: Final[float] = 2500.0
MIN_RESERVOIR_WATER_LEVEL_PERCENT: Final[float] = 25.0

DEFAULT_PUMP_FLOW_RATE_GPM: Final[float] = 12.0
MIN_SAFE_PUMP_FLOW_RATE_GPM: Final[float] = 5.0
MAX_SAFE_PUMP_FLOW_RATE_GPM: Final[float] = 20.0

TARGET_PUMP_PRESSURE_PSI: Final[float] = 45.0
MIN_SAFE_PUMP_PRESSURE_PSI: Final[float] = 30.0
MAX_SAFE_PUMP_PRESSURE_PSI: Final[float] = 65.0

TARGET_CHILLER_WATER_TEMP_CELSIUS: Final[float] = 19.5

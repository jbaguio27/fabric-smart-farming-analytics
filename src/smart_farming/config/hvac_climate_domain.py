"""
HVAC Microclimate Subsystem Configuration.

This module contains domain constants for indoor vertical farming HVAC thermal load,
relative humidity management, carbon dioxide (CO2) enrichment, and airflow CFM rates.
"""

from typing import Final


# HVAC Thermal & Humidity Bounds
TARGET_AIR_TEMPERATURE_CELSIUS: Final[float] = 22.0
MIN_SAFE_AIR_TEMPERATURE_CELSIUS: Final[float] = 18.0
MAX_SAFE_AIR_TEMPERATURE_CELSIUS: Final[float] = 28.0

TARGET_RELATIVE_HUMIDITY_PERCENT: Final[float] = 68.0
MIN_SAFE_RELATIVE_HUMIDITY_PERCENT: Final[float] = 60.0
MAX_SAFE_RELATIVE_HUMIDITY_PERCENT: Final[float] = 80.0

# CO2 Enrichment & Air Circulation Bounds
TARGET_CO2_PPM: Final[float] = 1000.0
MIN_SAFE_CO2_PPM: Final[float] = 600.0
MAX_SAFE_CO2_PPM: Final[float] = 1500.0

DEFAULT_HVAC_AIRFLOW_CFM: Final[float] = 2500.0

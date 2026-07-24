"""
Application constants for the HydroGrow Smart Farming Simulator.

This module contains immutable values shared across the application.
Runtime configuration belongs in settings.py
"""

from zoneinfo import ZoneInfo
from typing import Final, TypeAlias, Mapping

# ========================================================================================
# Application Metadata
# ========================================================================================

APPLICATION_NAME: Final[str] = "HydroGrow Smart Farming Simulator"
APPLICATION_VERSION: Final[str] = "1.0.0"
APPLICATION_OWNER: Final[str] = "HydroGrow Solutions"

# ========================================================================================
# Type Aliases
# ========================================================================================

SensorMetadata: TypeAlias = dict[
    str,
    str | float | int | bool
]

FacilityId: TypeAlias = str

WeatherType: TypeAlias = str

# ========================================================================================
# Date & Time
# ========================================================================================

DEFAULT_TIMEZONE: Final[ZoneInfo] = ZoneInfo("UTC")
ISO_8601_FORMAT: Final[str] = "%Y-%m-%dT%H:%M:%S.%fZ"

# ========================================================================================
# Event Metadata
# ========================================================================================

SCHEMA_VERSION: Final[str] = "1.0"
EVENT_SOURCE: Final[str] = "hydrogrow-smart-farming-simulator"

# ========================================================================================
# Event Types
# ========================================================================================

EVENT_TYPE_ENVIRONMENTAL = "environmental"
EVENT_TYPE_EQUIPMENT = "equipment"
EVENT_TYPE_CROP = "crop"
EVENT_TYPE_MAINTENANCE = "maintenance.event"
EVENT_TYPE_FACILITY = "facility"

EVENT_TYPES: Final[tuple[str, ...]] = (
    EVENT_TYPE_ENVIRONMENTAL,
    EVENT_TYPE_EQUIPMENT,
    EVENT_TYPE_CROP,
    EVENT_TYPE_MAINTENANCE,
    EVENT_TYPE_FACILITY
)

# ========================================================================================
# Weather Simulation
# ========================================================================================

SIMULATION_START_HOUR: Final[int] = 6
SIMULATION_START_MINUTE: Final[int] = 0

# ========================================================================================
# Configuration Validation
# ========================================================================================

VALID_ENVIRONMENTS: Final[frozenset[str]] = frozenset({
    "development",
    "test",
    "production",
})

VALID_LOG_LEVELS: Final[frozenset[str]] = frozenset({
    "DEBUG",
    "INFO",
    "WARNING",
    "ERROR",
    "CRITICAL",
})

# ========================================================================================
# Simulation Configurations
# ========================================================================================

MIN_EVENT_BATCH_SIZE: Final[int] = 1
MIN_RANDOM_SEED: Final[int] = 0
MIN_SIMULATION_INTERVAL_SECONDS: Final[int] = 1
MIN_TOTAL_FACILITIES: Final[int] = 1


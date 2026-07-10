"""
Application constants for the HydroGrow Smart Farming Simulator.

This module contains immutable values shared across the application.
Runtime configuration belongs in settings.py
"""

from zoneinfo import ZoneInfo
from typing import Final

# ========================================================================================
# Application Metadata
# ========================================================================================

APPLICATION_NAME: Final[str] = 'HydroGrow Smart Farming Simulator'
APPLICATION_VERSION: Final[str] = '1.0.0'
APPLICATION_OWNER: Final[str] = 'HydroGrow Solutions'

# ========================================================================================
# Date & Time
# ========================================================================================

DEFAULT_TIMEZONE: Final[ZoneInfo] = ZoneInfo('UTC')
IS0_8601_FORMAT: Final[str] = '%Y-%m-%dT%H:%M:%SZ'

# ========================================================================================
# Event Metadata
# ========================================================================================

SCHEMA_SCHEMA_VERSION: Final[str] = '1.0'
EVENT_SOURCE: Final[str] = 'hydrogrow-smart-farming-simulator'

# ========================================================================================
# Event Types
# ========================================================================================

EVENT_TYPE_ENVIRONMENTAL = 'environmental'
EVENT_TYPE_EQUIPMENT = 'equipment'
EVENT_TYPE_CROP = 'crop'
EVENT_TYPE_MAINTENANCE = 'maintenance'
EVENT_TYPE_FACILITY = 'facility'

EVENT_TYPES: Final[tuple[str, ...]] = (
    EVENT_TYPE_ENVIRONMENTAL,
    EVENT_TYPE_EQUIPMENT,
    EVENT_TYPE_CROP,
    EVENT_TYPE_MAINTENANCE,
    EVENT_TYPE_FACILITY
)

# ========================================================================================
# Sensor Types
# ========================================================================================

SENSOR_TYPES: Final[tuple[str, ...]] = (
    'water_ph',
    'dissolved_oxygen',
    'electrical_conductivity',
    'air_temperature',
    'humidity',
    'co2',
    'light_intensity'
)

# ========================================================================================
# Equipment Status
# ========================================================================================

STATUS_ONLINE = 'ONLINE'
STATUS_OFFLINE = 'OFFLINE'
STATUS_WARNING = 'WARNING'
STATUS_ERROR = 'ERROR'

EQUIPMENT_STATUSES: Final[tuple[str, ...]] = (
    STATUS_ONLINE,
    STATUS_OFFLINE,
    STATUS_WARNING,
    STATUS_ERROR
)

# ========================================================================================
# Sensor Health
# ========================================================================================

SENSOR_STATUS_HEALTHY = 'HEALTHY'
SENSOR_STATUS_WARNING = 'WARNING'
SENSOR_STATUS_FAILED = 'FAILED'

SENSOR__HEALTH_STATUSES: Final[tuple[str, ...]] = (
    SENSOR_STATUS_HEALTHY,
    SENSOR_STATUS_WARNING,
    SENSOR_STATUS_FAILED
)

# ========================================================================================
# Crop Growth Stages
# ========================================================================================

CROP_STAGE_SEEDLING = 'SEEDLING'
CROP_STAGE_GROWING = 'GROWING'
CROP_STAGE_READY = 'READY_FOR_HARVEST'
CROP_STAGE_HARVESTED = 'HARVESTED'

CROP_STAGES: Final[tuple[str, ...]] = (
    CROP_STAGE_SEEDLING,
    CROP_STAGE_GROWING,
    CROP_STAGE_READY,
    CROP_STAGE_HARVESTED
)


# ========================================================================================
# Configuration Validation
# ========================================================================================

VALID_ENVIRONMENTS: Final[frozenset[str]] = frozenset({
    'development',
    'test',
    'production',
})

VALID_LOG_LEVELS: Final[frozenset[str]] = frozenset({
    'DEBUG',
    'INFO',
    'WARNING',
    'ERROR',
    'CRITICAL',
})

# ========================================================================================
# Validation Limits
# ========================================================================================

MIN_EVENT_BATCH_SIZE: Final[int] = 1
MIN_RANDOM_SEED: Final[int] = 0
MIN_SIMULATION_INTERVAL_SECONDS: Final[int] = 1
MIN_TOTAL_FACILITIES: Final[int] = 1
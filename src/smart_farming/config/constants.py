"""
Application constants for the HydroGrow Smart Farming Simulator.

This module contains immutable values shared across the application.
Runtime configuration belongs in settings.py
"""

from zoneinfo import ZoneInfo
from typing import Final, TypeAlias

# ========================================================================================
# Application Metadata
# ========================================================================================

APPLICATION_NAME: Final[str] = "HydroGrow Smart Farming Simulator"
APPLICATION_VERSION: Final[str] = "1.0.0"
APPLICATION_OWNER: Final[str] = "HydroGrow Solutions"

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
EVENT_TYPE_MAINTENANCE = "maintenance"
EVENT_TYPE_FACILITY = "facility"

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

SENSOR_TYPE_WATER_PH: Final[str] = "water_ph"
SENSOR_TYPE_DISSOLVED_OXYGEN: Final[str] = "dissolved_oxygen"
SENSOR_TYPE_ELECTRICAL_CONDUCTIVITY: Final[str] = "electrical_conductivity"
SENSOR_TYPE_AIR_TEMPERATURE: Final[str] = "air_temperature"
SENSOR_TYPE_HUMIDITY: Final[str] = "humidity"
SENSOR_TYPE_CO2: Final[str] = "co2"
SENSOR_TYPE_LIGHT_INTENSITY: Final[str] = "light_intensity"

SENSOR_TYPES: Final[tuple[str, ...]] = (
    SENSOR_TYPE_WATER_PH,
    SENSOR_TYPE_DISSOLVED_OXYGEN,
    SENSOR_TYPE_ELECTRICAL_CONDUCTIVITY,
    SENSOR_TYPE_AIR_TEMPERATURE,
    SENSOR_TYPE_HUMIDITY,
    SENSOR_TYPE_CO2,
    SENSOR_TYPE_LIGHT_INTENSITY,
)

# ========================================================================================
# Environmental Sensor Metadata
# ========================================================================================

SensorMetadata: TypeAlias = dict[str, str | float | int]

ENVIRONMENTAL_SENSOR_CONFIG: Final[
    dict[str, SensorMetadata]
] = {
    SENSOR_TYPE_WATER_PH: {
        "unit": "pH",
        "min_value": 5.8,
        "max_value": 6.5,
        "precision": 2,
    },
    SENSOR_TYPE_DISSOLVED_OXYGEN: {
        "unit": "mg/L",
        "min_value": 6.0,
        "max_value": 10.0,
        "precision": 1,
    },
    SENSOR_TYPE_ELECTRICAL_CONDUCTIVITY: {
        "unit": "mS/cm",
        "min_value": 1.8,
        "max_value": 3.2,
        "precision": 2, 
    },
    SENSOR_TYPE_AIR_TEMPERATURE: {
        "unit": "°C",
        "min_value": 20.0,
        "max_value": 28.0,
        "precision": 1,
    },
    SENSOR_TYPE_HUMIDITY: {
        "unit": "%",
        "min_value": 55.0,
        "max_value": 75.0,
        "precision": 1,
    },
    SENSOR_TYPE_CO2: {
        "unit": "ppm",
        "min_value": 600.0,
        "max_value": 1200.0,
        "precision": 0,
    },
    SENSOR_TYPE_LIGHT_INTENSITY: {
        "unit": "lux",
        "min_value": 20000.0,
        "max_value": 45000.0,
        "precision": 0,
    },
}

# ========================================================================================
# Equipment Status
# ========================================================================================

STATUS_ONLINE = "ONLINE"
STATUS_OFFLINE = "OFFLINE"
STATUS_WARNING = "WARNING"
STATUS_ERROR = "ERROR"

EQUIPMENT_STATUSES: Final[tuple[str, ...]] = (
    STATUS_ONLINE,
    STATUS_OFFLINE,
    STATUS_WARNING,
    STATUS_ERROR
)

# ========================================================================================
# Sensor Health
# ========================================================================================

SENSOR_STATUS_HEALTHY = "HEALTHY"
SENSOR_STATUS_WARNING = "WARNING"
SENSOR_STATUS_FAILED = "FAILED"

SENSOR__HEALTH_STATUSES: Final[tuple[str, ...]] = (
    SENSOR_STATUS_HEALTHY,
    SENSOR_STATUS_WARNING,
    SENSOR_STATUS_FAILED
)

# ========================================================================================
# Sensor Health Simulation
# ========================================================================================

SENSOR_HEALTHY_PROBABILITY: Final[float] = 0.96
SENSOR_WARNING_PROBABILITY: Final[float] = 0.03
SENSOR_FAILED_PROBABILITY: Final[float] = 0.01
WARNING_SENSOR_OFFSET_PERCENTAGE: Final[float] = 0.05

SENSOR_STATUS_PROBABILITY_SUM: Final[float] = (
    SENSOR_HEALTHY_PROBABILITY
    + SENSOR_WARNING_PROBABILITY
    + SENSOR_FAILED_PROBABILITY
)

if abs(SENSOR_STATUS_PROBABILITY_SUM - 1.0) > 1e-9:
    raise ValueError(
        "Sensor health probabilities must sum to 1.0."
    )

# ========================================================================================
# Crop Growth Stages
# ========================================================================================

CROP_STAGE_SEEDLING = "SEEDLING"
CROP_STAGE_GROWING = "GROWING"
CROP_STAGE_READY = "READY_FOR_HARVEST"
CROP_STAGE_HARVESTED = "HARVESTED"

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
# Validation Limits
# ========================================================================================

MIN_EVENT_BATCH_SIZE: Final[int] = 1
MIN_RANDOM_SEED: Final[int] = 0
MIN_SIMULATION_INTERVAL_SECONDS: Final[int] = 1
MIN_TOTAL_FACILITIES: Final[int] = 1

# ========================================================================================
# Facility Configuration
# ========================================================================================

FacilityId: TypeAlias = str

FACILITY_ID_PREFIX: Final[str] = "FAC"
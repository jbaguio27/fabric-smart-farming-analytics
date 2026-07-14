"""
Application constants for the HydroGrow Smart Farming Simulator.

This module contains immutable values shared across the application.
Runtime configuration belongs in settings.py
"""

from zoneinfo import ZoneInfo
from typing import Final, TypeAlias, Mapping
from smart_farming.config.load_profile import (
    EquipmentLoadProfile,
)

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

ENVIRONMENTAL_SENSOR_CONFIG: Final[
    dict[str, SensorMetadata]
] = {
    SENSOR_TYPE_WATER_PH: {
        "unit": "pH",
        "min_value": 5.8,
        "max_value": 6.5,
        "precision": 2,
        "healthy_drift_percentage": 0.015,
        "warning_max_deviation_percentage": 0.08,
        "weather_sensitivity": 0.05,
        "facility_variation_percentage": 0.01,
    },
    SENSOR_TYPE_DISSOLVED_OXYGEN: {
        "unit": "mg/L",
        "min_value": 6.0,
        "max_value": 10.0,
        "precision": 1,
        "healthy_drift_percentage": 0.03,
        "warning_max_deviation_percentage": 0.12,
        "weather_sensitivity": 0.10,
        "facility_variation_percentage": 0.02,
    },
    SENSOR_TYPE_ELECTRICAL_CONDUCTIVITY: {
        "unit": "mS/cm",
        "min_value": 1.8,
        "max_value": 3.2,
        "precision": 2,
        "healthy_drift_percentage": 0.025,
        "warning_max_deviation_percentage": 0.10,
        "weather_sensitivity": 0.05,
        "facility_variation_percentage": 0.02,
    },
    SENSOR_TYPE_AIR_TEMPERATURE: {
        "unit": "°C",
        "min_value": 20.0,
        "max_value": 28.0,
        "precision": 1,
        "healthy_drift_percentage": 0.04,
        "warning_max_deviation_percentage": 0.15,
        "weather_sensitivity": 0.60,
        "facility_variation_percentage": 0.05,
    },
    SENSOR_TYPE_HUMIDITY: {
        "unit": "%",
        "min_value": 55.0,
        "max_value": 75.0,
        "precision": 1,
        "healthy_drift_percentage": 0.05,
        "warning_max_deviation_percentage": 0.15,
        "weather_sensitivity": 0.80,
        "facility_variation_percentage": 0.04,
    },
    SENSOR_TYPE_CO2: {
        "unit": "ppm",
        "min_value": 600.0,
        "max_value": 1200.0,
        "precision": 0,
        "healthy_drift_percentage": 0.06,
        "warning_max_deviation_percentage": 0.20,
        "weather_sensitivity": 0.35,
        "facility_variation_percentage": 0.06,
    },
    SENSOR_TYPE_LIGHT_INTENSITY: {
        "unit": "lux",
        "min_value": 20000.0,
        "max_value": 45000.0,
        "precision": 0,
        "healthy_drift_percentage": 0.08,
        "warning_max_deviation_percentage": 0.25,
        "weather_sensitivity": 0.40,
        "facility_variation_percentage": 0.08,
    },
}

# ========================================================================================
# Equipment Types
# ========================================================================================

EQUIPMENT_TYPES: Final[tuple[str, ...]] = (
    "water_pump",
    "hvac",
    "led_panel",
    "nutrient_pump",
    "ventilation_fan",
)

EQUIPMENT_LOAD_PROFILES: Final[
    Mapping[str, EquipmentLoadProfile]
] = {
    "water_pump": EquipmentLoadProfile(
        minimum=60.0,
        maximum=95.0,
        target=80.0,
        wear_multiplier=1.35,
        failure_multiplier=1.30,
        normal_threshold=70.0,
        warning_threshold=90.0,
        moderate_factor_max=0.35,
        critical_factor_max=1.00,
    ),
    "nutrient_pump": EquipmentLoadProfile(
        minimum=45.0,
        maximum=85.0,
        target=65.0,
        wear_multiplier=1.15,
        failure_multiplier=1.15,
        normal_threshold=70.0,
        warning_threshold=90.0,
        moderate_factor_max=0.35,
        critical_factor_max=1.00,
    ),
    "hvac": EquipmentLoadProfile(
        minimum=35.0,
        maximum=90.0,
        target=60.0,
        wear_multiplier=1.00,
        failure_multiplier=1.00,
        normal_threshold=70.0,
        warning_threshold=90.0,
        moderate_factor_max=0.35,
        critical_factor_max=1.00,
    ),
    "ventilation_fan": EquipmentLoadProfile(
        minimum=25.0,
        maximum=75.0,
        target=45.0,
        wear_multiplier=0.80,
        failure_multiplier=0.80,
        normal_threshold=75.0,
        warning_threshold=95.0,
        moderate_factor_max=0.25,
        critical_factor_max=0.80,
    ),
    "led_panel": EquipmentLoadProfile(
        minimum=80.0,
        maximum=100.0,
        target=90.0,
        wear_multiplier=0.45,
        failure_multiplier=0.60,
        normal_threshold=80.0,
        warning_threshold=95.0,
        moderate_factor_max=0.20,
        critical_factor_max=0.60,
    ),
}

# ========================================================================================
# Equipment Runtime Configuration
# ========================================================================================

MAX_EQUIPMENT_HEALTH: Final[float] = 100.0
MIN_EQUIPMENT_HEALTH: Final[float] = 0.0

MAX_LOAD_CHANGE_PER_CYCLE: Final[float] = 10.0
MAX_LOAD_VARIATION_PER_CYCLE: Final[float] = 3.0

DAYTIME_DEMAND_MULTIPLIER: Final[float] = 1.05
NIGHTTIME_DEMAND_MULTIPLIER: Final[float] = 0.95

MIN_INITIAL_EQUIPMENT_HEALTH: Final[float] = 96.0
MAX_INITIAL_EQUIPMENT_HEALTH: Final[float] = 100.0

MAX_EQUIPMENT_LOAD: Final[float] = 100.0
MIN_EQUIPMENT_LOAD: Final[float] = 0.0

INITIAL_FAILURE_PROBABILITY: Final[float] = 0.0

HEALTH_DEGRADATION_PER_RUNTIME_HOUR: Final[float] = 0.02

# ========================================================================================
# Equipment Failure Simulation
# ========================================================================================

MIN_FAILURE_PROBABILITY: Final[float] = 0.0
MAX_FAILURE_PROBABILITY: Final[float] = 1.0

# ========================================================================================
# Equipment Runtime
# ========================================================================================

MAX_EQUIPMENT_RUNTIME_HOURS: Final[float] = 50_000.0

# ========================================================================================
# Failure Probability Model
# ========================================================================================

MAX_LOAD_FAILURE_ADJUSTMENT: Final[float] = 0.15
HEALTHY_EQUIPMENT_THRESHOLD: Final[float] = 90.0

NORMAL_OPERATING_LOAD_THRESHOLD: Final[float] = 60.0

# ========================================================================================
# Equipment Operating Status Simulation
# ========================================================================================

ONLINE_FAILURE_THRESHOLD: Final[float] = 0.10
WARNING_FAILURE_THRESHOLD: Final[float] = 0.35
ERROR_FAILURE_THRESHOLD: Final[float] = 0.70

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
# Environmental Simulation
# ========================================================================================

DAY_START_HOUR: Final[int] = 6
NIGHT_START_HOUR: Final[int] = 18
HOURS_PER_DAY: Final[int] = 24

ENVIRONMENTAL_VARIATION_PERCENTAGE: Final[float] = 0.20

# ========================================================================================
# Weather Simulation
# ========================================================================================

SIMULATION_START_HOUR: Final[int] = 6
SIMULATION_START_MINUTE: Final[int] = 0

WEATHER_SUNNY: Final[str] = "SUNNY"
WEATHER_CLOUDY: Final[str] = "CLOUDY"
WEATHER_RAINY: Final[str] = "RAINY"

WEATHER_TYPES: Final[tuple[WeatherType, ...]] = (
    WEATHER_SUNNY,
    WEATHER_CLOUDY,
    WEATHER_RAINY,
)

WEATHER_PROBABILITIES: Final[
    dict[WeatherType, float]
] = {
    WEATHER_SUNNY: 0.45,
    WEATHER_CLOUDY: 0.30,
    WEATHER_RAINY: 0.25,
}

WEATHER_MIN_DURATION_CYCLES: Final[int] = 6
WEATHER_MAX_DURATION_CYCLES: Final[int] = 18

# ========================================================================================
# Environmental Sensor Adjustments
# ========================================================================================

DAYTIME_SENSOR_ADJUSTMENTS: Final[
    dict[str, float]
] = {
    SENSOR_TYPE_AIR_TEMPERATURE: 1.5,
    SENSOR_TYPE_HUMIDITY: -3.0,
    SENSOR_TYPE_CO2: -60.0,
    SENSOR_TYPE_LIGHT_INTENSITY: 12000.0,
}

NIGHTTIME_SENSOR_ADJUSTMENTS: Final[
    dict[str, float]
] = {
    SENSOR_TYPE_AIR_TEMPERATURE: -1.5,
    SENSOR_TYPE_HUMIDITY: 3.0,
    SENSOR_TYPE_CO2: 60.0,
    SENSOR_TYPE_LIGHT_INTENSITY: -15000.0,
}

WEATHER_SENSOR_ADJUSTMENTS: Final[
    dict[WeatherType, dict[str, float]]
] = {
    WEATHER_SUNNY: {
        SENSOR_TYPE_AIR_TEMPERATURE: 2.0,
        SENSOR_TYPE_HUMIDITY: -4.0,
        SENSOR_TYPE_CO2: -20.0,
        SENSOR_TYPE_LIGHT_INTENSITY: 8000.0,
    },
    WEATHER_CLOUDY: {
        SENSOR_TYPE_AIR_TEMPERATURE: -0.5,
        SENSOR_TYPE_HUMIDITY: 1.5,
        SENSOR_TYPE_LIGHT_INTENSITY: -6000.0,
    },
    WEATHER_RAINY: {
        SENSOR_TYPE_AIR_TEMPERATURE: -2.5,
        SENSOR_TYPE_HUMIDITY: 8.0,
        SENSOR_TYPE_CO2: 20.0,
        SENSOR_TYPE_LIGHT_INTENSITY: -12000.0,
    },
}

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
# Simulation Configurations
# ========================================================================================

MIN_EVENT_BATCH_SIZE: Final[int] = 1
MIN_RANDOM_SEED: Final[int] = 0
MIN_SIMULATION_INTERVAL_SECONDS: Final[int] = 1
MIN_SIMULATION_CYCLE_HOURS = 1.0
MIN_TOTAL_FACILITIES: Final[int] = 1


# ========================================================================================
# Facility Configuration
# ========================================================================================

FACILITY_ID_PREFIX: Final[str] = "FAC"

ZONE_ID_PREFIX: Final[str] = "ZONE"

DEFAULT_GROWING_ZONES_PER_FACILITY: Final[int] = 3

EQUIPMENT_ID_PREFIX: Final[str] = "EQ"

EQUIPMENT_MANUFACTURERS: Final[
    dict[str, str]
] = {
    "water_pump": "Grundfos",
    "hvac": "Daikin",
    "led_panel": "Philips",
    "nutrient_pump": "Netafim",
    "ventilation_fan": "ebm-papst",
}

EQUIPMENT_MODELS: Final[
    dict[str, str]
] = {
    "water_pump": "CRN10",
    "hvac": "VRV X",
    "led_panel": "GreenPower LED",
    "nutrient_pump": "NMC Pro",
    "ventilation_fan": "AxiBlade",
}
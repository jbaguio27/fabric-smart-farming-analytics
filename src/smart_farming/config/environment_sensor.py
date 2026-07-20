from typing import Final
from .constants import SensorMetadata, WeatherType
from .environment import (
    WEATHER_SUNNY,
    WEATHER_CLOUDY,
    WEATHER_RAINY,
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
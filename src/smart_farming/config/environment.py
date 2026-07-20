from typing import Final
from .constants import WeatherType

# ========================================================================================
# Environmental Simulation
# ========================================================================================

DAY_START_HOUR: Final[int] = 6
NIGHT_START_HOUR: Final[int] = 18

ENVIRONMENTAL_VARIATION_PERCENTAGE: Final[float] = 0.20

# ========================================================================================
# Weather Simulation
# ========================================================================================

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
# Facility Configuration
# ========================================================================================

FACILITY_ID_PREFIX: Final[str] = "FAC"

ZONE_ID_PREFIX: Final[str] = "ZONE"
"""
Runtime environmental conditions for a growing zone.

This module defines the mutable environmental state maintained for each
indoor growing zone. Unlike WeatherState, which represents facility-wide
conditions such as weather and daylight, GrowingEnvironmentState models
the localized conditions experienced by crops within an individual
hydroponic zone.

Instances are owned and updated by GrowingEnvironmentStateManager.
"""

from dataclasses import dataclass


@dataclass(slots=True)
class GrowingEnvironmentState:
    """
    Mutable environmental conditions for a growing zone.

    Attributes:
        zone_id:
            Unique growing zone identifier.

        air_temperature_celsius:
            Current air temperature.

        humidity_percent:
            Relative humidity.

        water_ph:
            Nutrient solution pH.

        electrical_conductivity:
            Nutrient solution electrical conductivity (EC).
    """

    zone_id: str

    air_temperature_celsius: float

    humidity_percent: float

    water_ph: float

    electrical_conductivity: float
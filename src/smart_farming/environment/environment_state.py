"""
Represents the current environmental conditions of the simulator.
"""

from dataclasses import dataclass

from smart_farming.config import WeatherType


@dataclass(slots=True)
class EnvironmentState:
    """
    Represents the current simulated environment.

    This state is shared across all facilities during a simulation cycle.
    """

    simulation_hour: int

    weather: WeatherType

    is_daytime: bool

    remaining_weather_cycles: int
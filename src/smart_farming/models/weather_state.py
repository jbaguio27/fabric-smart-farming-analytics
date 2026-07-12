"""
Shared environmental conditions for the simulator.
"""

from dataclasses import dataclass
from datetime import datetime

from smart_farming.config import WeatherType


@dataclass(slots=True)
class WeatherState:
    """
    Represents the current shared environmental conditions.
    """

    timestamp: datetime
    weather: WeatherType
    is_daytime: bool
"""
Environmental telemetry event model for the HydroGrow Smart Farming Simulator.

This model represents a single environmental sensor reading produced by
an indoor farming facility. It extends the shared BaseEvent with
environmental telemetry specific attributes.
"""

from dataclasses import dataclass
from smart_farming.models import (
    BaseEvent,
)
from smart_farming.config import (
    SENSOR_STATUS_HEALTHY,
)


@dataclass(slots=True)
class EnvironmentalTelemetryEvent(BaseEvent):
    """
    Represents a single environmental sensor telemetry event.

    Each instance captures one sensor reading generated for a specific
    facility at a particular point in time.
    """

    sensor_type: str
    sensor_value: float | None
    unit: str
    sensor_status: str
    weather: str
    is_daytime: bool

    def is_alert(self) -> bool:
        """
        Determine whether the sensor requires attention.

        Returns:
            True if the sensor status is not healthy, otherwise False.
        """

        return self.sensor_status != SENSOR_STATUS_HEALTHY
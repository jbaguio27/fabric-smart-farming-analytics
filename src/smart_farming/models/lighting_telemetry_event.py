"""
Lighting telemetry event model.

This module defines the normalized lighting telemetry event produced by
the HydroGrow Smart Farming Simulator.

Lighting telemetry represents the operational state of the artificial
grow-light system for an individual growing zone. The event captures the
lighting conditions experienced by crops and serves as the contract
consumed by downstream analytics platforms.
"""

from dataclasses import dataclass
from datetime import datetime


@dataclass(slots=True)
class LightingTelemetryEvent:
    """
    Normalized lighting telemetry event.

    Attributes:
        event_id:
            Unique telemetry event identifier.

        event_timestamp:
            UTC timestamp when the event was generated.

        event_type:
            Event classification.

        facility_id:
            Facility identifier.

        zone_id:
            Growing zone identifier.

        lights_enabled:
            Indicates whether the lighting system is currently active.

        light_intensity_percent:
            Current LED output intensity.

        photoperiod_hours:
            Configured daily photoperiod.

        daily_light_integral:
            Estimated Daily Light Integral (mol/m²/day).
    """

    event_id: str

    event_timestamp: datetime

    event_type: str

    facility_id: str

    zone_id: str

    lights_enabled: bool

    light_intensity_percent: float

    photoperiod_hours: float

    daily_light_integral: float
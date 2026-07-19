"""
Runtime lighting state for a growing zone.

LightingState represents the mutable lighting conditions maintained by
the simulator for a single growing zone. The runtime state acts as the
authoritative source for lighting telemetry generation.

This model intentionally contains only simulation state. Event
serialization and validation are handled by higher layers.
"""

from dataclasses import dataclass


@dataclass(slots=True)
class LightingState:
    """
    Mutable runtime lighting state.

    Attributes:
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
            Current Daily Light Integral (mol/m²/day).
        """

    facility_id: str

    zone_id: str

    lights_enabled: bool

    light_intensity_percent: float

    photoperiod_hours: float

    daily_light_integral: float

    last_irrigation_cycle: int = 0

    next_irrigation_cycle: int = 0

    irrigation_interval_cycles: int = 0
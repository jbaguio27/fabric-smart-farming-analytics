"""
Runtime manager for lighting conditions.

This module owns the mutable lighting runtime state for every growing
zone within the HydroGrow Smart Farming Simulator.

The manager acts as the authoritative source of lighting information
consumed by future lighting telemetry generators and crop growth
simulation.

During this implementation milestone the manager initializes lighting
states only. Dynamic lighting control will be introduced in later
milestones.
"""

from smart_farming.config import Settings
from smart_farming.models import LightingState


class LightingStateManager:
    """
    Owns the runtime lighting state for every growing zone.

    One LightingState exists for each simulated growing zone.

    Future milestones will introduce automatic dimming,
    photoperiod scheduling, daylight strategies, and
    crop-specific lighting recipes.
    """

    def __init__(
        self,
        settings: Settings,
        zone_count: int,
    ) -> None:
        """
        Initialize the lighting state manager.

        Args:
            settings:
                Simulator configuration.

            zone_count:
                Number of growing zones.
        """

        self._settings = settings

        self._states: dict[str, LightingState] = {}

        self._initialize(zone_count)

    def _initialize(
        self,
        zone_count: int,
    ) -> None:
        """
        Create an initial lighting state for every growing zone.

        The simulator begins with all lighting systems enabled and
        operating under nominal indoor growing conditions.
        """

        self._states.clear()

        for index in range(1, zone_count + 1):

            zone_id = f"ZONE-{index:03d}"
            facility_index = ((index - 1) // 10) + 1
            facility_id = f"FAC-{min(8, max(1, facility_index)):03d}"

            self._states[zone_id] = LightingState(
                facility_id=facility_id,
                zone_id=zone_id,
                lights_enabled=True,
                light_intensity_percent=100.0,
                photoperiod_hours=16.0,
                daily_light_integral=17.0,
            )

        self._cycle_count = 0

    def get_zone_state(
        self,
        zone_id: str,
    ) -> LightingState:
        """
        Retrieve the runtime lighting state of a growing zone.
        """

        return self._states[zone_id]

    def get_all_states(
        self,
    ) -> list[LightingState]:
        """
        Return every managed lighting state.
        """

        return list(self._states.values())

    def advance_cycle(self) -> None:
        """
        Advance the lighting simulation by one cycle.

        Simulates daytime/nighttime photoperiod cycles (16h day / 8h night).
        """
        self._cycle_count = getattr(self, "_cycle_count", 0) + 1
        # 1 day = 288 cycles (5-minute cycles)
        day_cycle = self._cycle_count % 288
        # 16h day = first 192 cycles, 8h night = remaining 96 cycles
        is_day = day_cycle < 192

        for state in self._states.values():
            if is_day:
                state.lights_enabled = True
                state.light_intensity_percent = 100.0
                state.daily_light_integral = 17.0
            else:
                state.lights_enabled = False
                state.light_intensity_percent = 0.0
                state.daily_light_integral = 0.0
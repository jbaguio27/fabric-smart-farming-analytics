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

            self._states[zone_id] = LightingState(
                facility_id="FAC-001",
                zone_id=zone_id,
                lights_enabled=True,
                light_intensity_percent=100.0,
                photoperiod_hours=16.0,
                daily_light_integral=17.0,
            )

    def get_zone_state(
        self,
        zone_id: str,
    ) -> LightingState:
        """
        Retrieve the runtime lighting state of a growing zone.

        Args:
            zone_id:
                Zone identifier.

        Returns:
            Mutable LightingState instance.
        """

        return self._states[zone_id]

    def get_all_states(
        self,
    ) -> list[LightingState]:
        """
        Return every managed lighting state.

        Returns:
            Runtime lighting states.
        """

        return list(self._states.values())

    def advance_cycle(self) -> None:
        """
        Advance the lighting simulation by one cycle.

        Dynamic lighting behavior is intentionally deferred to a
        later milestone. The runtime state therefore remains
        unchanged during this implementation phase.
        """

        return
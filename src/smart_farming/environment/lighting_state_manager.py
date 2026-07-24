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

        from smart_farming.config import PHILIPPINE_FACILITY_PROFILES

        zone_recipes = {
            1: (18.0, 22.0, 100.0),  # Strawberry high PPFD
            2: (16.0, 17.0, 95.0),   # Lettuce
            3: (16.0, 18.0, 90.0),   # Kale
            4: (14.0, 15.0, 85.0),   # Spinach
            5: (14.0, 14.0, 80.0),   # Arugula
            6: (16.0, 16.5, 90.0),   # Basil
            7: (14.0, 13.5, 75.0),   # Cilantro
            8: (14.0, 14.0, 80.0),   # Parsley
            9: (18.0, 20.0, 95.0),   # Microgreens
            10: (18.0, 22.0, 100.0), # Strawberry
        }

        for facility_id, fac_profile in PHILIPPINE_FACILITY_PROFILES.items():
            for idx, micro in enumerate(fac_profile.micro_locations, start=1):
                zone_id = micro.zone_id
                state_key = f"{facility_id}:{zone_id}"

                recipe_key = ((idx - 1) % 10) + 1
                photoperiod_h, target_dli, base_intensity = zone_recipes.get(recipe_key, (16.0, 17.0, 90.0))

                self._states[state_key] = LightingState(
                    facility_id=facility_id,
                    zone_id=zone_id,
                    lights_enabled=True,
                    light_intensity_percent=base_intensity,
                    photoperiod_hours=photoperiod_h,
                    daily_light_integral=target_dli,
                )

        self._cycle_count = 0

    def get_zone_state(
        self,
        zone_id: str,
        facility_id: str | None = None,
    ) -> LightingState:
        """
        Retrieve the runtime lighting state of a growing zone.
        """
        if facility_id:
            state_key = f"{facility_id}:{zone_id}"
            if state_key in self._states:
                return self._states[state_key]

        for state in self._states.values():
            if state.zone_id == zone_id:
                return state

        return list(self._states.values())[0]

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

        Simulates zone-staggered photoperiod day/night shifts and electrical micro-variations.
        """
        self._cycle_count = getattr(self, "_cycle_count", 0) + 1

        for index, (zone_id, state) in enumerate(self._states.items(), start=1):
            # Calculate total day cycles (288 cycles per 24 hours) with zone offset
            zone_offset = (index * 24) % 288
            day_cycle = (self._cycle_count + zone_offset) % 288
            
            # Convert photoperiod_hours into cycle count threshold (1h = 12 cycles)
            daytime_cycles = int(state.photoperiod_hours * 12)
            is_day = day_cycle < daytime_cycles

            if is_day:
                state.lights_enabled = True
                # Add slight electrical supply micro-variation (e.g. +/- 1.5%)
                variation = ((self._cycle_count + index * 7) % 7 - 3) * 0.4
                # Base intensity map per zone
                recipe_key = ((index - 1) % 10) + 1
                base_intensity = {1: 100.0, 2: 95.0, 3: 90.0, 4: 85.0, 5: 80.0, 6: 90.0, 7: 75.0, 8: 80.0, 9: 95.0, 10: 100.0}.get(recipe_key, 90.0)
                state.light_intensity_percent = round(min(100.0, max(50.0, base_intensity + variation)), 1)
                
                # Calculate dynamic DLI accumulation based on photoperiod progression
                target_dli = {1: 22.0, 2: 17.0, 3: 18.0, 4: 15.0, 5: 14.0, 6: 16.5, 7: 13.5, 8: 14.0, 9: 20.0, 10: 22.0}.get(recipe_key, 17.0)
                dli_progress = round(target_dli * (day_cycle / daytime_cycles), 1)
                state.daily_light_integral = max(0.5, dli_progress)
            else:
                state.lights_enabled = False
                state.light_intensity_percent = 0.0
                state.daily_light_integral = 0.0
"""
Runtime manager for growing environment conditions.

This module owns the mutable environmental conditions for every growing
zone within the HydroGrow Smart Farming Simulator.

Unlike EnvironmentStateManager, which manages facility-wide simulation
state such as weather and time progression, this manager maintains the
localized environmental conditions experienced directly by crops.

The manager acts as the authoritative source for zone temperature,
humidity, nutrient solution pH, and electrical conductivity.
"""

from smart_farming.config import Settings
from smart_farming.models import GrowingEnvironmentState
from smart_farming.utils import RandomManager
from smart_farming.config import (
    PHILIPPINE_FACILITY_PROFILES,
    DEFAULT_AIR_TEMPERATURE_C,
    DEFAULT_RELATIVE_HUMIDITY_PERCENT,
    DEFAULT_WATER_PH,
    DEFAULT_ELECTRICAL_CONDUCTIVITY,
)

class GrowingEnvironmentStateManager:
    """
    Owns the runtime environmental conditions for all growing zones.

    One GrowingEnvironmentState instance exists for each simulated zone.

    Runtime environmental data is consumed by:

    - CropStateManager for biological health evaluation.
    - CropLifecycleGenerator for environmental telemetry generation.
    """

    def __init__(
        self,
        settings: Settings,
        random_manager: RandomManager,
        zone_count: int
    ) -> None:
        """
        Initialize the growing environment manager.

        Args:
            settings:
                Simulator configuration.

            random_manager:
                Shared random provider.

            zone_count:
                Number of growing zones to initialize.
        """

        self._settings = settings
        self._random_manager = random_manager

        self._states: dict[str, GrowingEnvironmentState] = {}

        self._initialize(zone_count)

    def _initialize(
        self,
        zone_count: int,
    ) -> None:
        """
        Create an initial environment for every growing zone.

        Initial values intentionally begin near nominal operating
        conditions. Future roadmap phases will introduce realistic
        environmental drift and equipment influence.
        """

        self._states.clear()

        for facility_id, fac_profile in PHILIPPINE_FACILITY_PROFILES.items():
            for micro in fac_profile.micro_locations:
                zone_id = micro.zone_id
                state_key = f"{facility_id}:{zone_id}"

                self._states[state_key] = GrowingEnvironmentState(
                    zone_id=zone_id,
                    air_temperature_celsius=fac_profile.target_temperature_celsius,
                    humidity_percent=fac_profile.target_humidity_percent,
                    water_ph=fac_profile.target_ph,
                    electrical_conductivity=fac_profile.target_ec,
                )

    def get_zone_state(
        self,
        zone_id: str,
        facility_id: str | None = None,
    ) -> GrowingEnvironmentState:
        """
        Retrieve the current environmental state of a zone.

        Args:
            zone_id:
                Zone identifier.
            facility_id:
                Optional facility identifier.

        Returns:
            Mutable GrowingEnvironmentState instance.
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
    ) -> list[GrowingEnvironmentState]:
        """
        Return all managed zone environments.

        Returns:
            Runtime environmental states.
        """

        return list(self._states.values())

    def advance_cycle(self) -> None:
        """
        Advance the simulated growing environment by one simulation cycle.

        Implements thermal mass inertia (cooling lag for HVAC) and humidity lag.
        Indoor temperatures nudge gradually towards the facility targets rather than shifting instantly.
        """

        for state_key, state in self._states.items():
            # Determine parent facility location and targets based on state_key (FAC-XXX:ZONE-YYY)
            try:
                facility_id = state_key.split(":")[0] if ":" in state_key else "FAC-001"
                profile = PHILIPPINE_FACILITY_PROFILES[facility_id]
                target_temp = profile.target_temperature_celsius
                target_humidity = profile.target_humidity_percent
                target_ph = profile.target_ph
                target_ec = profile.target_ec
            except (IndexError, ValueError, KeyError):
                target_temp = DEFAULT_AIR_TEMPERATURE_C
                target_humidity = DEFAULT_RELATIVE_HUMIDITY_PERCENT
                target_ph = DEFAULT_WATER_PH
                target_ec = DEFAULT_ELECTRICAL_CONDUCTIVITY

            # Thermal Lag (cooling lag rate = 0.12 per cycle)
            state.air_temperature_celsius = round(
                state.air_temperature_celsius * 0.88 + target_temp * 0.12
                + self._random_manager.uniform(-0.05, 0.05),
                2
            )

            # Humidity Lag (moisture inertia rate = 0.10 per cycle)
            state.humidity_percent = round(
                state.humidity_percent * 0.90 + target_humidity * 0.10
                + self._random_manager.uniform(-0.1, 0.1),
                2
            )

            # pH closed-loop adjustment (rate = 0.15)
            state.water_ph = round(
                state.water_ph * 0.85 + target_ph * 0.15
                + self._random_manager.uniform(-0.01, 0.01),
                2
            )

            # EC closed-loop adjustment (rate = 0.15)
            state.electrical_conductivity = round(
                state.electrical_conductivity * 0.85 + target_ec * 0.15
                + self._random_manager.uniform(-0.01, 0.01),
                2
            )


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

        for index in range(1, zone_count + 1):

            zone_id=f"ZONE-{index:03d}"

            self._states[zone_id] = GrowingEnvironmentState(
                zone_id=zone_id,
                air_temperature_celsius=DEFAULT_AIR_TEMPERATURE_C,
                humidity_percent=DEFAULT_RELATIVE_HUMIDITY_PERCENT,
                water_ph=DEFAULT_WATER_PH,
                electrical_conductivity=DEFAULT_ELECTRICAL_CONDUCTIVITY,
            )

    def get_zone_state(
        self,
        zone_id: str,
    ) -> GrowingEnvironmentState:
        """
        Retrieve the current environmental state of a zone.

        Args:
            zone_id:
                Zone identifier.

        Returns:
            Mutable GrowingEnvironmentState instance.
        """

        return self._states[zone_id]

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

        for zone_id, state in self._states.items():
            # Determine parent facility location and targets based on zone index bounds
            try:
                zone_num = int(zone_id.split("-")[1])
                facility_index = ((zone_num - 1) // 10) + 1
                facility_id = f"FAC-{min(8, max(1, facility_index)):03d}"
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


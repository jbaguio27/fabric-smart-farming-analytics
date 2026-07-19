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
    DEFAULT_AIR_TEMPERATURE_C,
    DEFAULT_RELATIVE_HUMIDITY_PERCENT,
    DEFAULT_WATER_PH,
    DEFAULT_ELECTRICAL_CONDUCTIVITY,
    AIR_TEMPERATURE_VARIATION_C,
    HUMIDITY_VARIATION_PERCENT,
    WATER_PH_VARIATION,
    EC_VARIATION,
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

        Indoor vertical farms operate under closed-loop environmental control.
        Rather than allowing abrupt environmental changes, the control systems
        continuously regulate temperature, humidity, nutrient solution pH, and
        electrical conductivity toward their configured operating targets.

        During this implementation phase a lightweight controller is used. Each
        simulation cycle nudges the current environmental state toward its
        configured target values using a small correction factor. This produces
        stable and deterministic behavior suitable for telemetry generation.

        Future milestones may replace this simplified controller with equipment-
        driven HVAC, humidification, irrigation, and nutrient dosing models.
        """

        return

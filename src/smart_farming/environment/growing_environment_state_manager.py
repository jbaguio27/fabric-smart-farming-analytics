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

class GrowingEnvironmentStateManager:
    """
    Owns the runtime environmental conditions for all growing zones.

    One GrowingEnvironmentState instance exists for each simulated zone.
    CropStateManager consumes these runtime values during health
    evaluation.
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
                air_temperature_celsius=22.0,
                humidity_percent=65.0,
                water_ph=6.0,
                electrical_conductivity=1.8,
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
"""
Runtime manager for irrigation system state.

This module owns the mutable irrigation runtime state for every growing
zone within the HydroGrow Smart Farming Simulator.

Each growing zone is assigned one IrrigationState instance that
represents the current operating condition of the irrigation subsystem.

The IrrigationStateManager is the authoritative runtime source for
irrigation-related simulation data. Telemetry generators consume this
runtime state when constructing irrigation telemetry events.

Responsibilities
----------------
The manager is responsible for:

- Creating one IrrigationState per growing zone.
- Providing lookup access to runtime irrigation state.
- Providing enumeration of all irrigation states.

Future milestones will extend this manager with irrigation scheduling,
pump operation, nutrient dosing, equipment interaction, and runtime
simulation logic.
"""

from smart_farming.models import IrrigationState


class IrrigationStateManager:
    """
    Owns the runtime irrigation state for every growing zone.
    """

    def __init__(
        self,
        zone_count: int,
    ) -> None:
        """
        Initialize runtime irrigation state.

        Args
        ----
        zone_count:
            Total number of growing zones in the simulator.
        """

        self._states: dict[str, IrrigationState] = {}

        self._initialize(zone_count)

    def _initialize(
        self,
        zone_count: int,
    ) -> None:
        """
        Create one runtime irrigation state for every growing zone.

        Initial values represent an idle irrigation system.
        """

        self._states.clear()

        for index in range(1, zone_count + 1):

            zone_id = f"ZONE-{index:03d}"

            self._states[zone_id] = IrrigationState(
                zone_id=zone_id,
                irrigation_active=False,
                flow_rate_liters_per_minute=0.0,
                pressure_kpa=0.0,
                irrigation_duration_seconds=0,
                water_delivered_liters=0.0,
                nutrient_solution_delivered_liters=0.0,
            )

    def get_zone_state(
        self,
        zone_id: str,
    ) -> IrrigationState:
        """
        Retrieve the runtime irrigation state for a growing zone.

        Args
        ----
        zone_id:
            Growing zone identifier.

        Returns
        -------
        IrrigationState
            Mutable runtime irrigation state.
        """

        return self._states[zone_id]

    def get_all_states(
        self,
    ) -> list[IrrigationState]:
        """
        Return all managed irrigation runtime states.

        Returns
        -------
        list[IrrigationState]
            Runtime irrigation state for every growing zone.
        """

        return list(self._states.values())

    def advance_cycle(self) -> None:
        """
        Advance the irrigation runtime simulation.

        During this implementation phase the irrigation subsystem remains
        idle. Future milestones will introduce irrigation scheduling,
        flow regulation, nutrient dosing, and pump behavior.

        This method exists to establish a stable runtime lifecycle that
        matches the other simulation state managers.
        """

        return
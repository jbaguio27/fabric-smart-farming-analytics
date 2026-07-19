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
from smart_farming.config import (
    DEFAULT_IRRIGATION_INTERVAL_CYCLES,
    DEFAULT_IRRIGATION_DURATION_CYCLES,
)


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
        Create the initial irrigation state for every growing zone.

        Each zone begins with a deterministic irrigation schedule initialized
        from simulator configuration. Although no irrigation controller is
        active yet, every runtime state now tracks when its first irrigation
        event should occur.

        Future milestones will allow crop-specific irrigation intervals,
        dynamic scheduling, and closed-loop irrigation decisions based on
        crop demand and environmental conditions.
        """

        self._states.clear()

        for index in range(1, zone_count + 1):

            zone_id = f"ZONE-{index:03d}"

            self._states[zone_id] = IrrigationState(
                zone_id=zone_id,
                facility_id="FAC-001",
                irrigation_active=False,
                flow_rate_liters_per_minute=0.0,
                pressure_kpa=0.0,
                irrigation_duration_seconds=0,
                water_delivered_liters=0.0,
                nutrient_solution_delivered_liters=0.0,
                last_irrigation_cycle=0,
                next_irrigation_cycle=(
                    DEFAULT_IRRIGATION_INTERVAL_CYCLES
                ),
                irrigation_interval_cycles=(
                    DEFAULT_IRRIGATION_INTERVAL_CYCLES
                )
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
        Advance irrigation simulation..

        Every simulation cycle the controller evaluates whether each
        growing zone has reached its scheduled irrigation time.

        During this milestone the controller only determines irrigation
        eligibility and updates scheduling metadata. Actual irrigation,
        hydraulic simulation, and water delivery are implemented in later
        milestones.

        Args:
            current_cycle:
                Current simulation cycle.
        """

        for state in self._states.values():

            self._update_schedule(
                state=state,
                current_cycle=current_cycle,
            )

            self._update_irrigation_state(
                state=state,
                current_cycle=current_cycle,
            )

    def _update_schedule(
        self,
        state: IrrigationState,
        current_cycle: int,
    ) -> None:
        """
        Evaluate irrigation schedule.

        This method determines whether the current simulation cycle has
        reached the zone's next scheduled irrigation event.

        During this milestone no irrigation is started. The controller
        simply records that the irrigation window has been reached and
        schedules the next irrigation interval.

        Args:
            state:
                Mutable irrigation runtime state.

            current_cycle:
                Current simulator cycle.
        """

        if current_cycle < state.next_irrigation_cycle:
            return

        state.is_irrigation_active = True

        state.last_irrigation_cycle = current_cycle

        state.next_irrigation_cycle = (
            current_cycle
            + state.irrigation_interval_cycles
        )

    def _update_irrigation_state(
        self,
        state: IrrigationState,
        current_cycle: int
    ) -> None:
        """
        Updates the current state of the irrigation system.

        This method handles the high-level controller responsibilities for 
        activating and deactivating irrigation. 

        Note:
            This controller explicitly excludes the management of fluid dynamics 
            and application metrics. The following elements remain separate 
            responsibilities handled by external modules:
            - Flow rate monitoring
            - System pressure regulation
            - Water application depth/volume tracking

        Args:
            state:
                Mutable irrigation runtime state.

            current_cycle:
                Current simulator cycle.
        """

        if not state.is_irrigation_active:
            return

        elapsed_cycles = (
            current_cycle
            - state.last_irrigation_cycle
        )

        if (
            elapsed_cycles
            >= DEFAULT_IRRIGATION_DURATION_CYCLES
        ):
            state.is_irrigation_active = False
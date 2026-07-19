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
    DEFAULT_IRRIGATION_FLOW_RATE_LPM,
    DEFAULT_IRRIGATION_PRESSURE_BAR,
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
                ),
                irrigation_end_cycle=0,
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
        Advance the irrigation controller by one simulation cycle.

        Each simulation cycle performs three independent controller stages.

        1. Evaluate irrigation schedule.
        2. Update irrigation activation.
        3. Update hydraulic operating conditions.

        Separating these responsibilities keeps the irrigation controller
        modular and allows future milestones to evolve hydraulic behavior
        independently from scheduling logic and crop demand.

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

            self._update_hydraulics(
                state=state,
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

        state.irrigation_end_cycle = (
            current_cycle
            + DEFAULT_IRRIGATION_DURATION_CYCLES
        )

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
        Update the active irrigation window.

        The irrigation controller keeps irrigation active until the configured
        end cycle is reached. Using an explicit end-cycle simplifies future
        controller enhancements, including crop-specific irrigation durations,
        manual overrides, and adaptive scheduling.

        This milestone manages only runtime activation. Hydraulic simulation,
        flow generation, pressure modeling, and water delivery remain future
        enhancements.

        Args:
            state:
                Mutable irrigation runtime state.

            current_cycle:
                Current simulator cycle.
        """

        if not state.is_irrigation_active:
            return

        if (
            current_cycle
            < state.irrigation_end_cycle
        ):
            return

        state.is_irrigation_active = False

        state.irrigation_end_cycle = 0

    def _update_hydraulics(
        self,
        state: IrrigationState,
    ) -> None:
        """
        Update irrigation hydraulic operating conditions.

        The hydraulic model is responsible for exposing the runtime
        operating conditions of an irrigation zone while irrigation is
        active.

        During this milestone hydraulic behavior remains intentionally
        deterministic. When irrigation is active the configured nominal
        flow rate and operating pressure are applied. When irrigation is
        inactive both values return immediately to zero.

        Water application is intentionally excluded from this method and
        will be implemented during the next milestone.

        Args:
            state:
                Mutable irrigation runtime state.
        """

        if state.is_irrigation_active:

            state.flow_rate_lpm = (
                DEFAULT_IRRIGATION_FLOW_RATE_LPM
            )

            state.pressure_bar = (
                DEFAULT_IRRIGATION_PRESSURE_BAR
            )

            return

        state.flow_rate_lpm = 0.0

        state.pressure_bar = 0.0
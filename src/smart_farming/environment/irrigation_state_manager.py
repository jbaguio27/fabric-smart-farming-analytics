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
    DEFAULT_WATER_APPLICATION_LITERS,
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
        self._simulation_cycle = 0

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
                next_irrigation_cycle=index % 3,
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
        """
        current_cycle = self._simulation_cycle

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

            self._update_water_delivery(
                state=state,
            )

        self._simulation_cycle += 1

    def _update_schedule(
        self,
        state: IrrigationState,
        current_cycle: int,
    ) -> None:
        """
        Evaluate irrigation schedule.
        """

        if current_cycle < state.next_irrigation_cycle:
            return

        state.irrigation_active = True

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
        """

        if not state.irrigation_active:
            return

        if (
            current_cycle
            < state.irrigation_end_cycle
        ):
            return

        state.irrigation_active = False

        state.irrigation_end_cycle = 0

    def _update_hydraulics(
        self,
        state: IrrigationState,
    ) -> None:
        """
        Update irrigation hydraulic operating conditions.
        """

        if state.irrigation_active:

            state.flow_rate_liters_per_minute = (
                DEFAULT_IRRIGATION_FLOW_RATE_LPM
            )

            # Convert 2.2 bar to 220.0 kPa
            state.pressure_kpa = (
                DEFAULT_IRRIGATION_PRESSURE_BAR * 100.0
            )

            state.irrigation_duration_seconds = 300

            return

        state.flow_rate_liters_per_minute = 0.0

        state.pressure_kpa = 0.0

        state.irrigation_duration_seconds = 0

    def _update_water_delivery(
        self,
        state: IrrigationState,
    ) -> None:
        """
        Update irrigation water delivery.
        """

        if state.irrigation_active:

            # 2.5 L/min * 5 min = 12.5 liters water delivered
            state.water_delivered_liters = round(
                state.flow_rate_liters_per_minute * 5.0, 2
            )

            # 5% nutrient dosing solution = 0.63 liters
            state.nutrient_solution_delivered_liters = round(
                state.water_delivered_liters * 0.05, 2
            )

            state.total_water_delivered_liters += (
                state.water_delivered_liters
            )

            return

        state.water_delivered_liters = 0.0

        state.nutrient_solution_delivered_liters = 0.0
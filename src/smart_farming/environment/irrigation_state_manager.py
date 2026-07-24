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
        random_manager: object | None = None,
    ) -> None:
        """
        Initialize runtime irrigation state.

        Args
        ----
        zone_count:
            Total number of growing zones in the simulator.
        random_manager:
            Optional shared random number provider for realistic hydraulic drift.
        """

        self._states: dict[str, IrrigationState] = {}
        self._zone_baselines: dict[str, dict[str, float | int]] = {}
        self._random_manager = random_manager
        self._simulation_cycle = 0

        self._initialize(zone_count)

    def _initialize(
        self,
        zone_count: int,
    ) -> None:
        """
        Create the initial irrigation state and hydraulic baselines for every growing zone.
        """

        self._states.clear()
        self._zone_baselines.clear()

        from smart_farming.config import PHILIPPINE_FACILITY_PROFILES

        for facility_id, fac_profile in PHILIPPINE_FACILITY_PROFILES.items():
            for idx, micro in enumerate(fac_profile.micro_locations, start=1):
                zone_id = micro.zone_id
                state_key = f"{facility_id}:{zone_id}"
                zone_num = int(zone_id.split("-")[1]) if "-" in zone_id else idx

                # Establish zone-specific hydraulic baseline profiles
                self._zone_baselines[state_key] = {
                    "active_flow": 2.20 + (zone_num % 5) * 0.40,        # 2.20 to 3.80 L/min
                    "active_pressure": 180.0 + (zone_num % 6) * 14.0,   # 180.0 to 250.0 kPa
                    "active_duration": 240 + (zone_num % 4) * 60,       # 240 to 420 seconds
                    "idle_flow": 0.35 + (zone_num % 4) * 0.12,          # 0.35 to 0.71 L/min
                    "idle_pressure": 40.0 + (zone_num % 5) * 5.0,       # 40.0 to 60.0 kPa
                    "idle_duration": 50 + (zone_num % 3) * 15,          # 50 to 80 seconds
                }

                self._states[state_key] = IrrigationState(
                    zone_id=zone_id,
                    facility_id=facility_id,
                    irrigation_active=False,
                    flow_rate_liters_per_minute=0.0,
                    pressure_kpa=0.0,
                    irrigation_duration_seconds=0,
                    water_delivered_liters=0.0,
                    nutrient_solution_delivered_liters=0.0,
                    last_irrigation_cycle=0,
                    next_irrigation_cycle=idx % 3,
                    irrigation_interval_cycles=(
                        DEFAULT_IRRIGATION_INTERVAL_CYCLES
                    ),
                    irrigation_end_cycle=0,
                )

    def _get_random_variance(self, min_val: float, max_val: float) -> float:
        if self._random_manager and hasattr(self._random_manager, "uniform"):
            return self._random_manager.uniform(min_val, max_val)
        import random
        return random.uniform(min_val, max_val)

    def get_zone_state(
        self,
        zone_id: str,
        facility_id: str | None = None,
    ) -> IrrigationState:
        """
        Retrieve the runtime irrigation state for a growing zone.
        """
        if facility_id:
            state_key = f"{facility_id}:{zone_id}"
            if state_key in self._states:
                return self._states[state_key]

        # Search for first state matching zone_id if facility_id is unmapped
        for state in self._states.values():
            if state.zone_id == zone_id:
                return state

        return list(self._states.values())[0]

    def get_all_states(
        self,
    ) -> list[IrrigationState]:
        """
        Return all managed irrigation runtime states.
        """

        return list(self._states.values())

    def advance_cycle(self) -> None:
        """
        Advance the irrigation controller by one simulation cycle.
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
        Update irrigation hydraulic operating conditions with continuous drift.
        """
        state_key = f"{state.facility_id}:{state.zone_id}"
        baseline = self._zone_baselines.get(state_key, {
            "active_flow": 2.50, "active_pressure": 220.0, "active_duration": 300,
            "idle_flow": 0.50, "idle_pressure": 50.0, "idle_duration": 60
        })

        if state.irrigation_active:
            flow_var = self._get_random_variance(-0.25, 0.25)
            press_var = self._get_random_variance(-10.0, 10.0)
            dur_var = int(self._get_random_variance(-25, 25))

            state.flow_rate_liters_per_minute = round(max(1.2, float(baseline["active_flow"]) + flow_var), 2)
            state.pressure_kpa = round(max(100.0, float(baseline["active_pressure"]) + press_var), 1)
            state.irrigation_duration_seconds = max(120, int(baseline["active_duration"]) + dur_var)
            return

        # Continuous NFT film trickle baseline with physical micro-variations
        flow_var = self._get_random_variance(-0.06, 0.06)
        press_var = self._get_random_variance(-3.5, 3.5)
        dur_var = int(self._get_random_variance(-8, 8))

        state.flow_rate_liters_per_minute = round(max(0.15, float(baseline["idle_flow"]) + flow_var), 2)
        state.pressure_kpa = round(max(25.0, float(baseline["idle_pressure"]) + press_var), 1)
        state.irrigation_duration_seconds = max(30, int(baseline["idle_duration"]) + dur_var)

    def _update_water_delivery(
        self,
        state: IrrigationState,
    ) -> None:
        """
        Calculate continuous hydrodynamic water and nutrient delivery.
        """
        # Delivered volume = flow_rate (L/min) * (duration / 60)
        delivered = round(
            state.flow_rate_liters_per_minute * (state.irrigation_duration_seconds / 60.0), 2
        )

        # Dynamic dosing concentration (4.5% to 7.0%)
        dosing_percent = 0.05 + (hash(f"{state.facility_id}:{state.zone_id}") % 5) * 0.005
        nutrient_delivered = round(delivered * dosing_percent, 2)

        state.water_delivered_liters = delivered
        state.nutrient_solution_delivered_liters = nutrient_delivered
        state.total_water_delivered_liters += delivered
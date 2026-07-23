"""
Runtime manager for maintenance work orders.

This module owns the mutable runtime state representing maintenance work
orders within the HydroGrow Smart Farming Simulator.

Unlike telemetry generators, this manager contains no event formatting or
serialization logic. It is responsible only for maintaining the
authoritative runtime state used by higher application layers.

Initial implementation intentionally creates an empty maintenance
workspace. Future roadmap milestones will introduce predictive
maintenance, work-order creation, technician assignment, and lifecycle
progression.
"""

from smart_farming.models import (
    MaintenanceState,
)


class MaintenanceStateManager:
    """
    Owns runtime maintenance work orders.

    The MaintenanceStateManager is the authoritative owner of all active
    maintenance work orders during simulation execution.

    Responsibilities
    ----------------
    - Store runtime maintenance state.
    - Provide lookup methods.
    - Provide future lifecycle update entry points.

    Event generation remains the responsibility of the
    MaintenanceEventGenerator.
    """

    def __init__(self) -> None:
        """
        Initialize the maintenance workspace with routine zone maintenance work orders.
        """

        self._states: dict[str, MaintenanceState] = {}
        self._simulation_cycle: int = 0

        # Seed 10 initial routine maintenance work orders (1 per zone)
        for index in range(1, 11):
            wo_id = f"WO-{index:05d}"
            zone = f"ZONE-{index:03d}"
            facility = "FAC-001"
            equip = f"EQ-{index:05d}"
            self._states[wo_id] = MaintenanceState(
                work_order_id=wo_id,
                facility_id=facility,
                zone_id=zone,
                equipment_id=equip,
                maintenance_type="PREVENTATIVE",
                priority="MEDIUM",
                assigned_technician=f"tech.zone-{index:03d}@smartfarm.ph",
                work_status="IN_PROGRESS" if index % 2 == 0 else "COMPLETED",
                estimated_duration_minutes=60,
                remaining_duration_minutes=30 if index % 2 == 0 else 0,
                completion_percent=50.0 if index % 2 == 0 else 100.0,
                maintenance_cycle=1,
                is_active=True,
            )

    def add_work_order(
        self,
        state: MaintenanceState,
    ) -> None:
        """
        Register a runtime maintenance work order.

        Parameters
        ----------
        state:
            Runtime maintenance work order.
        """

        self._states[state.work_order_id] = state

    def get_work_order(
        self,
        work_order_id: str,
    ) -> MaintenanceState:
        """
        Retrieve a maintenance work order.

        Args:
            work_order_id:
                Unique maintenance work order identifier.

        Returns:
            Mutable MaintenanceState instance.
        """

        return self._states[work_order_id]

    def get_all_states(
        self,
    ) -> list[MaintenanceState]:
        """
        Return every active maintenance work order.

        Returns:
            List of runtime maintenance states.
        """

        return list(self._states.values())

    def active_work_order_count(
        self,
    ) -> int:
        """
        Return the number of active maintenance work orders.

        Returns:
            Active work order count.
        """

        return len(self._states)

    @property
    def simulation_cycle(self) -> int:
        """
        Return the current simulation cycle.

        Returns:
            int: The current simulation cycle index.
        """
        return self._simulation_cycle

    def advance_cycle(self) -> None:
        """
        Advance the maintenance simulation cycle and progress work orders.
        """

        self._simulation_cycle += 1

        for state in self._states.values():
            if state.work_status == "IN_PROGRESS":
                state.remaining_duration_minutes = max(0, state.remaining_duration_minutes - 5)
                state.completion_percent = min(100.0, ((state.estimated_duration_minutes - state.remaining_duration_minutes) / state.estimated_duration_minutes) * 100.0)
                if state.remaining_duration_minutes == 0:
                    state.work_status = "COMPLETED"
            elif state.work_status == "COMPLETED" and self._simulation_cycle % 10 == 0:
                # Re-issue a routine inspection work order every 10 cycles
                state.work_status = "IN_PROGRESS"
                state.remaining_duration_minutes = state.estimated_duration_minutes
                state.completion_percent = 0.0
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

        # Authentic Filipino Maintenance Technicians Roster per Facility
        facility_technician_roster = {
            "FAC-001": [("Juan Dela Cruz", "Senior HVAC Tech"), ("Ana Cruz", "Hydroponics Specialist")],
            "FAC-002": [("Maria Santos", "Lead Systems Tech"), ("Mark Dizon", "Electrical Engr")],
            "FAC-003": [("Jose Reyes", "Automation Engr"), ("Rhea Santos", "Nutrient Specialist")],
            "FAC-004": [("Paolo Ramos", "Mechanical Tech"), ("Grace Villanueva", "Pump Specialist")],
            "FAC-005": [("Danilo Aquino", "Industrial Tech"), ("Luzviminda Garcia", "PLC Engr")],
            "FAC-006": [("Gabriel Mendoza", "Senior Microgrid Tech"), ("Corazon Reyes", "Lighting Specialist")],
            "FAC-007": [("Eduardo Tan", "HVAC / Thermal Specialist"), ("Teresa Mercado", "RO System Specialist")],
            "FAC-008": [("Rodrigo Castillo", "Sensors Tech"), ("Elena Bautista", "Nutrient Line Specialist")],
        }

        maintenance_types = ["PREVENTATIVE", "CORRECTIVE", "CALIBRATION", "EMERGENCY_REPAIR", "INSPECTION"]
        priorities = ["ROUTINE", "LOW", "MEDIUM", "HIGH", "CRITICAL"]
        statuses = ["IN_PROGRESS", "COMPLETED", "IN_PROGRESS", "COMPLETED", "SCHEDULED", "IN_PROGRESS"]

        wo_counter = 1
        # Seed 48 work orders across all 8 facilities (6 work orders per facility)
        for fac_num in range(1, 9):
            facility_id = f"FAC-{fac_num:03d}"
            tech_pairs = facility_technician_roster[facility_id]

            for item_idx in range(1, 7):
                wo_id = f"WO-{wo_counter:05d}"
                zone_id = f"ZONE-{((item_idx - 1) % 4) + 1:03d}"
                equip_id = f"EQ-{(fac_num - 1) * 10 + item_idx:05d}"
                
                tech_name, _ = tech_pairs[(item_idx - 1) % len(tech_pairs)]
                mtype = maintenance_types[(item_idx - 1) % len(maintenance_types)]
                prio = priorities[(item_idx - 1) % len(priorities)]
                status = statuses[(item_idx - 1) % len(statuses)]
                
                est_dur = 30 + ((item_idx * 25) % 150)
                if status == "COMPLETED":
                    rem_dur = 0
                    comp_pct = 100.0
                elif status == "SCHEDULED":
                    rem_dur = est_dur
                    comp_pct = 0.0
                else:
                    rem_dur = int(est_dur * (0.3 + (item_idx * 0.1)))
                    comp_pct = round(((est_dur - rem_dur) / est_dur) * 100.0, 1)

                self._states[wo_id] = MaintenanceState(
                    work_order_id=wo_id,
                    facility_id=facility_id,
                    zone_id=zone_id,
                    equipment_id=equip_id,
                    maintenance_type=mtype,
                    priority=prio,
                    assigned_technician=tech_name,
                    work_status=status,
                    estimated_duration_minutes=est_dur,
                    remaining_duration_minutes=rem_dur,
                    completion_percent=comp_pct,
                    maintenance_cycle=1,
                    is_active=(status != "COMPLETED"),
                )
                wo_counter += 1

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
        Advance the maintenance simulation cycle and progress work orders realistically.
        """

        self._simulation_cycle += 1

        for state in self._states.values():
            if state.work_status == "IN_PROGRESS":
                state.remaining_duration_minutes = max(0, state.remaining_duration_minutes - 5)
                state.completion_percent = round(
                    min(100.0, ((state.estimated_duration_minutes - state.remaining_duration_minutes) / state.estimated_duration_minutes) * 100.0),
                    1
                )
                if state.remaining_duration_minutes == 0:
                    state.work_status = "COMPLETED"
                    state.is_active = False
            elif state.work_status == "SCHEDULED" and self._simulation_cycle % 3 == 0:
                state.work_status = "IN_PROGRESS"
                state.is_active = True
            elif state.work_status == "COMPLETED" and self._simulation_cycle % 12 == 0:
                # Re-issue routine service work order periodically
                state.work_status = "IN_PROGRESS"
                state.remaining_duration_minutes = state.estimated_duration_minutes
                state.completion_percent = 0.0
                state.is_active = True
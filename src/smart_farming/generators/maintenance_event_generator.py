"""
Maintenance Event Generator.

This module produces MaintenanceEvent telemetry from the runtime
MaintenanceStateManager.

The generator is intentionally lightweight during the initial
implementation phase. Its responsibility is limited to converting runtime
maintenance state into immutable telemetry events.

Future roadmap milestones will introduce:

- predictive maintenance
- automatic work-order creation
- technician scheduling
- maintenance completion
- maintenance history
"""

from smart_farming.config import (
    Settings,
    EVENT_TYPE_MAINTENANCE,
)
from smart_farming.environment import MaintenanceStateManager
from smart_farming.models import MaintenanceEvent
from smart_farming.generators.base_telemetry_generator import BaseTelemetryGenerator
from smart_farming.utils import (
    utc_now,
    format_timestamp,
)


class MaintenanceEventGenerator(BaseTelemetryGenerator):
    """
    Generates MaintenanceEvent telemetry.

    This generator translates runtime MaintenanceState objects into
    immutable MaintenanceEvent instances.
    """

    EVENT_TYPE = EVENT_TYPE_MAINTENANCE

    def __init__(
        self,
        settings: Settings,
        maintenance_state_manager: MaintenanceStateManager,
    ) -> None:
        """
        Initialize the maintenance telemetry generator.

        Args:
            settings:
                Simulator configuration.

            maintenance_state_manager:
                Runtime maintenance state owner.
        """
        self._settings = settings
        self._maintenance_state_manager = (
            maintenance_state_manager
        )

    def generate(
        self,
    ) -> list[MaintenanceEvent]:
        """
        Generate maintenance telemetry.

        Returns:
            Maintenance telemetry events.
        """

        events: list[MaintenanceEvent] = []

        timestamp = format_timestamp(utc_now())
        simulation_cycle = self._maintenance_state_manager.simulation_cycle
        
        for state in (
            self._maintenance_state_manager.get_all_states()
        ):

            # Generate realistic technician notes and health restoration data based on status
            is_completed = (state.work_status == "COMPLETED" or not state.is_active)
            tech_notes = (
                f"Work order {state.work_order_id} ({state.maintenance_type}) completed by {state.assigned_technician}. Calibration verified."
                if is_completed else f"Maintenance in progress by {state.assigned_technician}. {state.remaining_duration_minutes}m remaining."
            )
            # Dynamic max health restoration potential based on maintenance type
            max_restoration_map = {
                "EMERGENCY_REPAIR": 35.0,
                "CORRECTIVE": 25.0,
                "PREVENTATIVE": 15.0,
                "CALIBRATION": 8.0,
                "INSPECTION": 5.0,
            }
            max_health_points = max_restoration_map.get(state.maintenance_type, 15.0)
            
            # Dynamic health restoration proportional to completion percent
            health_restored_val = round((state.completion_percent / 100.0) * max_health_points, 1)

            events.append(
                MaintenanceEvent(
                    event_type=self.EVENT_TYPE,
                    facility_id=state.facility_id,
                    zone_id=state.zone_id,
                    equipment_id=state.equipment_id,
                    work_order_id=state.work_order_id,
                    maintenance_cycle=state.maintenance_cycle,
                    maintenance_type=state.maintenance_type,
                    priority=state.priority,
                    assigned_technician=state.assigned_technician,
                    maintenance_status=state.work_status,
                    estimated_duration_minutes=state.estimated_duration_minutes,
                    remaining_duration_minutes=state.remaining_duration_minutes,
                    completion_percent=state.completion_percent,
                    is_active=state.is_active,
                    technician_notes=tech_notes,
                    health_restored=health_restored_val,
                    simulation_cycle=simulation_cycle,
                )
            )

        return events
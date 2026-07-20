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
from .base_telemetry_generator import BaseTelemetryGenerator


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

        super().__init__(settings)

        self._maintenance_state_manager = (
            maintenance_state_manager
        )

    def generate(
        self,
        simulation_cycle: int,
    ) -> list[MaintenanceEvent]:
        """
        Generate maintenance telemetry.

        Args:
            simulation_cycle:
                Current simulator cycle.

        Returns:
            Maintenance telemetry events.
        """

        events: list[MaintenanceEvent] = []

        timestamp = self._build_timestamp()

        for state in (
            self._maintenance_state_manager.get_all_states()
        ):

            events.append(
                MaintenanceEvent(
                    event_type=self.EVENT_TYPE,
                    simulation_cycle=simulation_cycle,
                    timestamp=timestamp,
                    facility_id=state.facility_id,
                    work_order_id=state.work_order_id,
                    equipment_id=state.equipment_id,
                    zone_id=state.zone_id,
                    maintenance_type=state.maintenance_type,
                    priority=state.priority,
                    assigned_technician=state.assigned_technician,
                    work_status=state.work_status,
                    estimated_duration_minutes=(
                        state.estimated_duration_minutes
                    ),
                    remaining_duration_minutes=(
                        state.remaining_duration_minutes
                    ),
                    completion_percent=(
                        state.completion_percent
                    ),
                    is_active=state.is_active,
                )
            )

        return events
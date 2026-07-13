"""
Equipment telemetry generator.

This module generates telemetry events representing the current
operational state of equipment assets registered within the simulator.

The generator is intentionally read-only. It combines immutable
equipment metadata with mutable runtime state to construct telemetry
events without modifying simulator state.

Runtime state transitions remain the responsibility of the
EquipmentStateManager.
"""
from smart_farming.config import (
    EVENT_TYPE_EQUIPMENT,
    FacilityId,
    Settings
)
from smart_farming.environment import (
    EnvironmentStateManager,
    EquipmentRegistry,
    EquipmentStateManager,
)
from smart_farming.models import (
    Equipment,
    EquipmentTelemetryEvent,
)
from smart_farming.utils import (
    TelemetryGenerationError,
)
from smart_farming.monitoring import (
    get_logger
)
from smart_farming.generators import (
    BaseTelemetryGenerator,
)


class EquipmentTelemetryGenerator(BaseTelemetryGenerator):
    """
    Generates telemetry events for equipment assets.

    Each generated event represents the current runtime state of one
    equipment asset installed within a HydroGrow smart farming
    facility.

    This generator is intentionally read-only. Runtime state mutations
    remain the responsibility of the EquipmentStateManager.
    """

    def __init__(
        self,
        settings: Settings,
        environment_manager: EnvironmentStateManager,
        equipment_registry: EquipmentRegistry,
        equipment_state_manager: EquipmentStateManager,
    ) -> None:
        """
        Initialize the telemetry generator.

        Args:
            settings:
                Validated application settings.

            registry:
                Registry containing equipment metadata.

            state_manager:
                Manager providing runtime state for equipment assets.
        """
        self.settings = settings
        self.environment_manager = environment_manager
        self.equipment_registry = equipment_registry
        self.equipment_state_manager = equipment_state_manager

        self.logger = get_logger(__name__)

        self.logger.info(
            "Equipment telemetry generator initialized."
        )

    def generate(self) -> list[EquipmentTelemetryEvent]:
        """
        Generate telemetry events for every registered equipment asset.

        Returns:
            Collection of generated equipment telemetry events.

        Raises:
            TelemetryGenerationError:
                Raised when telemetry generation fails.
        """
        environment = (
            self.environment_manager.get_current_state()
        )

        events: list[EquipmentTelemetryEvent] = []

        try:
            for equipment in self.equipment_registry.list_all():
                events.append(
                    self._create_equipment_event(
                        equipment=equipment,
                        timestamp=environment.timestamp,
                    )
                )
        except Exception as exc:
            raise TelemetryGenerationError(
                "Failed to generate equipment telemetry events."
            ) from exc

        self.logger.info(
            "Generated %d equipment telemetry events.",
            len(events),
        )

        return events

    def _create_equipment_event(
        self,
        equipment: Equipment,
        timestamp,
    ) -> EquipmentTelemetryEvent:
        """
        Create a telemetry event for a single equipment asset.

        Args:
            equipment:
                Equipment metadata.

            timestamp:
                Shared simulation timestamp.

        Returns:
            Fully populated equipment telemetry event.
        """

        state = self.equipment_state_manager.get(
            equipment.equipment_id
        )

        event = EquipmentTelemetryEvent(
            event_type=EVENT_TYPE_EQUIPMENT,
            facility_id=equipment.facility_id,
            equipment_id=equipment.equipment_id,
            zone_id=equipment.zone_id,
            equipment_type=equipment.equipment_type,
            operating_status=state.operating_status,
            health=state.health,
            runtime_hours=state.runtime_hours,
            current_load=state.current_load,
            failure_probability=state.failure_probability,
        )

        event.timestamp = timestamp

        return event
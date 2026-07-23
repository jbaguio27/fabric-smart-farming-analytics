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
    RandomManager
)
from smart_farming.monitoring import (
    get_logger
)
from smart_farming.generators.base_telemetry_generator import (
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
        Initialize the equipment telemetry generator.

        Args:
            settings:
                Validated application settings.

            random_manager:
                Shared simulator random number generator.

            equipment_registry:
                Registry containing persistent equipment metadata.

            equipment_state_manager:
                Manager containing mutable runtime state.
        """
        self.settings = settings
        self.environment_manager = environment_manager

        self.equipment_registry = equipment_registry
        self.equipment_state_manager = equipment_state_manager

        self.logger = get_logger(__name__)

        self.logger.info(
            "Equipment telemetry generator initialized."
        )

    def _validate_generation_prerequisites(
        self,
    ) -> None:
        """
        Validate the equipment telemetry generation prerequisites.

        Equipment telemetry generation requires both the equipment registry
        and runtime state manager to be fully initialized and synchronized.
        This validation prevents silent generation failures caused by
        incomplete simulator initialization.

        Raises:
            TelemetryGenerationError:
                If the equipment registry is empty or runtime state is not
                synchronized with the registered equipment assets.
        """

        equipment = self.equipment_registry.list_all()

        if not equipment:
            raise TelemetryGenerationError(
                "Equipment registry contains no registered assets."
            )

        runtime_states = (
            self.equipment_state_manager.list_all()
        )

        if not runtime_states:
            raise TelemetryGenerationError(
                "Equipment runtime state manager is not initialized."
            )

        if len(equipment) != len(runtime_states):
            raise TelemetryGenerationError(
                "Equipment registry and runtime state manager are out of sync."
            )

        if self.environment_manager.get_current_state() is None:
            raise TelemetryGenerationError(
                "Environment state manager has not been initialized."
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

        self._validate_generation_prerequisites()
        
        environment = (
            self.environment_manager.get_current_state()
        )

        events: list[EquipmentTelemetryEvent] = []

        try:
            import random
            sample_rate = getattr(self.settings, "equipment_telemetry_sample_rate", 1.0)
            equipment_list = self.equipment_registry.list_all()
            
            if sample_rate < 1.0:
                k = max(1, int(len(equipment_list) * sample_rate))
                equipment_list = random.sample(equipment_list, k=k)

            for equipment in equipment_list:
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
            "Generated %d equipment telemetry events (Sample Rate: %.2f).",
            len(events),
            sample_rate,
        )

        return events

    def _create_equipment_event(
        self,
        equipment: Equipment,
        timestamp,
    ) -> EquipmentTelemetryEvent:
        """
        Create a telemetry event for a single equipment asset.

        Combines immutable equipment metadata with the equipment's
        current runtime state, including the baseline sensor metrics
        (power consumption, temperature, and vibration) maintained by
        EquipmentStateManager.update_sensor_metrics(). Sensor metrics
        are read directly off runtime state rather than recalculated
        here, preserving the generator's read-only contract.

        Args:
            equipment:
                Equipment metadata.

            timestamp:
                Shared simulation timestamp.

        Returns:
            Fully populated equipment telemetry event, including
            baseline sensor telemetry.
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
            power_consumption_kw=state.power_consumption_kw,
            operating_temperature_c=state.temperature_celsius,
            vibration_vps=state.vibration_mm_s,
            manufacturer=getattr(equipment, "manufacturer", ""),
            model_number=getattr(equipment, "model_number", ""),
        )

        event.timestamp = timestamp

        return event
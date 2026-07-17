"""
Crop Lifecycle Generator.

This module converts the mutable runtime state maintained by the
CropStateManager into immutable Crop Lifecycle events.

The generator serves as the boundary between simulation state and event
production. It contains no lifecycle simulation logic. All biological
progression remains the responsibility of CropStateManager.

During this initial implementation phase, the generator exposes the
structure required for future event generation while intentionally
producing no events. This minimizes regression risk and allows the
generator to be integrated incrementally.
"""
import uuid
from datetime import datetime, UTC
from smart_farming.config import Settings
from smart_farming.environment import (
    CropRegistry,
    CropStateManager,
    GrowingEnvironmentStateManager,
)
from smart_farming.models import (
    CropState,
    CropLifecycleEvent,
)
from .base_telemetry_generator import BaseTelemetryGenerator
from smart_farming.utils import RandomManager


class CropLifecycleGenerator(BaseTelemetryGenerator):
    """
    Generates Crop Batch Lifecycle events.

    The generator consumes immutable crop definitions from the
    CropRegistry and mutable runtime state from the CropStateManager.
    Environmental context is supplied by the EnvironmentStateManager.

    No event generation logic is implemented during this step.
    """

    def __init__(
        self,
        settings: Settings,
        random_manager: RandomManager,
        environment_manager: GrowingEnvironmentStateManager,
        crop_registry: CropRegistry,
        crop_state_manager: CropStateManager,
    ) -> None:
        """
        Initialize the crop lifecycle generator.

        Args:
            settings:
                Simulator configuration.

            random_manager:
                Shared random number provider.

            growing_enviroment_manager:
                Manager supplying the current environmental conditions for each
                growing zone.

            crop_registr:
                Registry containing immutable crop definitions.

            crop_state_manager:
                Manager supplying the authoritative runtime crop state.
        """

        self._settings = settings
        self._random_manager = random_manager
        self._environment_manager = environment_manager
        self._crop_registry = crop_registry
        self._crop_state_manager = crop_state_manager

    def generate(
        self,
    ) -> list[CropLifecycleEvent]:
        """
        Generate immutable crop lifecycle telemetry events.

        Returns
        -------
        list[CropLifecycleEvent]
            One event for every active crop.
        """

        events: list[CropLifecycleEvent] = []

        for crop_state in self._crop_state_manager.get_all_states():

            if not crop_state.is_active:
                continue

            events.append(
                self._build_event(crop_state)
            )

        return events

    def _build_event(
        self,
        crop_state: CropState
    ) -> CropLifecycleEvent:
        """
        Build an immutable CropLifecycleEvent.

        This helper converts mutable runtime state into an immutable event
        suitable for downstream telemetry pipelines.

        Args
        ----
        crop_state:
            Runtime crop state.

        Returns
        -------
        CropLifecycleEvent
            Immutable lifecycle telemetry event.
        """
        environment = self._environment_manager.get_zone_state(
            crop_state.zone_id,
        )

        definition = self._crop_registry.get(
            crop_state.crop_batch_id
        )

        return CropLifecycleEvent(
            crop_batch_id=definition.crop_batch_id,
            facility_id=definition.facility_id,
            zone_id=definition.zone_id,
            crop_type=definition.crop_type,

            lifecycle_stage=crop_state.lifecycle_stage,
            age_days=crop_state.age_days,
            health_score=crop_state.health_score,
            is_active=crop_state.is_active,

            air_temperature_celsius=environment.air_temperature_celsius,
            humidity_percent=environment.humidity_percent,
            water_ph=environment.water_ph,
            electrical_conductivity=environment.electrical_conductivity,

            event_timestamp=datetime.now(UTC),
            simulation_cycle=self._crop_state_manager.simulation_cycle,
            event_type="CropLifecycleEvent",
            event_id=str(uuid.uuid4())
        )
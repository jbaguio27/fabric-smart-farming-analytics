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
from datetime import datetime
from smart_farming.config import Settings
from smart_farming.environment import (
    CropRegistry,
    CropStateManager,
)
from smart_farming.models import (
    CropState,
    CropLifecycleEvent,
    GrowingEnvironmentState,
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
        growing_environment_manager: GrowingEnvironmentState,
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
        self._growing_environment_manager = growing_environment_manager
        self._crop_registry = crop_registry
        self._crop_state_manager = crop_state_manager

    def generate(
        self,
    ) -> list[CropLifecycleEvent]:
        """
        Generate immutable crop lifecycle telemetry events.

        One CropLifecycleEvent is emitted for every active crop batch.
        The generator combines runtime crop state with the current
        growing environment state while remaining completely free of
        simulation logic.

        Returns
        -------
        list[CropLifecycleEvent]
            Immutable telemetry events representing the current
            simulation state.
        """

        events: list[CropLifecycleEvent] = []

        for crop_state in self._crop_state_manager.states.values():

            if not crop_state.is_active:
                continue

            environment = (
                self._growing_environment_manager.get_zone_state(
                    crop_state.zone_id,
                )
            )

            events.append(
                CropLifecycleEvent(
                    event_timestamp=datetime.utcnow(),
                    crop_batch_id=crop_state.crop_batch_id,
                    zone_id=crop_state.zone_id,
                    crop_type=crop_state.crop_type,
                    lifecycle_stage=crop_state.lifecycle_stage,
                    age_days=crop_state.age_days,
                    health_score=crop_state.health_score,
                    is_active=crop_state.is_active,
                    air_temperature_celsius=environment.air_temperature_celsius,
                    humidity_percent=environment.humidity_percent,
                    water_ph=environment.water_ph,
                    electrical_conductivity=environment.electrical_conductivity
                )
            )

        return events

    def _build_event_payload(
        self,
        event: CropLifecycleEvent
    ) -> dict[str, object]:
        """
        Convert an immutable CropLifecycleEvent into a serializable
        payload.

        Serialization remains separate from event generation so future
        telemetry sinks can reuse the same immutable event model.

        Args
        ----
        event:
            Immutable crop lifecycle event.

        Returns
        -------
        dict[str, object]
            Serializable event payload.
        """

        return {
            "event_timestamp": event.event_timestamp.isoformat(),
            "crop_batch_id": event.crop_batch_id,
            "zone_id": event.zone_id,
            "crop_type": event.crop_type,
            "lifecycle_stage": event.lifecycle_stage,
            "age_days": event.age_days,
            "health_score": event.health_score,
            "is_active": event.is_active,
            "air_temperature_celsius": event.air_temperature_celsius,
            "humidity_percent": event.humidity_percent,
            "water_ph": event.water_ph,
            "electrical_conductivity": event.electrical_conductivity,
        }
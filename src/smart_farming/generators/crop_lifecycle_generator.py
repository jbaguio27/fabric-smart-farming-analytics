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
from smart_farming.config import Settings
from smart_farming.environment import (
    CropRegistry,
    CropStateManager,
)
from smart_farming.models import (
    CropState,
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

    def generate(self) -> list:
        """
        Generate crop lifecycle events.

        Returns:
            An empty list during this implementation phase.

        Notes:
            Future roadmap phases will construct one Crop Lifecycle Event
            per active crop batch.
        """

        events: list = []

        for crop_state in self._crop_state_manager.states.values():

            if not crop_state.is_active:
                continue

            _ = crop_state

        return events

    def _build_event_payload(
        self,
        crop_state: CropState,
    ) -> dict[str, object]:
        """
        Build the payload for a Crop Batch Lifecycle event.

        This helper translates the mutable CropState into a structure
        aligned with the documented Crop Batch Lifecycle Event contract.
        Event object construction and serialization remain the
        responsibility of later implementation steps.

        Args:
            crop_state:
                Runtime state of the crop batch.

        Returns:
            Dictionary representing the event payload.
        """

        return {
            "crop_batch_id": crop_state.crop_batch_id,
            "zone_id": crop_state.zone_id,
            "crop_type": crop_state.crop_type,
            "lifecycle_stage": crop_state.lifecycle_stage,
            "age_days": crop_state.age_days,
            "health_score": crop_state.health_score,
            "is_active": crop_state.is_active,
        }
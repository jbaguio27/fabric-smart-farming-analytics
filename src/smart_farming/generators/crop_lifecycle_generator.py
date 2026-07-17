"""
Crop lifecycle telemetry generator.

Generates Crop Batch Lifecycle events for the HydroGrow Smart Farming
Simulator.

This initial implementation establishes the generator's dependency
structure only. Event generation logic will be introduced in subsequent
roadmap steps once the crop runtime model has been finalized.
"""

from smart_farming.config import Settings
from smart_farming.environment import (
    CropRegistry,
    CropStateManager,
    EnvironmentStateManager,
)
from .base_telemetry_generator import BaseTelemetryGenerator
from smart_farming.utils import RandomManager
from smart_farming.models import CropState

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
        environment_manager: EnvironmentStateManager,
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

            environment_manager:
                Shared environmental state.

            crop_registry:
                Registry containing immutable crop definitions.

            crop_state_manager:
                Manager containing mutable crop runtime state.
        """

        self._settings = settings
        self._random_manager = random_manager
        self._environment_manager = environment_manager
        self._crop_registry = crop_registry
        self._crop_state_manager = crop_state_manager

    def generate(self) -> list:
        """
        Generate crop lifecycle telemetry events.

        This initial implementation establishes the generator execution
        flow by iterating over all managed crop runtime states.

        Event construction will be introduced in a subsequent roadmap
        step. For now, the method returns an empty collection while
        exercising the runtime architecture.

        Returns:
            Empty list of lifecycle events.
        """

        events: list = []

        for crop_state in (
            self._crop_state_manager.states().values()
        ):
            # Placeholder for future event generation. 

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
            "field_id": crop_state.field_id,
            "crop_type": crop_state.crop_type,
            "lifecycle_stage": crop_state.lifecycle_stage,
            "age_days": crop_state.age_days,
            "health_score": crop_state.health_score,
            "is_active": crop_state.is_active,
        }
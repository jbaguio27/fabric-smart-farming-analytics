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
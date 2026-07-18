"""
Crop Telemetry Generator.

This module converts the mutable runtime crop state maintained by the
CropStateManager into immutable Crop Telemetry events.

Unlike the CropLifecycleGenerator, which publishes business lifecycle
information, this generator emits continuous biological telemetry suitable
for real-time monitoring dashboards and analytics.

The generator performs no crop simulation. It simply transforms runtime
state into immutable telemetry events.
"""

from smart_farming.config import Settings
from smart_farming.environment import (
    CropRegistry,
    CropStateManager,
    GrowingEnvironmentStateManager,
)
from smart_farming.generators import BaseTelemetryGenerator
from smart_farming.utils import RandomManager


class CropTelemetryGenerator(BaseTelemetryGenerator):
    """
    Generates continuous crop telemetry events.

    The generator consumes runtime crop state together with the current
    growing environment.

    Biological simulation remains entirely owned by CropStateManager.
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
        Initialize the crop telemetry generator.

        Args:
            settings:
                Simulator configuration.

            random_manager:
                Shared random provider.

            environment_manager:
                Runtime growing environment manager.

            crop_registry:
                Immutable crop definitions.

            crop_state_manager:
                Runtime crop state manager.
        """

        self._settings = settings
        self._random_manager = random_manager
        self._environment_manager = environment_manager
        self._crop_registry = crop_registry
        self._crop_state_manager = crop_state_manager

    def generate(
        self,
    ) -> list:
        """
        Generate crop telemetry events.

        Returns
        -------
        list
            No telemetry events are generated during this implementation
            step.
        """

        return []
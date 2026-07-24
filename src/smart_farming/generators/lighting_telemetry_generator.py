"""
Lighting telemetry generator.

This module converts runtime lighting state into normalized lighting
telemetry events.

The generator owns no simulation logic. It simply translates the current
runtime state maintained by LightingStateManager into immutable telemetry
events suitable for downstream streaming platforms.
"""

from datetime import UTC, datetime
from uuid import uuid4

from smart_farming.config import Settings
from smart_farming.environment import LightingStateManager
from smart_farming.generators import BaseTelemetryGenerator
from smart_farming.models import LightingTelemetryEvent


class LightingTelemetryGenerator(BaseTelemetryGenerator):
    """
    Generates lighting telemetry events.

    One telemetry event is produced for every managed growing zone during
    each simulation cycle.
    """

    EVENT_TYPE = "lighting"

    def __init__(
        self,
        settings: Settings,
        lighting_state_manager: LightingStateManager,
    ) -> None:
        """
        Initialize the lighting telemetry generator.

        Args:
            settings:
                Simulator configuration.

            lighting_state_manager:
                Runtime lighting state manager.
        """

        self._settings = settings
        self._lighting_state_manager = (
            lighting_state_manager
        )

    def generate(
        self,
    ) -> list[LightingTelemetryEvent]:
        """
        Generate lighting telemetry events.

        Returns:
            Normalized lighting telemetry events.
        """

        return [
            self._build_event(state)
            for state in (
                self._lighting_state_manager.get_all_states()
            )
        ]

    def _build_event(
        self,
        state,
    ) -> LightingTelemetryEvent:
        """
        Convert runtime lighting state into a telemetry event.

        Args:
            state:
                Runtime lighting state.

        Returns:
            Lighting telemetry event.
        """

        return LightingTelemetryEvent(
            event_type=self.EVENT_TYPE,
            facility_id=state.facility_id,
            zone_id=state.zone_id,
            lighting_enabled=state.lights_enabled,
            lighting_intensity_percent=state.light_intensity_percent,
            photoperiod_hours=state.photoperiod_hours,
            daily_light_integral=state.daily_light_integral,
        )
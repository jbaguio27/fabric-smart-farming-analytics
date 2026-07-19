"""
Irrigation telemetry generator.

This module transforms mutable IrrigationState runtime objects into
immutable IrrigationTelemetryEvent records suitable for downstream
telemetry pipelines.

The generator does not own simulation logic. Its responsibility is
limited to reading runtime state and constructing telemetry events.
"""

from uuid import uuid4

from smart_farming.generators import BaseTelemetryGenerator
from smart_farming.models import IrrigationTelemetryEvent
from smart_farming.environment import (
    IrrigationStateManager,
    EnvironmentStateManager,
)
from smart_farming.config import Settings


class IrrigationTelemetryGenerator(
    BaseTelemetryGenerator,
):
    """
    Generates irrigation telemetry events.
    """

    EVENT_TYPE = "irrigation.telemetry"

    def __init__(
        self,
        settings: Settings,
        environment_manager: EnvironmentStateManager,
        irrigation_state_manager: IrrigationStateManager,
    ) -> None:
        """
        Initialize the irrigation telemetry generator.

        Args:
            settings:
                Simulator configuration.

            environment_manager:
                Provides the current simulation timestamp.

            irrigation_state_manager:
                Provides runtime irrigation state.
        """

        super().__init__(settings)

        self._environment_manager = (
            environment_manager
        )

        self._irrigation_state_manager = (
            irrigation_state_manager
        )

    def generate(
        self,
    ) -> list[IrrigationTelemetryEvent]:
        """
        Generate irrigation telemetry events.

        Returns:
            One telemetry event per growing zone.
        """

        timestamp = (
            self._environment_manager
            .get_current_state()
            .timestamp
        )

        events: list[
            IrrigationTelemetryEvent
        ] = []

        for state in (
            self._irrigation_state_manager
            .get_all_states()
        ):

            events.append(

                IrrigationTelemetryEvent(

                    event_id=str(
                        uuid4()
                    ),

                    event_type=self.EVENT_TYPE,

                    event_timestamp=timestamp,

                    facility_id=self.settings.facility_id,

                    zone_id=state.zone_id,

                    irrigation_active=(
                        state.irrigation_active
                    ),

                    flow_rate_liters_per_minute=(
                        state.flow_rate_liters_per_minute
                    ),

                    pressure_kpa=(
                        state.pressure_kpa
                    ),

                    irrigation_duration_seconds=(
                        state.irrigation_duration_seconds
                    ),

                    water_delivered_liters=(
                        state.water_delivered_liters
                    ),

                    nutrient_solution_delivered_liters=(
                        state.nutrient_solution_delivered_liters
                    ),
                )
            )

        return events
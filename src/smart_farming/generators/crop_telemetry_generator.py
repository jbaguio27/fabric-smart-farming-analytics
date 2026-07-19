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
from datetime import datetime, UTC
from smart_farming.config import Settings
from smart_farming.environment import (
    CropRegistry,
    CropStateManager,
    GrowingEnvironmentStateManager,
)
from smart_farming.generators import BaseTelemetryGenerator
from smart_farming.utils import RandomManager
from smart_farming.models import (
    CropState,
    CropTelemetryEvent,
)


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

        One immutable telemetry event is produced for every active crop.

        Returns
        -------
        list[CropTelemetryEvent]
            Continuous crop telemetry.
        """

        events: list[CropTelemetryEvent] = []

        for crop_state in self._crop_state_manager.get_all_states():

            if not crop_state.is_active:
                continue

            events.append(
                self._build_event(
                    crop_state,
                )
            )

        return events

    def _build_event(
        self,
        crop_state: CropState,
    ) -> CropTelemetryEvent:
        """
        Convert mutable runtime state into an immutable telemetry event.

        Parameters
        ----------
        crop_state:
            Runtime crop state.

        Returns
        -------
        CropTelemetryEvent
            Immutable telemetry snapshot.
        """

        definition = self._crop_registry.get(
            crop_state.crop_batch_id,
        )

        environment = (
            self._environment_manager.get_zone_state(
                crop_state.zone_id,
            )
        )

        return CropTelemetryEvent(
            event_timestamp=datetime.now(UTC),
            simulation_cycle=(
                self._crop_state_manager.simulation_cycle
            ),
            crop_batch_id=definition.crop_batch_id,
            facility_id=definition.facility_id,
            zone_id=definition.zone_id,
            crop_type=definition.crop_type,
            lifecycle_stage=crop_state.lifecycle_stage,
            age_days=crop_state.age_days,
            health_score=crop_state.health_score,
            growth_rate=crop_state.growth_rate,
            biomass_grams=crop_state.biomass_grams,
            water_uptake_liters=crop_state.water_uptake_liters,
            nutrient_uptake_grams=crop_state.nutrient_uptake_grams,
            stress_index=crop_state.stress_index,
            air_temperature_celsius=(
                environment.air_temperature_celsius
            ),
            humidity_percent=(
                environment.humidity_percent
            ),
            water_ph=environment.water_ph,
            electrical_conductivity=(
                environment.electrical_conductivity
            ),
        )
"""
Application entry point for the HydroGrow Smart Farming Simulator.
"""
from smart_farming.utils import RandomManager
from smart_farming.config import Settings
from smart_farming.monitoring import (
    configure_logging,
    get_logger,
    log_application_start,
    log_application_shutdown,
    log_unhandled_exception,
)
from smart_farming.producer import (
    EventDispatcher,
    Simulator,
)
from smart_farming.services import (
    WearModel,
    FailureModel,
    MaintenanceManager,
    FacilityDemandModel,
)
from smart_farming.utils import (
    SmartFarmingError,
)
from smart_farming.generators import (
    BaseTelemetryGenerator,
    EnvironmentalTelemetryGenerator,
    EquipmentTelemetryGenerator,
    CropLifecycleGenerator,
    CropTelemetryGenerator,
    IrrigationTelemetryGenerator,
    LightingTelemetryGenerator,
    MaintenanceEventGenerator,
)
from smart_farming.environment import (
    EnvironmentStateManager,
    EquipmentRegistry,
    EquipmentStateManager,
    GrowingEnvironmentStateManager,
    CropRegistry,
    CropStateManager,
    IrrigationStateManager,
    LightingStateManager,
    MaintenanceStateManager,
)


def main() -> None:
    """
    Bootstrap and start the HydroGrow Smart Farming Simulator.

    The application initializes shared infrastructure, creates the
    simulation managers, registers all telemetry generators, and starts
    the simulator.

    This function acts as the application's composition root, where
    dependencies are assembled before execution begins.
    """

    logger = get_logger(__name__)

    try:
        settings = Settings.from_env()

        configure_logging(settings)

        log_application_start(logger, settings)

        dispatcher = EventDispatcher()

        random_manager = RandomManager(
            seed=settings.random_seed,
        )

        environment_manager = EnvironmentStateManager(
            settings=settings,
            random_manager=random_manager,
        )

        equipment_registry = EquipmentRegistry()

        wear_model = WearModel()
        failure_model = FailureModel()
        maintenance_manager = MaintenanceManager()
        facility_demand_model = FacilityDemandModel()

        equipment_state_manager = EquipmentStateManager(
            equipment_registry=equipment_registry,
            random_manager=random_manager,
            wear_model=wear_model,
            failure_model=failure_model,
            maintenance_manager=maintenance_manager,
            facility_demand_model=facility_demand_model,
        )

        crop_registry = CropRegistry()

        growing_enviroment_manager = (
            GrowingEnvironmentStateManager(
                settings=settings,
                random_manager=random_manager,
                zone_count=settings.zone_count,
            )
        )

        irrigation_state_manager = (
            IrrigationStateManager(
                zone_count=settings.zone_count,
            )
        )

        lighting_state_manager = (
            LightingStateManager(
                settings=settings,
                zone_count=settings.zone_count,
            )
        )

        crop_state_manager = CropStateManager(
            settings=settings,
            random_manager=random_manager,
            crop_registry=crop_registry,
            growing_environment_manager=growing_enviroment_manager,
            irrigation_state_manager=irrigation_state_manager,
        )

        maintenance_state_manager = MaintenanceStateManager()

        environmental_generator = (
            EnvironmentalTelemetryGenerator(
                settings=settings,
                random_manager=random_manager,
                environment_manager=environment_manager,
            )
        )

        equipment_generator = (
            EquipmentTelemetryGenerator(
                settings=settings,
                environment_manager=environment_manager,
                equipment_registry=equipment_registry,
                equipment_state_manager=equipment_state_manager
            )
        )

        crop_lifecycle_generator = (
            CropLifecycleGenerator(
                settings=settings,
                random_manager=random_manager,
                environment_manager=growing_enviroment_manager,
                crop_registry=crop_registry,
                crop_state_manager=crop_state_manager,
            )
        )

        crop_telemetry_generator = (
            CropTelemetryGenerator(
                settings=settings,
                random_manager=random_manager,
                environment_manager=growing_enviroment_manager,
                crop_registry=crop_registry,
                crop_state_manager=crop_state_manager,
            )
        )

        irrigation_generator = (
            IrrigationTelemetryGenerator(
                settings=settings,
                environment_manager=environment_manager,
                irrigation_state_manager=irrigation_state_manager,
            )
        )

        lighting_generator = (
            LightingTelemetryGenerator(
                settings=settings,
                lighting_state_manager=lighting_state_manager,
            )
        )

        maintenance_generator = (
            MaintenanceEventGenerator(
                settings=settings,
                maintenance_state_manager=maintenance_state_manager,
            )
        )

        generators: list[
            BaseTelemetryGenerator
        ] = [
            environmental_generator,
            equipment_generator,
            crop_lifecycle_generator,
            crop_telemetry_generator,
            irrigation_generator,
            lighting_generator,
            maintenance_generator,
        ]

        simulator = Simulator(
            settings=settings,
            dispatcher=dispatcher,
            generators=generators,
            environment_manager=environment_manager,
            equipment_state_manager=equipment_state_manager,
            crop_state_manager=crop_state_manager,
            growing_environment_manager=growing_enviroment_manager,
            irrigation_state_manager=irrigation_state_manager,
            lighting_state_manager=lighting_state_manager,
            maintenance_state_manager=maintenance_state_manager,
        )

        simulator.run()

        log_application_shutdown(logger)

    except SmartFarmingError as exc:
        log_unhandled_exception(
            logger,
            f"Application failed: {exc}",
        )
        raise

    except Exception:
        log_unhandled_exception(
            logger,
            "An unexpected application error occurred."
        )
        raise

if __name__ == "__main__":
    main()
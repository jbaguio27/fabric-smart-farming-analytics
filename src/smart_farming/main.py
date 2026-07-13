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
from smart_farming.utils import (
    SmartFarmingError,
)
from smart_farming.generators import (
    BaseTelemetryGenerator,
    EnvironmentalTelemetryGenerator,
    EquipmentTelemetryGenerator,
)
from smart_farming.environment import (
    EnvironmentStateManager,
    EquipmentRegistry,
    EquipmentStateManager
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

        equipment_state_manager = EquipmentStateManager(
            equipment_registry=equipment_registry,
            random_manager=random_manager,
        )

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

        generators: list[
            BaseTelemetryGenerator
        ] = [
            environmental_generator,
            equipment_generator,
        ]

        simulator = Simulator(
            settings=settings,
            dispatcher=dispatcher,
            generators=generators,
            environment_manager=environment_manager,
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
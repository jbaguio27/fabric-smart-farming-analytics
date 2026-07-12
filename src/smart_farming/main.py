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
    EnvironmentalTelemetryGenerator,
)
from smart_farming.environment import (
    EnvironmentStateManager,
)


def main() -> None:
    """
    Bootstrap and start the Smart Farming Simulator.
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

        generator = EnvironmentalTelemetryGenerator(
            settings=settings,
            random_manager=random_manager,
            environment_manager=environment_manager
        )

        simulator = Simulator(
            settings=settings,
            dispatcher=dispatcher,
            generator=generator,
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
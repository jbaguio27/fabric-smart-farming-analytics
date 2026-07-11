"""
Application entry point for the HydroGrow Smart Farming Simulator.
"""

from smart_farming.config.settings import Settings
from smart_farming.monitoring.logger import (
    configure_logging,
    get_logger,
    log_application_start,
    log_application_shutdown,
    log_unhandled_exception,
)
from smart_farming.producer.event_dispatcher import EventDispatcher
from smart_farming.producer.simulator import Simulator
from smart_farming.utils.exceptions import SmartFarmingError
from smart_farming.generators import EnvironmentalTelemetryGenerator

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

        generator = EnvironmentalTelemetryGenerator(
            settings=settings,
        )

        simulator = Simulator(
            settings=settings,
            dispatcher=dispatcher,
            generator=generator,
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
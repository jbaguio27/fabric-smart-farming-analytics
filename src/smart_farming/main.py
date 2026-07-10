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

def main() -> None:
    """
    Bootstrap and start the Smart Farming Simulator.
    """

    configure_logging(settings)
    logger = get_logger(__name__)

    try:
        settings = Settings.from_env()

        log_application_start(logger, settings)

        dispatcher = EventDispatcher()

        simulator = Simulator(
            settings=settings,
            dispatcher=dispatcher,
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
            "An unexpected application error occured."
        )
        raise

if __name__ == "__main__":
    main()
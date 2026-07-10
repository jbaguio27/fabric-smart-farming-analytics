"""
Application entry point for the HydroGrow Smart Farming Simulator.
"""

from smart_farming.config.settings import Settings
from smart_farming.monitoring.logger import (
    configure_logging,
    get_logger,
)
from smart_farming.producer.event_dispatcher import EventDispatcher
from smart_farming.producer.simulator import Simulator
from smart_farming.utils.exceptions import SmartFarmingError

def main() -> None:
    """
    Bootstrap and start the Smart Farming Simulator.
    """

    configure_logging()
    logger = get_logger(__name__)

    try:
        settings = Settings.from_env()

        logger.info('Starting HydroGrow Smart Farming Simulator')
        logger.info(
            "Environment: %s | Log Level: %s",
            settings.environment,
            settings.log_level
        )
        logger.info(
            "Facilities: %d | Interval: %ds | Batch Size: %d",
            settings.total_facilities,
            settings.simulation_interval_seconds,
            settings.event_batch_size
        )

        dispatcher = EventDispatcher()

        simulator = Simulator(
            settings=settings,
            dispatcher=dispatcher,
        )

        simulator.run()

        logger.info('Simulator execution completed.')

    except SmartFarmingError:
        logger.exception(
            'Application terminated due to a simulator error.'
        )
        raise

    except Exception:
        logger.exception(
            'An unexpected application error occured.'
        )
        raise

if __name__ == "__main__":
    main()
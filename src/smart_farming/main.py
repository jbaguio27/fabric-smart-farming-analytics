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
        logger.info('Starting HydroGrow Smart Farming Simulator')

        settings = Settings()
        dispatcher = EventDispatcher()

        simulator = Simulator(
            settings=settings,
            dispatcher=dispatcher,
        )

        simulator.run()

        logger.info('Simulator execution completed.')

    except SmartFarmingError:
        logger.exception('Application terminated due to a simulator error.')
        raise

    except Exception:
        logger.exception('An unexpected application error occured.')
        raise

if __name__ == "__main__":
    main()
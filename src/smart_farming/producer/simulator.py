"""
Core simulator for the HydroGrow Smart Farming Simulator.
"""

from smart_farming.config.settings import Settings
from smart_farming.monitoring.logger import get_logger
from smart_farming.producer.event_dispatcher import EventDispatcher

logger = get_logger(__name__)

class Simulator:
    """
    Coordinates the execution of the Smart Farming Simulator.
    """

    def __init__(
        self,
        settings: Settings,
        dispatcher: EventDispatcher,
    ) -> None:
        self._settings = settings
        self._dispatcher = dispatcher

        logger.info('Simulator Initialized')

    def run(self) -> None:
        """
        Start the simulator.

        Generator registration and execution will be implemented in
        future milestones.
        """

        logger.info(
            "Starting simulator in '%s' environment.",
            self._settings.environment
        )

        logger.info('Simulator is ready to register generators.')
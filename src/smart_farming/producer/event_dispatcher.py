"""
Event dispatcher for the HydroGrow Smart Farming Simulator.
"""
import logging
from smart_farming.models.base_event import BaseEvent
from smart_farming.monitoring.logger import get_logger
from smart_farming.utils.exceptions import DispatchError


class EventDispatcher:
    """
    Dispatch simulator events to the configured destination.
    """

    def __init__(self) -> None:
        self.logger: logging.Logger = get_logger(__name__)

    def dispatch(
        self,
        events: list[BaseEvent],
    ) -> None:
        """
        Dispatch an event.

        Args:
            events: Events produced during a simulation cycle.

        Raises:
            DispatchError: If dispatching fails.
        """

        self.logger.info(
            "Dispatching batch of %d events.",
            len(events),
        )

        # Placeholder for future Evenstream integration.

        # Future implementation:
        # - Serialize event
        # - Send to Eventstream
        # - Retry Failures
        # - Record metrics

        self.logger.info(
            "Successfully dispatched %d events.",
            len(events)
        )
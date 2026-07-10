"""
Event dispatcher for the HydroGrow Smart Farming Simulator.
"""

from smart_farming.monitoring.logger import get_logger
from smart_farming.utils.exceptions import DispatchError

logger = get_logger(__name__)

class EventDispatcher:
    """
    Dispatch simulator events to the configured destination.

    During Project Setup, events are only logged. Future implementations
    will support Microsoft Fabric Eventstream.
    """

    def dispatch(self, event: object) -> None:
        """
        Dispatch an event.

        Args:
            event: Event instance to dispatch.

        Raises:
            DispatchError: If dispatching fails.
        """

        try:
            logger.info(
                "Dispatching %s event.",
                event.__class__.__name__,
            )

            # Future implementation:
            # - Serialize event
            # - Send to Eventstream
            # - Retry Failures
            # - Record metrics
        except Exception as exc:
            logger.exception('Failed to dispatch event.')

            raise DispatchError(
                'Failed to dispatch event.'
            ) from exc
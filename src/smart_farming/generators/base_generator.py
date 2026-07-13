"""
Base telemetry generator interface for the HydroGrow Smart Farming Simulator.

This module defines the common interface implemented by every telemetry
generator. A telemetry generator is responsible for producing one or
more events during a single simulation cycle.

Using a shared interface keeps the Simulator independent of concrete
generator implementations and allows new telemetry generators to be
introduced without modifying the simulator orchestration logic.
"""

from abc import ABC, abstractmethod
from smart_farming.models import BaseEvent

class BaseTelemetryGenerator(ABC):
    """
    Abstract base class for telemetry generators.

    Concrete implementations generate one or more telemetry events for
    each simulation cycle.
    """

    @abstractmethod
    def generate(
        self,
    ) -> list[BaseEvent]:
        """
        Generate telemetry events for the current simulation cycle.

        Returns:
            Collection of generated telemetry events.
        """

        raise NotImplementedError
"""
Facility Telemetry Generator.
This module provides the telemetry generator responsible for creating
FacilityEvent instances for all registered vertical farming facilities.
"""

from .base_telemetry_generator import BaseTelemetryGenerator
from smart_farming.environment import FacilityStateManager
from smart_farming.models import (
    FacilityEvent,
    BaseEvent,
)

class FacilityGenerator(BaseTelemetryGenerator):
    """
    Generator that produces operational telemetry snapshots for vertical farm facilities.
    """

    def __init__(
        self,
        facility_state_manager: FacilityStateManager,
    ) -> None:
        """
        Initialize the FacilityGenerator.
        Args:
            facility_state_manager: Shared FacilityStateManager instance.
        """

        self._facility_state_manager = facility_state_manager

    def generate(self) -> list[BaseEvent]:
        """
        Generate FacilityEvent snapshots for all registered facilities.

        Returns:
            List of BaseEvent (FacilityEvent) instances.
        """

        events: list[BaseEvent] = []
        for facility_id in self._facility_state_manager.list_facility_ids():
            facility_event = self._facility_state_manager.generate_facility_event(facility_id)
            events.append(facility_event)
        return events
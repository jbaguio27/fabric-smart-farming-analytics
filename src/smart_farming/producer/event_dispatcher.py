"""
Event dispatcher for the HydroGrow Smart Farming Simulator.
"""

from requests.utils import requote_uri
from requests.adapters import BaseAdapter
import logging
from dataclasses import is_dataclass, asdict
from datetime import datetime
from uuid import UUID
import requests

from smart_farming.config import Settings
from smart_farming.models import BaseEvent
from smart_farming.monitoring import get_logger
from smart_farming.utils import (
    DispatchError,
    EventSerializationError,
    format_timestamp,
)
from .anomaly_injector import DataAnomalyInjector


class EventDispatcher:
    """
    Dispatch simulator events to the configured destination (e.g., Microsoft Fabric Eventstream).
    """

    def __init__(
        self,
        settings: Settings | None = None,
    ) -> None:
        """
        Initialize the event dispatcher.

        Args:
            settings:
                Optional application settings containing endpoint configuration.
        """
        self.settings: Settings | None = settings
        self.logger: logging.Logger = get_logger(__name__)
        self.anomaly_injector = DataAnomalyInjector(
            anomaly_rate=0.05 if settings is not None else 0.0,
        )

    def dispatch(
        self,
        events: list[BaseEvent],
    ) -> None:

        if not events:
            self.logger.debug("No events to dispatch.")
            return

        self.logger.info(
            "Dispatching batch of %d events.",
            len(events),
        )

        serialized_events: list[dict[str, object]] = []

        for event in events:
            payloads = self._serialize_event(event)
            serialized_events.extend(payloads)

        endpoint = (
            self.settings.eventstream_endpoint
            if self.settings and hasattr(self.settings, "eventstream_endpoint")
            else ""
        )

        if endpoint:
            self._send_to_eventstream(endpoint, serialized_events)
        else:
            self.logger.info(
                "No Eventstream endpoint configured. Mock dispatched %d events locally.",
                len(events),
            )

        self.logger.info(
            "Successfully dispatched %d events.",
            len(events),
        )

    def _serialize_event(
        self,
        event: BaseEvent | object,
    ) -> dict[str, object]:
        """
        Serialize an event object into a JSON-compatible dictionary.

        Args:
            event:
                Event object to serialize.

        Returns:
            Dictionary payload ready for JSON encoding.

        Raises:
            EventSerializationError:
                If serialization fails.
        """
        try:
            if hasattr(event, "to_dict") and callable(getattr(event, "to_dict")):
                raw_dict = event.to_dict()
            elif is_dataclass(event):
                raw_dict = asdict(event)
            elif isinstance(event, dict):
                raw_dict = event
            else:
                raw_dict = getattr(event, "__dict__", {})

            normalized = self._normalize_payload(raw_dict)

            if isinstance(normalized, dict):
                return self.anomaly_injector.inject_anomalies(normalized)

            return [normalized] if isinstance(normalized, dict) else []

        except Exception as exc:
            raise EventSerializationError(
                f"Failed to serialize event '{event}': {exc}"
            ) from exc

    def _normalize_payload(
        self,
        data: object,
    ) -> object:
        """
        Recursively normalize complex types (datetime, UUID, Enum) for JSON encoding.

        Args:
            data:
                Data element to normalize.

        Returns:
            JSON-compatible data representation.
        """
        if isinstance(data, datetime):
            return format_timestamp(data)
        if isinstance(data, UUID):
            return str(data)
        if hasattr(data, "value"):
            return data.value
        if isinstance(data, dict):
            return {
                k: self._normalize_payload(v)
                for k, v in data.items()
            }
        if isinstance(data, list):
            return [self._normalize_payload(item) for item in data]

        return data

    def _send_to_eventstream(
        self,
        endpoint: str,
        payloads: list[dict[str, object]],
    ) -> None:
        """
        Send serialized events to Microsoft Fabric Eventstream over HTTP POST.

        Args:
            endpoint:
                Eventstream custom endpoint URL.

            payloads:
                List of serialized event payloads.

        Raises:
            DispatchError:
                If the HTTP POST request encounters an exception or non-2xx response.
        """
        headers = {"Content-Type": "application/json"}

        try:
            response = requests.post(
                endpoint,
                json=payloads,
                headers=headers,
                timeout=10,
            )
            response.raise_for_status()

            self.logger.debug(
                "HTTP POST to Eventstream status %d",
                response.status_code,
            )
        except requests.RequestException as exc:
            raise DispatchError(
                f"Failed to send {len(payloads)} events to Eventstream endpoint '{endpoint}': {exc}"
            ) from exc

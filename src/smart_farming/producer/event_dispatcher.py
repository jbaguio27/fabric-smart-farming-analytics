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


UNIFIED_EVENT_SCHEMA_KEYS: list[str] = [
    "event_id",
    "event_type",
    "facility_id",
    "zone_id",
    "equipment_id",
    "equipment_type",
    "operating_status",
    "health",
    "current_load",
    "failure_probability",
    "runtime_hours",
    "vibration_vps",
    "operating_temperature_c",
    "power_consumption_kw",
    "sensor_type",
    "sensor_value",
    "unit",
    "sensor_status",
    "weather",
    "is_daytime",
    "crop_batch_id",
    "crop_type",
    "lifecycle_stage",
    "age_days",
    "health_score",
    "growth_rate",
    "biomass_grams",
    "harvest_cycle_days",
    "target_biomass_g",
    "water_consumption_liters",
    "nutrient_consumption_grams",
    "environmental_stress_index",
    "ambient_temperature_celsius",
    "ambient_humidity_percent",
    "irrigation_active",
    "flow_rate_liters_per_minute",
    "pressure_kpa",
    "irrigation_duration_seconds",
    "water_delivered_liters",
    "nutrient_solution_delivered_liters",
    "lighting_enabled",
    "lighting_intensity_percent",
    "photoperiod_hours",
    "daily_light_integral",
    "work_order_id",
    "priority",
    "assigned_technician",
    "maintenance_type",
    "maintenance_status",
    "estimated_duration_minutes",
    "remaining_duration_minutes",
    "completion_percent",
    "technician_notes",
    "health_restored",
    "overall_health",
    "active_critical_alerts",
    "power_draw_kw",
    "water_circulation_lph",
    "facility_name",
    "region",
    "city",
    "latitude",
    "longitude",
    "elevation_m",
    "climate_zone",
    "water_source",
    "power_grid_redundancy",
    "max_zone_capacity",
    "manufacturer",
    "model_number",
    "operator_contact",
    "operator_phone",
    "timestamp",
    "schema_version",
]


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
                # Pad payload with master schema keys so all stream columns are always present
                unified_payload = {key: normalized.get(key, None) for key in UNIFIED_EVENT_SCHEMA_KEYS}
                for k, v in normalized.items():
                    unified_payload[k] = v

                return self.anomaly_injector.inject_anomalies(unified_payload)

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
        import time
        import urllib.parse
        import hmac
        import hashlib
        import base64

        headers = {"Content-Type": "application/json"}

        # Check if the configured endpoint is a Connection String instead of a raw URL
        if endpoint.startswith("Endpoint=sb://"):
            try:
                parts = dict(x.split("=", 1) for x in endpoint.split(";") if "=" in x)
                sb_endpoint = parts["Endpoint"]
                key_name = parts["SharedAccessKeyName"]
                key = parts["SharedAccessKey"]
                entity_path = parts["EntityPath"]

                # Extract host domain (e.g. esehsgl63ww6tcoggbvlhg.servicebus.windows.net)
                host = sb_endpoint.replace("sb://", "").replace("/", "")
                
                # Build the standard HTTP POST REST URL
                target_url = f"https://{host}/{entity_path}/messages"
                
                # Sign the Event Hub Resource URI
                resource_uri = f"https://{host}/{entity_path}"
                expiry = int(time.time() + 3600)
                string_to_sign = urllib.parse.quote_plus(resource_uri) + '\n' + str(expiry)
                
                sig = base64.b64encode(
                    hmac.new(
                        key.encode("utf-8"),
                        string_to_sign.encode("utf-8"),
                        hashlib.sha256
                    ).digest()
                ).decode("utf-8")
                
                sas_token = (
                    f"SharedAccessSignature sr={urllib.parse.quote_plus(resource_uri)}"
                    f"&sig={urllib.parse.quote_plus(sig)}&se={expiry}&skn={key_name}"
                )
                
                headers["Authorization"] = sas_token
                endpoint = target_url
                self.logger.info("Automatically generated SAS Token and configured HTTP headers for Eventstream authentication.")
            except Exception as e:
                raise DispatchError(f"Failed to parse Event Hub connection string from settings: {e}")

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

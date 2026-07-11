"""
Environmental telemetry generator for the HydroGrow Smart Farming Simulator.

This generator is responsible for producing environmental sensor
telemetry events for indoor farming facilities.
"""

import random
from smart_farming.monitoring.logger import get_logger
from smart_farming.config.constants import (
    SensorMetadata,
    FacilityId,
    ENVIRONMENTAL_SENSOR_CONFIG, 
    EVENT_TYPE_ENVIRONMENTAL,
    SENSOR_STATUS_HEALTHY,
    SENSOR_STATUS_WARNING,
    SENSOR_STATUS_FAILED,
    SENSOR_HEALTHY_PROBABILITY,
    SENSOR_WARNING_PROBABILITY,
    SENSOR_FAILED_PROBABILITY,
    WARNING_SENSOR_OFFSET_PERCENTAGE,
    FACILITY_ID_PREFIX,
)
from smart_farming.config.settings import Settings
from smart_farming.models.environmental_event import(
    EnvironmentalTelemetryEvent,
)


class EnvironmentalTelemetryGenerator:
    """
    Generate environmental telemetry for HydroGrow facilities.
    """

    def __init__(
        self,
        settings: Settings,
    ) -> None:
        """
        Initialize the environmental telemetry generator.

        Args:
            settings: Validated application settings.
        """

        self.settings = settings
        self.logger = get_logger(__name__)
        self.random_generator = random.Random(
            settings.random_seed
        )

        self.logger.info(
            "Environmental telemetry generator initialized."
        )

    def generate(
        self,
    ) -> list[EnvironmentalTelemetryEvent]:
        """
        Generate environmental telemetry events for all configured facilities.

        Returns:
            Collection of environmental telemetry events.
        """

        facility_ids = self._generate_facility_ids()

        events: list[EnvironmentalTelemetryEvent] = []

        for facility_id in facility_ids:
            facility_events = self._generate_facility_events(
                facility_id=facility_id
            )

            events.extend(facility_events)
        
        self.logger.info(
            "Generated %d environmental telemetry events across %d facilities.",
            len(events),
            len(facility_ids)
        )

        return events

    def generate_sensor_value(
        self,
        sensor_type: str,
        sensor_status: str,
    ) -> float | None:
        """
        Generate a realistic value for an environmental sensor based on its status.

        The generated value is constrained by the configured minimum and maximum limits
        defined in the environmental sensor configuration. The returned value is rounded
        using the sensor's configured precision.

        Args:
            sensor_type: Supported environmental sensor type.
            sensor_status: The operational status of the sensor (healthy, warning, failed).
        
        Returns:
            Randomly generated sensor reading, or None if failed.
        
        Raises:
            ValidationError: If the sensor type is unsupported or status is unknown.
        """

        if not self.is_supported_sensor(sensor_type):
            raise ValidationError(
                f"Unsupported environmental sensor: '{sensor_type}'."
            )

        sensor_metadata = self.get_sensor_metadata(sensor_type)
        
        if sensor_status == SENSOR_STATUS_HEALTHY:
            return self._generate_healthy_value(sensor_metadata)
        elif sensor_status == SENSOR_STATUS_WARNING:
            return self._generate_warning_value(sensor_metadata)
        elif sensor_status == SENSOR_STATUS_FAILED:
            return self._generate_failed_value(sensor_metadata)

        raise ValidationError(
            f"Unknown sensor status: '{sensor_status}'."
        )

    def get_supported_sensors(self) -> tuple[str, ...]:
        """
        Return all supported environmental sensor types.

        Returns:
            Tuple containing all supported sensor types.
        """

        return tuple(ENVIRONMENTAL_SENSOR_CONFIG.keys())

    def get_sensor_metadata(
        self,
        sensor_type: str,
    ) -> SensorMetadata:
        """
        Return metadata for an environmental sensor.

        Args:
            sensor_type: Environmental sensor type.

        Returns:
            Metadata describing the sensor.

        Raises:
            KeyError: If the sensor type is unsupported.
        """

        return ENVIRONMENTAL_SENSOR_CONFIG[sensor_type]

    def is_supported_sensor(
        self,
        sensor_type: str,
    ) -> bool:
        """
        Determine whether a sensor type is supported.

        Args:
            sensor_type: Sensor type.

        Returns:
            True if supported, otherwise False.
        """

        return sensor_type in ENVIRONMENTAL_SENSOR_CONFIG

    def _create_environmental_event(
        self,
        facility_id: FacilityId,
        sensor_type: str,
    ) -> EnvironmentalTelemetryEvent:
        """
        Create an environmental telemetry event for a single sensor.

        Args:
            facility_id: Facility producing the telemetry.
            sensor_type: Environmental sensor type.

        Returns:
            A populated environmental telemetry event.
        """

        metadata = self.get_sensor_metadata(sensor_type)

        sensor_status = self._determine_sensor_status()

        sensor_value = self.generate_sensor_value(
            sensor_type=sensor_type,
            sensor_status=sensor_status,
        )

        return EnvironmentalTelemetryEvent(
            event_type=EVENT_TYPE_ENVIRONMENTAL,
            facility_id=facility_id,
            sensor_type=sensor_type,
            sensor_value=sensor_value,
            unit=metadata['unit'],
            sensor_status=sensor_status,
        )
    
    def _generate_facility_events(
        self,
        facility_id: FacilityId,
    ) -> list[EnvironmentalTelemetryEvent]:
        """
        Generate environmental telemetry events for a single facility.

        One event is produced for each supported environmental sensor.

        Args:
            facility_id: Facility identifier.

        Returns:
            Environmental telemetry events for the facility.
        """

        events: list[EnvironmentalTelemetryEvent] = []

        for sensor_type in self.get_supported_sensors():
            events.append(
                self._create_environmental_event(
                    facility_id=facility_id,
                    sensor_type=sensor_type,
                )
            )
        
        return events

    def _generate_facility_ids(self) -> list[FacilityId]:
        """
        Generate the configured facility identifiers.

        Facility IDs are sequentially numbered using the format.
        FAC-001, FAC-002, ..., FAC-XXX.

        Returns:
            List of configured facility identifiers.
        """

        return [
            f"{FACILITY_ID_PREFIX}-{facility_number:03d}"
            for facility_number in range(
                1,
                self.settings.total_facilities + 1,
            )
        ]

    def _generate_healthy_value(
        self,
        metadata: SensorMetadata,
    ) -> float:
        """
        Generate a sensor reading within the configured operating range.

        Args:
            metadata: Environmental sensor configuration.

        Returns:
            Simulated healthy sensor value.
        """
        value = self.random_generator.uniform(
            metadata['min_value'],
            metadata['max_value'],
        )

        return round(value, metadata['precision'])

    def _generate_warning_value(
        self,
        metadata: SensorMetadata,
    ) -> float:
        """
        Generate a sensor reading within the configured operating range.

        Args:
            metadata: Environmental sensor configuration.

        Returns:
            Simulated warning sensor value.
        """
        minimum = metadata['min_value']
        maximum = metadata['max_value']
        precision = metadata['precision']

        operating_range = maximum - minimum
        warning_offset = operating_range * WARNING_SENSOR_OFFSET_PERCENTAGE

        generate_below_range = self.random_generator.choice(
            [True, False]
        )

        if generate_below_range:
            value = self.random_generator.uniform(
                minimum - warning_offset,
                minimum,
            )
        else:
            value = self.random_generator.uniform(
                maximum,
                maximum + warning_offset,
            )
        
        return round(value, precision)

    def _generate_failed_value(
        self,
        metadata: SensorMetadata,
    ) -> float | None:
        """
        Generate a sensor reading within the configured operating range.

        Args:
            metadata: Environmental sensor configuration.

        Returns:
            Simulated failed sensor value.
        """

        return None

    def _determine_sensor_status(self) -> str:
        """
        Randomly determine the health status of an environmental sensor.

        The returned status is selected according to the configured sensor
        health probabilities.

        Returns:
            Simulated sensor health status.
        """

        random_value = self.random_generator.random()

        if random_value < SENSOR_HEALTHY_PROBABILITY:
            return SENSOR_STATUS_HEALTHY

        if (
            random_value
            < SENSOR_HEALTHY_PROBABILITY
            + SENSOR_WARNING_PROBABILITY
        ):
            return SENSOR_STATUS_WARNING

        return SENSOR_STATUS_FAILED
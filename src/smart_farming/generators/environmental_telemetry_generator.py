"""
Environmental telemetry generator for the HydroGrow Smart Farming Simulator.

This generator is responsible for producing environmental sensor
telemetry events for indoor farming facilities.
"""

from smart_farming.utils import (
    RandomManager,
    ValidationError,
)
from smart_farming.environment import EnvironmentStateManager
from smart_farming.monitoring import (
    get_logger,
)
from smart_farming.config import (
    Settings,
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
    FACILITY_ID_PREFIX,
    DAYTIME_SENSOR_ADJUSTMENTS,
    NIGHTTIME_SENSOR_ADJUSTMENTS,
    WEATHER_SENSOR_ADJUSTMENTS,
    SENSOR_TYPE_AIR_TEMPERATURE,
    SENSOR_TYPE_HUMIDITY,
    SENSOR_TYPE_LIGHT_INTENSITY,
    SENSOR_TYPE_CO2,
    SENSOR_TYPE_DISSOLVED_OXYGEN,
)
from smart_farming.models import (
    EnvironmentalTelemetryEvent,
    WeatherState,
)
from smart_farming.generators.base_telemetry_generator import (
    BaseTelemetryGenerator,
)


class EnvironmentalTelemetryGenerator(BaseTelemetryGenerator):
    """
    Generates environmental telemetry for all smart farming facilities.

    This generator simulates realistic environmental sensor readings
    using the current environmental state, sensor health, facility
    characteristics, and historical sensor values.
    """

    def __init__(
        self,
        settings: Settings,
        random_manager: RandomManager,
        environment_manager: EnvironmentStateManager,
    ) -> None:
        """
        Initialize the environmental telemetry generator.

        Args:
            settings: 
                Validated application settings.
            random_manager:
                Shared random number generator.
            environment_manager:
                Provides the current environmental conditions.
        """

        self.settings = settings
        self.random_manager = random_manager
        self.environment_manager = environment_manager
        self.logger = get_logger(__name__)
        self.sensor_state: dict[
            FacilityId,
            dict[str, float | None],
        ] = {}
        
        self.facility_profiles: dict[
            FacilityId,
            dict[str, float],
        ] = self._generate_facility_profiles()

        self.logger.info(
            "Environmental telemetry generator initialized."
        )

    def generate(
        self,
    ) -> list[EnvironmentalTelemetryEvent]:
        """
        Generate environmental telemetry events for all configured facilities.

        One event is generated for every supported environmental sensor
        within each facility using the current shared environmental state.

        Returns:
            Collection of generated environmental telemetry events.
        """
        environment = (
            self.environment_manager.get_current_state()
        )

        facility_ids = self._generate_facility_ids()

        events: list[EnvironmentalTelemetryEvent] = []

        for facility_id in facility_ids:
            facility_events = self._generate_facility_events(
                facility_id=facility_id,
                environment=environment,
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
        facility_id: FacilityId,
        sensor_type: str,
        sensor_status: str,
    ) -> float | None:
        """
        Generate a sensor reading based on its operational status.

        Healthy sensors remain within their operating range, warning
        sensors gradually drift beyond acceptable limits, and failed
        sensors either stop reporting or become stuck.

        Args:
            facility_id:
                Facility producing the telemetry.

            sensor_type:
                Environmental sensor type.

            sensor_status:
                Current simulated sensor health.

        Returns:
            Generated sensor value or None for failed sensors.
        """

        if not self.is_supported_sensor(sensor_type):
            raise ValidationError(
                f"Unsupported environmental sensor: '{sensor_type}'."
            )

        sensor_metadata = self.get_sensor_metadata(sensor_type)

        previous_value = self._get_sensor_state(
            facility_id=facility_id,
            sensor_type=sensor_type
        )
        
        if sensor_status == SENSOR_STATUS_HEALTHY:
            return self._generate_healthy_value(
                metadata=sensor_metadata,
                previous_value=previous_value,
            )
        elif sensor_status == SENSOR_STATUS_WARNING:
            return self._generate_warning_value(
                metadata=sensor_metadata,
                previous_value=previous_value,
            )
        elif sensor_status == SENSOR_STATUS_FAILED:
            return self._generate_failed_value(
                metadata=sensor_metadata,
                previous_value=previous_value,
            )

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
        environment: WeatherState,
    ) -> EnvironmentalTelemetryEvent:
        """
        Create a fully populated environmental telemetry event.

        The generated event incorporates sensor health, environmental
        conditions, facility-specific adjustments, and the shared
        simulation timestamp.

        Args:
            facility_id: 
                Facility producing the telemetry.
            sensor_type: 
                Environmental sensor type.
            environment:
                Current simulated environmental state.

        Returns:
            A populated environmental telemetry event.
        """

        metadata = self.get_sensor_metadata(sensor_type)

        sensor_status = self._determine_sensor_status()

        sensor_value = self.generate_sensor_value(
            facility_id=facility_id,
            sensor_type=sensor_type,
            sensor_status=sensor_status,
        )

        sensor_value = self._apply_day_night_adjustment(
            sensor_type=sensor_type,
            sensor_value=sensor_value,
            is_daytime=environment.is_daytime,
        )

        sensor_value = self._apply_weather_adjustment(
            sensor_type=sensor_type,
            sensor_value=sensor_value,
            environment=environment,
            facility_id=facility_id,
        )

        sensor_value = self._apply_facility_adjustment(
            sensor_type=sensor_type,
            facility_id=facility_id,
            sensor_value=sensor_value,
        )

        self._update_sensor_state(
            facility_id=facility_id,
            sensor_type=sensor_type,
            sensor_value=sensor_value,
        )

        event = EnvironmentalTelemetryEvent(
            event_type=EVENT_TYPE_ENVIRONMENTAL,
            facility_id=facility_id,
            sensor_type=sensor_type,
            sensor_value=sensor_value,
            unit=metadata['unit'],
            sensor_status=sensor_status,
            weather=environment.weather,
            is_daytime=environment.is_daytime,
        )

        event.timestamp = environment.timestamp

        return event
    
    def _generate_facility_events(
        self,
        facility_id: FacilityId,
        environment: WeatherState,
    ) -> list[EnvironmentalTelemetryEvent]:
        """
        Generate environmental telemetry events for a single facility.

        One event is generated for each supported environmental sensor
        using the current shared environmental conditions.

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
                    environment=environment,
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

    def _get_sensor_state(
        self,
        facility_id: FacilityId,
        sensor_type: str
    ) -> float | None:
        """
        Return the previous reading for a sensor.

        The previous value is used to produce continuous telemetry
        instead of completely random sensor readings.

        Args:
            facility_id: Facility identifier.
            sensor_type: Environmental sensor type.

        Returns:
            Current sensor value or None if this is the first reading.
        """

        return self.sensor_state.get(
            (facility_id, sensor_type)
        )

    def _update_sensor_state(
        self,
        facility_id: FacilityId,
        sensor_type: str,
        sensor_value: float | None,
    ) -> None:
        """
        Persist the latest successful sensor reading.

        Failed sensor values are intentionally ignored to preserve
        the last valid measurement for future telemetry generation.

        Args:
            facility_id: Facility identifier.
            sensor_type: Environmental sensor type.
            sensor_value: Newly generated value.
        """

        if sensor_value is None:
            return

        self.sensor_state[
            (facility_id, sensor_type)
        ] = sensor_value

    def _generate_healthy_value(
        self,
        metadata: SensorMetadata,
        previous_value: float | None,
    ) -> float:
        """
        Generate a healthy sensor reading.

        Healthy readings remain within the configured operating range
        while drifting gradually from the previous measurement.

        Args:
            metadata: Environmental sensor configuration.
            previous_value: Previous sensor reading used to generate
            realistic continuous telemetry. None if this is the
            first reading.

        Returns:
            Simulated healthy sensor value.
        """

        minimum = metadata['min_value']
        maximum = metadata['max_value']
        precision = metadata['precision']
        
        healthy_drift = metadata[
            "healthy_drift_percentage"
        ]

        operating_range = maximum - minimum

        if previous_value is None:
            value = self.random_manager.uniform(
                minimum,
                maximum,
            )
        else:
            drift = self.random_manager.uniform(
                -operating_range * healthy_drift,
                operating_range * healthy_drift,
            )

            value = previous_value + drift
        
        value = max(
            minimum,
            min(
                value,
                maximum,
            ),
        )

        return round(value, precision)

    def _generate_warning_value(
        self,
        metadata: SensorMetadata,
        previous_value: float | None,
    ) -> float:
        """
        Generate a warning sensor reading that gradually drifts
        outside the healthy operating range.

        Warning values remain close to the acceptable range to simulate
        sensors that are beginning to drift but have not yet completely
        failed.

        Args:
            metadata: Environmental sensor configuration.
            previous_value: Previous sensor reading used to generate
            realistic continuous telemetry. None if this is the
            first reading.

        Returns:
            Simulated warning sensor value.
        """
        minimum = metadata['min_value']
        maximum = metadata['max_value']
        precision = metadata['precision']

        healthy_drift = metadata[
            "healthy_drift_percentage"
        ]

        maximum_deviation = metadata[
            "warning_max_deviation_percentage"
        ]

        operating_range = maximum - minimum
        
        if previous_value is None:
            previous_value = self.random_manager.uniform(
                minimum,
                maximum,
            )

        direction = (
            -1
            if previous_value < (minimum + maximum) / 2
            else 1
        )

        drift = self.random_manager.uniform(
            operating_range * healthy_drift,
            operating_range * (
                maximum_deviation * 0.5
            ),
        )

        value = previous_value + (
            direction * drift
        )

        allowed_deviation = (
            operating_range * maximum_deviation
        )

        lower_limit = minimum - allowed_deviation
        upper_limit = maximum + allowed_deviation

        value = max(
            lower_limit,
            min(
                value,
                upper_limit,
            ),
        )

        return round(value, precision)

    def _generate_failed_value(
        self,
        metadata: SensorMetadata,
        previous_value: float | None
    ) -> float | None:
        """
        Generate a failed sensor reading.

        Failed sensors either stop transmitting data or repeatedly
        report their previous measurement to simulate common sensor
        failure scenarios.

        Args:
            metadata: Environmental sensor configuration.
            previous_value: Previous sensor reading used to generate
            realistic continuous telemetry. None if this is the
            first reading.

        Returns:
            None if the sensor stops reporting, otherwise the last
            recorded value.
        """
        if previous_value is None:
            return None

        if self.random_manager.random() < 0.7:
            return None

        return round(
            previous_value,
            metadata["precision"]
        )

    def _apply_day_night_adjustment(
        self,
        sensor_type: str,
        sensor_value: float | None,
        is_daytime: bool,
    ) -> float | None:
        """
        Apply the configured day or night influence to a sensor reading.

        The adjustment simulates predictable environmental changes
        caused by daylight and nighttime operating conditions.

        Args:
            sensor_type:
                Environmental sensor type.
            sensor_value:
                Generated sensor reading.
            is_daytime:
                Indicates whether the current simulation time
                occurs during daytime.
        
        Returns:
            Adjusted sensor value.
        """

        if sensor_value is None:
            return None

        metadata = self.get_sensor_metadata(sensor_type)

        if is_daytime:
            adjustment = DAYTIME_SENSOR_ADJUSTMENTS.get(
                sensor_type,
                0.0,
            )
        else:
            adjustment = NIGHTTIME_SENSOR_ADJUSTMENTS.get(
                sensor_type,
                0.0,
            )

        return round(
            sensor_value + adjustment,
            metadata["precision"],
        )

    def _apply_weather_adjustment(
        self,
        sensor_type: str,
        sensor_value: float | None,
        environment: WeatherState,
        facility_id: FacilityId,
    ) -> float | None:
        """
        Apply the current weather influence to a sensor reading based on continuous physical variables.
        Each sensor responds dynamically to continuous temperature, humidity, solar radiation,
        and precipitation levels.
        Args:
            sensor_type: Environmental sensor type.
            sensor_value: Current sensor reading.
            environment: Current simulated weather state.
            facility_id: Target facility identifier.
        Returns:
            Weather-adjusted sensor value.
        """
        if sensor_value is None:
            return None
        
        metadata = self.get_sensor_metadata(sensor_type)
        sensitivity = metadata['weather_sensitivity']
        precision = metadata['precision']
        adjustment = 0.0
        if sensor_type == SENSOR_TYPE_AIR_TEMPERATURE:
            # Ambient air temp is perturbed by external temp and solar thermal roof gain
            temp_delta = environment.ambient_temperature_celsius - 24.0
            solar_gain = environment.solar_irradiance_w_m2 / 1000.0
            adjustment = (temp_delta * 0.45 + solar_gain * 1.8) * sensitivity
        elif sensor_type == SENSOR_TYPE_HUMIDITY:
            # Internal humidity drifts slightly with external ambient humidity levels
            humidity_delta = environment.ambient_humidity_percent - 65.0
            adjustment = (humidity_delta * 0.25) * sensitivity
        elif sensor_type == SENSOR_TYPE_LIGHT_INTENSITY:
            # Ambient daylight adds natural light component
            adjustment = (environment.solar_irradiance_w_m2 * 25.0) * sensitivity
        elif sensor_type == SENSOR_TYPE_CO2:
            # High rainfall limits CO2 concentration slightly due to pressure differences
            adjustment = (-environment.rainfall_mm_hr * 1.2) * sensitivity
        elif sensor_type == SENSOR_TYPE_DISSOLVED_OXYGEN:
            # Dissolved oxygen solubility decreases as ambient temperature increases (gas solubility law)
            current_temp = self._get_sensor_state(
                facility_id=facility_id,
                sensor_type=SENSOR_TYPE_AIR_TEMPERATURE,
            )
            if current_temp is None:
                current_temp = 24.0
            temp_delta = current_temp - 24.0
            adjustment = (-temp_delta * 0.15) * sensitivity
        value = sensor_value + adjustment
        # Clamp to safety limits
        value = max(metadata['min_value'], min(value, metadata['max_value']))

        return round(value, precision)

    def _apply_facility_adjustment(
        self,
        sensor_type: str,
        facility_id: FacilityId,
        sensor_value: float | None,
    ) -> float | None:
        """
        Apply a permanent facility-specific adjustment.

        Each facility receives a small deterministic offset that
        creates realistic operational differences between otherwise
        identical facilities.

        Args:
            sensor_type:
                Environmental sensor type.
            facility_id:
                Facility identifier.
            sensor_value:
                Current sensor reading.
        Returns:
            Sensor value adjusted for facility characteristics.
        """

        if sensor_value is None:
            return None
        
        metadata = self.get_sensor_metadata(sensor_type)

        adjustment = (
            self.facility_profiles
            [facility_id]
            [sensor_type]
        )

        return round(
            sensor_value + adjustment,
            metadata["precision"]
        )

    def _generate_facility_profiles(
        self,
    ) -> dict[FacilityId, dict[str, float]]:
        """
        Generate permanent environmental profiles for all facilities.

        Each facility receives a fixed sensor offset during simulator
        initialization to represent unique operating characteristics.

        Returns:
            Mapping of facility-specific sensor offsets.
        """

        profiles: dict[
            FacilityId,
            dict[str, float],
        ] = {}

        for facility_id in self._generate_facility_ids():
            sensor_offsets: dict[str, float] = {}
            for sensor_type in self.get_supported_sensors():
                metadata = self.get_sensor_metadata(sensor_type)

                operating_range = (
                    metadata["max_value"] -
                    metadata["min_value"]
                )

                variation = (
                    operating_range * metadata[
                        "facility_variation_percentage"
                    ]
                )
                
                sensor_offsets[sensor_type] = (
                    self.random_manager.uniform(
                        -variation,
                        variation,
                    )
                )
            profiles[facility_id] = sensor_offsets
        
        return profiles

    def _determine_sensor_status(self) -> str:
        """
        Determine the simulated health status of a sensor.

        The returned status is selected using the configured
        probability distribution and the shared random number
        generator.

        Returns:
            Simulated sensor health status.
        """

        random_value = self.random_manager.random()

        if random_value < SENSOR_HEALTHY_PROBABILITY:
            return SENSOR_STATUS_HEALTHY

        if (
            random_value
            < SENSOR_HEALTHY_PROBABILITY
            + SENSOR_WARNING_PROBABILITY
        ):
            return SENSOR_STATUS_WARNING

        return SENSOR_STATUS_FAILED
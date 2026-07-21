"""
Environment state manager for the HydroGrow Smart Farming Simulator.

Maintains the shared simulation clock, weather conditions,
and day/night cycle used by all telemetry generators.
"""

import math
from datetime import datetime, timedelta
from smart_farming.config import (
    Settings,
    WeatherType,
    DAY_START_HOUR,
    NIGHT_START_HOUR,
    WEATHER_TYPES,
    WEATHER_SUNNY,
    WEATHER_PARTLY_CLOUDY,
    WEATHER_CLOUDY,
    WEATHER_RAINY,
    WEATHER_THUNDERSTORM,
    WEATHER_FOGGY,
    WEATHER_SOLAR_ATTENUATION,
    WEATHER_TRANSITIONS_MORNING,
    WEATHER_TRANSITIONS_AFTERNOON,
    WEATHER_TRANSITIONS_NIGHT,
    DIURNAL_MIN_TEMP_HOUR,
    DIURNAL_MAX_TEMP_HOUR,
    SIMULATION_START_HOUR,
    SIMULATION_START_MINUTE,
    WEATHER_MIN_DURATION_CYCLES,
    WEATHER_MAX_DURATION_CYCLES,
)
from smart_farming.models import WeatherState
from smart_farming.utils import RandomManager


class EnvironmentStateManager:
    """
    Manages the shared environmental state for the simulator.

    This component maintains the simulation clock, weather
    conditions, and day/night cycle that are consumed by all
    telemetry generators.
    """

    def __init__(
        self,
        settings: Settings,
        random_manager: RandomManager,
    ) -> None:
        """
        Initialize the environment state manager.

        Args:
            settings: Validated application settings.
            random_manager: Shared random number generator.
        """
        self.random_manager = random_manager
        self.settings = settings

        self.current_weather: WeatherType = WEATHER_SUNNY
        self.remaining_cycles: int = 0
        self.state: WeatherState

        # Shared simulation clock used by all event generators.
        self.simulation_time = datetime.utcnow().replace(
            hour=SIMULATION_START_HOUR,
            minute=SIMULATION_START_MINUTE,
            second=0,
            microsecond=0
        )

        self._initialize_weather()

    def get_current_state(self) -> WeatherState:
        """
        Return the current environmental state.

        Returns:
            Current weather state.
        """
        return self.state

    def advance_cycle(self) -> None:
        """
        Advance the environmental simulation by one cycle.

        Updates the simulation clock, determines whether the
        current weather should change, and refreshes the shared
        environmental state.
        """
        self._advance_simulation_time()
        self.remaining_cycles -= 1

        if self.remaining_cycles <= 0:
            self.current_weather = self._select_weather()
            self.remaining_cycles = self._random_weather_duration()

        self._update_environmental_physics()

    def _advance_simulation_time(self) -> None:
        """
        Advance the simulation clock by one configured time step.
        """
        self.simulation_time += timedelta(
            minutes=self.settings.simulation_time_step_minutes,
        )

    def _initialize_weather(self) -> None:
        """
        Initialize the first environmental state.
        """
        self.current_weather = WEATHER_SUNNY
        self.remaining_cycles = self._random_weather_duration()
        self._update_environmental_physics()

    def _is_daytime(self, timestamp: datetime) -> bool:
        """
        Determine whether the timestamp falls within daytime.
        """
        return DAY_START_HOUR <= timestamp.hour < NIGHT_START_HOUR

    def _select_weather(self) -> WeatherType:
        """
        Select the next weather condition using the Markov transition matrix.
        """
        hour = self.simulation_time.hour
        if 5 <= hour < 11:
            transition_matrix = WEATHER_TRANSITIONS_MORNING
        elif 11 <= hour < 17:
            transition_matrix = WEATHER_TRANSITIONS_AFTERNOON
        else:
            transition_matrix = WEATHER_TRANSITIONS_NIGHT

        probabilities = transition_matrix.get(self.current_weather, transition_matrix[WEATHER_SUNNY])
        options = list(probabilities.keys())
        weights = list(probabilities.values())

        weather = self.random_manager.weighted_choice(options, weights)
        if weather not in WEATHER_TYPES:
            weather = WEATHER_SUNNY
        return weather

    def _random_weather_duration(self) -> int:
        """
        Determine how many simulation cycles the current weather should persist.
        """
        return self.random_manager.randint(
            WEATHER_MIN_DURATION_CYCLES,
            WEATHER_MAX_DURATION_CYCLES,
        )

    def _update_environmental_physics(self) -> None:
        """
        Update ambient temperature, humidity, solar irradiance, and rainfall physics
        based on the diurnal curve and weather conditions.
        """
        hour_float = self.simulation_time.hour + self.simulation_time.minute / 60.0
        is_day = self._is_daytime(self.simulation_time)

        # 1. Solar elevation and irradiance calculations
        solar_irradiance = 0.0
        if is_day:
            solar_factor = math.sin(math.pi * (hour_float - DAY_START_HOUR) / (NIGHT_START_HOUR - DAY_START_HOUR))
            attenuation = WEATHER_SOLAR_ATTENUATION.get(self.current_weather, 1.0)
            solar_irradiance = 1000.0 * max(0.0, solar_factor) * attenuation

        # 2. Rainfall rate calculations (mm/hour)
        rainfall = 0.0
        if self.current_weather == WEATHER_RAINY:
            rainfall = self.random_manager.uniform(1.0, 5.0)
        elif self.current_weather == WEATHER_THUNDERSTORM:
            rainfall = self.random_manager.uniform(10.0, 35.0)

        # 3. Sinusoidal Diurnal Ambient Temperature Curve
        # Peaks at DIURNAL_MAX_TEMP_HOUR, minimum at DIURNAL_MIN_TEMP_HOUR
        mid_hour = (DIURNAL_MAX_TEMP_HOUR + DIURNAL_MIN_TEMP_HOUR) / 2.0
        period = DIURNAL_MAX_TEMP_HOUR - DIURNAL_MIN_TEMP_HOUR
        diurnal_factor = math.sin(math.pi * (hour_float - mid_hour) / (period * 1.5))
        ambient_temp = 27.0 + 4.5 * diurnal_factor

        # Modulate temperature by weather state
        if self.current_weather == WEATHER_RAINY:
            ambient_temp -= 2.5
        elif self.current_weather == WEATHER_THUNDERSTORM:
            ambient_temp -= 4.5
        elif self.current_weather == WEATHER_FOGGY:
            ambient_temp -= 1.5
        elif self.current_weather == WEATHER_CLOUDY:
            ambient_temp -= 1.2
        elif self.current_weather == WEATHER_PARTLY_CLOUDY:
            ambient_temp -= 0.5

        # Tiny random thermal noise fluctuation
        ambient_temp += self.random_manager.uniform(-0.3, 0.3)

        # 4. Sinusoidal Relative Humidity Curve (inversely proportional to temperature)
        ambient_humidity = 78.0 - 15.0 * diurnal_factor

        # Boost humidity during precipitation or morning fog
        if self.current_weather == WEATHER_RAINY:
            ambient_humidity = self.random_manager.uniform(88.0, 94.0)
        elif self.current_weather == WEATHER_THUNDERSTORM:
            ambient_humidity = self.random_manager.uniform(92.0, 98.0)
        elif self.current_weather == WEATHER_FOGGY:
            ambient_humidity = self.random_manager.uniform(90.0, 96.0)

        # Clamp relative humidity bounds
        ambient_humidity = max(40.0, min(100.0, ambient_humidity))

        self.state = WeatherState(
            timestamp=self.simulation_time,
            weather=self.current_weather,
            is_daytime=is_day,
            ambient_temperature_celsius=round(ambient_temp, 2),
            ambient_humidity_percent=round(ambient_humidity, 2),
            solar_irradiance_w_m2=round(solar_irradiance, 2),
            rainfall_mm_hr=round(rainfall, 2),
        )

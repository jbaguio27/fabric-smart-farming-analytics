"""
Environment state manager for the HydroGrow Smart Farming Simulator.

Maintains the shared simulation clock, weather conditions,
and day/night cycle used by all telemetry generators.
"""

from datetime import (
    datetime,
    timedelta,
)
from smart_farming.config import (
    Settings,
    WeatherType,
    DAY_START_HOUR,
    DAY_END_HOUR,
    WEATHER_TYPES,
    WEATHER_PROBABILITIES,
    WEATHER_MIN_DURATION_CYCLES,
    WEATHER_MAX_DURATION_CYCLES,
    SIMULATION_START_HOUR,
    SIMULATION_START_MINUTE,
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
            settings:
                Validated application settings.
            random_manager:
                Shared random number generator used throughout the
                simulator.
        """

        self.random_manager = random_manager
        self.settings = settings

        self.current_weather: WeatherType
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
            self.remaining_cycles = (
                self._random_weather_duration()
            )

        self.state = WeatherState(
            timestamp=self.simulation_time,
            weather=self.current_weather,
            is_daytime=self._is_daytime(
                self.simulation_time
            )
        )

    def _advance_simulation_time(self) -> None:
        """
        Advance the simulation clock by one configured time step.

        The step size is determined by the simulator settings.
        """

        self.simulation_time += timedelta(
            minutes=self.settings.simulation_time_step_minutes,
        )

    def _initialize_weather(self) -> None:
        """
        Initialize the first environmental state.

        Randomly selects the initial weather condition,
        determines its duration, and creates the initial
        shared weather state.
        """

        self.current_weather = self._select_weather()
        self.remaining_cycles = (
            self._random_weather_duration()
        )

        self.state = WeatherState(
            timestamp=self.simulation_time,
            weather=self.current_weather,
            is_daytime=self._is_daytime(
                self.simulation_time,
            )
        )

    def _is_daytime(
        self,
        timestamp: datetime,
    ) -> bool:
        """
        Determine whether the timestamp falls within daytime.

        Args:
            timestamp:
                Timestamp to evaluate.

        Returns:
            True if the timestamp falls within daytime,
            otherwise False.
        """

        return (
            DAY_START_HOUR
            <= timestamp.hour
            < DAY_END_HOUR
        )

    def _select_weather(self) -> str:
        """
        Select the next weather condition.

        Weather selection is performed using the configured
        probability distribution.

        Returns:
            Randomly selected weather condition.
        """

        return self.random_manager.weighted_choice(
            options=WEATHER_TYPES,
            weights=[
                WEATHER_PROBABILITIES[weather]
                for weather in WEATHER_TYPES
            ],
        )

    def _random_weather_duration(self) -> int:
        """
        Determine how many simulation cycles the current weather
        should persist.

        Returns:
            Number of simulation cycles.
        """

        return self.random_manager.randint(
            WEATHER_MIN_DURATION_CYCLES,
            WEATHER_MAX_DURATION_CYCLES,
        )
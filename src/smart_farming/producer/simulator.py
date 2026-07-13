"""
Core simulator for the HydroGrow Smart Farming Simulator.
"""

import time
import logging
from smart_farming.config import Settings
from smart_farming.monitoring import (
    get_logger,
)
from smart_farming.producer import (
    EventDispatcher,
)
from smart_farming.generators import BaseTelemetryGenerator
from smart_farming.environment import EnvironmentStateManager


class Simulator:
    """
    Coordinates execution of the Smart Farming Simulator.

    The simulator advances the shared simulation state, executes every
    registered telemetry generator, and dispatches the resulting events.

    Telemetry generators are executed through the shared
    BaseTelemetryGenerator interface, allowing additional generators to
    be introduced without modifying simulator orchestration.

    """

    def __init__(
        self,
        settings: Settings,
        dispatcher: EventDispatcher,
        generator: list[BaseTelemetryGenerator],
        environment_manager: EnvironmentStateManager,
    ) -> None:
        self.settings: Settings = settings
        self.dispatcher: EventDispatcher = dispatcher
        self.generator: list[
            BaseTelemetryGenerator
        ] = generators
        self.environment_manager: EnvironmentStateManager = environment_manager
        self.logger: logging.Logger = get_logger(__name__)
        self.is_running: bool = False
        self.completed_cycles: int = 0

        self.logger.info(
            "Simulator initialized successfully."
        )

    def stop(self) -> None:
        """
        Stop the Smart Farming simulator.

        Marks the simulator as no logner running and performs
        shutdown logging.
        """

        self.is_running = False

        self.logger.info(
            "Simulator stopped successfully after %d simulation cycles.",
            self.completed_cycles,
        )    

    def run(self) -> None:
        """
        Run the Smart Farming simulation.

        Continuously executes simulation cycles until stopped.
        """

        self.logger.info(
            "Starting simulator in '%s' environment.",
            self.settings.environment
        )

        self.logger.info("Simulator is ready.")

        self.is_running = True

        try:
            while self.is_running:
                self._run_simulation_cycle()

                self.logger.debug(
                    "Waiting %d seconds before next simulation cycle.",
                    self.settings.simulation_interval_seconds,
                )

                time.sleep(
                    self.settings.simulation_interval_seconds
                )
        except KeyboardInterrupt:
            self.logger.info(
                "Shutdown signal received. Stopping simulator..."
            )

            self.stop()

    def _run_simulation_cycle(self) -> None:
        """
        Execute a single Smart Farming simulation cycle.

        A simulation cycle generates telemetry events for all configured
        facilities and dispatches them to the event dispatcher.
        """
        self.environment_manager.advance_cycle()

        environment = (
            self.environment_manager.get_current_state()
        )

        self.logger.info(
            (
                "Environment updated | "
                "Weather=%s | "
                "Daytime=%s | "
                "Time=%s"
            ),
            environment.weather,
            environment.is_daytime,
            environment.timestamp.isoformat(),
        )

        events = []

        for generator in self.generators:
            generated_events = generator.generate()

            events.extend(generated_events)

        self.logger.info(
            "Generated %d events for dispatch.",
            len(events),
        )

        # for event in events:
        #     self.logger.info(
        #         "Time=%s | Weather=%s | Day=%s | Facility=%s | Sensor=%s | Value=%s %s | Status=%s",
        #         event.timestamp,
        #         event.weather,
        #         event.is_daytime,
        #         event.facility_id,
        #         event.sensor_type,
        #         event.sensor_value,
        #         event.unit,
        #         event.sensor_status,
        #     )

        self.dispatcher.dispatch(events)

        self.completed_cycles += 1

        self.logger.info(
            "Simulation cycle completed."
        )
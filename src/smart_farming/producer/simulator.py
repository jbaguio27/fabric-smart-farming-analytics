"""
Core simulator for the HydroGrow Smart Farming Simulator.
"""

import time
import logging
from smart_farming.config.settings import Settings
from smart_farming.monitoring.logger import get_logger
from smart_farming.producer.event_dispatcher import EventDispatcher
from smart_farming.generators.environmental_generator import EnvironmentalTelemetryGenerator
from smart_farming.models.environmental_event import (
    EnvironmentalTelemetryEvent,
)


class Simulator:
    """
    Coordinates the execution of the Smart Farming Simulator.
    """

    def __init__(
        self,
        settings: Settings,
        dispatcher: EventDispatcher,
        generator: EnvironmentalTelemetryGenerator
    ) -> None:
        self.settings: Settings = settings
        self.dispatcher: EventDispatcher = dispatcher
        self.generator: EnvironmentalTelemetryGenerator = generator
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

        events: list[EnvironmentalTelemetryEvent] = (
            self.generator.generate()
        )

        self.logger.info(
            "Generated %d events for dispatch.",
            len(events),
        )

        self.dispatcher.dispatch(events)

        self.completed_cycles += 1

        self.logger.info(
            "Simulation cycle completed."
        )
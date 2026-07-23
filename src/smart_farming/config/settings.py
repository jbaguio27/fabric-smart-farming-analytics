"""
Application settings for the HydroGrow Smart Farming Simulator.

These settings define the simulator's runtime behavior.
Static application values belong in constants.py.
"""

from dataclasses import dataclass, field
import os
from dotenv import load_dotenv
from pathlib import Path
from smart_farming.utils.exceptions import ConfigurationError
from .constants import (
    VALID_ENVIRONMENTS,
    VALID_LOG_LEVELS,
    MIN_SIMULATION_INTERVAL_SECONDS,
    MIN_TOTAL_FACILITIES,
    MIN_EVENT_BATCH_SIZE,
    MIN_RANDOM_SEED,
)
from .equipment_runtime import MIN_SIMULATION_CYCLE_HOURS

@dataclass(slots=True)
class Settings:
    """Runtime configuration for the Smart Farming Simulator."""

    # ------------------------------------------------------------
    # Application Configuration
    # ------------------------------------------------------------

    environment: str = field(
        default_factory=lambda: os.getenv("ENVIRONMENT", "development")
    )
    log_level: str = field(
        default_factory=lambda: os.getenv("LOG_LEVEL", "INFO")
    )

    # ------------------------------------------------------------
    # Facility Configuration
    # ------------------------------------------------------------

    total_facilities: int = field(
        default_factory=lambda: int(
            os.getenv("TOTAL_FACILITIES", "8")
        )
    )

    zone_count: int = field(
        default_factory=lambda: int(
            os.getenv("ZONE_COUNT", "100")
        )
    )

    # ------------------------------------------------------------
    # Simulator Configuration
    # ------------------------------------------------------------

    random_seed: int = field(
        default_factory=lambda: int(
            os.getenv("RANDOM_SEED", "42")
        )
    )
    simulation_interval_seconds: int = field(
        default_factory=lambda: int(
            os.getenv("SIMULATION_INTERVAL_SECONDS", "5")
        )
    )
    simulation_cycle_hours: float = field(
        default_factory=lambda: float(
            os.getenv("SIMULATION_CYCLE_HOURS", "1.0")
        )
    )
    simulation_time_step_minutes: int = field(
        default_factory=lambda: int(
            os.getenv(
                "SIMULATION_TIME_STEP_MINUTES",
                "5"
            )
        )
    )

    event_batch_size: int = field(
        default_factory=lambda: int(
            os.getenv("EVENT_BATCH_SIZE", "100")
        )
    )

    equipment_telemetry_sample_rate: float = field(
        default_factory=lambda: float(
            os.getenv("EQUIPMENT_TELEMETRY_SAMPLE_RATE", "1.0")
        )
    )

    # ------------------------------------------------------------
    # Microsoft Fabric Configuration
    # ------------------------------------------------------------

    fabric_workspace: str = field(
        default_factory=lambda: os.getenv("FABRIC_WORKSPACE", "")
    )

    eventstream_endpoint: str = field(
        default_factory=lambda: os.getenv("EVENTSTREAM_ENDPOINT", "")
    )

    eventstream_name: str = field(
        default_factory=lambda: os.getenv("EVENTSTREAM_NAME", "")
    )

    eventhouse_name: str = field(
        default_factory=lambda: os.getenv("EVENTHOUSE_NAME", "")
    )

    kql_database: str = field(
        default_factory=lambda: os.getenv("KQL_DATABASE", "")
    )

    lakehouse_name: str = field(
        default_factory=lambda: os.getenv("LAKEHOUSE_NAME", "")
    )

    warehouse_name: str = field(
        default_factory=lambda: os.getenv("WAREHOUSE_NAME", "")
    )

    powerbi_workspace: str = field(
        default_factory=lambda: os.getenv("POWERBI_WORKSPACE", "")
    )

    @classmethod
    def from_env(cls) -> "Settings":
        """
        Create and validate a Settings instance from the projects's
        environment variables.

        Returns:
            Settings: The validated application configuration.
        """

        PROJECT_ROOT = Path(__file__).resolve().parents[3]
        load_dotenv(
            dotenv_path=PROJECT_ROOT / ".env",
            override=True,
        )

        return cls()

    def __post_init__(self) -> None:
        """
        Normalize and validate application configuration.

        Raises:
            ConfigurationError:
                If one or more configuration values are invalid.
        """
        # ------------------------------------------------------------
        # Normalize configuration values
        # ------------------------------------------------------------

        self.environment = self.environment.lower()
        self.log_level = self.log_level.upper()

        errors: list[str] = []

        # ------------------------------------------------------------
        # Application Configuration
        # ------------------------------------------------------------

        if self.environment not in VALID_ENVIRONMENTS:
            errors.append(
                "ENVIRONMENT must be one of: "
                f"{', '.join(sorted(VALID_ENVIRONMENTS))}."
            )

        if self.log_level not in VALID_LOG_LEVELS:
            errors.append(
                "LOG_LEVEL must be one of: "
                f"{', '.join(sorted(VALID_LOG_LEVELS))}."
            )

        # ------------------------------------------------------------
        # Simulator Configuration
        # ------------------------------------------------------------

        if self.simulation_interval_seconds < MIN_SIMULATION_INTERVAL_SECONDS:
            errors.append(
                f"SIMULATION_INTERVAL_SECONDS must be at least "
                f"{MIN_SIMULATION_INTERVAL_SECONDS}."
            )

        if self.simulation_cycle_hours < MIN_SIMULATION_CYCLE_HOURS:
            errors.append(
                f"SIMULATION_CYCLE_HOURS must be at least "
                f"{MIN_SIMULATION_CYCLE_HOURS}."
            )

        if self.simulation_time_step_minutes <= 0:
            errors.append(
                "SIMULATION_TIME_STEP_MINUTES must be greater than 0."
            )

        if self.total_facilities < MIN_TOTAL_FACILITIES:
            errors.append(
                f"TOTAL_FACILITIES must be at least "
                f"{MIN_TOTAL_FACILITIES}."
            )

        if self.event_batch_size < MIN_EVENT_BATCH_SIZE:
            errors.append(
                f"EVENT_BATCH_SIZE must be at least "
                f"{MIN_EVENT_BATCH_SIZE}."
            )
        
        if self.random_seed < MIN_RANDOM_SEED:
            errors.append(
                f"RANDOM_SEED must be at least "
                f"{MIN_RANDOM_SEED}."
            )

        # ------------------------------------------------------------
        # Raise Validation Errors
        # ------------------------------------------------------------

        if errors:
            raise ConfigurationError(
                "Invalid application configuration:\n- "
                + "\n- ".join(errors)
            )
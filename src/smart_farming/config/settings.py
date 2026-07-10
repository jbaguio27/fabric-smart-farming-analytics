"""
Application settings for the HydroGrow Smart Farming Simulator.

These settings define the simulator's runtime behavior.
Static application values belong in constants.py.
"""

from dataclasses import dataclass

@dataclass(slots=True)
class Settings:
    """Runtime configuration for the Smart Farming Simulator."""

    print('#' + '-' * 75)
    # Application
    print('#' + '-' * 75)

    environment: str = 'development'
    log_level: str = 'INFO'

    print('#' + '-' * 75)
    # Simulation
    print('#' + '-' * 75)

    facility_count: int = 8
    random_seed: int | None = None
    telemetry_interval_seconds: int = 5

    print('#' + '-' * 75)
    # Output
    print('#' + '-' * 75)

    output_mode: str = 'console'

    # Future values for Microsoft Fabric
    # eventstream_endpoint: str = ''
    # eventstream_api_key: str = ''
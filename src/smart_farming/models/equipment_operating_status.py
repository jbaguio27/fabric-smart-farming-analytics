"""
Equipment operating status enumeration.

This module defines the runtime operating states used by simulated
equipment assets throughout the HydroGrow Smart Farming simulator.

The operating status represents the current operational condition of an
equipment asset during simulation and is shared across runtime state
models, telemetry events, maintenance processing, and failure analysis.

Separating this enumeration into its own module avoids unnecessary
coupling between the immutable Equipment domain model and runtime
simulation components, while providing a single authoritative definition
for equipment operating states across the project.
"""

from enum import Enum


class EquipmentOperatingStatus(str, Enum):
    """
    Enumerates the runtime operating states of an equipment asset.

    These values describe the current operational condition of an
    equipment asset as determined by the simulation. They are updated by
    the EquipmentStateManager based on equipment health, operating load,
    calculated failure probability, and maintenance activity.

    The enumeration is intentionally independent of the Equipment domain
    model so that runtime state models, telemetry events, maintenance
    services, and failure models can reference a shared definition
    without introducing unnecessary dependencies.

    Attributes
    ----------
    ONLINE:
        Equipment is operating normally within expected parameters.

    OFFLINE:
        Equipment is intentionally not operating or has been taken out of
        service.

    WARNING:
        Equipment remains operational but exhibits elevated operating
        risk or degraded performance that may require maintenance.

    ERROR:
        Equipment has entered a critical operating state and requires
        maintenance or repair before returning to normal operation.
    """

    ONLINE = "ONLINE"
    OFFLINE = "OFFLINE"
    WARNING = "WARNING"
    ERROR = "ERROR"
"""
Equipment domain model.

This module defines the persistent business entity representing physical
equipment installed within a HydroGrow smart farming facility.

Equipment objects contain stable business metadata used throughout the
simulation. Dynamic runtime characteristics such as health, operating
status, power consumption, temperature, and vibration are intentionally
managed outside this model.

This separation keeps persistent asset information independent from
telemetry generation and aligns with the project's event-driven
architecture.
"""

from dataclasses import dataclass


@dataclass(slots=True)
class Equipment:
    """
    Represents a physical equipment asset installed within a facility.

    This model stores persistent business metadata only. Runtime values
    are managed by the EquipmentStateManager and emitted through
    equipment telemetry events.

    Attributes
    ----------
    equipment_id:
        Unique identifier for the equipment asset.

    facility_id:
        Identifier of the facility where the equipment is installed.

    zone_id:
        Identifier of the growing zone where the equipment operates.

    equipment_type:
        Equipment category.

    manufacturer:
        Equipment manufacturer.

    model:
        Manufacturer model designation.

    serial_number:
        Manufacturer-assigned serial number.
    """

    equipment_id: str
    facility_id: str
    zone_id: str

    equipment_type: str

    manufacturer: str
    model: str
    serial_number: str
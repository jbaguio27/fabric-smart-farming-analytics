"""
Maintenance Event telemetry model.

This module defines the immutable telemetry event representing a
maintenance work order within the HydroGrow Smart Farming Simulator.

Unlike MaintenanceState, which is mutable runtime state owned by the
MaintenanceStateManager, this model represents a snapshot of a maintenance
activity at the time the telemetry event is emitted.

The model intentionally contains no business logic, validation, or event
serialization.
"""

from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class MaintenanceEvent:
    """
    Immutable maintenance telemetry event.

    One MaintenanceEvent represents the current state of a maintenance
    work order when emitted by the MaintenanceEventGenerator.
    """

    event_type: str

    simulation_cycle: int

    timestamp: str

    facility_id: str

    work_order_id: str

    equipment_id: str

    zone_id: str

    maintenance_type: str

    priority: str

    assigned_technician: str

    work_status: str

    estimated_duration_minutes: int

    remaining_duration_minutes: int

    completion_percent: float

    is_active: bool
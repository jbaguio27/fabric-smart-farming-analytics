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
from .base_event import BaseEvent


@dataclass(slots=True)
class MaintenanceEvent(BaseEvent):
    """
    Immutable maintenance telemetry event.
    """

    zone_id: str
    equipment_id: str
    work_order_id: str
    maintenance_cycle: int
    maintenance_type: str
    priority: str
    assigned_technician: str
    maintenance_status: str
    estimated_duration_minutes: int
    remaining_duration_minutes: int
    completion_percent: float
    is_active: bool
    technician_notes: str
    health_restored: float
    simulation_cycle: int
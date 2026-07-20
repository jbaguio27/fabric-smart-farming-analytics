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

    event_type

    event_timestamp

    simulation_cycle

    facility_id

    zone_id

    equipment_id

    work_order_id

    maintenance_cycle

    maintenance_type

    priority

    assigned_technician

    work_status

    estimated_duration_minutes
    
    remaining_duration_minutes

    completion_percent

    is_active
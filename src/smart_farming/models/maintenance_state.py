"""
Runtime state model for maintenance work orders.

This module defines the mutable runtime state representing an active
maintenance activity within the HydroGrow Smart Farming Simulator.

Unlike Maintenance Event telemetry models, this runtime state exists only
inside the simulator and evolves continuously as work orders are created,
assigned, executed, and completed.

The MaintenanceStateManager owns these runtime objects and serves as the
authoritative source of maintenance information for the simulator.

Responsibilities
----------------
The runtime state tracks:

- Work order lifecycle
- Assigned equipment
- Assigned technician
- Maintenance priority
- Maintenance type
- Estimated duration
- Remaining duration
- Completion progress

Event serialization and validation are handled by higher application
layers.
"""

from dataclasses import dataclass


@dataclass(slots=True)
class MaintenanceState:
    """
    Mutable runtime maintenance state.

    One instance represents one maintenance work order.
    """

    work_order_id: str

    facility_id: str

    equipment_id: str

    maintenance_type: str

    priority: str

    assigned_technician: str

    work_status: str

    estimated_duration_minutes: int

    remaining_duration_minutes: int

    completion_percent: float

    maintenance_cycle: int

    is_active: bool
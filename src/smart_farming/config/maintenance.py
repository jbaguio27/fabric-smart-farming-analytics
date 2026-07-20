"""
Maintenance domain configuration.

This module contains immutable business configuration for the maintenance
subsystem used by the HydroGrow Smart Farming Simulator.

The values defined here describe maintenance policies, work-order
classification, technician identifiers, lifecycle states, and default
durations.

These values are consumed by:

- MaintenanceStateManager
- MaintenanceEventGenerator
- Future maintenance scheduling services

This module intentionally contains no runtime logic.
"""

from typing import Final

# ============================================================================
# Event
# ============================================================================

EVENT_TYPE_MAINTENANCE: Final[str] = "maintenance"

# ============================================================================
# Work Order Identifiers
# ============================================================================

WORK_ORDER_ID_PREFIX: Final[str] = "WO"

TECHNICIAN_ID_PREFIX: Final[str] = "TECH"

# ============================================================================
# Maintenance Types
# ============================================================================

MAINTENANCE_TYPE_PREVENTIVE: Final[str] = "PREVENTIVE"

MAINTENANCE_TYPE_CORRECTIVE: Final[str] = "CORRECTIVE"

MAINTENANCE_TYPE_EMERGENCY: Final[str] = "EMERGENCY"

MAINTENANCE_TYPE_INSPECTION: Final[str] = "INSPECTION"

MAINTENANCE_TYPES: Final[tuple[str, ...]] = (
    MAINTENANCE_TYPE_PREVENTIVE,
    MAINTENANCE_TYPE_CORRECTIVE,
    MAINTENANCE_TYPE_EMERGENCY,
    MAINTENANCE_TYPE_INSPECTION,
)

# ============================================================================
# Priority Levels
# ============================================================================

MAINTENANCE_PRIORITY_LOW: Final[str] = "LOW"

MAINTENANCE_PRIORITY_MEDIUM: Final[str] = "MEDIUM"

MAINTENANCE_PRIORITY_HIGH: Final[str] = "HIGH"

MAINTENANCE_PRIORITY_CRITICAL: Final[str] = "CRITICAL"

MAINTENANCE_PRIORITIES: Final[tuple[str, ...]] = (
    MAINTENANCE_PRIORITY_LOW,
    MAINTENANCE_PRIORITY_MEDIUM,
    MAINTENANCE_PRIORITY_HIGH,
    MAINTENANCE_PRIORITY_CRITICAL,
)

# ============================================================================
# Work Order Status
# ============================================================================

WORK_STATUS_OPEN: Final[str] = "OPEN"

WORK_STATUS_ASSIGNED: Final[str] = "ASSIGNED"

WORK_STATUS_IN_PROGRESS: Final[str] = "IN_PROGRESS"

WORK_STATUS_COMPLETED: Final[str] = "COMPLETED"

WORK_STATUS_CANCELLED: Final[str] = "CANCELLED"

WORK_STATUSES: Final[tuple[str, ...]] = (
    WORK_STATUS_OPEN,
    WORK_STATUS_ASSIGNED,
    WORK_STATUS_IN_PROGRESS,
    WORK_STATUS_COMPLETED,
    WORK_STATUS_CANCELLED,
)

# ============================================================================
# Default Work Durations (minutes)
# ============================================================================

DEFAULT_PREVENTIVE_DURATION_MINUTES: Final[int] = 60

DEFAULT_CORRECTIVE_DURATION_MINUTES: Final[int] = 90

DEFAULT_INSPECTION_DURATION_MINUTES: Final[int] = 30

DEFAULT_EMERGENCY_DURATION_MINUTES: Final[int] = 120

# ============================================================================
# Technician Pool
# ============================================================================

DEFAULT_TECHNICIANS: Final[tuple[str, ...]] = (
    "TECH001",
    "TECH002",
    "TECH003",
)

# ============================================================================
# Existing Simulator Policy
# ============================================================================

MAINTENANCE_INTERVAL_HOURS: Final[int] = 500

MAINTENANCE_HEALTH_THRESHOLD: Final[float] = 40.0

MAINTENANCE_RESTORE_HEALTH: Final[float] = 100.0

MAINTENANCE_RESET_FAILURE_PROBABILITY: Final[float] = 0.001
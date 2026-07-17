"""
Runtime state model for simulated crop batches.

This module defines the mutable in-memory state maintained for each
simulated crop batch throughout its lifecycle. The runtime state is the
authoritative source from which Crop Batch Lifecycle events are
generated.

The model intentionally contains only simulation state. Event formatting,
validation, and serialization remain the responsibility of higher
application layers.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass(slots=True)
class CropState:
    """
    Represents the mutable runtime state of a simulated crop batch.

    A CropState instance tracks the current biological lifecycle of a
    crop batch as it progresses through the simulation. This state is
    updated by the CropStateManager and consumed by the
    CropLifecycleGenerator when producing telemetry events.

    This model intentionally contains no business logic.
    """
    
    crop_batch_id: str
    zone_id: str
    crop_type: str

    lifecycle_stage: str

    planting_timestamp: Optional[datetime]
    expected_harvest_timestamp: Optional[datetime]

    age_days: float
    health_score: float
    is_active: bool
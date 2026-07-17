"""
Growth profile model for indoor vertical farming crops.

This module defines immutable biological characteristics used by the
Crop Lifecycle Generator to simulate realistic crop development.

Growth profiles contain species-specific constants rather than mutable
runtime state. Runtime progression remains the responsibility of the
CropStateManager.
"""

from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class CropGrowthProfile:
    """
    Immutable biological characteristics for a crop type.

    Instances of this model describe the expected lifecycle timing and
    health characteristics of a commercially cultivated indoor crop.
    These values are consumed by the CropStateManager during lifecycle
    simulation.

    Attributes:
        crop_type:
            Human-readable crop variety.

        germination_days:
            Expected duration of germination.

        seedling_days:
            Expected duration of the seedling stage.

        vegetative_days:
            Expected duration of vegetative growth.

        mature_days:
            Expected duration spent in the mature stage before harvest.

        optimal_health:
            Baseline health score assigned to newly planted crops.
    """

    crop_type: str
    
    germination_days: int
    seedling_days: int
    vegetative_days: int
    mature_days: int

    optimal_health: float
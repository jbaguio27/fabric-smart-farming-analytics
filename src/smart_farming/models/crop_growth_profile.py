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
    Immutable biological growth profile for an indoor vertical farming crop.

    A CropGrowthProfile defines the species-specific characteristics used
    throughout the simulation. These values describe the expected
    biological development timeline together with the optimal
    environmental conditions required for healthy growth.

    Growth profiles contain immutable business configuration only. They
    never store mutable runtime state, which remains the responsibility
    of the CropStateManager.

    Attributes:
        crop_type:
            Human-readable crop variety.

        germination_days:
            Expected duration of the germination stage.

        seedling_days:
            Expected duration of the seedling stage.

        vegetative_days:
            Expected duration of the vegetative growth stage.

        maturity_days:
            Expected number of days required to reach harvest maturity.

        optimal_temperature_celsius:
            Ideal air temperature for healthy crop development.

        optimal_humidity_percent:
            Ideal relative humidity for healthy crop development.

        optimal_ph:
            Ideal nutrient solution pH.

        optimal_ec:
            Ideal nutrient solution electrical conductivity
            measured in mS/cm.

        optimal_health:
            Initial health score assigned to newly planted crop batches.
            Future simulation logic uses this value as the biological
            baseline when evaluating environmental and operational
            stress.
    """

    crop_type: str

    germination_days: int
    seedling_days: int
    vegetative_days: int
    maturity_days: int

    optimal_temperature_celsius: float
    optimal_humidity_percent: float
    optimal_ph: float
    optimal_ec: float

    optimal_health: float = 100.0
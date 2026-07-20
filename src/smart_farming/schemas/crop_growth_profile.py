"""
Crop growth profile schema.

This module defines the immutable biological growth characteristics for a
crop species supported by the HydroGrow Smart Farming Simulator.

Unlike runtime crop state, these profiles describe species-specific
configuration that remains constant throughout the lifetime of the
application.

The CropStateManager consumes these profiles to determine growth rates,
stage transitions, biomass accumulation, and resource consumption.

These objects intentionally contain no simulation behaviour.
"""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class CropGrowthProfile:
    """
    Immutable biological configuration for a crop species.

    Attributes
    ----------
    crop_type:
        Human-readable crop name.

    germination_days:
        Expected germination duration.

    seedling_days:
        Expected seedling duration.

    vegetative_days:
        Expected vegetative growth duration.

    mature_days:
        Expected mature production duration.

    optimal_temperature_c:
        Ideal air temperature.

    optimal_humidity_percent:
        Ideal relative humidity.

    optimal_ph:
        Ideal nutrient solution pH.

    optimal_ec:
        Ideal electrical conductivity.

    biomass_growth_rate:
        Daily biomass accumulation factor.

    daily_water_uptake_liters:
        Expected daily water consumption.

    daily_nutrient_uptake_grams:
        Expected daily nutrient uptake.
    """

    crop_type: str

    germination_days: float
    seedling_days: float
    vegetative_days: float
    maturity_days: float

    optimal_temperature_celsius: float
    optimal_humidity_percent: float

    optimal_ph: float
    optimal_ec: float

    biomass_growth_rate: float

    daily_water_uptake_liters: float
    daily_nutrient_uptake_grams: float
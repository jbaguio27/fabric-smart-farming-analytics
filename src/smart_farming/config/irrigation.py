"""
Irrigation simulation configuration.

This module contains simulator-wide configuration values governing
runtime irrigation behavior.

The values defined here represent nominal operating targets for a
commercial indoor hydroponic vertical farm. They are intentionally
isolated from the irrigation controller so that scheduling behavior
can be tuned without modifying simulation logic.

Future milestones may extend this module with crop-specific irrigation
profiles, nutrient recipes, seasonal operating modes, and facility
optimization parameters.
"""

# ==================================================================
# Irrigation Scheduling
# ==================================================================

DEFAULT_IRRIGATION_INTERVAL_CYCLES = 3

DEFAULT_IRRIGATION_DURATION_CYCLES = 1

# ==================================================================
# Hydraulic Targets
# ==================================================================

DEFAULT_IRRIGATION_FLOW_RATE_LPM = 2.5

DEFAULT_IRRIGATION_PRESSURE_BAR = 2.2

# ==================================================================
# Water Delivery
# ==================================================================

DEFAULT_WATER_APPLICATION_LITERS = 0.20

# ==================================================================
# Controller
# ==================================================================

IRRIGATION_CONTROLLER_UPDATE_INTERVAL = 1

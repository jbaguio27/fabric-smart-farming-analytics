"""
LED Lighting Subsystem Configuration.

This module contains domain constants for LED spectrum, Photosynthetic Photon Flux Density
(PPFD), Daily Light Integral (DLI), and photoperiod operating hours for vertical racks.
"""

from typing import Final


# LED Array Spectrum & Intensity Parameters
TARGET_PPFD_UMOL_M2_S: Final[float] = 400.0
MIN_PPFD_UMOL_M2_S: Final[float] = 200.0
MAX_PPFD_UMOL_M2_S: Final[float] = 600.0

# Daily Light Integral (DLI) Bounds
TARGET_DLI_MOL_M2_DAY: Final[float] = 18.0
MIN_DLI_MOL_M2_DAY: Final[float] = 14.0
MAX_DLI_MOL_M2_DAY: Final[float] = 22.0

# Standard Vertical Farm Photoperiod Hours
DEFAULT_PHOTOPERIOD_HOURS: Final[float] = 16.0

"""
Utility functions for generating unique identifiers used throughout
the HydroGrow Smart Farming Simulator.
"""

from uuid import uuid4

def generate_event_id() -> str:
    """
    Generate a unique identifier for an event.

    Returns:
        A UUID4 string.
    """

    return str(uuid4())
"""
Utility functions for generating random values used throughout the
HydroGrow Smart Farming Simulator.
"""

import random
from typing import Any

def random_float(min_value: float, max_value: float, precision: int = 2) -> float:
    """
    Generate a random floating-point number.

    Args:
        min_value: Minimum value.
        max_value: Maximum value.
        precision: Number of decimal places.
    
    Returns:
        Random float.
    """

    return round(random.uniform(min_value, max_value), precision)

def random_int(min_value: int, max_value: int) -> int:
    """
    Generate a random integer.

    Args:
        min_value: Minimum value.
        max_value: Maximum value.
    
    Returns:
        Random integer.
    """
    
    return random.randint(min_value, max_value)

def random_bool() -> bool:
    """
    Generate a random boolean value.

    Returns:
        True or False
    """
    
    return random.choice((True, False))

def ramdom_choice(options: list[Any] | tuple[Any, ...]) -> Any:
    """
    Select a random item from a sequence.

    Args:
        options: List or tuple of values.
    
    Returns:
        Randomly selected item.
    """

    return random.choice(options)

def weighted_choice(
    options: list[Any] | tuple[Any, ...],
    weights: list[float],
) -> Any:
    """
    Select a random item using weighted probabilities.

    Args:
        options: Candidate values.
        weights: Probability weights.

    Returns:
        Randomly selected item.
    """

    return ramdom.choice(options, weights=weights, k=1)[0]
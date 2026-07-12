"""
Centralized random number generator for the HydroGrow Smart Farming
Simulator.

All simulator components should use this class instead of importing
Python's random module directly. This ensures deterministic and
reproducible simulation runs when a random seed is configured.
"""

import random
from typing import Any


class RandomManager:
    """
    Shared random number generator for the simulator.
    """

    def __init__(
        self,
        seed: int,
    ) -> None:
        """
        Initialize the random number generator.

        Args:
            seed: Seed used to produce deterministic simulation runs.
        """

        self._generator = random.Random(seed)

    def random(self) -> float:
        """
        Return a random float between 0.0 and 1.0.
        """

        return self._generator.random()

    def uniform(
        self,
        minimum: float,
        maximum: float,
    ) -> float:
        """
        Return a random floating point value.

        Args:
            minimum: Lower bound.
            maximum: Upper bound.

        Returns:
            Random floating point value.
        """

        return self._generator.uniform(
            minimum,
            maximum,
        )

    def randint(
        self,
        minimum: int,
        maximum: int,
    ) -> int:
        """
        Return a random integer.

        Args:
            minimum: Lower bound.
            maximum: Upper bound.

        Returns:
            Random integer.
        """

        return self._generator.randint(
            minimum,
            maximum,
        )

    def weighted_choice(
        self,
        options: list[Any] | tuple[Any, ...],
        weights: list[float],
    ) -> Any:
        """
        Return a weighted random item.

        Args:
            options:
                Available values.

            weights:
                Relative probability weights.

        Returns:
            Randomly selected value.
        """

        return self._generator.choices(
            population=options,
            weights=weights,
            k=1,
        )[0]

    def choices(
        self,
        options: list[Any] | tuple[Any, ...],
        weights: list[float],
    ) -> Any:
        """
        Return a weighted random item.

        Args:
            options: Available values.
            weights: Probability weights.

        Returns:
            Randomly selected value.
        """

        return self._generator.choices(
            population=options,
            weights=weights,
            k=1,
        )[0]
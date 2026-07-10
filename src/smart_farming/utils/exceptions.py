"""
Custom exception classes for the HydroGrow Smart Farming Simulator.

These exceptions provide meaningful error types that can be handled
throughout the application instead of using generic exceptions.
"""

class SmartFarmingError(Exception):
    """
    Base exception for all Smart Farming simulator erros.
    """

    pass

class ConfigurationError(SmartFarmingError):
    """
    Raised when application configuration is invalid.
    """

    pass

class SimulationError(SmartFarmingError):
    """
    Raised when the simulator encounters an unrecoverable error.
    """

    pass

class GeneratorError(SmartFarmingError):
    """
    Raised when a telemetry generator fails to produce events.
    """

    pass

class ValidationError(SmartFarmingError):
    """
    Raised when event validation fails.
    """

    pass

class DispatchError(SmartFarmingError):
    """
    Raised when an event cannot be dispatched to its destination.
    """

    pass
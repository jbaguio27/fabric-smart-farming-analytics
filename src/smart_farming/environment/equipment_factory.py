"""
Equipment inventory factory.

This module is responsible for constructing the initial equipment
inventory used by the simulator.

Unlike EquipmentRegistry, which stores and retrieves equipment assets,
the EquipmentFactory encapsulates the rules for creating the default
inventory.

Separating construction from storage follows the Single Responsibility
Principle and simplifies future expansion of equipment provisioning
strategies (facility templates, customer-specific layouts, scenario
loading, etc.).
"""

from smart_farming.config import (
    Settings,
    FACILITY_ID_PREFIX,
    ZONE_ID_PREFIX,
    DEFAULT_GROWING_ZONES_PER_FACILITY,
    EQUIPMENT_TYPES,
    EQUIPMENT_ID_PREFIX,
    EQUIPMENT_MANUFACTURERS,
    EQUIPMENT_MODELS,
)
from smart_farming.models import Equipment


class EquipmentFactory:
    """
    Factory responsible for constructing equipment assets.

    The factory contains all business rules related to creating the
    simulator's initial equipment inventory.

    It does not store equipment and performs no lookup operations.
    """

    def __init__(
        self,
        settings: Settings,
    ) -> None:
        """
        Initialize the factory.

        Args:
            settings:
                Simulator configuration.
        """

        self._settings = settings

    def create_inventory(
        self,
    ) -> list[Equipment]:
        """
        Build the simulator's default equipment inventory.

        Returns
        -------
        list[Equipment]
            Fully constructed equipment assets.
        """

        inventory: list[Equipment] = []

        equipment_counter = 1

        for facility_number in range(
            1,
            self._settings.total_facilities + 1,
        ):

            facility_id = (
                f"{FACILITY_ID_PREFIX}-{facility_number:03d}"
            )

            for zone_number in range(
                1,
                DEFAULT_GROWING_ZONES_PER_FACILITY + 1,
            ):

                zone_id = (
                    f"{ZONE_ID_PREFIX}-{zone_number:03d}"
                )

                for equipment_type in EQUIPMENT_TYPES:

                    inventory.append(
                        Equipment(
                            equipment_id=(
                                f"{EQUIPMENT_ID_PREFIX}-{equipment_counter:05d}"
                            ),
                            facility_id=facility_id,
                            zone_id=zone_id,
                            equipment_type=equipment_type,
                            manufacturer=(
                                EQUIPMENT_MANUFACTURERS[equipment_type]
                            ),
                            model=(
                                EQUIPMENT_MODELS[equipment_type]
                            ),
                            serial_number=(
                                f"SN-{equipment_counter:08d}"
                            ),
                        )
                    )

                    equipment_counter += 1

        return inventory
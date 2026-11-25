from enum import StrEnum


class CargoMovementType(StrEnum):
    """Who stuffed the cargo."""

    FCL = "FCL"  # customer stuffed the container
    LCL = "LCL"  # carrier stuffed it with other cargo
    BB = "BB"  # break bulk, not in a container

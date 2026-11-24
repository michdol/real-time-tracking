from enum import StrEnum


class EmptyIndicator(StrEnum):
    """Whether the container is empty or has cargo."""

    EMPTY = "EMPTY"
    LADEN = "LADEN"

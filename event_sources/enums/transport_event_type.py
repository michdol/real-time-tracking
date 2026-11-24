from enum import StrEnum


class TransportEventType(StrEnum):
    """The vehicle moved. The container is named on the event, the vehicle did the moving."""

    ARRI = "ARRI"
    DEPA = "DEPA"

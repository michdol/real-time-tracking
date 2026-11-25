from enum import StrEnum


class EventClassifier(StrEnum):
    """How firm the time on an event is."""

    ACT = "ACT"  # happened
    PLN = "PLN"  # planned
    EST = "EST"  # forecast
    REQ = "REQ"  # requested by the other party

from enum import StrEnum


class ModeOfTransport(StrEnum):
    """How the container is moving. The value is the DCSA word. The comment is the UN/CEFACT code."""

    VESSEL = "VESSEL"  # 1 maritime
    RAIL = "RAIL"  # 2
    TRUCK = "TRUCK"  # 3
    BARGE = "BARGE"  # 8 inland water

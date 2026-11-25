from enum import StrEnum


class ReceiptDeliveryType(StrEnum):
    """Where the carrier takes the cargo and where it gives it back."""

    CY = "CY"  # full container at the terminal or rail ramp
    SD = "SD"  # carrier trucks it to the customer's door
    CFS = "CFS"  # loose cargo at a freight station

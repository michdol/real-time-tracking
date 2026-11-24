from enum import StrEnum


class ShipmentEventType(StrEnum):
    """A document or commercial status. The container has not moved."""

    RECE = "RECE"  # document received
    DRFT = "DRFT"  # draft being edited
    PENA = "PENA"  # waiting for the shipper to approve
    PENU = "PENU"  # waiting for the shipper to update
    PENC = "PENC"  # waiting for the carrier to confirm
    REJE = "REJE"  # carrier rejected the document
    APPR = "APPR"  # counterpart approved it
    ISSU = "ISSU"  # carrier issued it
    SURR = "SURR"  # customer surrendered it
    SUBM = "SUBM"  # customer submitted it
    VOID = "VOID"  # original document cancelled
    CONF = "CONF"  # confirmed
    REQS = "REQS"  # requested, stays until completed
    CMPL = "CMPL"  # requested activity completed
    HOLD = "HOLD"  # shipment or container cannot progress
    RELS = "RELS"  # hold lifted, movement allowed
    CANC = "CANC"  # shipper cancelled the booking

from enum import StrEnum


class EquipmentEventType(StrEnum):
    """What happened to the container."""

    LOAD = "LOAD"  # lifted onto the vehicle and secured
    DISC = "DISC"  # lifted off the vehicle
    GTIN = "GTIN"  # entered a terminal or depot
    GTOT = "GTOT"  # left a terminal or depot
    STUF = "STUF"  # cargo loaded into the container
    STRP = "STRP"  # cargo unloaded from the container
    PICK = "PICK"  # collected at the customer
    DROP = "DROP"  # delivered at the customer
    INSP = "INSP"  # seal inspected
    RSEA = "RSEA"  # resealed after inspection
    RMVD = "RMVD"  # seal removed for inspection
    AVPU = "AVPU"  # ready for pick-up
    AVDO = "AVDO"  # ready for drop-off
    CUSS = "CUSS"  # customs selected it for scan
    CUSI = "CUSI"  # customs selected it for inspection
    CUSR = "CUSR"  # customs released it
    WAYP = "WAYP"  # crossed a waypoint

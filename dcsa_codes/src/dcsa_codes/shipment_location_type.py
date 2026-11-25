from enum import StrEnum


class ShipmentLocationType(StrEnum):
    """The role of a place on the booking. Not the same as facility type."""

    PRE = "PRE"  # place of receipt, line takes the cargo
    POL = "POL"  # port of loading, first sea vessel
    POD = "POD"  # port of discharge, last sea vessel
    PDE = "PDE"  # place of delivery, line hands the cargo over
    PCF = "PCF"  # pre-carriage from
    PSR = "PSR"  # pre-carriage under the shipper
    OIR = "OIR"  # inland routing after the port, consignee's job
    DRL = "DRL"  # depot release location
    ORI = "ORI"  # origin of the goods
    IEL = "IEL"  # intermediate export stop
    PTP = "PTP"  # prohibited transshipment port
    RTP = "RTP"  # requested transshipment port
    FCD = "FCD"  # full container drop-off
    ECP = "ECP"  # empty container pick-up

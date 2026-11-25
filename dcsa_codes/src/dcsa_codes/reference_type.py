from enum import StrEnum


class ReferenceType(StrEnum):
    """An id that is not one of the carrier document types."""

    FF = "FF"  # freight forwarder
    SI = "SI"  # shipper
    PO = "PO"  # purchase order
    CR = "CR"  # customer
    AAO = "AAO"  # consignee
    ECR = "ECR"  # empty container release
    CSI = "CSI"  # customer shipment id
    BPR = "BPR"  # booking party
    BID = "BID"  # booking request id
    EQ = "EQ"  # equipment, the container

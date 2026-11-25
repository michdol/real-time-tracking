from enum import StrEnum


class DocumentType(StrEnum):
    """Which document a reference or a shipment event is about."""

    CBR = "CBR"  # carrier booking request
    BKG = "BKG"  # booking
    SHI = "SHI"  # shipping instruction
    TRD = "TRD"  # transport document, the bill of lading
    DEI = "DEI"  # delivery instructions
    DEO = "DEO"  # delivery order
    TRO = "TRO"  # transport order
    CRO = "CRO"  # container release order
    ARN = "ARN"  # arrival notice
    VGM = "VGM"  # verified gross mass
    CAS = "CAS"  # cargo survey
    CUC = "CUC"  # customs clearance
    DGD = "DGD"  # dangerous goods declaration
    OOG = "OOG"  # out of gauge
    CQU = "CQU"  # contract quotation
    INV = "INV"  # invoice

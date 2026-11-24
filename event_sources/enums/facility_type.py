from enum import StrEnum


class FacilityType(StrEnum):
    """What kind of place the transport call is at."""

    BOCR = "BOCR"  # border crossing
    CLOC = "CLOC"  # customer premises
    COFS = "COFS"  # freight station, LCL stuffing and stripping
    OFFD = "OFFD"  # off-dock storage
    DEPO = "DEPO"  # empty depot
    INTE = "INTE"  # inland terminal
    POTE = "POTE"  # sea terminal
    PBPL = "PBPL"  # pilot boarding place
    BRTH = "BRTH"  # berth
    RAMP = "RAMP"  # rail ramp
    ANCH = "ANCH"  # anchorage

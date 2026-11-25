"""One booking, from confirmation to the empty box back at the depot.

Run from this directory: uv run python order_to_arrival.py

EVENTS is the DCSA shape a normalizer should emit.
NON_DCSA_EVENTS is the same journey in a made-up portal shape.
SEARATES_EVENTS is the same journey in the SeaRates tracking shape.
Same index in each list is the same moment.
"""

import json
from enum import Enum

from dcsa_codes import (
    CargoMovementType,
    DocumentType,
    EmptyIndicator,
    EquipmentEventType,
    EventClassifier,
    FacilityType,
    ModeOfTransport,
    ReceiptDeliveryType,
    ShipmentEventType,
    ShipmentLocationType,
    TransportEventType,
)

BOOKING = "MAEU00000001"
BILL_OF_LADING = "MAEU000000001"
CONTAINER = "MSKU0000006"
ORIGIN = "CNSHA"
DESTINATION = "NLRTM"

EVENTS = [
    (
        "The carrier confirms the booking. The box has not moved. FCL and CY say the customer will deliver a full container to the terminal.",
        {
            "eventType": "SHIPMENT",
            "eventClassifierCode": EventClassifier.ACT,
            "shipmentEventTypeCode": ShipmentEventType.CONF,
            "documentTypeCode": DocumentType.BKG,
            "documentID": BOOKING,
            "cargoMovementType": CargoMovementType.FCL,
            "receiptDeliveryType": ReceiptDeliveryType.CY,
            "shipmentLocations": [
                {"locationType": ShipmentLocationType.POL, "UNLocationCode": ORIGIN},
                {"locationType": ShipmentLocationType.POD, "UNLocationCode": DESTINATION},
                {"locationType": ShipmentLocationType.ECP, "UNLocationCode": ORIGIN},
            ],
        },
    ),
    (
        "The empty container leaves the Shanghai depot on a truck. This is the pick-up named on the booking.",
        {
            "eventType": "EQUIPMENT",
            "eventClassifierCode": EventClassifier.ACT,
            "equipmentEventTypeCode": EquipmentEventType.GTOT,
            "emptyIndicatorCode": EmptyIndicator.EMPTY,
            "equipmentReference": CONTAINER,
            "transportCall": {
                "modeOfTransport": ModeOfTransport.TRUCK,
                "facilityTypeCode": FacilityType.DEPO,
                "UNLocationCode": ORIGIN,
            },
            "documentReferences": [
                {"documentReferenceType": DocumentType.BKG, "documentReferenceValue": BOOKING},
            ],
        },
    ),
    (
        "The shipper has stuffed the container. It is gated into the Shanghai terminal, full.",
        {
            "eventType": "EQUIPMENT",
            "eventClassifierCode": EventClassifier.ACT,
            "equipmentEventTypeCode": EquipmentEventType.GTIN,
            "emptyIndicatorCode": EmptyIndicator.LADEN,
            "equipmentReference": CONTAINER,
            "transportCall": {
                "modeOfTransport": ModeOfTransport.TRUCK,
                "facilityTypeCode": FacilityType.POTE,
                "UNLocationCode": ORIGIN,
            },
            "documentReferences": [
                {"documentReferenceType": DocumentType.BKG, "documentReferenceValue": BOOKING},
            ],
        },
    ),
    (
        "The shipper submits the shipping instruction. This is paperwork, not a move.",
        {
            "eventType": "SHIPMENT",
            "eventClassifierCode": EventClassifier.ACT,
            "shipmentEventTypeCode": ShipmentEventType.SUBM,
            "documentTypeCode": DocumentType.SHI,
            "documentReferences": [
                {"documentReferenceType": DocumentType.BKG, "documentReferenceValue": BOOKING},
            ],
        },
    ),
    (
        "The terminal lifts the full container onto the vessel.",
        {
            "eventType": "EQUIPMENT",
            "eventClassifierCode": EventClassifier.ACT,
            "equipmentEventTypeCode": EquipmentEventType.LOAD,
            "emptyIndicatorCode": EmptyIndicator.LADEN,
            "equipmentReference": CONTAINER,
            "transportCall": {
                "modeOfTransport": ModeOfTransport.VESSEL,
                "facilityTypeCode": FacilityType.POTE,
                "UNLocationCode": ORIGIN,
                "vesselName": "MADRID MAERSK",
                "exportVoyageNumber": "612W",
            },
            "documentReferences": [
                {"documentReferenceType": DocumentType.BKG, "documentReferenceValue": BOOKING},
            ],
        },
    ),
    (
        "The vessel sails from Shanghai. The container is in transit.",
        {
            "eventType": "TRANSPORT",
            "eventClassifierCode": EventClassifier.ACT,
            "transportEventTypeCode": TransportEventType.DEPA,
            "equipmentReference": CONTAINER,
            "transportCall": {
                "modeOfTransport": ModeOfTransport.VESSEL,
                "facilityTypeCode": FacilityType.POTE,
                "UNLocationCode": ORIGIN,
                "vesselName": "MADRID MAERSK",
                "exportVoyageNumber": "612W",
            },
            "documentReferences": [
                {"documentReferenceType": DocumentType.BKG, "documentReferenceValue": BOOKING},
            ],
        },
    ),
    (
        "The carrier issues the bill of lading once the vessel has sailed.",
        {
            "eventType": "SHIPMENT",
            "eventClassifierCode": EventClassifier.ACT,
            "shipmentEventTypeCode": ShipmentEventType.ISSU,
            "documentTypeCode": DocumentType.TRD,
            "documentID": BILL_OF_LADING,
            "documentReferences": [
                {"documentReferenceType": DocumentType.BKG, "documentReferenceValue": BOOKING},
            ],
        },
    ),
    (
        "The vessel berths at Rotterdam. Transit is over. The container is still on board.",
        {
            "eventType": "TRANSPORT",
            "eventClassifierCode": EventClassifier.ACT,
            "transportEventTypeCode": TransportEventType.ARRI,
            "equipmentReference": CONTAINER,
            "transportCall": {
                "modeOfTransport": ModeOfTransport.VESSEL,
                "facilityTypeCode": FacilityType.POTE,
                "UNLocationCode": DESTINATION,
                "vesselName": "MADRID MAERSK",
                "importVoyageNumber": "612W",
            },
            "documentReferences": [
                {"documentReferenceType": DocumentType.BKG, "documentReferenceValue": BOOKING},
                {"documentReferenceType": DocumentType.TRD, "documentReferenceValue": BILL_OF_LADING},
            ],
        },
    ),
    (
        "The terminal lifts the full container off the vessel.",
        {
            "eventType": "EQUIPMENT",
            "eventClassifierCode": EventClassifier.ACT,
            "equipmentEventTypeCode": EquipmentEventType.DISC,
            "emptyIndicatorCode": EmptyIndicator.LADEN,
            "equipmentReference": CONTAINER,
            "transportCall": {
                "modeOfTransport": ModeOfTransport.VESSEL,
                "facilityTypeCode": FacilityType.POTE,
                "UNLocationCode": DESTINATION,
                "vesselName": "MADRID MAERSK",
                "importVoyageNumber": "612W",
            },
            "documentReferences": [
                {"documentReferenceType": DocumentType.BKG, "documentReferenceValue": BOOKING},
                {"documentReferenceType": DocumentType.TRD, "documentReferenceValue": BILL_OF_LADING},
            ],
        },
    ),
    (
        "Customs releases the container. It can leave the terminal.",
        {
            "eventType": "EQUIPMENT",
            "eventClassifierCode": EventClassifier.ACT,
            "equipmentEventTypeCode": EquipmentEventType.CUSR,
            "emptyIndicatorCode": EmptyIndicator.LADEN,
            "equipmentReference": CONTAINER,
            "transportCall": {
                "modeOfTransport": ModeOfTransport.TRUCK,
                "facilityTypeCode": FacilityType.POTE,
                "UNLocationCode": DESTINATION,
            },
            "documentReferences": [
                {"documentReferenceType": DocumentType.TRD, "documentReferenceValue": BILL_OF_LADING},
            ],
        },
    ),
    (
        "The carrier marks the container ready for the client to collect.",
        {
            "eventType": "EQUIPMENT",
            "eventClassifierCode": EventClassifier.ACT,
            "equipmentEventTypeCode": EquipmentEventType.AVPU,
            "emptyIndicatorCode": EmptyIndicator.LADEN,
            "equipmentReference": CONTAINER,
            "transportCall": {
                "modeOfTransport": ModeOfTransport.TRUCK,
                "facilityTypeCode": FacilityType.POTE,
                "UNLocationCode": DESTINATION,
            },
            "shipmentLocationType": ShipmentLocationType.PDE,
            "documentReferences": [
                {"documentReferenceType": DocumentType.BKG, "documentReferenceValue": BOOKING},
            ],
        },
    ),
    (
        "A truck gates the full container out of the Rotterdam terminal.",
        {
            "eventType": "EQUIPMENT",
            "eventClassifierCode": EventClassifier.ACT,
            "equipmentEventTypeCode": EquipmentEventType.GTOT,
            "emptyIndicatorCode": EmptyIndicator.LADEN,
            "equipmentReference": CONTAINER,
            "transportCall": {
                "modeOfTransport": ModeOfTransport.TRUCK,
                "facilityTypeCode": FacilityType.POTE,
                "UNLocationCode": DESTINATION,
            },
            "documentReferences": [
                {"documentReferenceType": DocumentType.BKG, "documentReferenceValue": BOOKING},
            ],
        },
    ),
    (
        "The truck delivers the container at the client's premises.",
        {
            "eventType": "EQUIPMENT",
            "eventClassifierCode": EventClassifier.ACT,
            "equipmentEventTypeCode": EquipmentEventType.DROP,
            "emptyIndicatorCode": EmptyIndicator.LADEN,
            "equipmentReference": CONTAINER,
            "transportCall": {
                "modeOfTransport": ModeOfTransport.TRUCK,
                "facilityTypeCode": FacilityType.CLOC,
                "UNLocationCode": DESTINATION,
            },
            "shipmentLocationType": ShipmentLocationType.PDE,
            "documentReferences": [
                {"documentReferenceType": DocumentType.BKG, "documentReferenceValue": BOOKING},
            ],
        },
    ),
    (
        "The client unloads the cargo. The container is empty.",
        {
            "eventType": "EQUIPMENT",
            "eventClassifierCode": EventClassifier.ACT,
            "equipmentEventTypeCode": EquipmentEventType.STRP,
            "emptyIndicatorCode": EmptyIndicator.EMPTY,
            "equipmentReference": CONTAINER,
            "transportCall": {
                "modeOfTransport": ModeOfTransport.TRUCK,
                "facilityTypeCode": FacilityType.CLOC,
                "UNLocationCode": DESTINATION,
            },
            "documentReferences": [
                {"documentReferenceType": DocumentType.BKG, "documentReferenceValue": BOOKING},
            ],
        },
    ),
    (
        "The empty container is gated back into the Rotterdam depot.",
        {
            "eventType": "EQUIPMENT",
            "eventClassifierCode": EventClassifier.ACT,
            "equipmentEventTypeCode": EquipmentEventType.GTIN,
            "emptyIndicatorCode": EmptyIndicator.EMPTY,
            "equipmentReference": CONTAINER,
            "transportCall": {
                "modeOfTransport": ModeOfTransport.TRUCK,
                "facilityTypeCode": FacilityType.DEPO,
                "UNLocationCode": DESTINATION,
            },
            "documentReferences": [
                {"documentReferenceType": DocumentType.BKG, "documentReferenceValue": BOOKING},
            ],
        },
    ),
    (
        "The carrier completes the booking. The order is closed.",
        {
            "eventType": "SHIPMENT",
            "eventClassifierCode": EventClassifier.ACT,
            "shipmentEventTypeCode": ShipmentEventType.CMPL,
            "documentTypeCode": DocumentType.BKG,
            "documentID": BOOKING,
            "documentReferences": [
                {"documentReferenceType": DocumentType.TRD, "documentReferenceValue": BILL_OF_LADING},
            ],
        },
    ),
]

# Carrier portal feed. Not DCSA. Index matches EVENTS.
NON_DCSA_EVENTS = [
    {
        "statusCode": "BKG_CONF",
        "statusText": "Booking confirmed",
        "bookingNo": BOOKING,
        "containerNo": None,
        "blNo": None,
        "city": "Shanghai",
        "podCity": "Rotterdam",
        "stuffing": "FCL",
        "handover": "CY",
    },
    {
        "statusCode": "EMPTY_OUT",
        "statusText": "Empty container picked up",
        "bookingNo": BOOKING,
        "containerNo": CONTAINER,
        "blNo": None,
        "city": "Shanghai",
        "place": "DEPOT",
        "move": "ROAD",
        "load": "E",
    },
    {
        "statusCode": "GATE_IN_FULL",
        "statusText": "Full container gated in",
        "bookingNo": BOOKING,
        "containerNo": CONTAINER,
        "blNo": None,
        "city": "Shanghai",
        "place": "TERMINAL",
        "move": "ROAD",
        "load": "F",
    },
    {
        "statusCode": "SI_SUBMITTED",
        "statusText": "Shipping instruction submitted",
        "bookingNo": BOOKING,
        "containerNo": CONTAINER,
        "blNo": None,
    },
    {
        "statusCode": "LOADED",
        "statusText": "Loaded on vessel",
        "bookingNo": BOOKING,
        "containerNo": CONTAINER,
        "blNo": None,
        "city": "Shanghai",
        "place": "TERMINAL",
        "move": "SEA",
        "load": "F",
        "vessel": "MADRID MAERSK",
        "voyage": "612W",
    },
    {
        "statusCode": "VESSEL_SAILED",
        "statusText": "Vessel departed",
        "bookingNo": BOOKING,
        "containerNo": CONTAINER,
        "blNo": None,
        "city": "Shanghai",
        "place": "TERMINAL",
        "move": "SEA",
        "vessel": "MADRID MAERSK",
        "voyage": "612W",
    },
    {
        "statusCode": "BL_ISSUED",
        "statusText": "Bill of lading issued",
        "bookingNo": BOOKING,
        "containerNo": CONTAINER,
        "blNo": BILL_OF_LADING,
    },
    {
        "statusCode": "VESSEL_ARRIVED",
        "statusText": "Vessel arrived",
        "bookingNo": BOOKING,
        "containerNo": CONTAINER,
        "blNo": BILL_OF_LADING,
        "city": "Rotterdam",
        "place": "TERMINAL",
        "move": "SEA",
        "vessel": "MADRID MAERSK",
        "voyage": "612W",
    },
    {
        "statusCode": "UNLOADED",
        "statusText": "Discharged from vessel",
        "bookingNo": BOOKING,
        "containerNo": CONTAINER,
        "blNo": BILL_OF_LADING,
        "city": "Rotterdam",
        "place": "TERMINAL",
        "move": "SEA",
        "load": "F",
        "vessel": "MADRID MAERSK",
        "voyage": "612W",
    },
    {
        "statusCode": "CUSTOMS_OK",
        "statusText": "Customs released",
        "bookingNo": BOOKING,
        "containerNo": CONTAINER,
        "blNo": BILL_OF_LADING,
        "city": "Rotterdam",
        "place": "TERMINAL",
        "load": "F",
    },
    {
        "statusCode": "READY_FOR_PICKUP",
        "statusText": "Available for pickup",
        "bookingNo": BOOKING,
        "containerNo": CONTAINER,
        "blNo": BILL_OF_LADING,
        "city": "Rotterdam",
        "place": "TERMINAL",
        "move": "ROAD",
        "load": "F",
    },
    {
        "statusCode": "GATE_OUT_FULL",
        "statusText": "Full container gated out",
        "bookingNo": BOOKING,
        "containerNo": CONTAINER,
        "blNo": BILL_OF_LADING,
        "city": "Rotterdam",
        "place": "TERMINAL",
        "move": "ROAD",
        "load": "F",
    },
    {
        "statusCode": "DELIVERED",
        "statusText": "Delivered to customer",
        "bookingNo": BOOKING,
        "containerNo": CONTAINER,
        "blNo": BILL_OF_LADING,
        "city": "Rotterdam",
        "place": "CUSTOMER",
        "move": "ROAD",
        "load": "F",
    },
    {
        "statusCode": "CARGO_UNLOADED",
        "statusText": "Cargo stripped",
        "bookingNo": BOOKING,
        "containerNo": CONTAINER,
        "blNo": BILL_OF_LADING,
        "city": "Rotterdam",
        "place": "CUSTOMER",
        "load": "E",
    },
    {
        "statusCode": "EMPTY_IN",
        "statusText": "Empty container returned",
        "bookingNo": BOOKING,
        "containerNo": CONTAINER,
        "blNo": BILL_OF_LADING,
        "city": "Rotterdam",
        "place": "DEPOT",
        "move": "ROAD",
        "load": "E",
    },
    {
        "statusCode": "BOOKING_CLOSED",
        "statusText": "Booking completed",
        "bookingNo": BOOKING,
        "containerNo": CONTAINER,
        "blNo": BILL_OF_LADING,
    },
]

# SeaRates tracking v2. location is an id into SEARATES_POINTS.
# type 4 is a land move, type 3 is a vessel move, as in their published example.
# https://docs.searates.com/reference/tracking/v2/response-statuses
SEARATES_POINTS = [
    {"id": 1, "name": "Shanghai", "country": "CN", "code5": "CNSHA"},
    {"id": 2, "name": "Rotterdam", "country": "NL", "code5": "NLRTM"},
]
SEARATES_EVENTS = [
    {"date": 1775008800, "location": 1, "description": "Booking confirmed", "type": None, "vessel": None, "voyage": None},
    {"date": 1775091600, "location": 1, "description": "Gate out empty", "type": 4, "vessel": None, "voyage": None},
    {"date": 1775286000, "location": 1, "description": "Arrival in", "type": 4, "vessel": None, "voyage": None},
    {"date": 1775354400, "location": 1, "description": "Shipping instruction submitted", "type": None, "vessel": None, "voyage": None},
    {"date": 1775437200, "location": 1, "description": "Loaded", "type": 3, "vessel": "MADRID MAERSK", "voyage": "612W"},
    {"date": 1775473200, "location": 1, "description": "Vessel departed", "type": 3, "vessel": "MADRID MAERSK", "voyage": "612W"},
    {"date": 1775476800, "location": 1, "description": "Bill of lading issued", "type": None, "vessel": None, "voyage": None},
    {"date": 1778238000, "location": 2, "description": "Vessel arrival", "type": 3, "vessel": "MADRID MAERSK", "voyage": "612W"},
    {"date": 1778266800, "location": 2, "description": "Discharged", "type": 3, "vessel": "MADRID MAERSK", "voyage": "612W"},
    {"date": 1778313600, "location": 2, "description": "Customs release", "type": 4, "vessel": None, "voyage": None},
    {"date": 1778320800, "location": 2, "description": "Available for pickup", "type": 4, "vessel": None, "voyage": None},
    {"date": 1778403600, "location": 2, "description": "Gate out", "type": 4, "vessel": None, "voyage": None},
    {"date": 1778421600, "location": 2, "description": "Delivered", "type": 4, "vessel": None, "voyage": None},
    {"date": 1778576400, "location": 2, "description": "Stripped", "type": 4, "vessel": None, "voyage": None},
    {"date": 1778745600, "location": 2, "description": "Empty container return", "type": 4, "vessel": None, "voyage": None},
    {"date": 1778774400, "location": 2, "description": "Booking completed", "type": None, "vessel": None, "voyage": None},
]


def _plain(value):
    if isinstance(value, Enum):
        return value.value
    if isinstance(value, dict):
        return {key: _plain(item) for key, item in value.items()}
    if isinstance(value, list):
        return [_plain(item) for item in value]
    return value


def main() -> None:
    payload = {
        "input": NON_DCSA_EVENTS,
        "searates": {"points": SEARATES_POINTS, "events": SEARATES_EVENTS},
        "output": [{"what": text, "event": _plain(event)} for text, event in EVENTS],
    }
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()

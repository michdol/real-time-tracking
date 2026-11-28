from datetime import datetime

from event_schemas.event_pb2 import (
    ShipmentEvent,
    EventEnvelope,
    DocumentType,
    EventClassifier,
    ShipmentEventType,
    Reference,
)


def normalize(raw_event: dict) -> EventEnvelope:
    payload = None
    if raw_event["type"] == "Register Customer Order":
        payload = _carrier_booking_request(raw_event)

    event = EventEnvelope(
        raw_event["id"],
        event_date_time=raw_event["time"],
        event_created_date_time=datetime.now(),
        shipment_event=payload,
    )
    return event


def _carrier_booking_request(raw_event: dict) -> ShipmentEvent:
    order_id = [
        r["objectId"]
        for r in raw_event["relationships"]
        if r["qualifier"] == "registered CO"
    ][0]

    shipment_event = ShipmentEvent(
        event_classifier=EventClassifier.EVENT_CLASSIFIER_ACT,
        shipment_event_type=ShipmentEventType.SHIPMENT_EVENT_TYPE_RECE,
        document_type=DocumentType.DOCUMENT_TYPE_CBR,
        document_id=order_id,
        references=[Reference(reference_type="PO", reference_value=order_id)],
    )
    return shipment_event


{
    "eventID": "reg_co2",
    "eventType": "SHIPMENT",
    "eventDateTime": "2023-05-22T18:33:30.000Z",
    "eventClassifierCode": "ACT",
    "shipmentEventTypeCode": "RECE",
    "documentTypeCode": "CBR",
    "documentID": "co2",
    "references": [{"referenceType": "PO", "referenceValue": "co2"}],
}

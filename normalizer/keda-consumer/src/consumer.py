from typing import Any

from event_schemas import ShipmentEvent
from event_schemas.event_pb2 import DocumentType, EventClassifier, ShipmentEventType


def normalize(raw_event: dict[str, Any]):
    event = ShipmentEvent(
        event_classifier=EventClassifier.EVENT_CLASSIFIER_ACT,
        shipment_event_type=ShipmentEventType.SHIPMENT_EVENT_TYPE_CONF,
        document_type=DocumentType.DOCUMENT_TYPE_BKG,
        document_id="MAEU00000001",
    )
    print(event)

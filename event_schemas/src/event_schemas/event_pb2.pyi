import datetime

from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class EventClassifier(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    EVENT_CLASSIFIER_UNSPECIFIED: _ClassVar[EventClassifier]
    EVENT_CLASSIFIER_ACT: _ClassVar[EventClassifier]
    EVENT_CLASSIFIER_PLN: _ClassVar[EventClassifier]
    EVENT_CLASSIFIER_EST: _ClassVar[EventClassifier]
    EVENT_CLASSIFIER_REQ: _ClassVar[EventClassifier]

class ShipmentEventType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SHIPMENT_EVENT_TYPE_UNSPECIFIED: _ClassVar[ShipmentEventType]
    SHIPMENT_EVENT_TYPE_RECE: _ClassVar[ShipmentEventType]
    SHIPMENT_EVENT_TYPE_DRFT: _ClassVar[ShipmentEventType]
    SHIPMENT_EVENT_TYPE_PENA: _ClassVar[ShipmentEventType]
    SHIPMENT_EVENT_TYPE_PENU: _ClassVar[ShipmentEventType]
    SHIPMENT_EVENT_TYPE_PENC: _ClassVar[ShipmentEventType]
    SHIPMENT_EVENT_TYPE_REJE: _ClassVar[ShipmentEventType]
    SHIPMENT_EVENT_TYPE_APPR: _ClassVar[ShipmentEventType]
    SHIPMENT_EVENT_TYPE_ISSU: _ClassVar[ShipmentEventType]
    SHIPMENT_EVENT_TYPE_SURR: _ClassVar[ShipmentEventType]
    SHIPMENT_EVENT_TYPE_SUBM: _ClassVar[ShipmentEventType]
    SHIPMENT_EVENT_TYPE_VOID: _ClassVar[ShipmentEventType]
    SHIPMENT_EVENT_TYPE_CONF: _ClassVar[ShipmentEventType]
    SHIPMENT_EVENT_TYPE_REQS: _ClassVar[ShipmentEventType]
    SHIPMENT_EVENT_TYPE_CMPL: _ClassVar[ShipmentEventType]
    SHIPMENT_EVENT_TYPE_HOLD: _ClassVar[ShipmentEventType]
    SHIPMENT_EVENT_TYPE_RELS: _ClassVar[ShipmentEventType]
    SHIPMENT_EVENT_TYPE_CANC: _ClassVar[ShipmentEventType]

class DocumentType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    DOCUMENT_TYPE_UNSPECIFIED: _ClassVar[DocumentType]
    DOCUMENT_TYPE_CBR: _ClassVar[DocumentType]
    DOCUMENT_TYPE_BKG: _ClassVar[DocumentType]
    DOCUMENT_TYPE_SHI: _ClassVar[DocumentType]
    DOCUMENT_TYPE_TRD: _ClassVar[DocumentType]
    DOCUMENT_TYPE_DEI: _ClassVar[DocumentType]
    DOCUMENT_TYPE_DEO: _ClassVar[DocumentType]
    DOCUMENT_TYPE_TRO: _ClassVar[DocumentType]
    DOCUMENT_TYPE_CRO: _ClassVar[DocumentType]
    DOCUMENT_TYPE_ARN: _ClassVar[DocumentType]
    DOCUMENT_TYPE_VGM: _ClassVar[DocumentType]
    DOCUMENT_TYPE_CAS: _ClassVar[DocumentType]
    DOCUMENT_TYPE_CUC: _ClassVar[DocumentType]
    DOCUMENT_TYPE_DGD: _ClassVar[DocumentType]
    DOCUMENT_TYPE_OOG: _ClassVar[DocumentType]
    DOCUMENT_TYPE_CQU: _ClassVar[DocumentType]
    DOCUMENT_TYPE_INV: _ClassVar[DocumentType]

class CargoMovementType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    CARGO_MOVEMENT_TYPE_UNSPECIFIED: _ClassVar[CargoMovementType]
    CARGO_MOVEMENT_TYPE_FCL: _ClassVar[CargoMovementType]
    CARGO_MOVEMENT_TYPE_LCL: _ClassVar[CargoMovementType]
    CARGO_MOVEMENT_TYPE_BB: _ClassVar[CargoMovementType]

class ReceiptDeliveryType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    RECEIPT_DELIVERY_TYPE_UNSPECIFIED: _ClassVar[ReceiptDeliveryType]
    RECEIPT_DELIVERY_TYPE_CY: _ClassVar[ReceiptDeliveryType]
    RECEIPT_DELIVERY_TYPE_SD: _ClassVar[ReceiptDeliveryType]
    RECEIPT_DELIVERY_TYPE_CFS: _ClassVar[ReceiptDeliveryType]

class ShipmentLocationType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SHIPMENT_LOCATION_TYPE_UNSPECIFIED: _ClassVar[ShipmentLocationType]
    SHIPMENT_LOCATION_TYPE_PRE: _ClassVar[ShipmentLocationType]
    SHIPMENT_LOCATION_TYPE_POL: _ClassVar[ShipmentLocationType]
    SHIPMENT_LOCATION_TYPE_POD: _ClassVar[ShipmentLocationType]
    SHIPMENT_LOCATION_TYPE_PDE: _ClassVar[ShipmentLocationType]
    SHIPMENT_LOCATION_TYPE_PCF: _ClassVar[ShipmentLocationType]
    SHIPMENT_LOCATION_TYPE_PSR: _ClassVar[ShipmentLocationType]
    SHIPMENT_LOCATION_TYPE_OIR: _ClassVar[ShipmentLocationType]
    SHIPMENT_LOCATION_TYPE_DRL: _ClassVar[ShipmentLocationType]
    SHIPMENT_LOCATION_TYPE_ORI: _ClassVar[ShipmentLocationType]
    SHIPMENT_LOCATION_TYPE_IEL: _ClassVar[ShipmentLocationType]
    SHIPMENT_LOCATION_TYPE_PTP: _ClassVar[ShipmentLocationType]
    SHIPMENT_LOCATION_TYPE_RTP: _ClassVar[ShipmentLocationType]
    SHIPMENT_LOCATION_TYPE_FCD: _ClassVar[ShipmentLocationType]
    SHIPMENT_LOCATION_TYPE_ECP: _ClassVar[ShipmentLocationType]

class EquipmentEventType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    EQUIPMENT_EVENT_TYPE_UNSPECIFIED: _ClassVar[EquipmentEventType]
    EQUIPMENT_EVENT_TYPE_LOAD: _ClassVar[EquipmentEventType]
    EQUIPMENT_EVENT_TYPE_DISC: _ClassVar[EquipmentEventType]
    EQUIPMENT_EVENT_TYPE_GTIN: _ClassVar[EquipmentEventType]
    EQUIPMENT_EVENT_TYPE_GTOT: _ClassVar[EquipmentEventType]
    EQUIPMENT_EVENT_TYPE_STUF: _ClassVar[EquipmentEventType]
    EQUIPMENT_EVENT_TYPE_STRP: _ClassVar[EquipmentEventType]
    EQUIPMENT_EVENT_TYPE_PICK: _ClassVar[EquipmentEventType]
    EQUIPMENT_EVENT_TYPE_DROP: _ClassVar[EquipmentEventType]
    EQUIPMENT_EVENT_TYPE_INSP: _ClassVar[EquipmentEventType]
    EQUIPMENT_EVENT_TYPE_RSEA: _ClassVar[EquipmentEventType]
    EQUIPMENT_EVENT_TYPE_RMVD: _ClassVar[EquipmentEventType]
    EQUIPMENT_EVENT_TYPE_AVPU: _ClassVar[EquipmentEventType]
    EQUIPMENT_EVENT_TYPE_AVDO: _ClassVar[EquipmentEventType]
    EQUIPMENT_EVENT_TYPE_CUSS: _ClassVar[EquipmentEventType]
    EQUIPMENT_EVENT_TYPE_CUSI: _ClassVar[EquipmentEventType]
    EQUIPMENT_EVENT_TYPE_CUSR: _ClassVar[EquipmentEventType]
    EQUIPMENT_EVENT_TYPE_WAYP: _ClassVar[EquipmentEventType]

class EmptyIndicator(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    EMPTY_INDICATOR_UNSPECIFIED: _ClassVar[EmptyIndicator]
    EMPTY_INDICATOR_EMPTY: _ClassVar[EmptyIndicator]
    EMPTY_INDICATOR_LADEN: _ClassVar[EmptyIndicator]

class TransportEventType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    TRANSPORT_EVENT_TYPE_UNSPECIFIED: _ClassVar[TransportEventType]
    TRANSPORT_EVENT_TYPE_ARRI: _ClassVar[TransportEventType]
    TRANSPORT_EVENT_TYPE_DEPA: _ClassVar[TransportEventType]

class ModeOfTransport(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    MODE_OF_TRANSPORT_UNSPECIFIED: _ClassVar[ModeOfTransport]
    MODE_OF_TRANSPORT_VESSEL: _ClassVar[ModeOfTransport]
    MODE_OF_TRANSPORT_RAIL: _ClassVar[ModeOfTransport]
    MODE_OF_TRANSPORT_TRUCK: _ClassVar[ModeOfTransport]
    MODE_OF_TRANSPORT_BARGE: _ClassVar[ModeOfTransport]

class FacilityType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    FACILITY_TYPE_UNSPECIFIED: _ClassVar[FacilityType]
    FACILITY_TYPE_BOCR: _ClassVar[FacilityType]
    FACILITY_TYPE_CLOC: _ClassVar[FacilityType]
    FACILITY_TYPE_COFS: _ClassVar[FacilityType]
    FACILITY_TYPE_OFFD: _ClassVar[FacilityType]
    FACILITY_TYPE_DEPO: _ClassVar[FacilityType]
    FACILITY_TYPE_INTE: _ClassVar[FacilityType]
    FACILITY_TYPE_POTE: _ClassVar[FacilityType]
    FACILITY_TYPE_PBPL: _ClassVar[FacilityType]
    FACILITY_TYPE_BRTH: _ClassVar[FacilityType]
    FACILITY_TYPE_RAMP: _ClassVar[FacilityType]
    FACILITY_TYPE_ANCH: _ClassVar[FacilityType]

class ReferenceType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    REFERENCE_TYPE_UNSPECIFIED: _ClassVar[ReferenceType]
    REFERENCE_TYPE_FF: _ClassVar[ReferenceType]
    REFERENCE_TYPE_SI: _ClassVar[ReferenceType]
    REFERENCE_TYPE_PO: _ClassVar[ReferenceType]
    REFERENCE_TYPE_CR: _ClassVar[ReferenceType]
    REFERENCE_TYPE_AAO: _ClassVar[ReferenceType]
    REFERENCE_TYPE_ECR: _ClassVar[ReferenceType]
    REFERENCE_TYPE_CSI: _ClassVar[ReferenceType]
    REFERENCE_TYPE_BPR: _ClassVar[ReferenceType]
    REFERENCE_TYPE_BID: _ClassVar[ReferenceType]
    REFERENCE_TYPE_EQ: _ClassVar[ReferenceType]
EVENT_CLASSIFIER_UNSPECIFIED: EventClassifier
EVENT_CLASSIFIER_ACT: EventClassifier
EVENT_CLASSIFIER_PLN: EventClassifier
EVENT_CLASSIFIER_EST: EventClassifier
EVENT_CLASSIFIER_REQ: EventClassifier
SHIPMENT_EVENT_TYPE_UNSPECIFIED: ShipmentEventType
SHIPMENT_EVENT_TYPE_RECE: ShipmentEventType
SHIPMENT_EVENT_TYPE_DRFT: ShipmentEventType
SHIPMENT_EVENT_TYPE_PENA: ShipmentEventType
SHIPMENT_EVENT_TYPE_PENU: ShipmentEventType
SHIPMENT_EVENT_TYPE_PENC: ShipmentEventType
SHIPMENT_EVENT_TYPE_REJE: ShipmentEventType
SHIPMENT_EVENT_TYPE_APPR: ShipmentEventType
SHIPMENT_EVENT_TYPE_ISSU: ShipmentEventType
SHIPMENT_EVENT_TYPE_SURR: ShipmentEventType
SHIPMENT_EVENT_TYPE_SUBM: ShipmentEventType
SHIPMENT_EVENT_TYPE_VOID: ShipmentEventType
SHIPMENT_EVENT_TYPE_CONF: ShipmentEventType
SHIPMENT_EVENT_TYPE_REQS: ShipmentEventType
SHIPMENT_EVENT_TYPE_CMPL: ShipmentEventType
SHIPMENT_EVENT_TYPE_HOLD: ShipmentEventType
SHIPMENT_EVENT_TYPE_RELS: ShipmentEventType
SHIPMENT_EVENT_TYPE_CANC: ShipmentEventType
DOCUMENT_TYPE_UNSPECIFIED: DocumentType
DOCUMENT_TYPE_CBR: DocumentType
DOCUMENT_TYPE_BKG: DocumentType
DOCUMENT_TYPE_SHI: DocumentType
DOCUMENT_TYPE_TRD: DocumentType
DOCUMENT_TYPE_DEI: DocumentType
DOCUMENT_TYPE_DEO: DocumentType
DOCUMENT_TYPE_TRO: DocumentType
DOCUMENT_TYPE_CRO: DocumentType
DOCUMENT_TYPE_ARN: DocumentType
DOCUMENT_TYPE_VGM: DocumentType
DOCUMENT_TYPE_CAS: DocumentType
DOCUMENT_TYPE_CUC: DocumentType
DOCUMENT_TYPE_DGD: DocumentType
DOCUMENT_TYPE_OOG: DocumentType
DOCUMENT_TYPE_CQU: DocumentType
DOCUMENT_TYPE_INV: DocumentType
CARGO_MOVEMENT_TYPE_UNSPECIFIED: CargoMovementType
CARGO_MOVEMENT_TYPE_FCL: CargoMovementType
CARGO_MOVEMENT_TYPE_LCL: CargoMovementType
CARGO_MOVEMENT_TYPE_BB: CargoMovementType
RECEIPT_DELIVERY_TYPE_UNSPECIFIED: ReceiptDeliveryType
RECEIPT_DELIVERY_TYPE_CY: ReceiptDeliveryType
RECEIPT_DELIVERY_TYPE_SD: ReceiptDeliveryType
RECEIPT_DELIVERY_TYPE_CFS: ReceiptDeliveryType
SHIPMENT_LOCATION_TYPE_UNSPECIFIED: ShipmentLocationType
SHIPMENT_LOCATION_TYPE_PRE: ShipmentLocationType
SHIPMENT_LOCATION_TYPE_POL: ShipmentLocationType
SHIPMENT_LOCATION_TYPE_POD: ShipmentLocationType
SHIPMENT_LOCATION_TYPE_PDE: ShipmentLocationType
SHIPMENT_LOCATION_TYPE_PCF: ShipmentLocationType
SHIPMENT_LOCATION_TYPE_PSR: ShipmentLocationType
SHIPMENT_LOCATION_TYPE_OIR: ShipmentLocationType
SHIPMENT_LOCATION_TYPE_DRL: ShipmentLocationType
SHIPMENT_LOCATION_TYPE_ORI: ShipmentLocationType
SHIPMENT_LOCATION_TYPE_IEL: ShipmentLocationType
SHIPMENT_LOCATION_TYPE_PTP: ShipmentLocationType
SHIPMENT_LOCATION_TYPE_RTP: ShipmentLocationType
SHIPMENT_LOCATION_TYPE_FCD: ShipmentLocationType
SHIPMENT_LOCATION_TYPE_ECP: ShipmentLocationType
EQUIPMENT_EVENT_TYPE_UNSPECIFIED: EquipmentEventType
EQUIPMENT_EVENT_TYPE_LOAD: EquipmentEventType
EQUIPMENT_EVENT_TYPE_DISC: EquipmentEventType
EQUIPMENT_EVENT_TYPE_GTIN: EquipmentEventType
EQUIPMENT_EVENT_TYPE_GTOT: EquipmentEventType
EQUIPMENT_EVENT_TYPE_STUF: EquipmentEventType
EQUIPMENT_EVENT_TYPE_STRP: EquipmentEventType
EQUIPMENT_EVENT_TYPE_PICK: EquipmentEventType
EQUIPMENT_EVENT_TYPE_DROP: EquipmentEventType
EQUIPMENT_EVENT_TYPE_INSP: EquipmentEventType
EQUIPMENT_EVENT_TYPE_RSEA: EquipmentEventType
EQUIPMENT_EVENT_TYPE_RMVD: EquipmentEventType
EQUIPMENT_EVENT_TYPE_AVPU: EquipmentEventType
EQUIPMENT_EVENT_TYPE_AVDO: EquipmentEventType
EQUIPMENT_EVENT_TYPE_CUSS: EquipmentEventType
EQUIPMENT_EVENT_TYPE_CUSI: EquipmentEventType
EQUIPMENT_EVENT_TYPE_CUSR: EquipmentEventType
EQUIPMENT_EVENT_TYPE_WAYP: EquipmentEventType
EMPTY_INDICATOR_UNSPECIFIED: EmptyIndicator
EMPTY_INDICATOR_EMPTY: EmptyIndicator
EMPTY_INDICATOR_LADEN: EmptyIndicator
TRANSPORT_EVENT_TYPE_UNSPECIFIED: TransportEventType
TRANSPORT_EVENT_TYPE_ARRI: TransportEventType
TRANSPORT_EVENT_TYPE_DEPA: TransportEventType
MODE_OF_TRANSPORT_UNSPECIFIED: ModeOfTransport
MODE_OF_TRANSPORT_VESSEL: ModeOfTransport
MODE_OF_TRANSPORT_RAIL: ModeOfTransport
MODE_OF_TRANSPORT_TRUCK: ModeOfTransport
MODE_OF_TRANSPORT_BARGE: ModeOfTransport
FACILITY_TYPE_UNSPECIFIED: FacilityType
FACILITY_TYPE_BOCR: FacilityType
FACILITY_TYPE_CLOC: FacilityType
FACILITY_TYPE_COFS: FacilityType
FACILITY_TYPE_OFFD: FacilityType
FACILITY_TYPE_DEPO: FacilityType
FACILITY_TYPE_INTE: FacilityType
FACILITY_TYPE_POTE: FacilityType
FACILITY_TYPE_PBPL: FacilityType
FACILITY_TYPE_BRTH: FacilityType
FACILITY_TYPE_RAMP: FacilityType
FACILITY_TYPE_ANCH: FacilityType
REFERENCE_TYPE_UNSPECIFIED: ReferenceType
REFERENCE_TYPE_FF: ReferenceType
REFERENCE_TYPE_SI: ReferenceType
REFERENCE_TYPE_PO: ReferenceType
REFERENCE_TYPE_CR: ReferenceType
REFERENCE_TYPE_AAO: ReferenceType
REFERENCE_TYPE_ECR: ReferenceType
REFERENCE_TYPE_CSI: ReferenceType
REFERENCE_TYPE_BPR: ReferenceType
REFERENCE_TYPE_BID: ReferenceType
REFERENCE_TYPE_EQ: ReferenceType

class EventEnvelope(_message.Message):
    __slots__ = ("event_id", "event_date_time", "event_created_date_time", "retracted_event_id", "shipment_event", "equipment_event", "transport_event")
    EVENT_ID_FIELD_NUMBER: _ClassVar[int]
    EVENT_DATE_TIME_FIELD_NUMBER: _ClassVar[int]
    EVENT_CREATED_DATE_TIME_FIELD_NUMBER: _ClassVar[int]
    RETRACTED_EVENT_ID_FIELD_NUMBER: _ClassVar[int]
    SHIPMENT_EVENT_FIELD_NUMBER: _ClassVar[int]
    EQUIPMENT_EVENT_FIELD_NUMBER: _ClassVar[int]
    TRANSPORT_EVENT_FIELD_NUMBER: _ClassVar[int]
    event_id: str
    event_date_time: _timestamp_pb2.Timestamp
    event_created_date_time: _timestamp_pb2.Timestamp
    retracted_event_id: str
    shipment_event: ShipmentEvent
    equipment_event: EquipmentEvent
    transport_event: TransportEvent
    def __init__(self, event_id: _Optional[str] = ..., event_date_time: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., event_created_date_time: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., retracted_event_id: _Optional[str] = ..., shipment_event: _Optional[_Union[ShipmentEvent, _Mapping]] = ..., equipment_event: _Optional[_Union[EquipmentEvent, _Mapping]] = ..., transport_event: _Optional[_Union[TransportEvent, _Mapping]] = ...) -> None: ...

class Reference(_message.Message):
    __slots__ = ("reference_type", "reference_value")
    REFERENCE_TYPE_FIELD_NUMBER: _ClassVar[int]
    REFERENCE_VALUE_FIELD_NUMBER: _ClassVar[int]
    reference_type: ReferenceType
    reference_value: str
    def __init__(self, reference_type: _Optional[_Union[ReferenceType, str]] = ..., reference_value: _Optional[str] = ...) -> None: ...

class ShipmentLocation(_message.Message):
    __slots__ = ("location_type", "un_location_code")
    LOCATION_TYPE_FIELD_NUMBER: _ClassVar[int]
    UN_LOCATION_CODE_FIELD_NUMBER: _ClassVar[int]
    location_type: ShipmentLocationType
    un_location_code: str
    def __init__(self, location_type: _Optional[_Union[ShipmentLocationType, str]] = ..., un_location_code: _Optional[str] = ...) -> None: ...

class DocumentReference(_message.Message):
    __slots__ = ("document_type", "document_value")
    DOCUMENT_TYPE_FIELD_NUMBER: _ClassVar[int]
    DOCUMENT_VALUE_FIELD_NUMBER: _ClassVar[int]
    document_type: DocumentType
    document_value: str
    def __init__(self, document_type: _Optional[_Union[DocumentType, str]] = ..., document_value: _Optional[str] = ...) -> None: ...

class ShipmentEvent(_message.Message):
    __slots__ = ("event_classifier", "shipment_event_type", "document_type", "document_id", "cargo_movement", "receipt_delivery", "shipment_locations", "document_references", "references")
    EVENT_CLASSIFIER_FIELD_NUMBER: _ClassVar[int]
    SHIPMENT_EVENT_TYPE_FIELD_NUMBER: _ClassVar[int]
    DOCUMENT_TYPE_FIELD_NUMBER: _ClassVar[int]
    DOCUMENT_ID_FIELD_NUMBER: _ClassVar[int]
    CARGO_MOVEMENT_FIELD_NUMBER: _ClassVar[int]
    RECEIPT_DELIVERY_FIELD_NUMBER: _ClassVar[int]
    SHIPMENT_LOCATIONS_FIELD_NUMBER: _ClassVar[int]
    DOCUMENT_REFERENCES_FIELD_NUMBER: _ClassVar[int]
    REFERENCES_FIELD_NUMBER: _ClassVar[int]
    event_classifier: EventClassifier
    shipment_event_type: ShipmentEventType
    document_type: DocumentType
    document_id: str
    cargo_movement: CargoMovementType
    receipt_delivery: ReceiptDeliveryType
    shipment_locations: _containers.RepeatedCompositeFieldContainer[ShipmentLocation]
    document_references: _containers.RepeatedCompositeFieldContainer[DocumentReference]
    references: _containers.RepeatedCompositeFieldContainer[Reference]
    def __init__(self, event_classifier: _Optional[_Union[EventClassifier, str]] = ..., shipment_event_type: _Optional[_Union[ShipmentEventType, str]] = ..., document_type: _Optional[_Union[DocumentType, str]] = ..., document_id: _Optional[str] = ..., cargo_movement: _Optional[_Union[CargoMovementType, str]] = ..., receipt_delivery: _Optional[_Union[ReceiptDeliveryType, str]] = ..., shipment_locations: _Optional[_Iterable[_Union[ShipmentLocation, _Mapping]]] = ..., document_references: _Optional[_Iterable[_Union[DocumentReference, _Mapping]]] = ..., references: _Optional[_Iterable[_Union[Reference, _Mapping]]] = ...) -> None: ...

class EquipmentEvent(_message.Message):
    __slots__ = ("event_classifier", "equipment_event_type", "empty_indicator", "equipment_reference", "transport_call", "document_references")
    EVENT_CLASSIFIER_FIELD_NUMBER: _ClassVar[int]
    EQUIPMENT_EVENT_TYPE_FIELD_NUMBER: _ClassVar[int]
    EMPTY_INDICATOR_FIELD_NUMBER: _ClassVar[int]
    EQUIPMENT_REFERENCE_FIELD_NUMBER: _ClassVar[int]
    TRANSPORT_CALL_FIELD_NUMBER: _ClassVar[int]
    DOCUMENT_REFERENCES_FIELD_NUMBER: _ClassVar[int]
    event_classifier: EventClassifier
    equipment_event_type: EquipmentEventType
    empty_indicator: EmptyIndicator
    equipment_reference: str
    transport_call: TransportCall
    document_references: _containers.RepeatedCompositeFieldContainer[DocumentReference]
    def __init__(self, event_classifier: _Optional[_Union[EventClassifier, str]] = ..., equipment_event_type: _Optional[_Union[EquipmentEventType, str]] = ..., empty_indicator: _Optional[_Union[EmptyIndicator, str]] = ..., equipment_reference: _Optional[str] = ..., transport_call: _Optional[_Union[TransportCall, _Mapping]] = ..., document_references: _Optional[_Iterable[_Union[DocumentReference, _Mapping]]] = ...) -> None: ...

class TransportEvent(_message.Message):
    __slots__ = ("event_classifier", "transport_event_type", "equipment_reference", "transport_call", "document_references")
    EVENT_CLASSIFIER_FIELD_NUMBER: _ClassVar[int]
    TRANSPORT_EVENT_TYPE_FIELD_NUMBER: _ClassVar[int]
    EQUIPMENT_REFERENCE_FIELD_NUMBER: _ClassVar[int]
    TRANSPORT_CALL_FIELD_NUMBER: _ClassVar[int]
    DOCUMENT_REFERENCES_FIELD_NUMBER: _ClassVar[int]
    event_classifier: EventClassifier
    transport_event_type: TransportEventType
    equipment_reference: str
    transport_call: TransportCall
    document_references: _containers.RepeatedCompositeFieldContainer[DocumentReference]
    def __init__(self, event_classifier: _Optional[_Union[EventClassifier, str]] = ..., transport_event_type: _Optional[_Union[TransportEventType, str]] = ..., equipment_reference: _Optional[str] = ..., transport_call: _Optional[_Union[TransportCall, _Mapping]] = ..., document_references: _Optional[_Iterable[_Union[DocumentReference, _Mapping]]] = ...) -> None: ...

class TransportCall(_message.Message):
    __slots__ = ("mode_of_transport", "facility_type", "un_location_code", "vessel_name", "export_voyage_number", "import_voyage_number")
    MODE_OF_TRANSPORT_FIELD_NUMBER: _ClassVar[int]
    FACILITY_TYPE_FIELD_NUMBER: _ClassVar[int]
    UN_LOCATION_CODE_FIELD_NUMBER: _ClassVar[int]
    VESSEL_NAME_FIELD_NUMBER: _ClassVar[int]
    EXPORT_VOYAGE_NUMBER_FIELD_NUMBER: _ClassVar[int]
    IMPORT_VOYAGE_NUMBER_FIELD_NUMBER: _ClassVar[int]
    mode_of_transport: ModeOfTransport
    facility_type: FacilityType
    un_location_code: str
    vessel_name: str
    export_voyage_number: str
    import_voyage_number: str
    def __init__(self, mode_of_transport: _Optional[_Union[ModeOfTransport, str]] = ..., facility_type: _Optional[_Union[FacilityType, str]] = ..., un_location_code: _Optional[str] = ..., vessel_name: _Optional[str] = ..., export_voyage_number: _Optional[str] = ..., import_voyage_number: _Optional[str] = ...) -> None: ...

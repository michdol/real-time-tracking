# Protobuf cheatsheet

One `.proto` file is the source. `generate.sh` turns it into Python. `register.py` uploads the same file. Field **numbers** go on the wire. Enum **names** are what you see in Python.

## File

```protobuf
syntax = "proto3";

package dcsa.tracking.v1;
```

- `syntax` stays `proto3`.
- The package ends in `.v1`. A breaking redesign is a new package `dcsa.tracking.v2`, not a reused number.
- Message names are `PascalCase`. Field names are `snake_case`.
- Generated Python uses the field name: `event.event_classifier`.

## Enums

Use an enum for a closed list (`ACT`, `PLN`, `CONF`). Use a `string` for an open value (booking id, container number, `UNLocationCode`).

```protobuf
enum EventClassifier {
  EVENT_CLASSIFIER_UNSPECIFIED = 0;
  EVENT_CLASSIFIER_ACT = 1;
  EVENT_CLASSIFIER_PLN = 2;
  EVENT_CLASSIFIER_EST = 3;
  EVENT_CLASSIFIER_REQ = 4;
}
```

- `0` is the default when a field is missing. Name it `*_UNSPECIFIED`. Never give `0` to a real code such as `ACT`.
- Prefix every value with the enum name. In this language the values share one namespace, so `ACT` in two enums will not compile.
- Append new codes. Do not renumber, and do not delete a number. Remove a code by name and keep the number:

```protobuf
reserved 4;
reserved "EVENT_CLASSIFIER_REQ";
```

- Python name is `EventClassifier.EVENT_CLASSIFIER_ACT`. The DCSA letters are the suffix, not the wire value. The wire value is the integer.

## Fields

```protobuf
EventClassifier event_classifier = 1;
string document_id = 2;
repeated ShipmentLocation shipment_locations = 3;
```

- The number after `=` is permanent. New fields take the next free number.
- `repeated` is a list. It has no null. An empty list means no locations.
- A plain `string` or enum cannot tell "missing" from "default". Default string is `""`, default enum is `0`. Write `optional` when absence matters:

```protobuf
optional string document_id = 4;
optional CargoMovementType cargo_movement = 5;
```

- Do not use a `string` for `event_classifier` once the list is closed.
- Do not put `event_type = "SHIPMENT"` on the message. The message name is the type. A topic that carries all three messages uses `oneof`:

```protobuf
message NormalizedEvent {
  oneof body {
    ShipmentEvent shipment = 1;
    EquipmentEvent equipment = 2;
    TransportEvent transport = 3;
  }
}
```

Exactly one branch is set. The three messages stay separate so each has its own fields.

## What is shared

Put a message in the same file when more than one event uses it.

| Message | Used by |
|---|---|
| `ShipmentLocation` | shipment |
| `DocumentReference` | shipment, equipment, transport |
| `TransportCall` | equipment, transport |

`ShipmentLocation.location_type` is the role of the place (`POL`, `ECP`). It is not `FacilityType` (`DEPO`, `POTE`). That one lives on `TransportCall`.

## ShipmentEvent

```protobuf
syntax = "proto3";

package dcsa.tracking.v1;

enum EventClassifier {
  EVENT_CLASSIFIER_UNSPECIFIED = 0;
  EVENT_CLASSIFIER_ACT = 1;
  EVENT_CLASSIFIER_PLN = 2;
  EVENT_CLASSIFIER_EST = 3;
  EVENT_CLASSIFIER_REQ = 4;
}

enum ShipmentEventType {
  SHIPMENT_EVENT_TYPE_UNSPECIFIED = 0;
  SHIPMENT_EVENT_TYPE_RECE = 1;
  SHIPMENT_EVENT_TYPE_DRFT = 2;
  SHIPMENT_EVENT_TYPE_PENA = 3;
  SHIPMENT_EVENT_TYPE_PENU = 4;
  SHIPMENT_EVENT_TYPE_PENC = 5;
  SHIPMENT_EVENT_TYPE_REJE = 6;
  SHIPMENT_EVENT_TYPE_APPR = 7;
  SHIPMENT_EVENT_TYPE_ISSU = 8;
  SHIPMENT_EVENT_TYPE_SURR = 9;
  SHIPMENT_EVENT_TYPE_SUBM = 10;
  SHIPMENT_EVENT_TYPE_VOID = 11;
  SHIPMENT_EVENT_TYPE_CONF = 12;
  SHIPMENT_EVENT_TYPE_REQS = 13;
  SHIPMENT_EVENT_TYPE_CMPL = 14;
  SHIPMENT_EVENT_TYPE_HOLD = 15;
  SHIPMENT_EVENT_TYPE_RELS = 16;
  SHIPMENT_EVENT_TYPE_CANC = 17;
}

enum DocumentType {
  DOCUMENT_TYPE_UNSPECIFIED = 0;
  DOCUMENT_TYPE_CBR = 1;
  DOCUMENT_TYPE_BKG = 2;
  DOCUMENT_TYPE_SHI = 3;
  DOCUMENT_TYPE_TRD = 4;
  DOCUMENT_TYPE_DEI = 5;
  DOCUMENT_TYPE_DEO = 6;
  DOCUMENT_TYPE_TRO = 7;
  DOCUMENT_TYPE_CRO = 8;
  DOCUMENT_TYPE_ARN = 9;
  DOCUMENT_TYPE_VGM = 10;
  DOCUMENT_TYPE_CAS = 11;
  DOCUMENT_TYPE_CUC = 12;
  DOCUMENT_TYPE_DGD = 13;
  DOCUMENT_TYPE_OOG = 14;
  DOCUMENT_TYPE_CQU = 15;
  DOCUMENT_TYPE_INV = 16;
}

enum CargoMovementType {
  CARGO_MOVEMENT_TYPE_UNSPECIFIED = 0;
  CARGO_MOVEMENT_TYPE_FCL = 1;
  CARGO_MOVEMENT_TYPE_LCL = 2;
  CARGO_MOVEMENT_TYPE_BB = 3;
}

enum ReceiptDeliveryType {
  RECEIPT_DELIVERY_TYPE_UNSPECIFIED = 0;
  RECEIPT_DELIVERY_TYPE_CY = 1;
  RECEIPT_DELIVERY_TYPE_SD = 2;
  RECEIPT_DELIVERY_TYPE_CFS = 3;
}

enum ShipmentLocationType {
  SHIPMENT_LOCATION_TYPE_UNSPECIFIED = 0;
  SHIPMENT_LOCATION_TYPE_PRE = 1;
  SHIPMENT_LOCATION_TYPE_POL = 2;
  SHIPMENT_LOCATION_TYPE_POD = 3;
  SHIPMENT_LOCATION_TYPE_PDE = 4;
  SHIPMENT_LOCATION_TYPE_PCF = 5;
  SHIPMENT_LOCATION_TYPE_PSR = 6;
  SHIPMENT_LOCATION_TYPE_OIR = 7;
  SHIPMENT_LOCATION_TYPE_DRL = 8;
  SHIPMENT_LOCATION_TYPE_ORI = 9;
  SHIPMENT_LOCATION_TYPE_IEL = 10;
  SHIPMENT_LOCATION_TYPE_PTP = 11;
  SHIPMENT_LOCATION_TYPE_RTP = 12;
  SHIPMENT_LOCATION_TYPE_FCD = 13;
  SHIPMENT_LOCATION_TYPE_ECP = 14;
}

message ShipmentLocation {
  ShipmentLocationType location_type = 1;
  string un_location_code = 2;
}

message DocumentReference {
  DocumentType document_type = 1;
  string document_value = 2;
}

message ShipmentEvent {
  EventClassifier event_classifier = 1;
  ShipmentEventType shipment_event_type = 2;
  DocumentType document_type = 3;
  optional string document_id = 4;
  optional CargoMovementType cargo_movement = 5;
  optional ReceiptDeliveryType receipt_delivery = 6;
  repeated ShipmentLocation shipment_locations = 7;
  repeated DocumentReference document_references = 8;
}
```

Booking confirmed is `event_classifier = EVENT_CLASSIFIER_ACT`, `shipment_event_type = SHIPMENT_EVENT_TYPE_CONF`, `document_type = DOCUMENT_TYPE_BKG`, `document_id` set, `cargo_movement` and `receipt_delivery` set, and three `shipment_locations`. A later paperwork event such as `SUBM` leaves `document_id`, `cargo_movement`, `receipt_delivery`, and `shipment_locations` unset and fills `document_references` instead.

## Equipment and transport

Same rules. Do not copy shipment fields onto them.

```protobuf
message EquipmentEvent {
  EventClassifier event_classifier = 1;
  EquipmentEventType equipment_event_type = 2;
  EmptyIndicator empty_indicator = 3;
  string equipment_reference = 4;
  TransportCall transport_call = 5;
  repeated DocumentReference document_references = 6;
}

message TransportEvent {
  EventClassifier event_classifier = 1;
  TransportEventType transport_event_type = 2;
  string equipment_reference = 3;
  TransportCall transport_call = 4;
  repeated DocumentReference document_references = 5;
}

message TransportCall {
  ModeOfTransport mode_of_transport = 1;
  FacilityType facility_type = 2;
  string un_location_code = 3;
  optional string vessel_name = 4;
  optional string export_voyage_number = 5;
  optional string import_voyage_number = 6;
}
```

`EquipmentEventType`, `EmptyIndicator`, `TransportEventType`, `ModeOfTransport`, and `FacilityType` follow the classifier pattern: `0` is `*_UNSPECIFIED`, then one number per code, prefixed.

## After editing

```
./event_schemas/generate.sh
python3 event_schemas/register.py
docker compose build keda-consumer
```

Adding a field with a new number is a compatible change. Renaming a field is compatible. Changing a number, a type, or the meaning of an enum value is not. The registry is `BACKWARD` and rejects the incompatible upload.

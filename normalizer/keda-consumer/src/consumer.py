from typing import Any

# from event_schemas import ShipmentEvent
from event_schemas.event_pb2 import EventEnvelope

from src.normalizers.fluent_float.normalizer import normalize

PROVIDER_FUNCTIONS = {
    "FluentFloat": normalize,
}


def consume(raw_event: dict[str, Any]):
    provider = raw_event["provider"]
    normalization_func = get_normalization_func(provider)
    dcsa_event: EventEnvelope = normalization_func(raw_event)
    print(dcsa_event)


def get_normalization_func(provider: str):
    try:
        return PROVIDER_FUNCTIONS[provider]
    except KeyError:
        raise Exception("Consumer: I'm angry")

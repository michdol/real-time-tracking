from confluent_kafka import Consumer
from typing import Any


def consume(consumer: Consumer):
    while True:
        message = consumer.poll(1.0)
        # TODO: handle this
        if message is None or message.error():
            continue


def normalize(raw_event: dict[str, Any]):
    pass

from confluent_kafka import Consumer
from src.settings import settings


def main():
    consumer = Consumer(settings.kafka.consumer_config)
    consumer.subscribe([settings.kafka.normalized_events_topic])
    while True:
        message = consumer.poll(1.0)
        # TODO: handle this
        if message is None or message.error():
            continue


if __name__ == "__main__":
    main()

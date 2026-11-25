from confluent_kafka import Consumer
from src.consumer import consume
from src.settings import settings


def main():
    consumer = Consumer(settings.kafka.consumer_config)
    consumer.subscribe([settings.kafka.normalized_events_topic])
    consume(consumer)


if __name__ == "__main__":
    main()

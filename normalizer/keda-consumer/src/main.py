import os

from confluent_kafka import Consumer

consumer = Consumer(
    {
        "bootstrap.servers": os.environ["KAFKA_BOOTSTRAP_SERVERS"],
        "group.id": os.environ["KAFKA_GROUP"],
        "auto.offset.reset": "earliest",
        "security.protocol": "SASL_PLAINTEXT",
        "sasl.mechanism": "SCRAM-SHA-256",
        "sasl.username": os.environ["KAFKA_SASL_USERNAME"],
        "sasl.password": os.environ["KAFKA_SASL_PASSWORD"],
    }
)
consumer.subscribe([os.environ["KAFKA_TOPIC"]])

while True:
    message = consumer.poll(1.0)
    if message is None or message.error():
        continue
    print(message.value())

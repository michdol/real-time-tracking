import os

os.environ.setdefault("SIGNING_SECRET", "test-secret")
os.environ.setdefault("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
os.environ.setdefault("KAFKA_SASL_USERNAME", "user")
os.environ.setdefault("KAFKA_SASL_PASSWORD", "password")
os.environ.setdefault("KAFKA_RAW_EVENTS_TOPIC", "raw-events")

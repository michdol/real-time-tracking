from fastapi import FastAPI
from confluent_kafka.aio import AIOProducer

from edge.settings import settings

app = FastAPI()


@app.get("/")
async def main():
    return "Ping"


@app.post("/event")
async def events() -> dict:
    producer = AIOProducer(settings.kafka.producer_config)
    try:
        future = await producer.produce("mytopic", value=b"hello")
        delivered_msg = await future
    finally:
        await producer.close()
    return {"status": "queued"}

from typing import Annotated
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, Depends
from confluent_kafka.aio import AIOProducer

from edge.settings import settings
from edge.dependencies.auth import verify_signature


@asynccontextmanager
async def lifespan(app: FastAPI):
    producer = AIOProducer(settings.kafka.producer_config)
    setattr(app, "producer", producer)
    yield
    try:
        await producer.flush()
    finally:
        await producer.close()


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def ping():
    return "ping"


@app.post("/event")
async def events(
    _: Annotated[None, Depends(verify_signature)], request: Request
) -> dict:
    """
    Send events to Kafka immediately.
    """
    await request.app.producer.produce(
        settings.kafka.raw_events_topic, value=await request.body()
    )
    await request.app.producer.flush()
    return {"status": "queued"}

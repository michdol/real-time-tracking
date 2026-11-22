from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from confluent_kafka.aio import AIOProducer

from edge.settings import settings


producers = {}


# FIXME: slow as hell endpoint
@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        producer = AIOProducer(settings.kafka.producer_config)
        producers[1] = producer
        yield
    finally:
        await producer.close()


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def ping():
    return "ping"


@app.post("/event")
async def events(request: Request) -> dict:
    future = await producers[1].produce("mytopic", value=await request.body())
    delivered_msg = await future
    return {"status": "queued"}

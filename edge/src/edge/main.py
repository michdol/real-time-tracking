from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from confluent_kafka.aio import AIOProducer

from edge.settings import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    producer = AIOProducer(settings.kafka.producer_config)
    setattr(app, "producer", producer)
    yield
    try:
        await producer.flush()
    except Exception:
        pass
    finally:
        await producer.close()


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def ping():
    return "ping"


@app.post("/event")
async def events(request: Request) -> dict:
    """
    Send events to Kafka immediately.
    """
    await request.app.producer.produce("mytopic", value=await request.body())
    await request.app.producer.flush()
    return {"status": "queued"}

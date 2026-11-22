import argparse
import asyncio
import os
import random
import time
import uuid
from datetime import datetime, timezone
import httpx


CARRIERS = ["dhl", "maersk", "hapag-lloyd"]

DHL_STATUSES = [
    ("transit", "Shipment in transit", "Package is moving through the DHL network."),
    ("transit", "Arrived at sort facility", "Shipment processed at regional hub."),
    ("delivered", "Delivered", "Delivered to recipient."),
    (
        "exception",
        "Clearance event - Customs hold",
        "Further clearance processing is required.",
    ),
]

MAERSK_DELAYS = [
    None,
    None,
    None,
    ("WEA", "Vessel delayed due to adverse weather"),
    ("CON", "Port congestion delay"),
]
HAPAG_EVENTS = [
    ("GTIN", "LADEN"),
    ("LOAD", "LADEN"),
    ("DISC", "LADEN"),
    ("GTOT", "EMPTY"),
]
PORTS = [
    ("PLGDN", "PLGDNDCT"),
    ("DEHAM", "DEHAMCTA"),
    ("NLRTM", "NLRTMAPM"),
    ("USNYC", "USNYCECT"),
]
CITIES = [("PL", "WROCLAW"), ("DE", "LEIPZIG"), ("NL", "ROTTERDAM"), ("FR", "PARIS")]


def now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def generate_dhl_payload(tracking_id: str) -> dict:
    status_code, status, desc = random.choice(DHL_STATUSES)
    orig_country, orig_city = random.choice(CITIES)
    dest_country, dest_city = random.choice(CITIES)
    ts = now_iso()

    return {
        "shipments": [
            {
                "id": tracking_id,
                "service": random.choice(["express", "parcel"]),
                "origin": {
                    "address": {
                        "countryCode": orig_country,
                        "addressLocality": orig_city,
                    }
                },
                "destination": {
                    "address": {
                        "countryCode": dest_country,
                        "addressLocality": dest_city,
                    }
                },
                "status": {
                    "timestamp": ts,
                    "location": {
                        "address": {
                            "countryCode": dest_country,
                            "addressLocality": f"{dest_city} HUB",
                        }
                    },
                    "statusCode": status_code,
                    "status": status,
                    "description": desc,
                },
                "events": [
                    {
                        "timestamp": ts,
                        "location": {
                            "address": {"addressLocality": f"{dest_city} HUB"}
                        },
                        "statusCode": status_code,
                        "description": desc,
                    }
                ],
            }
        ]
    }


def generate_maersk_payload(container_id: str) -> dict:
    port, facility = random.choice(PORTS)
    delay = random.choice(MAERSK_DELAYS)
    ts = now_iso()

    payload = {
        "eventID": str(uuid.uuid4()),
        "eventType": "TRANSPORT",
        "eventDateTime": ts,
        "eventCreatedDateTime": ts,
        "eventClassifierCode": "EST" if delay else "ACT",
        "transportEventTypeCode": random.choice(["ARRI", "DEPA"]),
        "transportCall": {
            "transportCallID": f"TC-{random.randint(10000, 99999)}",
            "carrierServiceCode": "AE10",
            "modeOfTransport": "VESSEL",
            "UNLocationCode": port,
            "facilityCode": facility,
            "vessel": {
                "vesselIMONumber": "9778791",
                "vesselName": random.choice(
                    ["MADRID MAERSK", "MONACO MAERSK", "MUNICH MAERSK"]
                ),
            },
        },
        "references": [
            {"referenceType": "EQ", "referenceValue": container_id},
            {
                "referenceType": "BL",
                "referenceValue": str(random.randint(100000000, 999999999)),
            },
        ],
    }

    if delay:
        payload["delayReasonCode"] = delay[0]
        payload["changeRemark"] = delay[1]

    return payload


def generate_hapag_payload(container_id: str) -> dict:
    port, facility = random.choice(PORTS)
    event_code, empty_code = random.choice(HAPAG_EVENTS)
    ts = now_iso()

    return {
        "eventID": str(uuid.uuid4()),
        "eventType": "EQUIPMENT",
        "eventDateTime": ts,
        "eventCreatedDateTime": ts,
        "eventClassifierCode": "ACT",
        "equipmentEventTypeCode": event_code,
        "equipmentReference": container_id,
        "ISOEquipmentCode": "45G1",
        "emptyIndicatorCode": empty_code,
        "transportCall": {
            "UNLocationCode": port,
            "facilityCode": facility,
            "facilityTypeCode": "POTE",
            "modeOfTransport": "VESSEL",
        },
        "documentReferences": [
            {
                "documentReferenceType": "BKG",
                "documentReferenceValue": str(random.randint(10000000, 99999999)),
            }
        ],
    }


def build_event(shipment_pool: list[str]) -> tuple[str, dict]:
    carrier = random.choice(CARRIERS)
    shipment_id = random.choice(shipment_pool)

    if carrier == "dhl":
        return carrier, generate_dhl_payload(f"0034{shipment_id}")
    elif carrier == "maersk":
        return carrier, generate_maersk_payload(f"MSKU{shipment_id}")
    else:
        return carrier, generate_hapag_payload(f"HLXU{shipment_id}")


async def worker(
    client: httpx.AsyncClient,
    queue: asyncio.Queue,
    url: str,
    stats: dict,
):
    while True:
        item = await queue.get()
        if item is None:
            queue.task_done()
            break

        carrier, payload = item
        headers = {
            "Content-Type": "application/json",
            "X-Carrier-Source": carrier,
        }

        try:
            resp = await client.post(url, json=payload, headers=headers)
            if 200 <= resp.status_code < 300:
                stats["success"] += 1
            else:
                stats["failed"] += 1
        except Exception:
            stats["failed"] += 1
        finally:
            queue.task_done()


async def run_load_test(
    url: str,
    total_events: int,
    concurrency: int,
    unique_shipments: int,
    rate_limit: float | None,
):
    shipment_pool = [
        f"{random.randint(1000000, 9999999)}" for _ in range(unique_shipments)
    ]
    queue: asyncio.Queue = asyncio.Queue(maxsize=concurrency * 4)
    stats = {"success": 0, "failed": 0}

    limits = httpx.Limits(
        max_keepalive_connections=concurrency, max_connections=concurrency * 2
    )
    timeout = httpx.Timeout(10.0, connect=5.0)

    start_time = time.perf_counter()

    async with httpx.AsyncClient(limits=limits, timeout=timeout) as client:
        workers = [
            asyncio.create_task(worker(client, queue, url, stats))
            for _ in range(concurrency)
        ]

        interval = (1.0 / rate_limit) if rate_limit and rate_limit > 0 else 0.0

        for i in range(total_events):
            await queue.put(build_event(shipment_pool))
            if interval > 0:
                await asyncio.sleep(interval)

            if (i + 1) % max(1, total_events // 10) == 0:
                elapsed = time.perf_counter() - start_time
                eps = (stats["success"] + stats["failed"]) / elapsed
                print(
                    f"Progress: {i + 1}/{total_events} queued | "
                    f"OK: {stats['success']} | Err: {stats['failed']} | "
                    f"Rate: {eps:.1f} req/s"
                )

        for _ in range(concurrency):
            await queue.put(None)

        await queue.join()
        await asyncio.gather(*workers)

    total_time = time.perf_counter() - start_time
    throughput = total_events / total_time if total_time > 0 else 0

    print("\n--- Load Generation Complete ---")
    print(f"Target URL:     {url}")
    print(f"Total Events:   {total_events}")
    print(f"Succeeded:      {stats['success']}")
    print(f"Failed:         {stats['failed']}")
    print(f"Elapsed Time:   {total_time:.2f}s")
    print(f"Avg Throughput: {throughput:.1f} events/sec")


def main():
    parser = argparse.ArgumentParser(
        description="High-volume carrier event generator for FastAPI."
    )
    parser.add_argument(
        "--url",
        default=os.getenv("INGEST_URL", "http://localhost:8000/webhooks/carrier"),
        help="FastAPI ingestion endpoint URL (env: INGEST_URL)",
    )
    parser.add_argument(
        "--events",
        type=int,
        default=int(os.getenv("TOTAL_EVENTS", "10000")),
        help="Total number of events to send (env: TOTAL_EVENTS)",
    )
    parser.add_argument(
        "--concurrency",
        type=int,
        default=int(os.getenv("CONCURRENCY", "50")),
        help="Number of concurrent async HTTP workers (env: CONCURRENCY)",
    )
    parser.add_argument(
        "--shipments",
        type=int,
        default=int(os.getenv("UNIQUE_SHIPMENTS", "500")),
        help="Pool size of unique shipment IDs to simulate multi-event histories (env: UNIQUE_SHIPMENTS)",
    )
    parser.add_argument(
        "--rate",
        type=float,
        default=float(os.getenv("RATE_LIMIT", "0")) or None,
        help="Optional max events per second; 0 = unlimited burst (env: RATE_LIMIT)",
    )
    args = parser.parse_args()

    asyncio.run(
        run_load_test(
            url=args.url,
            total_events=args.events,
            concurrency=args.concurrency,
            unique_shipments=args.shipments,
            rate_limit=args.rate,
        )
    )


if __name__ == "__main__":
    main()

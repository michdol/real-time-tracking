"""Send happy-path container voyages to the Edge app.

Each scenario is one container on one booking: empty pickup, gate in full,
load, depart, arrive, discharge, gate out full, empty return. Carriers rotate
through Maersk, Hapag-Lloyd, MSC, CMA CGM, and ONE. Events stay in DCSA Track
and Trace shape. The request body is one event. Carrier and scenario id are headers.

Settings come from event_sources/.env. Flags override those values.
"""

import argparse
import json
import os
import threading
import time
import urllib.error
import urllib.request
import uuid
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path

ISO_EQUIPMENT_CODE = "45G1"
SCENARIO_NAME = "happy_path_direct_voyage"
ENV_PATH = Path(__file__).with_name(".env")

_LETTER_VALUES = {
    "A": 10,
    "B": 12,
    "C": 13,
    "D": 14,
    "E": 15,
    "F": 16,
    "G": 17,
    "H": 18,
    "I": 19,
    "J": 20,
    "K": 21,
    "L": 23,
    "M": 24,
    "N": 25,
    "O": 26,
    "P": 27,
    "Q": 28,
    "R": 29,
    "S": 30,
    "T": 31,
    "U": 32,
    "V": 34,
    "W": 35,
    "X": 36,
    "Y": 37,
    "Z": 38,
}


@dataclass(frozen=True)
class Carrier:
    slug: str
    owner_code: str
    booking_prefix: str
    bl_prefix: str
    service_code: str
    vessel_name: str
    vessel_imo: str


@dataclass(frozen=True)
class Place:
    unlocode: str
    name: str
    tz: timezone
    terminal_code: str
    depot_code: str


@dataclass(frozen=True)
class Lane:
    origin: Place
    destination: Place
    transit: timedelta


CARRIERS = (
    Carrier("maersk", "MSKU", "MAEU", "MAEU", "AE1", "MADRID MAERSK", "9778791"),
    Carrier(
        "hapag-lloyd", "HLCU", "HLCU", "HLCUBC", "FE2", "BERLIN EXPRESS", "9540118"
    ),
    Carrier("msc", "MSCU", "MEDU", "MEDU", "LION", "MSC OSCAR", "9703291"),
    Carrier("cma-cgm", "CMAU", "CMDU", "CMDU", "FAL1", "CMA CGM MARCO POLO", "9454436"),
    Carrier("one", "ONEU", "ONEY", "ONEY", "FE3", "ONE CRANE", "9741401"),
)

PLUS_8 = timezone(timedelta(hours=8))
PLUS_2 = timezone(timedelta(hours=2))

LANES = (
    Lane(
        Place("CNSHA", "Shanghai", PLUS_8, "CNSHAYS4", "CNSHADEP"),
        Place("NLRTM", "Rotterdam", PLUS_2, "NLRTMAPM", "NLRTMDEP"),
        timedelta(days=32),
    ),
    Lane(
        Place("CNNGB", "Ningbo", PLUS_8, "CNNGBCTN", "CNNGBDEP"),
        Place("DEHAM", "Hamburg", PLUS_2, "DEHAMCTA", "DEHAMDEP"),
        timedelta(days=30),
    ),
    Lane(
        Place("SGSIN", "Singapore", PLUS_8, "SGSINPSA", "SGSINDEP"),
        Place("BEANR", "Antwerp", PLUS_2, "BEANRPSA", "BEANRDEP"),
        timedelta(days=28),
    ),
)


def load_env(path: Path) -> None:
    if not path.exists():
        return
    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or "=" not in stripped:
            continue
        key, value = stripped.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip())


def container_number(owner: str, serial: str) -> str:
    body = f"{owner}{serial}"
    total = sum(
        (_LETTER_VALUES[char] if char.isalpha() else int(char)) * (2**index)
        for index, char in enumerate(body)
    )
    check = total % 11
    if check == 10:
        check = 0
    return f"{body}{check}"


def _event_id(scenario_id: str, name: str) -> str:
    return str(uuid.uuid5(uuid.NAMESPACE_URL, f"rtt:{scenario_id}:{name}"))


def _stamp(local: datetime, reported_after: timedelta) -> tuple[str, str]:
    created = local.astimezone(timezone.utc) + reported_after
    return (
        local.isoformat(timespec="seconds"),
        created.strftime("%Y-%m-%dT%H:%M:%SZ"),
    )


def _documents(booking: str, bill_of_lading: str) -> list[dict[str, str]]:
    return [
        {"documentReferenceType": "BKG", "documentReferenceValue": booking},
        {"documentReferenceType": "TRD", "documentReferenceValue": bill_of_lading},
    ]


def _location(place: Place) -> dict[str, str]:
    return {"UNLocationCode": place.unlocode, "locationName": place.name}


def _transport_call(
    call_id: str,
    place: Place,
    facility_code: str,
    facility_type: str,
    mode: str,
    carrier: Carrier,
    voyage: str,
    vessel: bool,
) -> dict:
    call = {
        "transportCallID": call_id,
        "carrierServiceCode": carrier.service_code,
        "modeOfTransport": mode,
        "UNLocationCode": place.unlocode,
        "facilityCode": facility_code,
        "facilityTypeCode": facility_type,
        "location": _location(place),
    }
    if vessel:
        call["exportVoyageNumber"] = voyage
        call["importVoyageNumber"] = voyage
        call["vessel"] = {
            "vesselIMONumber": carrier.vessel_imo,
            "vesselName": carrier.vessel_name,
        }
    return call


def _equipment(
    scenario_id: str,
    name: str,
    happened: datetime,
    reported_after: timedelta,
    event_code: str,
    empty_indicator: str,
    container: str,
    documents: list[dict[str, str]],
    transport_call: dict,
) -> dict:
    event_time, created_time = _stamp(happened, reported_after)
    return {
        "eventID": _event_id(scenario_id, name),
        "eventType": "EQUIPMENT",
        "eventClassifierCode": "ACT",
        "eventDateTime": event_time,
        "eventCreatedDateTime": created_time,
        "equipmentEventTypeCode": event_code,
        "equipmentReference": container,
        "ISOEquipmentCode": ISO_EQUIPMENT_CODE,
        "emptyIndicatorCode": empty_indicator,
        "eventLocation": transport_call["location"],
        "transportCall": transport_call,
        "documentReferences": documents,
    }


def _transport(
    scenario_id: str,
    name: str,
    happened: datetime,
    reported_after: timedelta,
    event_code: str,
    container: str,
    documents: list[dict[str, str]],
    transport_call: dict,
) -> dict:
    event_time, created_time = _stamp(happened, reported_after)
    return {
        "eventID": _event_id(scenario_id, name),
        "eventType": "TRANSPORT",
        "eventClassifierCode": "ACT",
        "eventDateTime": event_time,
        "eventCreatedDateTime": created_time,
        "transportEventTypeCode": event_code,
        "equipmentReference": container,
        "eventLocation": transport_call["location"],
        "transportCall": transport_call,
        "documentReferences": documents,
    }


def happy_path(index: int) -> dict:
    carrier = CARRIERS[index % len(CARRIERS)]
    lane = LANES[index % len(LANES)]
    scenario_id = str(uuid.uuid5(uuid.NAMESPACE_URL, f"rtt:{SCENARIO_NAME}:{index}"))
    number = index + 1
    serial = f"{number % 1_000_000:06d}"
    container = container_number(carrier.owner_code, serial)
    booking = f"{carrier.booking_prefix}{number:08d}"
    bill_of_lading = f"{carrier.bl_prefix}{number:09d}"
    voyage = f"{600 + (index % 50)}W"
    documents = _documents(booking, bill_of_lading)
    call = f"tc-{index}"

    origin_depot = _transport_call(
        f"{call}-origin-depot",
        lane.origin,
        lane.origin.depot_code,
        "DEPO",
        "TRUCK",
        carrier,
        voyage,
        vessel=False,
    )
    origin_terminal = _transport_call(
        f"{call}-origin-terminal",
        lane.origin,
        lane.origin.terminal_code,
        "POTE",
        "TRUCK",
        carrier,
        voyage,
        vessel=False,
    )
    origin_vessel = _transport_call(
        f"{call}-origin-vessel",
        lane.origin,
        lane.origin.terminal_code,
        "POTE",
        "VESSEL",
        carrier,
        voyage,
        vessel=True,
    )
    destination_vessel = _transport_call(
        f"{call}-destination-vessel",
        lane.destination,
        lane.destination.terminal_code,
        "POTE",
        "VESSEL",
        carrier,
        voyage,
        vessel=True,
    )
    destination_terminal = _transport_call(
        f"{call}-destination-terminal",
        lane.destination,
        lane.destination.terminal_code,
        "POTE",
        "TRUCK",
        carrier,
        voyage,
        vessel=False,
    )
    destination_depot = _transport_call(
        f"{call}-destination-depot",
        lane.destination,
        lane.destination.depot_code,
        "DEPO",
        "TRUCK",
        carrier,
        voyage,
        vessel=False,
    )

    pickup = datetime(2026, 4, 2, 9, 0, tzinfo=lane.origin.tz) + timedelta(
        days=index % 45
    )
    gate_in = pickup + timedelta(days=2, hours=6)
    loaded = pickup + timedelta(days=4)
    departed = pickup + timedelta(days=4, hours=10)
    arrived = (departed + lane.transit).astimezone(lane.destination.tz)
    discharged = arrived + timedelta(hours=8)
    gate_out = arrived + timedelta(days=2)
    empty_return = arrived + timedelta(days=6)

    events = [
        _equipment(
            scenario_id,
            "empty-pickup",
            pickup,
            timedelta(minutes=20),
            "GTOT",
            "EMPTY",
            container,
            documents,
            origin_depot,
        ),
        _equipment(
            scenario_id,
            "gate-in-full",
            gate_in,
            timedelta(minutes=30),
            "GTIN",
            "LADEN",
            container,
            documents,
            origin_terminal,
        ),
        _equipment(
            scenario_id,
            "loaded",
            loaded,
            timedelta(minutes=25),
            "LOAD",
            "LADEN",
            container,
            documents,
            origin_vessel,
        ),
        _transport(
            scenario_id,
            "departed-origin",
            departed,
            timedelta(minutes=30),
            "DEPA",
            container,
            documents,
            origin_vessel,
        ),
        _transport(
            scenario_id,
            "arrived-destination",
            arrived,
            timedelta(minutes=40),
            "ARRI",
            container,
            documents,
            destination_vessel,
        ),
        _equipment(
            scenario_id,
            "discharged",
            discharged,
            timedelta(minutes=35),
            "DISC",
            "LADEN",
            container,
            documents,
            destination_vessel,
        ),
        _equipment(
            scenario_id,
            "gate-out-full",
            gate_out,
            timedelta(minutes=25),
            "GTOT",
            "LADEN",
            container,
            documents,
            destination_terminal,
        ),
        _equipment(
            scenario_id,
            "empty-returned",
            empty_return,
            timedelta(minutes=45),
            "GTIN",
            "EMPTY",
            container,
            documents,
            destination_depot,
        ),
    ]
    return {
        "scenario": SCENARIO_NAME,
        "scenarioId": scenario_id,
        "carrier": carrier.slug,
        "container": container,
        "booking": booking,
        "events": events,
    }


class RateLimiter:
    def __init__(self, per_second: float) -> None:
        self.interval = 1.0 / per_second if per_second > 0 else 0.0
        self._lock = threading.Lock()
        self._next_at = 0.0

    def wait(self) -> None:
        if self.interval <= 0:
            return
        with self._lock:
            now = time.perf_counter()
            slot = max(now, self._next_at)
            self._next_at = slot + self.interval
            delay = slot - now
        if delay > 0:
            time.sleep(delay)


def event_body(event: dict) -> bytes:
    return json.dumps(event).encode()


def post_event(
    url: str,
    scenario: dict,
    event: dict,
    limiter: RateLimiter,
    api_key: str,
    invalid: bool,
) -> tuple[bool, str]:
    limiter.wait()
    body = event_body(event)
    token = "invalid" if invalid else api_key
    request = urllib.request.Request(
        url,
        data=body,
        headers={
            "Content-Type": "application/json",
            "X-Carrier": scenario["carrier"],
            "X-Scenario": scenario["scenario"],
            "X-Scenario-Id": scenario["scenarioId"],
            "Authorization": f"Bearer {token}",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=10) as response:
            ok = 200 <= response.status < 300
            return ok, "" if ok else f"HTTP {response.status}"
    except urllib.error.HTTPError as exc:
        return False, f"HTTP {exc.code}"
    except urllib.error.URLError as exc:
        return False, str(exc.reason)


def send_scenario(
    url: str,
    scenario: dict,
    limiter: RateLimiter,
    api_key: str,
    invalid_every: int,
    scenario_index: int,
) -> tuple[int, int, str]:
    success = 0
    failed = 0
    sample_error = ""
    for event_index, event in enumerate(scenario["events"]):
        sequence = scenario_index * 8 + event_index
        invalid = invalid_every > 0 and sequence % invalid_every == 0
        ok, error = post_event(url, scenario, event, limiter, api_key, invalid)
        if ok:
            success += 1
        else:
            failed += 1
            if not sample_error:
                sample_error = error
    return success, failed, sample_error


def run_load(
    url: str,
    count: int,
    concurrency: int,
    rate: float,
    api_key: str,
    invalid_every: int,
) -> None:
    limiter = RateLimiter(rate)
    stats = {"success": 0, "failed": 0, "scenarios": 0}
    sample_error = ""
    lock = threading.Lock()
    started = time.perf_counter()
    report_every = max(1, count // 10)

    print(
        f"Sending {count} scenarios ({count * 8} events) to {url} "
        f"with concurrency {concurrency}"
    )

    with ThreadPoolExecutor(max_workers=concurrency) as pool:
        futures = [
            pool.submit(
                send_scenario,
                url,
                happy_path(index),
                limiter,
                api_key,
                invalid_every,
                index,
            )
            for index in range(count)
        ]
        for future in as_completed(futures):
            success, failed, error = future.result()
            with lock:
                stats["success"] += success
                stats["failed"] += failed
                stats["scenarios"] += 1
                if error and not sample_error:
                    sample_error = error
                done = stats["scenarios"]
            if done % report_every == 0 or done == count:
                elapsed = time.perf_counter() - started
                sent = stats["success"] + stats["failed"]
                pace = sent / elapsed if elapsed else 0
                print(
                    f"Scenarios {done}/{count} | "
                    f"OK {stats['success']} | Err {stats['failed']} | "
                    f"{pace:.1f} events/s"
                )

    elapsed = time.perf_counter() - started
    print(f"Finished in {elapsed:.2f}s")
    if sample_error:
        print(f"Sample error: {sample_error}")


def main() -> None:
    load_env(ENV_PATH)
    parser = argparse.ArgumentParser(description="Send happy-path voyages to Edge.")
    parser.add_argument(
        "--url",
        default=os.getenv("INGEST_URL", "http://localhost:8000/event"),
        help="Edge ingestion URL (env: INGEST_URL)",
    )
    parser.add_argument(
        "--scenarios",
        type=int,
        default=int(os.getenv("SCENARIOS", "100")),
        help="Number of voyages to send (env: SCENARIOS)",
    )
    parser.add_argument(
        "--concurrency",
        type=int,
        default=int(os.getenv("CONCURRENCY", "10")),
        help="Voyages in flight at once (env: CONCURRENCY)",
    )
    parser.add_argument(
        "--rate",
        type=float,
        default=float(os.getenv("RATE_LIMIT", "0")),
        help="Max events per second. 0 is unlimited (env: RATE_LIMIT)",
    )
    parser.add_argument(
        "--api-key",
        default=os.getenv("API_KEY", ""),
        help="Provider API key sent as Authorization: Bearer (env: API_KEY)",
    )
    parser.add_argument(
        "--invalid-every",
        type=int,
        default=int(os.getenv("INVALID_API_KEY_EVERY", "0")),
        help="Send Authorization: Bearer invalid on every Nth event. 0 disables it",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the first voyage and send nothing",
    )
    args = parser.parse_args()

    if args.scenarios < 1:
        raise SystemExit("scenarios must be at least 1")
    if args.concurrency < 1:
        raise SystemExit("concurrency must be at least 1")
    if not args.api_key:
        raise SystemExit("API_KEY is required")
    if args.invalid_every < 0:
        raise SystemExit("invalid-every must be 0 or greater")

    if args.dry_run:
        scenario = happy_path(0)
        print(json.dumps(scenario, indent=2))
        print(f"\nAuthorization: Bearer {args.api_key}")
        print(
            f"Dry run: {args.scenarios} scenarios, {args.scenarios * 8} events, "
            f"nothing sent to {args.url}"
        )
        return

    run_load(
        args.url,
        args.scenarios,
        args.concurrency,
        args.rate,
        args.api_key,
        args.invalid_every,
    )


if __name__ == "__main__":
    main()

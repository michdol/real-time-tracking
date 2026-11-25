import json
import os
import urllib.request
from pathlib import Path

SUBJECT = "normalized-events-value"
REGISTRY_URL = os.environ.get("SCHEMA_REGISTRY_URL", "http://localhost:18081")
PROTO = Path(__file__).with_name("proto") / "event.proto"


def registration_body() -> str:
    return json.dumps({"schemaType": "PROTOBUF", "schema": PROTO.read_text()})


def register(registry_url: str) -> int:
    config = json.dumps({"compatibility": "BACKWARD"}).encode()
    request = urllib.request.Request(
        f"{registry_url}/config/{SUBJECT}",
        data=config,
        headers={"Content-Type": "application/vnd.schemaregistry.v1+json"},
        method="PUT",
    )
    with urllib.request.urlopen(request) as response:
        response.read()

    request = urllib.request.Request(
        f"{registry_url}/subjects/{SUBJECT}/versions",
        data=registration_body().encode(),
        headers={"Content-Type": "application/vnd.schemaregistry.v1+json"},
        method="POST",
    )
    with urllib.request.urlopen(request) as response:
        return json.load(response)["id"]


if __name__ == "__main__":
    print(register(REGISTRY_URL))

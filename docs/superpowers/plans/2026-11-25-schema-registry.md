# Protobuf schemas, generated package, Redpanda registry

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** `.proto` files are the source of the schema. A local script generates an installable Python package, and a second script registers that same `.proto` in Redpanda Schema Registry.

**Architecture:** `event_schemas/proto/event.proto` is the schema for `ShipmentEvent`, `EquipmentEvent`, and `TransportEvent`. `event_schemas/generate.sh` runs `buf generate` and writes Python into `event_schemas/src/event_schemas/`. `event_schemas/register.py` POSTs the `.proto` text to subject `normalized-events-value`. Compose builds `keda-consumer:local` with the repo as the build context. The Dockerfile copies `event_schemas` to `/tmp/event_schemas`, runs `pip install /tmp/event_schemas`, and deletes that copy. The registry does not build the wheel.

**Tech Stack:** Protobuf 3, `buf` CLI, `protobuf` Python runtime, Redpanda Schema Registry (`http://localhost:18081` from the host, `http://redpanda-0:8081` on the Compose network), Docker Compose.

## Global Constraints

- Do not change Edge. `POST /event` still writes the raw body to `raw-events`.
- Do not register a schema for `raw-events`.
- Schema type is `PROTOBUF`. Subject is `normalized-events-value`. Compatibility is `BACKWARD`.
- Do not create git commits unless the user asks.
- Do not hand-edit `event_schemas/src/event_schemas/event_pb2.py` or `event_pb2.pyi`. Only `buf generate` writes them.

## Directory

```
event_schemas/
  buf.yaml
  buf.gen.yaml
  proto/event.proto
  generate.sh
  register.py
  pyproject.toml
  src/event_schemas/__init__.py
  src/event_schemas/event_pb2.py      # generated
  src/event_schemas/event_pb2.pyi     # generated
```

`buf.yaml` module path is `proto`. `buf.gen.yaml` writes into `src/event_schemas`. Import is `from event_schemas import ShipmentEvent`.

## Commands

Generate, after `buf` is installed on the host:

```
./event_schemas/generate.sh
```

Register the `.proto` text, not the generated Python:

```
python3 event_schemas/register.py
```

`SCHEMA_REGISTRY_URL` defaults to `http://localhost:18081`. A second run prints the same schema id.

Build the normalizer image. Compose does not copy into a running container. The build context is the repo root, so the Dockerfile can see `event_schemas`:

```
docker compose build keda-consumer
```

The image build fails if `event_pb2.py` is missing. `keda-bootstrap` does not build this image. It imports `keda-consumer:local` after the `keda-consumer` service has exited.

Confirm the install:

```
docker run --rm --entrypoint python keda-consumer:local -c "from event_schemas import ShipmentEvent"
```

## Requirements

| Tool or library | Where | Why |
|---|---|---|
| `buf` CLI | host, used by `generate.sh` | lint and `buf generate` |
| `protobuf` `>=7.36` | `event-schemas` dependency | generated code imports it |
| Redpanda Schema Registry | host port `18081` | stores the `.proto` |

Not required: `grpcio-tools`, a local `protoc`, or a relative `pip install -e ../../event_schemas`.

## Out of scope

- Producing or consuming the Confluent Protobuf wire format.
- Changing the KEDA consumer loop.

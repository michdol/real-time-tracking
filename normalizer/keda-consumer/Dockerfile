FROM python:3.13-slim

WORKDIR /app

COPY event_schemas /tmp/event_schemas
COPY normalizer/keda-consumer/requirements.txt requirements.txt

RUN test -f /tmp/event_schemas/src/event_schemas/event_pb2.py \
    || { echo "run event_schemas/generate.sh before building the normalizer" >&2; exit 1; }

RUN pip install --no-cache-dir /tmp/event_schemas \
    && pip install --no-cache-dir -r requirements.txt \
    && rm -rf /tmp/event_schemas

COPY normalizer/keda-consumer/src/ src/

WORKDIR /app/src

CMD ["python", "-u", "main.py"]

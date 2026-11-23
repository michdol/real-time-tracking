FROM python:3.13-slim AS build

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

COPY . /srv

WORKDIR /srv

RUN uv sync --no-cache

FROM python:3.13-slim

WORKDIR /edge

COPY --from=build /srv /edge

COPY --from=build /usr/bin/uv /usr/bin/uv

COPY --from=build /usr/bin/uvx /usr/bin/uvx

EXPOSE 8000

CMD ["uv", "run", "fastapi", "dev", "./src/edge/main.py", "--port", "8000", "--host", "0.0.0.0"]

# ENTRYPOINT ["tail", "-f", "/dev/null"]

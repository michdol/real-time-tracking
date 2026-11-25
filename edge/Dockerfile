FROM python:3.13-slim AS build

COPY --from=ghcr.io/astral-sh/uv:0.13.9 /uv /uvx /bin/

COPY . /edge

WORKDIR /edge

COPY pyproject.toml uv.lock ./

RUN --mount=type=cache,target=/root/.cache/uv \
	uv sync --frozen --no-dev

COPY src ./src

RUN --mount=type=cache,target=/root/.cache/uv \
	uv sync --frozen --no-dev

FROM python:3.13-slim

WORKDIR /edge

COPY --from=build /edge /edge

ENV PATH="/edge/.venv/bin:$PATH"

EXPOSE 8000

CMD ["fastapi", "dev", "./src/edge/main.py", "--port", "8000", "--host", "0.0.0.0"]

# ENTRYPOINT ["tail", "-f", "/dev/null"]

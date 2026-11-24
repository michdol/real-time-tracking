# Frontend task board

Completeness of the current UI scope: **100%**.

The four screens below are implemented. They call the API and show sample shipments when the API does not respond. Connecting this image to the repo `docker-compose.yaml` is not done. There is no control that starts a backend scenario, because no such endpoint was specified.

Started: 2026-11-24T08:03:00+01:00
Finished: 2026-11-24T08:07:18+01:00
Duration: 4 minutes

## Run

From `frontend/` inside WSL:

```
docker build -t rtt-frontend .
docker run --rm -p 5173:5173 rtt-frontend
```

Open `http://localhost:5173`. The image build runs the tests.

The image was not built in this session. Docker Desktop was not running.

`VITE_API_BASE` is fixed at image build time. Default is `http://localhost:8000`.

## Tasks

| Feature | Doc | Status |
| --- | --- | --- |
| Search orders | [search-orders.md](search-orders.md) | done |
| Real time tracking | [real-time-tracking.md](real-time-tracking.md) | done |
| Notifications | [notifications.md](notifications.md) | done |
| Alerting and resolution | [alerting-and-resolution.md](alerting-and-resolution.md) | done |

## API the UI calls

| Method | Path | Used by |
| --- | --- | --- |
| GET | `/orders?container&booking&billOfLading&status` | Search |
| GET | `/orders/{id}/tracking` | Real time tracking |
| GET | `/notifications` | Notifications |
| GET | `/alerts` | Alerts |

`status` is `active` or `historical`. Omit it for both. Response bodies are JSON arrays, or one tracking object. Field names match `src/types.ts`.

## Shared decisions

- React, TypeScript, Vite, Bootstrap. One Docker image. The dev machine does not install npm packages.
- Sample data is the fallback so the screens work before the backend exists. A warning is shown in that case.
- No login. The screen is one customer's orders.
- The resolution buttons do not call the API.

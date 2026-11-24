# Real time tracking

Started: 2026-11-24T08:03:00+01:00
Finished: 2026-11-24T08:07:18+01:00
Duration: 4 minutes

## Description

Shows one order: route, status, current milestone, ETA, the milestone list, and a one-line picture of where the container is on that route.

## Definition of done

- Route `/tracking/:orderId` loads `GET /orders/{id}/tracking`.
- The page shows order details, milestone history, and the route picture.
- The current milestone is wrapped in brackets in the picture.
- A missing order says that tracking was not found.
- Sample tracking is used when the API does not respond.

## Decisions

- The picture is text, not a map tile service. No API key and no extra dependency.
- Steps in order: empty pickup, gate in, loaded, at sea, arrived, discharged, gate out, empty returned.

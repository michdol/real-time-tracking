# Search orders

Started: 2026-11-24T08:03:00+01:00
Finished: 2026-11-24T08:07:18+01:00
Duration: 4 minutes

## Description

One page lists the customer's orders and shows the selected order beside the list. Search fields are container number, booking, bill of lading, and status (active, historical, or both). The selected order has a button to Real time tracking.

## Definition of done

- Search submits to `GET /orders` with those parameters.
- The list and the detail card are on the same page.
- The detail card links to `/tracking/{orderId}`.
- If the API does not respond, the same page shows the sample orders and a warning.

## Decisions

- The server is expected to apply the filters. The sample fallback filters in the browser with the same fields.
- Tracking is not a top-level nav item. The user reaches it from an order.

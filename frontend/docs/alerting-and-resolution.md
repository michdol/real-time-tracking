# Alerting and resolution

Started: 2026-11-24T08:03:00+01:00
Finished: 2026-11-24T08:07:18+01:00
Duration: 4 minutes

## Description

Lists disruptions on the customer's orders: container, booking, reason, original ETA, revised ETA. Each alert has three actions: Accept new schedule, Request reroute, Escalate to operations. The buttons do nothing.

## Definition of done

- The page loads `GET /alerts`.
- Each alert shows the affected order, the reason, and both ETAs.
- The three buttons render and have no click behavior.
- Sample data includes one weather delay.

## How this works in real life

A disruption is a rolled container, a missed connection, a customs hold, weather, or a blank sailing. The carrier or the visibility platform tells the customer which containers moved, why, and the new ETA. Someone then chooses one of three outcomes:

- Accept the new schedule and tell the consignee.
- Ask for another vessel or route when the delay is too long.
- Escalate when the cargo is urgent, the reason is unclear, or a person has to clear documents or customs.

That choice is the manual step. Later, AWS Step Functions can run the follow-up (notify parties, update the booking, confirm the vessel, close the alert). The three buttons are those choices. They are not wired.

## Decisions

- No `POST` from these buttons until the workflow exists.

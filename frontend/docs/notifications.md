# Notifications

Started: 2026-11-24T08:03:00+01:00
Finished: 2026-11-24T08:07:18+01:00
Duration: 4 minutes

## Description

One tab lists in-app notifications and emails. Each row is a message about a milestone on a booking: channel, milestone, text, and time. Buttons filter the list to all, in-app, or email.

## Definition of done

- The page loads `GET /notifications`.
- Email and in-app messages are in the same list.
- The channel filter only hides rows. It does not call the API again.
- Sample messages are shown when the API does not respond.

## Decisions

- A notification is a message already sent. This screen does not compose or send mail.

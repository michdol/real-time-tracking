import type { Alert, Notice, Order, Tracking } from "./types"

export const sampleOrders: Order[] = [
  {
    id: "ord-1",
    booking: "MAEU00000001",
    billOfLading: "MAEU000000001",
    container: "MSKU0000006",
    carrier: "maersk",
    origin: "Shanghai",
    destination: "Rotterdam",
    status: "active",
    milestone: "departed",
    eta: "2026-05-08T13:00:00+02:00",
  },
  {
    id: "ord-2",
    booking: "HLCU00000002",
    billOfLading: "HLCUBC000000002",
    container: "HLCU0000014",
    carrier: "hapag-lloyd",
    origin: "Ningbo",
    destination: "Hamburg",
    status: "historical",
    milestone: "empty_returned",
    eta: "2026-05-20T09:00:00+02:00",
  },
]

export const sampleTracking: Record<string, Tracking> = {
  "ord-1": {
    order: sampleOrders[0],
    milestones: [
      { name: "empty_pickup", location: "Shanghai", happenedAt: "2026-04-02T09:00:00+08:00" },
      { name: "gate_in", location: "Shanghai", happenedAt: "2026-04-04T15:00:00+08:00" },
      { name: "loaded", location: "Shanghai", happenedAt: "2026-04-06T09:00:00+08:00" },
      { name: "departed", location: "Shanghai", happenedAt: "2026-04-06T19:00:00+08:00" },
    ],
  },
  "ord-2": {
    order: sampleOrders[1],
    milestones: [
      { name: "empty_pickup", location: "Ningbo", happenedAt: "2026-04-03T09:00:00+08:00" },
      { name: "gate_in", location: "Ningbo", happenedAt: "2026-04-05T15:00:00+08:00" },
      { name: "loaded", location: "Ningbo", happenedAt: "2026-04-07T09:00:00+08:00" },
      { name: "departed", location: "Ningbo", happenedAt: "2026-04-07T19:00:00+08:00" },
      { name: "arrived", location: "Hamburg", happenedAt: "2026-05-07T08:00:00+02:00" },
      { name: "discharged", location: "Hamburg", happenedAt: "2026-05-07T16:00:00+02:00" },
      { name: "gate_out", location: "Hamburg", happenedAt: "2026-05-09T11:00:00+02:00" },
      { name: "empty_returned", location: "Hamburg", happenedAt: "2026-05-13T09:00:00+02:00" },
    ],
  },
}

export const sampleNotices: Notice[] = [
  {
    id: "ntc-1",
    orderId: "ord-1",
    booking: "MAEU00000001",
    channel: "email",
    milestone: "departed",
    message: "MSKU0000006 departed Shanghai on Madrid Maersk.",
    sentAt: "2026-04-06T12:10:00Z",
  },
  {
    id: "ntc-2",
    orderId: "ord-1",
    booking: "MAEU00000001",
    channel: "in-app",
    milestone: "loaded",
    message: "MSKU0000006 was loaded at Shanghai.",
    sentAt: "2026-04-06T01:25:00Z",
  },
  {
    id: "ntc-3",
    orderId: "ord-2",
    booking: "HLCU00000002",
    channel: "email",
    milestone: "empty_returned",
    message: "HLCU0000014 was returned empty in Hamburg.",
    sentAt: "2026-05-13T07:30:00Z",
  },
]

export const sampleAlerts: Alert[] = [
  {
    id: "alt-1",
    orderId: "ord-1",
    booking: "MAEU00000001",
    container: "MSKU0000006",
    reason: "Vessel delayed by weather. Rolled to the next berth window.",
    originalEta: "2026-05-08T13:00:00+02:00",
    revisedEta: "2026-05-11T18:00:00+02:00",
  },
]

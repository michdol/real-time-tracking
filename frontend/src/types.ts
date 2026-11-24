export type OrderStatus = "active" | "historical"

export type Order = {
  id: string
  booking: string
  billOfLading: string
  container: string
  carrier: string
  origin: string
  destination: string
  status: OrderStatus
  milestone: string
  eta: string
}

export type Milestone = {
  name: string
  location: string
  happenedAt: string
}

export type Tracking = {
  order: Order
  milestones: Milestone[]
}

export type OrderQuery = {
  container: string
  booking: string
  billOfLading: string
  status: "all" | OrderStatus
}

export type Notice = {
  id: string
  orderId: string
  booking: string
  channel: "email" | "in-app"
  milestone: string
  message: string
  sentAt: string
}

export type Alert = {
  id: string
  orderId: string
  booking: string
  container: string
  reason: string
  originalEta: string
  revisedEta: string
}

export type DataSource = "api" | "sample"

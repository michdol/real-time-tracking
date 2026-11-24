import { sampleAlerts, sampleNotices, sampleOrders, sampleTracking } from "./sampleData"
import type { Alert, DataSource, Notice, Order, OrderQuery, Tracking } from "./types"

const base = import.meta.env.VITE_API_BASE ?? "http://localhost:8000"

export function matchesQuery(order: Order, query: OrderQuery): boolean {
  const container = query.container.trim().toLowerCase()
  const booking = query.booking.trim().toLowerCase()
  const bill = query.billOfLading.trim().toLowerCase()
  if (container && !order.container.toLowerCase().includes(container)) return false
  if (booking && !order.booking.toLowerCase().includes(booking)) return false
  if (bill && !order.billOfLading.toLowerCase().includes(bill)) return false
  if (query.status !== "all" && order.status !== query.status) return false
  return true
}

async function readJson<T>(path: string): Promise<T> {
  const response = await fetch(`${base}${path}`)
  if (!response.ok) throw new Error(String(response.status))
  return response.json() as Promise<T>
}

export async function getOrders(query: OrderQuery): Promise<{ orders: Order[]; source: DataSource }> {
  const params = new URLSearchParams()
  if (query.container) params.set("container", query.container)
  if (query.booking) params.set("booking", query.booking)
  if (query.billOfLading) params.set("billOfLading", query.billOfLading)
  if (query.status !== "all") params.set("status", query.status)
  try {
    const orders = await readJson<Order[]>(`/orders?${params}`)
    return { orders, source: "api" }
  } catch {
    return { orders: sampleOrders.filter((order) => matchesQuery(order, query)), source: "sample" }
  }
}

export async function getTracking(orderId: string): Promise<{ tracking: Tracking | null; source: DataSource }> {
  try {
    const tracking = await readJson<Tracking>(`/orders/${orderId}/tracking`)
    return { tracking, source: "api" }
  } catch {
    return { tracking: sampleTracking[orderId] ?? null, source: "sample" }
  }
}

export async function getNotices(): Promise<{ notices: Notice[]; source: DataSource }> {
  try {
    const notices = await readJson<Notice[]>("/notifications")
    return { notices, source: "api" }
  } catch {
    return { notices: sampleNotices, source: "sample" }
  }
}

export async function getAlerts(): Promise<{ alerts: Alert[]; source: DataSource }> {
  try {
    const alerts = await readJson<Alert[]>("/alerts")
    return { alerts, source: "api" }
  } catch {
    return { alerts: sampleAlerts, source: "sample" }
  }
}

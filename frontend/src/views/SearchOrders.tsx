import { useState, type FormEvent } from "react"
import { Link } from "react-router-dom"
import { getOrders } from "../api"
import { SourceBanner } from "../SourceBanner"
import type { DataSource, Order, OrderStatus } from "../types"

export function SearchOrders() {
  const [container, setContainer] = useState("")
  const [booking, setBooking] = useState("")
  const [billOfLading, setBillOfLading] = useState("")
  const [status, setStatus] = useState<"all" | OrderStatus>("all")
  const [orders, setOrders] = useState<Order[]>([])
  const [selected, setSelected] = useState<Order | null>(null)
  const [source, setSource] = useState<DataSource | null>(null)
  const [searched, setSearched] = useState(false)

  async function onSubmit(event: FormEvent) {
    event.preventDefault()
    const result = await getOrders({ container, booking, billOfLading, status })
    setOrders(result.orders)
    setSelected(result.orders[0] ?? null)
    setSource(result.source)
    setSearched(true)
  }

  return (
    <>
      <h1 className="h3">Orders</h1>
      <form className="row g-2 align-items-end mb-4" onSubmit={onSubmit}>
        <label className="col-sm-6 col-md-3">
          Container
          <input className="form-control" value={container} onChange={(event) => setContainer(event.target.value)} />
        </label>
        <label className="col-sm-6 col-md-3">
          Booking
          <input className="form-control" value={booking} onChange={(event) => setBooking(event.target.value)} />
        </label>
        <label className="col-sm-6 col-md-3">
          Bill of lading
          <input
            className="form-control"
            value={billOfLading}
            onChange={(event) => setBillOfLading(event.target.value)}
          />
        </label>
        <label className="col-sm-6 col-md-2">
          Status
          <select
            className="form-select"
            value={status}
            onChange={(event) => setStatus(event.target.value as "all" | OrderStatus)}
          >
            <option value="all">Active and historical</option>
            <option value="active">Active</option>
            <option value="historical">Historical</option>
          </select>
        </label>
        <div className="col-md-1">
          <button className="btn btn-primary" type="submit">
            Search
          </button>
        </div>
      </form>
      <SourceBanner source={source} />
      <div className="row g-4">
        <div className="col-lg-7">
          {searched && orders.length === 0 ? <p>No orders matched.</p> : null}
          {orders.length > 0 ? (
            <table className="table table-sm">
              <thead>
                <tr>
                  <th>Container</th>
                  <th>Booking</th>
                  <th>Route</th>
                  <th>Status</th>
                  <th></th>
                </tr>
              </thead>
              <tbody>
                {orders.map((order) => (
                  <tr key={order.id} className={selected?.id === order.id ? "table-active" : undefined}>
                    <td>{order.container}</td>
                    <td>{order.booking}</td>
                    <td>
                      {order.origin} to {order.destination}
                    </td>
                    <td>{order.status}</td>
                    <td>
                      <button className="btn btn-link btn-sm" type="button" onClick={() => setSelected(order)}>
                        Details
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          ) : null}
        </div>
        <div className="col-lg-5">
          {selected ? (
            <article className="card">
              <div className="card-body">
                <h2 className="h5">{selected.container}</h2>
                <p className="mb-1">Booking {selected.booking}</p>
                <p className="mb-1">Bill of lading {selected.billOfLading}</p>
                <p className="mb-1">Carrier {selected.carrier}</p>
                <p className="mb-1">
                  {selected.origin} to {selected.destination}
                </p>
                <p className="mb-1">Milestone {selected.milestone}</p>
                <p className="mb-3">ETA {selected.eta}</p>
                <Link className="btn btn-outline-primary" to={`/tracking/${selected.id}`}>
                  Real time tracking
                </Link>
              </div>
            </article>
          ) : (
            <p>Search, then choose an order to see its details.</p>
          )}
        </div>
      </div>
    </>
  )
}

import { useEffect, useState } from "react"
import { useParams } from "react-router-dom"
import { getTracking } from "../api"
import { routePicture } from "../routeMap"
import { SourceBanner } from "../SourceBanner"
import type { DataSource, Tracking } from "../types"

export function RealTimeTracking() {
  const { orderId = "" } = useParams()
  const [tracking, setTracking] = useState<Tracking | null>(null)
  const [source, setSource] = useState<DataSource | null>(null)
  const [missing, setMissing] = useState(false)

  useEffect(() => {
    let active = true
    getTracking(orderId).then((result) => {
      if (!active) return
      setTracking(result.tracking)
      setSource(result.source)
      setMissing(result.tracking === null)
    })
    return () => {
      active = false
    }
  }, [orderId])

  if (missing) return <p>No tracking for this order.</p>
  if (!tracking) return <p>Loading tracking.</p>

  const { order, milestones } = tracking
  return (
    <>
      <h1 className="h3">Tracking {order.container}</h1>
      <SourceBanner source={source} />
      <p>
        {order.origin} to {order.destination}. Status {order.status}. Current milestone {order.milestone}. ETA{" "}
        {order.eta}.
      </p>
      <pre className="border rounded p-3">{routePicture(order.origin, order.destination, order.milestone)}</pre>
      <table className="table table-sm">
        <thead>
          <tr>
            <th>Milestone</th>
            <th>Location</th>
            <th>When</th>
          </tr>
        </thead>
        <tbody>
          {milestones.map((milestone) => (
            <tr key={`${milestone.name}-${milestone.happenedAt}`}>
              <td>{milestone.name}</td>
              <td>{milestone.location}</td>
              <td>{milestone.happenedAt}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </>
  )
}

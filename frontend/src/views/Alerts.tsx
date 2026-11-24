import { useEffect, useState } from "react"
import { getAlerts } from "../api"
import { SourceBanner } from "../SourceBanner"
import type { Alert, DataSource } from "../types"

const actions = ["Accept new schedule", "Request reroute", "Escalate to operations"]

export function Alerts() {
  const [alerts, setAlerts] = useState<Alert[]>([])
  const [source, setSource] = useState<DataSource | null>(null)

  useEffect(() => {
    let active = true
    getAlerts().then((result) => {
      if (!active) return
      setAlerts(result.alerts)
      setSource(result.source)
    })
    return () => {
      active = false
    }
  }, [])

  return (
    <>
      <h1 className="h3">Alerts</h1>
      <SourceBanner source={source} />
      {alerts.length === 0 ? <p>No disruptions.</p> : null}
      <div className="d-grid gap-3">
        {alerts.map((alert) => (
          <article className="card" key={alert.id}>
            <div className="card-body">
              <h2 className="h5">
                {alert.container} · {alert.booking}
              </h2>
              <p>{alert.reason}</p>
              <p className="mb-1">Original ETA {alert.originalEta}</p>
              <p className="mb-3">Revised ETA {alert.revisedEta}</p>
              <div className="d-flex gap-2 flex-wrap">
                {actions.map((label) => (
                  <button className="btn btn-outline-primary btn-sm" type="button" key={label}>
                    {label}
                  </button>
                ))}
              </div>
            </div>
          </article>
        ))}
      </div>
    </>
  )
}

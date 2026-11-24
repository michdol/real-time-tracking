import { useEffect, useState } from "react"
import { getNotices } from "../api"
import { SourceBanner } from "../SourceBanner"
import type { DataSource, Notice } from "../types"

export function Notifications() {
  const [notices, setNotices] = useState<Notice[]>([])
  const [source, setSource] = useState<DataSource | null>(null)
  const [channel, setChannel] = useState<"all" | Notice["channel"]>("all")

  useEffect(() => {
    let active = true
    getNotices().then((result) => {
      if (!active) return
      setNotices(result.notices)
      setSource(result.source)
    })
    return () => {
      active = false
    }
  }, [])

  const visible = channel === "all" ? notices : notices.filter((notice) => notice.channel === channel)

  return (
    <>
      <h1 className="h3">Notifications and email</h1>
      <SourceBanner source={source} />
      <div className="btn-group mb-3" role="group" aria-label="Channel">
        <button className="btn btn-outline-secondary" type="button" onClick={() => setChannel("all")}>
          All
        </button>
        <button className="btn btn-outline-secondary" type="button" onClick={() => setChannel("in-app")}>
          In-app
        </button>
        <button className="btn btn-outline-secondary" type="button" onClick={() => setChannel("email")}>
          Email
        </button>
      </div>
      <ul className="list-group">
        {visible.map((notice) => (
          <li className="list-group-item" key={notice.id}>
            <div className="fw-semibold">
              {notice.channel} · {notice.milestone} · {notice.booking}
            </div>
            <div>{notice.message}</div>
            <div className="text-secondary small">{notice.sentAt}</div>
          </li>
        ))}
      </ul>
      {visible.length === 0 ? <p className="mt-3">No messages.</p> : null}
    </>
  )
}

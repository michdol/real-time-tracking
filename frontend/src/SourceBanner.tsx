import type { DataSource } from "./types"

export function SourceBanner({ source }: { source: DataSource | null }) {
  if (source !== "sample") return null
  return (
    <p className="alert alert-warning" role="status">
      Showing sample shipments. The API did not respond.
    </p>
  )
}

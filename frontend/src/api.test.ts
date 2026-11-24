import { matchesQuery } from "./api"
import { sampleOrders } from "./sampleData"

describe("matchesQuery", () => {
  it("filters by container and status", () => {
    const [active, historical] = sampleOrders
    const query = { container: "MSKU", booking: "", billOfLading: "", status: "active" as const }
    expect(matchesQuery(active, query)).toBe(true)
    expect(matchesQuery(historical, query)).toBe(false)
  })
})
import { render, screen } from "@testing-library/react"
import { MemoryRouter } from "react-router-dom"
import { Alerts } from "./Alerts"

describe("Alerts", () => {
  it("shows the three resolution actions", async () => {
    vi.stubGlobal("fetch", vi.fn(() => Promise.reject(new Error("no api"))))
    render(
      <MemoryRouter>
        <Alerts />
      </MemoryRouter>,
    )
    expect(await screen.findByRole("button", { name: "Accept new schedule" })).toBeInTheDocument()
    expect(screen.getByRole("button", { name: "Request reroute" })).toBeInTheDocument()
    expect(screen.getByRole("button", { name: "Escalate to operations" })).toBeInTheDocument()
  })
})

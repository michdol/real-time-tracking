import { routePicture } from "./routeMap"

describe("routePicture", () => {
  it("marks the current milestone", () => {
    const picture = routePicture("Shanghai", "Rotterdam", "departed")
    expect(picture).toContain("[at sea]")
    expect(picture).toContain("empty pickup Shanghai")
    expect(picture).toContain("arrived Rotterdam")
    expect(picture).not.toContain("[loaded]")
  })
})

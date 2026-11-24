const STEPS = [
  { milestone: "empty_pickup", label: "empty pickup" },
  { milestone: "gate_in", label: "gate in" },
  { milestone: "loaded", label: "loaded" },
  { milestone: "departed", label: "at sea" },
  { milestone: "arrived", label: "arrived" },
  { milestone: "discharged", label: "discharged" },
  { milestone: "gate_out", label: "gate out" },
  { milestone: "empty_returned", label: "empty returned" },
] as const

export function routePicture(origin: string, destination: string, milestone: string): string {
  return STEPS.map((step) => {
    const place =
      step.milestone === "empty_pickup"
        ? origin
        : step.milestone === "arrived" || step.milestone === "empty_returned"
          ? destination
          : ""
    const text = place ? `${step.label} ${place}` : step.label
    return step.milestone === milestone ? `[${text}]` : text
  }).join(" -- ")
}

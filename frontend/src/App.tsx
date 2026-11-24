import { NavLink, Route, Routes } from "react-router-dom"
import { Alerts } from "./views/Alerts"
import { Notifications } from "./views/Notifications"
import { RealTimeTracking } from "./views/RealTimeTracking"
import { SearchOrders } from "./views/SearchOrders"

const linkClass = ({ isActive }: { isActive: boolean }) =>
  isActive ? "nav-link active" : "nav-link"

export function App() {
  return (
    <>
      <nav className="navbar navbar-expand navbar-dark bg-dark">
        <div className="container">
          <span className="navbar-brand">RTT</span>
          <div className="navbar-nav">
            <NavLink className={linkClass} to="/" end>
              Orders
            </NavLink>
            <NavLink className={linkClass} to="/notifications">
              Notifications
            </NavLink>
            <NavLink className={linkClass} to="/alerts">
              Alerts
            </NavLink>
          </div>
        </div>
      </nav>
      <main className="container py-4">
        <Routes>
          <Route path="/" element={<SearchOrders />} />
          <Route path="/tracking/:orderId" element={<RealTimeTracking />} />
          <Route path="/notifications" element={<Notifications />} />
          <Route path="/alerts" element={<Alerts />} />
        </Routes>
      </main>
    </>
  )
}

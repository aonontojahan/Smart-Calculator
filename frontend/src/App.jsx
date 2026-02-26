import { Routes, Route, Navigate } from "react-router-dom"
import Login from "./pages/Login"
import Register from "./pages/Register"
import Calculator from "./pages/Calculator"
import ProtectedRoute from "./components/ProtectedRoute"
import { useAuth } from "./context/AuthContext"

function App() {
  const { token } = useAuth()

  return (
    <Routes>

      <Route
        path="/"
        element={
          <ProtectedRoute>
            <Calculator />
          </ProtectedRoute>
        }
      />

      <Route
        path="/login"
        element={
          token ? <Navigate to="/" replace /> : <Login />
        }
      />

      <Route
        path="/register"
        element={<Register />}
      />

      <Route
        path="*"
        element={<Navigate to="/" />}
      />

    </Routes>
  )
}

export default App
import { useState, useEffect } from "react"
import { useAuth } from "../context/AuthContext"
import { useTheme } from "../context/ThemeContext"
import { useNavigate } from "react-router-dom"

function Calculator() {
  const [expression, setExpression] = useState("")
  const [error, setError] = useState("")
  const [history, setHistory] = useState([])
  const [copied, setCopied] = useState(false)
  const [resultPulse, setResultPulse] = useState(false)

  const { token, logout } = useAuth()
  const { theme, toggleTheme } = useTheme()
  const navigate = useNavigate()

  const fetchHistory = async () => {
    try {
      const response = await fetch("http://127.0.0.1:8000/calculate/history", {
        headers: { Authorization: `Bearer ${token}` }
      })
      if (!response.ok) return
      const data = await response.json()
      setHistory(data)
    } catch {}
  }

  useEffect(() => {
    if (token) fetchHistory()
  }, [token])

  useEffect(() => {
    const handleKeyDown = (e) => {
      const allowedKeys = "0123456789+-*/%^()."
      if (allowedKeys.includes(e.key)) {
        setExpression((prev) => prev + e.key)
      }
      if (e.key === "Enter") handleClick("=")
      if (e.key === "Backspace") setExpression((prev) => prev.slice(0, -1))
      if (e.key === "Escape") {
        setExpression("")
        setError("")
      }
    }

    window.addEventListener("keydown", handleKeyDown)
    return () => window.removeEventListener("keydown", handleKeyDown)
  }, [expression])

  const handleClick = async (value) => {
    if (value === "=") {
      if (!expression) return
      try {
        setError("")
        const response = await fetch("http://127.0.0.1:8000/calculate/evaluate", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`
          },
          body: JSON.stringify({ expression })
        })

        const data = await response.json()
        if (!response.ok) throw new Error(data.detail || "Calculation failed")

        setExpression(String(data.result))
        setResultPulse(true)
        setTimeout(() => setResultPulse(false), 300)
        fetchHistory()
      } catch (err) {
        setError(err.message)
      }
      return
    }

    setExpression((prev) => prev + value)
  }

  const copyResult = async () => {
    if (!expression) return
    await navigator.clipboard.writeText(expression)
    setCopied(true)
    setTimeout(() => setCopied(false), 1500)
  }

  const handleClear = () => {
    setExpression("")
    setError("")
  }

  const handleBackspace = () => {
    setExpression((prev) => prev.slice(0, -1))
  }

  const deleteSingle = async (id) => {
    await fetch(`http://127.0.0.1:8000/calculate/history/${id}`, {
      method: "DELETE",
      headers: { Authorization: `Bearer ${token}` }
    })
    fetchHistory()
  }

  const deleteAll = async () => {
    await fetch("http://127.0.0.1:8000/calculate/history", {
      method: "DELETE",
      headers: { Authorization: `Bearer ${token}` }
    })
    fetchHistory()
  }

  const handleLogout = () => {
    logout()
    navigate("/login")
  }

  return (
    <div className="min-h-screen bg-gray-100 dark:bg-gradient-to-br dark:from-indigo-900 dark:via-purple-900 dark:to-gray-900 flex items-center justify-center p-6 transition-all duration-500 fade-in">

      <div className="flex gap-6 w-full max-w-6xl">

        {/* Sidebar */}
        <div className="hidden md:block w-80 backdrop-blur-lg bg-white/70 dark:bg-white/10 border border-gray-200 dark:border-white/20 shadow-2xl rounded-2xl p-4 overflow-y-auto max-h-[600px] transition-all duration-500 hover:shadow-3xl">

          <div className="flex justify-between items-center mb-4">
            <h2 className="text-gray-800 dark:text-white text-xl font-semibold">
              History
            </h2>

            <button
              onClick={deleteAll}
              className="text-xs bg-red-600 hover:bg-red-700 text-white px-3 py-1 rounded-lg btn-press"
            >
              Clear All
            </button>
          </div>

          {history.map((item) => (
            <div
              key={item.id}
              className="bg-gray-200 dark:bg-white/10 rounded-lg p-3 mb-3 transition-all hover:scale-[1.02]"
            >
              <div
                onClick={() => setExpression(item.expression)}
                className="cursor-pointer"
              >
                <div className="text-gray-600 dark:text-gray-300 text-sm">
                  {item.expression}
                </div>
                <div className="text-gray-900 dark:text-white font-semibold">
                  = {item.result}
                </div>
              </div>

              <button
                onClick={() => deleteSingle(item.id)}
                className="mt-2 text-xs bg-red-500 hover:bg-red-600 text-white px-2 py-1 rounded btn-press"
              >
                Delete
              </button>
            </div>
          ))}
        </div>

        {/* Calculator */}
        <div className="flex-1 backdrop-blur-lg bg-white/70 dark:bg-white/10 border border-gray-200 dark:border-white/20 shadow-2xl rounded-2xl p-6 transition-all duration-500">

          <div className="flex justify-between items-center mb-6">
            <h1 className="text-3xl font-bold text-gray-900 dark:text-white">
              SmartCalc
            </h1>

            <div className="flex gap-3">
              <button
                onClick={toggleTheme}
                className="bg-indigo-600 hover:bg-indigo-700 text-white px-4 py-2 rounded-xl text-sm btn-press"
              >
                {theme === "dark" ? "Light Mode" : "Dark Mode"}
              </button>

              <button
                onClick={handleLogout}
                className="bg-gray-700 hover:bg-gray-800 text-white px-4 py-2 rounded-xl text-sm btn-press"
              >
                Logout
              </button>
            </div>
          </div>

          {/* Display */}
          <div className={`bg-gray-200 dark:bg-black/40 rounded-xl p-4 mb-2 transition-all ${resultPulse ? "scale-[1.02]" : ""}`}>
            <input
              type="text"
              value={expression}
              readOnly
              className="w-full bg-transparent text-right text-2xl text-gray-900 dark:text-white outline-none"
              placeholder="0"
            />

            <div className="flex justify-end mt-3">
              <button
                onClick={copyResult}
                className="text-xs bg-green-500 hover:bg-green-600 text-white px-3 py-1 rounded-lg btn-press"
              >
                {copied ? "Copied!" : "Copy Result"}
              </button>
            </div>
          </div>

          {error && (
            <div className="text-red-500 text-sm mb-3 text-right">
              {error}
            </div>
          )}

          <div className="grid grid-cols-2 gap-3 mb-4">
            <button
              onClick={handleClear}
              className="bg-red-500 hover:bg-red-600 text-white rounded-xl py-3 font-semibold btn-press"
            >
              Clear
            </button>

            <button
              onClick={handleBackspace}
              className="bg-yellow-500 hover:bg-yellow-600 text-white rounded-xl py-3 font-semibold btn-press"
            >
              Backspace
            </button>
          </div>

          <div className="grid grid-cols-5 gap-3">
            {[
              "sin(","cos(","tan(","sqrt(","log(",
              "log10(","ln(","factorial(","pi","^",
              "7","8","9","/","%",
              "4","5","6","*","(",
              "1","2","3","-",
              ")", "0",".","=","+"
            ].map((btn) => (
              <button
                key={btn}
                onClick={() => handleClick(btn)}
                className="bg-gray-300 dark:bg-white/20 hover:bg-gray-400 dark:hover:bg-white/30 text-gray-900 dark:text-white rounded-xl py-3 text-sm font-semibold shadow-md btn-press"
                
              >
                {btn}
              </button>
            ))}
          </div>

        </div>
      </div>
    </div>
  )
}

export default Calculator
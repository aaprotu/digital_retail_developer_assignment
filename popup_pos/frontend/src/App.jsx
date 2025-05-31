import { useState } from 'react'
import './App.css'

function App() {
  const [email, setEmail] = useState('')
  const [amount, setAmount] = useState('')
  const [currency, setCurrency] = useState('EUR')
  const [response, setResponse] = useState(null)
  const [loading, setLoading] = useState(false)

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    try {
      const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'
      const res = await fetch(`${API_URL}/pay`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, amount: parseFloat(amount), currency })
      })
      const data = await res.json()
      setResponse(data)
    } catch (err) {
      setResponse({ error: 'Something went wrong.', details: err.message })
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="page-container">
      <h1 className="title">MARIMEKKO POS</h1>
      <div className="form-container">
        <h2>Simple payment app</h2>
        <form onSubmit={handleSubmit}>
          <input
            type="email"
            placeholder="Email address"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
          <input
            type="number"
            placeholder="Amount"
            value={amount}
            onChange={(e) => setAmount(e.target.value)}
            required
          />
          <select value={currency} onChange={(e) => setCurrency(e.target.value)}>
            <option value="EUR">EUR</option>
            <option value="USD">USD</option>
            <option value="GBP">GBP</option>
            <option value="SEK">SEK</option>
            <option value="NOK">NOK</option>
            <option value="AUD">AUD</option>
            <option value="NZD">NZD</option>
            <option value="DKK">DKK</option>
          </select>
          <button type="submit" disabled={loading}>
            {loading ? 'Processing...' : 'Submit Payment'}
          </button>
        </form>

        {response && (
          <div className="response">
            <pre>{JSON.stringify(response, null, 2)}</pre>
          </div>
        )}
      </div>
    </div>
  )

}

export default App

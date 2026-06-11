import { useState } from 'react'
import { shorten } from './api'
import './App.css'

function App() {
  const [url, setUrl] = useState('')
  const [links, setLinks] = useState([])
  const [error, setError] = useState('')

  async function handleSubmit(e) {
    e.preventDefault()
    setError('')
    try {
      const link = await shorten(url)
      setLinks([link, ...links])
      setUrl('')
    } catch (err) {
      setError(err.message)
    }
  }

  return (
    <main className="app">
      <h1>openbitly</h1>

      <form onSubmit={handleSubmit}>
        <input
          type="url"
          required
          placeholder="Paste a long URL"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
        />
        <button type="submit">Shorten</button>
      </form>

      {error && <p className="error">{error}</p>}

      <ul className="links">
        {links.map((link) => (
          <li key={link.code}>
            <a href={link.short_url}>{link.short_url}</a> → {link.long_url}
          </li>
        ))}
      </ul>
    </main>
  )
}

export default App

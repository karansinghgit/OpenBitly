import { useEffect, useState } from 'react'
import { listLinks, shorten } from './api'
import './App.css'

function App() {
  const [url, setUrl] = useState('')
  const [links, setLinks] = useState([])
  const [error, setError] = useState('')
  const [submitting, setSubmitting] = useState(false)
  const [copiedCode, setCopiedCode] = useState('')

  useEffect(() => {
    listLinks()
      .then(setLinks)
      .catch((err) => setError(err.message))
  }, [])

  async function handleSubmit(e) {
    e.preventDefault()
    setError('')
    setSubmitting(true)
    try {
      const link = await shorten(url)
      setLinks([link, ...links])
      setUrl('')
    } catch (err) {
      setError(err.message)
    } finally {
      setSubmitting(false)
    }
  }

  async function handleCopy(link) {
    try {
      await navigator.clipboard.writeText(link.short_url)
      setCopiedCode(link.code)
      setTimeout(() => setCopiedCode(''), 1500)
    } catch {
      setError('Could not copy to clipboard')
    }
  }

  return (
    <div className="page">
      <header className="header">
        <div className="header__inner">
          <span className="logo">
            open<span className="logo__accent">bit.ly</span>
          </span>
          <span className="tagline">Shorten links in a click</span>
        </div>
      </header>

      <main className="container">
        <section className="card form-card">
          <h1 className="form-card__title">Shorten a new link</h1>
          <form className="form" onSubmit={handleSubmit}>
            <input
              className="form__input"
              type="url"
              required
              placeholder="Paste a long URL…"
              value={url}
              onChange={(e) => setUrl(e.target.value)}
            />
            <button className="form__button" type="submit" disabled={submitting}>
              {submitting ? 'Shortening…' : 'Shorten'}
            </button>
          </form>
          {error && <p className="error">{error}</p>}
        </section>

        <section className="links">
          {links.length === 0 ? (
            <p className="links__empty">No links yet — shorten one above to get started.</p>
          ) : (
            <ul className="links__list">
              {links.map((link) => (
                <li key={link.code} className="card link">
                  <div className="link__main">
                    <div className="link__short-row">
                      <a className="link__short" href={link.short_url} target="_blank" rel="noreferrer">
                        {link.short_url}
                      </a>
                      <button
                        className="link__copy"
                        type="button"
                        onClick={() => handleCopy(link)}
                        title="Copy short URL"
                      >
                        {copiedCode === link.code ? 'Copied' : 'Copy'}
                      </button>
                    </div>
                    <span className="link__destination" title={link.long_url}>
                      {link.long_url}
                    </span>
                  </div>
                  <span className="link__clicks" title="Total clicks">
                    <strong>{link.click_count}</strong>
                    {link.click_count === 1 ? ' click' : ' clicks'}
                  </span>
                </li>
              ))}
            </ul>
          )}
        </section>
      </main>
    </div>
  )
}

export default App

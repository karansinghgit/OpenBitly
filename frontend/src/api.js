export async function listLinks(codes) {
  if (!codes.length) return []
  const query = codes.map(encodeURIComponent).join(',')
  const res = await fetch(`/api/links?codes=${query}`)
  const data = await res.json()
  if (!res.ok) {
    throw new Error(data.error || 'Could not load links')
  }
  return data.links
}

export async function shorten(url) {
  const res = await fetch('/api/shorten', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ url }),
  })
  const data = await res.json()
  if (!res.ok) {
    throw new Error(data.error || 'Something went wrong')
  }
  return data
}

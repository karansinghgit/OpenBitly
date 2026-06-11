// Remembers which short codes this browser created (newest first). Only the
// codes are stored locally — the links themselves live in the database, so
// clearing this never deletes anything, it just empties this browser's list.
const KEY = 'openbitly.codes'

export function getCodes() {
  try {
    return JSON.parse(localStorage.getItem(KEY)) || []
  } catch {
    return []
  }
}

export function addCode(code) {
  const codes = getCodes().filter((c) => c !== code)
  codes.unshift(code)
  localStorage.setItem(KEY, JSON.stringify(codes))
}

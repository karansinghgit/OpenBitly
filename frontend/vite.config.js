import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// In dev, the React app runs on :5173 and forwards /api calls to Django on
// :8000, so both sides are same-origin and there's no CORS to deal with.
export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      // 127.0.0.1, not localhost: avoids Node resolving localhost to IPv6 (::1).
      '/api': 'http://127.0.0.1:8000',
    },
  },
})

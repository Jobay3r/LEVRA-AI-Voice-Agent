import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

/**
 * Vite Configuration
 * 
 * This configuration:
 * 1. Adds React plugin support for JSX and HMR
 * 2. Sets up an API proxy to forward requests to the backend server
 *    - Requests to /api are forwarded to localhost:5001
 *    - The /api prefix is stripped when forwarding
 * 
 * This allows the frontend to make relative API calls that are proxied
 * to the appropriate backend endpoint during development.
 */
export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      "/api": {
        target: "http://localhost:5001",
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, "")
      }
    }
  }
})

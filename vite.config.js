import { defineConfig } from 'vite'
import { svelte } from '@sveltejs/vite-plugin-svelte'

// https://vite.dev/config/
export default defineConfig({
  server: {
    host: '0.0.0.0',
    allowedHosts: [
      "nustkd-attendance-app-e897e90f665b.herokuapp.com/"
    ]
  },
  plugins: [svelte()],
})

import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000,
    // Proxy disabled - frontend will use VITE_API_URL from .env.local
    proxy: {},
  },
});

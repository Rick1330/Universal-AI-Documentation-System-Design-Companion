import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import tailwindcss from "@tailwindcss/vite";
import path from "path";

// https://vite.dev/config/
export default defineConfig({
  plugins: [react(), tailwindcss()],
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },
  server: {
    proxy: {
      "/api": {
        target: "http://localhost:8000",
        changeOrigin: true,
        secure: false,
      },
    },
    port: 3000, // Optional: specify a port for the dev server
    host: "0.0.0.0", // Optional: make it accessible externally if needed
    allowedHosts: ["3003-irmqj6k5szpiwa1k7xa2s-518dece1.manusvm.computer", "3004-idub5neusrw9om2vhfvi9-518dece1.manusvm.computer", "3005-idub5neusrw9om2vhfvi9-518dece1.manusvm.computer"],
  },
});


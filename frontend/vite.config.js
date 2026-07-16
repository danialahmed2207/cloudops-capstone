import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    // Alle /api-Requests gehen im Dev-Modus ans FastAPI-Backend.
    // In Produktion übernimmt das später Nginx (gleiche Pfad-Konvention).
    proxy: {
      '/api': 'http://localhost:8000',
    },
    // Der Projektpfad enthält einen Doppelpunkt ("Speicher: Macbook"),
    // den Vites Allow-List-Prüfung als Windows-Laufwerk fehlinterpretiert.
    // Nur für lokale Entwicklung relevant, nicht für den Build.
    fs: { strict: false },
  },
})

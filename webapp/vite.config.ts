import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    allowedHosts: [
      'sour-clocks-repair.loca.lt', // Добавь свой текущий адрес из ошибки
    ],
    // Или, если хочешь разрешить вообще любые туннели (удобно для тестов):
    // allowedHosts: true 
  }
})

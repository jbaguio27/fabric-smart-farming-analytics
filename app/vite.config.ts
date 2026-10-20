import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'
import path from 'path'

const BASE_PATH = '/fabric-smart-farming-analytics/'

function assetBasePlugin(base: string) {
  return {
    name: 'vite-plugin-asset-base',
    enforce: 'pre' as const,
    transform(code: string, id: string) {
      if (
        !id.includes('node_modules') &&
        (id.endsWith('.tsx') || id.endsWith('.jsx') || id.endsWith('.ts') || id.endsWith('.js'))
      ) {
        return code.replace(/(['"])\/assets\//g, `$1${base}assets/`)
      }
    },
  }
}

// https://vite.dev/config/
export default defineConfig(({ command }) => {
  const isBuild = command === 'build'
  const base = isBuild ? BASE_PATH : '/'

  return {
    base,
    plugins: [
      assetBasePlugin(base),
      react(),
      tailwindcss(),
    ],
    resolve: {
      alias: {
        '@': path.resolve(import.meta.dirname, './src'),
      },
    },
  }
})

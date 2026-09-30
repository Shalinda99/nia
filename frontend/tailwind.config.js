/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,jsx,ts,tsx}'],
  theme: {
    extend: {
      colors: {
        clinical: {
          50:  '#f0f4ff',
          100: '#dde6ff',
          200: '#c4d2ff',
          300: '#9fb4ff',
          400: '#7a8eff',
          500: '#5a6aff',
          600: '#3d47f5',
          700: '#3035e0',
          800: '#2a2db5',
          900: '#272d8e',
          950: '#181a5c',
        },
        slate: {
          850: '#172033',
          900: '#0f172a',
          950: '#080c19',
        },
      },
      animation: {
        'pulse-slow': 'pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'ping-slow': 'ping 2s cubic-bezier(0, 0, 0.2, 1) infinite',
        'bounce-subtle': 'bounce 2s infinite',
        'waveform': 'waveform 1.2s ease-in-out infinite',
      },
      keyframes: {
        waveform: {
          '0%, 100%': { transform: 'scaleY(0.3)' },
          '50%': { transform: 'scaleY(1)' },
        },
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
        mono: ['JetBrains Mono', 'monospace'],
      },
    },
  },
  plugins: [],
}

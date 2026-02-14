/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'brand-orange': '#F28C18',
        'brand-green': '#2E7D32',
        'light-bg': '#FFFFFF',
        'light-surface': '#F8FAFC',
        'light-text': '#111827',
        'light-text-secondary': '#6B7280',
        'light-border': '#E5E7EB',
      },
    },
  },
  plugins: [],
}

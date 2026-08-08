/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#fbf0e8',
          100: '#f5dcc7',
          200: '#eab98f',
          300: '#dd9660',
          400: '#d17f45',
          500: '#c8703f',
          600: '#a85a30',
          700: '#874726',
          800: '#66351d',
          900: '#452414',
        }
      }
    },
  },
  plugins: [],
}

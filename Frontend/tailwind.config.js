/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./pages/**/*.{js,ts,jsx,tsx}",
    "./components/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    fontFamily: {
      'Lato': ['Lato', "sans-serif"]
    },
    extend: {
      backgroundImage: {
        'body-bg': "url('../assets/svgs/bodybg.svg')"
      },
      animation: {
        grow: 'grow 500ms linear 0s infinite',
      },
      keyframes: {
        grow: {
          from: { transform: 'scale(0, 0)', opacity: 0 },
          to: { transform: 'scale(1, 1)', opacity: 1 }
          // '0%, 100%': { transform: 'rotate(-3deg)' },
          // '50%': { transform: 'rotate(3deg)' },
        }
      }
    },
  },
  plugins: [],
}

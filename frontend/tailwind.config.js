/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: '#1B4F72',
        accent: '#2471A3',
        success: '#1E8449',
        warning: '#D35400',
        danger: '#C0392B',
      },
    },
  },
  plugins: [],
}

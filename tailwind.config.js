/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./templates/**/*.html", "./static/js/**/*.js"],
  theme: {
    extend: {
      fontFamily: {
        sans: ["Inter", "ui-sans-serif", "system-ui", "sans-serif"],
      },
    },
  },
  safelist: [
    { pattern: /^(bg|text|hover:bg)-(red|amber|green|indigo)-(100|200|700)$/ },
  ],
  plugins: [],
};

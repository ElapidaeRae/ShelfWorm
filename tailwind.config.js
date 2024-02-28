/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: 'selector',
  content: [
      './templates/**/*.html',
      './static/**/*.js',
  ],
  theme: {
    extend: {},
    colors: {
        'primary': '#1c9eca',
        'secondary': '#470283',
        'accent': '#ad02c0',
        'background': {'light': '#f5f5f5', 'dark': '#1a202c', DEFAULT: '#f5f5f5'},
        'text': {'light': '#052029', 'dark': '#d6f1fa', DEFAULT: '#052029'},
      },
    fontFamily: {
            'sans': ['Poppins', 'sans-serif'],
            'serif': ['"El Messiri"', 'serif'],
          },
  },
  plugins: [
      require('autoprefixer'),
      require('tailwindcss'),
      '@tailwindcss/forms',
      '@tailwindcss/typography',
  ],
}

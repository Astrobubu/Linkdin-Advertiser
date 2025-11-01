import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        linkedin: {
          50: '#e8f4fd',
          100: '#d0e8fb',
          200: '#a1d2f7',
          300: '#72bbf3',
          400: '#43a5ef',
          500: '#0a66c2',
          600: '#08529b',
          700: '#063d74',
          800: '#04294e',
          900: '#021427',
        },
      },
    },
  },
  plugins: [],
};

export default config;

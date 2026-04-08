import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        // South African flag colors
        sa: {
          red: '#E03C31',
          blue: '#001489',
          green: '#007A4D',
          yellow: '#FFB81C',
          black: '#000000',
          white: '#FFFFFF',
        },
        primary: {
          50: '#e6f7f1',
          100: '#b3e6d4',
          200: '#80d5b7',
          300: '#4dc49a',
          400: '#1ab37d',
          500: '#007A4D', // SA Green
          600: '#006240',
          700: '#004a30',
          800: '#003220',
          900: '#001a10',
        },
      },
    },
  },
  plugins: [],
};

export default config;

import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        ink: {
          950: "#0a0a0b",
          900: "#121214",
          800: "#1a1a1d",
          700: "#242428",
          600: "#2e2e33",
        },
        gold: {
          300: "#f5d87a",
          400: "#eec84f",
          500: "#d9ad2b",
          600: "#b78d1a",
        },
      },
    },
  },
  plugins: [],
};
export default config;

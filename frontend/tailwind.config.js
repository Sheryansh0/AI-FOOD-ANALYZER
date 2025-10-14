/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      colors: {
        "neon-blue": "#00f3ff",
        "neon-purple": "#b537ff",
        "neon-pink": "#ff006e",
        "dark-bg": "#0a0a0f",
        "card-bg": "#1a1a2e",
      },
      animation: {
        glow: "glow 2s ease-in-out infinite alternate",
        float: "float 3s ease-in-out infinite",
        "pulse-slow": "pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite",
      },
      keyframes: {
        glow: {
          "0%": {
            boxShadow: "0 0 5px #00f3ff, 0 0 10px #00f3ff, 0 0 15px #00f3ff",
          },
          "100%": {
            boxShadow: "0 0 10px #00f3ff, 0 0 20px #00f3ff, 0 0 30px #00f3ff",
          },
        },
        float: {
          "0%, 100%": { transform: "translateY(0px)" },
          "50%": { transform: "translateY(-10px)" },
        },
      },
    },
  },
  plugins: [],
};

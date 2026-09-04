import type { Config } from "tailwindcss";

const config: Config = {
  darkMode: "class",
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        google: {
          navy: {
            DEFAULT: "#0B3D91",
            hover: "#082E6E",
            active: "#062252",
          },
          blue: {
            DEFAULT: "#1A73E8",
            hover: "#1557B0",
            tint: "#E8F0FE",
            text: "#1A73E8",
          },
          surface: "#FFFFFF",
          bg: "#F8F9FA",
          border: {
            DEFAULT: "#DADCE0",
            hover: "#BDC1C6",
            focus: "#0B3D91",
          },
          text: {
            primary: "#202124",
            secondary: "#5F6368",
            disabled: "#80868B",
            inverse: "#FFFFFF",
          },
          success: {
            DEFAULT: "#1E8E3E",
            tint: "#E6F4EA",
            text: "#137333",
            border: "#CEEAD6",
          },
          error: {
            DEFAULT: "#D93025",
            tint: "#FCE8E6",
            text: "#C5221F",
            border: "#FAD2CF",
          },
          warning: {
            DEFAULT: "#E37400",
            tint: "#FEF7E0",
            text: "#B06000",
            border: "#FEEFC3",
          },
          hover: "#F1F3F4",
        },
      },
      fontFamily: {
        sans: [
          "var(--font-roboto)",
          "Roboto",
          "-apple-system",
          "BlinkMacSystemFont",
          '"Segoe UI"',
          "system-ui",
          "sans-serif",
        ],
      },
      fontSize: {
        "page-title": ["22px", { lineHeight: "28px", fontWeight: "500" }],
        "section-header": ["16px", { lineHeight: "24px", fontWeight: "500" }],
        "body-text": ["14px", { lineHeight: "20px", fontWeight: "400" }],
        "caption-text": ["12px", { lineHeight: "16px", fontWeight: "400" }],
        "button-text": [
          "14px",
          { lineHeight: "20px", letterSpacing: "0.25px", fontWeight: "500" },
        ],
      },
      borderRadius: {
        "google-sm": "4px",
        "google-md": "8px",
        "google-pill": "9999px",
      },
      boxShadow: {
        "google-elevation-1":
          "0 1px 2px 0 rgba(60,64,67,0.3), 0 1px 3px 1px rgba(60,64,67,0.15)",
        "google-elevation-2":
          "0 1px 2px 0 rgba(60,64,67,0.3), 0 2px 6px 2px rgba(60,64,67,0.15)",
        "google-hover": "0 1px 3px 0 rgba(60,64,67,0.2)",
      },
      spacing: {
        "grid-1": "8px",
        "grid-2": "16px",
        "grid-3": "24px",
        "grid-4": "32px",
        "grid-5": "40px",
        "grid-6": "48px",
      },
    },
  },
  plugins: [],
};

export default config;

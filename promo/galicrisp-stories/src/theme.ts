// theme.ts — single source of truth. Never inline colours or easings.
import { Easing } from "remotion";

export const theme = {
  colors: {
    bg: "#2A1A0E", // warm bakery brown base
    primary: "#C8102E", // GaliCrisp red — hero, max one element per frame
    accent: "#E8A33D", // golden crust
    text: "#FFF8EC",
    textDim: "#F4E9DA",
    shadow: "rgba(25, 12, 5, 0.55)",
    glow: "rgba(200, 16, 46, 0.4)",
  },
  fonts: {
    display: "InterXB",
    body: "InterDisplayMedium",
  },
  ease: {
    out: Easing.bezier(0.16, 1, 0.3, 1),
    inOut: Easing.bezier(0.83, 0, 0.17, 1),
    in: Easing.bezier(0.7, 0, 0.84, 0),
  },
  spring: {
    snappy: { damping: 14, stiffness: 160, mass: 0.6 },
    smooth: { damping: 20, stiffness: 90, mass: 1 },
    bouncy: { damping: 11, stiffness: 170, mass: 0.7 },
  },
} as const;

// Timeline in seconds; components convert with fps.
export const beats = {
  packIn: 0,
  headline: 0.35,
  pill: 0.95,
  badges: 1.55,
  sheen: 1.8,
  textOut: 3.3,
  cta: 3.55,
  end: 5,
} as const;

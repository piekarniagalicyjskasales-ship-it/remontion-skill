import React from "react";
import {
  AbsoluteFill,
  Img,
  interpolate,
  spring,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";
import { theme } from "./theme";

const clamp = { extrapolateLeft: "clamp", extrapolateRight: "clamp" } as const;

export const sec = (fps: number, s: number) => Math.round(s * fps);

/** Fades + rises + scales out, faster than the entrance. */
export const useExit = (at: number, frames = 10) => {
  const frame = useCurrentFrame();
  const p = interpolate(frame, [at, at + frames], [0, 1], { ...clamp, easing: theme.ease.in });
  return { opacity: 1 - p, transform: `translateY(${-40 * p}px) scale(${1 - 0.04 * p})` };
};

export const KenBurns: React.FC<{ src: string }> = ({ src }) => {
  const frame = useCurrentFrame();
  const { durationInFrames } = useVideoConfig();
  const scale = interpolate(frame, [0, durationInFrames], [1.0, 1.09], { ...clamp, easing: theme.ease.inOut });
  const pan = interpolate(frame, [0, durationInFrames], [0, -22], { ...clamp, easing: theme.ease.inOut });
  return (
    <AbsoluteFill style={{ overflow: "hidden", backgroundColor: theme.colors.bg }}>
      <Img
        src={staticFile(src)}
        style={{ width: "100%", height: "100%", objectFit: "cover", transform: `scale(${scale}) translateX(${pan}px)` }}
      />
    </AbsoluteFill>
  );
};

/** The real pack: rises in, settles, breathes; a light sheen sweeps across it. */
export const Pack: React.FC<{ delay: number; sheenAt: number; height: number; bottom: number }> = ({
  delay,
  sheenAt,
  height,
  bottom,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const p = spring({ frame: frame - delay, fps, config: theme.spring.smooth });
  const y = interpolate(p, [0, 1], [320, 0]);
  const scale = interpolate(p, [0, 1], [0.86, 1]);
  const rot = interpolate(p, [0, 1], [-5, 0]);
  const breathe = Math.sin(frame / 26) * 5;
  const sheen = interpolate(frame, [sheenAt, sheenAt + sec(fps, 0.8)], [-60, 160], { ...clamp, easing: theme.ease.inOut });
  const mask = `url(${staticFile("product.png")})`;
  return (
    <div
      style={{
        position: "absolute",
        left: "50%",
        bottom,
        height,
        transform: `translateX(-50%) translateY(${y + breathe}px) scale(${scale}) rotate(${rot}deg)`,
        transformOrigin: "50% 100%",
        opacity: p,
      }}
    >
      {/* contact shadow */}
      <div
        style={{
          position: "absolute",
          left: "-12%",
          right: "-12%",
          bottom: -26,
          height: 60,
          borderRadius: "50%",
          background: `radial-gradient(ellipse at center, ${theme.colors.shadow}, transparent 70%)`,
          filter: "blur(10px)",
          transform: `scaleX(${1 - breathe / 120})`,
        }}
      />
      <Img
        src={staticFile("product.png")}
        style={{ height: "100%", display: "block", filter: `drop-shadow(18px 30px 40px ${theme.colors.shadow})` }}
      />
      {/* sheen masked to the pack silhouette */}
      <div
        style={{
          position: "absolute",
          inset: 0,
          WebkitMaskImage: mask,
          maskImage: mask,
          WebkitMaskSize: "100% 100%",
          maskSize: "100% 100%",
          background: `linear-gradient(105deg, transparent ${sheen - 18}%, rgba(255,255,255,0.38) ${sheen}%, transparent ${sheen + 18}%)`,
          mixBlendMode: "screen",
        }}
      />
    </div>
  );
};

export const Badge: React.FC<{ src: string; delay: number; size: number; style: React.CSSProperties }> = ({
  src,
  delay,
  size,
  style,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const p = spring({ frame: frame - delay, fps, config: theme.spring.bouncy });
  const float = Math.sin((frame + delay * 3) / 22) * 4;
  return (
    <Img
      src={staticFile(src)}
      style={{
        position: "absolute",
        width: size,
        opacity: Math.min(1, p * 1.4),
        transform: `translateY(${float + interpolate(p, [0, 1], [30, 0])}px) scale(${interpolate(p, [0, 1], [0.4, 1])}) rotate(${interpolate(p, [0, 1], [-25, 0])}deg)`,
        filter: `drop-shadow(6px 12px 18px ${theme.colors.shadow})`,
        ...style,
      }}
    />
  );
};

export const WordReveal: React.FC<{ text: string; delay: number; per?: number; size: number; color?: string; family?: string }> = ({
  text,
  delay,
  per = 3,
  size,
  color = theme.colors.text,
  family = theme.fonts.display,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  return (
    <div
      style={{
        display: "flex",
        flexWrap: "wrap",
        justifyContent: "center",
        gap: Math.round(size * 0.26),
        fontFamily: family,
        fontSize: size,
        lineHeight: 1.05,
        letterSpacing: "-0.03em",
        color,
        textShadow: `0 4px 30px rgba(0,0,0,0.45)`,
      }}
    >
      {text.split(" ").map((word, i) => {
        const p = spring({ frame: frame - delay - i * per, fps, config: theme.spring.snappy });
        return (
          <span
            key={i}
            style={{
              display: "inline-block",
              opacity: p,
              transform: `translateY(${interpolate(p, [0, 1], [40, 0])}px) scale(${interpolate(p, [0, 1], [0.92, 1])})`,
            }}
          >
            {word}
          </span>
        );
      })}
    </div>
  );
};

export const Pill: React.FC<{ text: string; delay: number; size: number }> = ({ text, delay, size }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const p = spring({ frame: frame - delay, fps, config: theme.spring.snappy });
  const tp = spring({ frame: frame - delay - 4, fps, config: theme.spring.snappy });
  return (
    <div
      style={{
        display: "inline-block",
        padding: `${Math.round(size * 0.35)}px ${Math.round(size * 0.75)}px`,
        borderRadius: size,
        background: theme.colors.primary,
        boxShadow: `0 0 50px ${theme.colors.glow}`,
        transform: `scale(${interpolate(p, [0, 1], [0.6, 1])})`,
        opacity: p,
      }}
    >
      <span
        style={{
          display: "inline-block",
          fontFamily: theme.fonts.body,
          fontSize: size,
          color: theme.colors.text,
          opacity: tp,
          transform: `translateY(${interpolate(tp, [0, 1], [14, 0])}px)`,
        }}
      >
        {text}
      </span>
    </div>
  );
};

export const Grade: React.FC = () => (
  <AbsoluteFill style={{ pointerEvents: "none" }}>
    <AbsoluteFill style={{ backgroundColor: theme.colors.accent, mixBlendMode: "soft-light", opacity: 0.14 }} />
    <AbsoluteFill
      style={{
        background: "linear-gradient(180deg, rgba(20,10,4,0.45), transparent 26%, transparent 70%, rgba(20,10,4,0.35))",
      }}
    />
  </AbsoluteFill>
);

export const Grain: React.FC = () => {
  const frame = useCurrentFrame();
  const noise = `url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='220' height='220'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='2'/%3E%3C/filter%3E%3Crect width='220' height='220' filter='url(%23n)' opacity='0.5'/%3E%3C/svg%3E")`;
  return (
    <AbsoluteFill
      style={{
        pointerEvents: "none",
        backgroundImage: noise,
        backgroundSize: "220px",
        backgroundPosition: `${(frame * 7) % 220}px ${(frame * 13) % 220}px`,
        opacity: 0.06,
        mixBlendMode: "multiply",
      }}
    />
  );
};

export const Vignette: React.FC = () => (
  <AbsoluteFill
    style={{ pointerEvents: "none", background: "radial-gradient(ellipse at center, transparent 55%, rgba(0,0,0,0.3) 100%)" }}
  />
);

import React from "react";
import { AbsoluteFill, Audio, Sequence, staticFile, useVideoConfig } from "remotion";
import "./fonts";
import { Badge, Grade, Grain, KenBurns, Pack, Pill, Vignette, WordReveal, sec, useExit } from "./components";
import { beats, theme } from "./theme";

const TextBlock: React.FC = () => {
  const { fps } = useVideoConfig();
  const exit = useExit(sec(fps, beats.textOut), 10);
  return (
    <div style={{ position: "absolute", top: 262, left: 70, right: 70, display: "flex", flexDirection: "column", alignItems: "center", gap: 34, ...exit }}>
      <WordReveal text="Chrupie naturalnie" delay={sec(fps, beats.headline)} size={118} />
      <Pill text="3 ziarna i sól morska" delay={sec(fps, beats.pill)} size={50} />
    </div>
  );
};

const Cta: React.FC = () => {
  const { fps } = useVideoConfig();
  const at = sec(fps, beats.cta);
  return (
    <div style={{ position: "absolute", top: 262, left: 70, right: 70, display: "flex", flexDirection: "column", alignItems: "center", gap: 26 }}>
      <WordReveal text="Spróbuj już dziś" delay={at} size={112} />
      <WordReveal text="GaliCrisp · pieczywko" delay={at + 8} size={46} per={4} family={theme.fonts.body} color={theme.colors.textDim} />
    </div>
  );
};

export const Story: React.FC = () => {
  const { fps } = useVideoConfig();
  const f = (s: number) => sec(fps, s);
  return (
    <AbsoluteFill style={{ backgroundColor: theme.colors.bg }}>
      {/* 1. background */}
      <KenBurns src="background.png" />
      {/* 2. assets */}
      <Pack delay={f(beats.packIn)} sheenAt={f(beats.sheen)} height={900} bottom={292} />
      <Badge src="extra-1.png" delay={f(beats.badges)} size={190} style={{ right: 70, top: 1030 }} />
      <Badge src="extra-2.png" delay={f(beats.badges) + 6} size={190} style={{ right: 70, top: 1245 }} />
      {/* 3. type */}
      <TextBlock />
      <Cta />
      {/* 4. grade, 5. grain + vignette */}
      <Grade />
      <Grain />
      <Vignette />
      {/* sound */}
      <Audio src={staticFile("sfx/bed.wav")} volume={0.28} />
      <Audio src={staticFile("sfx/whoosh.wav")} volume={0.6} />
      <Sequence from={f(beats.headline) - 2}><Audio src={staticFile("sfx/tick.wav")} volume={0.5} /></Sequence>
      <Sequence from={f(beats.pill) - 2}><Audio src={staticFile("sfx/pop.wav")} volume={0.55} /></Sequence>
      <Sequence from={f(beats.badges) - 2}><Audio src={staticFile("sfx/pop.wav")} volume={0.45} /></Sequence>
      <Sequence from={f(beats.badges) + 4}><Audio src={staticFile("sfx/pop.wav")} volume={0.45} /></Sequence>
      <Sequence from={f(beats.textOut) - 3}><Audio src={staticFile("sfx/whoosh.wav")} volume={0.45} /></Sequence>
      <Sequence from={f(beats.cta) - 2}><Audio src={staticFile("sfx/bass.wav")} volume={0.6} /></Sequence>
    </AbsoluteFill>
  );
};

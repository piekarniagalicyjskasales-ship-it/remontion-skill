import { Composition } from "remotion";
import { Story } from "./Story";
import { beats } from "./theme";

const FPS = 30;

export const Root: React.FC = () => (
  <Composition
    id="GaliCrispStory"
    component={Story}
    durationInFrames={Math.round(beats.end * FPS)}
    fps={FPS}
    width={1080}
    height={1920}
  />
);

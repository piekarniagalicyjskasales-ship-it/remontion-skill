import { continueRender, delayRender, staticFile } from "remotion";
import { theme } from "./theme";

const faces: Array<[string, string]> = [
  [theme.fonts.display, "Inter-ExtraBold.otf"],
  [theme.fonts.body, "InterDisplay-Medium.otf"],
];

const handle = delayRender("Loading fonts");
Promise.all(
  faces.map(([family, file]) => {
    const face = new FontFace(family, `url(${staticFile(file)})`);
    return face.load().then((loaded) => document.fonts.add(loaded));
  }),
)
  .then(() => continueRender(handle))
  .catch((err) => {
    console.error(err);
    continueRender(handle);
  });

import React from "react";
import { Composition, Freeze, useCurrentFrame } from "remotion";
import { BridgeShort, BRIDGE_FRAMES } from "./videos/bridge/Bridge";
const STEP = 3;
const Lite: React.FC = () => { const f = useCurrentFrame(); return <Freeze frame={Math.min(f * STEP, BRIDGE_FRAMES - 1)}><BridgeShort /></Freeze>; };
export const Root: React.FC = () => (<>
  <Composition id="BridgeShort" component={BridgeShort} durationInFrames={BRIDGE_FRAMES} fps={30} width={1080} height={1920} />
  <Composition id="BridgeLite" component={Lite} durationInFrames={BRIDGE_FRAMES} fps={30} width={1080} height={1920} />
</>);

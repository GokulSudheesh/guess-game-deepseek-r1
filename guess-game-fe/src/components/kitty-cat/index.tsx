import React, { useEffect, useRef, useState } from "react";
import { Application, extend } from "@pixi/react";
import { Container, AnimatedSprite, Assets, Spritesheet } from "pixi.js";
import { spriteTextureData } from "@/data/sprites";

// extend tells @pixi/react what Pixi.js components are available
extend({
  Container,
  AnimatedSprite,
});

interface IProps {
  state: "idle" | "box";
}

const KittyCat = ({ state }: IProps) => {
  const parentContainerRef = useRef<HTMLDivElement | null>(null);
  const [spriteSheet, setSpriteSheet] = useState<Spritesheet>();
  useEffect(() => {
    const parseSheet = async () => {
      const resource = await Assets.load(spriteTextureData.textureUrl);
      const sheet = new Spritesheet(
        resource,
        spriteTextureData.spritesheetData
      );
      await sheet.parse();
      // console.log("[LOG]", sheet);
      setSpriteSheet(sheet);
    };
    void parseSheet();
  }, []);
  // if (!spriteSheet) return null;

  return (
    <div
      ref={parentContainerRef}
      className="m-auto flex shrink-0 w-full sm:w-80 max-w-80 aspect-square h-fit bg-linear-0 from-white from-25% to-black to-25% border-2 border-white"
    >
      {spriteSheet && (
        <Application
          resizeTo={parentContainerRef}
          autoStart
          backgroundAlpha={0}
        >
          <pixiContainer>
            <pixiAnimatedSprite
              key={state}
              ref={(ref) => {
                ref?.play();
              }}
              anchor={{ x: -0.25, y: -0.25 }}
              width={224}
              height={224}
              textures={spriteSheet.animations[state]}
              animationSpeed={0.1}
              loop
            />
          </pixiContainer>
        </Application>
      )}
    </div>
  );
};

export default KittyCat;

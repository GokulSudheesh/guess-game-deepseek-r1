import { SpritesheetData } from "pixi.js";

const IMG_DIMS = 256;

export const data: SpritesheetData = {
  frames: {
    idle0: {
      frame: { x: 0, y: 0, w: IMG_DIMS, h: IMG_DIMS },
      sourceSize: { w: IMG_DIMS, h: IMG_DIMS },
    },
    idle1: {
      frame: { x: IMG_DIMS, y: 0, w: IMG_DIMS, h: IMG_DIMS },
      sourceSize: { w: IMG_DIMS, h: IMG_DIMS },
    },
    idle2: {
      frame: { x: IMG_DIMS * 2, y: 0, w: IMG_DIMS, h: IMG_DIMS },
      sourceSize: { w: IMG_DIMS, h: IMG_DIMS },
    },
    idle3: {
      frame: { x: IMG_DIMS * 3, y: 0, w: IMG_DIMS, h: IMG_DIMS },
      sourceSize: { w: IMG_DIMS, h: IMG_DIMS },
    },
    idle4: {
      frame: { x: IMG_DIMS * 4, y: 0, w: IMG_DIMS, h: IMG_DIMS },
      sourceSize: { w: IMG_DIMS, h: IMG_DIMS },
    },
    idle5: {
      frame: { x: IMG_DIMS * 5, y: 0, w: IMG_DIMS, h: IMG_DIMS },
      sourceSize: { w: IMG_DIMS, h: IMG_DIMS },
    },
    idle6: {
      frame: { x: IMG_DIMS * 6, y: 0, w: IMG_DIMS, h: IMG_DIMS },
      sourceSize: { w: IMG_DIMS, h: IMG_DIMS },
    },
    idle7: {
      frame: { x: IMG_DIMS * 7, y: 0, w: IMG_DIMS, h: IMG_DIMS },
      sourceSize: { w: IMG_DIMS, h: IMG_DIMS },
    },
    idle8: {
      frame: { x: IMG_DIMS * 8, y: 0, w: IMG_DIMS, h: IMG_DIMS },
      sourceSize: { w: IMG_DIMS, h: IMG_DIMS },
    },
    idle9: {
      frame: { x: IMG_DIMS * 9, y: 0, w: IMG_DIMS, h: IMG_DIMS },
      sourceSize: { w: IMG_DIMS, h: IMG_DIMS },
    },
    box0: {
      frame: { x: 0, y: IMG_DIMS, w: IMG_DIMS, h: IMG_DIMS },
      sourceSize: { w: IMG_DIMS, h: IMG_DIMS },
    },
    box1: {
      frame: { x: IMG_DIMS, y: IMG_DIMS, w: IMG_DIMS, h: IMG_DIMS },
      sourceSize: { w: IMG_DIMS, h: IMG_DIMS },
    },
    box2: {
      frame: { x: IMG_DIMS * 2, y: IMG_DIMS, w: IMG_DIMS, h: IMG_DIMS },
      sourceSize: { w: IMG_DIMS, h: IMG_DIMS },
    },
    box3: {
      frame: { x: IMG_DIMS * 3, y: IMG_DIMS, w: IMG_DIMS, h: IMG_DIMS },
      sourceSize: { w: IMG_DIMS, h: IMG_DIMS },
    },
  },
  meta: {
    scale: "1",
  },
  animations: {
    idle: [
      "idle0",
      "idle1",
      "idle2",
      "idle3",
      "idle4",
      "idle5",
      "idle6",
      "idle7",
      "idle8",
      "idle9",
    ],
    box: ["box0", "box1", "box2", "box3"],
  },
};

export const spriteTextureData: {
  name: string;
  textureUrl: string;
  spritesheetData: SpritesheetData;
} = {
  name: "kitty",
  textureUrl: "/images/sprites/kitty-sprite-sheet.png",
  spritesheetData: data,
};

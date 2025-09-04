export enum AnswerEnum {
  YES = "YES",
  NO = "NO",
  MAYBE = "MAYBE",
  DONT_THINK_SO = "DONT_THINK_SO",
  DONT_KNOW = "DONT_KNOW",
}

export type MenuState = "initial" | "thinking" | "asking" | "finished";

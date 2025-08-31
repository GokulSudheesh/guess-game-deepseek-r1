import React, { useCallback } from "react";
import { Button } from "@/components/ui/button";
import { MenuState, AnswerEnum } from "@/types/options";

const AnswerMap: Record<AnswerEnum, string> = {
  [AnswerEnum.YES]: "Yes",
  [AnswerEnum.NO]: "No",
  [AnswerEnum.MAYBE]: "Maybe",
  [AnswerEnum.DONT_THINK_SO]: "Don't think so",
  [AnswerEnum.DONT_KNOW]: "Don't know",
};

interface IProps {
  state: MenuState;
  question: string | undefined;
  startGame: () => void;
  resetGame: () => void;
  answerGuess: (answer: AnswerEnum) => void;
}

const Menu = ({
  state,
  question,
  startGame,
  resetGame,
  answerGuess,
}: IProps) => {
  const answerGuessCallback = useCallback(
    (event: React.MouseEvent<HTMLButtonElement>) => {
      const answer = event.currentTarget.dataset.answer as AnswerEnum;
      answerGuess(answer);
    },
    [answerGuess]
  );
  return (
    <div className="flex w-full max-[1080px]:flex-col max-[1080px]:gap-6 gap-10">
      <div className="flex shrink-0 w-full sm:w-64 max-w-64 aspect-square h-fit bg-red-500 border-2 border-white" />
      <div className="flex flex-col gap-4 w-full items-center">
        {state === "initial" && (
          <>
            <p className="text-lg">
              Think of a person and I will try to guess who it is.
            </p>
            <Button
              variant="default"
              className="w-full max-w-xs font-semibold text-base"
              onClick={startGame}
            >
              Start Game
            </Button>
          </>
        )}
        {state === "thinking" && (
          <>
            <p className="text-lg">Thinking...</p>
          </>
        )}
        {state === "asking" && question && (
          <>
            <p className="text-lg">{question}</p>
            {Object.values(AnswerEnum).map((answer) => (
              <Button
                key={answer}
                data-answer={answer}
                variant="outline"
                className="w-full max-w-xs"
                onClick={answerGuessCallback}
              >
                {AnswerMap[answer]}
              </Button>
            ))}
          </>
        )}
        {state === "finished" && question && (
          <>
            <p className="text-lg">{question}</p>
            <Button
              variant="default"
              className="w-full max-w-xs font-semibold text-base"
              onClick={resetGame}
            >
              Play Again
            </Button>
          </>
        )}
      </div>
    </div>
  );
};

export default Menu;

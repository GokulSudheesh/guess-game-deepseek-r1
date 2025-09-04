import { useCallback, useState } from "react";
import { AnswerEnum, MenuState } from "@/types/options";
import { useMutation } from "@tanstack/react-query";
import { APIResponse } from "@/types/response";
import { toast } from "sonner";

const startGameMutationFn = async (): Promise<APIResponse> => {
  const response = await fetch("/api/internal/guess/start", {
    method: "POST",
  });
  if (!response.ok) throw new Error("Failed to start game");
  return response.json();
};

const answerGuessMutationFn = async ({
  sessionId,
  answer,
}: {
  sessionId: string;
  answer: AnswerEnum;
}): Promise<APIResponse> => {
  const response = await fetch("/api/internal/guess/ask", {
    method: "POST",
    body: JSON.stringify({ session_id: sessionId, answer }),
    headers: {
      "Content-Type": "application/json",
    },
  });
  if (!response.ok) throw new Error("Failed to submit answer");
  return response.json();
};

export const useGuessGame = () => {
  const [menuState, setMenuState] = useState<MenuState>("initial");
  const [question, setQuestion] = useState<string | undefined>();
  const [sessionId, setSessionId] = useState<string | null>(null);
  const { mutate: startGameMutate } = useMutation({
    mutationFn: startGameMutationFn,
    onError: () => {
      toast.error("Something went wrong. Please try again.");
      setMenuState("initial");
    },
  });
  const { mutate: answerGuessMutate } = useMutation({
    mutationFn: answerGuessMutationFn,
    onError: () => {
      toast.error("Something went wrong. Please try again.");
      setMenuState("asking");
    },
  });

  const startGame = useCallback(() => {
    setMenuState("thinking");
    startGameMutate(undefined, {
      onSuccess: (data) => {
        console.log("Game started successfully:", data);
        setMenuState("asking");
        setSessionId(data.data?.session_id || null);
        if (data.data?.question) setQuestion(data.data.question);
      },
    });
  }, [startGameMutate]);

  const resetGame = useCallback(() => {
    setMenuState("initial");
    setQuestion(undefined);
    setSessionId(null);
  }, []);

  const answerGuess = useCallback(
    (answer: AnswerEnum) => {
      if (!sessionId) return;
      setMenuState("thinking");
      answerGuessMutate(
        { sessionId, answer },
        {
          onSuccess: (data) => {
            console.log("Next question:", data);
            setMenuState("asking");
            if (data.data?.question) setQuestion(data.data.question);
            if (data.data?.confidence === 1) setMenuState("finished");
          },
        }
      );
    },
    [sessionId, answerGuessMutate]
  );

  return {
    menuState,
    question,
    startGame,
    answerGuess,
    resetGame,
  };
};

"use client";
import React from "react";
import Menu from "@/components/menu";
import { useGuessGame } from "./hooks";

const Home = () => {
  const { menuState, question, startGame, answerGuess, resetGame } =
    useGuessGame();
  return (
    <div className="flex w-full mt-20 px-10 min-[1080px]:px-50">
      <Menu
        state={menuState}
        question={question}
        startGame={startGame}
        answerGuess={answerGuess}
        resetGame={resetGame}
      />
    </div>
  );
};

export default Home;

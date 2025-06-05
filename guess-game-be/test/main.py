import asyncio
import json
from utils.log import LogManager
from chain.completion import completion
from models.completion_response import CompletionResponse
from chain.prompts import mapper

log = LogManager()

chat_history = []


async def get_response(*, query: str) -> CompletionResponse:
    """Get a response from the model."""
    response = await completion.invoke(query=query, chat_history=chat_history)
    print(f"Model: {response.content}")
    log.append(f"User: {query}")
    log.append(f"Model: {response.content}")

    chat_history.append({"role": "user", "content": query})
    chat_history.append({"role": "assistant", "content": response.content})
    return response


async def main():
    print(
        """
    ---------------------------------------------------------------------------------------------
    |  Welcome to the Guessing Game!                                                            |
    |  Think of a person, and I will try to guess who it is by asking you yes or no questions.  |
    ---------------------------------------------------------------------------------------------
    """
    )
    response = await get_response(
        query="Who is the person I am thinking of? Ask me a yes or no question to start the game."
    )

    print(json.dumps(response.data, indent=2))

    while True:
        user_input = input(
            """
1 -> Yes
2 -> No
3 -> Maybe
4 -> Don't think so
5 -> Don't know
6 -> Exit
> """
        )
        if int(user_input) == 6:
            log.flush()
            break
        user_input = mapper.get(int(user_input), user_input)
        print(f"You: {user_input}")
        # Invoke the chain with the current chat history
        response = await get_response(query=user_input)

        # Print the model's response
        print(json.dumps(response.data, indent=2))

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        log.flush()
        print("\nExiting the game. Goodbye!")

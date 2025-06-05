import asyncio
import json
from utils.chat import ChatManager, ChatRole
from utils.log import LogManager
from chain.completion import completion
from models.completion_response import CompletionResponse
from chain.prompts import mapper

log = LogManager()

session_id = None
chat_manager = ChatManager()


async def get_response(*, query: str, session_id: str) -> CompletionResponse:
    """Get a response from the model."""
    chat_history = chat_manager.get_session(session_id).get_history()
    response = await completion.invoke(query=query, chat_history=chat_history)
    # print(f"Model: {response.content}")
    log.append(f"User: {query}")
    log.append(f"***********************************************************" * 2)
    log.append(f"Model: {response.content}")
    log.append(f"Model Metrics: {response.usage_metadata}")

    chat_manager.add_message(session_id=session_id,
                             role=ChatRole.USER, content=query)
    chat_manager.add_message(session_id=session_id, role=ChatRole.ASSISTANT, content=response.data.get(
        "question") or response.content)
    return response


async def start_up():
    global session_id
    session_id = chat_manager.create_session()
    print(
        """
    ---------------------------------------------------------------------------------------------
    |  Welcome to the Guessing Game!                                                            |
    |  Think of a person, and I will try to guess who it is by asking you yes or no questions.  |
    ---------------------------------------------------------------------------------------------
    """
    )
    response = await get_response(
        query="Who is the person I am thinking of? Ask me a yes or no question to start the game.",
        session_id=session_id
    )

    print(json.dumps(response.data, indent=2))


async def main():
    await start_up()

    while True:
        user_input = input(
            """
1 -> Yes
2 -> No
3 -> Maybe
4 -> Don't think so
5 -> Don't know
6 -> Restart
7 -> Exit
> """
        )
        try:
            user_input = int(user_input.strip())
        except:
            print("Invalid input. Please enter a number between 1 and 6.")
            continue
        if user_input == 6:
            chat_history = chat_manager.get_session(session_id).get_history()
            log.append(f"Chat history:\n{json.dumps(chat_history, indent=2)}")
            chat_manager.clear_sessions()
            await start_up()
            continue
        elif user_input == 7:
            chat_history = chat_manager.get_session(session_id).get_history()
            log.append(f"Chat history:\n{json.dumps(chat_history, indent=2)}")
            chat_manager.clear_sessions()
            log.flush()
            break
        elif not (1 <= user_input <= 7):
            print("Invalid input. Please enter a number between 1 and 6.")
            continue
        user_input = mapper.get(user_input)
        print(f"You: {user_input}")
        # Invoke the chain with the current chat history
        try:
            response = await get_response(query=user_input, session_id=session_id)
        except Exception as e:
            log.append(f"Error: {str(e)}")
            print(
                "An error occurred while processing your input. Please enter your previous response again.")
            continue
        # Print the model's response
        print(json.dumps(response.data, indent=2))

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        log.flush()
        print("\nExiting the game. Goodbye!")

import json
import logging
from fastapi import APIRouter, HTTPException, Depends
from app.core.models.guess_request import AnswerEnum, GuessRequestBody, GuessResponseWrapper
from app.core.utils.chat import ChatManager, ChatRole
from app.core.chain.completion import completion
from app.core.chain.prompts import initial_user_chat, user_answer_mapper
from app.api.deps.redis import get_chat_manager

router = APIRouter(prefix="/guess", tags=["Guess"])


@router.post("/start")
async def guess_start(chat_manager: ChatManager = Depends(get_chat_manager)) -> GuessResponseWrapper:
    session_id = await chat_manager.create_session()
    response = await completion.invoke_with_retry(query=initial_user_chat, chat_history=[])
    await chat_manager.add_message(
        session_id=session_id, role=ChatRole.USER, content=initial_user_chat)
    await chat_manager.add_message(session_id=session_id, role=ChatRole.ASSISTANT,
                                   content=response.data.get("question") or response.content)

    logging.info(
        f"Session ID: {session_id}, Initial Question: {response.data.get('question') or response.content}")
    return GuessResponseWrapper(
        data={
            "session_id": session_id,
            "question": response.data.get("question"),
            "confidence": response.data.get("confidence"),
            "question_number": response.data.get("question_number"),
        }
    )


@router.post("/ask")
async def guess_ask(body: GuessRequestBody, chat_manager: ChatManager = Depends(get_chat_manager)) -> GuessResponseWrapper:
    if not (body.session_id and await chat_manager.session_exists(body.session_id)):
        raise HTTPException(
            status_code=400, detail="Invalid session ID provided.")

    session_id = body.session_id
    answer = user_answer_mapper.get(body.answer)
    chat_history = await chat_manager.get_history(session_id)
    logging.info(
        f"Session ID: {session_id}, Answer: {answer}, Chat History: {json.dumps(chat_history, indent=2)}")
    response = await completion.invoke_with_retry(query=answer, chat_history=chat_history)
    logging.info(
        f"Session ID: {session_id}, Response: {response.data.get('question') or response.content}, Confidence: {response.data.get('confidence')}")
    await chat_manager.add_message(
        session_id=session_id, role=ChatRole.USER, content=answer)
    await chat_manager.add_message(session_id=session_id, role=ChatRole.ASSISTANT,
                                   content=response.data.get("question") or response.content)
    # Remove session if the user answered with YES and the confidence is 1 meaning the bot got it right
    if (response.data.get("confidence") == 1 and body.answer == AnswerEnum.YES):
        await chat_manager.remove_session(session_id)
    return GuessResponseWrapper(
        data={
            "session_id": session_id,
            "question": response.data.get("question"),
            "confidence": response.data.get("confidence"),
            "question_number": response.data.get("question_number"),
        }
    )

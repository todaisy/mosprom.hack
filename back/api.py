import os
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from db import get_db

from ..RAG.main_rag import rag_pipeline

from crud import (
    create_chat,
    create_user,
    create_message,
    get_n_messages_from_chat,
    get_last_message_local_id,
    get_all_user_chats,
    get_last_message_from_chat,
    get_chat_state,
    update_react,
    update_is_generated_chat,
    commit_changes,
)

from schemas import (
    CreateChatBase,
    CreateMessageBase,
    CreateLLMMessageBase,
    ReactionBase,
)

# Теперь LLM тоже идентифицируется по int ID
LLM_ID = 1  # Можно завести системного "бота" с таким ID

router = APIRouter(prefix="/api")


def fake_llm_ans(prompt: str) -> str:
    return "Здесь мог быть ответ от ЛЛМ, но его нет :("


@router.post("/create-llm-message")
async def create_llm_message_endpoint(
    message: CreateLLMMessageBase,
    db: AsyncSession = Depends(get_db),
):
    """
    Создаёт сообщение от LLM в чате (эмуляция).
    """
    try:
        chat_is_generating = await get_chat_state(db=db, chat_id=message.chat_id)

        if chat_is_generating:
            last_message = await get_last_message_from_chat(db=db, chat_id=message.chat_id)
            await update_is_generated_chat(db=db, chat_id=message.chat_id, new_state=True)
            await commit_changes(db=db)

            llm_ans = rag_pipeline(str(last_message.text))
            llm_message = await create_message(
                db=db,
                chat_id=message.chat_id,
                user_id=LLM_ID,
                text=llm_ans,
                is_bot=True,
                local_id=int(last_message.local_id) + 1,
                answer_to=int(last_message.local_id),
            )

            await update_is_generated_chat(db=db, chat_id=message.chat_id, new_state=False)
            await commit_changes(db=db)

            return {
                "status": "ok",
                "data": {
                    "chat_id": message.chat_id,
                    "message_id": llm_message.id,
                    "is_bot": True,
                    "text": llm_message.text,
                    "answer_to": last_message.id,
                    "react": 0,
                },
            }
        else:
            return {"status": "ignored", "detail": "Chat not generating"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/all-user-chats/{user_id}")
async def get_all_user_chats_endpoint(user_id: int, db: AsyncSession = Depends(get_db)):
    """
    Получить все существующие чаты пользователя
    """
    try:
        chats = await get_all_user_chats(db=db, user_id=user_id)
        return {"status": "ok", "data": chats}
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/chats/{chat_id}")
async def get_n_messages_from_chat_endpoint(
    chat_id: int,
    skip: int = 0,
    n: int = 100,
    db: AsyncSession = Depends(get_db),
):
    """
    Получить последние N сообщений из чата
    """
    try:
        chat = await get_n_messages_from_chat(db=db, chat_id=chat_id, n=n, skip=skip)
        is_generating = await get_chat_state(db=db, chat_id=chat_id)
        return {"status": "ok", "is_generating": is_generating, "data": chat}
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/create-user")
async def create_user_endpoint(db: AsyncSession = Depends(get_db)):
    """
    Создаёт нового пользователя
    """
    try:
        user = await create_user(db=db)
        await commit_changes(db=db)
        return {"status": "ok", "user_id": user.id}
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/create-chat")
async def create_chat_endpoint(
    chat_request: CreateChatBase,
    db: AsyncSession = Depends(get_db),
):
    """
    Создаёт новый чат
    """
    try:
        chat = await create_chat(db=db, user_id=chat_request.user_id)
        await commit_changes(db=db)
        return {"status": "ok", "chat_id": chat.id, "user_id": chat_request.user_id}
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/create-message")
async def create_message_endpoint(
    message: CreateMessageBase,
    db: AsyncSession = Depends(get_db),
):
    """
    Создаёт новое сообщение
    """
    try:
        local_id = await get_last_message_local_id(db=db, chat_id=message.chat_id)
        local_id = (local_id or 0) + 1

        message_obj = await create_message(
            db=db,
            user_id=message.user_id,
            chat_id=message.chat_id,
            local_id=local_id,
            text=message.text,
            answer_to=message.answer_to,
            is_bot=message.is_bot,
        )

        await commit_changes(db=db)
        return {"status": "ok", "message_id": message_obj.id, "local_id": local_id}
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.patch("/react")
async def update_react_endpoint(
    reaction: ReactionBase, db: AsyncSession = Depends(get_db)
):
    """
    Изменяет реакцию (лайк/дизлайк) на сообщение
    """
    try:
        updated_message = await update_react(
            db=db,
            message_id=reaction.message_id,
            react=reaction.react,
        )
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

    if not updated_message:
        raise HTTPException(status_code=404, detail="Message not found")

    await commit_changes(db=db)
    return {"status": "ok", "message_id": updated_message.id}

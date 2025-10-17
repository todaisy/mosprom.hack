from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import  AsyncSession
from db import get_db

from crud import create_chat, create_user, create_message
from crud import get_n_last_messages_from_chat, get_last_message_local_id, get_all_user_chats
from crud import update_react
from crud import commit_changes

from schemas import CreateChatBase, CreateMessageBase
from schemas import ReadMessageBase
from schemas import ReactionBase

from uuid import UUID

router = APIRouter(prefix="/api")

@router.get("/all-user-chats/{user_uuid}")
async def get_all_user_chats_endpoint(user_uuid: UUID, db: AsyncSession = Depends(get_db)):
    """
    Получить все существующие чаты пользователя
    """
    try:
        chats = await get_all_user_chats(db=db, user_uuid=user_uuid)
        return {"status": "ok","data": chats}
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/chats/{chat_id}")
async def get_n_last_messages_from_chat_endpoint(chat_id: int,
                                                 skip: int = 0,
                                                 n: int = 100,
                                                 db: AsyncSession = Depends(get_db)):
    try:
        chat = await get_n_last_messages_from_chat(db=db,chat_id=chat_id, n=n, skip=skip)
        return {"status": "ok","data": chat}
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.post("/create-user")
async def create_user_endpoint(db: AsyncSession = Depends(get_db)):
    """
    Сохдает нового пользователя
    """
    try:
        user = await create_user(db=db)
        await commit_changes(db=db)
        return {"status": "ok", "user_uuid": str(user.uuid)}
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.post('/create-chat')
async def create_chat_endpoint(
    chat_request: CreateChatBase,
    db: AsyncSession = Depends(get_db)
):
    """
    Создаёт новый чат.
    """
    try:
        chat = await create_chat(db=db, user_uuid=chat_request.user_uuid)
        await commit_changes(db=db)
        return {"status": "ok", "chat_id": chat.id, "user_uuid": str(chat_request.user_uuid)}
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.post('/create-message')
async def create_message_endpoint(
    message: CreateMessageBase,
    db: AsyncSession = Depends(get_db),
):
    """
    Создает новое сообщение
    """
    try:
        local_id = await get_last_message_local_id(db=db, chat_id=message.chat_id)
        local_id = (local_id or 0) + 1
        message = await create_message(db=db,
                                       user_uuid=message.user_uuid,
                                       chat_id=message.chat_id,
                                       local_id=local_id,
                                       text=message.text,
                                       answer_to=message.answer_to,
                                       is_bot=message.is_bot
                                       )

        await commit_changes(db=db)
        return {"status": "ok","message_id": message.id, "local_id": local_id}
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.patch("/react")
async def update_react_endpoint(reaction: ReactionBase,db: AsyncSession = Depends(get_db)):
    try:
        updated_message = await update_react(
            db=db,
            message_id=reaction.message_id,
            react=reaction.react
        )
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    if not updated_message:
        raise HTTPException(status_code=404, detail="Message not found")

    await commit_changes(db=db)
    return {"status": "ok", "message_id": updated_message.id}
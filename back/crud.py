from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from models import *
from uuid import UUID
from typing import Optional, List

# GET
async def get_last_message_from_chat(db: AsyncSession, chat_id: int) -> Optional[Message]:
    result = await db.execute(
        select(Message)
        .where(Message.chat_id == chat_id)
        .order_by(Message.local_id.desc())
        .limit(1)
    )
    return result.scalar_one_or_none()


async def get_last_message_local_id(db: AsyncSession,
                                    chat_id) -> Optional[int]:
    result = await db.execute(
        select(Message.local_id)
        .where(Message.chat_id == chat_id)
        .order_by(Message.created_at.desc())
        .limit(1)
    )
    return result.scalar_one_or_none()

async def get_n_last_messages_from_chat(db: AsyncSession,
                                        chat_id: int,
                                        skip: int,
                                        n: int)->List[Message]:

    result = await db.execute(select(Message)
                              .where(Message.chat_id == chat_id)
                              .order_by(Message.created_at.desc())
                              .offset(skip)
                              .limit(n))
    messages = result.scalars().all()
    return list(reversed(messages))

async def get_all_user_chats(db: AsyncSession,user_uuid: UUID)->List[Chat]:
    result = await db.execute(select(Chat)
                              .where(Chat.user_uuid == user_uuid)
                              .order_by(Chat.created_at.asc()))
    chats = result.scalars().all()
    return list(chats)

# POST
async def create_user(db: AsyncSession)-> User:
     user = User()
     db.add(user)
     await db.flush()
     return user

async def _create_chat_member(db: AsyncSession,
                              user_uuid: UUID,
                              chat_id: int)-> ChatMember:
        chat_member = ChatMember(chat_id=chat_id, user_uuid=user_uuid)
        db.add(chat_member)
        await db.flush()
        return chat_member

async def create_chat(db: AsyncSession,
                      user_uuid: UUID)-> Chat:
    chat = Chat(user_uuid=user_uuid)
    db.add(chat)
    await db.flush()
    chat_id = chat.id
    await _create_chat_member(db=db, user_uuid=user_uuid, chat_id=chat_id)
    await db.flush()
    return chat

async def create_message(db: AsyncSession,
                         chat_id: int,
                         user_uuid: UUID,
                         text: str,
                         is_bot: bool,
                         local_id: int,
                         answer_to: Optional[int] = None) -> Message:

    message = Message(chat_id=chat_id,
                      user_uuid= user_uuid,
                      text=text,
                      answer_to=answer_to,
                      local_id=local_id,
                      is_bot=is_bot)
    db.add(message)
    await db.flush()
    return message

# PATCH

async def update_react(db: AsyncSession,
                          message_id: int,
                          react: int) -> Optional[Message]:
    result = await db.execute(select(Message).where(Message.id == message_id))
    message = result.scalar_one_or_none()
    if not message:
        raise ValueError(f"Message {message_id} not found")
    setattr(message, 'react', react)
    await db.flush()
    return message

# ATHER
async def commit_changes(db: AsyncSession):
    try:
        await db.commit()
    except Exception as e:
        await db.rollback()
        raise e


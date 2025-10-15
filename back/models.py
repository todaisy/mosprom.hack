from tkinter.constants import CASCADE

from asyncpg import StringDataRightTruncation

from db import Base
import uuid
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.dialects import postgresql
from sqlalchemy import String, ForeignKey

class User(Base):
    __tablename__ = "users"
    uuid: Mapped[uuid.UUID] = mapped_column(
        postgresql.UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

class Chat(Base):
    __tablename__ = "chats"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(64))
    user_uuid: Mapped[uuid.UUID] = mapped_column(postgresql.UUID(as_uuid=True),
                                                 ForeignKey("users.uuid", ondelete="CASCADE"))


class Message(Base):
    __tablename__ = "messages"
    id: Mapped[int] = mapped_column(primary_key=True)
    local_id: Mapped[int] = mapped_column()
    chat_id: Mapped[int] = mapped_column(ForeignKey("chats.id", ondelete="CASCADE"))
    user_uuid: Mapped[uuid.UUID] = mapped_column(
        postgresql.UUID(as_uuid=True),
        ForeignKey("users.uuid", ondelete="CASCADE"))
    text: Mapped[str] = mapped_column(String(1000))
    answer_to: Mapped[int | None] = mapped_column()
    react: Mapped[int] = mapped_column() # -1/0/1
    is_bot: Mapped[bool] = mapped_column(default=False)

class ChatMember(Base):
    __tablename__ = "chat_members"
    id: Mapped[int] = mapped_column(primary_key=True)
    chat_id: Mapped[int] = mapped_column(ForeignKey("chats.id", ondelete="CASCADE"), unique=True)
    user_uuid: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.uuid", ondelete="CASCADE"))

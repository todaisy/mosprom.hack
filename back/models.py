from db import Base
from uuid import UUID as python_uuid
from uuid import  uuid4
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import String, ForeignKey, UniqueConstraint, func
from datetime import datetime

class User(Base):
    __tablename__ = "users"
    uuid: Mapped[python_uuid] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(server_default=func.now(),
                                                 nullable=False)

class Chat(Base):
    __tablename__ = "chats"
    id: Mapped[int] = mapped_column(primary_key=True,
                                    autoincrement=True,
                                    nullable=False)
    title: Mapped[str] = mapped_column(String(64),
                                       nullable=False,
                                       default="")
    user_uuid: Mapped[python_uuid] = mapped_column(UUID(as_uuid=True),
                                                 ForeignKey("users.uuid", ondelete="CASCADE"),
                                                 nullable=False)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now(),
                                                 nullable=False)
    is_generate: Mapped[bool] = mapped_column(default=False)


class Message(Base):
    __tablename__ = "messages"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, nullable=False)
    local_id: Mapped[int] = mapped_column(nullable=False)
    chat_id: Mapped[int] = mapped_column(ForeignKey("chats.id", ondelete="CASCADE"), nullable=False)
    user_uuid: Mapped[python_uuid] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.uuid", ondelete="CASCADE"), nullable=False)
    text: Mapped[str] = mapped_column(String(1000), nullable=False)
    answer_to: Mapped[int | None] = mapped_column()
    react: Mapped[int] = mapped_column(default=0) # -1/0/1
    is_bot: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now(), nullable=False)
    __table_args__ = (
        UniqueConstraint("chat_id", "local_id", name="uq_chat_local_message"),
    )

class ChatMember(Base):
    __tablename__ = "chat_members"
    id: Mapped[int] = mapped_column(primary_key=True)
    chat_id: Mapped[int] = mapped_column(ForeignKey("chats.id", ondelete="CASCADE"), nullable=False)
    user_uuid: Mapped[python_uuid] = mapped_column(UUID(as_uuid=True) ,ForeignKey("users.uuid", ondelete="CASCADE"), nullable=False)


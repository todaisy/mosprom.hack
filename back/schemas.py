from pydantic import BaseModel, Field, field_validator
from datetime import datetime


class CreateMessageBase(BaseModel):
    user_id: int
    chat_id: int
    text: str = Field(min_length=1, max_length=1000)
    answer_to: int | None = None
    is_bot: bool = False


class ReadMessageBase(CreateMessageBase):
    id: int
    local_id: int
    created_at: datetime
    react: int = 0


class ReactionBase(BaseModel):
    message_id: int
    react: int

    @field_validator("react")
    def validate_react(cls, v):
        if v not in range(-1, 2):
            raise ValueError("react must be between -1 and 1")
        return v


class CreateLLMMessageBase(BaseModel):
    chat_id: int


class CreateChatBase(BaseModel):
    user_id: int

    class Config:
        from_attributes = True

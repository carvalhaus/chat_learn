from typing import Optional
from datetime import datetime
from pydantic import BaseModel
from app.core.constants.sender import SenderEnum

class ChatMessageBase(BaseModel):
    session_id: int
    sender: SenderEnum
    message: str

class ChatMessageCreate(ChatMessageBase):
    pass

class ChatMessageUpdate(BaseModel):
    message: Optional[str] = None

class ChatMessageRead(ChatMessageBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class ChatProcessResponse(BaseModel):
    bot_message: ChatMessageRead

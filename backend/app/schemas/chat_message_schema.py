from typing import Optional
from datetime import datetime
from pydantic import BaseModel
from app.core.constants.sender import SenderEnum

class ChatMessageBase(BaseModel):
    sender: SenderEnum
    message: str
    external_user_id: int 

class ChatMessageCreate(ChatMessageBase):
    pass

class ChatMessageUpdate(BaseModel):
    message: Optional[str] = None

class ChatMessageRead(ChatMessageBase):
    id: int
    session_id: int
    created_at: datetime

    class Config:
        from_attributes = True

class ChatProcessResponse(BaseModel):
    bot_message: ChatMessageRead

from typing import List
from datetime import datetime
from pydantic import BaseModel
from .chat_message_schema import ChatMessageRead

class ChatSessionBase(BaseModel):
    external_user_id: int

class ChatSessionCreate(ChatSessionBase):
    pass

class ChatSessionRead(ChatSessionBase):
    id: int
    created_at: datetime
    messages: List["ChatMessageRead"] = []

    class Config:
        from_attributes = True 

from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel
from .chat_message_schema import ChatMessageRead

class ChatSessionBase(BaseModel):
    user_id: int

class ChatSessionCreate(ChatSessionBase):
    pass

class ChatSessionRead(ChatSessionBase):
    id: int
    created_at: datetime
    messages: Optional[List["ChatMessageRead"]] = []

    class Config:
        from_attributes = True 

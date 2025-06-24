from typing import List
from datetime import datetime
from pydantic import BaseModel
from .chat_message_schema import ChatMessageRead
from .external_user_schema import ExternalUserRead
from typing import Optional

class ChatSessionBase(BaseModel):
    external_id: str
    name: Optional[str] = None
    email: Optional[str] = None

class ChatSessionCreate(ChatSessionBase):
    pass

class ChatSessionRead(BaseModel):
    id: int
    created_at: datetime
    messages: List["ChatMessageRead"] = []

    class Config:
        from_attributes = True 

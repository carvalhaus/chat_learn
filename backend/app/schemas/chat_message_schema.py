from app.core.constants.feedback import FeedbackEnum
from datetime import datetime
from pydantic import BaseModel
from app.core.constants.sender import SenderEnum
from typing import Optional

class ChatMessageBase(BaseModel):
    sender: SenderEnum
    message: str
    external_user_id: int
    feedback: Optional[FeedbackEnum] = FeedbackEnum.NEUTRAL

class ChatMessageCreate(ChatMessageBase):
    pass

class ChatMessageUpdate(ChatMessageBase):
    pass

class ChatMessageFeedbackUpdate(BaseModel):
    feedback: FeedbackEnum

class ChatMessageRead(ChatMessageBase):
    id: int
    session_id: int
    created_at: datetime

    class Config:
        from_attributes = True

class ChatProcessResponse(BaseModel):
    bot_message: ChatMessageRead

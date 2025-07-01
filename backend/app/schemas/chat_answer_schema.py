from typing import Optional
from datetime import datetime
from pydantic import BaseModel

class ChatAnswerBase(BaseModel):
    question_id: int
    answer: str

class ChatAnswerCreate(ChatAnswerBase):
    pass

class ChatAnswerUpdate(BaseModel):
    answer: Optional[str] = None

class ChatAnswerRead(ChatAnswerBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True 

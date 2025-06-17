from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel
from .chat_answer_schema import ChatAnswerRead

class ChatQuestionBase(BaseModel):
    question: str
    subject: Optional[str] = None

class ChatQuestionCreate(ChatQuestionBase):
    pass

class ChatQuestionUpdate(ChatQuestionBase):
    pass

class ChatQuestionRead(ChatQuestionBase):
    id: int
    created_at: datetime
    updated_at: datetime
    answers: List[ChatAnswerRead] = []

    class Config:
        from_attributes = True 

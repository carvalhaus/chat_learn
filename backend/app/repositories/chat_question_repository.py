from app.models.chat_question_model import ChatQuestion
from app.repositories.base_repository import BaseRepository
from sqlalchemy.orm import Session

class ChatQuestionRepository(BaseRepository):
    def __init__(self):
        super().__init__(ChatQuestion)
    
    def get_by_subject(self, db: Session, subject: str):
        return db.query(ChatQuestion).filter(ChatQuestion.subject == subject).all()
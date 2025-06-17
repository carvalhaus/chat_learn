from app.models.chat_answer_model import ChatAnswer
from app.repositories.base_repository import BaseRepository
from sqlalchemy.orm import Session

class ChatAnswerRepository(BaseRepository):
    def __init__(self):
        super().__init__(ChatAnswer)

    def list_by_question_id(self, db: Session, question_id: int):
        return db.query(ChatAnswer).filter(ChatAnswer.question_id == question_id).all()

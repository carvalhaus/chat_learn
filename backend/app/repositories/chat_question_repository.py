from app.models.chat_question_model import ChatQuestion
from app.repositories.base_repository import BaseRepository
from sqlalchemy.orm import Session
from rapidfuzz import fuzz, process

class ChatQuestionRepository(BaseRepository):
    def __init__(self):
        super().__init__(ChatQuestion)

    def get_by_subject(self, db: Session, subject: str):
        return db.query(ChatQuestion).filter(ChatQuestion.subject == subject).all()
    
    def find_best_match(self, db: Session, user_message: str, threshold: int = 60):
        questions = db.query(ChatQuestion).all()
        if not questions:
            return None

        question_texts = [q.question for q in questions]
        best_match = process.extractOne(user_message, question_texts, scorer=fuzz.token_sort_ratio)

        if best_match and best_match[1] >= threshold:
            matched_text = best_match[0]
            return next((q for q in questions if q.question == matched_text), None)

        return None

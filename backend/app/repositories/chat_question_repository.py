from app.models.chat_question_model import ChatQuestion
from app.repositories.base_repository import BaseRepository
from sqlalchemy.orm import Session
from rapidfuzz import fuzz, process
import unicodedata

class ChatQuestionRepository(BaseRepository):
    def __init__(self):
        super().__init__(ChatQuestion)

    def get_by_subject(self, db: Session, subject: str):
        return db.query(ChatQuestion).filter(ChatQuestion.subject == subject).all()
    
    def normalize_text(self, text: str) -> str:
        text = unicodedata.normalize('NFKD', text).encode('ASCII', 'ignore').decode('ASCII')
        return text.lower().strip()
    
    def find_best_match(self, db: Session, user_message: str, threshold: int = 60):
        questions = db.query(ChatQuestion).all()
        if not questions:
            return None

        question_map = {self.normalize_text(q.question): q for q in questions}
        question_texts = list(question_map.keys())

        user_message_normalized = self.normalize_text(user_message)

        best_match = process.extractOne(
            user_message_normalized, question_texts, scorer=fuzz.partial_ratio
        )

        if best_match and best_match[1] >= threshold:
            matched_text = best_match[0]
            return question_map[matched_text]

        return None

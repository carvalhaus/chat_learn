from app.models.chat_session_model import ChatSession
from app.repositories.base_repository import BaseRepository
from sqlalchemy.orm import Session

class ChatSessionRepository(BaseRepository):
    def __init__(self):
        super().__init__(ChatSession)

    def get_by_user_id(self, db: Session, user_id: int):
        return db.query(ChatSession).filter(ChatSession.user_id == user_id).all()

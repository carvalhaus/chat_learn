from app.models.chat_message_model import ChatMessage
from app.repositories.base_repository import BaseRepository
from sqlalchemy.orm import Session

class ChatMessageRepository(BaseRepository):
    def __init__(self):
        super().__init__(ChatMessage)

    def list_by_session_id(self, db: Session, session_id: int):
        return db.query(ChatMessage).filter(ChatMessage.session_id == session_id).order_by(ChatMessage.created_at).all()

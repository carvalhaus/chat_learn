from app.models.chat_message_model import ChatMessage
from app.repositories.base_repository import BaseRepository
from sqlalchemy.orm import Session
from app.core.constants.sender import SenderEnum
from app.core.constants.feedback import FeedbackEnum
from sqlalchemy.exc import SQLAlchemyError

class ChatMessageRepository(BaseRepository):
    def __init__(self):
        super().__init__(ChatMessage)

    def list_by_session_id(self, db: Session, session_id: int):
        return db.query(ChatMessage).filter(ChatMessage.session_id == session_id).order_by(ChatMessage.created_at).all()

    def update_feedback(self, db: Session, message_id: int, feedback: FeedbackEnum):
        try:
            message = self.get_by_id(db, message_id)
            if not message:
                return None
            if message.sender != SenderEnum.BOT:
                raise ValueError("Só é permitido dar feedback a mensagens do bot.")
            
            message.feedback = feedback
            db.commit()
            db.refresh(message)
            return message
        except SQLAlchemyError:
            db.rollback()
            raise
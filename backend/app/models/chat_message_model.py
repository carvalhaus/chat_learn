from sqlalchemy import Column, Integer, Text, ForeignKey, DateTime, Enum as SqlEnum
from sqlalchemy.orm import relationship
from app.database.base import Base
from app.core.constants.sender import SenderEnum
from datetime import datetime, timezone

class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("chat_sessions.id", ondelete="CASCADE"), nullable=False)

    sender = Column(SqlEnum(SenderEnum), nullable=False)
    message = Column(Text, nullable=False)
    external_user_id = Column(Integer, ForeignKey("external_users.id", ondelete="CASCADE"), nullable=False)

    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    session = relationship("ChatSession", back_populates="messages")
    external_user = relationship("ExternalUser", back_populates="chat_messages")

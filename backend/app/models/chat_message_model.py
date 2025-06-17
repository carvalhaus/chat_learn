from sqlalchemy import Column, Integer, Text, ForeignKey, DateTime, Enum as SqlEnum
from sqlalchemy.orm import relationship
from app.database.base import Base
from app.core.constants.sender import SenderEnum
from datetime import datetime, timezone

class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("chat_sessions.id"), nullable=False)

    sender = Column(SqlEnum(SenderEnum), nullable=False)
    message = Column(Text, nullable=False)

    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    session = relationship("ChatSession", back_populates="messages")

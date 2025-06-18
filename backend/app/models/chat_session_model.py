from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.database.base import Base
from datetime import datetime, timezone

class ChatSession(Base):
    __tablename__ = "chat_sessions"

    id = Column(Integer, primary_key=True, index=True)
    external_user_id = Column(
        Integer, 
        ForeignKey("external_users.id", ondelete="CASCADE"), 
        nullable=False
    )

    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    external_user = relationship("ExternalUser", back_populates="chat_sessions")
    messages = relationship("ChatMessage", back_populates="session", cascade="all, delete-orphan", passive_deletes=True)

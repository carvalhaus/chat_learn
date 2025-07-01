from sqlalchemy import Column, Integer, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from ..database.base import Base
from datetime import datetime, timezone

class ChatAnswer(Base):
    __tablename__ = "chat_answers"

    id = Column(Integer, primary_key=True, index=True)
    question_id = Column(
        Integer,
        ForeignKey("chat_questions.id", ondelete="CASCADE"),
        nullable=False
    )
    answer = Column(Text, nullable=False)

    question = relationship("ChatQuestion", back_populates="answers", foreign_keys=[question_id])

    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
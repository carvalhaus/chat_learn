from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.orm import relationship
from ..database.base import Base
from datetime import datetime, timezone

class ChatQuestion(Base):
    __tablename__ = "chat_questions"

    id = Column(Integer, primary_key=True, index=True)
    question = Column(Text, nullable=False)
    subject = Column(String(100), nullable=True)

    answers = relationship(
        "ChatAnswer",
        back_populates="question",
        cascade="all, delete-orphan",
        passive_deletes=True
    )

    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

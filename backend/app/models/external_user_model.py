from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, JSON, UniqueConstraint
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.database.base import Base


class ExternalUser(Base):
    __tablename__ = "external_users"

    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("clients.id", ondelete="CASCADE"), nullable=False)

    external_id = Column(String(255), nullable=False)  # Ex.: ID, CPF, email, username...

    name = Column(String(255), nullable=True)
    email = Column(String(255), nullable=True)

    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    client = relationship("Client", back_populates="external_users")
    chat_messages = relationship("ChatMessage", back_populates="external_user", cascade="all, delete-orphan")
    chat_sessions = relationship("ChatSession", back_populates="external_user", cascade="all, delete-orphan")

    __table_args__ = (
        UniqueConstraint('client_id', 'external_id', name='uq_client_external_id'),
    )

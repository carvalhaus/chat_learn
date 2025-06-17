from typing import List, Optional
from app.database.session import SessionLocal
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.chat_session_model import ChatSession
from app.repositories.chat_session_repository import ChatSessionRepository
from app.schemas.chat_session_schema import ChatSessionCreate, ChatSessionRead

class ChatSessionService:
    def __init__(self):
        self.db: Session = SessionLocal()
        self.repository = ChatSessionRepository()

    def create_session(self, session_create: ChatSessionCreate) -> ChatSessionRead:
        try:
            session = self.repository.create(self.db, session_create.dict())
            return ChatSessionRead.from_orm(session)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Failed to create session: {str(e)}"
            )

    def get_session(self, session_id: int) -> Optional[ChatSessionRead]:
        session = self.repository.get_by_id(self.db, session_id)
        if not session:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Session not found"
            )
        return ChatSessionRead.from_orm(session)

    def list_sessions(self) -> List[ChatSessionRead]:
        sessions = self.repository.list_all(self.db)
        return [ChatSessionRead.from_orm(s) for s in sessions]

    def delete_session(self, session_id: int) -> bool:
        deleted = self.repository.delete(self.db, session_id)
        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Session not found"
            )
        return True

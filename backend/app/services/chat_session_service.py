from typing import List, Optional
from app.database.session import SessionLocal
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.chat_session_model import ChatSession
from app.repositories.chat_session_repository import ChatSessionRepository
from app.repositories.external_user_repository import ExternalUserRepository
from app.schemas.chat_session_schema import ChatSessionCreate, ChatSessionRead

class ChatSessionService:
    def __init__(self):
        self.db: Session = SessionLocal()
        self.repository = ChatSessionRepository()
        self.external_user_repo = ExternalUserRepository()

    def create_session(self, session_create: ChatSessionCreate) -> ChatSessionRead:
        client_id = 1
        try:
            external_user = self.external_user_repo.get_by_client_and_external_id(
                db=self.db,
                client_id=client_id,
                external_id=session_create.external_id
            )

            if not external_user:
                external_user = self.external_user_repo.create(self.db, {
                    "client_id": client_id,
                    "external_id": session_create.external_id,
                    "name": session_create.name,
                    "email": session_create.email
                })

            session = self.repository.create(self.db, {
                "external_user_id": external_user.id
            })

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

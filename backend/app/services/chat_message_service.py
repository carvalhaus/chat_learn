from typing import List, Optional
from app.database.session import SessionLocal
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.chat_message_model import ChatMessage
from app.repositories.chat_message_repository import ChatMessageRepository
from app.schemas.chat_message_schema import ChatMessageCreate, ChatMessageRead
from app.repositories.chat_session_repository import ChatSessionRepository
from app.repositories.chat_question_repository import ChatQuestionRepository
from app.core.constants.sender import SenderEnum

class ChatMessageService:
    def __init__(self):
        self.db: Session = SessionLocal()
        self.repository = ChatMessageRepository()
        self.session_repository = ChatSessionRepository()
        self.chat_question_repository = ChatQuestionRepository()

    def create_message(self, message_create: ChatMessageCreate) -> ChatMessageRead:
        try:
            session = self.session_repository.get_by_id(self.db, message_create.session_id)
            if not session:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Session with ID {message_create.session_id} not found."
                )

            message = self.repository.create(self.db, message_create.dict())
            return ChatMessageRead.from_orm(message)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Failed to create message: {str(e)}"
            )

    def get_message(self, message_id: int) -> Optional[ChatMessageRead]:
        message = self.repository.get_by_id(self.db, message_id)
        if not message:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Message not found"
            )
        return ChatMessageRead.from_orm(message)

    def list_messages(self) -> List[ChatMessageRead]:
        messages = self.repository.list_all(self.db)
        return [ChatMessageRead.from_orm(m) for m in messages]

    def delete_message(self, message_id: int) -> bool:
        deleted = self.repository.delete(self.db, message_id)
        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Message not found"
            )
        return True
    
    def process_message(self, session_id: int, message_text: str):
        user_message = self.repository.create(self.db, {
            "session_id": session_id,
            "sender": SenderEnum(1),
            "message": message_text.message
        })

        question = self.chat_question_repository.find_best_match(self.db, message_text)

        if not question or not question.answers:
            bot_response = "Sorry, I don't have an answer for that."
        else:
            bot_response = question.answers[0].answer

        bot_message = self.repository.create(self.db, {
            "session_id": session_id,
            "sender": SenderEnum(2),
            "message": bot_response
        })

        return {
            "bot_message": ChatMessageRead.from_orm(bot_message),
        }

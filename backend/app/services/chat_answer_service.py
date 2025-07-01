from typing import List, Optional
from app.database.session import SessionLocal
from sqlalchemy.orm import Session
from app.repositories.chat_answer_repository import ChatAnswerRepository
from app.repositories.chat_question_repository import ChatQuestionRepository
from app.schemas.chat_answer_schema import ChatAnswerCreate, ChatAnswerRead, ChatAnswerUpdate
from app.models.chat_answer_model import ChatAnswer
from fastapi import HTTPException, status

class ChatAnswerService:
    def __init__(self):
        self.repository = ChatAnswerRepository()
        self.question_repository = ChatQuestionRepository()
        self.db: Session = SessionLocal()

    def create_answer(self, answer_create: ChatAnswerCreate) -> ChatAnswer:
        try:
            question = self.question_repository.get_by_id(self.db, answer_create.question_id)
            if not question:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Question with ID {answer_create.question_id} not found."
                )
            
            answer = self.repository.create(self.db, answer_create.dict())
            return ChatAnswerRead.from_orm(answer)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Failed to create answer: {str(e)}"
            )

    def get_answer(self, answer_id: int) -> ChatAnswer:
        answer = self.repository.get_by_id(self.db, answer_id)
        if not answer:
            raise HTTPException(status_code=404, detail="Answer not found!")
        return ChatAnswerRead.from_orm(answer)

    def list_answers(self) -> List[ChatAnswer]:
        return self.repository.list_all(self.db)

    def update_answer(self, answer_id: int, answer_update: ChatAnswerUpdate) -> Optional[ChatAnswer]:
        update_data = answer_update.dict(exclude_unset=True)

        updated_answer = self.repository.update(self.db, answer_id, update_data)

        if not updated_answer:
            raise HTTPException(status_code=404, detail="Answer not found!")
        
        return ChatAnswerRead.model_validate(updated_answer)

    def delete_answer(self, answer_id: int) -> bool:
        deleted = self.repository.delete(self.db, answer_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="Answer not found")
        return True

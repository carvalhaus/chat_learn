from typing import List, Optional
from app.database.session import SessionLocal
from sqlalchemy.orm import Session
from app.repositories.chat_question_repository import ChatQuestionRepository
from app.repositories.chat_answer_repository import ChatAnswerRepository
from app.schemas.chat_question_schema import ChatQuestionCreate, ChatQuestionUpdate, ChatQuestionRead, QuestionWithAnswerCreate
from app.schemas.chat_answer_schema import ChatAnswerRead
from app.models.chat_question_model import ChatQuestion
from fastapi import HTTPException, status

class ChatQuestionService:
    def __init__(self):
        self.repository = ChatQuestionRepository()
        self.answer_repository = ChatAnswerRepository()
        self.db: Session = SessionLocal()

    def create_question(self, question_create: ChatQuestionCreate) -> ChatQuestion:
        try:
            question = self.repository.create(self.db, question_create.dict())
            return ChatQuestionRead.from_orm(question)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Failed to create question: {str(e)}"
            )

    def get_question(self, question_id: int) -> ChatQuestion:
        question = self.repository.get_by_id(self.db, question_id)
        if not question:
            raise HTTPException(status_code=404, detail="Question not found!")
        return ChatQuestionRead.from_orm(question)

    def list_questions(self) -> List[ChatQuestion]:
        return self.repository.list_all(self.db)

    def update_question(self, question_id: int, question_update: ChatQuestionUpdate) -> Optional[ChatQuestion]:
        update_data = question_update.dict(exclude_unset=True)

        updated_question = self.repository.update(self.db, question_id, update_data)

        if not updated_question:
            raise HTTPException(status_code=404, detail="Question not found!")
        
        return ChatQuestionRead.model_validate(updated_question)

    def delete_question(self, question_id: int) -> bool:
        deleted = self.repository.delete(self.db, question_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="Question not found")
        return True

    def create_question_with_answer(self, data: QuestionWithAnswerCreate):
        try:
            question = self.repository.create(self.db, {"question": data.question, "subject": data.question})
            answer = self.answer_repository.create(self.db, {"question_id": question.id, "answer": data.answer})
            return {
                "question": ChatQuestionRead.from_orm(question),
                "answer": ChatAnswerRead.from_orm(answer)
            }
        except Exception as e:
            self.db.rollback()
            raise HTTPException(status_code=400, detail=f"Failed to create question with answer: {str(e)}")

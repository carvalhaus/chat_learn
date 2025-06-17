from typing import List, Optional
from app.schemas.chat_question_schema import ChatQuestionCreate, ChatQuestionRead, ChatQuestionUpdate, QuestionWithAnswerCreate
from app.services.chat_question_service import ChatQuestionService

class ChatQuestionController:
    def __init__(self):
        self.service = ChatQuestionService()

    def create_question(self, question_create: ChatQuestionCreate) -> ChatQuestionRead:
        return self.service.create_question(question_create)

    def get_question(self, question_id: int) -> Optional[ChatQuestionRead]:
        return self.service.get_question(question_id)

    def list_questions(self) -> List[ChatQuestionRead]:
        return self.service.list_questions()

    def update_question(self, question_id: int, question_update: ChatQuestionUpdate) -> Optional[ChatQuestionRead]:
        return self.service.update_question(question_id, question_update)

    def delete_question(self, question_id: int) -> bool:
        return self.service.delete_question(question_id)

    def create_question_with_answer(self, data: QuestionWithAnswerCreate):
        return self.service.create_question_with_answer(data)
from typing import List, Optional
from app.schemas.chat_answer_schema import ChatAnswerCreate, ChatAnswerRead, ChatAnswerUpdate
from app.services.chat_answer_service import ChatAnswerService

class ChatAnswerController:
    def __init__(self):
        self.service = ChatAnswerService()

    def create_answer(self, answer_create: ChatAnswerCreate) -> ChatAnswerRead:
        return self.service.create_answer(answer_create)

    def get_answer(self, answer_id: int) -> Optional[ChatAnswerRead]:
        return self.service.get_answer(answer_id)

    def list_answers(self) -> List[ChatAnswerRead]:
        return self.service.list_answers()

    def update_answer(self, answer_id: int, answer_update: ChatAnswerUpdate) -> Optional[ChatAnswerRead]:
        return self.service.update_answer(answer_id, answer_update)

    def delete_answer(self, answer_id: int) -> bool:
        return self.service.delete_answer(answer_id)

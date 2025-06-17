from typing import List, Optional
from app.schemas.chat_session_schema import ChatSessionCreate, ChatSessionRead
from app.schemas.chat_message_schema import ChatMessageCreate
from app.services.chat_session_service import ChatSessionService
from app.services.chat_message_service import ChatMessageService

class ChatController:
    def __init__(self):
        self.service = ChatSessionService()
        self.chat_message_service = ChatMessageService()

    def create_session(self, session_create: ChatSessionCreate) -> ChatSessionRead:
        return self.service.create_session(session_create)

    def get_session(self, session_id: int) -> Optional[ChatSessionRead]:
        return self.service.get_session(session_id)

    def list_sessions(self) -> List[ChatSessionRead]:
        return self.service.list_sessions()

    def delete_session(self, session_id: int) -> bool:
        return self.service.delete_session(session_id)
    
    def process_message(self, session_id: int, message: ChatMessageCreate):
        return self.chat_message_service.process_message(session_id, message)

from fastapi import APIRouter, Depends
from typing import List
from app.schemas.chat_session_schema import ChatSessionCreate, ChatSessionRead, ChatSessionWithUserResponse
from app.schemas.chat_message_schema import ChatMessageCreate, ChatProcessResponse, ChatMessageFeedbackUpdate
from app.schemas.client_schema import ClientRead
from app.schemas.chat_message_schema import ChatMessageFeedbackUpdate
from app.controllers.chat_controller import ChatController
from app.middleware.permissions import clients_only

router = APIRouter(
    prefix="/chat",
    tags=["Chat"]
)
chat_controller = ChatController()

@router.post("/sessions", response_model=ChatSessionWithUserResponse)
def create_session(session_create: ChatSessionCreate, client: ClientRead = Depends(clients_only)):
    return chat_controller.create_session(session_create, client_id=client.id)

@router.get("/sessions", response_model=List[ChatSessionRead])
def list_sessions():
    return chat_controller.list_sessions()

@router.delete("/sessions/{session_id}")
def delete_session(session_id: int):
    chat_controller.delete_session(session_id)
    return {"message": "Session deleted successfully"}

@router.post("/sessions/{session_id}/process", response_model=ChatProcessResponse)
def process_message(
    session_id: int,
    message_create: ChatMessageCreate,
    _: str = Depends(clients_only)
):
    return chat_controller.process_message(session_id, message_create)

@router.get("/sessions/{session_id}", response_model=ChatSessionRead)
def get_session(session_id: int):
    return chat_controller.get_session(session_id)

@router.patch("/sessions/{session_id}/message-feedback/{message_id}", response_model=ChatMessageFeedbackUpdate)
def update_feedback(session_id: int, message_id: int, feedback: ChatMessageFeedbackUpdate, _: str = Depends(clients_only)):
    feedback = chat_controller.update_feedback(message_id, feedback)
    return feedback

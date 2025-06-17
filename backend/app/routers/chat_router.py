from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.schemas.chat_session_schema import ChatSessionCreate, ChatSessionRead
from app.schemas.chat_message_schema import ChatMessageCreate, ChatMessageRead, ChatProcessResponse
from app.controllers.chat_controller import ChatController

router = APIRouter(
    prefix="/chat",
    tags=["Chat"]
)
chat_controller = ChatController()

@router.post("/sessions", response_model=ChatSessionRead)
def create_session(session_create: ChatSessionCreate):
    return chat_controller.create_session(session_create)

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
    message_create: ChatMessageCreate
):
    return chat_controller.process_message(session_id, message_create)

@router.get("/sessions/{session_id}", response_model=ChatSessionRead)
def get_session(session_id: int):
    return chat_controller.get_session(session_id)

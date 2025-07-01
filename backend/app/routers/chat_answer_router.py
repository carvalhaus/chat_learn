from fastapi import APIRouter, HTTPException, status, Depends
from typing import List
from app.schemas.chat_answer_schema import ChatAnswerRead, ChatAnswerCreate, ChatAnswerUpdate
from app.controllers.chat_answer_controller import ChatAnswerController
from app.schemas.message_schema import MessageResponse
from app.middleware.permissions import user_only

router = APIRouter(prefix="/answers", tags=["Answers"], dependencies=[Depends(user_only)])
answer_controller = ChatAnswerController()

@router.post("/", response_model=ChatAnswerRead)
def create_answer(answer_create: ChatAnswerCreate):
    return answer_controller.create_answer(answer_create)

@router.get("/{answer_id}", response_model=ChatAnswerRead)
def get_answer(answer_id: int):
    answer = answer_controller.get_answer(answer_id)
    return answer

@router.get("/", response_model=List[ChatAnswerRead])
def list_answers():
    return answer_controller.list_answers()

@router.patch("/{answer_id}", response_model=ChatAnswerRead)
def update_answer(answer_id: int, answer_update: ChatAnswerUpdate):
    answer = answer_controller.update_answer(answer_id, answer_update)
    return answer

@router.delete("/{answer_id}", response_model=MessageResponse)
def delete_answer(answer_id: int):
    answer_controller.delete_answer(answer_id)
    return {"message": "Answer deleted successfully!"}

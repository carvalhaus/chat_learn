from fastapi import APIRouter, Depends
from typing import List
from app.schemas.chat_question_schema import ChatQuestionRead, ChatQuestionCreate, ChatQuestionUpdate, QuestionWithAnswerCreate
from app.controllers.chat_question_controller import ChatQuestionController
from app.schemas.message_schema import MessageResponse
from app.middleware.permissions import user_only

router = APIRouter(prefix="/questions", tags=["Questions"], dependencies=[Depends(user_only)])
question_controller = ChatQuestionController()

@router.post("/", response_model=ChatQuestionRead)
def create_question(question_create: ChatQuestionCreate):
    return question_controller.create_question(question_create)

@router.post("/with-answer")
def create_question_with_answer(data: QuestionWithAnswerCreate):
    return question_controller.create_question_with_answer(data)

@router.get("/{question_id}", response_model=ChatQuestionRead)
def get_question(question_id: int):
    question = question_controller.get_question(question_id)
    return question

@router.get("/", response_model=List[ChatQuestionRead])
def list_questions():
    return question_controller.list_questions()

@router.patch("/{question_id}", response_model=ChatQuestionRead)
def update_question(question_id: int, question_update: ChatQuestionUpdate):
    question = question_controller.update_question(question_id, question_update)
    return question

@router.delete("/{question_id}", response_model=MessageResponse)
def delete_question(question_id: int):
    question_controller.delete_question(question_id)
    return {"message": "Question deleted successfully!"}

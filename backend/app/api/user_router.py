from fastapi import APIRouter, HTTPException
from typing import List
from app.schemas.user_schema import UserRead, UserCreate, UserUpdate
from app.controllers.user_controller import UserController

router = APIRouter(prefix="/users", tags=["users"])
user_controller = UserController()

@router.post("/", response_model=UserRead)
def create_user(user_create: UserCreate):
    return user_controller.create_user(user_create)

@router.get("/{user_id}", response_model=UserRead)
def get_user(user_id: int):
    user = user_controller.get_user(user_id)
    return user

@router.get("/", response_model=List[UserRead])
def list_users():
    return user_controller.list_users()

@router.patch("/{user_id}", response_model=UserRead)
def update_user(user_id: int, user_update: UserUpdate):
    user = user_controller.update_user(user_id, user_update)
    return user

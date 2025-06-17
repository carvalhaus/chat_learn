from fastapi import APIRouter, HTTPException, status, Depends
from typing import List
from app.schemas.user_schema import UserRead, UserCreate, UserUpdate
from app.controllers.user_controller import UserController
from app.schemas.message_schema import MessageResponse
from app.middleware.permissions import admin_only

router = APIRouter(prefix="/users", tags=["Users"], dependencies=[Depends(admin_only)])
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

@router.delete("/{user_id}", response_model=MessageResponse)
def delete_user(user_id: int):
    user_controller.delete_user(user_id)
    return {"message": "User deleted successfully!"}
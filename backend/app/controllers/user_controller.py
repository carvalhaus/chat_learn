from typing import List, Optional
from app.schemas.user_schema import UserCreate, UserRead, UserUpdate
from app.services.user_service import UserService

class UserController:
    def __init__(self):
        self.service = UserService()

    def create_user(self, user_create: UserCreate) -> UserRead:
        return self.service.create_user(user_create)

    def get_user(self, user_id: int) -> Optional[UserRead]:
        return self.service.get_user(user_id)

    def list_users(self) -> List[UserRead]:
        return self.service.list_users()
    
    def update_user(self, user_id: int, user_update: UserUpdate) -> Optional[UserRead]:
        return self.service.update_user(user_id, user_update)
    
    def delete_user(self, user_id: int) -> bool:
        return self.service.delete_user(user_id)

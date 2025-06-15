from typing import List, Optional
from app.schemas.user_schema import UserCreate, UserRead, UserUpdate
from app.repositories.user_repository import UserRepository
from app.database.session import SessionLocal
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserService:
    def __init__(self):
        self.repository = UserRepository()
        self.db: Session = SessionLocal()

    def hash_password(self, password: str) -> str:
        return pwd_context.hash(password)

    def create_user(self, user_create: UserCreate) -> UserRead:
        try:
            hashed_password = self.hash_password(user_create.password)
            user_dict = user_create.dict()
            user_dict.pop("password")
            user_dict["hashed_password"] = hashed_password

            user = self.repository.create(self.db, user_dict)
            return UserRead.model_validate(user)
        except IntegrityError:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email or CPF already registered."
            )
        except Exception as e:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Unexpected error: {str(e)}"
            )

    def get_user(self, user_id: int) -> Optional[UserRead]:
        user = self.repository.get_by_id(self.db, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found!")
        return UserRead.from_orm(user)

    def list_users(self) -> List[UserRead]:
        users = self.repository.list_all(self.db)
        return [UserRead.from_orm(u) for u in users]
    
    def update_user(self, user_id: int, user_update: UserUpdate) -> Optional[UserRead]:

        update_data = user_update.dict(exclude_unset=True)

        updated_user = self.repository.update(self.db, user_id, update_data)

        if not updated_user:
            raise HTTPException(status_code=404, detail="User not found!")

        return UserRead.model_validate(updated_user)

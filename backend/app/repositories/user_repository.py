from app.models.user_model import User
from .base_repository import BaseRepository
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

class UserRepository(BaseRepository):
    def __init__(self):
        super().__init__(User)

    def get_by_email(self, db: Session, email: str) -> User | None:
        try:
            return db.query(User).filter(User.email == email).first()
        except SQLAlchemyError:
            db.rollback()
            raise

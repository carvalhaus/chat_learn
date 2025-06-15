from sqlalchemy.orm import Session
from app.models.user_model import User
from sqlalchemy.exc import SQLAlchemyError

class UserRepository:
    def get_by_id(self, db: Session, user_id: int) -> User | None:
        try:
            return db.query(User).filter(User.id == user_id).first()
        except SQLAlchemyError as e:
            db.rollback()
        raise e 

    def list_all(self, db: Session):
        return db.query(User).all()

    def create(self, db: Session, user_data: dict) -> User:
        user = User(**user_data)
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    
    def update(self, db: Session, user_id: int, update_data: dict) -> User | None:
        user = self.get_by_id(db, user_id)
        
        if not user:
            return None

        for key, value in update_data.items():
            setattr(user, key, value)

        db.commit()
        db.refresh(user)
        return user

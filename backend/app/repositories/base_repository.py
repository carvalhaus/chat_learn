from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

class BaseRepository:
    model = None

    def __init__(self, model):
        self.model = model

    def get_by_id(self, db: Session, id: int):
        try:
            return db.query(self.model).filter(self.model.id == id).first()
        except SQLAlchemyError:
            db.rollback()
            raise

    def list_all(self, db: Session):
        try:
            return db.query(self.model).all()
        except SQLAlchemyError:
            db.rollback()
            raise

    def create(self, db: Session, obj_data: dict):
        try:
            obj = self.model(**obj_data)
            db.add(obj)
            db.commit()
            db.refresh(obj)
            db.expire_all()
            return obj
        except SQLAlchemyError:
            db.rollback()
            raise

    def update(self, db: Session, id: int, update_data: dict):
        try:
            obj = self.get_by_id(db, id)
            if not obj:
                return None
            for key, value in update_data.items():
                setattr(obj, key, value)
            db.commit()
            db.refresh(obj)
            db.expire_all()
            return obj
        except SQLAlchemyError:
            db.rollback()
            raise

    def delete(self, db: Session, id: int) -> bool:
        try:
            obj = self.get_by_id(db, id)
            if not obj:
                return False
            db.delete(obj)
            db.commit()
            db.expire_all()
            return True
        except SQLAlchemyError:
            db.rollback()
            raise

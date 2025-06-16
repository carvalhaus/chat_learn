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
        return db.query(self.model).all()

    def create(self, db: Session, obj_data: dict):
        obj = self.model(**obj_data)
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj

    def update(self, db: Session, id: int, update_data: dict):
        obj = self.get_by_id(db, id)
        if not obj:
            return None
        for key, value in update_data.items():
            setattr(obj, key, value)
        db.commit()
        db.refresh(obj)
        return obj

    def delete(self, db: Session, id: int) -> bool:
        obj = self.get_by_id(db, id)
        if not obj:
            return False
        db.delete(obj)
        db.commit()
        return True

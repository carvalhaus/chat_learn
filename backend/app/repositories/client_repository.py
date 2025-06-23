from app.models.client_model import Client
from .base_repository import BaseRepository
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from typing import Optional

class ClientRepository(BaseRepository):
    def __init__(self):
        super().__init__(Client)

    def get_by_slug(self, db, slug: str):
        return db.query(self.model).filter(self.model.slug == slug).first()

    def get_by_name(self, db, name: str):
        return db.query(self.model).filter(self.model.name == name).first()
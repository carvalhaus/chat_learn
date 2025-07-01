from sqlalchemy.orm import Session
from app.models.external_user_model import ExternalUser
from app.repositories.base_repository import BaseRepository


class ExternalUserRepository(BaseRepository):
    def __init__(self):
        super().__init__(ExternalUser)

    def get_by_client_and_external_id(self, db: Session, client_id: int, external_id: str) -> ExternalUser | None:
        try:
            return db.query(self.model).filter(
                self.model.client_id == client_id,
                self.model.external_id == external_id
            ).first()
        except Exception:
            db.rollback()
            raise

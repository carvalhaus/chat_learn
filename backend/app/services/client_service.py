from app.schemas.client_schema import ClientCreate, ClientRead, ClientUpdate
from app.repositories.client_repository import ClientRepository
from app.database.session import SessionLocal
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class ClientService:
    def __init__(self):
        self.repository = ClientRepository()
        self.db: Session = SessionLocal()

    def generate_api_key(self, client_id: int, client_is_active: bool) -> str:
        from app.auth.auth_client_handler import create_client_access_token
        token = create_client_access_token(
            data={"sub": str(client_id),"is_active": client_is_active}
        )
        return token

    def create_client(self, client_create: ClientCreate) -> ClientRead:
        existing_slug = self.repository.get_by_slug(self.db, client_create.slug)
        if existing_slug:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Client with this slug already exists.",
            )

        existing_name = self.repository.get_by_name(self.db, client_create.name)
        if existing_name:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Client with this name already exists.",
            )

        client = self.repository.create(
            self.db,
            {
                "name": client_create.name,
                "slug": client_create.slug,
                "is_active": client_create.is_active,
            }
        )

        api_key = self.generate_api_key(client.id, client.is_active)
        client = self.repository.update(self.db, client.id, {"api_key": api_key})

        return client

    def get_by_id(self, client_id: int):
        client = self.repository.get_by_id(self.db, client_id)
        if not client:
            raise HTTPException(status_code=404, detail="Client not found")
        return client

    def list(self):
        return self.repository.list_all(self.db)

    def update(self, client_id: int, client_data: ClientUpdate):
        client = self.get_by_id(client_id)

        if client_data.slug:
            existing_slug = self.repository.get_by_slug(self.db, client_data.slug)
            if existing_slug and existing_slug.id != client_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Slug is already in use by another client.",
                )

        if client_data.name:
            existing_name = self.repository.get_by_name(self.db, client_data.name)
            if existing_name and existing_name.id != client_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Name is already in use by another client.",
                )

        data = client_data.dict(exclude_unset=True)
        
        if "is_active" in data:
            if data["is_active"] is False:
                data["api_key"] = None
            elif data["is_active"] is True and not client.api_key:
                api_key = self.generate_api_key(client_id, client_is_active=True)
                data["api_key"] = api_key

        updated_client = self.repository.update(self.db, client_id, data)
        
        return ClientRead.model_validate(updated_client)

    def delete(self, client_id: int):
        success = self.repository.delete(self.db, client_id)
        if not success:
            raise HTTPException(status_code=404, detail="Client not found")
        return True

    def regenerate_api_key(self, client_id: int):
        client = self.get_by_id(client_id)

        api_key = self.generate_api_key(client.id, client.is_active)
        client = self.repository.update(self.db, client.id, {"api_key": api_key})

        return client

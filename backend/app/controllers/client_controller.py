from fastapi import HTTPException
from app.schemas.client_schema import ClientCreate, ClientUpdate
from app.services.client_service import ClientService


class ClientController:
    def __init__(self):
        self.service = ClientService()

    def create(self, client_data: ClientCreate):
        try:
            return self.service.create_client(client_data)
        except HTTPException as e:
            raise e

    def get_by_id(self, client_id: int):
        try:
            return self.service.get_by_id(client_id)
        except HTTPException as e:
            raise e

    def list(self):
        return self.service.list()

    def update(self, client_id: int, client_data: ClientUpdate):
        try:
            return self.service.update(client_id, client_data)
        except HTTPException as e:
            raise e

    def delete(self, client_id: int):
        try:
            return self.service.delete(client_id)
        except HTTPException as e:
            raise e

    def regenerate_api_key(self, client_id: int):
        try:
            return self.service.regenerate_api_key(client_id)
        except HTTPException as e:
            raise e

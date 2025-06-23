from fastapi import APIRouter, status
from typing import List
from app.schemas.client_schema import ClientCreate, ClientRead, ClientUpdate
from app.controllers.client_controller import ClientController
from app.schemas.message_schema import MessageResponse

router = APIRouter(prefix="/clients", tags=["Clients"])
controller = ClientController()


@router.post(
    "/",
    response_model=ClientRead,
    status_code=status.HTTP_201_CREATED
)
def create_client(client_data: ClientCreate):
    return controller.create(client_data)


@router.get(
    "/",
    response_model=List[ClientRead],
    status_code=status.HTTP_200_OK
)
def list_clients():
    return controller.list()


@router.get(
    "/{client_id}",
    response_model=ClientRead,
    status_code=status.HTTP_200_OK
)
def get_client(client_id: int, ):
    return controller.get_by_id(client_id)


@router.patch(
    "/{client_id}",
    response_model=ClientRead,
    status_code=status.HTTP_200_OK
)
def update_client(client_id: int, client_data: ClientUpdate, ):
    return controller.update(client_id, client_data)


@router.delete(
    "/{client_id}",
    status_code=status.HTTP_200_OK,
    response_model=MessageResponse
)
def delete_client(client_id: int):
    controller.delete(client_id)
    return {"message": "Client deleted successfully!"}


@router.post(
    "/{client_id}/regenerate-api-key",
    response_model=ClientRead,
    status_code=status.HTTP_200_OK
)
def regenerate_api_key(client_id: int, ):
    return controller.regenerate_api_key(client_id)

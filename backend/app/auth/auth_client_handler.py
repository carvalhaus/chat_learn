from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import jwt, JWTError
from fastapi import HTTPException, status
from app.schemas.token_schema import TokenClientData
from app.services.client_service import ClientService
from app.core.config import settings 

def create_client_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(days=365)

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

    return encoded_jwt

def verify_client_token(token: str):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        client_id: str = payload.get("sub")

        if client_id is None:
            raise credentials_exception

        token_data = TokenClientData(client_id=int(client_id))

    except JWTError:
        raise credentials_exception

    client = ClientService().get_by_id(token_data.client_id)

    if client is None:
        raise credentials_exception

    return client

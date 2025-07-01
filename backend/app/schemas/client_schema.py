from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ClientBase(BaseModel):
    name: str
    slug: str
    is_active: Optional[bool] = True

class ClientCreate(ClientBase):
    pass


class ClientUpdate(BaseModel):
    name: Optional[str] = None
    slug: Optional[str] = None
    is_active: Optional[bool] = None


class ClientRead(ClientBase):
    id: int
    api_key: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
from typing import Optional
from datetime import datetime
from pydantic import BaseModel

class ExternalUserBase(BaseModel):
    client_id: int
    external_id: str
    name: Optional[str] = None
    email: Optional[str] = None

class ExternalUserCreate(ExternalUserBase):
    pass

class ExternalUserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None

class ExternalUserRead(ExternalUserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

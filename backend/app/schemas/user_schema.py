from pydantic import BaseModel, EmailStr, constr
from datetime import date
from typing import Optional

class UserBase(BaseModel):
    name: str
    email: EmailStr
    cpf: constr(min_length=11, max_length=14) 
    gender: str
    phone: str
    birth_date: date

class UserCreate(UserBase):
    password: str

class UserRead(UserBase):
    id: int

    class Config:
        from_attributes = True

class UserUpdate(BaseModel):
    name: Optional[str] = None
    gender: Optional[str] = None
    phone: Optional[str] = None
    birth_date: Optional[date] = None

    class Config:
        from_attributes = True 

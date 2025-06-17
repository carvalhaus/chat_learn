from pydantic import BaseModel, EmailStr, constr
from datetime import date
from typing import Optional
from ..core.constants.perfil import PerfilEnum
from ..core.constants.gender import GenderEnum

class UserBase(BaseModel):
    name: str
    email: EmailStr
    cpf: constr(min_length=11, max_length=14) 
    gender: GenderEnum
    phone: str
    birth_date: date
    perfil: PerfilEnum = PerfilEnum.USER

class UserCreate(UserBase):
    password: str

class UserRead(UserBase):
    id: int

    class Config:
        from_attributes = True

class UserUpdate(BaseModel):
    name: Optional[str] = None
    gender: Optional[GenderEnum] = None
    phone: Optional[str] = None
    birth_date: Optional[date] = None
    perfil: Optional[PerfilEnum] = None

    class Config:
        from_attributes = True 

class UserEmail(BaseModel):
    id: int
    email: EmailStr
    hashed_password: str
    perfil: PerfilEnum

    class Config:
        from_attributes = True 
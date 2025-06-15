from sqlalchemy.orm import Session
from .session import engine, SessionLocal
from .base import Base
from ..models.user_model import User
from ..services.user_service import UserService
from ..schemas.user_schema import UserCreate

def create_tables():
    Base.metadata.create_all(bind=engine)
    print("✅ Tabelas criadas com sucesso.")

def seed_users():
    db = SessionLocal()
    user_service = UserService()
    db_users = user_service.list_users()
    
    if db_users:
        print("Usuários já existem. Seed ignorado.")
        return

    users = [
        {
            "name": "Admin",
            "email": "admin@example.com",
            "cpf": "12345678901",
            "password": "admin123",
            "gender": "M",
            "phone": "51999999999",
            "birth_date": "1990-01-01"
        },
        {
            "name": "Usuário Teste",
            "email": "user@example.com",
            "cpf": "98765432100",
            "password": "user123",
            "gender": "F",
            "phone": "51988888888",
            "birth_date": "1992-05-15"
        },
    ]

    for u in users:
        user_create = UserCreate(**u)
        user_service.create_user(user_create)

    print("Seed de usuários realizado com sucesso!")

def init_db():
    create_tables()
    seed_users()
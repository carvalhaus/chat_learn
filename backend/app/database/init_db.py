from sqlalchemy.orm import Session
from sqlalchemy import inspect
from .session import engine, SessionLocal
from .base import Base
from ..services.user_service import UserService
from ..schemas.user_schema import UserCreate

def create_tables():
    inspector = inspect(engine)
    existing_tables = inspector.get_table_names()

    Base.metadata.create_all(bind=engine)

    for table in Base.metadata.tables.keys():
        if table in existing_tables:
            print(f"⚠️ Table '{table}' already exist.")
        else:
            print(f"✅ Table '{table}' created successfully")

def seed_users():
    db = SessionLocal()
    user_service = UserService()
    db_users = user_service.list_users()
    
    if db_users:
        print("⚠️ Users already exist. Seed ignored.")
        return

    users = [
        {
            "name": "Admin",
            "email": "admin@example.com",
            "cpf": "12345678901",
            "password": "admin123",
            "gender": 1,
            "phone": "51999999999",
            "birth_date": "1990-01-01",
            "perfil": 1
        },
        {
            "name": "Usuário Teste",
            "email": "user@example.com",
            "cpf": "98765432100",
            "password": "user123",
            "gender": 2,
            "phone": "51988888888",
            "birth_date": "1992-05-15",
            "perfil": 2
        },
    ]

    for u in users:
        user_create = UserCreate(**u)
        user_service.create_user(user_create)

    print("✅ User seeding successfully completed!")

def init_db():
    create_tables()
    seed_users()